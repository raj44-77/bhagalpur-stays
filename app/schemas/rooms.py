"""Room schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RoomImageSchema(BaseModel):
    id: int
    image_url: str
    caption: Optional[str] = None

    class Config:
        from_attributes = True


class RoomTypeResponse(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str] = None
    room_size_sqft: Optional[int] = None
    bed_type: Optional[str] = None
    max_guests: int
    base_price: float
    extra_bed_price: float = 0
    total_rooms: int
    is_active: bool
    images: List[RoomImageSchema] = []
    created_at: datetime

    class Config:
        from_attributes = True


class RoomTypeCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    room_size_sqft: Optional[int] = None
    bed_type: Optional[str] = None
    max_guests: int = Field(default=2, ge=1)
    base_price: float = Field(..., gt=0)
    extra_bed_price: float = Field(default=0, ge=0)
    total_rooms: int = Field(default=1, ge=1)


class RoomInventoryResponse(BaseModel):
    id: int
    room_type_id: int
    date: str
    available_rooms: int
    price_override: Optional[float] = None
    is_available: bool

    class Config:
        from_attributes = True