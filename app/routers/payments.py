from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Payment, Booking
router = APIRouter(prefix="/api/payments", tags=["Payments"])
@router.post("/mark-paid/{booking_id}")
def mark_paid(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    booking.payment_status = "paid"
    existing = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    if not existing:
        db.add(Payment(booking_id=booking_id, amount=booking.total_amount, payment_method="cash", status="success"))
    db.commit()
    return {"message": "Payment marked as paid"}
