from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, RefreshTokenRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.services import auth_service
router = APIRouter(prefix="/api/auth", tags=["Auth"])
@router.post("/signup", status_code=201)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    return auth_service.signup(db, data)
@router.post("/login")
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    return auth_service.login(db, data, request)
@router.post("/refresh")
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_access_token(db, data.refresh_token)
@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    token = auth_service.forgot_password(db, data.email)
    return {"message": "If the email exists, a reset link has been sent.", "debug_token": token}
@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    auth_service.reset_password(db, data.token, data.new_password)
    return {"message": "Password reset successful"}
@router.post("/logout")
def logout(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    auth_service.logout(db, data.refresh_token)
    return {"message": "Logged out successfully"}
