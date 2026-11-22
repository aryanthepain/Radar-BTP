# Plan 02-08 Summary: Forensic Evidence Audit Dossier & Reference Verification

**Phase:** Phase 2: GitHub Pages Chapter-by-Chapter Content Finalization  
**Plan:** 02-08  
**Status:** Completed & Deterministically Verified  

---

### Accomplishments
1. **Authored Comprehensive Forensic Audit Dossier (`02-EVIDENCE-AUDIT.md`):**
   - Established complete 9-section authoritative technical dossier mapping every claim in the BTP report to verified repository artifacts, source code lines, and benchmark checkpoints.
   - Formalized 3-tier evidence taxonomy per D-14: Tier 1 (Verified), Tier 2 (Partially Verified / Comparative), and Tier 3 (Smoke Test / Prototyping).
2. **Recalculated FMCW Physical Radar Mathematical Derivations (D-04, D-05, R2):**
   - Derived step-by-step FMCW radar equations using authoritative constants from `src/sim/radar_config.py:22-69` ($f_c = 77\text{ GHz}$, $B = 1.0\text{ GHz}$, $T_c = 50.0\ \mu\text{s}$, $S = 20\text{ THz/s}$, $\Delta R = 0.15\text{ m}$, $\Delta v = 0.304\text{ m/s}$, $R_{\max} = 38.4\text{ m}$, $v_{\max} = 19.47\text{ m/s}$).
   - Derived ULA steering vector $\mathbf{a}(\theta)$ and established physical $\approx 28.6^\circ$ Rayleigh beamwidth limit for 4-element half-wavelength array, clarifying the $1^\circ$ step size of the 180-bin MUSIC evaluation grid.
   - Documented historical evolution from legacy 58.8 μs sweep to authoritative 50 μs active chirp configuration.
3. **Synthesized 6-Column Classical DSP Baseline Matrix (Table 3.1, D-06):**
   - Detailed operating principles, mathematical formulations, statistical assumptions (noting linear-power exponential noise power statistics $f(x) = \frac{1}{\sigma^2} e^{-x/\sigma^2}$ resulting from Rayleigh complex amplitude envelope), computational complexities, and known failure modes for Range FFT, MTI, Doppler FFT, CFAR, MUSIC/Capon, and DBSCAN.
4. **Reconciled the 5 Disputed Experimental Areas (D-01, D-02, D-03, D-04, D-08, R3):**
   - *Claim 1:* Evaluated 14,001 / 6,001 / 20,001 partition mapped against published 20,000 / 14,000 / 6,000 ICASSP split; derived the exact $20,001 // 6 = 3,333 \times 6 = 19,998$ integer division math in `scripts/build_raddet_notebook.py:721-726`.
   - *Claim 2:* Fully trained 66-epoch YOLOv9-C run (25.30M params, 25.25% mAP50, 19.03% mAP50:95, 892.9 FPS on Tesla T4) framed as comparative benchmark against Lin et al. Table III YOLOv9-M (20.02M params, 25.93% mAP50); demarcated 15-epoch YOLOv8n run as prototype smoke test.
   - *Claim 3:* Audited `02_radar_deep_learning_detection.ipynb` Cell 3, 7, 9 proving 136,041-parameter CNN trained on 32 samples (25 train / 7 val) in 26.89s, framed as lightweight proof-of-concept smoke test.
   - *Claim 4:* Audited `src/dsp/clutter_removal.py:57-67` proving 12.94 dB measures total average signal-power reduction under mean-subtraction.
   - *Claim 5:* Grounded range-only target association limitations and decoupled numerical grid from physical array resolution.
5. **Decoupled Track I and Track II Architecture & RF Spectrum Grounding (R3, R4):**
   - Grounded RadDet classes via `data.yaml:5-16` proving the 11 classes are modulation types (`Rect`, `Barker`, `Frank`, `P1`..`P4`, `Px`, `ZadoffChu`, `LFM`, `FMCW`), not physical road-scene vehicles or pedestrians.
6. **Built Structured Human Confirmation Registry & Defense Triage (D-13, D-15):**
   - Established 4-field table for oral defense preparation and drafted GitHub tracking issue specification.
7. **Assembled Canonical Reference Table & Bijective Renumbering Mapping (D-09, D-10, D-11):**
   - Audited all 32+ literature references, standardizing Skolnik (2001 3rd ed.), RadDet (ICASSP 2025), Richards (2014 2nd ed.), AdaRadar (ICCPS 2023), and RAVEN (KTH 2023).
   - Constructed complete bijective mapping table mapping active citations sequentially `[1..18]` by first appearance and archival references `[19..32]` below `<hr>`.
8. **Authored Wave 0 Test `test_evidence_audit_dossier` in `tests/test_academic_website.py`:**
   - Asserted dossier existence (>5KB), all 9 sections, 3-tier taxonomy, authoritative FMCW parameters, 6-column DSP matrix, 5 reconciled claims, Track I/II decoupling, and citation mappings.
   - Test suite passed in 0.08s (21/21 passed overall).
