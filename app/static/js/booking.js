// Booking form logic
export function calculateTotal(pricePerNight, nights, discount = 0) {
  const subtotal = pricePerNight * nights;
  const tax = subtotal * 0.12; // 12% GST
  const total = subtotal + tax - discount;
  
  return {
    subtotal,
    tax: Math.round(tax),
    discount,
    total: Math.round(total),
  };
}

export function formatPrice(amount) {
  return "₹" + amount.toLocaleString("en-IN");
}

export function getNights(checkIn, checkOut) {
  const start = new Date(checkIn);
  const end = new Date(checkOut);
  const diff = end - start;
  return Math.max(1, Math.ceil(diff / (1000 * 60 * 60 * 24)));
}

export function generateBookingId() {
  const prefix = "ABH";
  const year = new Date().getFullYear();
  const random = Math.floor(1000 + Math.random() * 9000);
  return `${prefix}-${year}-${random}`;
}

// Initialize booking page
document.addEventListener("DOMContentLoaded", () => {
  const bookingForm = document.querySelector("[data-booking-form]");
  if (!bookingForm) return;
  
  const checkIn = bookingForm.querySelector('[name="checkin"]');
  const checkOut = bookingForm.querySelector('[name="checkout"]');
  const priceDisplay = bookingForm.querySelector("[data-price-display]");
  
  function updatePrice() {
    if (checkIn && checkOut && priceDisplay) {
      const nights = getNights(checkIn.value, checkOut.value);
      const pricePerNight = parseInt(priceDisplay.dataset.price) || 0;
      const { total } = calculateTotal(pricePerNight, nights);
      priceDisplay.textContent = formatPrice(total);
    }
  }
  
  checkIn?.addEventListener("change", updatePrice);
  checkOut?.addEventListener("change", updatePrice);
  
  // Set min dates
  const today = new Date().toISOString().split("T")[0];
  if (checkIn) checkIn.min = today;
  if (checkOut) {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    checkOut.min = tomorrow.toISOString().split("T")[0];
  }
});