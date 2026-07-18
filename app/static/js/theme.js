// Theme toggle functionality
const THEME_KEY = "abh-theme";

export function getTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved) return saved;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem(THEME_KEY, theme);
  
  // Update toggle buttons
  document.querySelectorAll("[data-theme-toggle]").forEach(btn => {
    btn.setAttribute("aria-pressed", String(theme === "dark"));
    const icon = btn.querySelector("svg");
    if (icon) {
      if (theme === "dark") {
        icon.innerHTML = '<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>';
      } else {
        icon.innerHTML = '<path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>';
      }
    }
  });
}

export function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  applyTheme(current === "dark" ? "light" : "dark");
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  applyTheme(getTheme());
  
  document.addEventListener("click", (e) => {
    const toggle = e.target.closest("[data-theme-toggle]");
    if (toggle) toggleTheme();
  });
});