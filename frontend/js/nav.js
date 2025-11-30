// Навигация: бургер + плавный скролл
document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".header");
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelectorAll(".nav a[href^='#']");
  const panelLinks = document.querySelectorAll(".header-panel a");


  // Открытие/закрытие бургер-меню (мобилка)
  if (header && navToggle) {
    navToggle.addEventListener("click", () => {
      const isOpen = header.classList.toggle("header--menu-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  // Клик по ссылкам в раздвигающейся панели: прячем панель, чтобы не перекрывала контент
  if (header && panelLinks.length > 0) {
    panelLinks.forEach((link) => {
      link.addEventListener("click", () => {
        header.classList.add("header--panel-hidden");

        // заодно закрываем мобильное меню, если открыто
        if (header.classList.contains("header--menu-open")) {
          header.classList.remove("header--menu-open");
          if (navToggle) {
            navToggle.setAttribute("aria-expanded", "false");
          }
        }
      });
    });

    // Когда уводим мышь с шапки — возвращаем нормальное поведение панели
    header.addEventListener("mouseleave", () => {
      header.classList.remove("header--panel-hidden");
    });
  }


  // Плавный скролл по якорям + закрытие меню после клика
  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href") || "";
      if (href.startsWith("#")) {
        e.preventDefault();
        const id = href.substring(1);
        const target = document.getElementById(id);
        if (target) {
          target.scrollIntoView({ behavior: "smooth" });
        }
      }

      // Закрываем бургер-меню после перехода
      if (header && header.classList.contains("header--menu-open")) {
        header.classList.remove("header--menu-open");
        if (navToggle) {
          navToggle.setAttribute("aria-expanded", "false");
        }
      }
    });
  });
});
