import uuid
from typing import Optional, List

from app.business_objects.user.repository import Users
from pydantic import BaseModel, Field


# =========================================================
# FUNCTION INJECT USERS
# =========================================================
def inject_users() -> Users:
    return Users()


# =========================================================
# CLASS USER
# =========================================================
class User(BaseModel):
    _id: Optional[str] = Field(None, title="Internal Identifier")

    uid: str = Field(str(uuid.uuid4()), title="Unique identifier of the user")

    phash: str = Field(None, title="Password hash")

    salt: str = Field(None, title="Password salt")

    name: str = Field(None, title="Name of the user")

    last_name: str = Field(None, title="Last name of the user")

    email: str = Field(None, title="Email of the user")

    disabled: bool = Field(
        True, title="Weather the user is disabled or not. Disabled by default"
    )

    claims: Optional[List[str]] = Field(["authenticate"], title="User claims")

    # -----------------------------------------------------
    # METHOD CAN
    # -----------------------------------------------------
    def can(self, claim: str) -> bool:
        """
        Validates if a particular claim is associated with
        given user
        :param claim: The claim to be verified
        :return: True is the user has the claim. False if the
        user does not have the claim
        """
        return claim in self.claims

    # -----------------------------------------------------
    # PROPERTY SESSION
    # -----------------------------------------------------
    @property
    def session(self):
        return UserSession(
            sub=self.uid,
            desc=f"{self.name} {self.last_name}",
            email=self.email,
            claims=self.claims,
        )


# =========================================================
# CLASS ONLINE USER
# =========================================================
class UserSession(BaseModel):
    """
    Represents the session of an authenticated user
    """

    sub: str = Field(None, title="Unique identifier of the user")
    desc: str = Field(None, title="First name and lastname")
    email: str = Field(None, title="Email of the user")
    claims: List[str] = Field(None, title="User claims")
    exp: Optional[int] = Field(None, title="Expiration of the session in Unix time")

    # -----------------------------------------------------
    # METHOD CAN
    # -----------------------------------------------------
    def can(self, claim: str) -> bool:
        """
        Validates if a particular claim is associated with
        given user
        :param claim: The claim to be verified
        :return: True is the user has the claim. False if the
        user does not have the claim
        """
        return claim in self.claims
