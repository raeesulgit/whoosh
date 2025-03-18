import logging
from sqlalchemy.orm import Session
from services import booking_service

def extract_booking_id(payload: dict) -> str:
    """Extract booking_id from any relevant entity in the payload."""
    for entity in ["payment_link", "payment", "order", "refund"]:
        notes = payload.get("payload", {}).get(entity, {}).get("entity", {}).get("notes", {})
        if notes.get("booking_id"):
            return notes["booking_id"]
    logging.error("No booking_id found in notes")
    return None


async def handle_payment_success(payload: dict, db: Session):
    """Handle payment success for both payment_link.paid and payment.captured."""
    booking_id = extract_booking_id(payload)
    if not booking_id:
        return {"status": "error", "message": "Missing booking_id"}

    booking_service.mark_booking_as_paid(db, int(booking_id))
    logging.info(f"Booking {booking_id} marked as 'paid'")
    return {"status": "ok"}


async def handle_payment_failure(payload: dict):
    """Log payment failure."""
    booking_id = extract_booking_id(payload)
    reason = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("error_reason", "Unknown reason")

    if booking_id:
        logging.warning(f"Payment failed for booking {booking_id}, reason: {reason}")
    else:
        logging.warning(f"Payment failed (booking_id missing), reason: {reason}")

    return {"status": "ok"}


async def handle_payment_link_expired(payload: dict):
    """Log payment link expiry."""
    booking_id = extract_booking_id(payload)

    if booking_id:
        logging.info(f"Payment link expired for booking {booking_id}")
    else:
        logging.info(f"Payment link expired (booking_id missing)")

    return {"status": "ok"}


async def handle_order_paid(payload: dict, db: Session):
    """Handle order.paid event."""
    booking_id = extract_booking_id(payload)

    if booking_id:
        booking_service.mark_booking_as_paid(db, int(booking_id))
        logging.info(f"Order paid for booking {booking_id}")
    else:
        logging.warning(f"Order paid - booking_id missing")

    return {"status": "ok"}


async def handle_refund_processed(payload: dict):
    """Log refund processed."""
    booking_id = extract_booking_id(payload)
    refund = payload.get("payload", {}).get("refund", {}).get("entity", {})
    payment_id = refund.get("payment_id")

    if booking_id:
        logging.info(f"Refund processed for payment {payment_id}, linked to booking {booking_id}")
    else:
        logging.info(f"Refund processed for payment {payment_id} (booking_id missing)")

    return {"status": "ok"}


async def handle_refund_failed(payload: dict):
    """Log refund failure."""
    booking_id = extract_booking_id(payload)
    refund = payload.get("payload", {}).get("refund", {}).get("entity", {})
    payment_id = refund.get("payment_id")

    if booking_id:
        logging.warning(f"Refund failed for payment {payment_id}, linked to booking {booking_id}")
    else:
        logging.warning(f"Refund failed for payment {payment_id} (booking_id missing)")

    return {"status": "ok"}

