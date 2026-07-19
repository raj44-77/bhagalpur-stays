from app.models import Hotel, HotelImage, RoomType, City
def get_hotels(db, skip=0, limit=20, **kwargs):
    hotels = db.query(Hotel).filter(Hotel.status == 'approved').offset(skip).limit(limit).all()
    result = []
    for h in hotels:
        images = db.query(HotelImage).filter(HotelImage.hotel_id == h.id).all()
        min_price = db.query(RoomType).filter(RoomType.hotel_id == h.id).first()
        city = db.query(City).filter(City.id == h.city_id).first()
        result.append({
            "id": h.id, "name": h.name, "slug": h.slug, "star_rating": h.star_rating,
            "status": h.status, "is_featured": h.is_featured,
            "city_name": city.name if city else None,
            "primary_image": images[0].image_url if images else None,
            "min_price": float(min_price.base_price) if min_price else None,
            "avg_rating": None, "review_count": 0
        })
    return {"total": len(result), "hotels": result}
def get_hotel_by_slug(db, slug):
    h = db.query(Hotel).filter(Hotel.slug == slug).first()
    if not h: return None
    images = db.query(HotelImage).filter(HotelImage.hotel_id == h.id).all()
    rooms = db.query(RoomType).filter(RoomType.hotel_id == h.id).all()
    city = db.query(City).filter(City.id == h.city_id).first()
    return {
        "id": h.id, "name": h.name, "slug": h.slug, "description": h.description,
        "full_address": h.full_address, "star_rating": h.star_rating,
        "city_name": city.name if city else None,
        "images": [{"id": i.id, "image_url": i.image_url, "is_primary": i.is_primary} for i in images],
        "room_types": [{"id": r.id, "name": r.name, "bed_type": r.bed_type, "max_guests": r.max_guests, "base_price": float(r.base_price), "total_rooms": r.total_rooms} for r in rooms],
        "min_price": float(rooms[0].base_price) if rooms else None
    }