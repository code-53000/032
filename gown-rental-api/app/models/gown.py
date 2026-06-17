import enum

from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class GownStatus(str, enum.Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    CLEANING = "cleaning"
    REPAIR = "repair"
    RETIRED = "retired"


class GownStyle(str, enum.Enum):
    A_LINE = "A-line"
    BALL_GOWN = "ball_gown"
    MERMAID = "mermaid"
    SHEATH = "sheath"
    TRUMPET = "trumpet"
    EMPIRE = "empire"
    TEA_LENGTH = "tea_length"


class Gown(Base):
    __tablename__ = "gowns"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    designer = Column(String(100), default="")
    style = Column(Enum(GownStyle), nullable=False, default=GownStyle.A_LINE)
    color = Column(String(50), default="white")
    size = Column(String(20), default="M")
    image_url = Column(String(500), default="")
    status = Column(Enum(GownStatus), nullable=False, default=GownStatus.AVAILABLE)
    rental_price = Column(Float, nullable=False, default=0.0)
    description = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    appointments = relationship("Appointment", back_populates="gown")
    rental_orders = relationship("RentalOrder", back_populates="gown")
    care_records = relationship("GownCare", back_populates="gown")
