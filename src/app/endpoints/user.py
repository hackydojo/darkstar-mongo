from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

router = APIRouter()


# =========================================================
# GET USER BY ID
# =========================================================
@router.get("/user/{user_id}")
def get_user_by_id(user_id: UUID):
    if not user_id:
        raise HTTPException(status_code=400, detail="You must provide a valid user_id")


# =========================================================
# LIST USERS
# =========================================================
@router.get("/users")
def list_users():
    return []
