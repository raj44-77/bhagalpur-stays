// Simple chart rendering for dashboards
export function renderBarChart(container, data, options = {}) {
  if (!container) return;
  
  const maxVal = Math.max(...data.map(d => d.value), 1);
  
  container.innerHTML = `
    <div class="chart-bars">
      ${data.map(d => `
        <div class="bar" style="height: ${(d.value / maxVal) * 100}%;" title="${d.label}: ${d.value}">
          <span>${d.label}</span>
        </div>
      `).join("")}
    </div>
  `;
}

export function renderLineChart(container, data, options = {}) {
  if (!container) return;
  
  const width = container.clientWidth || 600;
  const height = options.height || 240;
  const padding = options.padding || 40;
  
  const maxVal = Math.max(...data.map(d => d.value), 1);
  const points = data.map((d, i) => {
    const x = padding + (i / (data.length - 1)) * (width - padding * 2);
    const y = height - padding - (d.value / maxVal) * (height - padding * 2);
    return `${x},${y}`;
  }).join(" ");
  
  container.innerHTML = `
    <svg class="chart" viewBox="0 0 ${width} ${height}" style="width:100%; height:${height}px;">
      <polyline points="${points}" fill="none" stroke="var(--brand)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      ${data.map((d, i) => {
        const x = padding + (i / (data.length - 1)) * (width - padding * 2);
        const y = height - padding - (d.value / maxVal) * (height - padding * 2);
        return `<circle cx="${x}" cy="${y}" r="4" fill="var(--brand)"/>`;
      }).join("")}
    </svg>
  `;
}

export function renderStatCard(container, { label, value, change, icon }) {
  if (!container) return;
  
  container.innerHTML = `
    <div class="kpi">
      <div class="head">
        <div>
          <div class="label">${label}</div>
          <div class="val">${value}</div>
        </div>
        ${icon ? `<div class="icon-badge">${icon}</div>` : ""}
      </div>
      ${change ? `<div class="delta ${change > 0 ? 'up' : 'down'}">${change > 0 ? '↑' : '↓'} ${Math.abs(change)}%</div>` : ""}
    </div>
  `;
}