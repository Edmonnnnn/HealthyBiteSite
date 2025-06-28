console.log("✅ Healthy Bite frontend loaded");

document.addEventListener("DOMContentLoaded", () => {
  const startBtn = document.getElementById("startVideos");
  const videoElement = document.getElementById("heroPlayer");

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

  let currentIndex = 0;

  function playNextVideo() {
    const src = videoSources[currentIndex];
    console.log(`🎬 Playing video [${currentIndex + 1}/${videoSources.length}]: ${src}`);
    videoElement.classList.remove("fade-in");

    videoElement.src = src;
    videoElement.load();

    videoElement
      .play()
      .then(() => {
        setTimeout(() => videoElement.classList.add("fade-in"), 100);
      })
      .catch((err) => {
        console.error("⚠️ Video playback error:", err);
      });

    currentIndex = (currentIndex + 1) % videoSources.length;
  }

  function startSlideshow() {
    console.log("🟢 Starting video slideshow...");
    playNextVideo();
    setInterval(playNextVideo, 5000);
  }

  if (startBtn) {
    startBtn.onclick = () => {
      console.log("👆 Start button clicked");
      startBtn.remove();
      startSlideshow();
    };
  } else {
    console.warn("⚠️ Button #startVideos not found in DOM");
  }

  // Optional fade animation for About section
  const about = document.querySelector(".fade-up");
  if (about) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("show");
        }
      });
    }, { threshold: 0.3 });
    obs.observe(about);
  }
});
