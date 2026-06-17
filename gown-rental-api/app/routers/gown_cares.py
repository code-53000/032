from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import GownCare, CareStatus, Gown, GownStatus, User, UserRole
from app.schemas.gown_care import GownCareCreate, GownCareUpdate, GownCareOut
from app.utils.auth import get_current_user, require_role

router = APIRouter(prefix="/api/gown-cares", tags=["gown-cares"])


@router.get("/", response_model=List[GownCareOut])
def list_gown_cares(
    gown_id: Optional[int] = None,
    status: Optional[CareStatus] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CONSULTANT)),
):
    query = db.query(GownCare)
    if gown_id:
        query = query.filter(GownCare.gown_id == gown_id)
    if status:
        query = query.filter(GownCare.status == status)
    return query.order_by(GownCare.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{care_id}", response_model=GownCareOut)
def get_gown_care(care_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.CONSULTANT))):
    care = db.query(GownCare).filter(GownCare.id == care_id).first()
    if not care:
        raise HTTPException(status_code=404, detail="Care record not found")
    return care


@router.post("/", response_model=GownCareOut)
def create_gown_care(care_in: GownCareCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.CONSULTANT))):
    gown = db.query(Gown).filter(Gown.id == care_in.gown_id).first()
    if not gown:
        raise HTTPException(status_code=404, detail="Gown not found")

    care = GownCare(
        gown_id=care_in.gown_id,
        care_type=care_in.care_type,
        notes=care_in.notes,
        cost=care_in.cost,
    )

    if care_in.care_type.value in ("cleaning", "repair"):
        gown.status = GownStatus.CLEANING if care_in.care_type.value == "cleaning" else GownStatus.REPAIR

    db.add(care)
    db.commit()
    db.refresh(care)
    return care


@router.put("/{care_id}", response_model=GownCareOut)
def update_gown_care(care_id: int, care_in: GownCareUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.CONSULTANT))):
    care = db.query(GownCare).filter(GownCare.id == care_id).first()
    if not care:
        raise HTTPException(status_code=404, detail="Care record not found")

    update_data = care_in.model_dump(exclude_unset=True)

    if care_in.status == CareStatus.IN_PROGRESS and not care.started_at:
        care.started_at = datetime.utcnow()

    if care_in.status == CareStatus.COMPLETED:
        care.completed_at = datetime.utcnow()
        gown = db.query(Gown).filter(Gown.id == care.gown_id).first()
        if gown and gown.status in (GownStatus.CLEANING, GownStatus.REPAIR):
            gown.status = GownStatus.AVAILABLE

    for k, v in update_data.items():
        setattr(care, k, v)
    db.commit()
    db.refresh(care)
    return care
