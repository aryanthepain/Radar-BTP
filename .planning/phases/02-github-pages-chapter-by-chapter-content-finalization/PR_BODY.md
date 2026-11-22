## Summary

**Phase 2: GitHub Pages Chapter-by-Chapter Content Finalization**
**Goal:** Progressively refine, update, and finalize the academic BTP thesis report content on the GitHub Pages website (`docs/`) chapter-by-chapter based on iterative user-supplied content and guidance, accommodating multiple sequential planning and execution waves within this single phase.
**Status:** Verified ✓

Brings the GitHub Pages BTP-1 academic thesis report (`docs/index.html` and `docs/app.js`) to publication-grade scientific rigor: step-by-step FMCW mathematical physics derivations, 6-column Classical DSP synthesis matrix, RadDet RF spectrum sensing terminology alignment, honest experimental discrepancy reconciliations, sequential IEEE citation renumbering [1..18] with interactive tooltip popovers, Canva timeline Gantt schedule modernization (Figure 5.1), and permanent regression gates.

Closes #21

## Changes

### Plan 02-01: Report Framing & Chapter 1 Introduction
- Updated thesis title and subtitle to approved IIT Guwahati BTP-1 formulations.
- Injected verbatim Chapter 1 content with research questions, motivation, and scope.
- **Key files:** `docs/index.html`

### Plan 02-02: Chapter 2 Literature Review & Bibliography Ingestion
- Injected Chapter 2 Literature Review covering automotive radar evolution, classical DSP milestones, and deep learning detectors.
- Synchronized initial bibliography entries.
- **Key files:** `docs/index.html`

### Plan 02-03: Chapter 3 Methodology & Mathematical Architecture
- Injected Chapter 3 Methodology covering FMCW signal model, Range/Doppler processing, CFAR algorithms, and spatial AoA.
- Added Section 1.4, Table 2.1, Algorithms 3.1–3.5, and Figures 3.1–3.4.
- **Key files:** `docs/index.html`

### Plan 02-04: Chapter 4 Experimental Results & Quantitative Benchmarks
- Injected Chapter 4 Experimental Results & Analysis.
- Added Table III reproduction, fully trained YOLOv9-C empirical metrics, Tables 4.1–4.7, Figures 4.1–4.10, and Code Listing 4.1.
- **Key files:** `docs/index.html`

### Plan 02-05: Chapter 5 Conclusion, Future Work & Synthesis
- Injected Chapter 5 Conclusion & Future Work with Dual-Path Synthesis (Track I vs Track II).
- Added Tables 5.1–5.2, lab checklist, and updated ScrollSpy TOC links.
- **Key files:** `docs/index.html`

### Plan 02-06: Official Abstract Finalization
- Finalized structured abstract container with empirical dual-track summary and approved index terms.
- **Key files:** `docs/index.html`

### Plan 02-07: Additional Thesis Artifacts Finalization
- Scaffolding of thesis defense artifacts, appendices, and timeline specifications.
- **Key files:** `docs/index.html`, `.planning/`

### Plan 02-08: Evidence Audit Dossier & Discrepancy Reconciliation
- Authored forensic evidence audit dossier in `02-EVIDENCE-AUDIT.md`.
- Documented 5 experimental claims with verified artifact mapping (RadDet partition math, YOLOv9-C vs prototype runs, synthetic CNN samples, clutter attenuation definition, and MUSIC search grid vs physical resolution).
- **Key files:** `.planning/phases/02-github-pages-chapter-by-chapter-content-finalization/02-EVIDENCE-AUDIT.md`

### Plan 02-09: Publication-Grade HTML/JS Realignment & Invariant Gates
- Injected FMCW KaTeX math derivations into Chapter 2 Section 2.1 ($f_b \approx 2 S R_0 / c$, $\Delta R = 0.15\text{ m}$, $\Delta v = 0.304\text{ m/s}$).
- Silently purged all legacy 58.8 μs parameters in active manuscript.
- Replaced Table 3.1 with publication-grade 6-column DSP synthesis table.
- Rectified RadDet RF spectrum sensing terminology across all 5 active chapters.
- Injected Table 4.1/4.5 partition disclosure footnote (14,001/6,001/20,001 split, 19,998 frame chunking).
- Renumbered IEEE citations sequentially [1..18] in order of first appearance and segregated legacy citations [19..32] below `<hr>`.
- Synchronized `docs/app.js` `CITATIONS_DB` keys 1–32 for offline floating tooltips.
- Added permanent regression tests in `tests/test_academic_website.py`.
- **Key files:** `docs/index.html`, `docs/app.js`, `tests/test_academic_website.py`

### Plan 02-10: Canva Gantt Schedule Modernization (Figure 5.1)
- Modernized Figure 5.1 Gantt schedule using high-resolution export from Canva design `DAHbQ0tvIMc`.
- Exported and integrated `docs/assets/diagrams/timeline_gantt.png` and valid `docs/assets/diagrams/timeline_gantt.svg` (>1KB).
- Aligned Figure 5.1 caption, alt text, and Section 5.5 narrative with A1–A9 milestones, presentation dates (23 Nov presentation, May '27 defense), and semester break.
- Confined all changes strictly to GitHub Pages assets; zero LaTeX/PDF regressions.
- **Key files:** `docs/assets/diagrams/timeline_gantt.png`, `docs/assets/diagrams/timeline_gantt.svg`, `docs/index.html`

## Requirements Addressed

- **R1 (Evidence Audit)**: Authored `02-EVIDENCE-AUDIT.md` classifying all 5 disputed claims against git artifacts.
- **R2 (FMCW Physics Recovery)**: Step-by-step KaTeX derivations in Chapter 2/3 with verified constants ($T_c = 50\ \mu\text{s}$, $f_c = 77\text{ GHz}$, $\Delta v = 0.304\text{ m/s}$); legacy 58.8 μs parameters purged.
- **R3 (Experimental Discrepancy Reconciliation)**: Decoupled Track I from Track II, disclosed 14k/6k/20k split, qualified comparative benchmark vs Table III.
- **R4 (RadDet Terminology)**: Standardized to RF wideband spectrum sensing and modulation classification from spectrograms; zero automotive road scene conflation.
- **R5 (IEEE Citation Realignment)**: Citations sequentially numbered [1..18], mirrored in `docs/app.js` tooltips, legacy references segregated.
- **R6 (Scope & Zero-Regression Gate)**: Zero changes to LaTeX templates; 100% deterministic test pass rate.
- **R7 (Canva Gantt Modernization)**: Modernized Figure 5.1 Gantt chart and Section 5.5 narrative with Canva design `DAHbQ0tvIMc` and A1–A9 taxonomy.

## Verification

- [x] Automated verification: Passed
  - `pytest tests/test_academic_website.py tests/test_showcase_website.py`: 17 passed in 0.36s
  - `pwsh -File ./scripts/verify.ps1`: 58 passed, 97.35% code coverage, zero exposed secrets, syntax valid
- [x] Security Audit: `02-SECURITY.md` asserts `threats_open: 0` across 4 categories
- [x] Broken Windows Audit: 0 open windows

## Key Decisions

- **D-01 (RadDet Partition Truth)**: Disclose official 20k/14k/6k partition vs 14,001/6,001/20,001 benchmark split in Table 4.1 footnote.
- **D-02 (YOLOv9-C Framing)**: Frame as comparative benchmark against Lin et al. Table III YOLOv9-M rather than exact reproduction.
- **D-03 (Synthetic Sample Count)**: Demarcate 136k-param CNN with 32 samples as lightweight proof-of-concept.
- **D-04 (Clutter Attenuation Definition)**: Define 12.94 dB as total average signal-power reduction under slow-time mean-subtraction.
- **D-05 (Radar Parameter Authority)**: `src/sim/radar_config.py` is sole source of truth ($T_c = 50\ \mu\text{s}$, $\Delta v = 0.304\text{ m/s}$).
- **D-06 (6-Column Synthesis Matrix)**: Replace Table 3.1 with comprehensive 6-column DSP synthesis table.
- **D-08 (Angular Grid Clarification)**: 180-bin MUSIC search grid is numerical discretization, distinct from Rayleigh limit ($\approx 28.6^\circ$).
- **D-09 (Sequential Citations)**: Number citations [1..18] sequentially by first appearance in 5-chapter manuscript.
- **D-10 (Archival Segregation)**: Segregate archival citations [19..32] below `<hr class="archival-ref-divider">`.
- **D-11 (Canva Design Authority)**: Canva design `DAHbQ0tvIMc` is visual authority for Figure 5.1 Gantt schedule.
- **D-12 (Tooltip DB Synchronization)**: `docs/app.js` `CITATIONS_DB` synchronized with offline text representation.
- **D-16 (Zero Scope Bleed)**: LaTeX/Overleaf templates strictly preserved with zero edits.
