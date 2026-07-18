"""Wishlist service"""
from sqlalchemy.orm import Session, joinedload
from app.models import Wishlist, Hotel, HotelImage


def add_to_wishlist(db: Session, user_id: int, hotel_id: int):
    """Add hotel to wishlist"""
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.hotel_id == hotel_id
    ).first()
    if existing:
        return None, "Already in wishlist"

    wishlist = Wishlist(user_id=user_id, hotel_id=hotel_id)
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)
    return wishlist, None


def remove_from_wishlist(db: Session, user_id: int, hotel_id: int):
    """Remove hotel from wishlist"""
    db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.hotel_id == hotel_id
    ).delete()
    db.commit()
    return True


def get_user_wishlist(db: Session, user_id: int):
    """Get user's wishlist with hotel details"""
    wishlist_items = (
        db.query(Wishlist)
        .options(
            joinedload(Wishlist.hotel).joinedload(Hotel.images)
        )
        .filter(Wishlist.user_id == user_id)
        .all()
    )

    result = []
    for item in wishlist_items:
        hotel = item.hotel
        if not hotel:
            continue

        image = None
        if hotel.images and len(hotel.images) > 0:
            for img in hotel.images:
                if img.is_primary:
                    image = img.image_url
                    break
            if not image:
                image = hotel.images[0].image_url

        result.append({
            "id": item.id,
            "hotel_id": hotel.id,
            "hotel_slug": hotel.slug,
            "hotel_name": hotel.name,
            "hotel_image": image,
            "added_at": item.created_at.isoformat() if item.created_at else None,
        })

    return result