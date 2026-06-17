from datetime import date, time
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Gown, GownStatus, RentalOrder, RentalStatus, Appointment, AppointmentStatus, GownCare, CareStatus


class AvailabilityService:
    def __init__(self, db: Session):
        self.db = db

    def is_gown_rentable(self, gown_id: int) -> bool:
        gown = self.db.query(Gown).filter(Gown.id == gown_id).first()
        if not gown:
            return False
        return gown.status == GownStatus.AVAILABLE

    def is_gown_available_for_date_range(
        self, gown_id: int, start_date: date, end_date: date, exclude_order_id: Optional[int] = None
    ) -> bool:
        if not self.is_gown_rentable(gown_id):
            return False

        query = self.db.query(RentalOrder).filter(
            RentalOrder.gown_id == gown_id,
            RentalOrder.status.in_([RentalStatus.PENDING, RentalStatus.ACTIVE]),
            RentalOrder.pickup_date <= end_date,
            RentalOrder.return_date >= start_date,
        )
        if exclude_order_id:
            query = query.filter(RentalOrder.id != exclude_order_id)

        conflict = query.first()
        return conflict is None

    def is_gown_available_for_appointment(
        self, gown_id: int, appointment_date: date, start_time: time, end_time: time, exclude_appointment_id: Optional[int] = None
    ) -> bool:
        query = self.db.query(Appointment).filter(
            Appointment.gown_id == gown_id,
            Appointment.appointment_date == appointment_date,
            Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]),
            Appointment.start_time < end_time,
            Appointment.end_time > start_time,
        )
        if exclude_appointment_id:
            query = query.filter(Appointment.id != exclude_appointment_id)

        conflict = query.first()
        return conflict is None

    def has_active_care(self, gown_id: int) -> bool:
        return self.db.query(GownCare).filter(
            GownCare.gown_id == gown_id,
            GownCare.status.in_([CareStatus.PENDING, CareStatus.IN_PROGRESS]),
        ).first() is not None

    def get_gown_availability_summary(self, gown_id: int, target_date: date) -> dict:
        gown = self.db.query(Gown).filter(Gown.id == gown_id).first()
        if not gown:
            return {"available": False, "reason": "gown_not_found"}

        if gown.status == GownStatus.RETIRED:
            return {"available": False, "reason": "retired"}
        if gown.status == GownStatus.REPAIR:
            return {"available": False, "reason": "under_repair"}
        if gown.status == GownStatus.CLEANING:
            return {"available": False, "reason": "cleaning"}
        if gown.status == GownStatus.RENTED:
            rental = self.db.query(RentalOrder).filter(
                RentalOrder.gown_id == gown_id,
                RentalOrder.status.in_([RentalStatus.PENDING, RentalStatus.ACTIVE]),
                RentalOrder.pickup_date <= target_date,
                RentalOrder.return_date >= target_date,
            ).first()
            if rental:
                return {"available": False, "reason": "rented", "return_date": rental.return_date.isoformat()}

        return {"available": True, "reason": None}
