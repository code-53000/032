from typing import Optional
from datetime import date, time, datetime

from pydantic import BaseModel

from app.models import AppointmentStatus


class AppointmentCreate(BaseModel):
    gown_id: int
    appointment_date: date
    start_time: time
    end_time: time
    notes: Optional[str] = ""


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[AppointmentStatus] = None
    consultant_id: Optional[int] = None
    notes: Optional[str] = None


class AppointmentOut(BaseModel):
    id: int
    gown_id: int
    bride_id: int
    consultant_id: Optional[int] = None
    appointment_date: date
    start_time: time
    end_time: time
    status: AppointmentStatus
    notes: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
