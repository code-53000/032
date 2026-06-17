from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment, AppointmentStatus, User, UserRole
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentOut
from app.services.availability import AvailabilityService
from app.utils.auth import get_current_user, require_role

router = APIRouter(prefix="/api/appointments", tags=["appointments"])


@router.get("/", response_model=List[AppointmentOut])
def list_appointments(
    status: Optional[AppointmentStatus] = None,
    gown_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Appointment)
    if current_user.role == UserRole.BRIDE:
        query = query.filter(Appointment.bride_id == current_user.id)
    if status:
        query = query.filter(Appointment.status == status)
    if gown_id:
        query = query.filter(Appointment.gown_id == gown_id)
    return query.order_by(Appointment.appointment_date.desc()).offset(skip).limit(limit).all()


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    apt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if current_user.role == UserRole.BRIDE and apt.bride_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return apt


@router.post("/", response_model=AppointmentOut)
def create_appointment(apt_in: AppointmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    svc = AvailabilityService(db)
    if not svc.is_gown_available_for_appointment(apt_in.gown_id, apt_in.appointment_date, apt_in.start_time, apt_in.end_time):
        raise HTTPException(status_code=409, detail="This time slot is already booked for this gown")

    apt = Appointment(
        gown_id=apt_in.gown_id,
        bride_id=current_user.id,
        appointment_date=apt_in.appointment_date,
        start_time=apt_in.start_time,
        end_time=apt_in.end_time,
        notes=apt_in.notes,
    )
    db.add(apt)
    db.commit()
    db.refresh(apt)
    return apt


@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, apt_in: AppointmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    apt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if current_user.role == UserRole.BRIDE and apt.bride_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    if apt_in.status == AppointmentStatus.CONFIRMED and current_user.role != UserRole.CONSULTANT:
        raise HTTPException(status_code=403, detail="Only consultants can confirm appointments")

    update_data = apt_in.model_dump(exclude_unset=True)

    if apt_in.appointment_date or apt_in.start_time or apt_in.end_time:
        new_date = apt_in.appointment_date or apt.appointment_date
        new_start = apt_in.start_time or apt.start_time
        new_end = apt_in.end_time or apt.end_time
        svc = AvailabilityService(db)
        if not svc.is_gown_available_for_appointment(apt.gown_id, new_date, new_start, new_end, exclude_appointment_id=apt.id):
            raise HTTPException(status_code=409, detail="This time slot conflicts with another appointment")

    for k, v in update_data.items():
        setattr(apt, k, v)
    db.commit()
    db.refresh(apt)
    return apt


@router.delete("/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    apt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if current_user.role == UserRole.BRIDE and apt.bride_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    apt.status = AppointmentStatus.CANCELLED
    db.commit()
    return {"detail": "Appointment cancelled"}
