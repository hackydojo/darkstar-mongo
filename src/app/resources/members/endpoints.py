from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

router = APIRouter()


# =========================================================
# GET USER BY ID
# =========================================================
@router.get("/member/{member_id}")
def get_member_by_id(member_id: UUID):
    if not member_id:
        raise HTTPException(
            status_code=400, detail="You must provide a valid member_id"
        )


# =========================================================
# LIST USERS
# =========================================================
@router.get("/member")
def list_members():
    return []
