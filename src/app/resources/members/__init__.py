from pydantic import BaseModel, Field
from typing import Optional


# =========================================================
# CLASS MEMBER BASE
# =========================================================
class MemberBase(BaseModel):
    name: str = Field(None, title="Name")

    last_name: str = Field(None, title="Last Name")

    second_last_name: Optional[str] = Field(None, title="Second Last Name")

    email: str = Field(None, title="Email")

    gov_id: str = Field(None, title="Government Issued Id")


# =========================================================
# CLASS MEMBER CREATION REQUEST
# =========================================================
class MemberCreationRequest(MemberBase):
    phone: str = Field(None, title="The Phone Number")
