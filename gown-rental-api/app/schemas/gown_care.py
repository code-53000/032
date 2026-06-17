from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.models import CareType, CareStatus


class GownCareCreate(BaseModel):
    gown_id: int
    care_type: CareType
    notes: Optional[str] = ""
    cost: Optional[float] = 0.0


class GownCareUpdate(BaseModel):
    care_type: Optional[CareType] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: Optional[CareStatus] = None
    notes: Optional[str] = None
    cost: Optional[float] = None


class GownCareOut(BaseModel):
    id: int
    gown_id: int
    care_type: CareType
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: CareStatus
    notes: str
    cost: float
    created_at: datetime

    class Config:
        from_attributes = True
