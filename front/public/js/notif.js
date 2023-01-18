// Pssst, I've created a github package - https://github.com/brookesb91/dismissible

const showBanner = (selector, text) => {
  hideBanners();
  // Ensure animation plays even if the same alert type is triggered.
  requestAnimationFrame(() => {
    const banner = document.querySelector(selector);
    banner.classList.add("visible");
    setTimeout(function(){
        hideBanners();
    }, 4000);
  });
  if (selector == '.banner.error') {
    const text_banner = document.getElementById('error-message')
    text_banner.innerHTML = text
  }
  if (selector == '.banner.success') {
    const text_banner = document.getElementById('success-message')
    text_banner.innerHTML = text
  }

};

const hideBanners = (e) => {
  document
    .querySelectorAll(".error")
    .forEach((b) => b.classList.remove("visible"));
  document
    .querySelectorAll(".success")
    .forEach((b) => b.classList.remove("visible"));
};
