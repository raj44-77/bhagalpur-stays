// Modal system
function initModals() {
  // Open modal
  document.addEventListener("click", (e) => {
    const opener = e.target.closest("[data-modal-open]");
    if (opener) {
      const id = opener.getAttribute("data-modal-open");
      const modal = document.getElementById(id);
      if (modal) {
        modal.classList.add("open");
        document.body.style.overflow = "hidden";
        
        // Focus trap
        const focusable = modal.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length) focusable[0].focus();
      }
    }
  });
  
  // Close modal
  document.addEventListener("click", (e) => {
    const closer = e.target.closest("[data-modal-close]");
    if (closer) {
      const modal = closer.closest(".modal-backdrop");
      if (modal) {
        modal.classList.remove("open");
        document.body.style.overflow = "";
      }
    }
    
    // Click backdrop to close
    if (e.target.classList.contains("modal-backdrop")) {
      e.target.classList.remove("open");
      document.body.style.overflow = "";
    }
  });
  
  // Escape key to close
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const openModal = document.querySelector(".modal-backdrop.open");
      if (openModal) {
        openModal.classList.remove("open");
        document.body.style.overflow = "";
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", initModals);