"""Payments router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models import User, Payment, Booking
from app.services import payment_service

router = APIRouter(prefix="/api/payments", tags=["Payments"])


class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    payment_method: str = "pay_at_hotel"


@router.post("/")
def make_payment(data: PaymentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Process a payment"""
    payment = payment_service.create_payment(db, data.booking_id, current_user.id, data.amount, data.payment_method)
    return {"message": "Payment recorded", "status": payment.status}


@router.get("/booking/{booking_id}")
def get_payment(booking_id: int, db: Session = Depends(get_db)):
    """Get payment status"""
    return payment_service.get_payment_status(db, booking_id)


@router.post("/mark-paid/{booking_id}")
def mark_paid(booking_id: int, db: Session = Depends(get_db)):
    """Mark a booking as paid (owner/admin)"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.payment_status = "paid"

    existing = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    if not existing:
        payment = Payment(
            booking_id=booking_id,
            user_id=booking.user_id,
            amount=booking.total_amount,
            payment_method="cash",
            status="success",
            paid_at=func.now()
        )
        db.add(payment)
    else:
        existing.status = "success"
        existing.paid_at = func.now()

    db.commit()
    return {"message": "Payment marked as paid"}