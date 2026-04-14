"""
Pydantic schemas for user-related request/response validation.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Alphanumeric username (3-50 chars)",
    )
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password (min 8 chars)",
    )


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user data in responses (no password)."""
    id: UUID
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
