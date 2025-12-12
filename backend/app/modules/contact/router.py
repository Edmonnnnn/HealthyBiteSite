"""FastAPI routes for contact submissions."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.common.deps import get_db
from . import schemas, service

router = APIRouter()


@router.post("/support", response_model=schemas.ContactResponse)
def create_support(payload: schemas.ContactSupportRequest, db: Session = Depends(get_db)):
    return service.create_support_request(db=db, payload=payload)


@router.post("/consult", response_model=schemas.ContactResponse)
def create_consult(payload: schemas.ContactConsultRequest, db: Session = Depends(get_db)):
    return service.create_consult_request(db=db, payload=payload)
