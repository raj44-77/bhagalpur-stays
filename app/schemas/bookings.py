"""Booking schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class BookingCreateRequest(BaseModel):
    hotel_id: int
    room_type_id: int
    check_in: date
    check_out: date
    number_of_rooms: int = Field(default=1, ge=1)
    guests: int = Field(default=2, ge=1)
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    special_requests: Optional[str] = None
    coupon_code: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    booking_ref: str
    hotel_name: Optional[str] = None
    room_type_name: Optional[str] = None
    hotel_image: Optional[str] = None
    check_in: date
    check_out: date
    number_of_rooms: int
    guests: int
    guest_name: Optional[str] = None
    base_amount: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    status: str
    payment_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class BookingStatusUpdateRequest(BaseModel):
    status: str = Field(..., pattern="^(confirmed|checked_in|checked_out|cancelled|no_show)$")


class CancelBookingRequest(BaseModel):
    cancellation_reason: Optional[str] = None