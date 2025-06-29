const doctors = [
  { name: "Dr. Anna Green", spec: "dietologist", about: "Certified dietologist", img: "assets/image/doctor1.jpg" },
  { name: "Dr. John Smith", spec: "nutritionist", about: "Sports nutrition expert", img: "assets/image/doctor2.jpg" },
  { name: "Dr. Emily Chen", spec: "endocrinologist", about: "Hormonal balance specialist", img: "assets/image/doctor3.jpg" },
];

const grid = document.getElementById("doctorGrid");
const select = document.getElementById("specialtySelect");

function renderDoctors(filter = "all") {
  grid.innerHTML = "";
  doctors
    .filter(doc => filter === "all" || doc.spec === filter)
    .forEach(doc => {
      const card = document.createElement("div");
      card.className = "doctor-card";
      card.innerHTML = `
        <img src="${doc.img}" alt="${doc.name}" />
        <h3>${doc.name}</h3>
        <p>${doc.about}</p>
        <button>Send Request</button>
      `;
      grid.appendChild(card);
    });
}

select.addEventListener("change", (e) => {
  renderDoctors(e.target.value);
});

renderDoctors();

// 🍔 Бургер-меню
const burger = document.getElementById('burger');
const sideMenu = document.getElementById('sideMenu');

if (burger && sideMenu) {
  burger.addEventListener('click', () => {
    const isOpen = sideMenu.classList.toggle('active');
    burger.classList.toggle('open', isOpen);
  });

  // Автоматическое закрытие при клике по ссылке
  document.querySelectorAll('.side-menu a').forEach(link => {
    link.addEventListener('click', () => {
      sideMenu.classList.remove('active');
      burger.classList.remove('open');
    });
  });
}
