// Notification badge and dropdown
export function updateNotificationBadge(count) {
  const dots = document.querySelectorAll(".nav-icon-btn .dot");
  dots.forEach(dot => {
    if (count > 0) {
      dot.style.display = "block";
      dot.textContent = count > 9 ? "9+" : count;
    } else {
      dot.style.display = "none";
    }
  });
}

export function fetchNotificationCount() {
  // Simulate fetching from API
  const count = Math.floor(Math.random() * 5);
  updateNotificationBadge(count);
  return count;
}

// Simulated notifications
const MOCK_NOTIFICATIONS = [
  { id: 1, title: "Booking confirmed", message: "Your stay at Ganga Vilas Palace is confirmed.", time: "2h ago", read: false },
  { id: 2, title: "Special offer", message: "Get 25% off on Silk City Inn this weekend!", time: "5h ago", read: false },
  { id: 3, title: "Review reminder", message: "How was your stay at Vikramshila Grand?", time: "1d ago", read: true },
];

export function renderNotificationDropdown(container) {
  if (!container) return;
  
  const unread = MOCK_NOTIFICATIONS.filter(n => !n.read).length;
  updateNotificationBadge(unread);
  
  container.innerHTML = `
    <div class="notif-header">
      <h4>Notifications</h4>
      ${unread > 0 ? `<span class="badge badge-danger">${unread} new</span>` : ""}
    </div>
    <div class="notif-list">
      ${MOCK_NOTIFICATIONS.map(n => `
        <div class="notif-item ${n.read ? '' : 'unread'}">
          <div class="notif-dot"></div>
          <div>
            <strong>${n.title}</strong>
            <p>${n.message}</p>
            <small>${n.time}</small>
          </div>
        </div>
      `).join("")}
    </div>
    <a href="notifications.html" class="notif-footer">View all notifications</a>
  `;
}

document.addEventListener("DOMContentLoaded", () => {
  fetchNotificationCount();
});