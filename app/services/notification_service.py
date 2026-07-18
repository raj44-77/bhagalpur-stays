"""Notification service"""
from sqlalchemy.orm import Session
from app.models import Notification


def create_notification(db: Session, user_id: int, title: str, message: str, ntype: str = "system", link: str = None):
    """Create a notification for a user"""
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=ntype,
        link_url=link
    )
    db.add(notif)
    db.commit()
    return notif


def get_user_notifications(db: Session, user_id: int, unread_only: bool = False):
    """Get notifications for a user"""
    query = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        query = query.filter(Notification.is_read == False)
    return query.order_by(Notification.created_at.desc()).limit(50).all()


def get_unread_count(db: Session, user_id: int) -> int:
    """Get unread notification count"""
    return db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).count()


def mark_as_read(db: Session, notification_id: int, user_id: int):
    """Mark a notification as read"""
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()
    if notif:
        notif.is_read = True
        db.commit()
    return notif


def mark_all_read(db: Session, user_id: int):
    """Mark all notifications as read"""
    db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()