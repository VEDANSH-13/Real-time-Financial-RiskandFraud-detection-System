"""
Pydantic schemas for JWT token handling.
"""

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data extracted from JWT token."""
    username: Optional[str] = None
    role: Optional[str] = None
