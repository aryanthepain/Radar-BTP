# WORKING.md — Active Sprint & Context Scratchpad

## Current Objective: Comprehensive Report Revision & Academic Polish

### VERBATIM USER REQUEST (Recorded for Verification Gate)

```text
/gsd-verify-work 2.
remove this "Index Terms: 77 GHz FMCW Radar, Resource-Efficient AI, Radar Signal Processing, Deep Spectrum Detection, RadDet Benchmark, YOLOv9-C, CPU Inference, Constant False Alarm Rate (CFAR), Edge Computing."
move the old report to a new page and add the link to go to the old report if need be. keep the archived references there as well.
in bibliography add 19 and 20, 26, 27, 30, 31 as reference as well. mention 19 and 20, 26, 27, as reference in figure 5.1 in repective locations.

i have made some changes myself in the content.
do not have these scrollbars for formulae as given in the picture.

also in a side chat /add-question what is the stuff in chapter 2 mean. and new question for stuff in table 3.1. new question for this formula X∈C N rx ×N chirp ×N sample

provide a reference to karlssons thesis wherever some topics need to be explained.
Also please make sure that references numbers Are proper Because there are many places where references are not properly matched With what Point to. For example the trans rAd And carrada datasets Are mentioned in chapter two But are not properly linked up. adaradar and raven are not linked up properly as well. you will need to check all the different references that are there. spin up a subagent to check each and every reference and fix it if required.
in 3.1 mention that the synthetic radar was created based on the matlab radar designer app and also rference it.

remove the file names from codes -> src/dsp/range_processing.py
add codes to other section of 3.2.2 as well.
change the mermaid diagrams for teh flow in chapter 3 to be more presentable and to be suitable for the final a4 eport that we are going to use. these flows will be on one side of the column hence they should be easily readable fro there as well. you can ask me anything if any part is ambiguous.

no need for this Code Listing 3.3: Grayscale Spectrogram Loading and Normalisation

formulae like this C={Rect, Barker, Frank, P1, P2, P3, P4, Px, ZadoffChu, LFM, FMCW} are taking up the whole width when they only need to be in one column. this is seen all across the webpage. spin up a subagent tocheck each of teh formula. \Delta R pprox 0.1499\text{ m} this formula is nt showing properly in chapter 4.
table 3.2 and 3.3  can be in one column instead of fulll width.

Code Listing 4.1: Calculation of Range and Velocity Errors from Matched CFAR Detections is unnnecessary
table 4.4 is unnecessary explain using the graph only. there must be A better graph that might be present That corresponds to the whole Training process instead of this smoke one In figure 4.6 a.

The changes I'm telling needs to be changed but also the text around it might need to be changed as well in order to Properly Change the things.

*Partition & Chunking Disclosure Note: The evaluated split (14,001 train / 6,001 val / 20,001 test) reflects the directory structure in the Kaggle benchmark distribution, which differs from the official 20,000 / 14,000 / 6,000 partition in Huang et al. In the multi-SNR evaluation across 6 discrete SNR tiers, integer division (20,001//6=3,333) evaluated 6×3,333=19,998 frames, leaving exactly 3 unassigned residual frames. The 15-epoch YOLOv8n run is demarcated strictly as an internal prototype smoke test. remov this note please in 4.3.2. in table 4.5 no need to mention the small run that is just smoke test. remove from surrounding as well.
write down this whole prompt as it is somewhere So Things are not missed And are later verified Against the original prompt itself instead of Some context deep down.

we can remove table 5.2 and use figure 5.1 instead to propose the roadmap.

remove this  Laboratory & Hardware Confirmation Protocol
remove mention of (ONNX Runtime, OpenVINO) from everywhere.

remove this BTP-1 Thesis Portal · Autumn 2026
KaTeX: Offline (20 Fonts)
Verified: ICASSP Table III

Course
DA4098P BTP Project I (Autumn 2026) -> DA4098P BTP Project I
```

### Action Checklist Derived from User Prompt:

- [x] 0. Prompt saved verbatim in `WORKING.md` (Done).
- [x] 1. Preserve user changes in `docs/index.html` (check git diff before editing).
- [x] 2. Remove "Index Terms: 77 GHz FMCW Radar, Resource-Efficient AI..." div completely.
- [x] 3. Move old 7-chapter report and archived references to `docs/archived-report.html`. Add clean reciprocal links between `index.html` and `archived-report.html`.
- [x] 4. Fix formulas with horizontal scrollbars (split long side-by-side equations, e.g., $\Delta R$, $\Delta v$, $R_{\max}$, $v_{\max}$ so they wrap nicely within one column without scrollbars).
- [x] 5. Fix full-width formulas across the page that should be single-column (e.g., $C=\{\text{Rect}, \dots\}$).
- [x] 6. Fix `\Delta R pprox 0.1499\text{ m}` syntax error in Chapter 4 ($\Delta R \approx 0.15\text{ m}$).
- [x] 7. Tables 3.2 and 3.3 moved to single column instead of full width.
- [x] 8. Remove file path headers from code listings (e.g., `src/dsp/range_processing.py`).
- [x] 9. Remove Code Listing 3.3 (Grayscale Spectrogram Loading and Normalisation) and adjust surrounding text.
- [x] 10. Add Python code snippets to other subsections of 3.2.2 (e.g., Doppler processing, CFAR, AoA, DBSCAN).
- [x] 11. Refactor Chapter 3 Mermaid flowcharts to be vertical / single-column presentable, matching A4 column layout.
- [x] 12. Mention in 3.1 that the synthetic radar was modeled on the MATLAB Radar Designer App and add citation to it.
- [x] 13. Remove Code Listing 4.1 (Calculation of Range and Velocity Errors) and adjust surrounding text.
- [x] 14. Remove Table 4.4 and explain using graph only; replace Figure 4.6 (a) smoke run with a full training process curve graph if available (or high-res full curve).
- [x] 15. Remove the Partition & Chunking Disclosure Note in 4.3.2; remove the 15-epoch smoke test from Table 4.5 and surrounding text.
- [x] 16. Remove Table 5.2 and use Figure 5.1 to present roadmap.
- [x] 17. Remove "Laboratory & Hardware Confirmation Protocol".
- [x] 18. Remove mentions of "(ONNX Runtime, OpenVINO)" from everywhere.
- [x] 19. Header/Hero cleanups:
  - Remove "BTP-1 Thesis Portal · Autumn 2026", "KaTeX: Offline (20 Fonts)", "Verified: ICASSP Table III".
  - Change "DA4098P BTP Project I (Autumn 2026)" to "DA4098P BTP Project I".
- [x] 20. Reference & Bibliography Audit:
  - Add references 19, 20, 26, 27, 30, 31 to bibliography.
  - Mention 19, 20, 26, 27 in Figure 5.1 in respective locations.
  - Provide citations to Karlsson's PhD thesis wherever topics need explanation.
  - Fix dataset citations: TransRAD, CARRADA, AdaRadar, RAVEN, etc., verifying every reference mapping in both `index.html` and `app.js`.
- [x] 21. Draft and formulate the 3 Advisor Defense Focus Questions in chat under `/add-question`:
  - Q1: What does the stuff in Chapter 2 mean?
  - Q2: Explanation of Table 3.1 parameters & equations.
  - Q3: Explanation of tensor formula $X \in \mathbb{C}^{N_{rx} \times N_{chirp} \times N_{sample}}$.

---

- **Project**: Radar DSP & AI Detection Testbench (BTP)
- **Active Phase**: Phase 2 Complete (Merged into `main` via PR #24; GitHub Pages live from `main`)
- **Active Branch**: `main` (clean, fully synced with `origin/main`)
- **Status**: Phase 2 fully merged, GitHub Issue #21 closed, GitHub Pages deployment run #44406734785 succeeded on `main`. 60/60 deterministic tests passing at 97.35% coverage.

---

## Grounded Research Assets & Citations

1. **Thesis in Workspace**:
   - `FULLTEXT01_AI_radar.pdf` (_"Radar Signal Processing using Artificial Neural Networks"_, Alexander Karlsson, PhD Thesis, KTH Royal Institute of Technology & Saab Surveillance, 2023, 253 pages).
   - Core chapters incorporated: FMCW & Saab SIRS 1600 radar parameters (Ch 2), Stepped-frequency pulse compression CNN (Ch 4), Track-Before-Detect (TBD) with max-channel CNN + polynomial MLP (Ch 5), Drone vs bird/human micro-Doppler classification with synthetic blade modeling & sparse autoencoder QDA (Ch 6), Low-angle naval multipath phase difference estimation & dual Kalman filter tracking (Ch 7).
2. **DRDO Survey in Workspace**:
   - `Artificial_Intelligence_based_Radar_Technology_Current_Advancements_Future_Directions_and_Challenges.pdf` (Dr. Tapas Kumar Pal, Scientist, RCI DRDO, IEEE SPACE 2025).
   - Core concepts incorporated: Complete radar range equation with system losses, GAN-based adaptive clutter suppression, RL adaptive beamforming with DQN, INT8 edge quantization formula, and XAI gradient saliency maps.
3. **ICASSP 2025 Benchmark in Workspace**:
   - `RadDet_A_Wideband_Dataset_for_Real-Time_Radar_Spectrum_Detection.pdf` (Zi Huang et al., QUT & Revolution Aerospace, IEEE ICASSP 2025, arXiv:2501.10407).
   - Core empirical data incorporated: Table I signal parameters, Table II variants, Table III reproduction across 40,003 frames, 11 classes, 6 SNR levels down to -20 dB, YOLOv3/v6/v9/RT-DETR latency and mAP trade-offs.
4. **Online Literature SOTA (2024–2026)**:
   - _TransRAD_ (IEEE Trans. Radar Systems, 2025): Retentive Vision Transformer with Manhattan Self-Attention for dense RAD tensors.
   - _E-RODNet_ (IEEE Sensors Journal, 2024): Embedded lightweight single-stage radar object detector.
   - _RadarMOTR_ (IEEE RADAR, 2024): Direct Transformer-based tracking on Range-Doppler maps.
   - _Physics-Informed Super-Resolution_ (L-FISTA, CVPR/IEEE 2024–2025): Deep unrolling deconvolution breaking the physical Rayleigh limit without scaling physical antenna aperture.
5. **IIT Guwahati Institutional Reference Templates**:
   - `templates/230122021@BTP-1 Signed.pdf` (24 pages, Jinay Mehta, Nov 2026).
   - `templates/BTP_2026_27_RajNandiniSaanvi.pdf` (58 pages, Raj Nandani & Saanvi Goel, Nov 2026).

---

## Acceptance Criteria

- [x] 1. Dedicated phase branch created: `gsd/phase-01.2.2-btp-thesis-report-academic-showcase`.
- [x] 2. `ROADMAP.md` and `state.json` synchronized with Phase 01.2.2 and 3-plan roadmap.
- [x] 3. Templates in `templates/` inspected and extracted via `read_file`.
- [x] 4. Comprehensive research dossier authored in `.planning/phases/01.2.2-.../01.2.2-RESEARCH.md` and augmented with web SOTA + Karlsson PhD thesis + DRDO survey + ICASSP RadDet paper.
- [x] 5. Professor focus questions thoroughly investigated and answered with mathematical & empirical rigor.
- [x] 6. 1-Year timeline and Mermaid Gantt chart created spanning BTP-1 (completed) and BTP-2 (planned).
- [x] 7. Phase 01.2.2 Plan 01 executed: Comprehensive academic literature synthesis, 7-axis research-gap matrix, mathematical formulation of 5 candidate methodologies (Primary: Methods 1, 2, 3; Exploratory: Methods 4, 5), dual constrained/Pareto optimization framework, and 6 supervisor defense questions authored in `01.2.2-RESEARCH-SYNTHESIS.md` (545 lines).
- [x] 8. Execute Phase 01.2.2 Plan 02: Conduct Socratic grilling with Aryan Sandeep Gupta (230150003), document developer experience, 3 debugging case studies, domain gap analysis, full 1-year Gantt roadmap (Aug 2026 – May 2027), and Phase 01.2.3 figure generation specification in `01.2.2-BTP-EXPERIENCE.md` (268 lines).
- [x] 9. Execute Phase 01.2.2 Plan 03: Rework GitHub Pages website into academic manuscript reader (two-column CSS layout, offline vendored KaTeX with 20 fonts, 30 IEEE interactive citations in `app.js`, scroll-spy, reading progress bar, Wave 0 test suite in `tests/test_academic_website.py`, all deterministic gates passing).
- [x] 10. Execute Phase 01.2.2 Plan 04: Author and integrate complete BTP-1 Thesis Portal (~20-page equivalent) into `docs/index.html` with Chapters 1–7, 6 Advisor Defense Callout cards, Table III benchmark reproduction, 7-axis Research-Gap Matrix, 1-year Gantt & Risk Assessment, and 30 IEEE citations. All deterministic gates green (38/38 tests passing).
- [x] 11. Execute Phase 01.2.2 Plan 05: Refine publication-grade academic thesis portal (`docs/index.html`) incorporating D-11 through D-18 (official IIT Guwahati hierarchy, clean print-like layout without progress bar, 5 interactive IDE code drawers, strict two-part problem partition in Chapters 4 & 5, multi-stage latency waterfall timing budget table, CPU-first experimental protocol with zero fabricated metrics, academic curriculum & defense date, and deprecation of compiler script). All 13 portal tests and 44 deterministic testbench gates passing 100% green.
- [x] 12. Modularize Advisor Defense Cards: Commented out all 6 Advisor Defense cards in `docs/index.html` with explicit `style="display: none;"` (enabling effortless manual toggling whenever desired) and extracted the complete unabridged mathematical proofs and physical defenses into `docs/ADVISOR-DEFENSE.md` and `01.2.2-ADVISOR-DEFENSE.md`. All 44 deterministic tests green.
- [x] 13. Mobile Drawer & Lightbox Zoom Polish: Fixed off-canvas navigation drawer opening synchronization on mobile viewports (`docs/app.js` and `docs/styles.css`), resolved zoomable image selector matching all 20 figures, added in-modal tap-to-magnify (`.zoomed` scaling with smooth pan scrolling), centered mobile lightbox close button (`#lightbox-close`), collapsed inline multi-column grids on narrow screens, and bumped asset cache-busters to `?v=1.2.1`. All 63 deterministic tests passing at 97.35% coverage.
