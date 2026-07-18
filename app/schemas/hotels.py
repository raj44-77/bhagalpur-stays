"""Hotel schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, time


class HotelImageSchema(BaseModel):
    id: int
    image_url: str
    caption: Optional[str] = None
    is_primary: bool = False

    class Config:
        from_attributes = True


class AmenitySchema(BaseModel):
    id: int
    name: str
    icon: Optional[str] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True


class HotelResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    full_address: str
    star_rating: int
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    cancellation_hours: int = 24
    status: str
    is_featured: bool
    total_rooms: int
    city_name: Optional[str] = None
    area_name: Optional[str] = None
    images: List[HotelImageSchema] = []
    amenities: List[AmenitySchema] = []
    avg_rating: Optional[float] = None
    review_count: int = 0
    min_price: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class HotelListResponse(BaseModel):
    id: int
    name: str
    slug: str
    star_rating: int
    status: str
    is_featured: bool
    city_name: Optional[str] = None
    area_name: Optional[str] = None
    primary_image: Optional[str] = None
    avg_rating: Optional[float] = None
    review_count: int = 0
    min_price: Optional[float] = None

    class Config:
        from_attributes = True


class HotelCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    city_id: int
    area_id: Optional[int] = None
    description: Optional[str] = None
    full_address: str
    star_rating: int = Field(default=3, ge=1, le=5)
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class HotelUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    full_address: Optional[str] = None
    star_rating: Optional[int] = Field(None, ge=1, le=5)
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None