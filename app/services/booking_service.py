"""Booking service"""
from sqlalchemy.orm import Session
from datetime import datetime
import random
from app.models import Booking, RoomType, Hotel, Coupon
def generate_booking_ref():
    return f"ABH-{datetime.now().year}-{random.randint(1000, 9999)}"
def create_booking(db, user_id, data):
    room_type = db.query(RoomType).filter(RoomType.id == data.get("room_type_id")).first()
    if not room_type: return None, "Room not found"
    nights = (data["check_out"] - data["check_in"]).days
    if nights < 1: return None, "Invalid dates"
    discount = 0
    if data.get("coupon_code"):
        coupon = db.query(Coupon).filter(Coupon.code == data["coupon_code"], Coupon.is_active == True).first()
        if coupon:
            if coupon.discount_type == "fixed": discount = float(coupon.discount_value)
            else: discount = min(float(room_type.base_price) * nights * float(coupon.discount_value) / 100, float(coupon.max_discount or 99999))
    subtotal = float(room_type.base_price) * nights
    tax = round(subtotal * 0.12)
    total = subtotal + tax - discount
    booking = Booking(booking_ref=generate_booking_ref(), user_id=user_id, hotel_id=room_type.hotel_id, room_type_id=data["room_type_id"], check_in=data["check_in"], check_out=data["check_out"], guests=data.get("guests", 2), guest_name=data.get("guest_name"), guest_email=data.get("guest_email"), guest_phone=data.get("guest_phone"), base_amount=subtotal, tax_amount=tax, discount_amount=discount, total_amount=total, status="pending")
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking, None
def get_user_bookings(db, user_id):
    bookings = db.query(Booking).filter(Booking.user_id == user_id).order_by(Booking.created_at.desc()).all()
    return [{"id": b.id, "booking_ref": b.booking_ref, "hotel_name": b.hotel.name if b.hotel else None, "room_type_name": b.room_type.name if b.room_type else None, "check_in": str(b.check_in), "check_out": str(b.check_out), "guests": b.guests, "guest_name": b.guest_name, "base_amount": float(b.base_amount), "tax_amount": float(b.tax_amount), "discount_amount": float(b.discount_amount), "total_amount": float(b.total_amount), "status": b.status, "payment_status": b.payment_status, "created_at": str(b.created_at), "hotel_id": b.hotel_id, "hotel_image": b.hotel.images[0].image_url if b.hotel and b.hotel.images else None} for b in bookings]
def cancel_booking(db, booking_id, reason=None):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking: return None, "Not found"
    booking.status = "cancelled"
    db.commit()
    return booking, None
