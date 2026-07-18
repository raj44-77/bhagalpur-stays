// Navbar scroll behavior and mobile drawer
function initNavbar() {
  const nav = document.querySelector(".nav");
  
  // Scroll effect
  if (nav) {
    const onScroll = () => {
      nav.classList.toggle("scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }
  
  // Mobile drawer
  const drawer = document.querySelector(".mobile-drawer");
  const backdrop = document.querySelector(".mobile-backdrop");
  const openBtn = document.querySelector("[data-drawer-open]");
  const closeBtn = document.querySelector("[data-drawer-close]");
  
  const close = () => {
    drawer?.classList.remove("open");
    backdrop?.classList.remove("open");
    document.body.style.overflow = "";
  };
  
  const open = () => {
    drawer?.classList.add("open");
    backdrop?.classList.add("open");
    document.body.style.overflow = "hidden";
  };
  
  openBtn?.addEventListener("click", open);
  closeBtn?.addEventListener("click", close);
  backdrop?.addEventListener("click", close);
  
  // Close drawer when a link is clicked
  drawer?.querySelectorAll("a").forEach(a => {
    a.addEventListener("click", close);
  });
}

// Active nav link highlighting
function markActiveNav() {
  const path = location.pathname.replace(/\/$/, "") || "/index.html";
  
  document.querySelectorAll(".nav-links a, .mobile-drawer nav a").forEach(a => {
    const href = a.getAttribute("href");
    if (!href) return;
    const norm = href.replace(/\/$/, "");
    if (norm === path || (path.endsWith(norm) && norm !== "/index.html")) {
      a.classList.add("active");
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initNavbar();
  markActiveNav();
});