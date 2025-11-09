# app/routers/categories.py
import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.supabase_client import supabase
from app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from app.dependencies import get_current_user
from typing import List

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/", response_model=List[CategoryResponse])
def get_my_categories(current_user=Depends(get_current_user)):
    try:
        response = supabase.table('categories').select('*').execute()
        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=CategoryResponse)
def create_category(
        category_in: CategoryCreate,
        current_user=Depends(get_current_user)
):
    category_data = category_in.model_dump()
    category_data["user_id"] = current_user.id

    try:
        response = supabase.table('categories').insert(category_data).execute()
        data = response.data

        if not data:
            raise HTTPException(status_code=500, detail="Failed to create category")

        return data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
        category_id: uuid.UUID,
        category_in: CategoryUpdate,
        current_user=Depends(get_current_user)
):
    update_data = category_in.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    try:
        response = supabase.table('categories').update(update_data).eq('id', category_id).execute()
        data = response.data

        if not data:
            raise HTTPException(status_code=404, detail="Category not found or no permission")

        return data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{category_id}", status_code=204)
def delete_category(
        category_id: uuid.UUID,
        current_user=Depends(get_current_user)
):

    try:
        response = supabase.table('categories').delete().eq('id', category_id).execute()
        data = response.data

        if not data:
            raise HTTPException(status_code=404, detail="Category not found or no permission")

        return None

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))