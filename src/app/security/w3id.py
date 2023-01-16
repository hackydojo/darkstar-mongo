from typing import List

from authlib.integrations.starlette_client import OAuth
from authlib.oidc.core import UserInfo
from app.context import get_context
import uuid


# --------------------------------------------------------
# GET OR DEFAULT
# --------------------------------------------------------
class W3Identity(object):
    def __init__(self, user_info: UserInfo):
        self.name: str = self.__get_or_default(user_info.get("name"))
        self.uid: str = self.__get_or_default(user_info.get("uid"))
        self.email: str = self.__get_or_default(user_info.get("email")).lower()
        self.s_hash: str = self.__get_or_default(user_info.get("s_hash")).lower()
        self.blue_groups: list = self.__filter_blue_groups(user_info.get("blueGroups"))
        self.challenge: str = self.__gen_challenge()

    @staticmethod
    def __gen_challenge() -> str:
        return str(uuid.uuid4()).replace("-", "#").upper()

    @staticmethod
    def __filter_blue_groups(blue_groups: List[str]) -> List[str]:
        groups: list = []
        for group in blue_groups:
            normalized_group: str = group.lower()
            if normalized_group.startswith("cloud_platform_appsec"):
                groups.append(normalized_group)
        return groups

    def dict(self) -> dict:
        return {
            "name": self.name,
            "uid": self.uid,
            "email": self.email,
            "s_hash": self.s_hash,
            "blue_groups": self.blue_groups,
            "challenge": self.challenge,
        }

    @staticmethod
    def __get_or_default(value: str) -> str:
        if value is None or value == "":
            return "n/a"
        return value


# --------------------------------------------------------
# REGISTER AND GET OAUTH PROVIDER
# --------------------------------------------------------
def get_oauth() -> OAuth:
    provider = OAuth()
    config = get_context()
    provider.register(
        name="w3id",
        server_metadata_url=config.as_str("W3ID_DISCOVERY_ENDPOINT"),
        client_id=config.as_str("W3ID_CLIENT_ID"),
        client_secret=config.as_str("W3ID_CLIENT_SECRET"),
        client_kwargs={"scope": "openid email profile"},
    )
    return provider
