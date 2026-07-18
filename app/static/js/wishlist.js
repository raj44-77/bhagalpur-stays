// Wishlist management
const WISHLIST_KEY = "abh-wishlist";

export function getWishlist() {
  try {
    return JSON.parse(localStorage.getItem(WISHLIST_KEY)) || [];
  } catch {
    return [];
  }
}

export function addToWishlist(hotelId) {
  const wishlist = getWishlist();
  if (!wishlist.includes(hotelId)) {
    wishlist.push(hotelId);
    localStorage.setItem(WISHLIST_KEY, JSON.stringify(wishlist));
    return true;
  }
  return false;
}

export function removeFromWishlist(hotelId) {
  let wishlist = getWishlist();
  wishlist = wishlist.filter(id => id !== hotelId);
  localStorage.setItem(WISHLIST_KEY, JSON.stringify(wishlist));
}

export function isInWishlist(hotelId) {
  return getWishlist().includes(hotelId);
}

export function toggleWishlist(hotelId) {
  if (isInWishlist(hotelId)) {
    removeFromWishlist(hotelId);
    return false;
  } else {
    addToWishlist(hotelId);
    return true;
  }
}

// Initialize wishlist buttons
document.addEventListener("DOMContentLoaded", () => {
  updateWishlistButtons();
  
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".wishlist");
    if (!btn) return;
    
    e.preventDefault();
    e.stopPropagation();
    
    const hotelId = btn.dataset.hotelId;
    if (!hotelId) return;
    
    const added = toggleWishlist(hotelId);
    btn.classList.toggle("active", added);
    
    window.toast?.(
      added ? "Added to wishlist" : "Removed from wishlist",
      added ? "success" : "info"
    );
  });
});

export function updateWishlistButtons() {
  const wishlist = getWishlist();
  
  document.querySelectorAll(".wishlist").forEach(btn => {
    const hotelId = btn.dataset.hotelId;
    if (hotelId && wishlist.includes(hotelId)) {
      btn.classList.add("active");
    }
  });
}