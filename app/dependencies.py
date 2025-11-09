# app/dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.supabase_client import supabase # client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") # login path

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user = supabase.auth.get_user(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        # [email (id), password] in user.user instance
        return user.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")