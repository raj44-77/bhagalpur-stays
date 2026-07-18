"""Dashboard service"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models import Hotel, User, Booking, Review, Payment
def get_admin_dashboard(db: Session):
    """Get admin dashboard stats"""
    total_hotels = db.query(func.count(Hotel.id)).scalar() or 0
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
    total_bookings = db.query(func.count(Booking.id)).scalar() or 0
    pending_approvals = db.query(func.count(Hotel.id)).filter(Hotel.status == "pending").scalar() or 0
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    revenue = db.query(func.sum(Booking.total_amount)).filter(
        Booking.payment_status == "paid",
        Booking.updated_at >= month_start
    ).scalar() or 0
    weekly = []
    for i in range(6, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)
        count = db.query(func.count(Booking.id)).filter(
            func.date(Booking.created_at) == day
        ).scalar() or 0
        weekly.append({"label": day.strftime("%a"), "value": count})
    recent = db.query(Booking).order_by(Booking.created_at.desc()).limit(5).all()
    recent_list = [
        {
            "id": b.id,
            "booking_ref": b.booking_ref,
            "hotel_name": b.hotel.name if b.hotel else "N/A",
            "total_amount": float(b.total_amount),
            "status": b.status,
            "created_at": str(b.created_at)
        }
        for b in recent
    ]
    return {
        "kpis": {
            "total_hotels": total_hotels,
            "active_users": active_users,
            "total_bookings": total_bookings,
            "monthly_revenue": float(revenue),
            "pending_approvals": pending_approvals
        },
        "weekly_bookings": weekly,
        "recent_bookings": recent_list
    }
def get_owner_dashboard(db: Session, owner_id: int):
    """Get hotel owner dashboard stats"""
    hotels = db.query(Hotel.id).filter(Hotel.owner_id == owner_id).all()
    hotel_ids = [h.id for h in hotels]
    if not hotel_ids:
        return {"kpis": {}, "recent_bookings": []}
    total_bookings = db.query(func.count(Booking.id)).filter(
        Booking.hotel_id.in_(hotel_ids)
    ).scalar() or 0
    paid_revenue = db.query(func.sum(Booking.total_amount)).filter(
        Booking.hotel_id.in_(hotel_ids),
        Booking.payment_status == "paid"
    ).scalar() or 0
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.hotel_id.in_(hotel_ids)
    ).scalar() or 0
    recent = db.query(Booking).filter(
        Booking.hotel_id.in_(hotel_ids)
    ).order_by(Booking.created_at.desc()).limit(20).all()
    return {
        "kpis": {
            "total_bookings": total_bookings,
            "monthly_revenue": float(paid_revenue),
            "avg_rating": round(float(avg_rating), 1),
            "total_hotels": len(hotel_ids)
        },
        "recent_bookings": [
            {
                "id": b.id,
                "booking_ref": b.booking_ref,
                "guest_name": b.guest_name or "N/A",
                "room_type": b.room_type.name if b.room_type else "N/A",
                "check_in": str(b.check_in),
                "check_out": str(b.check_out),
                "total_amount": float(b.total_amount),
                "status": b.status,
                "payment_status": b.payment_status
            }
            for b in recent
        ]
    }
