"""Hotel, HotelImage, Amenity, HotelAmenity models"""
from sqlalchemy import Column, Integer, String, Boolean, Enum, Text, DECIMAL, ForeignKey, TIMESTAMP, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    area_id = Column(Integer, ForeignKey("areas.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    full_address = Column(Text, nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    star_rating = Column(Integer, default=3)
    contact_phone = Column(String(15))
    contact_email = Column(String(150))
    check_in_time = Column(Time, default='14:00:00')
    check_out_time = Column(Time, default='11:00:00')
    cancellation_hours = Column(Integer, default=24)
    status = Column(Enum('draft', 'pending', 'approved', 'rejected', 'suspended'), default='draft')
    is_featured = Column(Boolean, default=False)
    total_rooms = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    owner = relationship("User", back_populates="hotels")
    city = relationship("City", back_populates="hotels")
    area = relationship("Area", back_populates="hotels")
    images = relationship("HotelImage", back_populates="hotel")
    amenities = relationship("HotelAmenity", back_populates="hotel")
    room_types = relationship("RoomType", back_populates="hotel")
    bookings = relationship("Booking", back_populates="hotel")
    reviews = relationship("Review", back_populates="hotel")
    wishlists = relationship("Wishlist", back_populates="hotel")


class HotelImage(Base):
    __tablename__ = "hotel_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(500), nullable=False)
    caption = Column(String(200))
    sort_order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    hotel = relationship("Hotel", back_populates="images")


class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    icon = Column(String(50))
    category = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    hotels = relationship("HotelAmenity", back_populates="amenity")


class HotelAmenity(Base):
    __tablename__ = "hotel_amenities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False)
    amenity_id = Column(Integer, ForeignKey("amenities.id", ondelete="CASCADE"), nullable=False)
    is_available = Column(Boolean, default=True)
    extra_charge = Column(DECIMAL(10, 2), default=0)

    hotel = relationship("Hotel", back_populates="amenities")
    amenity = relationship("Amenity", back_populates="hotels")