"""Auth router - login, signup, refresh"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    SignupRequest, LoginRequest, TokenResponse,
    RefreshTokenRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from app.schemas.users import UserResponse
from app.services import auth_service
from app.services.audit_service import log_action

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(data: SignupRequest, request: Request, db: Session = Depends(get_db)):
    """Register a new user"""
    user = auth_service.signup(db, data)
    log_action(
        db, user_id=user.id, action="signup",
        entity_type="user", entity_id=user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """Login and get access token"""
    result = auth_service.login(db, data, request)
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        log_action(
            db, user_id=user.id, action="login",
            entity_type="user", entity_id=user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
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
        log_action(
            db, user_id=user.id, action="password_reset_requested",
            entity_type="user", entity_id=user.id,
            ip_address=request.client.host
        )
    return {"message": "If the email exists, a reset link has been sent.", "debug_token": token}


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """Reset password with token"""
    auth_service.reset_password(db, data.token, data.new_password)
    log_action(
        db, action="password_reset_completed",
        ip_address=request.client.host
    )
    return {"message": "Password reset successful"}


@router.post("/logout")
def logout(data: RefreshTokenRequest, request: Request, db: Session = Depends(get_db)):
    """Logout and invalidate refresh token"""
    auth_service.logout(db, data.refresh_token)
    return {"message": "Logged out successfully"}