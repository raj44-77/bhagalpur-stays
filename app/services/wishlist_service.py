from app.models import Wishlist, Hotel
def add_to_wishlist(db, user_id, hotel_id):
    existing = db.query(Wishlist).filter(Wishlist.user_id == user_id, Wishlist.hotel_id == hotel_id).first()
    if existing: return None, "Already in wishlist"
    w = Wishlist(user_id=user_id, hotel_id=hotel_id)
    db.add(w)
    db.commit()
    return w, None
def remove_from_wishlist(db, user_id, hotel_id):
    db.query(Wishlist).filter(Wishlist.user_id == user_id, Wishlist.hotel_id == hotel_id).delete()
    db.commit()
    return True
def get_user_wishlist(db, user_id):
    items = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    return [{"id": i.id, "hotel_id": i.hotel_id, "hotel_name": i.hotel.name if i.hotel else None, "hotel_image": i.hotel.images[0].image_url if i.hotel and i.hotel.images else None, "hotel_slug": i.hotel.slug if i.hotel else None} for i in items]
