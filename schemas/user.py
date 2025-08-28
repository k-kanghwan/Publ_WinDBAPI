from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    email: str = Field(..., example="user@example.com")
    full_name: str = Field(..., example="John Doe")
    password: str = Field(..., example="password123")


class UserLogin(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., example="password123")
