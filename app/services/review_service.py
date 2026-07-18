"""Review service"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Review, Booking


def create_review(db: Session, user_id: int, data: dict):
    """Submit a hotel review"""
    # Check if booking exists and is completed
    booking = db.query(Booking).filter(
        Booking.id == data["booking_id"],
        Booking.user_id == user_id,
        Booking.status == "checked_out"
    ).first()
    if not booking:
        return None, "You can only review completed stays"

    # Check for duplicate
    existing = db.query(Review).filter(
        Review.booking_id == data["booking_id"],
        Review.user_id == user_id
    ).first()
    if existing:
        return None, "You have already reviewed this stay"

    review = Review(
        user_id=user_id,
        hotel_id=data["hotel_id"],
        booking_id=data["booking_id"],
        rating=data["rating"],
        cleanliness_rating=data.get("cleanliness_rating"),
        service_rating=data.get("service_rating"),
        comfort_rating=data.get("comfort_rating"),
        value_rating=data.get("value_rating"),
        location_rating=data.get("location_rating"),
        title=data.get("title"),
        comment=data.get("comment"),
        is_verified=True
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review, None


def get_hotel_reviews(db: Session, hotel_id: int, skip: int = 0, limit: int = 20):
    """Get reviews for a hotel"""
    reviews = db.query(Review).filter(
        Review.hotel_id == hotel_id,
        Review.is_active == True
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()

    total = db.query(func.count(Review.id)).filter(
        Review.hotel_id == hotel_id,
        Review.is_active == True
    ).scalar()

    return {
        "total": total,
        "reviews": [
            {
                "id": r.id,
                "user_name": r.user.full_name if r.user else "Anonymous",
                "rating": r.rating,
                "cleanliness_rating": r.cleanliness_rating,
                "service_rating": r.service_rating,
                "comfort_rating": r.comfort_rating,
                "value_rating": r.value_rating,
                "location_rating": r.location_rating,
                "title": r.title,
                "comment": r.comment,
                "is_verified": r.is_verified,
                "created_at": str(r.created_at)
            }
            for r in reviews
        ]
    }