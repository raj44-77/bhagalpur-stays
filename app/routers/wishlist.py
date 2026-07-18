"""Wishlist router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models import User
from app.services import wishlist_service

router = APIRouter(prefix="/api/wishlist", tags=["Wishlist"])


@router.get("/")
def my_wishlist(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's wishlist"""
    return wishlist_service.get_user_wishlist(db, current_user.id)


@router.post("/{hotel_id}")
def add_wishlist(hotel_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Add hotel to wishlist"""
    result, error = wishlist_service.add_to_wishlist(db, current_user.id, hotel_id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Added to wishlist"}


@router.delete("/{hotel_id}")
def remove_wishlist(hotel_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Remove hotel from wishlist"""
    wishlist_service.remove_from_wishlist(db, current_user.id, hotel_id)
    return {"message": "Removed from wishlist"}