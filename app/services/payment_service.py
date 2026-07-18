"""Payment service"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Payment, Booking


def create_payment(db: Session, booking_id: int, user_id: int, amount: float, method: str = "pay_at_hotel"):
    """Record a payment"""
    payment = Payment(
        booking_id=booking_id,
        user_id=user_id,
        amount=amount,
        payment_method=method,
        status="success" if method == "pay_at_hotel" else "pending",
        paid_at=datetime.utcnow() if method == "pay_at_hotel" else None
    )
    db.add(payment)

    # Update booking payment status
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        booking.payment_status = "paid" if method != "pay_at_hotel" else "unpaid"

    db.commit()
    db.refresh(payment)
    return payment


def get_payment_status(db: Session, booking_id: int):
    """Get payment status for a booking"""
    payment = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    if not payment:
        return {"status": "no_payment", "amount": 0}
    return {
        "status": payment.status,
        "amount": float(payment.amount),
        "method": payment.payment_method,
        "paid_at": str(payment.paid_at) if payment.paid_at else None
    }