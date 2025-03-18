from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import schemas
from database import get_db
from services import booking_service, payment_service
import models

router = APIRouter()

@router.post("/", response_model=schemas.BookingOut)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    new_booking = booking_service.create_booking(db, booking)
    return new_booking

@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_service.cancel_booking(db, booking_id)
    payment_service.process_refund(db, booking_id)
    return {"detail": "Booking cancelled"}

@router.get("/{booking_id}", response_model=schemas.BookingOut)
def check_booking_status(booking_id: int, db: Session = Depends(get_db)):
    booking = booking_service.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.get("/admin/all/", response_model=List[schemas.BookingOut])
def list_bookings(
    page: int = Query(0, description="Page number (starts from 0)"),
    limit: int = Query(50, description="Number of bookings per page"),
    date: Optional[str] = Query(None, description="Filter by appointment date (YYYY-MM-DD)"),
    status: Optional[models.BookingStatus] = Query(None, description="Filter by booking status"),
    payment_status: Optional[models.PaymentStatus] = Query(None, description="Filter by payment status"),
    customer_name: Optional[str] = Query(None, description="Filter by customer name"),
    db: Session = Depends(get_db)
):
    filters = {}

    if date:
        filters["date"] = date
    if status:
        filters["status"] = status.value
    if payment_status:
        filters["payment_status"] = payment_status.value
    if customer_name:
        filters["customer_name"] = customer_name

    bookings = booking_service.get_bookings(db, page=page, limit=limit, filters=filters)

    return bookings

@router.post("/{booking_id}/complete", response_model=schemas.BookingOut)
def complete_booking(booking_id: int,
    request: schemas.CompleteBookingRequest,
    db: Session = Depends(get_db)):
    booking = booking_service.mark_booking_as_completed(db, booking_id, request.completion_notes)
    return booking