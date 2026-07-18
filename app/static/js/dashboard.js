// Dashboard functionality
import { renderBarChart, renderStatCard } from './charts.js';

export function initDashboard() {
  // Weekly booking data
  const weeklyData = [
    { label: "M", value: 55 },
    { label: "T", value: 62 },
    { label: "W", value: 70 },
    { label: "T", value: 88 },
    { label: "F", value: 96 },
    { label: "S", value: 100 },
    { label: "S", value: 82 },
  ];
  
  const chartContainer = document.querySelector(".chart-bars");
  if (!chartContainer) {
    // Find or create chart area
    const panel = document.querySelector(".panel .chart-bars");
    if (panel) {
      renderBarChart(panel, weeklyData);
    }
  }
}

document.addEventListener("DOMContentLoaded", initDashboard);