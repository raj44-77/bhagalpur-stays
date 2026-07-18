"""Users router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models import User
from app.security import hash_password
router = APIRouter(prefix="/api/users", tags=["Users"])
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
class PasswordChange(BaseModel):
    current_password: str
    new_password: str
@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "role": current_user.role,
        "is_verified": current_user.is_verified,
        "created_at": str(current_user.created_at)
    }
@router.put("/me")
def update_profile(data: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.full_name:
        current_user.full_name = data.full_name
    if data.phone:
        current_user.phone = data.phone
    db.commit()
    return {"message": "Profile updated"}
@router.post("/change-password")
def change_password(data: PasswordChange, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.security import verify_password
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.password_hash = hash_password(data.new_password)
    db.commit()
    return {"message": "Password changed"}
