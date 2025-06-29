// === GSAP + Language Switcher for About Page ===
import gsap from "https://cdn.skypack.dev/gsap@3.12.2";
import ScrollTrigger from "https://cdn.skypack.dev/gsap@3.12.2/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

const langData = {
  en: {
    title: "About Healthy Bite",
    subtitle: "Your companion on the journey to a healthier lifestyle",
    who: "Who We Are",
    whoText: "Healthy Bite is more than just a website — it's a holistic ecosystem...",
    mission: "Our Mission",
    missionText: "To make healthy living accessible, beautiful, and enjoyable for everyone...",
    why: "Why We Exist",
    whyList: [
      "Because diets shouldn't be boring.",
      "Because health is personal.",
      "Because motivation needs a spark."
    ],
    quote: "Healthy eating is not a restriction. It's a celebration of life.",
    what: "What You Can Do Here",
    whatList: [
      "Chat with AI for diet tips and motivation.",
      "Book a consultation with a doctor.",
      "Read expert-written guides.",
      "Discover and share recipes."
    ],
    team: "Meet the Team",
    teamText: "We're developers, doctors, designers and dreamers..."
  },
  ru: {
    title: "О Healthy Bite",
    subtitle: "Твой спутник на пути к здоровому образу жизни",
    who: "Кто мы",
    whoText: "Healthy Bite — это не просто сайт, а экосистема...",
    mission: "Наша миссия",
    missionText: "Сделать здоровый образ жизни доступным, красивым и приятным...",
    why: "Зачем мы нужны",
    whyList: [
      "Потому что диеты не должны быть скучными.",
      "Потому что здоровье — это индивидуально.",
      "Потому что нужна мотивация."
    ],
    quote: "Здоровое питание — это не ограничение. Это праздник жизни.",
    what: "Что ты можешь здесь делать",
    whatList: [
      "Общайся с ИИ-ассистентом.",
      "Консультируйся с врачами.",
      "Читайте статьи и рекомендации.",
      "Открывай и делись рецептами."
    ],
    team: "Наша команда",
    teamText: "Мы — разработчики, врачи, дизайнеры и мечтатели..."
  },
  hy: {
    title: "Մեր Մասին Healthy Bite",
    subtitle: "Քո ուղեկիցը՝ առողջ ապրելակերպի ճանապարհին",
    who: "Ովքե՞ր ենք մենք",
    whoText: "Healthy Bite-ը ամբողջական էկոհամակարգ է...",
    mission: "Մեր առաքելությունը",
    missionText: "Առողջ ապրելակերպը դարձնել հասանելի ու հաճելի...",
    why: "Ինչու ենք մենք այստեղ",
    whyList: [
      "Որովհետեւ սննդակարգը չպետք է լինի ձանձրալի։",
      "Որովհետեւ առողջությունը անձնական է։",
      "Որովհետեւ մոտիվացիան կարիք ունի կայծի։"
    ],
    quote: "Առողջ սնունդը սահմանափակում չէ, այլ՝ տոն։",
    what: "Ինչ կարող ես անել այստեղ",
    whatList: [
      "Զրուցիր AI-ի հետ սննդի մասին։",
      "Պատվիր խորհրդատվություն բժշկի հետ։",
      "Կարդա հոդվածներ և ուղեցույցներ։",
      "Բացահայտիր և կիսվիր բաղադրատոմսերով։"
    ],
    team: "Թիմը",
    teamText: "Մենք՝ ծրագրավորողներ, բժիշկներ, դիզայներներ ու երազողներ ենք..."
  }
};

const switchLang = (lang) => {
  const t = langData[lang];
  document.querySelector(".overlay h1").textContent = t.title;
  document.querySelector(".overlay p").textContent = t.subtitle;
  document.querySelector(".lang-who").textContent = t.who;
  document.querySelector(".lang-whoText").textContent = t.whoText;
  document.querySelector(".lang-mission").textContent = t.mission;
  document.querySelector(".lang-missionText").textContent = t.missionText;
  document.querySelector(".lang-why").textContent = t.why;
  document.querySelector(".lang-whyList").innerHTML = t.whyList.map(item => `<li>${item}</li>`).join("");
  document.querySelector(".quote").textContent = t.quote;
  document.querySelector(".lang-what").textContent = t.what;
  document.querySelector(".lang-whatList").innerHTML = t.whatList.map(item => `<li>${item}</li>`).join("");
  document.querySelector(".lang-team").textContent = t.team;
  document.querySelector(".lang-teamText").textContent = t.teamText;
};

document.querySelectorAll(".lang-btn").forEach(btn => {
  btn.addEventListener("click", () => switchLang(btn.dataset.lang));
});

// GSAP animations
window.addEventListener("load", () => {
  gsap.from(".overlay h1", { opacity: 0, y: -50, duration: 1 });
  gsap.from(".overlay p", { opacity: 0, y: 20, delay: 0.5, duration: 1 });

  gsap.utils.toArray(".about-content section, .quote, .team").forEach(el => {
    gsap.from(el, {
      scrollTrigger: {
        trigger: el,
        start: "top 80%",
      },
      opacity: 0,
      y: 40,
      duration: 1
    });
  });
});