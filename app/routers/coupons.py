"""Coupons router"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import coupon_service

router = APIRouter(prefix="/api/coupons", tags=["Coupons"])


@router.get("/validate")
def validate_coupon(code: str = Query(...), amount: float = Query(...), db: Session = Depends(get_db)):
    """Validate a coupon code"""
    result, error = coupon_service.validate_coupon(db, code, amount)
    if error:
        return {"valid": False, "message": error}
    return {"valid": True, **result}


@router.get("/")
def active_coupons(db: Session = Depends(get_db)):
    """Get active coupons"""
    coupons = coupon_service.get_active_coupons(db)
    return [
        {
            "id": c.id,
            "code": c.code,
            "description": c.description,
            "discount_type": c.discount_type,
            "discount_value": float(c.discount_value),
            "min_booking_amount": float(c.min_booking_amount),
        }
        for c in coupons
    ]