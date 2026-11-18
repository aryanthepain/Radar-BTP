# Phase 02: GitHub Pages Chapter-by-Chapter Content Finalization — Specification

**Created:** 2026-11-18  
**Ambiguity score:** 0.15 (gate: ≤ 0.20)  
**Requirements:** 6 locked  

---

## Goal

Bring the GitHub Pages BTP-1 academic thesis report (`docs/index.html` and `docs/app.js`) to publication-grade scientific rigor through a staged two-plan sequence (Plan 02-08 for repository evidence auditing, mathematical recovery, and discrepancy documentation; Plan 02-09 for HTML content integration, citation renumbering, and verification), strictly preserving the archived 7-chapter draft and leaving LaTeX templates untouched.

---

## Background

The repository hosts an academic thesis portal on GitHub Pages (`docs/index.html`) containing two distinct report sections:
1. **The Active 5-Chapter Manuscript (`#ch1-intro` through `#ch5-conclusion`):** The authoritative submission draft for IIT Guwahati BTP-1.
2. **The Archived 7-Chapter Original Draft (`#ch1-intro-original` through `#ch7-conclusion`):** A reference repository of mathematical derivations, classical DSP principles, and initial project history.

A comprehensive audit guided by `report_content/changes.md` reveals critical gaps:
- **Mathematical Derivations:** Classical FMCW physics (chirp generation, dechirping, beat frequency, range/velocity resolution, ULA steering vectors) must be recovered from the old draft and reconciled with current `src/sim/radar_config.py` parameters ($f_c = 77\text{ GHz}$, $B = 1\text{ GHz}$, $T_c = 50\ \mu\text{s}$, 256 samples, 128 chirps, 4 Rx).
- **Experimental Discrepancies:** Five specific experimental claims require honest evidentiary reconciliation:
  1. RadDet dataset split: official 20k/14k/6k partition vs current benchmark summary of 14,001/6,001/20,001 (and 19,998 vs 20,001 bin count math).
  2. YOLOv9-C benchmark claim: 66-epoch full-scale run vs tracked prototype 15-epoch config; comparative benchmark against published Table III (YOLOv9-M) vs exact reproduction.
  3. Synthetic FMCW CNN sample count: 150 generated samples (default utility) vs 32-sample reported experiment.
  4. Clutter attenuation: 12.94 dB total signal power ratio vs pure clutter suppression.
  5. Angle estimation: range-only target association limitations, 180-point search grid spacing vs physical array resolution.
- **RadDet Perception vs Spectrum Sensing:** Terminology must be corrected across all chapters to reflect that RadDet is wideband RF spectrum sensing and modulation classification via time-frequency spectrograms, not automotive physical road scenes.
- **Citation & Bibliography Realignment:** IEEE numerical citations must be sequentially renumbered [1..N] in order of first appearance in the 5-chapter report and synchronized with `docs/app.js`, while legacy citations are separated below `<hr>`.

---

## Requirements

1. **R1 (Evidence Audit & Claim-to-Artifact Mapping)**: Conduct an exhaustive repository audit across source code, Kaggle notebooks/logs, checkpoints, CSV files, and Git commits, producing `.planning/phases/02-github-pages-chapter-by-chapter-content-finalization/02-EVIDENCE-AUDIT.md` that maps every technical claim to its supporting artifact, identifies verified configurations, and details unresolved discrepancies.
   - Current: Claims exist across `docs/index.html` and old drafts with conflicting partition numbers, unverified epoch counts, and ambiguous clutter metrics.
   - Target: A structured audit dossier (`02-EVIDENCE-AUDIT.md`) documenting exact evidence for RadDet splits, YOLOv9-C runs, synthetic CNN samples, clutter attenuation, and AoA association.
   - Acceptance: `02-EVIDENCE-AUDIT.md` exists with dedicated sections for each disputed experiment, classifying each as Verified, Partially Verified, or Proposed/Unverified with explicit file paths.

2. **R2 (FMCW Mathematical Physics & Classical DSP Recovery)**: Recover rigorous mathematical physics derivations from the archived draft and integrate them into Chapter 2 and Chapter 3, using current `src/sim/radar_config.py` values ($f_c = 77\text{ GHz}$, $B = 1\text{ GHz}$, $T_c = 50\ \mu\text{s}$, $\Delta R \approx 0.15\text{ m}$, $\Delta v \approx 0.304\text{ m/s}$, $R_{\max} \approx 38.4\text{ m}$).
   - Current: Active Chapter 2 and 3 omit complete step-by-step dechirp/beat-frequency derivations, or carry forward legacy $58.8\ \mu\text{s}$ chirp duration and $0.258\text{ m/s}$ velocity resolution values.
   - Target: Chapter 2 and 3 contain complete derivations of FMCW chirp generation, round-trip delay, beat frequency, range/velocity resolution, ULA steering vectors, and a classical DSP comparative table (Range FFT, MTI, Doppler FFT, CFAR linear-power statistics, MUSIC/Capon, DBSCAN).
   - Acceptance: KaTeX equations render correctly in `docs/index.html`; numerical parameters match `src/sim/radar_config.py` ($T_c = 50\ \mu\text{s}$, $\Delta v = 0.304\text{ m/s}$); zero references to legacy $58.8\ \mu\text{s}$ parameters in active chapters.

3. **R3 (Experimental Discrepancy Reconciliation & Honest Reporting)**: Revise Chapter 4 to clearly decouple Track I (synthetic 77 GHz FMCW automotive targets) from Track II (RadDet wideband RF spectrum sensing), disclose data split deviations, qualify benchmark comparisons against published RadDet Table III, and acknowledge reproducibility limitations transparently.
   - Current: Track I and Track II results are occasionally juxtaposed without qualification, and unverified 66-epoch full-scale runs are asserted as exact reproductions.
   - Target: Chapter 4 presents verified prototype evidence alongside honestly qualified comparative benchmarks, discloses the 14,001/6,001/20,001 split, clarifies that 12.94 dB measures total average power reduction, and acknowledges AoA range-only association limitations.
   - Acceptance: Chapter 4 explicitly distinguishes Track I from Track II; benchmark is described as comparative rather than exact reproduction; reproducibility limitations are explicitly stated for unverified runs.

4. **R4 (RadDet Terminology & Concept Alignment)**: Correct terminology across all 5 active chapters in `docs/index.html` to consistently describe RadDet as wideband RF radar-spectrum detection and radar-emission modulation classification from time-frequency spectrograms.
   - Current: Misleading statements across multiple chapters imply RadDet contains automotive road scenes with physical cars, pedestrians, or range-azimuth physical point clouds.
   - Target: All descriptions define RadDet as time-frequency RF spectrogram detection, preserving the dual-track structure without conflation.
   - Acceptance: Grep search across active chapters (`#ch1-intro` through `#ch5-conclusion`) reveals zero instances of describing RadDet as physical road scenes or automotive vehicles.

5. **R5 (IEEE Citation & Bibliography Realignment)**: Renumber all citations in the 5-chapter manuscript sequentially [1..N] in order of first appearance, synchronize the tooltip lookup dictionary in `docs/app.js`, and segregate legacy citations into an "Archival Draft References" section below an `<hr>`.
   - Current: Reference numbers are non-sequential in active text, missing keys in tooltip dictionary cause undefined tooltips, and citations from the old draft clutter the bibliography.
   - Target: Citations [1..N] match IEEE order of appearance; `docs/app.js` mirrors the exact IDs; archived draft references reside below `<hr>`.
   - Acceptance: Every citation link in `#ch1-intro` through `#ch5-conclusion` has a matching entry in the primary bibliography; `docs/app.js` tooltip dictionary resolves all active citations; zero broken anchor links.

6. **R6 (GitHub Pages Scope & Deterministic Zero-Regression Gate)**: Confine all changes strictly to GitHub Pages assets (`docs/index.html`, `docs/app.js`) and `.planning/` documentation, preserving the archived 7-chapter draft and ensuring all deterministic tests pass.
   - Current: Deterministic website test suite passes with 20 tests.
   - Target: All modifications execute cleanly without mutating any LaTeX/PDF template files, maintaining 100% test pass rate.
   - Acceptance: `pytest tests/test_academic_website.py tests/test_showcase_website.py` passes; `git status --porcelain templates/BTP_Report_Template_Overleaf/` shows zero modified files; `#ch1-intro-original` remains intact.

---

## Boundaries

**In scope:**
- Staged execution of Phase 2 extension:
  - **Plan 02-08**: Complete repository and artifact audit, synthesis of `02-EVIDENCE-AUDIT.md`, mathematical physics derivations, and discrepancy resolution documentation.
  - **Plan 02-09**: HTML content integration in `docs/index.html`, RadDet terminology rectification, IEEE citation renumbering, `docs/app.js` dictionary synchronization, and deterministic test suite execution.
- Preservation of the archived 7-chapter draft (`#ch1-intro-original` through `#ch7-conclusion`) in `docs/index.html`.
- Creation of `.planning/phases/02-github-pages-chapter-by-chapter-content-finalization/02-EVIDENCE-AUDIT.md`.

**Out of scope:**
- Modifying PDF or LaTeX files in `templates/BTP_Report_Template_Overleaf/` or `build/` — strictly deferred to a subsequent milestone/phase as specified in user instructions.
- Modifying or deleting the archived 7-chapter draft in `docs/index.html`.
- Re-running full-scale 100-epoch training on external Kaggle or cloud GPU clusters during this phase.
- Altering the approved thesis title ("AI Applications in Radar Signal Processing — Towards Resource-Efficient AI-Based Radar Detection for Millimetre-Wave FMCW Systems") or institutional metadata.

---

## Constraints

- **Scope Restriction**: Zero edits to `.tex`, `.bib`, or `.pdf` files in `templates/BTP_Report_Template_Overleaf/`.
- **Physical Grounding**: All FMCW radar parameters must strictly adhere to `src/sim/radar_config.py` ($f_c = 77\text{ GHz}$, $B = 1\text{ GHz}$, $T_c = 50\ \mu\text{s}$, $N_{\text{samples}} = 256$, $N_{\text{chirps}} = 128$, $N_{\text{rx}} = 4$).
- **Test Invariant**: Deterministic test suites (`tests/test_academic_website.py` and `tests/test_showcase_website.py`) must pass in sub-30s with zero failures.
- **Zero Secrets**: No tokens, API keys, or personal credentials committed to version control.

---

## Acceptance Criteria

- [ ] `02-EVIDENCE-AUDIT.md` authored in `.planning/phases/02-.../` covering all 5 disputed experimental areas.
- [ ] Active Chapter 2 and 3 contain complete FMCW mathematical derivations based on $T_c = 50\ \mu\text{s}$ and $f_c = 77\text{ GHz}$.
- [ ] All instances of legacy $58.8\ \mu\text{s}$ chirp duration and $0.258\text{ m/s}$ velocity resolution removed from active chapters.
- [ ] Active Chapter 4 clearly decouples Track I (synthetic FMCW) from Track II (RadDet RF spectrum sensing).
- [ ] RadDet dataset split discrepancy (20k/14k/6k vs 14,001/6,001/20,001 and 19,998 frame math) explicitly disclosed.
- [ ] YOLOv9-C benchmark described as a comparative benchmark against published Table III rather than an exact reproduction.
- [ ] 12.94 dB clutter attenuation accurately defined as total average signal power reduction rather than pure clutter suppression.
- [ ] Range-only target association limitations in MUSIC/Capon AoA explicitly documented.
- [ ] Active citations [1..N] renumbered sequentially in order of appearance in `docs/index.html`.
- [ ] Citation tooltip database in `docs/app.js` synchronized with renumbered active citations.
- [ ] Bibliography contains an `<hr>` separating active citations from legacy archived citations.
- [ ] Archived 7-chapter draft (`#ch1-intro-original` through `#ch7-conclusion`) remains fully preserved.
- [ ] Zero files modified in `templates/BTP_Report_Template_Overleaf/`.
- [ ] `pytest tests/test_academic_website.py tests/test_showcase_website.py` passes 100%.

---

## Edge Coverage

**Coverage:** 6/6 applicable edges resolved · 0 unresolved

| Category | Requirement | Status | Resolution / Reason |
|---|---|---|---|
| Edge Case: Missing Artifacts | R1 | ✅ covered | If an execution log or checkpoint is missing, qualify claim as comparative/historical with explicit reproducibility limitations in `02-EVIDENCE-AUDIT.md`. |
| Edge Case: Parameter Inconsistency | R2 | ✅ covered | Authoritative derivation strictly uses `src/sim/radar_config.py` ($T_c = 50\ \mu\text{s}$, $\Delta v = 0.304\text{ m/s}$, $R_{\max} = 38.4\text{ m}$); idle time distinction noted. |
| Edge Case: Split Count Discrepancy | R3 | ✅ covered | Explicitly disclose both recorded counts (14,001/6,001/20,001) and official paper partitions (20k/14k/6k), documenting the 19,998 vs 20,001 bin math. |
| Adjacency / Empty Input | R4 | ⛔ dismissed | Terminology rectification involves discrete semantic replacements in static HTML sections; empty input cannot occur. |
| Ordering: Citation IDs | R5 | ✅ covered | Active references [1..N] renumbered sequentially by first appearance; legacy references placed below `<hr>` divider with intact anchors. |
| Concurrency / File Scope | R6 | ✅ covered | Staged plan execution (02-08 audit first, 02-09 HTML injection second) ensures clean file scope and zero concurrent race conditions. |

---

## Prohibitions (must-NOT)

**Coverage:** 4/4 applicable prohibitions resolved · 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|---|---|---|---|
| MUST NOT fabricate or invent experimental logs, checkpoints, metrics, or hardware profiles | R1, R3 | resolved | `verification: judgment` (audited against live artifacts in `02-EVIDENCE-AUDIT.md`) |
| MUST NOT modify or commit changes to files in `templates/BTP_Report_Template_Overleaf/` or `build/` | R6 | resolved | `verification: test` (`git status --porcelain templates/BTP_Report_Template_Overleaf/` must be empty) |
| MUST NOT delete or truncate the archived 7-chapter original draft section in `docs/index.html` | R6 | resolved | `verification: test` (`tests/test_academic_website.py` asserts `#ch1-intro-original` exists) |
| MUST NOT claim sub-Rayleigh target resolution or real-time automotive ECU performance without empirical hardware proof | R2, R3 | resolved | `verification: judgment` (textual review of Chapter 2, 4, 5) |

---

## Ambiguity Report

| Dimension | Score | Min | Status | Notes |
|---|---|---|---|---|
| Goal Clarity | 0.90 | 0.75 | ✓ | Clear two-plan staged audit and HTML integration scope. |
| Boundary Clarity | 0.85 | 0.70 | ✓ | Explicitly restricted to GitHub Pages; LaTeX strictly excluded; old draft preserved. |
| Constraint Clarity | 0.80 | 0.65 | ✓ | Grounded in `radar_config.py`, sub-30s test execution, zero secrets. |
| Acceptance Criteria | 0.80 | 0.70 | ✓ | 14 unambiguous pass/fail checklist items. |
| **Ambiguity** | **0.15** | **≤0.20** | ✓ | Gate passed. |

---

## Interview Log

| Round | Perspective | Question summary | Decision locked |
|---|---|---|---|
| 1 | Researcher | How should this comprehensive revision scope be structured within Phase 2? | Staged two-plan structure: Plan 02-08 for repository audit, mathematical recovery, and discrepancy dossier, followed by Plan 02-09 for HTML content injection, bibliography split, and verification. |
| 1 | Researcher | How should unresolved or partially documented experiments be handled? | Qualify claims honestly as comparative benchmarks with explicit reproducibility notes, and document the full audit trail in `02-EVIDENCE-AUDIT.md`. |
| 1 | Researcher | How should the IEEE bibliography and citation popovers be restructured? | Renumber active citations sequentially [1..N] in the 5-chapter report and `docs/app.js` tooltip dictionary, followed by `<hr>` and an "Archival Draft References" section for legacy citations. |
| 2 | Gatekeeper | Ambiguity gate passed (0.15 ≤ 0.20). Proceed to write SPEC.md? | User confirmed proceeding directly to Edge Probe and generating `02-SPEC.md`. |

---

*Phase: 02-github-pages-chapter-by-chapter-content-finalization*  
*Spec created: 2026-11-18*  
*Next step: /gsd-discuss-phase 2 — implementation decisions (how to build what's specified above)*  
