"""User schemas"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    role: str
    avatar_url: Optional[str] = None
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    avatar_url: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=50)


class OwnerDetailRequest(BaseModel):
    business_name: Optional[str] = None
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None
    address: Optional[str] = None