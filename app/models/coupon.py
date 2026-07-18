"""Coupon and CouponUsage models"""
from sqlalchemy import Column, Integer, String, Boolean, Enum, Text, DECIMAL, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    discount_type = Column(Enum('percentage', 'fixed'), nullable=False)
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    min_booking_amount = Column(DECIMAL(10, 2), default=0)
    max_discount = Column(DECIMAL(10, 2))
    usage_limit = Column(Integer, default=0)
    used_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    valid_from = Column(Date)
    valid_until = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


class CouponUsage(Base):
    __tablename__ = "coupon_usages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    discount_amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())