from fastapi import APIRouter, Depends, HTTPException
from app.business_objects.member import inject_members, Members
from uuid import UUID

from app.business_objects.member.operations import CreateMemberOperation
from app.resources.members import MemberCreationRequest

router = APIRouter()


# =========================================================
# GET MEMBER BY ID
# =========================================================
@router.get("/member/{member_id}", tags=["Members"])
def get_member_by_id(member_id: UUID, members: Members = Depends(inject_members)):
    if not member_id:
        raise HTTPException(
            status_code=400, detail="You must provide a valid member_id"
        )


# =========================================================
# LIST MEMBERS
# =========================================================
@router.get("/members", tags=["Members"])
def list_members(members: Members = Depends(inject_members)):
    return []


# =========================================================
# CREATE MEMBER
# =========================================================
@router.post("/member", tags=["Members"], response_model=MemberCreationRequest)
def create_member(
    member: MemberCreationRequest, members: Members = Depends(inject_members)
):
    return CreateMemberOperation(member=member, members=members).operation_result


# =========================================================
# UPDATE MEMBER
# =========================================================
@router.put("/member/{member_id}", tags=["Members"])
def update_member_by_id(member_id: UUID, members: Members = Depends(inject_members)):
    return None
