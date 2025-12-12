"""Pydantic schemas for the AI chat module."""

from typing import List, Optional, Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    lang: Optional[str] = "en"
    sessionId: Optional[str] = None
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
    suggestedNextQuestions: List[str]
