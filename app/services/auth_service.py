"""Authentication service"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from app.models import User, RefreshToken, PasswordReset
from app.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.middleware.rate_limit import record_failed_login, reset_login_attempts
import secrets


def signup(db: Session, data: SignupRequest) -> User:
    """Register a new user"""
    existing = db.query(User).filter(
        (User.email == data.email) | (User.phone == data.phone)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone already registered"
        )

    user = User(
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        password_hash=hash_password(data.password),
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, data: LoginRequest, request: Request = None) -> TokenResponse:
    """Authenticate user and return tokens"""
    user = db.query(User).filter(User.email == data.email).first()
    
    # Get client IP for rate limiting
    client_ip = request.client.host if request else "unknown"
    
    if not user or not verify_password(data.password, user.password_hash):
        # Record failed login attempt
        record_failed_login(client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )

    # Reset login attempts on successful login
    reset_login_attempts(client_ip)

    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token_str = create_refresh_token({"sub": str(user.id)})

    refresh = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(refresh)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token_str)


def refresh_access_token(db: Session, refresh_token_str: str) -> TokenResponse:
    """Get new access token using refresh token"""
    token_record = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token_str
    ).first()

    if not token_record or token_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db.delete(token_record)

    new_access = create_access_token({"sub": str(user.id), "role": user.role})
    new_refresh = create_refresh_token({"sub": str(user.id)})

    db.add(RefreshToken(
        user_id=user.id,
        token=new_refresh,
        expires_at=datetime.utcnow() + timedelta(days=7)
    ))
    db.commit()

    return TokenResponse(access_token=new_access, refresh_token=new_refresh)


def forgot_password(db: Session, email: str) -> str:
    """Generate password reset token"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return "If the email exists, a reset link has been sent."

    token = secrets.token_urlsafe(32)
    reset = PasswordReset(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    db.add(reset)
    db.commit()

    # In production, send email here
    return token


def reset_password(db: Session, token: str, new_password: str) -> bool:
    """Reset password using token"""
    reset = db.query(PasswordReset).filter(
        PasswordReset.token == token,
        PasswordReset.used == False,
        PasswordReset.expires_at > datetime.utcnow()
    ).first()

    if not reset:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == reset.user_id).first()
    user.password_hash = hash_password(new_password)
    reset.used = True
    db.commit()
    return True


def logout(db: Session, refresh_token_str: str):
    """Invalidate refresh token"""
    db.query(RefreshToken).filter(RefreshToken.token == refresh_token_str).delete()
    db.commit()