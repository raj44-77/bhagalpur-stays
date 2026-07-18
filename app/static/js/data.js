// Dummy hotel data — realistic Bhagalpur listings
export const HOTELS = [
  {
    id: "h1",
    name: "The Ganga Vilas Palace",
    location: "Adampur, Bhagalpur",
    distance: "0.8 km from Bhagalpur Junction",
    price: 4899, strike: 6499, discount: 25,
    rating: 4.8, reviews: 1284,
    tag: "Luxury", tagKind: "gold",
    image: "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1000&auto=format&fit=crop",
    gallery: [
      "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1400",
      "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=1400",
      "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=1400",
      "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=1400",
      "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1400",
    ],
    amenities: ["Free WiFi", "Pool", "Spa", "Restaurant", "Gym", "Parking", "AC", "Room Service"],
    category: "luxury",
  },
  {
    id: "h2",
    name: "Vikramshila Grand",
    location: "Tilkamanjhi, Bhagalpur",
    distance: "1.2 km from City Center",
    price: 2999, strike: 3999, discount: 25,
    rating: 4.6, reviews: 892,
    tag: "Popular", tagKind: "solid-gold",
    image: "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=1000&auto=format&fit=crop",
    gallery: [
      "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=1400",
      "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=1400",
      "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=1400",
    ],
    amenities: ["Free WiFi", "Restaurant", "Breakfast", "Parking", "AC"],
    category: "business",
  },
  {
    id: "h3",
    name: "Silk City Inn",
    location: "Nathnagar, Bhagalpur",
    distance: "3.5 km from Junction",
    price: 1499, strike: 2199, discount: 32,
    rating: 4.3, reviews: 512,
    tag: "Budget Pick", tagKind: "gold",
    image: "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=1000&auto=format&fit=crop",
    gallery: ["https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=1400"],
    amenities: ["Free WiFi", "AC", "Parking", "Room Service"],
    category: "budget",
  },
  {
    id: "h4",
    name: "Vikramshila Riverside Resort",
    location: "Sultanganj Road, Bhagalpur",
    distance: "5 km from City Center",
    price: 5499, strike: 6999, discount: 21,
    rating: 4.9, reviews: 734,
    tag: "Editor's Choice", tagKind: "dark",
    image: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1000&auto=format&fit=crop",
    gallery: ["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1400"],
    amenities: ["Free WiFi", "Pool", "Spa", "Restaurant", "Gym", "Parking", "Pet Friendly"],
    category: "luxury",
  },
  {
    id: "h5",
    name: "Hotel Kohinoor Residency",
    location: "Bhikhanpur, Bhagalpur",
    distance: "0.5 km from Bus Stand",
    price: 1899, strike: 2599, discount: 27,
    rating: 4.4, reviews: 428,
    tag: "Family Friendly", tagKind: "success",
    image: "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=1000&auto=format&fit=crop",
    gallery: ["https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=1400"],
    amenities: ["Free WiFi", "Restaurant", "Breakfast", "AC", "Family Rooms"],
    category: "family",
  },
  {
    id: "h6",
    name: "The Champa Boutique",
    location: "Barari, Bhagalpur",
    distance: "2 km from Riverside",
    price: 3499, strike: 4499, discount: 22,
    rating: 4.7, reviews: 615,
    tag: "Couple Friendly", tagKind: "brand",
    image: "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=1000&auto=format&fit=crop",
    gallery: ["https://images.unsplash.com/photo-1582719508461-905c673771fd?w=1400"],
    amenities: ["Free WiFi", "Restaurant", "Spa", "Room Service", "AC"],
    category: "couple",
  },
  {
    id: "h7",
    name: "Business Suites Bhagalpur",
    location: "Court Road, Bhagalpur",
    distance: "0.3 km from Metro",
    price: 2699, strike: 3499, discount: 23,
    rating: 4.5, reviews: 389,
    tag: "Business", tagKind: "brand",
    image: "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1000&auto=format&fit=crop",
    gallery: ["https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1400"],
    amenities: ["Free WiFi", "Gym", "Breakfast", "Meeting Room", "AC"],
    category: "business",
  },
  {
    id: "h8",
    name: "Ganga View Homestay",
    location: "Champanagar, Bhagalpur",
    distance: "4 km from Junction",
    price: 999, strike: 1499, discount: 33,
    rating: 4.2, reviews: 245,
    tag: "Homestay", tagKind: "gold",
    image: "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=1000&auto=format&fit=crop",
    gallery: ["https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=1400"],
    amenities: ["Free WiFi", "Breakfast", "AC", "Parking"],
    category: "budget",
  },
];
export const CATEGORIES = [
  { key: "luxury", label: "Luxury Collection", icon: "sparkles" },
  { key: "budget", label: "Budget Stays", icon: "wallet" },
  { key: "family", label: "Family Hotels", icon: "users" },
  { key: "business", label: "Business Hotels", icon: "briefcase" },
  { key: "couple", label: "Couple Friendly", icon: "heart" },
  { key: "airport", label: "Near Airport", icon: "plane" },
];
// Simple SVG icon lookup
export const ICON = {
  wifi: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M5 12.55a11 11 0 0114 0M8.5 16.05a6 6 0 017 0M2 8.82a15 15 0 0120 0"/><circle cx="12" cy="20" r="1" fill="currentColor"/></svg>`,
  park: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="3" y="6" width="18" height="12" rx="2"/><path d="M9 9v6M14 9h1a2 2 0 010 4h-1"/></svg>`,
  breakfast: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M17 8h1a4 4 0 010 8h-1"/><path d="M3 8h14v9a4 4 0 01-4 4H7a4 4 0 01-4-4V8z"/></svg>`,
  ac: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M12 2v20M2 12h20M4.9 4.9l14.2 14.2M19.1 4.9L4.9 19.1"/></svg>`,
  pool: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M2 20c2 0 2-2 4-2s2 2 4 2 2-2 4-2 2 2 4 2 2-2 4-2M6 15V6a3 3 0 016 0M12 6h6"/></svg>`,
  gym: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M4 8v8M8 6v12M16 6v12M20 8v8M2 12h4M18 12h4M8 12h8"/></svg>`,
  spa: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M12 22c3-4 3-8 0-14M12 22c-3-4-3-8 0-14M12 22c-4-2-8-3-12-3M12 22c4-2 8-3 12-3"/></svg>`,
  restaurant: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M3 2v20M7 2v20M11 2v6a4 4 0 01-8 0M17 2c-2 0-4 2-4 6s2 5 4 5v9"/></svg>`,
  service: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M12 2a8 8 0 018 8v4a2 2 0 01-2 2h-2v-6h4M6 16h2v-6H4a2 2 0 00-2 2v2a2 2 0 002 2"/></svg>`,
  pet: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><circle cx="6" cy="10" r="2"/><circle cx="10" cy="5" r="2"/><circle cx="14" cy="5" r="2"/><circle cx="18" cy="10" r="2"/><path d="M12 12a4 4 0 014 4c0 3-3 5-4 5s-4-2-4-5a4 4 0 014-4z"/></svg>`,
  meeting: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M7 22h10M12 18v4"/></svg>`,
  family: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><circle cx="9" cy="7" r="3"/><circle cx="17" cy="9" r="2"/><path d="M3 21a6 6 0 0112 0M14 21a4 4 0 018 0"/></svg>`,
};
export function iconFor(amenity) {
  const map = {
    "Free WiFi": ICON.wifi, "Parking": ICON.park, "Breakfast": ICON.breakfast,
    "AC": ICON.ac, "Pool": ICON.pool, "Gym": ICON.gym, "Spa": ICON.spa,
    "Restaurant": ICON.restaurant, "Room Service": ICON.service,
    "Pet Friendly": ICON.pet, "Meeting Room": ICON.meeting, "Family Rooms": ICON.family,
  };
  return map[amenity] || `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>`;
}
export function star(filled) {
  return filled
    ? `<svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`
    : `<svg class="dim" viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`;
}
export function stars(n) {
  const full = Math.round(n);
  return `<div class="stars" aria-label="${n} out of 5">${
    Array.from({length: 5}, (_, i) => star(i < full)).join("")
  }</div>`;
}
export function hotelCard(h) {
  return `
    <a class="hotel-card" href="hotel-details.html?id=${h.id}" data-reveal>
      <div class="thumb">
        <img src="${h.image}" alt="${h.name}" loading="lazy">
        <div class="thumb-badges">
          <span class="badge badge-${h.tagKind}">${h.tag}</span>
          ${h.discount ? `<span class="badge badge-danger">-${h.discount}%</span>` : ""}
        </div>
        <button class="wishlist" aria-label="Add to wishlist">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
        </button>
      </div>
      <div class="info">
        <div>
          <div class="name">${h.name}</div>
          <div class="loc">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
            ${h.location}
          </div>
        </div>
        <div class="amenities">
          ${h.amenities.slice(0,4).map(a => `<span>${iconFor(a)}${a}</span>`).join("")}
        </div>
        <div class="foot">
          <div class="price">
            ${h.strike ? `<div class="strike">₹${h.strike.toLocaleString()}</div>` : ""}
            <div class="amount">₹${h.price.toLocaleString()}</div>
            <div class="per">per night · incl. taxes</div>
          </div>
          <div class="rating-block" style="text-align:right; display:flex; flex-direction:column; align-items:flex-end; gap:4px;">
            <span class="rating-chip">
              <svg viewBox="0 0 24 24" fill="currentColor" width="12" height="12"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
              ${h.rating}
            </span>
            <small class="muted">${h.reviews.toLocaleString()} reviews</small>
          </div>
        </div>
      </div>
    </a>
  `;
}
