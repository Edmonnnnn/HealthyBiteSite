"""SQLAlchemy models for AI chat logs."""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.sql import func

from app.db import Base


class AiChatLog(Base):
    __tablename__ = "ai_chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    lang = Column(String, default="en", nullable=False)
    user_message = Column(Text, nullable=False)
    reply = Column(Text, nullable=True)
    suggested_next_questions = Column(SQLiteJSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
