// Pagination utility
export class Pagination {
  constructor(items, perPage = 10) {
    this.items = items;
    this.perPage = perPage;
    this.currentPage = 1;
  }
  
  get totalPages() {
    return Math.ceil(this.items.length / this.perPage);
  }
  
  get currentItems() {
    const start = (this.currentPage - 1) * this.perPage;
    const end = start + this.perPage;
    return this.items.slice(start, end);
  }
  
  goToPage(page) {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
    return this;
  }
  
  next() {
    return this.goToPage(this.currentPage + 1);
  }
  
  prev() {
    return this.goToPage(this.currentPage - 1);
  }
  
  getPageNumbers(maxVisible = 5) {
    const pages = [];
    const total = this.totalPages;
    
    if (total <= maxVisible) {
      for (let i = 1; i <= total; i++) pages.push(i);
    } else {
      pages.push(1);
      
      let start = Math.max(2, this.currentPage - 1);
      let end = Math.min(total - 1, this.currentPage + 1);
      
      if (start > 2) pages.push("…");
      
      for (let i = start; i <= end; i++) pages.push(i);
      
      if (end < total - 1) pages.push("…");
      
      pages.push(total);
    }
    
    return pages;
  }
}

// Render pagination UI
export function renderPagination(container, pagination, onPageChange) {
  if (!container) return;
  
  const pages = pagination.getPageNumbers();
  
  container.innerHTML = `
    <button ${pagination.currentPage === 1 ? "disabled" : ""} data-page="prev" aria-label="Previous">‹</button>
    ${pages.map(p => {
      if (p === "…") return "<button disabled>…</button>";
      return `<button class="${p === pagination.currentPage ? 'active' : ''}" data-page="${p}">${p}</button>`;
    }).join("")}
    <button ${pagination.currentPage === pagination.totalPages ? "disabled" : ""} data-page="next" aria-label="Next">›</button>
  `;
  
  // Event delegation
  container.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn || btn.disabled) return;
    
    const page = btn.dataset.page;
    if (page === "prev") {
      pagination.prev();
    } else if (page === "next") {
      pagination.next();
    } else {
      pagination.goToPage(parseInt(page));
    }
    
    onPageChange(pagination.currentItems, pagination.currentPage);
    renderPagination(container, pagination, onPageChange);
  });
}