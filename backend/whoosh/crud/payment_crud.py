from sqlalchemy.orm import Session
import models

def mark_payment_as_paid(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise ValueError(f"Booking {booking_id} not found.")

    booking.payment_status = models.PaymentStatus.PAID
    db.commit()
    db.refresh(booking)

