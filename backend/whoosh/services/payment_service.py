import razorpay
import json
import config
from sqlalchemy.orm import Session
from services import booking_service  # Call booking_service, not booking_crud directly
import models
import logging
from helpers.booking import fetch_and_validate_booking
from helpers.payment import (
    handle_payment_success,
    handle_payment_failure,
    handle_payment_link_expired,
    handle_order_paid,
    handle_refund_processed,
    handle_refund_failed
)

rz_client = razorpay.Client(auth=(config.RAZORPAY_API_KEY, config.RAZORPAY_API_SECRET))

def get_payment_link_for_booking(db: Session, booking_id: int) -> str:
    booking = fetch_and_validate_booking(db, booking_id, required_payment_status=models.PaymentStatus.PENDING)
    response = generate_payment_link(booking)
    booking.payment_reference_id = response["id"]
    booking.payment_link_url = response["short_url"]
    db.commit()
    db.refresh(booking)
    return booking.payment_link_url

def generate_payment_link(booking) -> str:
    response = rz_client.payment_link.create({
        "amount": int(booking.amount * 100),  # Convert to paise
        "currency": "INR",
        "description": f"Payment for Booking ID {booking.id}",
        "customer": {
            "name": booking.customer_name,
            "email": booking.customer_email,
            "contact": booking.customer_phone,
        },
        "notify": {"sms": False, "email": False},
        "callback_url": "https://6cb0-2406-7400-56-d5ef-cdc4-50e2-5fa8-c3fc.ngrok-free.app/payments/callback",  # Update with actual callback
        "callback_method": "get",
        "notes": {
            "booking_id": str(booking.id)
        }
    })
    return response

async def handle_payment_webhook(payload: dict, db: Session, headers: dict):
    event = payload.get("event")

    # 1. Verify Signature
    webhook_signature = headers.get("x-razorpay-signature")
    if not webhook_signature:
        logging.warning("Missing webhook signature")
        return {"status": "error", "message": "Missing signature"}

    try:
        body = json.dumps(payload, separators=(',', ':'))
        razorpay.Utility(client=rz_client).verify_webhook_signature(
            body,
            webhook_signature,
            config.RAZORPAY_WEBHOOK_SECRET
        )
    except razorpay.errors.SignatureVerificationError:
        logging.warning("Invalid webhook signature")
        return {"status": "error", "message": "Invalid signature"}

    # 2. Route event to appropriate handler
    if event in ["payment_link.paid", "payment.captured"]:
        return await handle_payment_success(payload, db)

    elif event == "payment.failed":
        return await handle_payment_failure(payload)

    elif event == "payment_link.expired":
        return await handle_payment_link_expired(payload)

    elif event == "order.paid":
        return await handle_order_paid(payload, db)

    elif event == "refund.processed":
        return await handle_refund_processed(payload)

    elif event == "refund.failed":
        return await handle_refund_failed(payload)

    # 3. Log and ignore unhandled events
    logging.info(f"Unhandled Razorpay event type: {event}")
    return {"status": "ok"}


def process_refund(payment_reference_id: str, amount: float):
    """
    Process a refund for a given payment reference ID.

    Args:
        payment_reference_id (str): The reference ID of the payment to refund.
        amount (float): The amount to be refunded.

    Returns:
        dict: Refund status and message.
    """
    # Simulate refund processing (you would replace this with actual API call to payment gateway)
    if not payment_reference_id:
        return {"status": "failed", "message": "Invalid payment reference ID"}

    # In real scenario, you'd call your payment provider's refund API here.
    # Example (pseudo-code):
    # response = payment_gateway.refund(payment_reference_id, amount)
    # return response.json()

    # Mock successful response
    return {"status": "success", "message": f"Refund of ₹{amount} processed successfully for {payment_reference_id}"}

def retry_payment(db: Session, booking_id: int) -> dict:
    booking = booking_service.get_booking(db, booking_id)

    if not booking:
        return {"status": "error", "message": "Booking not found"}

    if booking.payment_status != models.PaymentStatus.PENDING:
        return {"status": "error", "message": f"Cannot retry payment for booking as payment is in '{booking.status}' state"}

    if not booking.payment_link_url:
        return {"status": "error", "message": "No payment link found for this booking"}

    logging.info(f"Retrying payment for booking {booking_id} using link: {booking.payment_link_url}")

    return {"status": "ok", "payment_link": booking.payment_link_url}
