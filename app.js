/* ============================================
   ICSE STUDY HUB - Shared Interactive Logic
   Modular + reusable across pages
   ============================================ */

(function () {
  // --- COLLAPSIBLE Q&A (for content pages) ---
  function initQaCards() {
    const qaCards = document.querySelectorAll('.qa-card');
    if (!qaCards.length) return;

    qaCards.forEach(card => {
      const header = card.querySelector('.qa-header');
      if (!header) return;
      header.addEventListener('click', () => {
        card.classList.toggle('open');
      });
    });

    // Global reveal button (if exists)
    const revealAllBtn = document.getElementById('reveal-all-btn');
    if (revealAllBtn) {
      let allRevealed = false;
      revealAllBtn.addEventListener('click', () => {
        allRevealed = !allRevealed;
        qaCards.forEach(card => {
          if (allRevealed) card.classList.add('open');
          else card.classList.remove('open');
        });

        // Also toggle quote containers
        document.querySelectorAll('.quote-analysis-container').forEach(c => {
          if (allRevealed) c.classList.add('open');
          else c.classList.remove('open');
        });

        // Update icon
        if (allRevealed) {
          revealAllBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
            <span class="tooltip">Hide Answers</span>`;
          revealAllBtn.style.color = 'var(--color-primary)';
        } else {
          revealAllBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            <span class="tooltip">Reveal Answers</span>`;
          revealAllBtn.style.color = '';
        }
      });
    }
  }

  // --- QUOTE ANALYSIS TOGGLES ---
  function initQuoteToggles() {
    const toggles = document.querySelectorAll('.quote-analysis-toggle');
    toggles.forEach(toggle => {
      toggle.addEventListener('click', () => {
        const container = toggle.nextElementSibling;
        if (!container) return;
        container.classList.toggle('open');
        const isOpen = container.classList.contains('open');
        toggle.innerHTML = isOpen
          ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="18 15 12 9 6 15"/></svg> Hide Significance`
          : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg> Show Significance`;
      });
    });
  }

  // --- THEME TOGGLE (persisted) ---
  function initThemeToggle() {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;

    const saved = localStorage.getItem('icse-theme');
    const isLight = saved === 'light';
    if (isLight) {
      document.body.classList.add('light-theme');
      updateThemeIcon(toggle, true);
    }

    toggle.addEventListener('click', () => {
      const nowLight = document.body.classList.toggle('light-theme');
      localStorage.setItem('icse-theme', nowLight ? 'light' : 'dark');
      updateThemeIcon(toggle, nowLight);
    });

    function updateThemeIcon(btn, light) {
      btn.innerHTML = light
        ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg><span class="tooltip">Toggle Theme</span>`
        : `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><span class="tooltip">Toggle Theme</span>`;
    }
  }

  // --- REVISION CHECKLIST + PROGRESS (localStorage) ---
  function initRevisionTracker() {
    const checkboxes = document.querySelectorAll('.checklist-checkbox');
    const fill = document.getElementById('progress-fill');
    const pct = document.getElementById('progress-percent');
    if (!checkboxes.length || !fill || !pct) return;

    checkboxes.forEach(cb => {
      const saved = localStorage.getItem(cb.id);
      if (saved === 'true') cb.checked = true;

      cb.addEventListener('change', () => {
        localStorage.setItem(cb.id, cb.checked);
        update();
      });
    });

    function update() {
      const total = checkboxes.length;
      const done = Array.from(checkboxes).filter(c => c.checked).length;
      const perc = Math.round((done / total) * 100);
      fill.style.width = perc + '%';
      pct.textContent = perc + '%';
    }
    update();
  }

  // --- REAL-TIME SEARCH (content pages) ---
  function initSearch() {
    const input = document.getElementById('search-input');
    if (!input) return;

    const cards = document.querySelectorAll('.searchable-card');
    const main = document.querySelector('main');
    if (!cards.length || !main) return;

    let noResults = main.querySelector('.no-results');
    if (!noResults) {
      noResults = document.createElement('div');
      noResults.className = 'no-results';
      noResults.style.display = 'none';
      noResults.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <p>No matches found. Try "bond", "Shylock", "revenge", or a character name.</p>`;
      main.appendChild(noResults);
    }

    function removeHighlights(el) {
      el.querySelectorAll('mark.search-match').forEach(m => {
        const p = m.parentNode;
        p.replaceChild(document.createTextNode(m.textContent), m);
        p.normalize();
      });
    }

    function highlight(el, q) {
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
      const nodes = [];
      let n;
      while ((n = walker.nextNode())) {
        const tag = n.parentElement.tagName;
        if ((['SCRIPT', 'STYLE', 'BUTTON', 'SVG'].includes(tag) || n.parentElement.closest('button')) && !n.parentElement.classList.contains('qa-question')) continue;
        if (n.nodeValue.toLowerCase().includes(q)) nodes.push(n);
      }
      nodes.forEach(node => {
        const txt = node.nodeValue;
        const frag = document.createDocumentFragment();
        let cur = txt;
        while (true) {
          const i = cur.toLowerCase().indexOf(q);
          if (i < 0) { frag.appendChild(document.createTextNode(cur)); break; }
          frag.appendChild(document.createTextNode(cur.slice(0, i)));
          const mark = document.createElement('mark');
          mark.className = 'search-match';
          mark.textContent = cur.slice(i, i + q.length);
          frag.appendChild(mark);
          cur = cur.slice(i + q.length);
        }
        node.parentNode.replaceChild(frag, node);
      });
    }

    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      let visible = 0;

      cards.forEach(card => {
        removeHighlights(card);
        if (!q) {
          card.style.display = '';
          visible++;
          return;
        }
        const txt = card.textContent.toLowerCase();
        if (txt.includes(q)) {
          card.style.display = '';
          visible++;
          highlight(card, q);
          if (card.classList.contains('qa-card')) card.classList.add('open');
        } else {
          card.style.display = 'none';
        }
      });

      noResults.style.display = (visible === 0 && q) ? 'block' : 'none';
    });

    // '/' shortcut
    document.addEventListener('keydown', e => {
      if (e.key === '/' && document.activeElement !== input) {
        e.preventDefault();
        input.focus();
      }
    });
  }

  // --- MOBILE DRAWER NAV ---
  function initMobileNav() {
    const toggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    if (!toggle || !sidebar) return;

    // Create backdrop if not present
    let backdrop = document.querySelector('.sidebar-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'sidebar-backdrop';
      document.body.appendChild(backdrop);
    }

    function open() {
      sidebar.classList.add('open');
      backdrop.classList.add('visible');
      document.body.style.overflow = 'hidden';
    }
    function close() {
      sidebar.classList.remove('open');
      backdrop.classList.remove('visible');
      document.body.style.overflow = '';
    }

    toggle.addEventListener('click', e => {
      e.stopPropagation();
      if (sidebar.classList.contains('open')) close();
      else open();
    });

    backdrop.addEventListener('click', close);

    // Close on nav link tap (mobile)
    sidebar.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        if (window.innerWidth <= 860) close();
      });
    });

    // Close on outside click (safety)
    document.addEventListener('click', e => {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== toggle) {
        close();
      }
    });
  }

  // --- SCROLLSPY (only if sidebar nav exists) ---
  function initScrollSpy() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('main section[id]');
    if (!navItems.length || !sections.length) return;

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const id = entry.target.getAttribute('id');
        navItems.forEach(item => {
          item.classList.remove('active');
          const link = item.querySelector('a');
          if (link && link.getAttribute('href') === `#${id}`) {
            item.classList.add('active');
          }
        });
      });
    }, { root: null, rootMargin: '0px 0px -42% 0px', threshold: 0 });

    sections.forEach(sec => observer.observe(sec));
  }

  // --- PRINT BUTTON (if present) ---
  function initPrint() {
    const btn = document.getElementById('print-btn');
    if (btn) {
      btn.addEventListener('click', () => window.print());
    }
  }

  // --- COLLAPSIBLE LINE-BY-LINE SECTIONS ---
  function initSectionToggles() {
    const toggles = document.querySelectorAll('.section-toggle');
    if (!toggles.length) return;

    toggles.forEach(btn => {
      btn.addEventListener('click', () => {
        const body = document.getElementById(btn.getAttribute('aria-controls'));
        if (!body) return;
        const open = body.classList.toggle('open');
        btn.setAttribute('aria-expanded', open);
        btn.classList.toggle('collapsed', !open);
      });
    });

    const expandBtn = document.getElementById('expand-sections-btn');
    if (expandBtn) {
      let expanded = true;
      expandBtn.addEventListener('click', () => {
        expanded = !expanded;
        document.querySelectorAll('.section-body').forEach(b => b.classList.toggle('open', expanded));
        document.querySelectorAll('.section-toggle').forEach(b => {
          b.setAttribute('aria-expanded', expanded);
          b.classList.toggle('collapsed', !expanded);
        });
        const tip = expandBtn.querySelector('.tooltip');
        if (tip) tip.textContent = expanded ? 'Collapse All' : 'Expand All';
      });
    }
  }

  // Public init for full content pages
  window.initStudyPage = function () {
    initQaCards();
    initQuoteToggles();
    initThemeToggle();
    initRevisionTracker();
    initSearch();
    initMobileNav();
    initScrollSpy();
    initPrint();
    initSectionToggles();
  };

  // Minimal init for hub pages (theme + mobile header if any)
  window.initHubPage = function () {
    initThemeToggle();
    // Future: any global search across pages could go here
  };

  // Auto-run sensible defaults on DOM ready
  document.addEventListener('DOMContentLoaded', () => {
    // Rich study pages: Q&A, line-by-line, or searchable content
    if (document.querySelector('.qa-card') || document.querySelector('.line-pair') || document.getElementById('search-input')) {
      window.initStudyPage();
    } else {
      window.initHubPage();
    }
  });
})();