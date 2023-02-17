from confite import Confite
from dotenv import load_dotenv
from pymongo import MongoClient, database
from app.logging import AbstractLogger, StandardOutputLogger
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import logging

disable_warnings(InsecureRequestWarning)


# ---------------------------------------------------------
# CLASS HEIMDALL SERVER SETTINGS
# ---------------------------------------------------------
class ServerContext(Confite):
    """
    Server Context is the top level implementation
    of a parameter object that implement the Flyweight design
    pattern to help sharing settings and connection resources
    across the application by exposing them as properties
    abstracted through common interfaces that enable the
    inversion of control (Dependency Inversion) pattern across
    all the application.
    """

    # -----------------------------------------------------
    # CLASS CONSTRUCTOR
    # -----------------------------------------------------
    def __init__(self, env_variable_names: list):
        super().__init__(env_variable_names)

    # -----------------------------------------------------
    # BUILD CONNECTION STRING
    # -----------------------------------------------------
    def build_connection_string(self):
        user: str = self.as_str("MONGO_USER")
        pwd: str = self.as_str("MONGO_PASSWORD")
        host: str = self.as_str("MONGO_SERVER")
        db: str = self.as_str("MONGO_DB")
        port: int = self.as_int("MONGO_PORT")
        if self.as_int("MONGO_SRV") == 1:
            return f"mongodb+srv://{user}:{pwd}@{host}/{db}"
        return f"mongodb://{user}:{pwd}@{host}:{port}/{db}"

    # -----------------------------------------------------
    # TLS_REQUIRED
    # -----------------------------------------------------
    def tls_required(self) -> bool:
        return self.as_int("MONGO_TLS_CONNECTION") == 1

    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------
    @property
    def database(self) -> database:
        if self.tls_required:
            return self.database_with_tls
        return self.database_without_tls

    # -----------------------------------------------------
    # DATABASE WITHOUT
    # -----------------------------------------------------
    @property
    def database_without_tls(self) -> database:
        print("Connecting without database encryption...")
        return MongoClient(
            self.build_connection_string() + f"?authSource=admin{self.replica_set}"
        )[self.as_str("MONGO_DB")]

    # -----------------------------------------------------
    # DATABASE WITH TLS
    # -----------------------------------------------------
    @property
    def database_with_tls(self) -> database:
        print(
            self.build_connection_string()
            + f"?authSource=admin{self.replica_set}&tls=true"
        )
        return MongoClient(
            self.build_connection_string()
            + f"?authSource=admin{self.replica_set}&tls=true"
        )[self.as_str("MONGO_DB")]

    # -----------------------------------------------------
    # PROPERTY IS_CLUSTER
    # -----------------------------------------------------
    @property
    def is_cluster(self) -> bool:
        return self.as_int("MONGO_CLUSTER") == 1

    # -----------------------------------------------------
    # PROPERTY REPLICA SET
    # -----------------------------------------------------
    @property
    def replica_set(self) -> str:
        replica_set_str = ""
        if self.is_cluster:
            replica_set_str = f"&replicaSet={self.as_str('MONGO_REPLICA_SET')}"
        return replica_set_str

    # -----------------------------------------------------
    # PROPERTY LOGGING
    # -----------------------------------------------------
    @property
    def logging(self) -> AbstractLogger:
        return StandardOutputLogger()

    # -----------------------------------------------------
    # PROPERTY MIDDLEWARE KEY
    # -----------------------------------------------------
    @property
    def middleware_key(self) -> str:
        return self.as_str("SESSION_MIDDLEWARE_KEY")

    # -----------------------------------------------------
    # PROPERTY API_VERSION
    # -----------------------------------------------------
    @property
    def api_version(self) -> str:
        return self.as_str("API_VERSION")

    # -----------------------------------------------------
    # PROPERTY OIDC_CLIENT_ID
    # -----------------------------------------------------
    @property
    def oidc_client_id(self) -> str:
        return self.as_str("OIDC_CLIENT_ID")

    # -----------------------------------------------------
    # PROPERTY OIDC_CLIENT_SECRET
    # -----------------------------------------------------
    @property
    def oidc_client_secret(self) -> str:
        return self.as_str("OIDC_CLIENT_SECRET")

    # -----------------------------------------------------
    # PROPERTY OIDC_DISCOVERY_ENDPOINT
    # -----------------------------------------------------
    @property
    def oidc_discovery_endpoint(self) -> str:
        return self.as_str("OIDC_DISCOVERY_ENDPOINT")

    # -----------------------------------------------------
    # PROPERTY QUERY LIMIT
    # -----------------------------------------------------
    @property
    def query_limit(self) -> int:
        return self.as_int("QUERY_LIMIT")

    # -----------------------------------------------------
    # PROPERTY LOG LEVEL
    # -----------------------------------------------------
    @property
    def log_level(self):
        match self.as_str("LOG_LEVEL").upper():
            case "DEBUG":
                return logging.DEBUG
            case "ERROR":
                return logging.ERROR
            case "WARNING":
                return logging.WARNING
            case "INFO":
                return logging.INFO
            case _:
                return logging.INFO

    # -----------------------------------------------------
    # PROPERTY JWT KEY
    # -----------------------------------------------------
    @property
    def jwt_key(self) -> str:
        return self.as_str("JWT_SECRET_KEY")

    # -----------------------------------------------------
    # PROPERTY JWT SIGNING ALGORITHM
    # -----------------------------------------------------
    @property
    def jwt_signing_algorithm(self) -> str:
        return self.as_str("JWT_SIGN_ALGORITHM")

    # -----------------------------------------------------
    # PROPERTY JWT TOKEN DURATION
    # -----------------------------------------------------
    @property
    def jwt_token_duration(self) -> int:
        return self.as_int("JWT_TOKEN_DURATION_IN_MINUTES")


# ---------------------------------------------------------
# METHOD GET SETTINGS
# ---------------------------------------------------------
def get_context() -> ServerContext:
    load_dotenv()
    return ServerContext(
        [
            "MONGO_USER",
            "MONGO_PASSWORD",
            "MONGO_SERVER",
            "MONGO_DB",
            "MONGO_PORT",
            "MONGO_TLS_CONNECTION",
            "MONGO_REPLICA_SET",
            "MONGO_CLUSTER",
            "MONGO_SRV",
            "OIDC_DISCOVERY_ENDPOINT",
            "OIDC_CLIENT_ID",
            "OIDC_CLIENT_SECRET",
            "SESSION_MIDDLEWARE_KEY",
            "API_VERSION",
            "QUERY_LIMIT",
            "LOG_LEVEL",
            "JWT_SECRET_KEY",
            "JWT_SIGN_ALGORITHM",
            "JWT_TOKEN_DURATION_IN_MINUTES",
        ]
    )
