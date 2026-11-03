## Summary

**Phase 01.2.1: Interactive Research Showcase & Thesis Presentation Website**
**Goal:** Deliver a lightweight, clean, interactive presentation website for the supervising professor illustrating the end-to-end BTP journey across all three notebooks (`01_radar_classical_dsp`, `02_radar_deep_learning_detection`, `03_raddet_spectrum_detection_kaggle`), showcasing key DSP/DL code snippets, visual flowcharts, benchmark metrics, and clear comparative progression (analytical toy baseline -> synthetic FMCW radar simulation -> real-world RadDet ICASSP 2025 dataset).
**Status:** Verified ✓

## Changes

### Plan 01.2.1-01: Asset Pipeline, Automated Notebook Extraction & Vector Diagrams
- Implemented automated notebook image extraction script `scripts/export_showcase_assets.py` to extract 25 visual figures, architecture SVGs, timeline diagram, benchmark artifacts, and offline Prism.js assets into `docs/assets/`.
- **Key files:** `scripts/export_showcase_assets.py`, `docs/assets/nb1/*`, `docs/assets/nb2/*`, `docs/assets/nb3/*`, `docs/assets/diagrams/*`, `docs/assets/vendor/*`.

### Plan 01.2.1-02: Zero-Build Static Website Implementation
- Constructed single-page longform presentation website in `docs/` using the Dark Cyber-Radar aesthetic (`#0a0e17` canvas, neon cyan `#00f0ff` & amber `#f59e0b` accents), sticky sidebar with ScrollSpy, interactive image lightboxes, 1-click code copying, and 7-metric master comparison table.
- **Key files:** `docs/index.html`, `docs/styles.css`, `docs/app.js`.

### Plan 01.2.1-03: Deterministic Smoke Test Suite & GitHub Pages Deployment
- Authored fast, offline Python in-memory test suite in `tests/test_showcase_website.py` verifying DOM structure, local asset resolution, zero dead anchors, zero external CDN links, and table completeness.
- Added GitHub Pages deployment workflow `.github/workflows/deploy-pages.yml` and `docs/.nojekyll` static bypass.
- **Key files:** `tests/test_showcase_website.py`, `.github/workflows/deploy-pages.yml`, `docs/.nojekyll`.

## Requirements Addressed
- **PRES-WEB-01**: Automated Asset Extraction & Pre-Rendered Vector Visuals (Verified)
- **PRES-WEB-02**: Zero-Build Responsive Static Presentation Website (Verified)
- **PRES-WEB-03**: Deterministic Smoke Test Suite & Zero Broken Links (Verified)

## Verification
- [x] Automated verification: Passed 31/31 unit & integration tests in `pwsh -File ./scripts/verify.ps1`
- [x] Fast in-memory DOM & asset validation in `tests/test_showcase_website.py`: Passed 4/4 in 0.48s
- [x] JavaScript syntax verification: `node --check docs/app.js` cleanly exited with code 0
- [x] GitHub Pages API configuration: Configured `build_type: workflow` targeting `https://aryanthepain.github.io/Radar-BTP/`

## Key Decisions
- **Zero-Build Static Architecture**: No npm, Webpack, or Vite build steps; runs natively via static file serving or `file:///` protocol.
- **Offline Resilience**: Zero external CDN font/CSS/JS links to guarantee zero-fail offline presentation during professor reviews.
- **Dark Cyber-Radar Design System**: High-contrast palette (`#0a0e17`, `#00f0ff`, `#f59e0b`) tailored for radar spectrograms and signal representations.
- **Automated Pages Deployment**: GitHub Actions workflow triggers on push to `main` deploying `./docs` artifact directly to GitHub Pages.
