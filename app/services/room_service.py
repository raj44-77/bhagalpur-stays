from app.models import RoomType, Booking
def get_room_types(db, hotel_id):
    return db.query(RoomType).filter(RoomType.hotel_id == hotel_id, RoomType.is_active == True).all()
def check_availability(db, room_type_id, check_in, check_out):
    room = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room: return {"available": False}
    nights = (check_out - check_in).days
    if nights < 1: return {"available": False}
    booked = db.query(Booking).filter(Booking.room_type_id == room_type_id, Booking.status.in_(["pending","confirmed"]), Booking.check_in < check_out, Booking.check_out > check_in).count() or 0
    available = room.total_rooms - booked
    return {"available": available > 0, "available_rooms": available, "price_per_night": float(room.base_price), "total_price": float(room.base_price) * nights}
