console.log("✅ Healthy Bite frontend loaded");

document.addEventListener("DOMContentLoaded", () => {
  const videoEl = document.getElementById("heroPlayer");
  const overlay = document.querySelector(".video-overlay");
  const errorBox = document.getElementById("videoError");

  const videoSources = [
    "assets/videos/3195728-uhd_3840_2160_25fps.mp4",
    "assets/videos/3245641-uhd_3840_2160_25fps.mp4",
    "assets/videos/5645055-hd_1920_1080_25fps.mp4",
    "assets/videos/5865847-uhd_3840_2160_25fps.mp4",
    "assets/videos/4253150-uhd_4096_2160_25fps.mp4",
    "assets/videos/6617422-uhd_3840_2160_30fps.mp4",
    "assets/videos/3298718-uhd_4096_2160_25fps.mp4",
    "assets/videos/5645037-hd_1920_1080_25fps.mp4"
  ];

  const SHOW_MS = 7000;      // сколько держим один ролик
  const OVERLAY_MS = 350;    // скорость появления белого экрана

  let index = 0;

  function vLog(msg) {
    console.log(`[🎥 VIDEO]: ${msg}`);
  }

  function showError(msg) {
    if (errorBox) errorBox.textContent = msg || "";
  }

  function playSource(src, useOverlay) {
    if (!videoEl) return;

    vLog(`🔁 Switching to: ${src}`);

    const doLoad = () => {
      videoEl.oncanplay = null;
      videoEl.onerror = null;

      videoEl.src = src;
      videoEl.load();

      videoEl.oncanplay = () => {
        videoEl
          .play()
          .then(() => {
            vLog("✅ Video started playing.");
            showError("");

            // когда новое видео пошло — убираем белый слой
            if (useOverlay && overlay) {
              // чуть подождём, чтобы кадр точно появился
              setTimeout(() => {
                overlay.classList.remove("is-active");
              }, 50);
            }
          })
          .catch((err) => {
            vLog(`❌ Error playing video: ${err.message}`);
            showError("⚠️ Не удалось воспроизвести видео.");
          });
      };

      videoEl.onerror = () => {
        vLog(`❌ Error loading video: ${src}`);
        showError("⚠️ Видео не загрузилось.");
      };
    };

    if (useOverlay && overlay) {
      // 1) плавно накрываем всё белым/светлым слоем
      overlay.classList.add("is-active");
      // 2) когда слой полностью виден — меняем src "за кадром"
      setTimeout(doLoad, OVERLAY_MS);
    } else {
      // первый старт — без белого экрана
      doLoad();
    }
  }

  function startSlideshow() {
    if (!videoEl) {
      vLog("❌ #heroPlayer not found in DOM.");
      return;
    }

    vLog("▶️ Starting slideshow with white overlay transitions...");

    // первый ролик — без белого экрана
    playSource(videoSources[index], false);

    setInterval(() => {
      index = (index + 1) % videoSources.length;
      playSource(videoSources[index], true);
    }, SHOW_MS);
  }

  startSlideshow();

  // --- Анимация появления секций .fade-up ---
  const faders = document.querySelectorAll(".fade-up");
  if (faders.length > 0) {
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("show");
          }
        });
      },
      { threshold: 0.3 }
    );

    faders.forEach((el) => obs.observe(el));
  }
});
