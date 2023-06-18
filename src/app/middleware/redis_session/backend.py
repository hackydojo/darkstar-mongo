from typing import Optional, Any
from functools import partial
from redis.client import Redis
from pickle import HIGHEST_PROTOCOL, dumps, loads

from app.middleware.redis_session.interfaces import SessionBackend


# ---------------------------------------------------------
# REDIS SESSION BACKEND
# ---------------------------------------------------------
class RedisSessionBackend(SessionBackend):
    def __init__(self, redis: Redis):
        self.redis: Redis = redis
        self._dumps = partial(dumps, protocol=HIGHEST_PROTOCOL)
        self._loads = partial(loads)

    # -----------------------------------------------------
    # METHOD SET
    # -----------------------------------------------------
    async def set(
        self,
        key: str,
        value: dict,
        exp: Optional[int],
        **kwargs: dict,
    ) -> Optional[str]:
        value = self.redis.set(name=key, value=self._dumps(value), ex=exp, **kwargs)
        return value if value is not None else None

    # -----------------------------------------------------
    # METHOD DELETE
    # -----------------------------------------------------
    async def delete(
        self,
        key: str,
        **kwargs: dict,
    ) -> Any:
        return self.redis.delete(key)

    # -----------------------------------------------------
    # METHOD GET
    # -----------------------------------------------------
    async def get(self, key: str) -> Optional[dict]:
        value = self.redis.get(name=key)
        return self._loads(value) if value is not None else None
