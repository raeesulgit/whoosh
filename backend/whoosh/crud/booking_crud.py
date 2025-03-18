from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import models, schemas

def create_booking(db: Session, booking_data: schemas.BookingCreate, amount: float) -> models.Booking:
    """Create a new booking."""
    db_booking = models.Booking(**booking_data.dict(), amount=amount)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_booking_by_id(db: Session, booking_id: int) -> Optional[models.Booking]:
    """Get a booking by ID."""
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def update_booking(db: Session, booking: models.Booking, **fields):
    """Generic method to update booking fields."""
    for key, value in fields.items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)
    return booking

def get_bookings(
    db: Session,
    offset: int = 0,
    limit: int = 50,
    filters: Optional[Dict[str, Any]] = None
) -> List[models.Booking]:
    query = db.query(models.Booking)

    if filters:
        if "appointment_time" in filters:
            start_of_day, end_of_day = filters["appointment_time"]
            query = query.filter(
                models.Booking.appointment_time >= start_of_day,
                models.Booking.appointment_time <= end_of_day
            )

        if "status" in filters:
            query = query.filter(models.Booking.status == filters["status"])

        if "payment_status" in filters:
            query = query.filter(models.Booking.payment_status == filters["payment_status"])

        if "customer_name" in filters:
            query = query.filter(models.Booking.customer_name.ilike(f"%{filters['customer_name']}%"))

    return (query
            .order_by(models.Booking.appointment_time.asc())
            .offset(offset)
            .limit(limit)
            .all())
