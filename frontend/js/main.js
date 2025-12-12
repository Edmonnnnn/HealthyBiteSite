console.log("✅ Healthy Bite frontend loaded");

document.addEventListener("DOMContentLoaded", () => {
  const videoEl = document.getElementById("heroPlayer");
  const overlay = document.querySelector(".video-overlay");
  const errorBox = document.getElementById("videoError");

  const videoSources = [
    "assets/videos/10_varkyan_1.mp4",
  ];

  const SHOW_MS = 7000;   // сколько держим один ролик в режиме слайдшоу
  const OVERLAY_MS = 350; // скорость появления белого экрана

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

            if (useOverlay && overlay) {
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
      overlay.classList.add("is-active");
      setTimeout(doLoad, OVERLAY_MS);
    } else {
      doLoad();
    }
  }

  function initVideo() {
    if (!videoEl) {
      vLog("❌ #heroPlayer not found in DOM.");
      return;
    }

    if (!videoSources || videoSources.length === 0) {
      vLog("❌ No video sources provided.");
      showError("⚠️ Нет доступных видео.");
      return;
    }

    // ✅ Режим одного видео — без слайдшоу и без setInterval
    if (videoSources.length === 1) {
      vLog("▶️ Single video mode (no slideshow).");
      // если нужно зациклить видео — оставляем loop = true
      videoEl.loop = true;
      playSource(videoSources[0], false);
      return;
    }

    // ✅ Режим слайдшоу для нескольких роликов
    vLog("▶️ Starting slideshow with white overlay transitions...");

    // первый ролик — без белого экрана
    playSource(videoSources[index], false);

    setInterval(() => {
      index = (index + 1) % videoSources.length;
      playSource(videoSources[index], true);
    }, SHOW_MS);
  }

  initVideo();

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
