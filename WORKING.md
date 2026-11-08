# WORKING.md — Active Sprint & Context Scratchpad

## Current Objective

- **Project**: Radar DSP & AI Detection Testbench (BTP)
- **Active Phase**: Phase 01.2.2: Comprehensive BTP Thesis Report & Academic Publication Showcase Website
- **Active Branch**: `gsd/phase-01.2.2-btp-thesis-report-academic-showcase`
- **Status**: Research Dossier comprehensively expanded with live IEEE 2024–2026 web research, Alexander Karlsson's Saab/KTH 2023 PhD thesis, Dr. Tapas Kumar Pal's DRDO 2025 survey, and Zi Huang et al. ICASSP 2025 RadDet benchmark (`.planning/phases/01.2.2-comprehensive-btp-thesis-report-academic-publication-showcas/01.2.2-RESEARCH.md`).
- **Next Step**: Conduct the interactive discussion-based grilling sessions on the report chapters and lock in content decisions with the user (Plan 01.2.2-02), then proceed to draft the formal ~24-page IIT Guwahati BTP-1 report and publication website.

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
- [ ] 7. In new session: Execute interactive discussion grilling on report sections (Plan 01.2.2-02).
- [ ] 8. Generate complete ~20-24 page BTP report text and figures.
- [ ] 9. Rework GitHub Pages website into academic manuscript reader (Plan 01.2.2-03).
