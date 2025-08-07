window.addEventListener("DOMContentLoaded", () => {
  const currentPath = window.location.pathname;

  if (currentPath === "/" || currentPath.includes("login")) {
    // Borra todo localStorage si vuelve al login
    localStorage.clear();
  }
});

window.addEventListener("pageshow", function (event) {
  const currentPath = window.location.pathname;

  if (currentPath === "/" || currentPath.includes("login")) {
    if (event.persisted) {
      // La página fue restaurada desde cache (browsing back/forward)
      localStorage.clear();
    }
  }
});