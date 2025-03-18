import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from services import payment_service

router = APIRouter()

@router.post("/callback")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    headers = dict(request.headers)

    print(f"Headers: {headers}")
    print(f"Raw Body: {body.decode()}")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return {"status": "error", "message": "Invalid JSON"}

    await payment_service.handle_payment_webhook(payload, db, headers)
    return {"status": "ok"}


@router.get("/generate-link/{booking_id}")
def generate_payment_link(booking_id: int, db: Session = Depends(get_db)):
    return payment_service.get_payment_link_for_booking(db, booking_id)

@router.get("/retry/{booking_id}")
def retry_payment(booking_id: int, db: Session = Depends(get_db)):
    return payment_service.retry_payment(db, booking_id)