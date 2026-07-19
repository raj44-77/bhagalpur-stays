from app.models import Payment, Booking
def create_payment(db, booking_id, user_id, amount, method="pay_at_hotel"):
    payment = Payment(booking_id=booking_id, amount=amount, payment_method=method, status="success" if method == "pay_at_hotel" else "pending")
    db.add(payment)
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking: booking.payment_status = "paid" if method != "pay_at_hotel" else "unpaid"
    db.commit()
    return payment
def get_payment_status(db, booking_id):
    payment = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    if not payment: return {"status": "no_payment"}
    return {"status": payment.status, "amount": float(payment.amount), "method": payment.payment_method}
