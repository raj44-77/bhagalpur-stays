from app.models import Wishlist, Hotel, HotelImage
def add_to_wishlist(db, user_id, hotel_id):
    from app.models import Wishlist
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
    result = []
    for i in items:
        hotel = db.query(Hotel).filter(Hotel.id == i.hotel_id).first()
        img = db.query(HotelImage).filter(HotelImage.hotel_id == i.hotel_id, HotelImage.is_primary == True).first()
        result.append({"id": i.id, "hotel_id": i.hotel_id, "hotel_name": hotel.name if hotel else None, "hotel_slug": hotel.slug if hotel else None, "hotel_image": img.image_url if img else None})
    return result
