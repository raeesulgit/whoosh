from fastapi import APIRouter, Depends,  UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ServiceCreate, ServiceOut
from services import service_service

router = APIRouter()

@router.post("/", response_model=ServiceOut)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    return service_service.create_service(db, service)

@router.get("/", response_model=list[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return service_service.get_all_services(db)

@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    return service_service.get_service(db, service_id)

@router.put("/{service_id}", response_model=ServiceOut)
def update_service(service_id: int, service: ServiceCreate, db: Session = Depends(get_db)):
    return service_service.update_service(db, service_id, service)

@router.delete("/{service_id}", response_model=ServiceOut)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    return service_service.delete_service(db, service_id)


@router.post("/{service_id}/upload-image")
def upload_service_image(service_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    service_service.upload_service_image(db, service_id, file)
