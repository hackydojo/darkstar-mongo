from fastapi import APIRouter, Depends, HTTPException
from app.business_objects.member import inject_members, Members
from uuid import UUID

from app.resources.members import MemberCreationRequest

router = APIRouter()


# =========================================================
# GET MEMBER BY ID
# =========================================================
@router.get("/member/{member_id}")
def get_member_by_id(member_id: UUID, members: Members = Depends(inject_members)):
    if not member_id:
        raise HTTPException(
            status_code=400, detail="You must provide a valid member_id"
        )


# =========================================================
# LIST MEMBERS
# =========================================================
@router.get("/members")
def list_members(members: Members = Depends(inject_members)):
    return []


# =========================================================
# CREATE MEMBER
# =========================================================
@router.post("/member")
def create_member(
    member: MemberCreationRequest, members: Members = Depends(inject_members)
):
    return


# =========================================================
# UPDATE MEMBER
# =========================================================
@router.put("/member/{member_id}")
def update_member_by_id(member_id: UUID, members: Members = Depends(inject_members)):
    return None
