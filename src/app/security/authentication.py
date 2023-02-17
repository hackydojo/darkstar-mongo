import datetime
from abc import ABCMeta, abstractmethod

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status

from app.business_objects.user import Users, UserSession, User
from app.security import IdentityCredential
from app.security.cryptography import Password
from app.context import get_context, ServerContext
from app.business_objects.user import inject_users

from jose import jwt, JWTError

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"/api/{get_context().api_version}/auth/token"
)


# ---------------------------------------------------------
# CLASS TOKEN EXPIRATION PROVIDER
# ---------------------------------------------------------
class TokenExpirationProvider:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_expiration_time(self):
        raise NotImplementedError()


# ---------------------------------------------------------
# CLASS INTERNAL TOKEN EXPIRATION PROVIDER
# ---------------------------------------------------------
class InternalTokenExpirationProvider(TokenExpirationProvider):
    # -----------------------------------------------------
    # CONSTRUCTOR METHOD
    # -----------------------------------------------------
    def __init__(self, server_context: ServerContext = get_context()):
        """
        Creates instances of al internal token expiration
        provider
        :param server_context: The server context to access
        token settings
        """
        self.context: ServerContext = server_context

    # -----------------------------------------------------
    # METHOD GET EXPIRATION TIME
    # -----------------------------------------------------
    def get_expiration_time(self):
        """
        Computes the expiration time based on current local
        time by adding the defined time delta in minutes that
        is configures in the server context.
        :return:  Unix time when the token will expire
        """
        return datetime.datetime.now() + datetime.timedelta(
            minutes=self.context.jwt_token_duration
        )


# ---------------------------------------------------------
# CLASS USER AUTHENTICATION
# ---------------------------------------------------------
class UserAuthentication:
    """
    A user authentication is the process of determining if a
    given set of credentials are valid for a particular user.
    This class can be extended to support other authentication
    schemas.
    """

    # -----------------------------------------------------
    # CONSTRUCTOR METHOD
    # -----------------------------------------------------
    def __init__(
        self,
        username: str,
        password: str,
        users: Users = inject_users(),
        token_expiration_provider: TokenExpirationProvider = InternalTokenExpirationProvider(),
        context: ServerContext = get_context(),
    ):
        self.username: str = username
        self.password: str = password
        self.users: Users = users
        self.user_data: User = User(**self.__user_data)
        self.context: ServerContext = context
        self.token_expiration_provider: TokenExpirationProvider = (
            token_expiration_provider
        )

    # -----------------------------------------------------
    # DESTRUCTOR METHOD
    # -----------------------------------------------------
    def __del__(self):
        """
        Cleans values in memory before releasing memory
        back to the operating system.
        :return: None
        """
        self.password = 0000000000000000000000000000000000
        self.username = 0000000000000000000000000000000000
        self.user_data = 000000000000000000000000000000000

    # -----------------------------------------------------
    # METHOD RETRIEVE USER DATA
    # -----------------------------------------------------
    @property
    def __user_data(self) -> dict:
        """
        Retrieves the user data from the database using the
        users' repository.
        :return: Dict
        """
        user_data: dict = self.users.get_by_username(self.username)
        user_data["_id"] = str(user_data["_id"])
        return user_data

    # -----------------------------------------------------
    # VERIFY PASSWORD
    # -----------------------------------------------------
    @staticmethod
    def __verify_password(password: str, password_hash: str, salt: str) -> bool:
        """
        Verifies if a given password is valid
        :param password: The password to be verified
        :param password_hash: The hash of the password stored
        in the internal user database
        :param salt: salt to link password to this specific
        context and prevent rainbow table attacks
        :return: True if password is valid / False if password
        is not valid
        """
        credential: IdentityCredential = Password(
            plain_text_password=password, salt=salt
        )
        return credential.verify(stored_hash=password_hash)

    # -----------------------------------------------------
    # PROPERTY IS VALID
    # -----------------------------------------------------
    @property
    def is_valid(self) -> bool:
        return self.__verify_password(
            password=self.password,
            password_hash=self.user_data.phash,
            salt=self.user_data.salt,
        )

    # -----------------------------------------------------
    # METHOD SERIALIZE SESSION TO DICT
    # -----------------------------------------------------
    def __serialize_session_to_dict(self) -> dict:
        return self.user_data.session.dict().copy()

    # -----------------------------------------------------
    # METHOD APPEND EXPIRATION
    # -----------------------------------------------------
    @staticmethod
    def __append_expiration(session_dict: dict) -> dict:
        output: dict = session_dict.copy()

    # -----------------------------------------------------
    # PROPERTY JWT ACCESS TOKEN
    # -----------------------------------------------------
    @property
    def jwt_access_token(self) -> str:
        if self.is_valid:
            to_encode: dict = self.__serialize_session_to_dict()
            to_encode["exp"] = self.token_expiration_provider.get_expiration_time()
            return jwt.encode(
                claims=to_encode,
                key=self.context.jwt_key,
                algorithm=self.context.jwt_signing_algorithm,
            )
        raise get_credentials_exception()


# ---------------------------------------------------------
# FUNCTION GET CREDENTIALS EXCEPTION
# ---------------------------------------------------------
def get_credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


# ---------------------------------------------------------
# FUNCTION GETY CURRENT USER
# ---------------------------------------------------------
async def get_user_session(
    token: str = Depends(oauth2_schema), context: ServerContext = Depends(get_context)
) -> UserSession:
    """
    Given a valid JWT access token, this functions decodes
    the token and validates its digital signature
    :param token: The encoded JWT access token fetched from
    the Authorization header in the HTTP Request
    :param context: Server context to securely access
    the signing keys
    :return:
    """
    try:
        payload = jwt.decode(
            token=token, key=context.jwt_key, algorithms=[context.jwt_signing_algorithm]
        )
        key_id: str = payload.get("sub")
        if key_id is None:
            raise get_credentials_exception()
    except JWTError:
        raise get_credentials_exception()

    session: UserSession = UserSession(**payload)
    if session is None:
        raise get_credentials_exception()
    context.logging.debug(f"User: {session.dict()} successfully authenticated")
    return session
