// Filter management for hotel listing
export class FilterManager {
  constructor() {
    this.filters = {
      maxPrice: null,
      minRating: null,
      category: null,
      amenities: [],
      tag: null,
      freeCancellation: false,
      instantConfirmation: false,
    };
  }
  
  setFilter(key, value) {
    this.filters[key] = value;
    return this;
  }
  
  toggleAmenity(amenity) {
    const index = this.filters.amenities.indexOf(amenity);
    if (index > -1) {
      this.filters.amenities.splice(index, 1);
    } else {
      this.filters.amenities.push(amenity);
    }
    return this;
  }
  
  getFilters() {
    return { ...this.filters };
  }
  
  reset() {
    this.filters = {
      maxPrice: null,
      minRating: null,
      category: null,
      amenities: [],
      tag: null,
      freeCancellation: false,
      instantConfirmation: false,
    };
    return this;
  }
  
  hasActiveFilters() {
    return (
      this.filters.maxPrice !== null ||
      this.filters.minRating !== null ||
      this.filters.category !== null ||
      this.filters.amenities.length > 0 ||
      this.filters.tag !== null ||
      this.filters.freeCancellation ||
      this.filters.instantConfirmation
    );
  }
}

// Initialize filter UI
document.addEventListener("DOMContentLoaded", () => {
  const filterForm = document.querySelector("[data-filters]");
  const resetBtn = document.querySelector("[data-filters-reset]");
  
  if (filterForm) {
    const manager = new FilterManager();
    
    filterForm.addEventListener("change", () => {
      const formData = new FormData(filterForm);
      // Handle filter changes
      for (let [key, value] of formData.entries()) {
        if (key === "amenities") {
          manager.toggleAmenity(value);
        } else {
          manager.setFilter(key, value);
        }
      }
      
      // Dispatch event with current filters
      window.dispatchEvent(new CustomEvent("filters-changed", {
        detail: manager.getFilters()
      }));
    });
    
    resetBtn?.addEventListener("click", () => {
      manager.reset();
      filterForm.reset();
      window.dispatchEvent(new CustomEvent("filters-changed", {
        detail: manager.getFilters()
      }));
    });
  }
});