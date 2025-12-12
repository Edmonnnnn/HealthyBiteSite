"""SQLAlchemy models for storing contact requests."""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.db import Base


class ContactSupportRequest(Base):
    __tablename__ = "contact_support_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    topic = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    lang = Column(String, default="en", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ContactConsultRequest(Base):
    __tablename__ = "contact_consult_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    preferred_channel = Column(String, nullable=True)
    preferred_time = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    lang = Column(String, default="en", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
