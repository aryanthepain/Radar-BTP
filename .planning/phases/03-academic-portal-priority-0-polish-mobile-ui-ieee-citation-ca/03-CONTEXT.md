# Phase 03: Academic Portal Priority 0 Polish: Mobile UI & IEEE Citation Cards - Context

**Gathered:** 2026-11-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Delivering publication-grade responsive ergonomics, touch navigation targets, equation/table overflow containment, and interactive floating IEEE citation previews for the BTP academic thesis reading portal in `docs/` (`docs/index.html`, `docs/styles.css`, `docs/app.js`), fulfilling GitHub Priority 0 issues [#23](https://github.com/aryanthepain/Radar-BTP/issues/23) and [#21](https://github.com/aryanthepain/Radar-BTP/issues/21).

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**6 requirements are locked.** See `03-SPEC.md` for full requirements, boundaries, and acceptance criteria.

Downstream agents MUST read `03-SPEC.md` before planning or implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Responsive layout refactoring in `docs/styles.css` for viewports 360px–1024px.
- Mobile drawer navigation ergonomics and touch target upgrades in `docs/index.html` and `docs/styles.css`.
- Mathematical and tabular overflow containment with fluid font floor and momentum scroll wrappers.
- Activation, styling, and touch tap-to-inspect logic for floating IEEE citation cards in `docs/app.js` and `docs/styles.css`.
- Test suite expansion in `tests/test_showcase_website.py` and `tests/test_academic_website.py`.

**Out of scope (from SPEC.md):**
- Backend radar signal processing, simulation, or PyTorch models (`src/sim/*`, `src/dsp/*`, `src/models/*`).
- LaTeX thesis report modifications (`report/main.tex`).
- External frontend framework additions (React, Vue, Tailwind, Bootstrap, NPM build toolchains) — must preserve zero-build offline vanilla architecture.
- Alterations to the 30 peer-reviewed paper citations in `CITATIONS_DB`.

</spec_lock>

<decisions>
## Implementation Decisions

### Math & Table Overflow Strategy (Issue #23)
- **D-01 (Hybrid Scroll Wrappers):** Author semantic HTML containers (`.table-scroll-wrapper`, `.formula-scroll-wrapper`) in `docs/index.html` around all wide benchmark comparison tables and breakout equations, AND implement an automated client-side safety sweep in `docs/app.js` on `DOMContentLoaded` that wraps any uncontained `.katex-display` or `table` elements. — **Reversibility:** reversible
- **D-02 (Two-Tier Responsive Font & Scroll Scaling):** Apply fluid font scaling down to an accessible floor (0.75rem / 11px for tables, 0.85em for KaTeX math); below this threshold, horizontal momentum scroll containers (`overflow-x: auto; -webkit-overflow-scrolling: touch;`) activate with subtle edge-fade indicators, strictly guaranteeing zero horizontal body overflow (`document.documentElement.scrollWidth <= window.innerWidth`). — **Reversibility:** reversible

### Citation Popover Positioning & Layout (Issue #21)
- **D-03 (Adaptive Desktop Tooltip & Mobile Bottom-Sheet):**
  - **Desktop (>600px):** Render citation preview as an elevated floating card dynamically positioned relative to the badge coordinate with edge collision detection and safe margin clamping (`max-width: 480px`).
  - **Mobile (<600px):** Display citation preview as a slide-up bottom-sheet card (`position: fixed; bottom: 0; left: 0; right: 0; border-radius: 16px 16px 0 0;`) with darkened backdrop, paper title, authors, venue, year, direct DOI pill button, and a prominent "View in Reference List" button that smooth-scrolls to the Section 9 anchor with pulse highlight. — **Reversibility:** reversible
- **D-04 (Global Default Activation):** Remove the gating flag `if (!window.ENABLE_CITATION_TOOLTIPS) return;` in `docs/app.js`. Citation cards are active unconditionally by default for all readers. — **Reversibility:** reversible

### Mobile Drawer Navigation Ergonomics (Issue #23)
- **D-05 (Touch Target Standard & Focus Rings):** Guarantee all mobile interactive controls (`#nav-toggle`, TOC anchor links, modal close buttons) satisfy $\ge 44\times 44\text{px}$ touch bounding boxes with visible high-contrast focus rings (`outline: 2px solid var(--accent-sky)`). — **Reversibility:** reversible
- **D-06 (Body Scroll-Lock & Icon Morphing):**
  - When the mobile sidebar drawer opens, toggle `.nav-open` on `document.body` applying `overflow: hidden; touch-action: none;` to prevent background content scrolling behind the drawer backdrop.
  - Animate the hamburger button icon (`#nav-toggle`) into an animated "✕" close icon on open.
  - Automatically close the drawer and release scroll-lock when any TOC link or backdrop is tapped. — **Reversibility:** reversible

### Deterministic Test Architecture (PORTAL-VERIF-01)
- **D-07 (Static AST & DOM Parser Verification):** Implement deterministic test suites in `tests/test_academic_website.py` and `tests/test_showcase_website.py` utilizing Python's native `html.parser` and CSS regex tokens to assert touch target rules, media query coverage (`1024px`, `900px`, `600px`), scroll wrapper classes, and citation DOM integrity in $<5\text{s}$ without external browser binaries. — **Reversibility:** reversible

### the agent's Discretion
- Exact CSS transition easing curves (`cubic-bezier(0.16, 1, 0.3, 1)`) and subtle elevation shadows for bottom-sheet and tooltip containers.
- Styling of edge-fade scroll cues (linear-gradient masks on scroll wrapper pseudo-elements).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase 3 Specifications & Tracked Issues
- `.planning/phases/03-academic-portal-priority-0-polish-mobile-ui-ieee-citation-ca/03-SPEC.md` — Complete locked specification with falsifiable requirements, edge probes, and prohibitions.
- `.planning/REQUIREMENTS.md` § PORTAL-P0 — Phase requirements `PORTAL-MOB-01`, `PORTAL-CITE-01`, `PORTAL-VERIF-01`.
- `https://github.com/aryanthepain/Radar-BTP/issues/23` — Issue #23: Comprehensive Mobile-Friendly UI Overhaul & Responsive Ergonomics.
- `https://github.com/aryanthepain/Radar-BTP/issues/21` — Issue #21: Interactive Floating IEEE Citation Cards & Bibliography Previews.

### Academic Showcase Codebase Assets
- `docs/index.html` — Thesis publication portal structure, hamburger toggle, TOC drawer, KaTeX math blocks, and reference section.
- `docs/styles.css` — Portal stylesheet, two-column layout rules, responsive breakpoints, citation badge classes, and mobile drawer styles.
- `docs/app.js` — Client runtime logic, `CITATIONS_DB` (30 references), `initCitationTooltips()`, and `initMobileDrawer()`.
- `tests/test_academic_website.py` — Deterministic academic website test suite.
- `tests/test_showcase_website.py` — Deterministic showcase website smoke test suite.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `CITATIONS_DB` in `docs/app.js`: Complete 30-entry dictionary of peer-reviewed references matching Section 9.
- `.citation-badge` & `.citation-tooltip` CSS classes in `docs/styles.css`: Pre-existing styling foundations for citation badges and popovers.
- `#nav-toggle`, `.sidebar`, `.nav-backdrop`: Pre-existing drawer DOM elements in `docs/index.html`.

### Established Patterns
- Zero-build vanilla architecture: No npm/webpack build step; pure browser-native HTML, CSS, and JS.
- Dark Cyber-Radar theme: Primary background `#030712`, surfaces `#0b1120`/`#0f172a`, borders `#1e293b`/`#334155`, sky accents `#38bdf8`/`#0284c7`.
- Deterministic in-memory testing: Fast unit tests using Python's `html.parser` without headless browser overhead.

### Integration Points
- `docs/app.js` line 362: Remove `if (!window.ENABLE_CITATION_TOOLTIPS) return;` gate and enhance `initCitationTooltips()`.
- `docs/app.js` line 622: Enhance `initMobileDrawer()` with body scroll-lock and icon toggle classes.
- `docs/styles.css` lines 1078, 1451, 1464: Expand responsive media queries for 360px–1024px, bottom-sheet popovers, and table/formula scroll wrappers.

</code_context>

<specifics>
## Specific Ideas

- Mobile citation bottom-sheet: Provides a natural touch-friendly sheet rising from the bottom edge on smartphones with a clear "✕" close button, direct link to DOI/arXiv, and "View in Reference List" jump button.
- Two-tier overflow containment: Fluid font scaling down to 11px / 0.85em first; momentum scroll only when equations or wide tables exceed that minimum readable threshold.

</specifics>

<deferred>
## Deferred Ideas

- Full offline PWA service worker with service-worker caching (deferred to future portal polish phase).
- Dynamic reading progress bar enhancements (Issue #20: `feat(docs): Dynamic Reading Progress Bar & Scroll Tracking in Thesis Portal`).

</deferred>

---

*Phase: 03-academic-portal-priority-0-polish-mobile-ui-ieee-citation-ca*
*Context gathered: 2026-11-19*
