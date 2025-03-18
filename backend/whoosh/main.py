import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import booking_router, payment_router, service_router
from database import init_db


app = FastAPI()

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
@app.on_event("startup")
def startup_event():
    init_db()  # This ensures tables are created on startup
current_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory (where main.py lives)
uploads_dir = os.path.join(current_dir, "uploads")       # Full path to uploads folder

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Add this CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - during development
    allow_credentials=True,
    allow_methods=["*"],   # Allow all methods
    allow_headers=["*"],   # Allow all headers
)

app.include_router(booking_router.router, prefix="/bookings", tags=["Bookings"])
app.include_router(payment_router.router, prefix="/payments", tags=["Payments"])
app.include_router(service_router.router, prefix="/services", tags=["Services"])
