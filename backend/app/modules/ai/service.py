"""Service layer for AI replies using a real provider with a safe mock fallback."""

from __future__ import annotations

import logging
import re
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.config import settings
from . import models
from .schemas import ChatRequest, ChatResponse, ChatMessage

logger = logging.getLogger(__name__)


SUGGESTED_NEXT_QUESTIONS_BY_LANG: dict[str, list[str]] = {
    "en": [
        "Which meal feels easiest to start with?",
        "What usually makes that meal stressful or rushed?",
        "Do you prefer very specific steps or more general guidance?",
        "Is there a time of day when overeating feels most likely?",
    ],
    "ru": [
        "С какого приёма пищи проще всего начать?",
        "Что обычно делает этот приём пищи стрессовым или «на бегу»?",
        "Тебе нужны очень конкретные шаги или общий вектор?",
        "В какое время дня чаще всего тянет переесть?",
    ],
}

SYSTEM_PROMPT_BASE = (
    "You are HealthyBite AI: a gentle, practical assistant helping people improve eating habits and daily routines. "
    "Scope: nutrition, eating habits, meal structure, mindful eating, cravings, energy, sleep/routine as it relates to habits. "
    "If the user asks about unrelated topics (cars, tech support, finance, coding, politics, etc.), politely decline and redirect to HealthyBite topics. "
    "Do NOT provide medical diagnoses, do NOT override medical advice, and do NOT prescribe medications. "
    "If the user reports urgent or severe symptoms, advise seeking professional medical help. "
    "Focus on small, realistic steps, emotional support, and balanced, non-restrictive habits. "
    "Avoid shame, moralizing, and extreme dieting advice."
)

# Lightweight off-topic filter. This makes behavior deterministic even if the model "tries" to answer.
# We keep it intentionally conservative to avoid false positives.
OFFTOPIC_KEYWORDS = {
    "en": [
        "car", "engine", "bmw", "mercedes", "toyota", "honda", "tesla", "oil", "gearbox", "transmission", "tires",
        "laptop", "windows", "linux", "python", "javascript", "server", "database", "credit", "loan", "crypto",
        "stock", "trading", "mortgage", "tax", "politics",
    ],
    "ru": [
        "машин", "авто", "двигател", "коробк", "акпп", "мкпп", "шины", "резин", "масло", "аккумулятор",
        "ноутбук", "виндовс", "линукс", "питон", "javascript", "сервер", "база данных", "кредит", "займ",
        "крипто", "акции", "трейдинг", "ипотек", "налог", "политик",
    ],
}

ONTOPIC_HINTS = {
    "en": ["food", "eat", "meal", "diet", "nutrition", "hunger", "craving", "snack", "protein", "calories", "weight"],
    "ru": ["еда", "питани", "приём пищ", "диет", "рацион", "голод", "тяга", "перекус", "белок", "калори", "вес"],
}


def _norm_lang(lang: Optional[str]) -> str:
    raw = (lang or "en").strip().lower()
    if raw.startswith("ru"):
        return "ru"
    return "en"


def _lang_instruction(lang: str) -> str:
    return "Отвечай по-русски." if lang == "ru" else "Respond in English."


def _suggestions_for(lang: str) -> list[str]:
    return SUGGESTED_NEXT_QUESTIONS_BY_LANG.get(lang, SUGGESTED_NEXT_QUESTIONS_BY_LANG["en"])


def _extract_last_user_message(messages: List[ChatMessage]) -> Optional[str]:
    for message in reversed(messages):
        if message.role == "user":
            return message.content
    return None


def _is_offtopic(user_text: str, lang: str) -> bool:
    """Conservative rule: off-topic keywords present AND no strong nutrition hints."""
    if not user_text:
        return False

    t = user_text.strip().lower()

    # quick accept if clearly on-topic
    if any(h in t for h in ONTOPIC_HINTS.get(lang, [])):
        return False

    # keyword hit
    hits = 0
    for kw in OFFTOPIC_KEYWORDS.get(lang, []):
        if kw in t:
            hits += 1
            if hits >= 1:
                return True

    # fallback: if user asks "which car" style questions
    if lang == "ru":
        if re.search(r"\bкакую\b.*\bмашин", t) or re.search(r"\bкакой\b.*\bавто", t):
            return True
    else:
        if re.search(r"\bwhich\b.*\bcar\b", t) or re.search(r"\bwhat\b.*\bcar\b", t):
            return True

    return False


def _offtopic_reply(lang: str) -> ChatResponse:
    if lang == "ru":
        reply = (
            "Я могу помочь только по теме питания и привычек (HealthyBite). "
            "По вопросам вроде выбора машины или техники я не самый подходящий помощник. "
            "Если хочешь — расскажи, какая у тебя цель по питанию (вес, энергия, режим, тяга к сладкому), "
            "и я предложу конкретные, спокойные шаги."
        )
    else:
        reply = (
            "I’m built specifically for HealthyBite topics: nutrition and habit-building. "
            "I can’t help with unrelated requests (like choosing a car or tech advice). "
            "If you tell me your goal around food (weight, energy, routine, cravings), I’ll suggest a few calm, practical next steps."
        )
    return ChatResponse(reply=reply, suggestedNextQuestions=_suggestions_for(lang))


def build_mock_reply(messages: List[ChatMessage], lang: str) -> ChatResponse:
    last_user = _extract_last_user_message(messages) or (
        "Расскажи немного, как у тебя обычно проходит питание на неделе." if lang == "ru"
        else "Tell me a bit about your eating routine this week."
    )

    if _is_offtopic(last_user, lang=lang):
        return _offtopic_reply(lang)

    if lang == "ru":
        reply = (
            "Понял. Давай начнём с одного маленького, спокойного шага на этой неделе: "
            "выбери один приём пищи и попробуй есть чуть медленнее, замечая голод/насыщение, "
            "и убери один отвлекающий фактор — например, телефон. "
            "Если скажешь, в какое время дня сложнее всего, я подстрою шаги точнее."
        )
    else:
        reply = (
            "Got it. Let’s start with one small, calmer change this week: "
            "pick one meal to slow down, notice hunger/fullness cues, and remove one distraction (like your phone). "
            "If you tell me when your day feels hardest, I’ll tailor the next steps."
        )

    return ChatResponse(reply=reply, suggestedNextQuestions=_suggestions_for(lang))


def _prepare_openai_messages(messages: List[ChatMessage], lang: str) -> List[dict]:
    context = messages[-10:]  # modest cap to reduce token usage
    system_text = f"{SYSTEM_PROMPT_BASE} {_lang_instruction(lang)}"
    prepared: List[dict] = [{"role": "system", "content": system_text}]

    # Only forward user/assistant messages; ignore client-side system messages
    for msg in context:
        if msg.role not in {"user", "assistant"}:
            continue
        prepared.append({"role": msg.role, "content": msg.content})

    return prepared


def call_openai(messages: List[ChatMessage], lang: str) -> ChatResponse:
    try:
        from openai import OpenAI  # type: ignore
    except Exception as exc:
        raise RuntimeError("openai_package_missing") from exc

    if not settings.OPENAI_API_KEY:
        raise RuntimeError("openai_api_key_missing")

    last_user = _extract_last_user_message(messages) or ""
    if _is_offtopic(last_user, lang=lang):
        # Deterministic off-topic behavior; do not call external API.
        return _offtopic_reply(lang)

    client_kwargs = {
        "api_key": settings.OPENAI_API_KEY,
        "timeout": float(settings.OPENAI_TIMEOUT_S),
    }
    if settings.OPENAI_BASE_URL:
        client_kwargs["base_url"] = settings.OPENAI_BASE_URL

    client = OpenAI(**client_kwargs)

    completion = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=_prepare_openai_messages(messages, lang=lang),
        temperature=settings.OPENAI_TEMPERATURE,
        max_tokens=settings.OPENAI_MAX_TOKENS,
    )

    choice = completion.choices[0] if completion.choices else None
    reply = (choice.message.content if choice and choice.message else "") or ""
    reply = reply.strip()
    if not reply:
        raise RuntimeError("openai_empty_reply")

    return ChatResponse(reply=reply, suggestedNextQuestions=_suggestions_for(lang))


def generate_reply(payload: ChatRequest) -> Tuple[ChatResponse, str, Optional[str]]:
    """Generate a reply using OpenAI when configured, otherwise fallback to mock."""
    lang = _norm_lang(payload.lang)
    desired_provider = (settings.AI_PROVIDER or "mock").strip().lower()

    # Only support: "openai" or "mock"
    if desired_provider not in {"openai", "mock"}:
        logger.warning("[HB ai] Unknown AI_PROVIDER=%r, falling back to mock", desired_provider)
        desired_provider = "mock"

    use_openai = desired_provider == "openai" and bool(settings.OPENAI_API_KEY)

    response: Optional[ChatResponse] = None
    provider_used = "mock"
    fallback_reason: Optional[str] = None

    if use_openai:
        try:
            response = call_openai(payload.messages, lang=lang)
            provider_used = "openai"
        except Exception as exc:
            fallback_reason = f"openai_failed: {exc}"
            logger.exception("[HB ai] OpenAI call failed, falling back to mock")

    if response is None:
        if not fallback_reason and desired_provider == "openai" and not settings.OPENAI_API_KEY:
            fallback_reason = "openai_api_key_missing"
        elif not fallback_reason and desired_provider != "openai":
            fallback_reason = "provider_mock_config"

        response = build_mock_reply(payload.messages, lang=lang)
        provider_used = "mock"

    return response, provider_used, fallback_reason


def handle_chat(db: Session, payload: ChatRequest) -> ChatResponse:
    """Route chat requests through the configured AI provider, then log to DB."""
    response, provider_used, fallback_reason = generate_reply(payload)

    user_text = _extract_last_user_message(payload.messages) or ""

    db_log = models.AiChatLog(
        session_id=payload.sessionId or "unknown",
        lang=_norm_lang(payload.lang),
        user_message=user_text,
        reply=response.reply,
        suggested_next_questions=response.suggestedNextQuestions,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    logger.info("[HB db] Stored AI chat log id=%s", db_log.id)
    logger.info("[HB ai] provider_used=%s fallback_reason=%s", provider_used, fallback_reason or "none")

    return response
