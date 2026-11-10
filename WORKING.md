# WORKING.md — Active Sprint & Context Scratchpad

## Current Objective

- **Project**: Radar DSP & AI Detection Testbench (BTP)
- **Active Phase**: Phase 1.3: High-Coverage Deterministic Unit & Integration Testing
- **Active Branch**: `feat/phase-1.3-high-coverage-deterministic-testing`
- **Status**: Phase 01.2.2 merged to `main` (PR #14). Initialized Phase 1.3 targeting $\ge 90\%$ test coverage across `src/` (baseline is 74%).
- **Next Step**: Author Phase 1.3 Plans (`01.3-01`, `01.3-02`, `01.3-03`) and `01.3-VALIDATION.md`.

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
