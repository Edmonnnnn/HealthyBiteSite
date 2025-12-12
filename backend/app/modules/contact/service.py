"""Database-backed service layer for contact requests."""

import uuid

from sqlalchemy.orm import Session

from . import models, schemas


def create_support_request(db: Session, payload: schemas.ContactSupportRequest) -> schemas.ContactResponse:
    request_id = f"support_{uuid.uuid4().hex[:8]}"
    db_obj = models.ContactSupportRequest(
        request_id=request_id,
        name=payload.name,
        email=payload.email,
        topic=payload.topic,
        message=payload.message,
        lang=payload.lang or "en",
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return schemas.ContactResponse(status="ok", requestId=request_id)


def create_consult_request(db: Session, payload: schemas.ContactConsultRequest) -> schemas.ContactResponse:
    request_id = f"consult_{uuid.uuid4().hex[:8]}"
    db_obj = models.ContactConsultRequest(
        request_id=request_id,
        name=payload.name,
        email=payload.email,
        preferred_channel=payload.preferredChannel,
        preferred_time=payload.preferredTime,
        message=payload.message,
        lang=payload.lang or "en",
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return schemas.ContactResponse(status="ok", requestId=request_id)
