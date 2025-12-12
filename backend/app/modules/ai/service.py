"""Service layer for AI replies using pluggable engines."""

from typing import List, Optional

from sqlalchemy.orm import Session

from . import models
from .engine import AiEngine, DummyAiEngine
from .schemas import ChatRequest, ChatResponse, ChatMessage

engine: AiEngine = DummyAiEngine()


def _extract_last_user_message(messages: List[ChatMessage]) -> Optional[str]:
    for message in reversed(messages):
        if message.role == "user":
            return message.content
    return None


def handle_chat(db: Session, payload: ChatRequest) -> ChatResponse:
    """Route chat requests through the current AI engine, then log to DB."""
    response = engine.generate(lang=payload.lang or "en", messages=payload.messages)

    user_text = _extract_last_user_message(payload.messages) or ""

    db_log = models.AiChatLog(
        session_id=payload.sessionId or "unknown",
        lang=payload.lang or "en",
        user_message=user_text,
        reply=response.reply,
        suggested_next_questions=response.suggestedNextQuestions,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    print("[HB db] Stored AI chat log id:", db_log.id)

    return response
