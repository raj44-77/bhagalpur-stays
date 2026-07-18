"""Notifications router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models import User
from app.services import notification_service

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("/")
def my_notifications(unread_only: bool = False, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user notifications"""
    notifs = notification_service.get_user_notifications(db, current_user.id, unread_only)
    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "notification_type": n.notification_type,
            "is_read": n.is_read,
            "link_url": n.link_url,
            "created_at": str(n.created_at)
        }
        for n in notifs
    ]


@router.get("/unread-count")
def unread_count(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get unread notification count"""
    return {"unread": notification_service.get_unread_count(db, current_user.id)}


@router.post("/{notification_id}/read")
def mark_read(notification_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Mark notification as read"""
    notification_service.mark_as_read(db, notification_id, current_user.id)
    return {"message": "Marked as read"}


@router.post("/read-all")
def mark_all_read(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Mark all notifications as read"""
    notification_service.mark_all_read(db, current_user.id)
    return {"message": "All marked as read"}