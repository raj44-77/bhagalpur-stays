// Search functionality for hotels
import { HOTELS } from './data.js';

export function searchHotels(query) {
  if (!query || query.trim().length < 2) return HOTELS;
  
  const q = query.toLowerCase().trim();
  
  return HOTELS.filter(hotel => {
    return (
      hotel.name.toLowerCase().includes(q) ||
      hotel.location.toLowerCase().includes(q) ||
      hotel.tag.toLowerCase().includes(q) ||
      hotel.amenities.some(a => a.toLowerCase().includes(q)) ||
      hotel.category.toLowerCase().includes(q)
    );
  });
}

export function filterHotels(filters = {}) {
  let results = [...HOTELS];
  
  // Price range
  if (filters.maxPrice) {
    results = results.filter(h => h.price <= filters.maxPrice);
  }
  
  // Star rating
  if (filters.minRating) {
    results = results.filter(h => h.rating >= filters.minRating);
  }
  
  // Category
  if (filters.category) {
    results = results.filter(h => h.category === filters.category);
  }
  
  // Amenities
  if (filters.amenities && filters.amenities.length) {
    results = results.filter(h => 
      filters.amenities.every(a => h.amenities.includes(a))
    );
  }
  
  // Tags
  if (filters.tag) {
    results = results.filter(h => h.tag.toLowerCase() === filters.tag.toLowerCase());
  }
  
  return results;
}

export function sortHotels(hotels, sortBy = "popularity") {
  const sorted = [...hotels];
  
  switch (sortBy) {
    case "price-low":
      return sorted.sort((a, b) => a.price - b.price);
    case "price-high":
      return sorted.sort((a, b) => b.price - a.price);
    case "rating":
      return sorted.sort((a, b) => b.rating - a.rating);
    case "reviews":
      return sorted.sort((a, b) => b.reviews - a.reviews);
    default:
      return sorted; // Default: popularity (original order)
  }
}

// Live search initialization
document.addEventListener("DOMContentLoaded", () => {
  const searchInputs = document.querySelectorAll("[data-search]");
  
  searchInputs.forEach(input => {
    const target = document.querySelector(input.dataset.search);
    if (!target) return;
    
    input.addEventListener("input", () => {
      const results = searchHotels(input.value);
      // Dispatch custom event for the page to handle
      target.dispatchEvent(new CustomEvent("search-results", { 
        detail: { results, query: input.value } 
      }));
    });
  });
});