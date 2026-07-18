"""Booking service"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import date, datetime
import random
from app.models import Booking, RoomType, Hotel, HotelImage, Coupon, CouponUsage, Payment


def generate_booking_ref():
    """Generate unique booking reference"""
    return f"ABH-{datetime.now().year}-{random.randint(1000, 9999)}"


def calculate_total(base_amount: float, nights: int, discount: float = 0):
    """Calculate total with 12% tax"""
    subtotal = base_amount * nights
    tax = round(subtotal * 0.12)
    total = subtotal + tax - discount
    return {"base_amount": subtotal, "tax_amount": tax, "discount_amount": discount, "total_amount": total}


def create_booking(db: Session, user_id: int, data: dict):
    """Create a new booking"""
    room_type = db.query(RoomType).filter(RoomType.id == data["room_type_id"]).first()
    if not room_type:
        return None, "Room type not found"

    nights = (data["check_out"] - data["check_in"]).days
    if nights < 1:
        return None, "Invalid dates"

    discount = 0
    coupon_id = None

    # Apply coupon if provided
    if data.get("coupon_code"):
        coupon = db.query(Coupon).filter(
            Coupon.code == data["coupon_code"],
            Coupon.is_active == True
        ).first()
        if coupon:
            if coupon.discount_type == "fixed":
                discount = float(coupon.discount_value)
            elif coupon.discount_type == "percentage":
                discount = min(float(room_type.base_price) * nights * coupon.discount_value / 100, float(coupon.max_discount or 99999))
            coupon_id = coupon.id
            coupon.used_count += 1

    calc = calculate_total(float(room_type.base_price), nights, discount)

    booking = Booking(
        booking_ref=generate_booking_ref(),
        user_id=user_id,
        hotel_id=room_type.hotel_id,
        room_type_id=data["room_type_id"],
        check_in=data["check_in"],
        check_out=data["check_out"],
        number_of_rooms=data.get("number_of_rooms", 1),
        guests=data.get("guests", 2),
        guest_name=data.get("guest_name"),
        guest_email=data.get("guest_email"),
        guest_phone=data.get("guest_phone"),
        special_requests=data.get("special_requests"),
        base_amount=calc["base_amount"],
        tax_amount=calc["tax_amount"],
        discount_amount=calc["discount_amount"],
        coupon_id=coupon_id,
        total_amount=calc["total_amount"],
        status="pending",
        payment_status="unpaid"
    )
    db.add(booking)

    # Record coupon usage
    if coupon_id:
        db.add(CouponUsage(
            coupon_id=coupon_id,
            user_id=user_id,
            booking_id=booking.id,
            discount_amount=discount
        ))

    db.commit()
    db.refresh(booking)
    return booking, None


def get_user_bookings(db: Session, user_id: int):
    """Get all bookings for a user"""
    bookings = db.query(Booking).options(
        joinedload(Booking.hotel).joinedload(Hotel.images),
        joinedload(Booking.room_type)
    ).filter(Booking.user_id == user_id).order_by(Booking.created_at.desc()).all()

    result = []
    for b in bookings:
        primary_image = None
        if b.hotel and b.hotel.images:
            for img in b.hotel.images:
                if img.is_primary:
                    primary_image = img.image_url
                    break
            if not primary_image:
                primary_image = b.hotel.images[0].image_url

        result.append({
            "id": b.id,
            "booking_ref": b.booking_ref,
            "hotel_name": b.hotel.name if b.hotel else None,
            "hotel_image": primary_image,
            "room_type_name": b.room_type.name if b.room_type else None,
            "check_in": str(b.check_in),
            "check_out": str(b.check_out),
            "number_of_rooms": b.number_of_rooms,
            "guests": b.guests,
            "guest_name": b.guest_name,
            "base_amount": float(b.base_amount),
            "tax_amount": float(b.tax_amount),
            "discount_amount": float(b.discount_amount),
            "total_amount": float(b.total_amount),
            "status": b.status,
            "payment_status": b.payment_status,
            "created_at": str(b.created_at)
        })
    return result


def cancel_booking(db: Session, booking_id: int, reason: str = None):
    """Cancel a booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        return None, "Booking not found"
    if booking.status == "cancelled":
        return None, "Booking already cancelled"

    booking.status = "cancelled"
    booking.cancelled_at = datetime.utcnow()
    booking.cancellation_reason = reason

    # Calculate refund (full refund if cancelled 24h before)
    hours_before = (booking.check_in - date.today()).days * 24
    if hours_before >= 24:
        booking.refund_amount = float(booking.total_amount)
    else:
        booking.refund_amount = float(booking.total_amount) * 0.5

    db.commit()
    return booking, None


def get_owner_bookings(db: Session, owner_id: int):
    """Get bookings for owner's hotels"""
    bookings = db.query(Booking).join(Booking.hotel).filter(
        Booking.hotel.has(owner_id=owner_id)
    ).options(
        joinedload(Booking.room_type),
        joinedload(Booking.user)
    ).order_by(Booking.created_at.desc()).all()

    return [
        {
            "id": b.id,
            "booking_ref": b.booking_ref,
            "hotel_name": b.hotel.name if b.hotel else None,
            "room_type_name": b.room_type.name if b.room_type else None,
            "guest_name": b.guest_name or (b.user.full_name if b.user else "N/A"),
            "check_in": str(b.check_in),
            "check_out": str(b.check_out),
            "total_amount": float(b.total_amount),
            "status": b.status,
            "payment_status": b.payment_status,
            "created_at": str(b.created_at)
        }
        for b in bookings
    ]