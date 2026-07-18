"""Hotel service"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models import Hotel, HotelImage, HotelAmenity, Amenity, RoomType, Review, City, Area
from app.schemas.hotels import HotelCreateRequest, HotelUpdateRequest


def get_hotels(
    db: Session,
    city_slug: str = None,
    area_slug: str = None,
    min_price: float = None,
    max_price: float = None,
    star_rating: int = None,
    category: str = None,
    search: str = None,
    status: str = "approved",
    skip: int = 0,
    limit: int = 20
):
    """Get filtered list of hotels"""
    query = db.query(Hotel).options(
        joinedload(Hotel.images),
        joinedload(Hotel.city),
        joinedload(Hotel.area)
    ).filter(Hotel.status == status)

    if city_slug:
        query = query.join(City).filter(City.slug == city_slug)

    if area_slug:
        query = query.join(Area).filter(Area.slug == area_slug)

    if star_rating:
        query = query.filter(Hotel.star_rating >= star_rating)

    if search:
        query = query.filter(
            (Hotel.name.ilike(f"%{search}%")) |
            (Hotel.description.ilike(f"%{search}%"))
        )

    total = query.count()
    hotels = query.offset(skip).limit(limit).all()

    result = []
    for h in hotels:
        min_price_query = db.query(func.min(RoomType.base_price)).filter(
            RoomType.hotel_id == h.id, RoomType.is_active == True
        ).scalar()

        avg_rating = db.query(func.avg(Review.rating)).filter(
            Review.hotel_id == h.id, Review.is_active == True
        ).scalar()

        review_count = db.query(func.count(Review.id)).filter(
            Review.hotel_id == h.id, Review.is_active == True
        ).scalar()

        primary_image = None
        for img in h.images:
            if img.is_primary:
                primary_image = img.image_url
                break
        if not primary_image and h.images:
            primary_image = h.images[0].image_url

        result.append({
            "id": h.id,
            "name": h.name,
            "slug": h.slug,
            "star_rating": h.star_rating,
            "status": h.status,
            "is_featured": h.is_featured,
            "city_name": h.city.name if h.city else None,
            "area_name": h.area.name if h.area else None,
            "primary_image": primary_image,
            "avg_rating": round(float(avg_rating), 1) if avg_rating else None,
            "review_count": review_count or 0,
            "min_price": float(min_price_query) if min_price_query else None,
        })

    return {"total": total, "hotels": result}


def get_hotel_by_slug(db: Session, slug: str):
    """Get hotel details by slug"""
    hotel = db.query(Hotel).options(
        joinedload(Hotel.images),
        joinedload(Hotel.city),
        joinedload(Hotel.area),
        joinedload(Hotel.amenities).joinedload(HotelAmenity.amenity),
        joinedload(Hotel.room_types),
    ).filter(Hotel.slug == slug).first()

    if not hotel:
        return None

    amenities = []
    for ha in hotel.amenities:
        if ha.amenity:
            amenities.append({
                "id": ha.amenity.id,
                "name": ha.amenity.name,
                "icon": ha.amenity.icon,
                "category": ha.amenity.category,
            })

    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.hotel_id == hotel.id, Review.is_active == True
    ).scalar()

    review_count = db.query(func.count(Review.id)).filter(
        Review.hotel_id == hotel.id, Review.is_active == True
    ).scalar()

    min_price = db.query(func.min(RoomType.base_price)).filter(
        RoomType.hotel_id == hotel.id, RoomType.is_active == True
    ).scalar()

    return {
        "id": hotel.id,
        "name": hotel.name,
        "slug": hotel.slug,
        "description": hotel.description,
        "full_address": hotel.full_address,
        "star_rating": hotel.star_rating,
        "contact_phone": hotel.contact_phone,
        "contact_email": hotel.contact_email,
        "check_in_time": str(hotel.check_in_time) if hotel.check_in_time else None,
        "check_out_time": str(hotel.check_out_time) if hotel.check_out_time else None,
        "cancellation_hours": hotel.cancellation_hours,
        "status": hotel.status,
        "is_featured": hotel.is_featured,
        "total_rooms": hotel.total_rooms,
        "city_name": hotel.city.name if hotel.city else None,
        "area_name": hotel.area.name if hotel.area else None,
        "images": [{"id": img.id, "image_url": img.image_url, "caption": img.caption, "is_primary": img.is_primary} for img in hotel.images],
        "amenities": amenities,
        "room_types": [
            {
                "id": rt.id,
                "name": rt.name,
                "description": rt.description,
                "room_size_sqft": rt.room_size_sqft,
                "bed_type": rt.bed_type,
                "max_guests": rt.max_guests,
                "base_price": float(rt.base_price),
                "extra_bed_price": float(rt.extra_bed_price),
                "total_rooms": rt.total_rooms,
            }
            for rt in hotel.room_types if rt.is_active
        ],
        "avg_rating": round(float(avg_rating), 1) if avg_rating else None,
        "review_count": review_count or 0,
        "min_price": float(min_price) if min_price else None,
    }


def create_hotel(db: Session, owner_id: int, data: HotelCreateRequest):
    """Create a new hotel"""
    slug = data.name.lower().replace(" ", "-").replace(",", "")
    hotel = Hotel(
        owner_id=owner_id,
        name=data.name,
        slug=slug,
        city_id=data.city_id,
        area_id=data.area_id,
        description=data.description,
        full_address=data.full_address,
        star_rating=data.star_rating,
        contact_phone=data.contact_phone,
        contact_email=data.contact_email,
        status="pending"
    )
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    return hotel


def update_hotel(db: Session, hotel_id: int, data: HotelUpdateRequest):
    """Update hotel details"""
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(hotel, key, value)

    db.commit()
    db.refresh(hotel)
    return hotel