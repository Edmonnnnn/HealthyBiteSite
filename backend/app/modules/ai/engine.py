"""Pluggable AI engine abstractions."""

from typing import List, Optional, Protocol

from .schemas import ChatMessage, ChatResponse

HEALTHYBITE_SYSTEM_PROMPT = (
    "You are a gentle, practical assistant helping people improve their eating habits and daily routines. "
    "You never give medical diagnoses or override medical advice. "
    "You focus on small, realistic steps, emotional support, and balanced, non-restrictive habits. "
    "You keep answers short, concrete, and non-judgmental."
)


class AiEngine(Protocol):
    def generate(self, *, lang: str, messages: List[ChatMessage]) -> ChatResponse:
        ...


class DummyAiEngine:
    """Deterministic, local-only AI engine used for prototyping."""

    def generate(self, *, lang: str, messages: List[ChatMessage]) -> ChatResponse:
        last_user: Optional[str] = None
        for message in reversed(messages):
            if message.role == "user":
                last_user = message.content
                break

        user_text = last_user or "Tell me a bit about your eating routine this week."

        reply = (
            f"I hear that you said: '{user_text}'. Let's start with one small, calmer change this week. "
            "Choose one meal to slow down, notice hunger and fullness cues, and remove one distraction like your phone."
        )

        suggested_next_questions: List[str] = [
            "Which meal feels easiest to start with?",
            "What usually makes that meal stressful or rushed?",
            "Do you prefer very specific steps or more general guidance?",
            "Is there a time of day when overeating feels most likely?",
        ]

        return ChatResponse(reply=reply, suggestedNextQuestions=suggested_next_questions)


class OpenAiEngine:
    """Placeholder for a future OpenAI-backed engine."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        timeout: int = 30,
        temperature: float = 0.3,
        max_tokens: int = 512,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, *, lang: str, messages: List[ChatMessage]) -> ChatResponse:
        """
        Prepare an OpenAI-style payload without making external calls.
        Returns a safe fallback response.
        """
        last_user: Optional[str] = None
        for message in reversed(messages):
            if message.role == "user":
                last_user = message.content
                break
        user_text = last_user or "I'm not sure what to ask yet."

        openai_messages = [{"role": "system", "content": HEALTHYBITE_SYSTEM_PROMPT}]
        for msg in messages:
            if msg.role not in {"user", "assistant", "system"}:
                continue
            if msg.role == "system":
                # Avoid overriding our system prompt; skip/normalize client system messages.
                continue
            openai_messages.append({"role": msg.role, "content": msg.content})

        payload = {
            "model": self.model,
            "messages": openai_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        # No external API call; payload is prepared for future use only.
        _ = payload  # avoid lint warnings

        reply = (
            f"I see that you said: '{user_text}'. A real AI assistant will be connected here later. "
            "For now, let's focus on one small, realistic step you could take this week."
        )
        suggested_next_questions: List[str] = [
            "What feels like the hardest moment of the day around food or energy?",
            "Do you prefer very specific step-by-step tips or just a general direction?",
            "Are there any habits you already tried that worked even a little?",
            "Is there anything you want to avoid (diets, tracking, strict rules)?",
        ]

        return ChatResponse(reply=reply, suggestedNextQuestions=suggested_next_questions)
