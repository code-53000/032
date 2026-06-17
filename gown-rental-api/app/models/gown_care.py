import enum

from sqlalchemy import Column, Integer, Float, Enum, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class CareType(str, enum.Enum):
    CLEANING = "cleaning"
    REPAIR = "repair"
    IRONING = "ironing"
    INSPECTION = "inspection"


class CareStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class GownCare(Base):
    __tablename__ = "gown_cares"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gown_id = Column(Integer, ForeignKey("gowns.id"), nullable=False, index=True)
    care_type = Column(Enum(CareType), nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    status = Column(Enum(CareStatus), nullable=False, default=CareStatus.PENDING)
    notes = Column(Text, default="")
    cost = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())

    gown = relationship("Gown", back_populates="care_records")
