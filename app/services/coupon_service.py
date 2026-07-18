from app.models import Coupon
from datetime import date
def validate_coupon(db, code, booking_amount):
    coupon = db.query(Coupon).filter(Coupon.code == code.upper(), Coupon.is_active == True).first()
    if not coupon: return None, "Invalid coupon"
    if booking_amount < float(coupon.min_booking_amount): return None, f"Minimum booking amount of Rs.{coupon.min_booking_amount} required"
    if coupon.discount_type == "fixed": discount = float(coupon.discount_value)
    else: discount = min(booking_amount * float(coupon.discount_value) / 100, float(coupon.max_discount or 99999))
    return {"coupon_id": coupon.id, "code": coupon.code, "discount_type": coupon.discount_type, "discount_amount": round(discount, 2)}, None
def get_active_coupons(db):
    return db.query(Coupon).filter(Coupon.is_active == True).all()
