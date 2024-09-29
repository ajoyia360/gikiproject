// friendsystem/static/friendsystem/js/custom_admin.js

document.addEventListener("DOMContentLoaded", function () {
  // Fade-in effect on page load
  const adminPanels = document.querySelectorAll(".admin-panel");
  adminPanels.forEach((panel) => {
    panel.style.opacity = "0";
    setTimeout(() => {
      panel.style.transition = "opacity 0.5s ease-in-out";
      panel.style.opacity = "1";
    }, 100);
  });

  // Add additional JS as needed
});
