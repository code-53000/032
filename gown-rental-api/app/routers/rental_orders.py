from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RentalOrder, RentalStatus, Gown, GownStatus, User, UserRole
from app.schemas.rental_order import RentalOrderCreate, RentalOrderUpdate, RentalOrderOut
from app.services.availability import AvailabilityService
from app.utils.auth import get_current_user, require_role

router = APIRouter(prefix="/api/rental-orders", tags=["rental-orders"])


@router.get("/", response_model=List[RentalOrderOut])
def list_rental_orders(
    status: Optional[RentalStatus] = None,
    gown_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(RentalOrder)
    if current_user.role == UserRole.BRIDE:
        query = query.filter(RentalOrder.bride_id == current_user.id)
    if status:
        query = query.filter(RentalOrder.status == status)
    if gown_id:
        query = query.filter(RentalOrder.gown_id == gown_id)
    return query.order_by(RentalOrder.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{order_id}", response_model=RentalOrderOut)
def get_rental_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(RentalOrder).filter(RentalOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Rental order not found")
    if current_user.role == UserRole.BRIDE and order.bride_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return order


@router.post("/", response_model=RentalOrderOut)
def create_rental_order(order_in: RentalOrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    svc = AvailabilityService(db)
    if not svc.is_gown_available_for_date_range(order_in.gown_id, order_in.pickup_date, order_in.return_date):
        raise HTTPException(status_code=409, detail="Gown is not available for the requested date range")

    gown = db.query(Gown).filter(Gown.id == order_in.gown_id).first()
    if not gown:
        raise HTTPException(status_code=404, detail="Gown not found")

    days = (order_in.return_date - order_in.pickup_date).days + 1
    total_price = round(gown.rental_price * days, 2)

    order = RentalOrder(
        gown_id=order_in.gown_id,
        bride_id=current_user.id,
        pickup_date=order_in.pickup_date,
        return_date=order_in.return_date,
        total_price=total_price,
        notes=order_in.notes,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}", response_model=RentalOrderOut)
def update_rental_order(order_id: int, order_in: RentalOrderUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(RentalOrder).filter(RentalOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Rental order not found")

    if current_user.role == UserRole.BRIDE and order.bride_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    if order_in.status == RentalStatus.ACTIVE and current_user.role == UserRole.CONSULTANT:
        gown = db.query(Gown).filter(Gown.id == order.gown_id).first()
        if gown:
            gown.status = GownStatus.RENTED

    if order_in.status == RentalStatus.RETURNED:
        order.actual_return_date = order_in.actual_return_date or __import__("datetime").date.today()
        gown = db.query(Gown).filter(Gown.id == order.gown_id).first()
        if gown:
            gown.status = GownStatus.AVAILABLE

    update_data = order_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(order, k, v)
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}")
def cancel_rental_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(RentalOrder).filter(RentalOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Rental order not found")
    if order.status not in [RentalStatus.PENDING]:
        raise HTTPException(status_code=400, detail="Only pending orders can be cancelled")
    order.status = RentalStatus.RETURNED
    order.actual_return_date = __import__("datetime").date.today()
    order.notes = (order.notes or "") + " [已取消]"
    db.commit()
    return {"detail": "Rental order cancelled"}
