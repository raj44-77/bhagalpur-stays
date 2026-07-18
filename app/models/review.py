"""Review model"""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True, unique=True)
    rating = Column(Integer, nullable=False)
    cleanliness_rating = Column(Integer)
    service_rating = Column(Integer)
    comfort_rating = Column(Integer)
    value_rating = Column(Integer)
    location_rating = Column(Integer)
    title = Column(String(200))
    comment = Column(Text)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    user = relationship("User", back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")
    booking = relationship("Booking", back_populates="review")