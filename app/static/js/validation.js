// Form validation utilities
export function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

export function validatePhone(phone) {
  // Indian phone number: +91 followed by 10 digits, or just 10 digits
  const re = /^(\+91[\s-]?)?[6-9]\d{9}$/;
  return re.test(phone.replace(/\s/g, ""));
}

export function validatePassword(password) {
  // Min 8 chars, at least 1 uppercase, 1 lowercase, 1 number
  const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
  return re.test(password);
}

export function showFieldError(input, message) {
  const formGroup = input.closest(".form-group, .float-field");
  if (!formGroup) return;
  
  // Remove existing error
  const existing = formGroup.querySelector(".field-error");
  if (existing) existing.remove();
  
  // Add error message
  const error = document.createElement("span");
  error.className = "field-error";
  error.style.cssText = "color: var(--danger); font-size: var(--fs-xs); margin-top: 4px; display: block;";
  error.textContent = message;
  formGroup.appendChild(error);
  
  // Highlight input
  input.style.borderColor = "var(--danger)";
  input.addEventListener("input", function clearError() {
    input.style.borderColor = "";
    error.remove();
  }, { once: true });
}

export function validateForm(form) {
  let isValid = true;
  const inputs = form.querySelectorAll("input[required], select[required], textarea[required]");
  
  inputs.forEach(input => {
    if (!input.value.trim()) {
      showFieldError(input, "This field is required");
      isValid = false;
    }
    
    if (input.type === "email" && input.value && !validateEmail(input.value)) {
      showFieldError(input, "Please enter a valid email address");
      isValid = false;
    }
    
    if (input.type === "tel" && input.value && !validatePhone(input.value)) {
      showFieldError(input, "Please enter a valid phone number");
      isValid = false;
    }
  });
  
  return isValid;
}

// Initialize form validation on submit
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form[data-validate]").forEach(form => {
    form.addEventListener("submit", (e) => {
      if (!validateForm(form)) {
        e.preventDefault();
        window.toast?.("Please fix the errors before submitting", "error");
      }
    });
  });
});