# app/routers/priorities.py
from fastapi import APIRouter, Depends, HTTPException
from app.supabase_client import supabase
from app.schemas import PriorityResponse
from app.dependencies import get_current_user
from typing import List

router = APIRouter(
    prefix="/priorities",
    tags=["Priorities"]
)

@router.get("/", response_model=List[PriorityResponse])
def get_all_priorities(current_user=Depends(get_current_user)):
    try:
        response = supabase.table('priorities').select('*').order('id').execute()
        data = response.data

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))