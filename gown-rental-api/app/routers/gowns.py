from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Gown, GownStatus, User, UserRole
from app.schemas.gown import GownCreate, GownUpdate, GownOut
from app.services.availability import AvailabilityService
from app.utils.auth import get_current_user, require_role
from datetime import date

router = APIRouter(prefix="/api/gowns", tags=["gowns"])


@router.get("/", response_model=List[GownOut])
def list_gowns(
    status: Optional[GownStatus] = None,
    style: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Gown)
    if status:
        query = query.filter(Gown.status == status)
    if style:
        query = query.filter(Gown.style == style)
    return query.offset(skip).limit(limit).all()


@router.get("/{gown_id}", response_model=GownOut)
def get_gown(gown_id: int, db: Session = Depends(get_db)):
    gown = db.query(Gown).filter(Gown.id == gown_id).first()
    if not gown:
        raise HTTPException(status_code=404, detail="Gown not found")
    return gown


@router.post("/", response_model=GownOut)
def create_gown(gown_in: GownCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.CONSULTANT))):
    gown = Gown(**gown_in.model_dump())
    db.add(gown)
    db.commit()
    db.refresh(gown)
    return gown


@router.put("/{gown_id}", response_model=GownOut)
def update_gown(gown_id: int, gown_in: GownUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.CONSULTANT))):
    gown = db.query(Gown).filter(Gown.id == gown_id).first()
    if not gown:
        raise HTTPException(status_code=404, detail="Gown not found")
    update_data = gown_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(gown, k, v)
    db.commit()
    db.refresh(gown)
    return gown


@router.delete("/{gown_id}")
def delete_gown(gown_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.CONSULTANT))):
    gown = db.query(Gown).filter(Gown.id == gown_id).first()
    if not gown:
        raise HTTPException(status_code=404, detail="Gown not found")
    gown.status = GownStatus.RETIRED
    db.commit()
    return {"detail": "Gown retired"}


@router.get("/{gown_id}/availability")
def check_availability(gown_id: int, target_date: date, db: Session = Depends(get_db)):
    svc = AvailabilityService(db)
    return svc.get_gown_availability_summary(gown_id, target_date)
