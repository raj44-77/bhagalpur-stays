// Footer newsletter and dynamic year
document.addEventListener("DOMContentLoaded", () => {
  // Update copyright year
  const yearSpan = document.querySelector("[data-current-year]");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }
  
  // Newsletter form
  const newsletterForms = document.querySelectorAll(".newsletter");
  newsletterForms.forEach(form => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = form.querySelector('input[type="email"]');
      if (email && email.value) {
        window.toast?.("Welcome aboard! Check your inbox for 20% off.", "success");
        email.value = "";
      }
    });
  });
});