"""Coupon service"""
from sqlalchemy.orm import Session
from datetime import date
from app.models import Coupon


def validate_coupon(db: Session, code: str, booking_amount: float):
    """Validate a coupon code"""
    coupon = db.query(Coupon).filter(
        Coupon.code == code.upper(),
        Coupon.is_active == True
    ).first()

    if not coupon:
        return None, "Invalid coupon code"

    if coupon.valid_until and coupon.valid_until < date.today():
        return None, "Coupon has expired"

    if coupon.usage_limit > 0 and coupon.used_count >= coupon.usage_limit:
        return None, "Coupon usage limit reached"

    if booking_amount < float(coupon.min_booking_amount):
        return None, f"Minimum booking amount of ₹{coupon.min_booking_amount} required"

    # Calculate discount
    if coupon.discount_type == "fixed":
        discount = float(coupon.discount_value)
    else:
        discount = booking_amount * float(coupon.discount_value) / 100
        if coupon.max_discount:
            discount = min(discount, float(coupon.max_discount))

    return {
        "coupon_id": coupon.id,
        "code": coupon.code,
        "discount_type": coupon.discount_type,
        "discount_value": float(coupon.discount_value),
        "discount_amount": round(discount, 2),
        "final_amount": booking_amount - round(discount, 2),
        "description": coupon.description
    }, None


def get_active_coupons(db: Session):
    """Get all active coupons"""
    return db.query(Coupon).filter(
        Coupon.is_active == True
    ).all()