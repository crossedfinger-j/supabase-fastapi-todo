# app/routers/todos.py
import uuid

from fastapi import APIRouter, Depends, HTTPException
from app.supabase_client import supabase
from app.schemas import TodoCreate, TodoResponse, TodoUpdate  # schema
from app.dependencies import get_current_user  # for authentication
from typing import List

router = APIRouter(
    prefix="/todos",  # start with /todos
    tags=["Todos"]
)


@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, current_user=Depends(get_current_user)):
    todo_data = todo.model_dump()
    todo_data["user_id"] = current_user.id  # Add the current user's ID

    try:
        response = supabase.table('todos').insert(todo_data).execute()
        data = response.data

        return data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[TodoResponse])
def read_todos(current_user=Depends(get_current_user)):
    try:
        response = supabase.table('todos').select('*').execute()
        data = response.data
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo_details(todo_id: uuid.UUID, current_user=Depends(get_current_user)):
    try:
        response = supabase.table('todos').select('*').eq('id', todo_id).execute()
        data = response.data

        if not data:
            raise HTTPException(status_code=404, detail="Todo not found")

        return data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo_item(
        todo_id: uuid.UUID,
        todo_update: TodoUpdate,
        current_user=Depends(get_current_user)
):
    update_data = todo_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    try:
        response = supabase.table('todos').update(update_data).eq('id', todo_id).execute()
        data = response.data

        if not data:
            raise HTTPException(status_code=404, detail="Todo not found")

        return data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{todo_id}", status_code=204)  # 성공 시 204 No Content 반환
def delete_todo(todo_id: uuid.UUID, current_user=Depends(get_current_user)):
    try:
        response = supabase.table('todos').delete().eq('id', todo_id).execute()
        data = response.data

        if not data:
            raise HTTPException(status_code=404, detail="Todo not found")

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))