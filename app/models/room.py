"""RoomType, RoomImage, RoomInventory models"""
from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    room_size_sqft = Column(Integer)
    bed_type = Column(String(50))
    max_guests = Column(Integer, default=2)
    base_price = Column(DECIMAL(10, 2), nullable=False)
    extra_bed_price = Column(DECIMAL(10, 2), default=0)
    total_rooms = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    hotel = relationship("Hotel", back_populates="room_types")
    images = relationship("RoomImage", back_populates="room_type")
    inventory = relationship("RoomInventory", back_populates="room_type")
    bookings = relationship("Booking", back_populates="room_type")


class RoomImage(Base):
    __tablename__ = "room_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(500), nullable=False)
    caption = Column(String(200))
    sort_order = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    room_type = relationship("RoomType", back_populates="images")


class RoomInventory(Base):
    __tablename__ = "room_inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    available_rooms = Column(Integer, nullable=False, default=0)
    price_override = Column(DECIMAL(10, 2))
    is_available = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    room_type = relationship("RoomType", back_populates="inventory")