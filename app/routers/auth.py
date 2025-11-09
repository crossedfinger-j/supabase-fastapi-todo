# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.supabase_client import supabase
from app.schemas import UserCreate, Token # schema

router = APIRouter()

@router.post("/signup")
def signup(user_credentials: UserCreate):
    try:
        user = supabase.auth.sign_up({
            "email": user_credentials.email,
            "password": user_credentials.password,
        })
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        session = supabase.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password,
        })
        return {"access_token": session.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Incorrect email or password")