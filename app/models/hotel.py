"""Hotel model - simplified for TiDB"""
from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    full_address = Column(Text, nullable=False)
    star_rating = Column(Integer, default=3)
    status = Column(String(20), default='approved')
    is_featured = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    owner = relationship("User", back_populates="hotels")
    city = relationship("City", back_populates="hotels")
    images = relationship("HotelImage", back_populates="hotel")
    room_types = relationship("RoomType", back_populates="hotel")
    bookings = relationship("Booking", back_populates="hotel")
    reviews = relationship("Review", back_populates="hotel")
    wishlists = relationship("Wishlist", back_populates="hotel")
class HotelImage(Base):
    __tablename__ = "hotel_images"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    hotel = relationship("Hotel", back_populates="images")
class RoomType(Base):
    __tablename__ = "room_types"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(150), nullable=False)
    bed_type = Column(String(50))
    max_guests = Column(Integer, default=2)
    base_price = Column(DECIMAL(10,2), nullable=False)
    total_rooms = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    hotel = relationship("Hotel", back_populates="room_types")
    bookings = relationship("Booking", back_populates="room_type")
