"""Auth router - login, signup, refresh"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas.auth import (
    SignupRequest, LoginRequest, TokenResponse,
    RefreshTokenRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from app.schemas.users import UserResponse
from app.services import auth_service


router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(data: SignupRequest, request: Request, db: Session = Depends(get_db)):
    """Register a new user"""
    user = auth_service.signup(db, data)
    # audit removed
    )
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """Login and get access token"""
    result = auth_service.login(db, data, request)
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        # audit removed
        )
    return result


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Get new access token from refresh token"""
    return auth_service.refresh_access_token(db, data.refresh_token)


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """Request password reset"""
    token = auth_service.forgot_password(db, data.email)
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        # audit removed
    return {"message": "If the email exists, a reset link has been sent.", "debug_token": token}


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """Reset password with token"""
    auth_service.reset_password(db, data.token, data.new_password)
    # audit removed
    return {"message": "Password reset successful"}


@router.post("/logout")
def logout(data: RefreshTokenRequest, request: Request, db: Session = Depends(get_db)):
    """Logout and invalidate refresh token"""
    auth_service.logout(db, data.refresh_token)
    return {"message": "Logged out successfully"}