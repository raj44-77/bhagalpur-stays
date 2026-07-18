"""Payment schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PaymentCreateRequest(BaseModel):
    booking_id: int
    payment_method: str = Field(default="pay_at_hotel")
    amount: float = Field(..., gt=0)


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: float
    payment_method: str
    transaction_id: Optional[str] = None
    status: str
    paid_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True