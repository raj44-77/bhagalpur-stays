"""Dashboard router"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user, get_current_admin, get_current_owner
from app.models import User
from app.services import dashboard_service

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/admin")
def admin_dashboard(current_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Admin dashboard stats"""
    return dashboard_service.get_admin_dashboard(db)


@router.get("/owner")
def owner_dashboard(current_user: User = Depends(get_current_owner), db: Session = Depends(get_db)):
    """Owner dashboard stats"""
    return dashboard_service.get_owner_dashboard(db, current_user.id)

@router.get("/audit-logs")
def get_audit_logs(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get audit logs (admin only)"""
    from app.models import AuditLog
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    total = db.query(AuditLog).count()
    
    return {
        "total": total,
        "logs": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "entity_type": log.entity_type,
                "entity_id": log.entity_id,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent[:100] if log.user_agent else None,
                "created_at": str(log.created_at)
            }
            for log in logs
        ]
    }