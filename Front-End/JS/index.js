// 🍔 Бургер-меню логика
const burger = document.getElementById('burger');
const sideMenu = document.getElementById('sideMenu');

burger.addEventListener('click', () => {
  const isOpen = sideMenu.classList.toggle('active');
  burger.classList.toggle('open', isOpen);
});

// 🎬 Видео слайдшоу
const videoSources = [
  "assets/videos/3195728-uhd_3840_2160_25fps.mp4",
  "assets/videos/3245641-uhd_3840_2160_25fps.mp4",
  "assets/videos/5645055-hd_1920_1080_25fps.mp4",
  "assets/videos/5865847-uhd_3840_2160_25fps.mp4"
];

const video = document.getElementById("hero-video");
const errorBox = document.getElementById("videoError");

let index = 0;
let slideshowInterval;

function playVideo(i) {
  const source = videoSources[i];
  video.src = source;
  video.load();

  video.oncanplay = () => {
    video.play().catch(err => {
      errorBox.textContent = "⚠️ Не удалось воспроизвести видео.";
    });
  };

  video.onerror = () => {
    errorBox.textContent = "⚠️ Видео не загрузилось.";
  };
}

function startSlideshow() {
  playVideo(index);
  slideshowInterval = setInterval(() => {
    index = (index + 1) % videoSources.length;
    playVideo(index);
  }, 5000);
}

document.getElementById("startVideos")?.addEventListener("click", () => {
  document.getElementById("startVideos").remove();
  startSlideshow();
});

// 🧭 Анимации появления блоков
const faders = document.querySelectorAll('.fade-up');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
    }
  });
}, { threshold: 0.3 });
faders.forEach(el => observer.observe(el));
