import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas import ServiceCreate, VehicleType
from crud import service_crud
UPLOAD_FOLDER = "uploads"
import os
# Make sure the uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def create_service(db: Session, service_data: ServiceCreate):
    if service_data.price <= 0:
        service_data.is_active = False

    return service_crud.create(db, service_data)

def get_all_services(db: Session):
    return service_crud.get_all(db)

def get_service(db: Session, service_id: int):
    service = service_crud.get_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

def update_service(db: Session, service_id: int, service_data: ServiceCreate):
    if not service_crud.get_by_id(db, service_id):
        raise HTTPException(status_code=404, detail="Service not found")

    return service_crud.update(db, service_id, service_data)

def delete_service(db: Session, service_id: int):
    service = service_crud.get_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service_crud.delete(db, service_id)

def upload_service_image(db: Session, service_id: int, file):
    service = service_crud.get_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    ext = file.filename.split('.')[-1]
    file_name = f"service_{service_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Update the image_url field in the service
    service.image_url = f"/{file_path}"
    db.commit()
    db.refresh(service)

    return {"message": "Image uploaded successfully", "image_url": service.image_url}
def get_service_by_name_and_vehicle(db: Session, service_name: str, vehicle_type: VehicleType):
    return service_crud.get_by_name_and_vehicle(db, service_name, vehicle_type)
