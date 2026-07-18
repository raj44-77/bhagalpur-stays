"""Reviews router"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models import User
from app.services import review_service

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


class ReviewCreate(BaseModel):
    hotel_id: int
    booking_id: int
    rating: int
    cleanliness_rating: Optional[int] = None
    service_rating: Optional[int] = None
    comfort_rating: Optional[int] = None
    value_rating: Optional[int] = None
    location_rating: Optional[int] = None
    title: Optional[str] = None
    comment: Optional[str] = None


@router.post("/")
def submit_review(data: ReviewCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Submit a hotel review"""
    review, error = review_service.create_review(db, current_user.id, data.dict())
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Review submitted", "id": review.id}


@router.get("/hotel/{hotel_id}")
def get_reviews(hotel_id: int, skip: int = Query(0), limit: int = Query(20), db: Session = Depends(get_db)):
    """Get reviews for a hotel"""
    return review_service.get_hotel_reviews(db, hotel_id, skip, limit)