from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
async def read_current_user(user=Depends(get_current_user)):
    return {
        "username": user["username"],
        "email": user["email"]
    }
