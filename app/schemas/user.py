from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.db import PyObjectId


class UserBase(BaseModel):
    username:str
    email:EmailStr
    
class UserCreate(UserBase):
    password:str
    
class UserResponse(UserBase):
    id:str= Field(default_factory=str, alias="_id")
    
    class config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId:str}
        
        