// Auth form handling
import { validateEmail, validatePassword, showFieldError } from './validation.js';

export function handleLogin(email, password) {
  // Simulate login
  if (!validateEmail(email)) {
    window.toast?.("Please enter a valid email address", "error");
    return false;
  }
  
  if (!password || password.length < 6) {
    window.toast?.("Password must be at least 6 characters", "error");
    return false;
  }
  
  // Mock successful login
  localStorage.setItem("abh-user", JSON.stringify({ email, name: "Guest User" }));
  window.toast?.("Welcome back!", "success");
  
  setTimeout(() => {
    window.location.href = "index.html";
  }, 1000);
  
  return true;
}

export function handleSignup(data) {
  const { name, email, password, confirmPassword } = data;
  
  if (!name || name.trim().length < 2) {
    window.toast?.("Please enter your full name", "error");
    return false;
  }
  
  if (!validateEmail(email)) {
    window.toast?.("Please enter a valid email address", "error");
    return false;
  }
  
  if (!validatePassword(password)) {
    window.toast?.("Password must be at least 8 characters with uppercase, lowercase, and number", "error");
    return false;
  }
  
  if (password !== confirmPassword) {
    window.toast?.("Passwords don't match", "error");
    return false;
  }
  
  // Mock successful signup
  localStorage.setItem("abh-user", JSON.stringify({ name, email }));
  window.toast?.("Account created successfully!", "success");
  
  setTimeout(() => {
    window.location.href = "index.html";
  }, 1000);
  
  return true;
}

export function isLoggedIn() {
  return !!localStorage.getItem("abh-user");
}

export function logout() {
  localStorage.removeItem("abh-user");
  window.toast?.("Logged out successfully", "info");
  setTimeout(() => {
    window.location.href = "index.html";
  }, 500);
}

// Initialize auth forms
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.querySelector("[data-login-form]");
  const signupForm = document.querySelector("[data-signup-form]");
  
  loginForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = loginForm.querySelector('[type="email"]')?.value;
    const password = loginForm.querySelector('[type="password"]')?.value;
    handleLogin(email, password);
  });
  
  signupForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = signupForm.querySelector('[name="name"]')?.value;
    const email = signupForm.querySelector('[type="email"]')?.value;
    const password = signupForm.querySelector('[name="password"]')?.value;
    const confirm = signupForm.querySelector('[name="confirm-password"]')?.value;
    handleSignup({ name, email, password, confirmPassword: confirm });
  });
});