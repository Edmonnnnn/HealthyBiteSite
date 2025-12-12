const HB_AI_API_BASE = "http://127.0.0.1:8810";

function hbCreateSessionId() {
  return "sess_" + Math.random().toString(36).slice(2) + "_" + Date.now();
}

const HB_AI_SESSION_ID = hbCreateSessionId();
const hbAiMessages = [];

function hbGetCurrentLangSafe() {
  if (window.hbGetCurrentLang) {
    return window.hbGetCurrentLang();
  }
  return localStorage.getItem("hb_lang") || "en";
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("[HB ai] init ai chat page");

  const chatContainer = document.querySelector("#ai-chat-thread");
  const input = document.querySelector("#ai-chat-input");
  const sendButton = document.querySelector("#ai-chat-send");
  const suggestionsContainer = document.querySelector("#ai-chat-suggestions");
  const statusLine = document.querySelector("#ai-chat-status");

  if (!chatContainer || !input || !sendButton) {
    console.warn("[HB ai] required chat elements missing");
    return;
  }

  chatContainer.innerHTML = "";

  function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function renderUserMessage(text) {
    const wrapper = document.createElement("div");
    wrapper.className = "ai-msg ai-msg-user";
    const bubble = document.createElement("div");
    bubble.className = "ai-bubble";
    bubble.textContent = text;
    wrapper.appendChild(bubble);
    chatContainer.appendChild(wrapper);
    scrollToBottom();
  }

  function renderAssistantMessage(text) {
    const wrapper = document.createElement("div");
    wrapper.className = "ai-msg ai-msg-ai";
    const avatar = document.createElement("div");
    avatar.className = "ai-avatar";
    avatar.textContent = "AI";
    const bubble = document.createElement("div");
    bubble.className = "ai-bubble";
    bubble.textContent = text;
    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatContainer.appendChild(wrapper);
    scrollToBottom();
  }

  function clearSuggestions() {
    if (!suggestionsContainer) return;
    suggestionsContainer.innerHTML = "";
  }

  function setStatus(text) {
    if (!statusLine) return;
    statusLine.hidden = !text;
    statusLine.textContent = text || "";
  }

  function renderSuggestions(list) {
    if (!suggestionsContainer) return;
    clearSuggestions();
    if (!Array.isArray(list) || list.length === 0) return;
    list.forEach((item) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "ai-chip";
      btn.textContent = item;
      btn.addEventListener("click", () => {
        input.value = item;
        sendMessage(item, true);
      });
      suggestionsContainer.appendChild(btn);
    });
  }

  function ensureSystemMessage() {
    if (!hbAiMessages.some((m) => m.role === "system")) {
      hbAiMessages.unshift({
        role: "system",
        content: "You are a gentle nutrition assistant for HealthyBite.",
      });
    }
  }

  async function sendMessage(text, fromSuggestion = false) {
    const trimmed = (text || "").trim();
    if (!trimmed) return;

    const lang = hbGetCurrentLangSafe();

    const userMessage = { role: "user", content: trimmed };
    hbAiMessages.push(userMessage);
    renderUserMessage(trimmed);
    if (!fromSuggestion) {
      input.value = "";
    }

    ensureSystemMessage();

    const payload = {
      lang,
      sessionId: HB_AI_SESSION_ID,
      messages: hbAiMessages,
    };

    console.log("[HB ai] sending payload", payload);
    setStatus("Thinking...");
    sendButton.disabled = true;
    clearSuggestions();

    try {
      const response = await fetch(`${HB_AI_API_BASE}/api/v1/ai/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      console.log("[HB ai] response status", response.status);

      if (!response.ok) {
        throw new Error("HTTP " + response.status);
      }

      const data = await response.json();
      console.log("[HB ai] response data", data);

      const replyText = data.reply || "";
      const suggestions = Array.isArray(data.suggestedNextQuestions)
        ? data.suggestedNextQuestions
        : [];

      if (replyText) {
        hbAiMessages.push({ role: "assistant", content: replyText });
        renderAssistantMessage(replyText);
      }

      clearSuggestions();
      if (suggestions.length > 0) {
        renderSuggestions(suggestions);
      }

      setStatus("");
    } catch (err) {
      console.error("[HB ai] error while sending message", err);
      setStatus("Error. Please try again.");
    } finally {
      sendButton.disabled = false;
    }
  }

  sendButton.addEventListener("click", () => {
    sendMessage(input.value);
  });

  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage(input.value);
    }
  });
});
