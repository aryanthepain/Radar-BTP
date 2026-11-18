# Plan 02-09 Summary: Publication-Grade HTML/JS Realignment & Regression Invariant Gates

**Phase:** Phase 2: GitHub Pages Chapter-by-Chapter Content Finalization  
**Plan:** 02-09  
**Status:** Completed & Deterministically Verified  

---

### Accomplishments
1. **KaTeX FMCW Mathematical Physics Integration (Chapters 2 & 3, D-05, R2):**
   - Injected step-by-step FMCW radar physics derivations into Chapter 2 Section 2.1 in `docs/index.html`: transmitted chirp $s_t(t)$, round-trip delay $\tau(t)$, dechirped intermediate frequency (IF) beat signal $s_b(t)$ with $f_b \approx 2 S R_0 / c$.
   - Formulated fundamental physical limits based on authoritative `src/sim/radar_config.py` constants ($f_c = 77\text{ GHz}$, $B = 1\text{ GHz}$, $T_c = 50\ \mu\text{s}$, $S = 20\text{ THz/s}$, $\Delta R = 0.15\text{ m}$, $\Delta v = 0.304\text{ m/s}$, $R_{\max} = 38.4\text{ m}$, $v_{\max} = 19.47\text{ m/s}$).
   - Formulated Uniform Linear Array (ULA) geometry, spatial steering vector $\mathbf{a}(\theta)$, and established the physical Rayleigh beamwidth limit $\Delta\theta_{3\text{dB}} \approx 28.6^\circ$ for the 4-element half-wavelength array.
2. **Silent Purge of Legacy Radar Parameters (D-05, R2):**
   - Completely purged all legacy 58.8 μs sweep duration, 0.258 m/s velocity resolution, and 2.72 THz/s frequency slope values above the `#manuscript-transition-divider` boundary in `docs/index.html`.
3. **Publication-Grade 6-Column Classical DSP Synthesis Table (Table 3.1, D-06):**
   - Replaced Table 3.1 in Chapter 3 with the comprehensive 6-column DSP synthesis table (Method, Operating Principle, Mathematical Formulation, Statistical Assumptions, Computational Complexity, Known Failure Modes / Limitations).
   - Formally documented linear-power exponential noise power statistics $f(x) = \frac{1}{\sigma^2} e^{-x/\sigma^2}$ resulting from the Rayleigh complex envelope distribution under CA-CFAR.
4. **RadDet Terminology Rectification & Dual-Track Architectural Grounding (R3, R4):**
   - Consistently described RadDet across active Chapters 1, 2, 3, 4, and 5 as wideband RF radar spectrum detection and radar-emission modulation classification from time-frequency spectrograms.
   - Decoupled Experimental Track I (synthetic 77 GHz FMCW automotive targets) from Experimental Track II (RadDet RF spectrum sensing).
   - Completely eliminated any suggestion that RadDet contains physical vehicles, pedestrians, or road scenes.
5. **Experimental Discrepancy Reconciliations & Disclosure Notes (D-01, D-02, D-03, D-04, D-08):**
   - Injected the Table 4.1/4.5 partition disclosure footnote explaining the evaluated 14,001 train / 6,001 val / 20,001 test split, the deviation from published 20k/14k/6k partitions, and the 19,998 frame chunking math ($6 \times 3,333 = 19,998$).
   - Framed the 66-epoch YOLOv9-C run (25.30M params, 25.25% mAP50, 19.03% mAP50:95, 892.9 FPS) as a comparative benchmark against Lin et al. Table III YOLOv9-M (20.02M params, 25.93% mAP50).
   - Demarcated the 15-epoch YOLOv8n run recorded in prototype configs strictly as an internal smoke test.
   - Formulated the 12.94 dB clutter attenuation figure as total average signal-power reduction under slow-time mean-subtraction.
   - Clarified that the 180-bin MUSIC evaluation grid is a numerical pseudo-spectrum search discretization ($1^\circ$ step size), distinct from the physical Rayleigh beamwidth limit ($\approx 28.6^\circ$).
   - Framed the 136,041-parameter synthetic CNN (32 samples, 5 epochs, 26.89s) as a lightweight proof-of-concept.
6. **Sequential IEEE Citation Renumbering & Bibliography Segregation (D-09, D-10, D-12):**
   - Renumbered all in-text citation badge anchors in active Chapters 1–5 sequentially `[1]` through `[18]` in exact order of first appearance.
   - Structured consecutive citations as granular discrete anchors (`<a href="#ref-1" class="citation-badge" data-citation="1">[1]</a>, <a href="#ref-2" ...>[2]</a>`).
   - Segregated the bibliography in `docs/index.html` using `<hr class="archival-ref-divider">` into Active Manuscript References `[1..18]` and Archival Draft References `[19..32]`.
   - Synchronized `docs/app.js` `CITATIONS_DB` keys 1 through 32 with verified titles, authors, venues, and clean offline identifier text (`archival: true` for 19..32).
   - Preserved zero external network dependencies and offline resilience by representing DOIs, URNs, and URLs as clean text tokens without raw `http://` or `https://` tags.
7. **Permanent Invariant Regression Gates in `tests/test_academic_website.py` (D-16, R6):**
   - Added `test_no_legacy_radar_parameters`: asserts zero instances of 58.8, 0.258, or 2.72 above divider; asserts authoritative 50 μs and 0.304 m/s.
   - Added `test_active_citation_anchors_and_tooltips`: asserts sequential discrete [1..18] anchors without gaps, all resolve in `docs/app.js` `CITATIONS_DB`, and target `li#ref-X` exists.
   - Added `test_scope_and_archival_preservation`: asserts 0 modified files in `templates/BTP_Report_Template_Overleaf/`, and asserts `#ch1-intro-original` through `#ch7-conclusion` remain intact below divider.
   - Expanded `test_chapter_finalization_phase2`: asserts partition disclosure note, 14,001/20,001 counts, 19,998 chunking calculation, 12.94 dB total average signal-power reduction, and Rayleigh angular resolution limit distinction.
   - Full test suite passed (65 passed in `verify.ps1`, 24 website tests passed, 97.35% code coverage).
