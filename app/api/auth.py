from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from bson import ObjectId

from app.db import db 
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post ("/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing = await db.users.find_one({"email":user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hash_password(user.password),
    }
    
    result= await db.users.insert_one(user_dict)
    user_dict["_id"] = str (result.inserted_id)
    return user_dict 



@router.post("/login")
async def login(form_data:OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"username": form_data.username})
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username pr password")
    
    token = create_access_token({"sub":str(user["_id"])})
    return {"access_token":token, "token_type":"bearer"}

async def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id : str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="INvalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await db.user.find_one({"_id":ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user:dict = Depends(get_current_user)):
    current_user["_id"] = str(current_user["_id"])
    return current_user




