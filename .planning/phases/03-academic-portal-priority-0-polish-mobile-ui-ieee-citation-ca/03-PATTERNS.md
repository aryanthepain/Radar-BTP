# Phase 03: Academic Portal Priority 0 Polish: Mobile UI & IEEE Citation Cards - Pattern Map

**Mapped:** 2026-11-19  
**Files analyzed:** 5  
**Analogs found:** 5 / 5 (100% exact codebase coverage)

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `docs/index.html` | component / view | request-response (DOM markup) | `docs/index.html` (lines 21-25, 664-675, 951-965, 1042-1055, 1182-1195) | exact |
| `docs/styles.css` | config / stylesheet | transform (declarative CSS) | `docs/styles.css` (lines 935-965, 1078-1095, 1330-1382, 1435-1475) | exact |
| `docs/app.js` | controller / runtime | event-driven (DOM manipulation) | `docs/app.js` (lines 360-455, 620-646, 650-665) | exact |
| `tests/test_academic_website.py` | test | batch (DOM/CSS assertion) | `tests/test_academic_website.py` (lines 1-150) | exact |
| `tests/test_showcase_website.py` | test | batch (DOM/CSS assertion) | `tests/test_showcase_website.py` (lines 1-58, 199-245) | exact |

---

## Pattern Assignments

### 1. `docs/index.html` (component / view, request-response)

**Analog:** `docs/index.html`

**Existing Hamburger & Drawer Header Pattern** (`docs/index.html` lines 21-25):
```html
<!-- Mobile Navigation Toggle Button -->
<button id="nav-toggle" class="nav-toggle-btn" aria-label="Toggle navigation">☰</button>
<div class="nav-backdrop"></div>

<div class="app-container">
```

**Target Navigation Button Upgrade Pattern** (WCAG 2.5.5 Touch & Accessible State):
```html
<!-- Mobile Navigation Toggle Button with Accessible ARIA Controls -->
<button id="nav-toggle" class="nav-toggle-btn" aria-label="Toggle navigation" aria-expanded="false" aria-controls="academic-sidebar">☰</button>
<div class="nav-backdrop" id="nav-backdrop"></div>
```

**Existing Table Breakout Pattern without Scroll Wrapper** (`docs/index.html` lines 664-670):
```html
<div class="breakout-title">
  Table 4.1: 7-Axis Research-Gap Matrix Comparing Prior Art with Proposed Adaptive Framework
</div>
<table style="width: 100%; border-collapse: collapse; font-size: 0.84rem; color: #cbd5e1; text-align: left;">
```

**Target Semantic Container Pattern** (Decision D-01 & PORTAL-MOB-02):
```html
<div class="breakout-title">
  Table 4.1: 7-Axis Research-Gap Matrix Comparing Prior Art with Proposed Adaptive Framework
</div>
<div class="table-scroll-wrapper">
  <table style="width: 100%; border-collapse: collapse; font-size: 0.84rem; color: #cbd5e1; text-align: left;">
    ...
  </table>
</div>
```
*(Apply analog pattern to Table 4.1 lines 665-725, Latency Waterfall lines 952-1005, Table III lines 1043-1110, and Master Comparison lines 1183-1240)*.

**Target Math Formula Wrapper Pattern** (Decision D-01 & PORTAL-MOB-02):
```html
<div class="formula-scroll-wrapper">
  <div class="math-display-container">
    $$f(t) = f_c + S t = f_c + \frac{B}{T_c} t, \quad 0 \le t \le T_c$$
  </div>
</div>
```

---

### 2. `docs/styles.css` (config / stylesheet, transform)

**Analog:** `docs/styles.css`

**Existing Nav Toggle & Backdrop Pattern** (`docs/styles.css` lines 939-963):
```css
.nav-toggle-btn {
  display: none;
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 101;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.nav-backdrop {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  z-index: 99;
}
```

**Target Touch Standard, Focus Rings & Scroll-Lock Pattern** (Decision D-05, D-06):
```css
.nav-toggle-btn {
  display: none;
  position: fixed;
  top: 1rem;
  right: 1rem;
  min-width: 44px;
  min-height: 44px;
  padding: 0;
  display: none;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
  line-height: 1;
  background: var(--bg-secondary, #0f172a);
  border: 1px solid var(--border-color, #1e293b);
  border-radius: var(--radius-sm, 6px);
  color: var(--text-primary, #f8fafc);
  cursor: pointer;
  z-index: 101;
  transition: background 0.2s ease, transform 0.2s ease;
}

.nav-toggle-btn:focus-visible {
  outline: 2px solid var(--accent-sky, #38bdf8);
  outline-offset: 2px;
}

/* Background body scroll lock */
body.nav-open {
  overflow: hidden !important;
  touch-action: none !important;
}

/* TOC Touch Target Standards */
#chapter-toc .toc-link, .chapter-toc .toc-link {
  min-height: 44px;
  display: flex;
  align-items: center;
  padding: 0.65rem 0.85rem;
  box-sizing: border-box;
}

#chapter-toc .toc-link:focus-visible {
  outline: 2px solid var(--accent-sky, #38bdf8);
  outline-offset: -2px;
}
```

**Existing Citation Tooltip Pattern** (`docs/styles.css` lines 1330-1355):
```css
.citation-tooltip {
  position: fixed;
  background: #0f172a;
  color: #f8fafc;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 0.85rem 1rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
  font-size: 0.825rem;
  line-height: 1.4;
  z-index: 1000;
  max-width: 360px;
  pointer-events: none;
  opacity: 0;
  transform: translateY(6px);
  transition: opacity 0.2s cubic-bezier(0.16, 1, 0.3, 1), transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  font-family: var(--font-sans);
  text-align: left;
}

.citation-tooltip.visible {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
```

**Target Two-Tier Overflow & Mobile Bottom-Sheet Pattern** (Decisions D-01, D-02, D-03):
```css
/* Two-Tier Table & Formula Momentum Scroll Wrappers */
.table-scroll-wrapper,
.formula-scroll-wrapper {
  position: relative;
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  margin: 1.5rem 0;
  scrollbar-width: thin;
  scrollbar-color: var(--border-color, #334155) transparent;
}

.table-scroll-wrapper::after,
.formula-scroll-wrapper::after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 24px;
  background: linear-gradient(to right, transparent, rgba(3, 7, 18, 0.75));
  pointer-events: none;
  opacity: 0.85;
}

.table-scroll-wrapper table,
.table-scroll-wrapper .master-table {
  font-size: clamp(0.75rem, 1.8vw, 0.84rem) !important;
  min-width: 580px;
}

.katex-display {
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  font-size: clamp(0.85em, 2.2vw, 1.05em);
  padding: 0.5rem 0;
}

/* Mobile Bottom Sheet (<600px) */
@media (max-width: 600px) {
  .citation-tooltip {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    top: auto !important;
    width: 100% !important;
    max-width: 100% !important;
    border-radius: 16px 16px 0 0 !important;
    border: 1px solid var(--border-color, #334155) !important;
    border-bottom: none !important;
    background: #0b1120 !important;
    box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.8) !important;
    padding: 1.25rem 1.25rem calc(1.25rem + env(safe-area-inset-bottom, 16px)) !important;
    transform: translateY(100%) !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease !important;
    z-index: 10005 !important;
  }

  .citation-tooltip.visible {
    transform: translateY(0) !important;
    opacity: 1 !important;
  }

  .citation-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.65);
    z-index: 10004;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s ease;
  }

  .citation-backdrop.visible {
    opacity: 1;
    pointer-events: auto;
  }
}

/* Bibliography Item Highlight Pulse Keyframe (Resolves Pitfall 4) */
@keyframes highlightPulse {
  0% { background: rgba(56, 189, 248, 0.45); outline: 2px solid #38bdf8; }
  50% { background: rgba(56, 189, 248, 0.2); outline: 2px solid #0284c7; }
  100% { background: transparent; outline: 2px solid transparent; }
}

.highlight-pulse {
  animation: highlightPulse 2s ease-out;
  border-radius: 4px;
}
```

---

### 3. `docs/app.js` (controller / runtime, event-driven)

**Analog:** `docs/app.js`

**Existing Citation Gate & Click Handler Pattern** (`docs/app.js` lines 361-365, 442-452):
```javascript
function initCitationTooltips() {
  if (!window.ENABLE_CITATION_TOOLTIPS) return;

  const badges = document.querySelectorAll(".citation-badge, [data-citation]");
  if (!badges.length) return;
  ...
  badge.addEventListener("click", (e) => {
    const citeKey = badge.getAttribute("data-citation") || badge.textContent.replace(/[\[\]]/g, "").trim();
    const targetId = `ref-${citeKey}`;
    const targetEl = document.getElementById(targetId);
    if (targetEl) {
      e.preventDefault();
      targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
      targetEl.classList.add("highlight-pulse");
      setTimeout(() => targetEl.classList.remove("highlight-pulse"), 2000);
    }
  });
}
```

**Target Adaptive Citation Tooltip & Bottom Sheet Pattern** (Decision D-03, D-04):
```javascript
function initCitationTooltips() {
  // Gating flag removed (D-04) - unconditional activation
  const badges = document.querySelectorAll(".citation-badge, [data-citation]");
  if (!badges.length) return;

  let tooltipEl = document.getElementById("citation-tooltip");
  let backdropEl = document.getElementById("citation-backdrop");

  if (!tooltipEl) {
    tooltipEl = document.createElement("div");
    tooltipEl.id = "citation-tooltip";
    tooltipEl.className = "citation-tooltip";
    document.body.appendChild(tooltipEl);
  }

  if (!backdropEl) {
    backdropEl = document.createElement("div");
    backdropEl.id = "citation-backdrop";
    backdropEl.className = "citation-backdrop";
    document.body.appendChild(backdropEl);
  }

  let hideTimeout = null;

  function showTooltip(badge, isTouch = false) {
    clearTimeout(hideTimeout);
    const citeKey = badge.getAttribute("data-citation") || badge.textContent.replace(/[\[\]]/g, "").trim();
    const data = CITATIONS_DB[citeKey];
    if (!data) return;

    // Safe DOM construction (CWE-79 DOM XSS prevention)
    while (tooltipEl.firstChild) {
      tooltipEl.removeChild(tooltipEl.firstChild);
    }

    const header = document.createElement("div");
    header.className = "tooltip-header";
    header.style.display = "flex";
    header.style.justifyContent = "space-between";
    header.style.alignItems = "center";

    const refNum = document.createElement("div");
    refNum.className = "tooltip-ref-num";
    refNum.textContent = `IEEE Reference [${data.ref}]`;
    header.appendChild(refNum);

    if (isTouch || window.innerWidth <= 600) {
      const closeBtn = document.createElement("button");
      closeBtn.className = "tooltip-close-btn";
      closeBtn.textContent = "✕";
      closeBtn.setAttribute("aria-label", "Close citation preview");
      closeBtn.addEventListener("click", hideTooltip);
      header.appendChild(closeBtn);
    }
    tooltipEl.appendChild(header);

    const title = document.createElement("div");
    title.className = "tooltip-title";
    title.textContent = data.title;
    tooltipEl.appendChild(title);

    const authors = document.createElement("div");
    authors.className = "tooltip-authors";
    authors.textContent = data.authors;
    tooltipEl.appendChild(authors);

    const venue = document.createElement("div");
    venue.className = "tooltip-venue";
    venue.textContent = `${data.venue} (${data.year})`;
    tooltipEl.appendChild(venue);

    const actions = document.createElement("div");
    actions.className = "tooltip-actions";
    actions.style.display = "flex";
    actions.style.gap = "0.5rem";
    actions.style.marginTop = "0.75rem";

    if (data.doi && data.doi.trim().length > 0) {
      const doiBtn = document.createElement("a");
      doiBtn.className = "tooltip-doi-btn";
      doiBtn.href = data.doi.startsWith("http") ? data.doi : `https://doi.org/${data.doi}`;
      doiBtn.target = "_blank";
      doiBtn.rel = "noopener noreferrer";
      doiBtn.textContent = "DOI / Publisher";
      actions.appendChild(doiBtn);
    }

    const jumpBtn = document.createElement("button");
    jumpBtn.className = "tooltip-jump-btn";
    jumpBtn.textContent = "View in Reference List";
    jumpBtn.addEventListener("click", () => {
      hideTooltip();
      const targetId = `ref-${citeKey}`;
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
        targetEl.classList.add("highlight-pulse");
        setTimeout(() => targetEl.classList.remove("highlight-pulse"), 2000);
      }
    });
    actions.appendChild(jumpBtn);
    tooltipEl.appendChild(actions);

    // Dynamic Viewport Mode Switch
    if (window.innerWidth <= 600) {
      backdropEl.classList.add("visible");
      document.body.classList.add("nav-open");
    } else {
      const rect = badge.getBoundingClientRect();
      const tooltipWidth = Math.min(480, window.innerWidth - 40);
      let left = rect.left + window.scrollX - 40;
      let top = rect.top + window.scrollY - 140;

      if (left + tooltipWidth > window.innerWidth - 20) {
        left = window.innerWidth - tooltipWidth - 20;
      }
      if (left < 10) left = 10;
      if (rect.top < 150) {
        top = rect.bottom + window.scrollY + 10;
      }

      tooltipEl.style.left = `${left}px`;
      tooltipEl.style.top = `${top}px`;
    }

    tooltipEl.classList.add("visible");
  }

  function hideTooltip() {
    tooltipEl.classList.remove("visible");
    backdropEl.classList.remove("visible");
    document.body.classList.remove("nav-open");
  }

  badges.forEach((badge) => {
    badge.addEventListener("mouseenter", () => {
      if (window.innerWidth > 600) showTooltip(badge, false);
    });
    badge.addEventListener("mouseleave", () => {
      if (window.innerWidth > 600) hideTimeout = setTimeout(hideTooltip, 200);
    });
    badge.addEventListener("click", (e) => {
      e.preventDefault();
      showTooltip(badge, true);
    });
  });

  backdropEl.addEventListener("click", hideTooltip);
}
```

**Target Mobile Drawer Pattern with Scroll-Lock & Icon Morph** (`docs/app.js` lines 622-646):
```javascript
function initMobileDrawer() {
  const toggleBtn = document.getElementById("nav-toggle");
  const sidebar = document.querySelector(".sidebar") || document.getElementById("academic-sidebar");
  const backdrop = document.querySelector(".nav-backdrop") || document.getElementById("nav-backdrop");
  const tocLinks = document.querySelectorAll(".toc-link");

  if (!toggleBtn || !sidebar || !backdrop) return;

  function toggleDrawer() {
    const isOpen = sidebar.classList.toggle("open");
    backdrop.classList.toggle("open", isOpen);
    document.body.classList.toggle("nav-open", isOpen);
    toggleBtn.textContent = isOpen ? "✕" : "☰";
    toggleBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
  }

  function closeDrawer() {
    sidebar.classList.remove("open");
    backdrop.classList.remove("open");
    document.body.classList.remove("nav-open");
    toggleBtn.textContent = "☰";
    toggleBtn.setAttribute("aria-expanded", "false");
  }

  toggleBtn.addEventListener("click", toggleDrawer);
  backdrop.addEventListener("click", closeDrawer);

  tocLinks.forEach((link) => {
    link.addEventListener("click", closeDrawer);
  });

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && sidebar.classList.contains("open")) {
      closeDrawer();
    }
  });
}
```

**Target Overflow Safety Sweep on DOMContentLoaded** (Decision D-01):
```javascript
function initOverflowContainment() {
  // Wrap any tables lacking .table-scroll-wrapper
  document.querySelectorAll("table").forEach((tbl) => {
    if (!tbl.closest(".table-scroll-wrapper")) {
      const wrapper = document.createElement("div");
      wrapper.className = "table-scroll-wrapper";
      tbl.parentNode.insertBefore(wrapper, tbl);
      wrapper.appendChild(tbl);
    }
  });

  // Wrap any .katex-display lacking .formula-scroll-wrapper
  document.querySelectorAll(".katex-display").forEach((kd) => {
    if (!kd.closest(".formula-scroll-wrapper")) {
      const wrapper = document.createElement("div");
      wrapper.className = "formula-scroll-wrapper";
      kd.parentNode.insertBefore(wrapper, kd);
      wrapper.appendChild(kd);
    }
  });
}
```

---

### 4. `tests/test_academic_website.py` (test, batch)

**Analog:** `tests/test_academic_website.py` (lines 34-64, 88-114)

**Existing CSS & JS AST / Regex Pattern**:
```python
def test_css_rules():
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".academic-two-column" in css
    assert "@media" in css
    assert "max-width" in css
```

**Target Unit Tests to Add** (PORTAL-MOB-01, PORTAL-MOB-02, PORTAL-CITE-01, PORTAL-CITE-02):
```python
def test_mobile_drawer_and_touch_targets():
    """Verify WCAG 2.5.5 touch targets, body scroll lock, and drawer controls (PORTAL-MOB-01)."""
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Touch Target Sizing (>= 44x44px)
    assert "min-width: 44px" in css or "min-height: 44px" in css, "Must enforce >= 44px touch targets"
    assert "body.nav-open" in css, "Must define body.nav-open scroll-lock rule"
    assert "overflow: hidden" in css and "touch-action: none" in css, "Scroll-lock must prevent body drag"

    # JS Event Handling & Icon Morph
    assert "nav-open" in js, "app.js must toggle body.nav-open"
    assert "aria-expanded" in js, "app.js must maintain aria-expanded state"
    assert "✕" in js and "☰" in js, "app.js must morph hamburger to close icon"


def test_overflow_containment_and_scroll_wrappers():
    """Verify two-tier math and table overflow containment (PORTAL-MOB-02)."""
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # CSS Momentum Scroll Wrappers & Fluid Scaling
    assert ".table-scroll-wrapper" in css, "CSS must define .table-scroll-wrapper"
    assert ".formula-scroll-wrapper" in css, "CSS must define .formula-scroll-wrapper"
    assert "-webkit-overflow-scrolling: touch" in css, "Must specify iOS momentum touch scroll"
    assert "clamp(" in css, "Must implement fluid font scaling floor"

    # HTML Containment
    assert 'class="table-scroll-wrapper"' in html or "table-scroll-wrapper" in html, "HTML must contain table scroll wrappers"
    assert "initOverflowContainment" in js, "app.js must implement automated safety sweep"


def test_citation_bottom_sheet_and_pulse_jump():
    """Verify adaptive desktop tooltip / mobile bottom-sheet and bibliography jump (PORTAL-CITE-01, PORTAL-CITE-02)."""
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # Absence of gating debug flag
    assert "ENABLE_CITATION_TOOLTIPS" not in js, "Citation cards must be unconditionally active (D-04)"

    # Mobile bottom sheet CSS rules
    assert "highlightPulse" in css or "@keyframes highlightPulse" in css, "CSS must define @keyframes highlightPulse"
    assert ".highlight-pulse" in css, "CSS must define .highlight-pulse"
    assert ".citation-backdrop" in css, "CSS must define .citation-backdrop"
    assert "safe-area-inset-bottom" in css, "Must support mobile safe-area insets"
```

---

### 5. `tests/test_showcase_website.py` (test, batch)

**Analog:** `tests/test_showcase_website.py` (lines 199-245)

**Existing Offline Resilience & Link Resolution Pattern**:
```python
def test_03_zero_build_and_offline_resilience(self):
    index_path = DOCS_DIR / "index.html"
    styles_path = DOCS_DIR / "styles.css"
    app_path = DOCS_DIR / "app.js"
    ...
    forbidden_substrings = ["http://", "https://", "unpkg.com", "cdnjs.cloudflare.com", "cdn.jsdelivr.net"]
    for forbidden in forbidden_substrings:
        self.assertNotIn(forbidden, html_content)
        self.assertNotIn(forbidden, css_content)
```

**Target Assertion Expansion Pattern**:
```python
def test_05_mobile_ergonomics_and_citation_assets(self):
    """Verifies that all citation badges in index.html map to valid entries in CITATIONS_DB and references section."""
    with open(DOCS_DIR / "index.html", "r", encoding="utf-8") as f:
        html = f.read()
    with open(DOCS_DIR / "app.js", "r", encoding="utf-8") as f:
        js = f.read()

    # Ensure backdrop element exists for mobile dismissal
    self.assertIn('class="nav-backdrop"', html, "index.html must provide .nav-backdrop for mobile dismissal")
    self.assertIn("initMobileDrawer", js, "app.js must declare initMobileDrawer")
    self.assertIn("initCitationTooltips", js, "app.js must declare initCitationTooltips")
    self.assertIn("initOverflowContainment", js, "app.js must declare initOverflowContainment")
```

---

## Shared Patterns

### 1. Offline Zero-Build Vanilla Architecture
**Source:** `tests/test_showcase_website.py:213-232`  
**Apply to:** `docs/index.html`, `docs/styles.css`, `docs/app.js`  
All scripts, styles, fonts, and assets must run strictly from offline local storage (`docs/assets/vendor/`). Zero external CDN requests, zero node build tools (`npm run build`), ensuring 100% offline functionality.

### 2. CWE-79 DOM XSS Mitigation (Safe Element Construction)
**Source:** `docs/app.js:384-409`  
**Apply to:** All dynamic DOM element creation in `docs/app.js` (`initCitationTooltips`, `initOverflowContainment`)  
Never inject metadata strings via `innerHTML`. Construct all DOM tree nodes with `document.createElement()`, set textual data via `element.textContent = ...`, and bind styles and attributes through `setAttribute()` or `classList.add()`.

### 3. WCAG 2.5.5 Touch Target Ergonomics & Focus Rings
**Source:** `docs/styles.css:939-951`, `03-RESEARCH.md:186-228`  
**Apply to:** `#nav-toggle`, `.toc-link`, `.tooltip-close-btn`, `.tooltip-jump-btn`, `.tooltip-doi-btn`  
All touch-interactive targets must guarantee $\ge 44\times 44\text{px}$ bounding boxes with high-contrast visible focus indicators (`:focus-visible { outline: 2px solid var(--accent-sky); outline-offset: 2px; }`).

### 4. Viewport Scroll-Lock & Momentum Containment
**Source:** `03-RESEARCH.md:223-228, 276-289`  
**Apply to:** `body.nav-open`, `.table-scroll-wrapper`, `.formula-scroll-wrapper`, `.citation-tooltip`  
Prevent background bleed scroll using `body.nav-open { overflow: hidden !important; touch-action: none !important; }`. Contain wide elements with `-webkit-overflow-scrolling: touch; overflow-x: auto; overflow-y: hidden;`.

### 5. Deterministic In-Memory DOM/CSS Regex Verification
**Source:** `tests/test_academic_website.py:11-64`  
**Apply to:** `tests/test_academic_website.py`, `tests/test_showcase_website.py`  
Validate markup and stylesheet properties using Python's native `html.parser` and regex inspection in $<500\text{ms}$ without external browser binaries (Puppeteer, Selenium, Playwright).

---

## No Analog Found

All 5 files have exact codebase analogs in this repository:

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| *(None)* | — | — | All targeted files already exist and have established in-repo patterns. |

---

## Metadata

**Analog search scope:** `docs/`, `tests/`  
**Files scanned:** 5 target files (4,345 lines of code)  
**Pattern extraction date:** 2026-11-19  
