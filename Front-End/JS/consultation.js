document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("message-input");
  const button = document.getElementById("send-button");
  const chatBox = document.getElementById("chat-box");
  const burger = document.getElementById("burger");
  const sideMenu = document.getElementById("sideMenu");

const chatContainer = document.getElementById("chat-container");
const toggleBtn = document.getElementById("toggle-chat");
const closeBtn = document.getElementById("close-chat");
const bgWrapper = document.getElementById("backgroundWrapper");

  // ✉️ Отправка сообщения
  function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user-message");
    input.value = "";
    scrollToBottom();

    setTimeout(() => {
      botReply(text);
    }, 600); // задержка бота
  }

  // 👤 Сообщение от пользователя
  function addMessage(text, className = "") {
    const message = document.createElement("div");
    message.className = `chat-message ${className}`;
    message.textContent = text;
    chatBox.appendChild(message);
    scrollToBottom();
  }

  // 🤖 Ответ бота
  function botReply(userText) {
    const responses = [
      "Спасибо за ваше сообщение!",
      "Наш специалист скоро с вами свяжется.",
      "Пожалуйста, уточните ваш вопрос.",
      "Мы работаем над этим. 🙌",
      "Понял вас. Спасибо за информацию!"
    ];
    const reply = responses[Math.floor(Math.random() * responses.length)];
    addMessage(reply);
  }

  // 🔻 Прокрутка вниз
  function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // 👆 Enter / Кнопка
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
  button.addEventListener("click", sendMessage);

  // 🍔 Меню
  burger.addEventListener("click", () => {
    burger.classList.toggle("open");
    sideMenu.classList.toggle("active");
  });

// Открытие чата
toggleBtn.addEventListener("click", () => {
  chatContainer.style.display = "flex";
  setTimeout(() => {
    chatContainer.classList.add("show");
  }, 10);
  toggleBtn.style.display = "none";
  bgWrapper.classList.add("blur");
});

closeBtn.addEventListener("click", () => {
  chatContainer.classList.remove("show");
  setTimeout(() => {
    chatContainer.style.display = "none";
    toggleBtn.style.display = "block";
  }, 400);
  bgWrapper.classList.remove("blur");
})})