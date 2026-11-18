# Phase 02: GitHub Pages Chapter-by-Chapter Content Finalization - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-11-18T19:30:00+05:30
**Phase:** 02-github-pages-chapter-by-chapter-content-finalization
**Areas discussed:** Discrepancy Reconciliation & Experimental Framing, Mathematical Physics Derivation Depth & Parameter Transition, IEEE Citation Renumbering Strategy & Archival Bibliography Separation, Evidence Audit Dossier Exposure & Advisor Defense Linkage

---

## Discrepancy Reconciliation & Experimental Framing

| Option | Description | Selected |
|--------|-------------|----------|
| Dual-Partition Comparative Table + Deviation Note | Report both official ICASSP partition (20k/14k/6k) and project split (14k/6k/20k) with full deviation box | |
| Dedicated Evaluation Partition Subsection | Create standalone subsection detailing data-loader extraction and SNR binning | |
| Minimal Disclosure Footnote | Keep main table showing project's evaluated partition numbers and add concise footnote disclosing deviation | ✓ |
| You decide | Standard academic disclosure | |

**User's choice:** Minimal Disclosure Footnote. Keep main table showing project's evaluated partition numbers with concise footnote disclosing deviation from published ICASSP benchmark split.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Two-Tier Benchmark Structure | Present 15-epoch prototype as validated baseline, 66-epoch YOLOv9-C as comparative cloud benchmark | |
| Unified Table with Verification Status Column | Group prototype and cloud runs with validation status column | |
| Demote Unverified Cloud Run to Appendix | Keep only 15-epoch prototype in Chapter 4 | |
| User Freeform Clarification | The 15-epoch run is just a smoke test, no need to pay any heed to it | ✓ |

**User's choice:** The 15-epoch run is just a smoke test, no need to pay any heed to it. Focus on the 66-epoch YOLOv9-C run as the primary benchmark.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Comparative Benchmark against Published Baseline | Present 66-epoch YOLOv9-C run as comparative benchmark against published Table III (YOLOv9-M) with close metric convergence | ✓ |
| Independent Evaluation Benchmark | Frame as independent experimental evaluation on RadDet | |
| You decide | Standard academic phrasing | |

**User's choice:** Comparative Benchmark against Published Baseline. Present 66-epoch YOLOv9-C as comparative benchmark against Lin et al.'s Table III YOLOv9-M results, highlighting close metric convergence. Also include the graphs from GitHub Pages to showcase the result.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Accurate Physical Nomenclature & Clear Qualification | Directly define 12.94 dB as total average signal power reduction; distinguish 180-point grid from ~28° physical beamwidth | ✓ |
| Dedicated Experimental Nuance Callout Box | Highlight in special callout box | |
| You decide | Integrated DSP subsections | |

**User's choice:** Accurate Physical Nomenclature & Clear Qualification. Define 12.94 dB as total average signal power reduction and distinguish 180-point MUSIC grid from ~28° physical array beamwidth with range-only association constraints noted.

---

## Mathematical Physics Derivation Depth & Parameter Transition

| Option | Description | Selected |
|--------|-------------|----------|
| Active Sweep vs PRI Demarcation | Derive active simulator config and add technical note distinguishing sweep from PRI | |
| Direct Canonical Replacement with Historical Note | Footnote noting legacy 58.8 μs exploratory drafts | |
| Silent Purge (with internal doc) | Exclusively derive active 50 μs config on public page; record history in internal planning file | ✓ |
| You decide | Standard derivation structure | |

**User's choice:** Silent purge on GitHub Pages (derive strictly 50 μs configuration), and record the historical parameter evolution in an internal planning file in Phase 2 (`02-EVIDENCE-AUDIT.md`).

---

| Option | Description | Selected |
|--------|-------------|----------|
| Comprehensive 6-Column Synthesis Table | Method, Operating Principle, Mathematical Formulation, Statistical Assumptions, Complexity, Failure Modes | ✓ |
| Two Focused Modular Tables | Table 3.1 Spectral/Clutter + Table 3.2 Detection/AoA | |
| You decide | Optimal visual clarity | |

**User's choice:** Comprehensive 6-Column Synthesis Table in Table 3.1.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Full 7-Axis Matrix with Strict Bibliographic Grounding | Full 7-axis matrix, 'Not reported' for unmeasured parameters, correct AdaRadar neural routing | ✓ |
| Two-Tier Literature Table | Two separate tables for task vs efficiency | |
| You decide | Maximum readability | |

**User's choice:** Full 7-Axis Matrix with Strict Bibliographic Grounding.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Evidence-Grounded Proof-of-Concept | Audit checkpoint in Plan 02-08, update Chapters 3 & 4 with verified values, qualify as proof-of-concept | ✓ |
| Dual-Configuration Presentation | Document both 32-sample and 150-sample baselines | |
| You decide | Defensible scientific presentation | |

**User's choice:** Evidence-Grounded Proof-of-Concept. Audit checkpoint during Plan 02-08 to lock exact parameters and qualify as lightweight proof-of-concept. Note that rapid runs (e.g., 32 samples) may have been smoke tests and should not hinder progress.

---

## IEEE Citation Renumbering Strategy & Archival Bibliography Separation

| Option | Description | Selected |
|--------|-------------|----------|
| Active [1..N] + Monotonic Archival [N+1..M] below <hr> | Active numbered [1..N], archival continued monotonically [N+1..M] below <hr> | ✓ |
| Active [1..N] + Prefixed Archival [A1..AK] | Archival prefixed with [A1]..[AK] | |
| Retain Legacy IDs for Archival References | Keep legacy IDs intact below <hr> | |
| You decide | Cleanest scheme | |

**User's choice:** Active [1..N] + Monotonic Archival [N+1..M] below `<hr>`.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Comprehensive Dictionary for Both [1..N] and [N+1..M] | Synchronize app.js with all references, archival badged | ✓ |
| Active-Only Dictionary [1..N] | Tooltips for active only, archival jumps to anchor | |
| You decide | Zero console errors | |

**User's choice:** Comprehensive Dictionary for Both [1..N] and [N+1..M] in `docs/app.js`.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Verified Reference Table in 02-EVIDENCE-AUDIT.md | Canonical reference verification table assembled in Plan 02-08 before Plan 02-09 injection | ✓ |
| Direct In-Code Verification during Plan 02-09 | Audit directly while editing HTML/JS | |
| You decide | Zero placeholder DOIs | |

**User's choice:** Verified Reference Table in `02-EVIDENCE-AUDIT.md` (Plan 02-08).

---

| Option | Description | Selected |
|--------|-------------|----------|
| Granular Individually-Linked Anchors | Each citation in a group is an independent clickable anchor for discrete popovers | ✓ |
| Grouped Range Anchors | Only range endpoints linked | |
| You decide | Standard academic web UX | |

**User's choice:** Granular Individually-Linked Anchors (`<a href="#ref-1">[1]</a>, <a href="#ref-2">[2]</a>`).

---

## Evidence Audit Dossier Exposure & Advisor Defense Linkage

| Option | Description | Selected |
|--------|-------------|----------|
| Mirror Discrepancy Q&As into docs/ADVISOR-DEFENSE.md | Immediately add defense Q&As to docs/ADVISOR-DEFENSE.md | |
| Strictly Planning-Internal (with GitHub Issue) | Confine to 02-EVIDENCE-AUDIT.md; create GitHub issue to triage which go to ADVISOR-DEFENSE.md | ✓ |
| You decide | Best placement | |

**User's choice:** Confine all discrepancy findings to `02-EVIDENCE-AUDIT.md` for now, and create a GitHub issue to review discrepancies and decide which are worthy to go into `docs/ADVISOR-DEFENSE.md`.

---

| Option | Description | Selected |
|--------|-------------|----------|
| 3-Tier Evidence Taxonomy | (1) Verified, (2) Partially Verified / Comparative, (3) Smoke Test / Prototyping | ✓ |
| 2-Tier Binary Taxonomy | Confirmed vs Discrepancy | |
| You decide | Standard academic taxonomy | |

**User's choice:** 3-Tier Evidence Taxonomy in `02-EVIDENCE-AUDIT.md`.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Dedicated Section in 02-EVIDENCE-AUDIT.md + GitHub Issue Linkage | 4-field table in Section 8 of 02-EVIDENCE-AUDIT.md and referenced in GitHub issue | ✓ |
| Standalone Markdown Checklist | 02-HUMAN-CONFIRMATION.md separate file | |
| You decide | Seamless tracking | |

**User's choice:** Dedicated Section in `02-EVIDENCE-AUDIT.md` + GitHub Issue Linkage.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Augment test_academic_website.py with Invariant Checks | Add deterministic tests for citations, DOIs, legacy params, original draft preservation, zero LaTeX edits | ✓ |
| Retain Existing Test Suite without Additions | Rely on existing 20 tests | |
| You decide | Regression protection | |

**User's choice:** Augment `tests/test_academic_website.py` with Invariant Checks.

---

## Agent's Discretion

- Styling of the `<hr>` bibliography divider, table formatting, and KaTeX container layout.

## Deferred Ideas

- Creation of GitHub issue to triage and migrate selected discrepancy defense Q&As into `docs/ADVISOR-DEFENSE.md`.
- LaTeX/PDF report synchronization deferred until after web content finalization.
