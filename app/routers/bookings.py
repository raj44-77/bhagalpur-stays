"""Bookings router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models import User
from app.services import booking_service

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


class BookingCreate(BaseModel):
    hotel_id: int
    room_type_id: int
    check_in: date
    check_out: date
    number_of_rooms: int = 1
    guests: int = 2
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    special_requests: Optional[str] = None
    coupon_code: Optional[str] = None


@router.post("/")
def create_booking(data: BookingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new booking"""
    booking, error = booking_service.create_booking(db, current_user.id, data.dict())
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Booking created", "booking_ref": booking.booking_ref, "total_amount": float(booking.total_amount)}


@router.get("/")
def my_bookings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's bookings"""
    return booking_service.get_user_bookings(db, current_user.id)


@router.get("/{booking_id}")
def get_booking(booking_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get booking details"""
    bookings = booking_service.get_user_bookings(db, current_user.id)
    for b in bookings:
        if b["id"] == booking_id:
            return b
    raise HTTPException(status_code=404, detail="Booking not found")


@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: int, reason: Optional[str] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Cancel a booking"""
    booking, error = booking_service.cancel_booking(db, booking_id, reason)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Booking cancelled", "refund_amount": float(booking.refund_amount)}