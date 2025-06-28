// 🍔 Бургер-меню
const burger = document.getElementById('burger');
const sideMenu = document.getElementById('sideMenu');
burger.addEventListener('click', () => {
  const isOpen = sideMenu.classList.toggle('active');
  burger.classList.toggle('open', isOpen);
});

// 🎬 Видео логика
const videoSources = [
  "assets/videos/1.mp4", "assets/videos/2.mp4", "assets/videos/3.mp4", "assets/videos/4.mp4",
  "assets/videos/5.mp4", "assets/videos/6.mp4", "assets/videos/7.mp4", "assets/videos/8.mp4"
];

const startBtn = document.getElementById("startVideos");
const videoBox = document.querySelector(".video-box");
const mainVideo = document.getElementById("hero-video");
const errorBox = document.getElementById("videoError");

let videoIndex = 0;

// 🌌 Сетка миниатюр
function showThumbnails() {
  const grid = document.createElement("div");
  grid.className = "thumbnail-grid";
  videoBox.innerHTML = "";
  videoBox.appendChild(grid);

  let thumbIndex = 0;
  const showThumb = () => {
    const thumb = document.createElement("video");
    thumb.className = "thumb fade-thumb";
    thumb.src = videoSources[thumbIndex];
    thumb.muted = true;
    thumb.playsInline = true;
    thumb.autoplay = true;
    grid.appendChild(thumb);
    thumbIndex++;
    if (thumbIndex < videoSources.length) {
      setTimeout(showThumb, 1000);
    } else {
      // После 8 секунд паузы удаляем сетку
      setTimeout(() => {
        grid.remove();
        videoIndex = 0;
        startVideoSequence();
      }, 8000);
    }
  };
  showThumb();
}

// 🔁 Воспроизведение видео по очереди
function startVideoSequence() {
  videoBox.innerHTML = "";
  videoBox.appendChild(mainVideo);
  mainVideo.classList.add("fade");
  mainVideo.style.opacity = 0;

  const playNext = () => {
    mainVideo.style.opacity = 0;
    setTimeout(() => {
      mainVideo.src = videoSources[videoIndex];
      mainVideo.load();
      mainVideo.oncanplay = () => {
        mainVideo.play();
        mainVideo.style.opacity = 1;
      };
      videoIndex++;
      if (videoIndex < videoSources.length) {
        setTimeout(playNext, 5000);
      } else {
        setTimeout(showThumbnails, 5000);
      }
    }, 1000); // fade delay
  };
  playNext();
}

// 🚀 Запуск при клике
startBtn?.addEventListener("click", () => {
  startBtn.remove();
  videoBox.style.display = "block";
  videoBox.classList.add("centered-box");
  startVideoSequence();
});

// 🧭 Анимации появления
const faders = document.querySelectorAll('.fade-up');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('show');
  });
}, { threshold: 0.3 });
faders.forEach(el => observer.observe(el));
