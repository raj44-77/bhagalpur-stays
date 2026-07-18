"""Review schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewCreateRequest(BaseModel):
    hotel_id: int
    booking_id: int
    rating: int = Field(..., ge=1, le=5)
    cleanliness_rating: Optional[int] = Field(None, ge=1, le=5)
    service_rating: Optional[int] = Field(None, ge=1, le=5)
    comfort_rating: Optional[int] = Field(None, ge=1, le=5)
    value_rating: Optional[int] = Field(None, ge=1, le=5)
    location_rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    user_name: Optional[str] = None
    hotel_name: Optional[str] = None
    rating: int
    cleanliness_rating: Optional[int] = None
    service_rating: Optional[int] = None
    comfort_rating: Optional[int] = None
    value_rating: Optional[int] = None
    location_rating: Optional[int] = None
    title: Optional[str] = None
    comment: Optional[str] = None
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True