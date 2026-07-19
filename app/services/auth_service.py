from app.models import User, RefreshToken, PasswordReset
from app.security import hash_password, verify_password, create_access_token, create_refresh_token
from fastapi import HTTPException
from datetime import datetime, timedelta
import secrets
def signup(db, data):
    from app.models import User
    existing = db.query(User).filter((User.email == data.email) | (User.phone == data.phone)).first()
    if existing: raise HTTPException(400, "Email or phone already registered")
    user = User(full_name=data.full_name, email=data.email, phone=data.phone, password_hash=hash_password(data.password), role=data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
def login(db, data, request=None):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    if not user.is_active: raise HTTPException(403, "Account deactivated")
    access = create_access_token({"sub": str(user.id), "role": user.role})
    refresh = create_refresh_token({"sub": str(user.id)})
    db.add(RefreshToken(user_id=user.id, token=refresh, expires_at=datetime.utcnow() + timedelta(days=7)))
    db.commit()
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
def refresh_access_token(db, token):
    record = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not record or record.expires_at < datetime.utcnow(): raise HTTPException(401, "Invalid token")
    user = db.query(User).filter(User.id == record.user_id).first()
    db.delete(record)
    access = create_access_token({"sub": str(user.id), "role": user.role})
    refresh = create_refresh_token({"sub": str(user.id)})
    db.add(RefreshToken(user_id=user.id, token=refresh, expires_at=datetime.utcnow() + timedelta(days=7)))
    db.commit()
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
def forgot_password(db, email):
    user = db.query(User).filter(User.email == email).first()
    if not user: return "If exists, reset link sent"
    token = secrets.token_urlsafe(32)
    db.add(PasswordReset(user_id=user.id, token=token, expires_at=datetime.utcnow() + timedelta(hours=1)))
    db.commit()
    return token
def reset_password(db, token, new_password):
    reset = db.query(PasswordReset).filter(PasswordReset.token == token, PasswordReset.used == False, PasswordReset.expires_at > datetime.utcnow()).first()
    if not reset: raise HTTPException(400, "Invalid token")
    user = db.query(User).filter(User.id == reset.user_id).first()
    user.password_hash = hash_password(new_password)
    reset.used = True
    db.commit()
    return True
def logout(db, token):
    db.query(RefreshToken).filter(RefreshToken.token == token).delete()
    db.commit()