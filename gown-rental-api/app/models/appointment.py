import enum

from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, ForeignKey, Time, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gown_id = Column(Integer, ForeignKey("gowns.id"), nullable=False, index=True)
    bride_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    consultant_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    appointment_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.PENDING)
    notes = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    gown = relationship("Gown", back_populates="appointments")
    bride = relationship("User", back_populates="appointments_as_bride", foreign_keys=[bride_id])
    consultant = relationship("User", back_populates="appointments_as_consultant", foreign_keys=[consultant_id])
