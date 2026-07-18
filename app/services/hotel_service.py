"""Hotel service"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models import Hotel, HotelImage, RoomType, Review, City
def get_hotels(db, city_slug=None, area_slug=None, min_price=None, max_price=None, star_rating=None, category=None, search=None, status="approved", skip=0, limit=20):
    query = db.query(Hotel).options(joinedload(Hotel.images), joinedload(Hotel.city)).filter(Hotel.status == status)
    if city_slug: query = query.join(City).filter(City.slug == city_slug)
    if star_rating: query = query.filter(Hotel.star_rating >= star_rating)
    if search: query = query.filter(Hotel.name.ilike(f"%{search}%") | Hotel.description.ilike(f"%{search}%"))
    total = query.count()
    hotels = query.offset(skip).limit(limit).all()
    result = []
    for h in hotels:
        min_price_q = db.query(func.min(RoomType.base_price)).filter(RoomType.hotel_id == h.id, RoomType.is_active == True).scalar()
        if min_price and min_price_q and min_price_q < min_price: continue
        avg_rating = db.query(func.avg(Review.rating)).filter(Review.hotel_id == h.id).scalar()
        review_count = db.query(func.count(Review.id)).filter(Review.hotel_id == h.id).scalar()
        primary_image = None
        for img in h.images:
            if img.is_primary: primary_image = img.image_url; break
        if not primary_image and h.images: primary_image = h.images[0].image_url
        result.append({"id": h.id, "name": h.name, "slug": h.slug, "star_rating": h.star_rating, "status": h.status, "is_featured": h.is_featured, "city_name": h.city.name if h.city else None, "primary_image": primary_image, "avg_rating": round(float(avg_rating), 1) if avg_rating else None, "review_count": review_count or 0, "min_price": float(min_price_q) if min_price_q else None})
    return {"total": len(result), "hotels": result}
def get_hotel_by_slug(db, slug):
    hotel = db.query(Hotel).options(joinedload(Hotel.images), joinedload(Hotel.city), joinedload(Hotel.room_types)).filter(Hotel.slug == slug).first()
    if not hotel: return None
    avg_rating = db.query(func.avg(Review.rating)).filter(Review.hotel_id == hotel.id).scalar()
    review_count = db.query(func.count(Review.id)).filter(Review.hotel_id == hotel.id).scalar()
    min_price = db.query(func.min(RoomType.base_price)).filter(RoomType.hotel_id == hotel.id, RoomType.is_active == True).scalar()
    return {"id": hotel.id, "name": hotel.name, "slug": hotel.slug, "description": hotel.description, "full_address": hotel.full_address, "star_rating": hotel.star_rating, "status": hotel.status, "is_featured": hotel.is_featured, "city_name": hotel.city.name if hotel.city else None, "images": [{"id": img.id, "image_url": img.image_url, "is_primary": img.is_primary} for img in hotel.images], "room_types": [{"id": rt.id, "name": rt.name, "bed_type": rt.bed_type, "max_guests": rt.max_guests, "base_price": float(rt.base_price), "total_rooms": rt.total_rooms} for rt in hotel.room_types if rt.is_active], "avg_rating": round(float(avg_rating), 1) if avg_rating else None, "review_count": review_count or 0, "min_price": float(min_price) if min_price else None}
