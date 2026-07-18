"""Booking model"""
from sqlalchemy import Column, Integer, String, Enum, Text, DECIMAL, Date, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_ref = Column(String(20), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    number_of_rooms = Column(Integer, default=1)
    guests = Column(Integer, default=2)
    guest_name = Column(String(100))
    guest_email = Column(String(150))
    guest_phone = Column(String(15))
    special_requests = Column(Text)
    base_amount = Column(DECIMAL(10, 2), nullable=False)
    tax_amount = Column(DECIMAL(10, 2), default=0)
    discount_amount = Column(DECIMAL(10, 2), default=0)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled', 'no_show'), default='pending')
    payment_status = Column(Enum('unpaid', 'partial', 'paid', 'refunded'), default='unpaid')
    cancelled_at = Column(TIMESTAMP, nullable=True)
    cancellation_reason = Column(Text)
    refund_amount = Column(DECIMAL(10, 2), default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    user = relationship("User", back_populates="bookings")
    hotel = relationship("Hotel", back_populates="bookings")
    room_type = relationship("RoomType", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)
    review = relationship("Review", back_populates="booking", uselist=False)