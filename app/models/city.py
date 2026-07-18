from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    state = Column(String(100), default='Bihar')
    slug = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    hotels = relationship("Hotel", back_populates="city")
class Area(Base):
    __tablename__ = "areas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(String(150), nullable=False)
    slug = Column(String(150), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
