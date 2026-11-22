---
phase: 03-academic-portal-priority-0-polish-mobile-ui-ieee-citation-ca
plan: 02
subsystem: ui
tags:
  [
    ieee-citations,
    mobile-bottom-sheet,
    citation-popover,
    pulse-animation,
    viewport-clamping,
    safe-dom,
    vanillajs,
  ]

# Dependency graph
requires:
  - phase: 03-academic-portal-priority-0-polish-mobile-ui-ieee-citation-ca
    provides: Mobile drawer navigation, touch targets, and two-tier overflow containment (03-01)
provides:
  - Unconditionally active IEEE citation preview engine across all 30 references in CITATIONS_DB without debug flags (D-04)
  - Desktop floating popover card with dynamic badge coordinate positioning and viewport collision boundary clamping (D-03)
  - Mobile slide-up bottom-sheet card with rounded top corners, backdrop scrim (.citation-backdrop), and safe-area-inset padding (D-03)
  - Background body scroll-lock (body.nav-open) during mobile bottom-sheet inspection
  - Direct DOI/publisher link navigation (<a class="tooltip-doi-btn">)
  - Interactive "View in Reference List" button (<button class="tooltip-jump-btn">) smooth-scrolling to Section 9 (#ref-X) with 2-second glowing sky-blue pulse animation (.highlight-pulse)
  - Safe DOM element construction (document.createElement, textContent, classList) preventing CWE-79 DOM XSS
affects: [phase-03, academic-portal, docs]

# Actuals (#2632)
actuals:
  tokens: 22000
  tasks: 3
  commits: 3
  plan_head_before: b09887c4024321bc45280ae15936f2ff3a2f53f9
  plan_head_after: 6ed79de3f4c5c7198a4f2693606b8986e2fdf284

# Tech tracking
tech-stack:
  added: []
  patterns:
    [
      adaptive-citation-popover,
      mobile-bottom-sheet,
      highlight-pulse-animation,
      collision-boundary-clamping,
      safe-dom-construction,
    ]

key-files:
  created: []
  modified:
    - docs/app.js
    - docs/styles.css
    - tests/test_academic_website.py
    - tests/test_showcase_website.py

key-decisions:
  - "Eliminate debug flag window.ENABLE_CITATION_TOOLTIPS entirely; activate IEEE citation popovers unconditionally by default across all 30 references in CITATIONS_DB per D-04."
  - "Differentiate viewport interaction models: desktop (>600px) receives elevated floating tooltip with boundary clamping; mobile (<=600px) and touch taps receive slide-up bottom-sheet with backdrop scrim and body scroll lock per D-03."
  - "Prevent immediate anchor jumps to Section 9 on mobile tap by executing e.preventDefault() and opening the preview bottom-sheet card first (PORTAL-CITE-02, resolving Pitfall 2)."
  - "Implement @keyframes highlightPulse in docs/styles.css with 2-second sky-blue glow outline triggered when smooth-scrolling from 'View in Reference List' button to #ref-X (resolving Pitfall 4)."
  - "Construct all popover and bottom-sheet DOM nodes strictly via document.createElement() and textContent to prevent CWE-79 DOM XSS vulnerabilities per T-03-03."

patterns-established:
  - "Pattern 1: Adaptive IEEE citation preview engine with desktop boundary clamping and mobile slide-up bottom-sheet"
  - "Pattern 2: Section 9 smooth scroll with visual pulse highlight animation (.highlight-pulse)"
  - "Pattern 3: Safe zero-build DOM assembly with strict offline asset isolation"

requirements-completed:
  - PORTAL-CITE-01
  - PORTAL-CITE-02
  - PORTAL-VERIF-01

coverage:
  - id: D1
    description: "Unconditional default activation of citation popovers across all 30 references without gating flags"
    requirement: PORTAL-CITE-01
    verification:
      - kind: unit
        ref: tests/test_academic_website.py#test_citation_popover_active_by_default
        status: pass
    human_judgment: false
  - id: D2
    description: "Mobile slide-up bottom-sheet card with darkened backdrop scrim and safe-area padding"
    requirement: PORTAL-CITE-02
    verification:
      - kind: unit
        ref: tests/test_academic_website.py#test_citation_bottom_sheet_and_pulse_jump
        status: pass
    human_judgment: false
  - id: D3
    description: "Smooth scroll jump to Section 9 with 2-second glowing pulse animation (.highlight-pulse)"
    requirement: PORTAL-CITE-02
    verification:
      - kind: unit
        ref: tests/test_academic_website.py#test_citation_bottom_sheet_and_pulse_jump
        status: pass
    human_judgment: false
  - id: D4
    description: "Desktop floating popover card with horizontal and vertical viewport boundary collision clamping"
    requirement: PORTAL-CITE-01
    verification:
      - kind: unit
        ref: tests/test_academic_website.py#test_desktop_citation_tooltip_collision_clamping
        status: pass
    human_judgment: false
  - id: D5
    description: "Universal verification gate pass rate (100%), coverage >= 90%, and offline resilience"
    requirement: PORTAL-VERIF-01
    verification:
      - kind: other
        ref: scripts/verify.ps1
        status: pass
    human_judgment: false

# Metrics
duration: 12 min
completed: 2026-11-19
status: complete
---

# Phase 03 Plan 02: IEEE Citation Preview Engine & Mobile Bottom-Sheet Summary

**Always-active, publication-grade IEEE citation popover engine, mobile slide-up bottom-sheet cards, Section 9 pulse jump animation, and offline resilience sign-off for the BTP academic thesis reading portal in docs/ (Closes #21).**

## Performance

- **Duration:** 12 min
- **Started:** 2026-11-19T02:54:21+05:30
- **Completed:** 2026-11-19T03:06:00+05:30
- **Tasks:** 3
- **Files modified:** 4

## Accomplishments

- Eliminated the gating debug flag `window.ENABLE_CITATION_TOOLTIPS` entirely; interactive IEEE citation cards are now active unconditionally by default across all 30 references in `CITATIONS_DB` (D-04, PORTAL-CITE-01).
- Designed and styled an ergonomic mobile slide-up bottom-sheet card under `@media (max-width: 600px)` featuring rounded top corners (`border-radius: 16px 16px 0 0`), darkened scrim backdrop (`.citation-backdrop`), mobile dismiss button ("✕"), and iOS safe area padding (`env(safe-area-inset-bottom)`).
- Prevented immediate jarring page jumps on touchscreens (resolving Pitfall 2): tapping a citation badge opens the bottom-sheet card in tap-to-inspect mode with background body scroll-lock (`body.nav-open`).
- Implemented Section 9 smooth scroll navigation with an animated glowing pulse: clicking "View in Reference List" smooth-scrolls the viewport directly to `#ref-X`, activates `@keyframes highlightPulse` (`.highlight-pulse`) with a 2-second glowing sky-blue aura, and auto-dismisses the preview card.
- Provided direct DOI/publisher link navigation buttons (`.tooltip-doi-btn`) for instant outbound academic paper exploration.
- Implemented desktop floating card positioning with dynamic badge coordinate calculation, max-width clamping (`Math.min(480, window.innerWidth - 40)`), horizontal boundary clamping against viewport edges, and vertical boundary flipping (`rect.top < 150` flips below badge).
- Cleanly isolated desktop hover timeouts with 200ms debounce grace period, preventing card flickering or orphaned popovers during cursor transitions.
- Strictly mitigated CWE-79 DOM XSS (T-03-03): all popover and bottom-sheet DOM nodes are constructed via `document.createElement`, `textContent`, and `classList` without dynamic `innerHTML` string evaluation.
- Added comprehensive deterministic test suites in `tests/test_academic_website.py` (`test_citation_popover_active_by_default`, `test_citation_bottom_sheet_and_pulse_jump`, `test_desktop_citation_tooltip_collision_clamping`) and expanded `tests/test_showcase_website.py` (`test_05_mobile_ergonomics_and_citation_assets`).
- Verified universal verification gate `pwsh -File ./scripts/verify.ps1`: 100% test pass rate across 64 unit/integration tests with 97.35% code coverage and zero external CDN leaks.

## Task Commits

Each task was committed atomically:

1. **Task 1: Tracer slice — Scaffold citation popover test harness & wire un-gated citation card foundation** - `147f6fc` (feat)
2. **Task 2: Mobile slide-up bottom-sheet card, Section 9 pulse jump, and touch tap-to-inspect** - `767cbac` (feat)
3. **Task 3: Desktop floating tooltip boundary clamping and universal verification sign-off** - `6ed79de` (feat)

**Plan metadata commit:** pending next step.

## Files Created/Modified

- `docs/app.js`: Refactored `initCitationTooltips()` to remove `ENABLE_CITATION_TOOLTIPS` gate, assemble safe DOM nodes, render direct DOI and "View in Reference List" buttons, handle mobile touch tap-to-inspect, manage `body.nav-open` scroll lock, and perform desktop coordinate clamping and debounce timers.
- `docs/styles.css`: Added `@keyframes highlightPulse` and `.highlight-pulse`, `.citation-backdrop`, tooltip header, close button, DOI link button, and Section 9 jump button; authored `@media (max-width: 600px)` slide-up bottom-sheet card rules; updated desktop `.citation-tooltip` max-width to 480px.
- `tests/test_academic_website.py`: Added `test_citation_popover_active_by_default`, `test_citation_bottom_sheet_and_pulse_jump`, and `test_desktop_citation_tooltip_collision_clamping`.
- `tests/test_showcase_website.py`: Expanded `test_05_mobile_ergonomics_and_citation_assets` to verify `initCitationTooltips` declaration and zero external CDNs across HTML, CSS, and JS.

## Decisions Made

- _D-03 (Citation Tooltip Ergonomics):_ Dual-mode display: elevated floating popover on desktop with collision clamping; slide-up bottom-sheet on mobile (<600px) with backdrop scrim and Section 9 pulse jump.
- _D-04 (Elimination of Gating Flag):_ Fully un-gate citation tooltips; remove `window.ENABLE_CITATION_TOOLTIPS` so all 30 citations in `CITATIONS_DB` are interactive by default.
- _D-07 (Safe DOM Construction):_ Strictly assemble DOM nodes using `document.createElement()` and `textContent` to eliminate CWE-79 DOM XSS risks.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED

- All 3 task commits (`147f6fc`, `767cbac`, `6ed79de`) exist in git history.
- `docs/styles.css`, `docs/app.js`, `tests/test_academic_website.py`, and `tests/test_showcase_website.py` exist and pass all tests.
- Universal verification gate `pwsh -File ./scripts/verify.ps1` passes with 64/64 tests green and 97.35% code coverage.
