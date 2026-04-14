"""
Authentication routes: register, login, and profile endpoints.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.user import UserCreate, UserResponse, UserLogin
from schemas.token import Token
from services.user_service import UserService
from services.auth_service import AuthService, get_current_user
from models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.

    - **username**: Unique alphanumeric username (3-50 chars)
    - **email**: Valid email address
    - **password**: Minimum 8 characters
    """
    user = UserService.create_user(db, user_data)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Login and receive JWT token",
)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return a JWT access token.
    """
    user = UserService.authenticate_user(db, credentials.username, credentials.password)
    access_token = AuthService.create_access_token(
        data={"sub": user.username, "role": user.role.value}
    )
    return Token(access_token=access_token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Return the currently authenticated user's profile.
    """
    return current_user
