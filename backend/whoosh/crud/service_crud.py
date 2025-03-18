from sqlalchemy.orm import Session
from models import Service
from schemas import ServiceCreate, VehicleType

def create(db: Session, service_data: ServiceCreate) -> Service:
    service = Service(**service_data.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

def get_all(db: Session):
    return db.query(Service).all()

def get_by_id(db: Session, service_id: int):
    return db.query(Service).filter(Service.id == service_id).first()

def get_by_name(db: Session, name: str):
    return db.query(Service).filter(Service.name == name).first()

def update(db: Session, service_id: int, service_data: ServiceCreate):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        return None
    for key, value in service_data.model_dump().items():
        setattr(service, key, value)
    db.commit()
    db.refresh(service)
    return service

def delete(db: Session, service_id: int):
    service = db.query(Service).filter(Service.id == service_id).first()
    if service:
        db.delete(service)
        db.commit()
    return service

def get_by_name_and_vehicle(db: Session, name: str, vehicle_type: VehicleType):
    return db.query(Service).filter(
        Service.name == name,
        Service.vehicle_type == vehicle_type
    ).first()