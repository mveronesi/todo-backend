from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import date


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: uuid.UUID
    is_active: bool

    class Config:
        from_attributes=True


class TodoBase(BaseModel):
    text: str
    done: bool
    important: bool
    date: date
    user_id: uuid.UUID


class Todo(TodoBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None