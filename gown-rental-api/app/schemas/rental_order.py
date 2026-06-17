from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel

from app.models import RentalStatus


class RentalOrderCreate(BaseModel):
    gown_id: int
    pickup_date: date
    return_date: date
    notes: Optional[str] = ""


class RentalOrderUpdate(BaseModel):
    pickup_date: Optional[date] = None
    return_date: Optional[date] = None
    actual_return_date: Optional[date] = None
    status: Optional[RentalStatus] = None
    consultant_id: Optional[int] = None
    notes: Optional[str] = None


class RentalOrderOut(BaseModel):
    id: int
    gown_id: int
    bride_id: int
    consultant_id: Optional[int] = None
    pickup_date: date
    return_date: date
    actual_return_date: Optional[date] = None
    status: RentalStatus
    total_price: float
    notes: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
