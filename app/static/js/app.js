// =============================================
// App.js — shared UI: navbar, theme, toast, modal
// reveal-on-scroll, counters, ripple
// =============================================
/* ---------- Theme ---------- */
const THEME_KEY = "abh-theme";
function applyTheme(t) {
  document.documentElement.setAttribute("data-theme", t);
  localStorage.setItem(THEME_KEY, t);
  const btns = document.querySelectorAll("[data-theme-toggle]");
  btns.forEach(b => b.setAttribute("aria-pressed", String(t === "dark")));
}
function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(saved || (prefersDark ? "dark" : "light"));
  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-theme-toggle]");
    if (!t) return;
    const cur = document.documentElement.getAttribute("data-theme");
    applyTheme(cur === "dark" ? "light" : "dark");
  });
}
/* ---------- Navbar ---------- */
function initNavbar() {
  const nav = document.querySelector(".nav");
  if (nav) {
    const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }
  const drawer = document.querySelector(".mobile-drawer");
  const backdrop = document.querySelector(".mobile-backdrop");
  const openBtn = document.querySelector("[data-drawer-open]");
  const closeBtn = document.querySelector("[data-drawer-close]");
  const close = () => { drawer?.classList.remove("open"); backdrop?.classList.remove("open"); document.body.style.overflow = ""; };
  const open = () => { drawer?.classList.add("open"); backdrop?.classList.add("open"); document.body.style.overflow = "hidden"; };
  openBtn?.addEventListener("click", open);
  closeBtn?.addEventListener("click", close);
  backdrop?.addEventListener("click", close);
  drawer?.querySelectorAll("a").forEach(a => a.addEventListener("click", close));
}
/* ---------- Toast ---------- */
export function toast(msg, kind = "info") {
  let stack = document.querySelector(".toast-stack");
  if (!stack) {
    stack = document.createElement("div");
    stack.className = "toast-stack";
    document.body.appendChild(stack);
  }
  const el = document.createElement("div");
  el.className = `toast ${kind}`;
  el.innerHTML = `<span>${msg}</span>`;
  stack.appendChild(el);
  setTimeout(() => {
    el.style.animation = "toast-in .3s var(--ease-out) reverse";
    setTimeout(() => el.remove(), 300);
  }, 3200);
}
window.toast = toast;
/* ---------- Modal ---------- */
function initModals() {
  document.addEventListener("click", (e) => {
    const opener = e.target.closest("[data-modal-open]");
    if (opener) {
      const id = opener.getAttribute("data-modal-open");
      document.getElementById(id)?.classList.add("open");
      document.body.style.overflow = "hidden";
    }
    const closer = e.target.closest("[data-modal-close]");
    if (closer) {
      closer.closest(".modal-backdrop")?.classList.remove("open");
      document.body.style.overflow = "";
    }
    if (e.target.classList?.contains("modal-backdrop")) {
      e.target.classList.remove("open");
      document.body.style.overflow = "";
    }
  });
}
/* ---------- Reveal on scroll ---------- */
function initReveal() {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        en.target.classList.add("visible");
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -60px 0px" });
  document.querySelectorAll("[data-reveal]").forEach(el => io.observe(el));
}
/* ---------- Counters ---------- */
function animateCount(el) {
  const target = parseFloat(el.getAttribute("data-count") || "0");
  const dur = 1400;
  const suffix = el.getAttribute("data-suffix") || "";
  const start = performance.now();
  const step = (t) => {
    const p = Math.min((t - start) / dur, 1);
    const v = target * (1 - Math.pow(1 - p, 3));
    el.textContent = (target % 1 === 0 ? Math.round(v).toLocaleString() : v.toFixed(1)) + suffix;
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}
function initCounters() {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        animateCount(en.target);
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll("[data-count]").forEach(el => io.observe(el));
}
/* ---------- Ripple ---------- */
function initRipple() {
  document.addEventListener("pointerdown", (e) => {
    const btn = e.target.closest(".btn");
    if (!btn) return;
    const rect = btn.getBoundingClientRect();
    btn.style.setProperty("--x", ((e.clientX - rect.left) / rect.width * 100) + "%");
    btn.style.setProperty("--y", ((e.clientY - rect.top) / rect.height * 100) + "%");
  });
}
/* ---------- Accordion ---------- */
function initAccordion() {
  document.querySelectorAll(".accordion-head").forEach(head => {
    head.addEventListener("click", () => {
      const acc = head.closest(".accordion");
      const body = acc.querySelector(".accordion-body");
      const inner = acc.querySelector(".accordion-body-inner");
      const open = acc.classList.toggle("open");
      body.style.maxHeight = open ? inner.offsetHeight + "px" : "0";
    });
  });
}
/* ---------- Tabs ---------- */
function initTabs() {
  document.querySelectorAll("[data-tabs]").forEach(group => {
    const buttons = group.querySelectorAll(".tabs button");
    const panels = document.querySelectorAll(`[data-tab-panel][data-tabs-target="${group.dataset.tabs}"]`);
    buttons.forEach(b => b.addEventListener("click", () => {
      buttons.forEach(x => x.classList.remove("active"));
      b.classList.add("active");
      const key = b.dataset.tab;
      panels.forEach(p => p.classList.toggle("hidden", p.dataset.tabPanel !== key));
    }));
  });
}
/* ---------- Wishlist toggle ---------- */
function initWishlist() {
  document.addEventListener("click", (e) => {
    const w = e.target.closest(".wishlist");
    if (!w) return;
    e.preventDefault(); e.stopPropagation();
    w.classList.toggle("active");
    toast(w.classList.contains("active") ? "Added to wishlist" : "Removed from wishlist",
          w.classList.contains("active") ? "success" : "info");
  });
}
/* ---------- Set active nav link ---------- */
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
/* ---------- Init ---------- */
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initNavbar();
  initModals();
  initReveal();
  initCounters();
  initRipple();
  initAccordion();
  initTabs();
  initWishlist();
  markActiveNav();
  document.querySelector("main")?.classList.add("silk-fade-in");
});
