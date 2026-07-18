"""Notification schemas"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: Optional[str] = None
    notification_type: str
    is_read: bool
    link_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationCountResponse(BaseModel):
    total: int
    unread: int