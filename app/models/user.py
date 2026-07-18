"""User, RefreshToken, PasswordReset, OwnerDetail models"""
from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(15), unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('guest', 'owner', 'admin'), default='guest')
    avatar_url = Column(String(500))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    owner_detail = relationship("OwnerDetail", back_populates="user", uselist=False)
    hotels = relationship("Hotel", back_populates="owner")
    bookings = relationship("Booking", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    wishlists = relationship("Wishlist", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class OwnerDetail(Base):
    __tablename__ = "owner_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    business_name = Column(String(150))
    gst_number = Column(String(20))
    pan_number = Column(String(15))
    aadhaar_number = Column(String(20))
    address = Column(Text)
    document_url = Column(String(500))
    verification_status = Column(Enum('pending', 'verified', 'rejected'), default='pending')
    verified_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    user = relationship("User", back_populates="owner_detail")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(500), unique=True, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(500), unique=True, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())