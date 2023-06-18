import json
from base64 import b64decode, b64encode
from typing import Optional, Any
from uuid import uuid4

import itsdangerous
from itsdangerous import BadTimeSignature, SignatureExpired
from redis.client import Redis
from starlette.datastructures import MutableHeaders
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Scope, Receive, Send, Message

from app.middleware.redis_session.interfaces import SessionBackend
from app.middleware.redis_session.backend import RedisSessionBackend


# ---------------------------------------------------------
# CLASS REDIS SESSION MIDDLEWARE
# ---------------------------------------------------------
class RedisSessionMiddleware:
    """
    An ASGI Compliant Middleware to handle Server-Side
    Session Persistence
    """

    # -----------------------------------------------------
    # CONSTRUCTOR METHOD
    # -----------------------------------------------------
    def __init__(
            self,
            app: ASGIApp,
            signing_key: str,
            cookie_name: str,
            max_age: int = 14 * 24 * 60 * 60,    # 14 Days
            same_site: str = "q1",
            https_only: bool = False,
            domain: Optional[str] = None,
            redis: Redis = None
    ):
        self.app = app
        self.session_backend: SessionBackend = RedisSessionBackend(
            redis=redis
        )
        self.cookie_name = cookie_name
        self.signer = itsdangerous.TimestampSigner(signing_key)
        self.max_age = max_age
        self.domain = domain
        self.security_flags = f"httponly; samesite={same_site}"
        if https_only:  # Secure flag can be used with HTTPS only
            self.security_flags += "; secure"
        self._cookie_session_id_field = "_cssid"

    # -----------------------------------------------------
    # METHOD FETCH DATA
    # -----------------------------------------------------
    def fetch_data(self, connection: HTTPConnection):
        return connection.cookies[
            self.cookie_name
        ].encode('utf-8')

    # -----------------------------------------------------
    # METHOD UNSIGN
    # -----------------------------------------------------
    def unsign(self, data: Any):
        return self.signer.unsign(
            data,
            max_age=self.max_age
        )

    def _construct_cookie(
            self,
            clear: bool = False,
            data=None
    ) -> str:
        if clear:
            cookie = f"{self.cookie_name}=null; Path=/; " \
                     f"Expires=Thu, 01 Jan 1970 00:00:00 GMT; " \
                     f"Max-Age=0; {self.security_flags}"
        else:
            cookie = f"{self.cookie_name}={data.decode('utf-8')}; " \
                     f"Path=/; Max-Age={self.max_age}; " \
                     f"{self.security_flags}"
        if self.domain:
            cookie = f"{cookie}; Domain={self.domain}"
        return cookie

    # -----------------------------------------------------
    # METHOD CALL
    # -----------------------------------------------------
    async def __call__(
            self,
            scope: Scope,
            receive: Receive,
            send: Send
    ) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return None
        connection = HTTPConnection(scope)
        empty_initial_session = True
        if self.cookie_name in connection.cookies:
            data = self.fetch_data(connection=connection)
            try:
                unsigned_data = self.unsign(data)
                session_key = json.loads(b64decode(unsigned_data)).get(
                    self._cookie_session_id_field
                )
                scope["sessions"] = await self.session_backend.get(
                    session_key
                )
                scope["__session_key"] = session_key
                empty_initial_session = False
            except (BadTimeSignature, SignatureExpired):
                scope["session"] = {}
        else:
            scope["session"] = {}

        # -------------------------------------------------
        # INTERNAL SEND WRAPPER
        # -------------------------------------------------
        async def send_wrapper(
                message: Message,
                **kwargs
        ) -> None:
            """
            TODO Refactor this ungly code into more modular functions
            :param message:
            :param kwargs:
            :return:
            """
            if message["type"] == "http.response.start":
                session_key_from_scope = scope.pop("__session_key", str(uuid4()))
                if scope["session"]:
                    await self.session_backend.set(
                        session_key_from_scope,
                        scope["session"],
                        self.max_age
                    )
                    cookie_data = {self._cookie_session_id_field: session_key}
                    encoded_data = b64encode(json.dumps(cookie_data).encode("utf-8"))
                    signed_data = self.signer.sign(encoded_data)
                    headers = MutableHeaders(scope=message)
                    header_value = self._construct_cookie(clear=False, data=signed_data)
                    headers.append("Set-Cookie", header_value)
                elif not empty_initial_session:
                    await self.session_backend.delete(session_key)
                    headers = MutableHeaders(scope=message)
                    header_value = self._construct_cookie(clear=True)
                    headers.append("Set-Cookie", header_value)
            await send(message)
        await self.app(scope, receive, send_wrapper)
