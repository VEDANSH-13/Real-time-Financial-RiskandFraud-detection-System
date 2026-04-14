"""
User service: business logic for user operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserCreate
from services.auth_service import AuthService


class UserService:
    """Handles user CRUD operations and authentication logic."""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Register a new user."""
        # Check for existing username
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already registered",
            )

        # Check for existing email
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        hashed_pw = AuthService.hash_password(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_pw,
        )

        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Authenticate a user by username and password."""
        user = db.query(User).filter(User.username == username).first()
        if not user or not AuthService.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """Get a user by their ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
