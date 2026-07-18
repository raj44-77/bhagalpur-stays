"""Rooms router"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.services import room_service

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])


@router.get("/hotel/{hotel_id}")
def get_hotel_rooms(hotel_id: int, db: Session = Depends(get_db)):
    """Get all room types for a hotel"""
    rooms = room_service.get_room_types(db, hotel_id)
    return [
        {
            "id": r.id,
            "hotel_id": r.hotel_id,
            "name": r.name,
            "description": r.description,
            "bed_type": r.bed_type,
            "max_guests": r.max_guests,
            "base_price": float(r.base_price),
            "extra_bed_price": float(r.extra_bed_price),
            "total_rooms": r.total_rooms,
            "images": [{"id": img.id, "image_url": img.image_url} for img in r.images]
        }
        for r in rooms
    ]


@router.get("/{room_type_id}")
def get_room(room_type_id: int, db: Session = Depends(get_db)):
    """Get room type details"""
    room = room_service.get_room_type(db, room_type_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "id": room.id,
        "hotel_id": room.hotel_id,
        "name": room.name,
        "description": room.description,
        "bed_type": room.bed_type,
        "max_guests": room.max_guests,
        "base_price": float(room.base_price),
        "extra_bed_price": float(room.extra_bed_price),
        "total_rooms": room.total_rooms,
    }


@router.get("/{room_type_id}/availability")
def check_availability(
    room_type_id: int,
    check_in: date = Query(...),
    check_out: date = Query(...),
    db: Session = Depends(get_db)
):
    """Check room availability for given dates"""
    return room_service.check_availability(db, room_type_id, check_in, check_out)


@router.post("/seed")
def seed_rooms(db: Session = Depends(get_db)):
    """Seed demo room types for all hotels"""
    count = room_service.seed_rooms_for_hotels(db)
    return {"message": f"Seeded {count} room types"}