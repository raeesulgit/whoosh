from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class BookingStatus(str, Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class VehicleType(str, Enum):
    CAR = "CAR"
    BIKE = "BIKE"

class BookingCreate(BaseModel):
    customer_name: str = Field(..., example="John Doe")
    customer_email: EmailStr = Field(..., example="raeesulasad@gmail.com")
    customer_phone: str = Field(..., example="8139098007")
    vehicle_type: VehicleType
    service: str = Field(..., example="BASIC_WASH")
    appointment_time: datetime = Field(..., example="2025-03-02T10:30:00")
    notes: Optional[str] = Field(None, example="Please wash thoroughly.")

class BookingOut(BookingCreate):
    id: int
    status: BookingStatus
    payment_status: str  # This will override the Optional[str] from BookingCreate
    completion_notes: Optional[str] = None

    class Config:
        orm_mode = True

class CompleteBookingRequest(BaseModel):
    completion_notes: Optional[str] = None
class ServiceBase(BaseModel):
    name: str = Field(..., example="BASIC_WASH")
    description: Optional[str] = Field(None, example="Basic wash for exterior cleaning")
    price: float = Field(..., example=300.0)
    vehicle_type: VehicleType = Field(..., example="BIKE")  # New Field

class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    vehicle_type: VehicleType
    image_url: Optional[str] = Field(None, example="/static/service_20250303121212.png")  # Image URL can be optional if you allow services without images


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    vehicle_type: Optional[VehicleType] = None  # Optional for partial update
    image_url: Optional[str] = Field(None, example="/static/service_20250303121212.png")

class ServiceOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    vehicle_type: VehicleType
    image_url: Optional[str]

    class Config:
        orm_mode = True

