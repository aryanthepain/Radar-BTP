# Phase 02: GitHub Pages Chapter-by-Chapter Content Finalization - Context

**Gathered:** 2026-11-18
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase delivers a publication-grade academic and technical revision of the B.Tech Project (BTP-1) report hosted on GitHub Pages (`docs/index.html` and `docs/app.js`).

The revision executes across a staged two-plan sequence:
1. **Plan 02-08:** Comprehensive repository evidence audit, mathematical physics derivation recovery, reference metadata verification, and discrepancy documentation in `.planning/phases/02-github-pages-chapter-by-chapter-content-finalization/02-EVIDENCE-AUDIT.md`.
2. **Plan 02-09:** HTML content integration into `docs/index.html`, RadDet terminology rectification, sequential IEEE citation renumbering [1..N], `docs/app.js` tooltip database synchronization, bibliography `<hr>` archival segregation, and deterministic test suite execution.

All work strictly preserves the archived 7-chapter draft (`#ch1-intro-original` through `#ch7-conclusion`) and makes zero modifications to LaTeX templates in `templates/BTP_Report_Template_Overleaf/`.
</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**6 requirements are locked.** See `02-SPEC.md` for full requirements, boundaries, constraints, and acceptance criteria.

Downstream agents MUST read `02-SPEC.md` before planning or implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Staged execution of Phase 2 extension:
  - Plan 02-08: Complete repository and artifact audit, synthesis of `02-EVIDENCE-AUDIT.md`, mathematical physics derivations, and discrepancy resolution documentation.
  - Plan 02-09: HTML content integration in `docs/index.html`, RadDet terminology rectification, IEEE citation renumbering, `docs/app.js` dictionary synchronization, and deterministic test suite execution.
- Preservation of the archived 7-chapter draft (`#ch1-intro-original` through `#ch7-conclusion`) in `docs/index.html`.
- Creation of `.planning/phases/02-github-pages-chapter-by-chapter-content-finalization/02-EVIDENCE-AUDIT.md`.

**Out of scope (from SPEC.md):**
- Modifying PDF or LaTeX files in `templates/BTP_Report_Template_Overleaf/` or `build/` — strictly deferred to a subsequent milestone/phase.
- Modifying or deleting the archived 7-chapter draft in `docs/index.html`.
- Re-running full-scale 100-epoch training on external Kaggle or cloud GPU clusters during this phase.
- Altering the approved thesis title ("AI Applications in Radar Signal Processing — Towards Resource-Efficient AI-Based Radar Detection for Millimetre-Wave FMCW Systems") or institutional metadata.

</spec_lock>

<decisions>
## Implementation Decisions

### 1. Discrepancy Reconciliation & Experimental Framing (Chapter 4)
- **D-01:** Minimal Disclosure Footnote for RadDet Split — In Chapter 4 (Table 4.1), display the project's evaluated partition numbers (14,001 train / 6,001 val / 20,001 test) and append an explicit disclosure footnote explaining the deviation from the published ICASSP partition (20,000 / 14,000 / 6,000) and the 19,998 frame 6-bin mathematics.
- **D-02:** Smoke Test Demarcation for YOLO Prototype — The 15-epoch YOLOv8n run recorded in prototype configs is treated strictly as an internal smoke test / sanity check; downstream agents must not treat it as a competing benchmark against the 66-epoch run.
- **D-03:** YOLOv9-C Comparative Benchmark Framing — Present the 66-epoch YOLOv9-C run (25.30M params, 25.25% mAP@0.5) as a comparative benchmark against Lin et al.'s published YOLOv9-M Table III results (20.02M params, 25.93% mAP@0.5), noting architectural metric convergence and incorporating the precision-recall and multi-SNR graphs from GitHub Pages.
- **D-04:** Accurate Physical Radar Nomenclature — Define the 12.94 dB clutter attenuation figure directly as total average signal-power reduction across range-Doppler cells under mean-subtraction (rather than pure clutter suppression). Explicitly distinguish the 180-point MUSIC numerical evaluation grid from the 4-element ULA physical beamwidth (~28° Rayleigh limit), documenting range-only association limitations.

### 2. Mathematical Physics Derivations & Parameter Transition (Chapters 2 & 3)
- **D-05:** Silent Purge of Legacy Parameters on GitHub Pages — Author all mathematical derivations in Chapter 2 and Chapter 3 strictly using the authoritative `src/sim/radar_config.py` parameters ($f_c = 77\text{ GHz}$, $B = 1\text{ GHz}$, $T_c = 50\ \mu\text{s}$, $\Delta R \approx 0.15\text{ m}$, $\Delta v \approx 0.304\text{ m/s}$, $R_{\max} \approx 38.4\text{ m}$). Completely excise all legacy 58.8 μs and 0.258 m/s values from active chapters in `docs/index.html`. Document the historical parameter evolution (58.8 μs sweep vs 50 μs active time) in `02-EVIDENCE-AUDIT.md`.
- **D-06:** Comprehensive 6-Column Classical DSP Table — Structure Table 3.1 as a comprehensive synthesis table with 6 columns: Method, Operating Principle, Mathematical Formulation, Statistical Assumptions (e.g., square-law exponential noise power vs Rayleigh amplitude), Computational Complexity, and Known Failure Modes / Limitations.
- **D-07:** Full 7-Axis Literature Review Grounding — Retain the complete 7-axis literature comparison matrix in Chapter 2, strictly using "Not reported" for unmeasured parameters, correctly describing AdaRadar's neural routing (avoiding speculative hardware chirp duration claims), and verifying all primary citations.
- **D-08:** Evidence-Grounded Synthetic CNN Framing — In Plan 02-08, audit the executed notebook / checkpoint to lock the exact training parameters (e.g., 32 vs 150 samples, epochs, loss) and qualify the 136,041-parameter CNN in Chapters 3 & 4 as a lightweight synthetic proof-of-concept, recognizing that smaller runs (e.g. 32 samples) functioned as smoke tests.

### 3. IEEE Citation Renumbering Strategy & Archival Bibliography Separation
- **D-09:** Active [1..N] + Monotonic Archival [N+1..M] below `<hr>` — Active 5-chapter manuscript citations will be sequentially renumbered [1..N] in order of first appearance. Citations unique to the archived 7-chapter draft will be placed below `<hr>` continuing monotonically as [N+1..M], ensuring uniform IEEE numeric styling and zero anchor collisions.
- **D-10:** Comprehensive Tooltip Dictionary in `docs/app.js` — Synchronize `docs/app.js` with all references [1..M], displaying verified popovers with authors, title, venue, year, and clean DOI links (archival entries tagged with an "Archival Reference" badge).
- **D-11:** Canonical Reference Verification Table in `02-EVIDENCE-AUDIT.md` — During Plan 02-08, assemble an authoritative reference table resolving all citation discrepancies (Skolnik edition/year, RadDet ICASSP 2025, RAVEN, AdaRadar, TJ4DRadSet) with verified DOIs/URLs before Plan 02-09 maps them into HTML and JS.
- **D-12:** Granular Individually-Linked Citation Anchors — Render multiple or consecutive in-text citations as discrete anchors (e.g., `<a href="#ref-1">[1]</a>, <a href="#ref-2">[2]</a>`) so each reference independently triggers its specific tooltip popover.

### 4. Evidence Audit Dossier Exposure & Advisor Defense Linkage (Plan 02-08)
- **D-13:** Planning-Internal Dossier & GitHub Issue for Defense Triage — Confine all discrepancy details, audit matrices, and human confirmation lists to `.planning/phases/02-github-pages-chapter-by-chapter-content-finalization/02-EVIDENCE-AUDIT.md`. Create a dedicated GitHub issue to review discrepancies and decide which items are worthy of being incorporated into `docs/ADVISOR-DEFENSE.md`.
- **D-14:** 3-Tier Evidence Taxonomy — Grade all audited experiments in `02-EVIDENCE-AUDIT.md` using:
  1. *Verified:* Complete artifact trail, checkpoints, and execution logs available.
  2. *Partially Verified / Comparative:* Metrics documented in benchmark summaries, but raw execution log or full checkpoint unarchived.
  3. *Smoke Test / Prototyping:* Rapid sanity checks (e.g., 15-epoch YOLOv8n, 32-sample CNN) not intended as primary benchmark claims.
- **D-15:** Structured Human Confirmation Registry — Section 8 of `02-EVIDENCE-AUDIT.md` must maintain a 4-field table for each uncertain item: Why Confirmation is Necessary, Available Evidence, What Remains Uncertain, and Recommended Action, mirrored into the GitHub tracking issue.
- **D-16:** Permanent Invariant Assertions in `tests/test_academic_website.py` — Augment the automated test suite with deterministic checks verifying:
  1. Active citation anchors resolve without broken targets (`#ref-X` exists).
  2. Zero placeholder DOIs exist in HTML or JS.
  3. No legacy 58.8 μs or 0.258 m/s strings appear in active Chapters 1–5.
  4. The 7-chapter archived draft (`#ch1-intro-original`) is preserved intact.
  5. Zero tracked modifications in `templates/BTP_Report_Template_Overleaf/`.

### Agent's Discretion
- Exact layout styling of the `<hr>` bibliography divider, table responsive overflows, and KaTeX mathematical display environments to ensure publication-grade visual rendering.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing:**

### User Instruction & Phase Specification
- `report_content/changes.md` — Authoritative audit prompt and requirement breakdown for comprehensive revision.
- `.planning/phases/02-github-pages-chapter-by-chapter-content-finalization/02-SPEC.md` — Locked requirements, boundaries, constraints, and acceptance criteria for Phase 2 extension.

### Academic Web Portal Files
- `docs/index.html` — Authoritative single-page academic reading portal containing both active 5 chapters and archived 7 chapters.
- `docs/app.js` — Client-side reading progress, sidebar chapter navigation, and citation tooltip dictionary.
- `docs/styles.css` — High-contrast academic paper styling, typography, and KaTeX equation formatting.

### Radar Simulation & DSP Ground Truth
- `src/sim/radar_config.py` — Authoritative 77 GHz FMCW radar parameters ($f_c = 77\text{ GHz}$, $B = 1\text{ GHz}$, $T_c = 50\ \mu\text{s}$, $N_{\text{samples}} = 256$, $N_{\text{chirps}} = 128$, $N_{\text{rx}} = 4$).
- `src/sim/radar_sim.py` — FMCW chirp synthesis, target kinematics, and thermal noise generation.
- `src/dsp/clutter_removal.py` — Clutter suppression implementations (mean subtraction and MTI canceller).
- `src/dsp/aoa_estimation.py` — MUSIC and Capon/MVDR spatial pseudospectrum angle estimation over 181 angular bins.
- `src/dsp/cfar_detector.py` — 2D CA-CFAR, OS-CFAR, GOCA-CFAR, and SOCA-CFAR detection routines.

### Repository Verification Gates
- `tests/test_academic_website.py` — Deterministic test suite validating HTML structure, KaTeX rendering, and navigation.
- `tests/test_showcase_website.py` — Deterministic test suite for showcase website assets.
- `scripts/verify.ps1` — Universal repository verification harness.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `docs/app.js` tooltip engine: Existing DOM event listeners on `a[href^="#ref-"]` already handle hover states; populating the citation metadata object updates tooltips immediately.
- `tests/test_academic_website.py`: Built using `BeautifulSoup4` and `pytest`, allowing fast sub-second DOM tree parsing and assertion checking.

### Established Patterns
- KaTeX Math Rendering: Inline math formatted as `<span class="math inline">\( ... \)</span>` and display equations formatted as `<div class="math display">\[ ... \]</div>`.
- Academic Section Anchors: Chapters keyed as `#ch1-intro` through `#ch5-conclusion`, with archived original draft sections keyed as `#ch1-intro-original` through `#ch7-conclusion`.

### Integration Points
- `docs/index.html` `div.references-list`: Ordered list `<ol>` of bibliography items with IDs `ref-1`, `ref-2`, etc.
- Invariant tests in `tests/test_academic_website.py`: Executed on every `verify.ps1` pass.
</code_context>

<specifics>
## Specific Ideas
- The 15-epoch YOLOv8n run is an internal smoke test; do not treat it as a competing benchmark against the 66-epoch YOLOv9-C run.
- Do not let smoke tests hinder forward progress or confuse the primary benchmark claims.
- Create a GitHub issue on GitHub to triage discrepancies and evaluate which ones should be mirrored into `docs/ADVISOR-DEFENSE.md`.
</specifics>

<deferred>
## Deferred Ideas
- Evaluation of which audited discrepancies in `02-EVIDENCE-AUDIT.md` should be formally added as Q&As to `docs/ADVISOR-DEFENSE.md` — tracked via a dedicated GitHub issue.
- Generation and Overleaf synchronization of the final LaTeX/PDF report (`templates/BTP_Report_Template_Overleaf/report.tex`) — strictly deferred until GitHub Pages content is finalized.
</deferred>

---

*Phase: 02-GitHub Pages Chapter-by-Chapter Content Finalization*
*Context gathered: 2026-11-18*
