from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.models import GownStatus, GownStyle


class GownCreate(BaseModel):
    name: str
    designer: Optional[str] = ""
    style: GownStyle = GownStyle.A_LINE
    color: Optional[str] = "white"
    size: Optional[str] = "M"
    image_url: Optional[str] = ""
    rental_price: float
    description: Optional[str] = ""


class GownUpdate(BaseModel):
    name: Optional[str] = None
    designer: Optional[str] = None
    style: Optional[GownStyle] = None
    color: Optional[str] = None
    size: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[GownStatus] = None
    rental_price: Optional[float] = None
    description: Optional[str] = None


class GownOut(BaseModel):
    id: int
    name: str
    designer: str
    style: GownStyle
    color: str
    size: str
    image_url: str
    status: GownStatus
    rental_price: float
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
