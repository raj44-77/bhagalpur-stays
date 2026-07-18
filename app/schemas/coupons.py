"""Coupon schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class CouponValidateRequest(BaseModel):
    code: str
    booking_amount: float


class CouponResponse(BaseModel):
    id: int
    code: str
    description: Optional[str] = None
    discount_type: str
    discount_value: float
    min_booking_amount: float
    max_discount: Optional[float] = None
    is_active: bool
    valid_until: Optional[date] = None

    class Config:
        from_attributes = True


class CouponApplyResponse(BaseModel):
    coupon_id: int
    code: str
    discount_type: str
    discount_amount: float
    final_amount: float
    message: str