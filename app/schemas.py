from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
import uuid

# --- Authentication Schemas
class UserBase(BaseModel):
    """ base model of all user schema """
    email: str

class UserCreate(UserBase):
    """ schema for register user (request) """
    password: str

class UserResponse(UserBase):
    """
    schema for update user information (response)
    modeling for auth.users table of Supabase
    """
    id: uuid.UUID   # auth.users.id of Supabase
    created_at: datetime

    class Config:
        orm_mode = True # Allows FastAPI to convert the object using this schema.

class Token(BaseModel):
    """ JWT token schema when login success """
    access_token: str
    token_type: str


# --- Priority Schemas
class PriorityBase(BaseModel):
    name: str

class PriorityResponse(PriorityBase):
    """ schema used for retrieving importance. (Response) """
    id: int

    class Config:
        orm_mode = True


# --- Category Schemas
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass # only name

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: uuid.UUID
    user_id: uuid.UUID # owner of this category in auth.users
    created_at: datetime

    class Config:
        orm_mode = True


# --- Todos Schemas
class TodoBase(BaseModel):
    content: str
    due_date: Optional[date] = None
    category_id: Optional[uuid.UUID] = None
    priority_id: Optional[int] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    content: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[date] = None
    category_id: Optional[uuid.UUID] = None
    priority_id: Optional[int] = None

class TodoResponse(TodoBase):
    id: uuid.UUID
    is_completed: bool
    created_at: datetime
    user_id: uuid.UUID

    class Config:
        orm_mode = True