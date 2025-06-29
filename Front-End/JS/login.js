document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();

  // 🚧 Временно фейковая авторизация
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (username === "user" && password === "1234") {
    localStorage.setItem("loggedIn", "true");
    alert("Login successful!");
    window.location.href = "index.html";
  } else {
    alert("Invalid credentials. Try user / 1234");
  }
});
