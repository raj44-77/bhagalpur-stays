"""Hotels router"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services import hotel_service

router = APIRouter(prefix="/api/hotels", tags=["Hotels"])


@router.get("/")
def list_hotels(
    city: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    star_rating: Optional[int] = Query(None, ge=1, le=5),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get list of hotels with filters"""
    return hotel_service.get_hotels(
        db=db,
        city_slug=city,
        area_slug=area,
        min_price=min_price,
        max_price=max_price,
        star_rating=star_rating,
        category=category,
        search=search,
        skip=skip,
        limit=limit
    )


@router.get("/{slug}")
def get_hotel(slug: str, db: Session = Depends(get_db)):
    """Get hotel details by slug"""
    hotel = hotel_service.get_hotel_by_slug(db, slug)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel