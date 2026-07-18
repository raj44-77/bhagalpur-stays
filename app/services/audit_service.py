"""Audit logging service"""
from sqlalchemy.orm import Session
from app.models import AuditLog


def log_action(
    db: Session,
    user_id: int = None,
    action: str = "",
    entity_type: str = None,
    entity_id: int = None,
    old_values: dict = None,
    new_values: dict = None,
    ip_address: str = None,
    user_agent: str = None
):
    """Record an audit log entry"""
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(log)
    db.commit()
    return log