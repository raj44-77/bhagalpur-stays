"""Room service"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import date, timedelta
from app.models import RoomType, RoomImage, RoomInventory, Hotel, Booking


def get_room_types(db: Session, hotel_id: int):
    """Get all room types for a hotel"""
    return db.query(RoomType).options(
        joinedload(RoomType.images)
    ).filter(
        RoomType.hotel_id == hotel_id,
        RoomType.is_active == True
    ).all()


def get_room_type(db: Session, room_type_id: int):
    """Get a single room type with details"""
    return db.query(RoomType).options(
        joinedload(RoomType.images)
    ).filter(RoomType.id == room_type_id).first()


def create_room_type(db: Session, hotel_id: int, data: dict):
    """Create a new room type"""
    room = RoomType(
        hotel_id=hotel_id,
        name=data.get("name"),
        description=data.get("description"),
        room_size_sqft=data.get("room_size_sqft"),
        bed_type=data.get("bed_type"),
        max_guests=data.get("max_guests", 2),
        base_price=data.get("base_price"),
        extra_bed_price=data.get("extra_bed_price", 0),
        total_rooms=data.get("total_rooms", 1)
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


def check_availability(db: Session, room_type_id: int, check_in: date, check_out: date):
    """Check room availability for given dates"""
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        return {"available": False, "message": "Room type not found"}

    nights = (check_out - check_in).days
    if nights < 1:
        return {"available": False, "message": "Invalid dates"}

    # Count existing bookings for these dates
    booked_rooms = db.query(func.count(Booking.id)).filter(
        Booking.room_type_id == room_type_id,
        Booking.status.in_(["pending", "confirmed", "checked_in"]),
        Booking.check_in < check_out,
        Booking.check_out > check_in
    ).scalar() or 0

    available = room_type.total_rooms - booked_rooms
    total_price = float(room_type.base_price) * nights

    return {
        "available": available > 0,
        "available_rooms": available,
        "total_rooms": room_type.total_rooms,
        "price_per_night": float(room_type.base_price),
        "total_price": total_price,
        "nights": nights,
        "room_type": room_type.name
    }


def seed_rooms_for_hotels(db: Session):
    """Seed demo room types for all hotels"""
    hotels = db.query(Hotel).all()
    
    room_templates = {
        5: [  # 5-star
            {"name": "Deluxe Room", "bed_type": "King", "max_guests": 2, "base_price": 4899, "total_rooms": 12},
            {"name": "Executive Suite", "bed_type": "King + Sofa", "max_guests": 3, "base_price": 6499, "total_rooms": 8},
            {"name": "Riverfront Villa", "bed_type": "King + Twin", "max_guests": 4, "base_price": 9999, "total_rooms": 4},
        ],
        4: [  # 4-star
            {"name": "Superior Room", "bed_type": "Queen", "max_guests": 2, "base_price": 3499, "total_rooms": 10},
            {"name": "Premium Suite", "bed_type": "King", "max_guests": 3, "base_price": 5499, "total_rooms": 6},
        ],
        3: [  # 3-star
            {"name": "Standard Room", "bed_type": "Queen", "max_guests": 2, "base_price": 1899, "total_rooms": 10},
            {"name": "Deluxe Room", "bed_type": "King", "max_guests": 2, "base_price": 2699, "total_rooms": 5},
        ],
        2: [  # 2-star
            {"name": "Budget Room", "bed_type": "Double", "max_guests": 2, "base_price": 999, "total_rooms": 6},
        ],
    }

    count = 0
    for hotel in hotels:
        existing = db.query(RoomType).filter(RoomType.hotel_id == hotel.id).count()
        if existing > 0:
            continue

        templates = room_templates.get(hotel.star_rating, room_templates[3])
        for tpl in templates:
            room = RoomType(
                hotel_id=hotel.id,
                name=tpl["name"],
                description=f"{tpl['bed_type']} bed, max {tpl['max_guests']} guests",
                bed_type=tpl["bed_type"],
                max_guests=tpl["max_guests"],
                base_price=tpl["base_price"],
                total_rooms=tpl["total_rooms"]
            )
            db.add(room)
            count += 1

    db.commit()
    return count