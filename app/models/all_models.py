from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text, DECIMAL, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    email = Column(String(150), unique=True)
    phone = Column(String(15))
    password_hash = Column(String(255))
    role = Column(String(10), default='guest')
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    state = Column(String(100), default='Bihar')
    slug = Column(String(100), unique=True)
class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    city_id = Column(Integer)
    name = Column(String(200))
    slug = Column(String(200), unique=True)
    description = Column(Text)
    full_address = Column(Text)
    star_rating = Column(Integer, default=3)
    status = Column(String(20), default='approved')
    is_featured = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
class HotelImage(Base):
    __tablename__ = "hotel_images"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer)
    image_url = Column(String(500))
    is_primary = Column(Boolean, default=False)
class RoomType(Base):
    __tablename__ = "room_types"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer)
    name = Column(String(150))
    bed_type = Column(String(50))
    max_guests = Column(Integer, default=2)
    base_price = Column(DECIMAL(10,2))
    total_rooms = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    booking_ref = Column(String(20), unique=True)
    user_id = Column(Integer)
    hotel_id = Column(Integer)
    room_type_id = Column(Integer)
    check_in = Column(Date)
    check_out = Column(Date)
    guests = Column(Integer, default=2)
    guest_name = Column(String(100))
    guest_email = Column(String(150))
    guest_phone = Column(String(15))
    base_amount = Column(DECIMAL(10,2))
    tax_amount = Column(DECIMAL(10,2), default=0)
    discount_amount = Column(DECIMAL(10,2), default=0)
    total_amount = Column(DECIMAL(10,2))
    status = Column(String(20), default='pending')
    payment_status = Column(String(20), default='unpaid')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    hotel_id = Column(Integer)
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    hotel_id = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True)
    code = Column(String(50))
    discount_type = Column(String(20))
    discount_value = Column(DECIMAL(10,2))
    min_booking_amount = Column(DECIMAL(10,2), default=0)
    max_discount = Column(DECIMAL(10,2))
    is_active = Column(Boolean, default=True)
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer)
    amount = Column(DECIMAL(10,2))
    payment_method = Column(String(20), default='pay_at_hotel')
    status = Column(String(20), default='pending')
