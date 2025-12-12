"""FastAPI routes for the AI chat module."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.common.deps import get_db
from . import schemas, service

router = APIRouter()


@router.post("/chat", response_model=schemas.ChatResponse)
def chat(payload: schemas.ChatRequest, db: Session = Depends(get_db)):
    return service.handle_chat(db=db, payload=payload)
