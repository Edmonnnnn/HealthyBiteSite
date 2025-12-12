"""Data schemas for the Contact module."""

from typing import Optional

from pydantic import BaseModel


class ContactSupportRequest(BaseModel):
    name: str
    email: str
    topic: Optional[str] = None
    message: str
    lang: Optional[str] = "en"


class ContactConsultRequest(BaseModel):
    name: str
    email: str
    preferredChannel: Optional[str] = None
    preferredTime: Optional[str] = None
    message: str
    lang: Optional[str] = "en"


class ContactResponse(BaseModel):
    status: str
    requestId: str
