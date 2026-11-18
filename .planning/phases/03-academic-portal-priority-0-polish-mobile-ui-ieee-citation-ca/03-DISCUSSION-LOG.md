# Phase 03: Academic Portal Priority 0 Polish: Mobile UI & IEEE Citation Cards - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-11-19
**Phase:** 03-academic-portal-priority-0-polish-mobile-ui-ieee-citation-ca
**Areas discussed:** Math/Table Wrappers, Citation Popover Positioning, Mobile Drawer Polish, Test Strategy

---

## Math & Table Scroll Wrappers

| Option | Description | Selected |
|--------|-------------|----------|
| Hybrid Approach | Hardcode semantic CSS scroll wrappers in `docs/index.html` AND add a runtime JS safety sweep in `docs/app.js` to wrap any remaining dynamic/KaTeX blocks | ✓ |
| Pure Client-Side JS | Keep HTML clean and let `docs/app.js` automatically wrap all `.katex-display` and `<table>` elements on `DOMContentLoaded` | |
| Pure Static HTML | Manually wrap every table and formula block in `<div class="table-scroll-wrapper">` without JS intervention | |

**User's choice:** Hybrid Approach: Hardcode semantic CSS scroll wrappers in docs/index.html AND add a runtime JS safety sweep in docs/app.js to wrap any remaining dynamic/KaTeX blocks.
**Notes:** Combines static HTML rendering speed with client-side defensive safety against uncontained KaTeX equations.

---

## Citation Popover Positioning & Layout

| Option | Description | Selected |
|--------|-------------|----------|
| Floating popover on desktop, bottom-sheet card on mobile | Render floating near badge on >600px, but slide up as an accessible bottom-sheet card with backdrop on <600px | ✓ |
| Universal floating popover | Always float near the tapped badge with viewport coordinate clamping (left/right bounds) across all screen widths | |
| Centered modal dialog | Always open as a centered modal dialog box on all viewports on click/tap | |

**User's choice:** Floating popover on desktop, bottom-sheet card on mobile: Render floating near badge on >600px, but slide up as an accessible bottom-sheet card with backdrop on <600px.
**Notes:** Provides optimal ergonomics for mouse/desktop (hover tooltip) and touch/mobile (bottom-sheet modal with thumb-friendly controls).

---

## Mobile Drawer Interaction Polish

| Option | Description | Selected |
|--------|-------------|----------|
| Full polish | Enable body scroll-lock (prevent background scrolling) when drawer is open AND morph hamburger into an animated ✕ icon | ✓ |
| Scroll-lock only | Prevent body scrolling behind the open drawer, but keep the hamburger button static without animation | |
| Minimal | Simple show/hide toggle without scroll lock or icon morphing | |

**User's choice:** Full polish: Enable body scroll-lock (prevent background scrolling) when drawer is open AND morph hamburger into an animated ✕ icon.
**Notes:** Toggles `.nav-open` on `body` and rotates hamburger lines into a cross icon.

---

## Test Assertion Coverage

| Option | Description | Selected |
|--------|-------------|----------|
| Comprehensive Static DOM & CSS Parser Tests | Parse HTML/CSS AST, assert touch target rules (min 44px), media queries (@media <=1024px, <=900px, <=600px), scroll wrapper classes, and citation DOM integrity (zero external browser binary dependencies, sub-5s execution) | ✓ |
| Simulated Browser Geometry with Headless Driver | Install Playwright/Selenium to measure exact boundingClientRects in a headless Chromium instance | |
| Basic File Content Grep | Simple string matching for class names and selectors | |

**User's choice:** Comprehensive Static DOM & CSS Parser Tests.
**Notes:** Preserves sub-30s deterministic test gate under `scripts/verify.ps1`.

---

## the agent's Discretion

- Easing curves for bottom-sheet slide up animation.
- Subtle edge-fade scroll mask styling for overflow wrappers.

## Deferred Ideas

- Full offline PWA service worker with service-worker caching (deferred to future portal polish phase).
- Dynamic reading progress bar enhancements (Issue #20: `feat(docs): Dynamic Reading Progress Bar & Scroll Tracking in Thesis Portal`).
