# Phase 3: Academic Portal Priority 0 Polish: Mobile UI & IEEE Citation Cards — Specification

**Created:** 2026-11-19
**Ambiguity score:** 0.09 (gate: ≤ 0.20)
**Requirements:** 6 locked

## Goal

Deliver publication-grade mobile responsiveness, touch ergonomics, KaTeX equation/table overflow containment, and interactive floating IEEE citation previews for the BTP academic thesis reading portal (`docs/index.html`, `docs/styles.css`, `docs/app.js`), resolving GitHub Priority 0 issues #23 and #21 with 100% deterministic test verification.

## Background

The academic reading portal (`docs/index.html`) currently delivers a desktop-optimized two-column publication layout with fixed sidebars, KaTeX equations, and radar plots. However, review on mobile viewports (360px–1024px) reveals critical ergonomics and interaction defects:
1. **Disabled IEEE Citation Tooltips (Issue #21)**: In `docs/app.js`, `initCitationTooltips()` is gated behind `if (!window.ENABLE_CITATION_TOOLTIPS) return;`, rendering citation badges static and non-interactive by default. Touch devices lack dedicated tap-to-inspect card behaviors, and tooltips risk clipping beyond viewport boundaries on narrow screens.
2. **Touch Target Deficiencies (Issue #23)**: The mobile hamburger toggle `#nav-toggle` and TOC navigation items lack guaranteed minimum $\ge 44\times 44\text{px}$ touch targets, posing usability friction under mobile accessibility guidelines.
3. **Math & Wide Table Overflow (Issue #23)**: Multi-term KaTeX equations and 7-column benchmark comparison tables lack bounded momentum scroll containers, risking horizontal page blowout across standard mobile widths (360px–480px).
4. **Typography & Figure Reflow (Issue #23)**: Two-column academic text reflow below 900px requires strict single-column collapse, header text wrap protection, and constrained SVG/PNG container scaling.

## Requirements

1. **PORTAL-MOB-01 (Navigation Drawer & Touch Targets)**:
   - Current: Mobile drawer toggle `#nav-toggle` has variable padding and lacks explicit $44\times 44\text{px}$ touch-target bounds.
   - Target: Provide $\ge 44\times 44\text{px}$ tap targets for `#nav-toggle`, close controls, and TOC links with accessible focus rings, smooth off-canvas transition (`left: -290px` to `0`), backdrop dismissal, and auto-close on TOC link click.
   - Acceptance: Deterministic DOM assertion verifying `#nav-toggle` bounding style, backdrop dismiss listener, and TOC click handlers.

2. **PORTAL-MOB-02 (Two-Tier Math & Table Overflow Strategy)**:
   - Current: Large KaTeX math blocks and breakout comparison tables risk horizontal body scroll or text truncation on <480px viewports.
   - Target: Implement a two-tier responsive strategy: (1) apply fluid font scaling down to an accessible floor (minimum 0.75rem / 11px for tables, 0.85em for KaTeX); (2) if content still exceeds viewport width below that floor, enclose in horizontal momentum scroll wrappers (`overflow-x: auto`, `-webkit-overflow-scrolling: touch`) with subtle edge-fade scroll cues.
   - Acceptance: Zero horizontal page overflow (`document.documentElement.scrollWidth <= window.innerWidth`) simulated across 360px, 390px, 412px, 768px, and 1024px viewports; scroll wrapper CSS rules verified in tests.

3. **PORTAL-MOB-03 (Single-Column Reflow & Responsive Media)**:
   - Current: Layout reflows at 900px, but heading sizes, metadata badges, and large SVGs can wrap awkwardly on narrow viewports.
   - Target: Ensure `.academic-two-column` strictly reflows to `column-count: 1 !important` below 900px; responsive typography scaling for `h1`–`h4` and metadata badges; all figures and SVG diagrams enforce `max-width: 100%` and `height: auto`.
   - Acceptance: CSS parser tests in `tests/test_showcase_website.py` and `tests/test_academic_website.py` verify media query coverage and media scaling invariants.

4. **PORTAL-CITE-01 (Always-Active Floating Citation Popover Cards)**:
   - Current: `initCitationTooltips()` is disabled by default via `if (!window.ENABLE_CITATION_TOOLTIPS) return;`.
   - Target: Remove the gating flag; activate interactive floating citation cards globally by default for all 30 IEEE references in `CITATIONS_DB`. Cards render paper title, full author list, publication venue, year, and direct DOI/arXiv hyperlink.
   - Acceptance: DOM tests verify `initCitationTooltips()` executes unconditionally without gate flags and renders complete citation metadata fields.

5. **PORTAL-CITE-02 (Mobile Touch Tap-to-Inspect & Viewport Collision Detection)**:
   - Current: Tooltip relies primarily on mouse hover; touch interaction either triggers immediate page jumping or erratic tooltip flickering.
   - Target: On touch/mobile devices, first tap on citation badge opens floating card popover; popover includes an explicit "View in Reference List" button/link that smooth-scrolls to Section 9 with highlight pulse; tapping outside dismisses popover; floating positioning dynamically clamps to viewport bounds (`max-width: 92vw`, safe margin offset) to prevent edge clipping.
   - Acceptance: Click/touch event handlers verified; collision clamping styles (`max-width: 92vw`, `left/right: 4vw`) validated in `tests/test_academic_website.py`.

6. **PORTAL-VERIF-01 (Deterministic Test Gates & Zero-Build Resilience)**:
   - Current: Existing tests cover basic CSS and file existence, but do not assert mobile touch targets, overflow containment rules, or citation tooltip DOM integrity.
   - Target: Extend `tests/test_showcase_website.py` and `tests/test_academic_website.py` with deterministic assertions covering mobile media queries, touch target sizes, citation popover DOM structure, and zero external CDN leaks; pass all tests under `pwsh -File ./scripts/verify.ps1`.
   - Acceptance: 100% test pass rate with $\ge 90\%$ code coverage under sub-30s local execution.

## Boundaries

**In scope:**
- Responsive layout refactoring in `docs/styles.css` for viewports 360px–1024px.
- Mobile drawer navigation ergonomics and touch target upgrades in `docs/index.html` and `docs/styles.css`.
- Mathematical and tabular overflow containment with fluid font floor and momentum scroll wrappers.
- Activation, styling, and touch tap-to-inspect logic for floating IEEE citation cards in `docs/app.js` and `docs/styles.css`.
- Test suite expansion in `tests/test_showcase_website.py` and `tests/test_academic_website.py`.

**Out of scope:**
- Backend radar signal processing, simulation, or PyTorch models (`src/sim/*`, `src/dsp/*`, `src/models/*`).
- LaTeX thesis report modifications (`report/main.tex`).
- External frontend framework additions (React, Vue, Tailwind, Bootstrap, NPM build toolchains) — must preserve zero-build offline vanilla architecture.
- Alterations to the 30 peer-reviewed paper citations in `CITATIONS_DB`.

## Constraints

- **Zero-Build Vanilla Architecture**: All improvements must use vanilla HTML5, CSS3, and standard client JavaScript. Zero Node/Webpack/Vite build steps.
- **Offline Resilience**: Must strictly function without active Internet connectivity; all vendor dependencies (KaTeX, Highlight.js) remain vendored locally in `docs/assets/vendor/`.
- **Accessibility Minimums**: All interactive tap targets must maintain $\ge 44\times 44\text{px}$ touch bounds; keyboard focus indicators (`:focus-visible`) must provide $\ge 3:1$ contrast ratio.
- **Deterministic Gates**: All test suites must execute deterministically in $<30\text{s}$ under `pwsh -File ./scripts/verify.ps1`.

## Acceptance Criteria

- [ ] Mobile navigation toggle `#nav-toggle` and primary interactive controls have touch targets $\ge 44\times 44\text{px}$.
- [ ] Mobile sidebar drawer transitions smoothly off-canvas and dismisses on backdrop tap or TOC link selection.
- [ ] Body viewport width never exceeds screen width (`document.documentElement.scrollWidth <= window.innerWidth`) on 360px, 390px, 412px, 768px, and 1024px viewports.
- [ ] Multi-term KaTeX formulas and comparison tables enforce fluid font scaling with a hard minimum floor (11px / 0.75rem for tables, 0.85em for math), enclosed in horizontal momentum scroll containers.
- [ ] `.academic-two-column` strictly collapses to single-column layout below 900px.
- [ ] All SVG diagrams, Mermaid diagrams, and PNG radar plots auto-scale with `max-width: 100%` and `height: auto`.
- [ ] Floating IEEE citation popover cards are active by default for all 30 references in Section 9 without requiring debug flag activation.
- [ ] Citation cards display reference number, paper title, authors, venue, year, and direct DOI/arXiv hyperlink.
- [ ] On touch devices, first tap opens the floating citation popover; popover includes a "View in Reference List" jump link; tap outside dismisses.
- [ ] Floating citation cards dynamically adjust position to prevent clipping off the left, right, or bottom viewport edges.
- [ ] Unit and DOM test suites (`tests/test_showcase_website.py` and `tests/test_academic_website.py`) pass 100% under `pwsh -File ./scripts/verify.ps1`.

## Edge Coverage

**Coverage:** 6/6 applicable edges resolved · 0 unresolved

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| boundary | PORTAL-MOB-01 | ✅ covered | Verified at exact viewport thresholds: 360px (minimum mobile phone), 480px, 600px, 900px, 1024px. |
| boundary | PORTAL-MOB-02 | ✅ covered | Font scaling floor enforced at 0.75rem / 11px; momentum scroll activates immediately when table/math content exceeds container width. |
| empty | PORTAL-CITE-01 | ✅ covered | Citation keys missing from `CITATIONS_DB` gracefully fallback to plain jump link without throwing JS exceptions or blank popovers. |
| concurrency | PORTAL-CITE-02 | ✅ covered | Rapid sequential taps on different citation badges clear prior timeout/hide queues and cleanly swap active popover without orphaned tooltips. |
| boundary | PORTAL-CITE-02 | ✅ covered | Popovers positioned near the viewport right/bottom boundaries are dynamically clamped to `max-width: 92vw` and safe viewport margins. |
| idempotency | PORTAL-MOB-01 | ✅ covered | Repeated opening/closing of the mobile drawer leaves DOM classes (`open`) and scroll lock in deterministic states. |

## Prohibitions (must-NOT)

**Coverage:** 4/4 applicable prohibitions resolved · 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT introduce external CDN scripts or remote stylesheet links | PORTAL-VERIF-01 | resolved (test) | Verified by `test_zero_external_dependencies` in test suites; preserves offline resilience. |
| MUST NOT produce horizontal body scroll on viewports between 360px and 1024px | PORTAL-MOB-02 | resolved (test) | Verified by DOM overflow assertion; overflow restricted strictly to internal scroll wrappers. |
| MUST NOT truncate or shrink mathematical equations below accessible readability floor (0.85em) | PORTAL-MOB-02 | resolved (test) | Verified by CSS font-size clamp rules and scroll fallback. |
| MUST NOT block or hijack native touch gestures outside the mobile drawer backdrop | PORTAL-MOB-01 | resolved (test) | Verified by pointer-events and passive event listener configurations. |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                                                        |
|--------------------|-------|------|--------|--------------------------------------------------------------|
| Goal Clarity       | 0.95  | 0.75 | ✅ PASS | Specific, measurable mobile ergonomics and citation preview outcomes. |
| Boundary Clarity   | 0.90  | 0.70 | ✅ PASS | Explicit in-scope deliverables and strict out-of-scope backend boundaries. |
| Constraint Clarity | 0.88  | 0.65 | ✅ PASS | Zero-build, offline-first, $\ge 44\times 44\text{px}$ touch targets, sub-30s gates. |
| Acceptance Criteria| 0.90  | 0.70 | ✅ PASS | 11 falsifiable pass/fail criteria.                          |
| **Ambiguity**      | **0.09** | **≤ 0.20** | **✅ GATE PASSED** | **Requirements fully locked and ready for discuss-phase.** |
