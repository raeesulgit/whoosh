from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
from services import booking_service
from typing import Optional
import logging

logger = logging.getLogger("uvicorn")  # Use the existing Uvicorn logger

def fetch_and_validate_booking(
    db: Session,
    booking_id: int,
    required_status: Optional[models.BookingStatus] = None,
    disallowed_statuses: Optional[list[models.BookingStatus]] = None,
    required_payment_status: Optional[models.PaymentStatus] = None,
    disallowed_payment_statuses: Optional[list[models.PaymentStatus]] = None,
) -> models.Booking:
    """General-purpose booking validator to check existence, status, and payment conditions."""

    booking = booking_service.get_booking(db, booking_id)
    if not booking:
        msg = f"Booking {booking_id} not found"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    if required_status and booking.status != required_status:
        msg = f"Booking {booking_id} must be in status '{required_status}' but found '{booking.status}'"
        logger.warning(msg)
        raise HTTPException(status_code=400, detail=msg)

    if disallowed_statuses and booking.status in disallowed_statuses:
        msg = f"Booking {booking_id} has invalid status '{booking.status}'"
        logger.warning(msg)
        raise HTTPException(status_code=400, detail=msg)

    if required_payment_status and booking.payment_status != required_payment_status:
        msg = f"Booking {booking_id} must have payment status '{required_payment_status}' but found '{booking.payment_status}'"
        logger.warning(msg)
        raise HTTPException(status_code=400, detail=msg)

    if disallowed_payment_statuses and booking.payment_status in disallowed_payment_statuses:
        msg = f"Booking {booking_id} has disallowed payment status '{booking.payment_status}'"
        logger.warning(msg)
        raise HTTPException(status_code=400, detail=msg)

    return booking
