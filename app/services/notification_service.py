from app.models import Notification
def get_user_notifications(db, user_id, unread_only=False):
    q = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only: q = q.filter(Notification.is_read == False)
    return q.order_by(Notification.created_at.desc()).limit(50).all()
def get_unread_count(db, user_id):
    return db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).count()
def mark_as_read(db, notification_id, user_id):
    n = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if n: n.is_read = True; db.commit()
    return n
def mark_all_read(db, user_id):
    db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).update({"is_read": True})
    db.commit()
