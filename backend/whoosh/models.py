from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Float, Boolean, Text
from database import Base
from enum import Enum


class BookingStatus(str, Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class PaymentStatus(str, Enum):
    PAID = "PAID"
    PENDING = "PENDING"
    REFUNDED = "REFUNDED"

class VehicleType(str, Enum):
    CAR = "CAR"
    BIKE = "BIKE"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_email = Column(String)
    customer_phone = Column(String)
    vehicle_type = Column(SQLEnum(VehicleType))
    service = Column(String)
    amount = Column(Float)
    appointment_time = Column(DateTime)
    payment_status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_reference_id = Column(String, nullable=True)
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.BOOKED)
    payment_link_url = Column(String)
    notes = Column(String)
    completion_notes = Column(String, nullable=True)

class Service(Base):
    __tablename__ = "services"
    __table_args__ = {'extend_existing': True}  # Add this if needed to fix your current issue

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    vehicle_type = Column(SQLEnum(VehicleType))
    image_url = Column(String, nullable=True)  # New field for service image


