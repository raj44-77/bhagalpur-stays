from app.models import Review, Booking
def create_review(db, user_id, data):
    existing = db.query(Review).filter(Review.user_id == user_id, Review.booking_id == data["booking_id"]).first()
    if existing: return None, "Already reviewed"
    review = Review(user_id=user_id, hotel_id=data["hotel_id"], booking_id=data.get("booking_id"), rating=data["rating"], comment=data.get("comment"))
    db.add(review)
    db.commit()
    return review, None
def get_hotel_reviews(db, hotel_id, skip=0, limit=20):
    reviews = db.query(Review).filter(Review.hotel_id == hotel_id).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    from sqlalchemy import func
    total = db.query(func.count(Review.id)).filter(Review.hotel_id == hotel_id).scalar()
    return {"total": total, "reviews": [{"id": r.id, "user_name": r.user.full_name if r.user else "Guest", "rating": r.rating, "comment": r.comment, "created_at": str(r.created_at)} for r in reviews]}
