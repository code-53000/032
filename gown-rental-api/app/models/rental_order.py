import enum

from sqlalchemy import Column, Integer, Float, Enum, DateTime, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class RentalStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


class RentalOrder(Base):
    __tablename__ = "rental_orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gown_id = Column(Integer, ForeignKey("gowns.id"), nullable=False, index=True)
    bride_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    consultant_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    pickup_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    actual_return_date = Column(Date, nullable=True)
    status = Column(Enum(RentalStatus), nullable=False, default=RentalStatus.PENDING)
    total_price = Column(Float, nullable=False, default=0.0)
    notes = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    gown = relationship("Gown", back_populates="rental_orders")
    bride = relationship("User", back_populates="rental_orders", foreign_keys=[bride_id])
