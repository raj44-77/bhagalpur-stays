from app.models import Hotel, User, Booking, Review
from sqlalchemy import func
from datetime import datetime, timedelta
def get_admin_dashboard(db):
    total_hotels = db.query(func.count(Hotel.id)).scalar() or 0
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
    total_bookings = db.query(func.count(Booking.id)).scalar() or 0
    revenue = db.query(func.sum(Booking.total_amount)).filter(Booking.payment_status == "paid").scalar() or 0
    weekly = []
    for i in range(6, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)
        count = db.query(func.count(Booking.id)).filter(func.date(Booking.created_at) == day).scalar() or 0
        weekly.append({"label": day.strftime("%a"), "value": count})
    recent = db.query(Booking).order_by(Booking.created_at.desc()).limit(5).all()
    return {"kpis": {"total_hotels": total_hotels, "active_users": active_users, "total_bookings": total_bookings, "monthly_revenue": float(revenue), "pending_approvals": 0}, "weekly_bookings": weekly, "recent_bookings": [{"id": b.id, "booking_ref": b.booking_ref, "hotel_name": db.query(Hotel).filter(Hotel.id == b.hotel_id).first().name if db.query(Hotel).filter(Hotel.id == b.hotel_id).first() else "N/A", "total_amount": float(b.total_amount), "status": b.status} for b in recent]}
def get_owner_dashboard(db, owner_id):
    hotels = db.query(Hotel).filter(Hotel.owner_id == owner_id).all()
    hotel_ids = [h.id for h in hotels]
    if not hotel_ids: return {"kpis": {}, "recent_bookings": []}
    total_bookings = db.query(func.count(Booking.id)).filter(Booking.hotel_id.in_(hotel_ids)).scalar() or 0
    revenue = db.query(func.sum(Booking.total_amount)).filter(Booking.hotel_id.in_(hotel_ids), Booking.payment_status == "paid").scalar() or 0
    recent = db.query(Booking).filter(Booking.hotel_id.in_(hotel_ids)).order_by(Booking.created_at.desc()).limit(20).all()
    return {"kpis": {"total_bookings": total_bookings, "monthly_revenue": float(revenue), "avg_rating": 0, "total_hotels": len(hotel_ids)}, "recent_bookings": [{"id": b.id, "booking_ref": b.booking_ref, "guest_name": b.guest_name or "N/A", "check_in": str(b.check_in), "total_amount": float(b.total_amount), "status": b.status, "payment_status": b.payment_status} for b in recent]}
