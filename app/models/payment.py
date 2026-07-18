"""Payment model"""
from sqlalchemy import Column, Integer, String, Enum, DECIMAL, JSON, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(Enum('upi', 'card', 'netbanking', 'wallet', 'cash', 'pay_at_hotel'), default='pay_at_hotel')
    transaction_id = Column(String(200))
    gateway_response = Column(JSON)
    status = Column(Enum('pending', 'success', 'failed', 'refunded'), default='pending')
    paid_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    booking = relationship("Booking", back_populates="payment")