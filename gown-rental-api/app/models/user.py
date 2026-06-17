import enum

from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    BRIDE = "bride"
    CONSULTANT = "consultant"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.BRIDE)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    appointments_as_bride = relationship("Appointment", back_populates="bride", foreign_keys="Appointment.bride_id")
    appointments_as_consultant = relationship("Appointment", back_populates="consultant", foreign_keys="Appointment.consultant_id")
    rental_orders = relationship("RentalOrder", back_populates="bride", foreign_keys="RentalOrder.bride_id")
