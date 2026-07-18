"""Notification model"""
from sqlalchemy import Column, Integer, String, Boolean, Enum, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text)
    notification_type = Column(Enum('booking', 'payment', 'review', 'promotion', 'system', 'owner'), default='system')
    is_read = Column(Boolean, default=False)
    link_url = Column(String(500))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="notifications")