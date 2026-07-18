"""City and Area models"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    state = Column(String(100), default='Bihar')
    slug = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    areas = relationship("Area", back_populates="city")
    hotels = relationship("Hotel", back_populates="city")


class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    slug = Column(String(150), nullable=False)
    pincode = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    city = relationship("City", back_populates="areas")
    hotels = relationship("Hotel", back_populates="area")