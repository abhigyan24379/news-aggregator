from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError
from app.core.auth import SECRET_KEY, ALGORITHM
from app import db  


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token :str = Depends(oauth2_scheme)) :
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email:str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="User Not Found")
        user = await db["users"].find_one({"email":email})
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")




