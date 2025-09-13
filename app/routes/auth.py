from fastapi import APIRouter, Depends, HTTPException
from app import db
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token


router = APIRouter()

@router.post("/register")
async def register_user(username:str, email:str, password:str):
    user_exists = await db["users"].find_one({"email":email})
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(password)
    new_user = {"username":username, "email":email, "hashed_password":hashed_pw}
    await db["users"].insert_one(new_user)
    return {"msg":"User registered successfull"}

@router.post("/login")
async def login_user(email:str, password:str):
    user = await db["users"].find_one({"email":email})
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token= create_access_token(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type":"bearer"}
