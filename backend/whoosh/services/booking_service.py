import logging

import models, schemas
from crud import booking_crud
from services import email_service, service_service
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from schemas import BookingOut
from datetime import datetime
from helpers.booking import fetch_and_validate_booking

def create_booking(db: Session, booking_data: schemas.BookingCreate) -> models.Booking:
    """Create a new booking and trigger confirmation email."""
    service = service_service.get_service_by_name_and_vehicle(
        db,
        booking_data.service,
        booking_data.vehicle_type
    )
    if not service:
        raise ValueError(f"Service '{booking_data.service}' not found for vehicle type '{booking_data.vehicle_type}'")

    amount = service.price  # Direct from service table
    booking = booking_crud.create_booking(db, booking_data, amount)
    email_service.send_booking_email(booking)
    return booking


def get_booking(db: Session, booking_id: int) -> Optional[models.Booking]:
    """Fetch single booking by ID."""
    return booking_crud.get_booking_by_id(db, booking_id)

def cancel_booking(db: Session, booking_id: int) -> Optional[models.Booking]:
    """Cancel booking and trigger cancellation email."""
    booking = fetch_and_validate_booking(
        db, booking_id,
        required_status=models.BookingStatus.BOOKED
    )
    logging.info(f"Cancelling booking {booking_id}")
    booking = booking_crud.update_booking(db, booking, status=models.BookingStatus.CANCELLED)
    email_service.send_cancellation_email(booking)
    return booking

def get_bookings(
    db: Session,
    page: int = 0,
    limit: int = 50,
    filters: Optional[Dict[str, Any]] = None
) -> List[BookingOut]:
    offset = page * limit

    # Prepare filter arguments for the CRUD method
    filter_criteria = {}

    if filters:
        if "date" in filters:
            try:
                target_date = datetime.strptime(filters["date"], '%Y-%m-%d').date()
                start_of_day = datetime.combine(target_date, datetime.min.time())
                end_of_day = datetime.combine(target_date, datetime.max.time())
                filter_criteria["appointment_time"] = (start_of_day, end_of_day)
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD")

        if "status" in filters:
            filter_criteria["status"] = filters["status"]

        if "payment_status" in filters:
            filter_criteria["payment_status"] = filters["payment_status"]

        if "customer_name" in filters:
            filter_criteria["customer_name"] = filters["customer_name"]

    # Call the actual CRUD method
    bookings = booking_crud.get_bookings(db, offset=offset, limit=limit, filters=filter_criteria)

    return bookings

def mark_booking_as_paid(db: Session, booking_id: int) -> Optional[models.Booking]:
    """Mark booking as paid."""
    booking = fetch_and_validate_booking(
        db, booking_id,
        required_status=models.BookingStatus.BOOKED
    )
    if booking:
        booking.payment_status = models.PaymentStatus.PAID
        db.commit()
        db.refresh(booking)
    return booking

def mark_booking_as_completed(
        db: Session,
        booking_id: int,
        completion_notes: Optional[str] = None) -> Optional[models.Booking]:

    booking = fetch_and_validate_booking(
        db, booking_id,
        required_payment_status=models.PaymentStatus.PAID,
        required_status=models.BookingStatus.BOOKED
    )
    booking = booking_crud.update_booking(db, booking,
                                          status=models.BookingStatus.COMPLETED,
                                          completion_notes=completion_notes)
    return booking