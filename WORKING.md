# WORKING.md — Active Sprint & Context Scratchpad

## Current Objective

- **Project**: Radar DSP & AI Detection Testbench (BTP)
- **Active Phase**: Phase 01.2.2: Comprehensive BTP Thesis Report & Academic Publication Showcase Website
- **Active Branch**: `gsd/phase-01.2.2-btp-thesis-report-academic-showcase`
- **Status**: Research Dossier & Structural Blueprint Complete (`.planning/phases/01.2.2-comprehensive-btp-thesis-report-academic-publication-showcas/01.2.2-RESEARCH.md`).
- **Next Step**: When resuming in a new session, begin the interactive discussion-based grilling sessions on the report sections to lock in content choices, then proceed to generate the formal report and website.

---

## Hand-Off Context for New Session

The user is AFK and requested to ready everything up, keep all context intact, and note that the actual interactive discussion will start in a **new session**.

### 1. Key Inputs & Documents Grounded
1. **IIT Guwahati BTP Reference Templates**:
   - `templates/230122021@BTP-1 Signed.pdf`: 24-page report (Jinay Mehta, Nov 2026). Established standard: Front matter (Cover with IITG logo, Certificate, 1.5-page structured Abstract, TOC), 5 core chapters, Appendix, References (IEEE), Acknowledgment, Declaration, Plagiarism report.
   - `templates/BTP_2026_27_RajNandiniSaanvi.pdf`: 58-page report (Raj Nandani & Saanvi Goel, Nov 2026). Rigorous mathematical style, numbered equations, comparative baseline vs refined tables, vector figures, Phase 1 vs Phase 2 division.
2. **Supervising Professor's Mandate & Key Questions**:
   - **Guiding Principle**: *"Do one thing in a very detailed way instead of doing multiple things."*
     - **Chosen Core Focus**: Deep 2.5D Range-Azimuth-Doppler spectrum detection under adverse SNR (-20 to +20 dB) for 77 GHz FMCW radar.
   - **Value Addition of AI**: Bypasses heuristic CFAR in heterogeneous clutter, breaks Rayleigh resolution limits, unites detection and semantic classification, and achieves deterministic 1.12 ms latency.
   - **Close Targets**: Rayleigh limits ($\Delta R = c/2B$, $\Delta \theta \approx \lambda / D \cos\theta$). Why FFT/CFAR/MUSIC merge or degrade, and how deep convolutional receptive fields disentangle sub-bin phase signatures.
   - **Compute vs Latency**: FLOPs/latency comparison between classical DSP (2D FFT + CFAR + MUSIC + DBSCAN) and deep learning (YOLOv9-C at 893 FPS).
   - **Realistic Data**: Review of nuScenes, CARRADA, TJ4D, and deep dive into the ICASSP 2025 RadDet benchmark (40,003 frames, 11 classes, multi-SNR).
   - **Raw Data Inversion**: Trade-offs between Level 0 raw ADC cubes vs Level 1/2 Range-Doppler/RAD tensors; why hybrid FFT front-end + deep learning back-end is optimal.
   - **Utilities**: Autonomous vehicle perception in zero-visibility weather, pedestrian micro-Doppler classification; low-RCS drone swarm detection in defense/EW.
3. **Report Structure (~20-24 pages)**:
   - Cover, Certificate, Abstract, TOC / LOF / LOT, Ch 1 (Intro & SOTA), Ch 2 (Problem Statement & Subproblems), Ch 3 (Methodology), Ch 4 (Implementation), Ch 5 (Results & Discussion), Ch 6 (1-Year Timeline & Gantt Chart), Ch 7 (Conclusion & Future Work), References (IEEE), Appendix, Declarations.
4. **Three-Plan Breakdown**:
   - **Plan 01.2.2-01**: Research, Template Guidelines, Chapter Blueprint & Figure Mapping.
   - **Plan 01.2.2-02**: Discussion-Based Content Grilling (section by section).
   - **Plan 01.2.2-03**: Academic GitHub Pages Website Rework (Distill/arXiv style reader for professor review).

---

## Acceptance Criteria

- [x] 1. Dedicated phase branch created: `gsd/phase-01.2.2-btp-thesis-report-academic-showcase`.
- [x] 2. `ROADMAP.md` and `state.json` synchronized with Phase 01.2.2 and 3-plan roadmap.
- [x] 3. Templates in `templates/` inspected and extracted via `read_file`.
- [x] 4. Comprehensive research dossier authored in `.planning/phases/01.2.2-.../01.2.2-RESEARCH.md`.
- [x] 5. Professor focus questions thoroughly investigated and answered with mathematical & empirical rigor.
- [x] 6. 1-Year timeline and Mermaid Gantt chart created spanning BTP-1 (completed) and BTP-2 (planned).
- [ ] 7. In new session: Execute interactive discussion grilling on report sections (Plan 01.2.2-02).
- [ ] 8. Generate complete ~20-page BTP report text and figures.
- [ ] 9. Rework GitHub Pages website into academic manuscript reader (Plan 01.2.2-03).
