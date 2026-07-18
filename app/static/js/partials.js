// Reusable navbar & footer injectors
const LINKS = [
  { href: "/", label: "Home" },
  { href: "/hotels", label: "Hotels" },
  { href: "/offers", label: "Offers" },
  { href: "/travel-guide", label: "Travel Guide" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
];

function navHTML() {
  return `
  <header class="nav" role="banner">
    <div class="nav-inner">
      <a class="logo" href="/" aria-label="Bhagalpur Stays">
        <span class="logo-mark">A</span>
        <span>
          Bhagalpur Stays
          <small>Hotels · Bihar</small>
        </span>
      </a>
      <nav aria-label="Primary">
        <ul class="nav-links">
          ${LINKS.map(l => `<li><a href="${l.href}">${l.label}</a></li>`).join("")}
        </ul>
      </nav>
      <div class="nav-actions">
        <a href="/hotel-register" class="btn btn-outline btn-sm btn-desktop">List Your Hotel</a>
        <button class="nav-icon-btn" data-theme-toggle aria-label="Toggle theme">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
        </button>
        <a href="/wishlist" class="nav-icon-btn" aria-label="Wishlist">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
        </a>
        <a href="/login" class="btn btn-primary btn-sm btn-desktop" id="nav-login-btn">Login</a>
        <a href="/admin-dashboard" class="btn btn-gold btn-sm btn-desktop hidden" id="nav-admin-btn">Admin</a>
        <a href="/owner-dashboard" class="btn btn-gold btn-sm btn-desktop hidden" id="nav-owner-btn">Dashboard</a>
        <a href="/profile" class="btn btn-outline btn-sm btn-desktop hidden" id="nav-profile-btn">Profile</a>
        <button class="btn btn-ghost btn-sm btn-desktop hidden" id="nav-logout-btn" onclick="doLogout()">Logout</button>
        <a href="/profile" class="avatar btn-desktop" aria-label="Profile">R</a>
        <button class="hamburger nav-icon-btn" data-drawer-open aria-label="Menu">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
        </button>
      </div>
    </div>
  </header>
  <div class="mobile-backdrop"></div>
  <aside class="mobile-drawer" aria-label="Mobile menu">
    <button class="close nav-icon-btn" data-drawer-close aria-label="Close menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22"><path d="M18 6L6 18M6 6l12 12"/></svg>
    </button>
    <nav>
      ${LINKS.map(l => `<a href="${l.href}">${l.label}</a>`).join("")}
      <a href="/hotel-register">Become a Hotel Partner</a>
      <a href="/my-bookings">My Bookings</a>
      <a href="/wishlist">Wishlist</a>
      <a href="/admin-dashboard" id="mobile-admin-link" class="hidden">Admin Dashboard</a>
      <a href="/owner-dashboard" id="mobile-owner-link" class="hidden">Partner Dashboard</a>
    </nav>
    <div class="drawer-cta" id="mobile-auth-btns">
      <a href="/login" class="btn btn-outline btn-block">Login</a>
      <a href="/signup" class="btn btn-primary btn-block">Create Account</a>
    </div>
    <div class="drawer-cta hidden" id="mobile-logout-btn">
      <button class="btn btn-ghost btn-block" onclick="doLogout()">Logout</button>
    </div>
  </aside>
  `;
}

function footerHTML() {
  return `
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="logo" href="/">
            <span class="logo-mark">A</span>
            <span>Bhagalpur Stays<small>Hotels · Bihar</small></span>
          </a>
          <p>The largest hotel booking platform for Bhagalpur. Discover, compare and book the best hotels in Silk City with confidence.</p>
          <div class="newsletter" style="max-width: 360px;">
            <input type="email" placeholder="Your email address" aria-label="Email">
            <button class="btn btn-gold btn-sm" onclick="event.preventDefault(); window.toast('Subscribed to newsletter','success')">Subscribe</button>
          </div>
        </div>
        <div class="footer-col">
          <h5>Company</h5>
          <ul>
            <li><a href="/about">About Us</a></li>
            <li><a href="/contact">Contact</a></li>
            <li><a href="/travel-guide">Travel Guide</a></li>
            <li><a href="/hotel-register">Partner Portal</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Explore</h5>
          <ul>
            <li><a href="/hotels">All Hotels</a></li>
            <li><a href="/offers">Special Offers</a></li>
            <li><a href="/hotels?tag=luxury">Luxury</a></li>
            <li><a href="/hotels?tag=budget">Budget</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Support</h5>
          <ul>
            <li><a href="/faq">FAQ</a></li>
            <li><a href="/my-bookings">My Bookings</a></li>
            <li><a href="/contact">Help Center</a></li>
            <li><a href="/contact">Cancellation</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Legal</h5>
          <ul>
            <li><a href="/privacy-policy">Privacy Policy</a></li>
            <li><a href="/terms">Terms &amp; Conditions</a></li>
            <li><a href="/terms">Refund Policy</a></li>
            <li><a href="/terms">Sitemap</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© ${new Date().getFullYear()} Bhagalpur Stays. All rights reserved.</div>
        <div class="socials" aria-label="Social">
          <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M22 12a10 10 0 10-11.6 9.9v-7H8v-3h2.4V9.5c0-2.4 1.4-3.7 3.6-3.7 1 0 2.1.2 2.1.2v2.3h-1.2c-1.2 0-1.5.7-1.5 1.5V12h2.6l-.4 3h-2.2v7A10 10 0 0022 12z"/></svg></a>
          <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
          <a href="#" aria-label="Twitter"><svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M22 5.9a8 8 0 01-2.4.7 4.2 4.2 0 001.8-2.3 8.5 8.5 0 01-2.6 1 4.1 4.1 0 00-7.1 3.8A11.6 11.6 0 013 4.9a4.2 4.2 0 001.3 5.5 4 4 0 01-1.9-.5v.1a4.1 4.1 0 003.3 4 4 4 0 01-1.8.1 4.1 4.1 0 003.8 2.9A8.2 8.2 0 012 18.6a11.5 11.5 0 006.3 1.9c7.5 0 11.6-6.3 11.6-11.7v-.5A8 8 0 0022 5.9z"/></svg></a>
          <a href="#" aria-label="YouTube"><svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M23 12s0-3.6-.5-5.3a2.8 2.8 0 00-2-2C18.9 4.2 12 4.2 12 4.2s-6.9 0-8.5.5a2.8 2.8 0 00-2 2C1 8.4 1 12 1 12s0 3.6.5 5.3a2.8 2.8 0 002 2c1.6.5 8.5.5 8.5.5s6.9 0 8.5-.5a2.8 2.8 0 002-2c.5-1.7.5-5.3.5-5.3zM9.8 15.3V8.7l5.7 3.3-5.7 3.3z"/></svg></a>
        </div>
      </div>
    </div>
  </footer>`;
}

// Cookie Consent Banner
function cookieBannerHTML() {
  if (localStorage.getItem('cookies-accepted')) return '';
  return '<div id="cookie-banner" style="position:fixed;bottom:0;left:0;right:0;background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;z-index:999;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;box-shadow:0 -4px 20px rgba(0,0,0,0.1);">' +
    '<p style="font-size:var(--fs-sm);color:var(--text-muted);max-width:600px;">🍪 We use cookies to enhance your experience. By continuing, you agree to our <a href="/privacy-policy">Privacy Policy</a>.</p>' +
    '<button class="btn btn-primary btn-sm" onclick="acceptCookies()">Accept</button>' +
  '</div>';
}

function acceptCookies() {
  localStorage.setItem('cookies-accepted', 'true');
  var banner = document.getElementById('cookie-banner');
  if (banner) banner.remove();
}

// Get user from JWT token
function getUserFromToken() {
  var token = localStorage.getItem('access_token');
  if (!token) return null;
  try {
    var payload = JSON.parse(atob(token.split('.')[1]));
    return payload;
  } catch(e) { return null; }
}

// Update navbar based on login state
function updateNavbar() {
  var user = getUserFromToken();
  var loginBtn = document.getElementById('nav-login-btn');
  var adminBtn = document.getElementById('nav-admin-btn');
  var ownerBtn = document.getElementById('nav-owner-btn');
  var profileBtn = document.getElementById('nav-profile-btn');
  var logoutBtn = document.getElementById('nav-logout-btn');
  var mobileAdmin = document.getElementById('mobile-admin-link');
  var mobileOwner = document.getElementById('mobile-owner-link');
  var mobileAuth = document.getElementById('mobile-auth-btns');
  var mobileLogout = document.getElementById('mobile-logout-btn');

  if (user) {
    if (loginBtn) loginBtn.classList.add('hidden');
    if (profileBtn) profileBtn.classList.remove('hidden');
    if (logoutBtn) logoutBtn.classList.remove('hidden');
    if (mobileAuth) mobileAuth.classList.add('hidden');
    if (mobileLogout) mobileLogout.classList.remove('hidden');
    if (user.role === 'admin' && adminBtn) adminBtn.classList.remove('hidden');
    if (user.role === 'admin' && mobileAdmin) mobileAdmin.classList.remove('hidden');
    if (user.role === 'owner' && ownerBtn) ownerBtn.classList.remove('hidden');
    if (user.role === 'owner' && mobileOwner) mobileOwner.classList.remove('hidden');
  } else {
    if (loginBtn) loginBtn.classList.remove('hidden');
    if (adminBtn) adminBtn.classList.add('hidden');
    if (ownerBtn) ownerBtn.classList.add('hidden');
    if (profileBtn) profileBtn.classList.add('hidden');
    if (logoutBtn) logoutBtn.classList.add('hidden');
    if (mobileAdmin) mobileAdmin.classList.add('hidden');
    if (mobileOwner) mobileOwner.classList.add('hidden');
    if (mobileAuth) mobileAuth.classList.remove('hidden');
    if (mobileLogout) mobileLogout.classList.add('hidden');
  }
}

// Logout function
function doLogout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  window.toast('Logged out', 'info');
  setTimeout(function() { location.href = '/'; }, 500);
}
window.showLoading = function() {
  var overlay = document.createElement('div');
  overlay.className = 'loading-overlay';
  overlay.id = 'loading-overlay';
  overlay.innerHTML = '<div class="loading-spinner"></div>';
  document.body.appendChild(overlay);
};

window.hideLoading = function() {
  var overlay = document.getElementById('loading-overlay');
  if (overlay) overlay.remove();
};

document.addEventListener("DOMContentLoaded", () => {
  const navSlot = document.getElementById("nav-slot");
  const footSlot = document.getElementById("footer-slot");
  if (navSlot) navSlot.innerHTML = navHTML();
  if (footSlot) footSlot.innerHTML = footerHTML();
  document.body.insertAdjacentHTML('beforeend', cookieBannerHTML());
  updateNavbar();
  
  // Load chatbot
  var chatScript = document.createElement('script');
  chatScript.src = '../static/js/chatbot.js';
  document.body.appendChild(chatScript);
});