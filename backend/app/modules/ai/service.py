"""Service layer for AI replies using a real provider with a safe mock fallback."""

from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.config import settings
from . import models
from .schemas import ChatRequest, ChatResponse, ChatMessage

SUGGESTED_NEXT_QUESTIONS: List[str] = [
    "Which meal feels easiest to start with?",
    "What usually makes that meal stressful or rushed?",
    "Do you prefer very specific steps or more general guidance?",
    "Is there a time of day when overeating feels most likely?",
]

SYSTEM_PROMPT = (
    "You are HealthyBite AI. Provide supportive, non-medical guidance. "
    "If the user mentions urgent medical symptoms, advise them to seek professional help."
)


def _extract_last_user_message(messages: List[ChatMessage]) -> Optional[str]:
    for message in reversed(messages):
        if message.role == "user":
            return message.content
    return None


def build_mock_reply(messages: List[ChatMessage]) -> ChatResponse:
    last_user = _extract_last_user_message(messages) or "Tell me a bit about your eating routine this week."
    reply = (
        f"I hear that you said: '{last_user}'. Let's start with one small, calmer change this week. "
        "Choose one meal to slow down, notice hunger and fullness cues, and remove one distraction like your phone."
    )
    return ChatResponse(reply=reply, suggestedNextQuestions=SUGGESTED_NEXT_QUESTIONS)


def _prepare_openai_messages(messages: List[ChatMessage]) -> List[dict]:
    context = messages[-6:]  # cap context to reduce prompt size
    prepared = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in context:
        if msg.role not in {"user", "assistant"}:
            continue
        prepared.append({"role": msg.role, "content": msg.content})
    return prepared


def call_openai(messages: List[ChatMessage]) -> ChatResponse:
    try:
        from openai import OpenAI  # type: ignore
    except Exception as exc:  # pragma: no cover - defensive import for missing dependency
        raise RuntimeError("openai_package_missing") from exc

    client_kwargs = {
        "api_key": settings.OPENAI_API_KEY,
        "timeout": settings.OPENAI_TIMEOUT_S,
    }
    if settings.OPENAI_BASE_URL:
        client_kwargs["base_url"] = settings.OPENAI_BASE_URL

    client = OpenAI(**client_kwargs)
    completion = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=_prepare_openai_messages(messages),
        temperature=settings.OPENAI_TEMPERATURE,
        max_tokens=settings.OPENAI_MAX_TOKENS,
    )

    choice = completion.choices[0] if completion.choices else None
    reply = (choice.message.content if choice and choice.message else "") or ""
    reply = reply.strip()
    if not reply:
        raise RuntimeError("openai_empty_reply")

    return ChatResponse(reply=reply, suggestedNextQuestions=SUGGESTED_NEXT_QUESTIONS)


def generate_reply(payload: ChatRequest) -> Tuple[ChatResponse, str, Optional[str]]:
    """Generate a reply using OpenAI when configured, otherwise fallback to mock."""
    desired_provider = (settings.AI_PROVIDER or "mock").lower()
    use_openai = desired_provider == "openai" and bool(settings.OPENAI_API_KEY)
    response: Optional[ChatResponse] = None
    provider_used = "mock"
    fallback_reason: Optional[str] = None

    if use_openai:
        try:
            response = call_openai(payload.messages)
            provider_used = "openai"
        except Exception as exc:
            fallback_reason = f"openai_failed: {exc}"
            print("[HB ai] OpenAI call failed, falling back to mock:", exc)

    if response is None:
        if not fallback_reason and desired_provider == "openai" and not settings.OPENAI_API_KEY:
            fallback_reason = "openai_api_key_missing"
        elif not fallback_reason and desired_provider != "openai":
            fallback_reason = "provider_mock_config"
        response = build_mock_reply(payload.messages)
        provider_used = "mock"

    return response, provider_used, fallback_reason


def handle_chat(db: Session, payload: ChatRequest) -> ChatResponse:
    """Route chat requests through the configured AI provider, then log to DB."""
    response, provider_used, fallback_reason = generate_reply(payload)

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
    print("[HB ai] provider_used:", provider_used, "| fallback_reason:", fallback_reason or "none")

    return response
