# Radar-BTP: FMCW Radar Signal Processing & Deep Learning Perception

## What This Is

An exploratory radar perception framework developed for an undergraduate thesis (BTP). It integrates high-fidelity 77 GHz FMCW radar waveform simulation, classical radar signal processing primitives (Range/Doppler FFT, MTI, 2D CFAR, MUSIC AoA, DBSCAN clustering), and deep learning Range-Doppler object detection. It is designed to be cleanly compartmentalized and easily presentable to the thesis advisor/professor before finalizing the formal BTP problem statement.

## Core Value

Modular, decoupled radar perception enabling multi-level data ingestion (raw ADC cubes, Range-Doppler tensors, or point cloud dataframes) and transparent academic presentation of radar signal processing.

## Requirements

### Validated

- ✓ 77 GHz FMCW baseband radar signal simulator with kinematics, micro-Doppler pedestrian modulation, ground clutter, and AWGN noise (`src/sim/`) — existing
- ✓ 1D Fast-Time Range FFT processing with Hann windowing (`src/dsp/range_processing.py`) — existing
- ✓ Slow-time Moving Target Indication (MTI) clutter suppression filters (`src/dsp/clutter_removal.py`) — existing
- ✓ 2D Slow-Time Doppler FFT processing with `fftshift` and STFT micro-Doppler spectrogram computation (`src/dsp/doppler_processing.py`) — existing
- ✓ 2D CA-CFAR and OS-CFAR adaptive threshold detection with peak extraction (`src/dsp/cfar_detector.py`) — existing
- ✓ Subspace MUSIC and Capon MVDR spatial angle-of-arrival (AoA) estimation across antenna arrays (`src/dsp/aoa_estimation.py`) — existing
- ✓ DBSCAN spatial clustering of polar detections into Cartesian object tracks (`src/dsp/clustering.py`) — existing
- ✓ Multi-task convolutional neural network (`RadarObjectDetectorCNN`) for heatmap and bounding box prediction (`src/models/`) — existing
- ✓ Deterministic test verification suite and end-to-end pipeline testbench (`scripts/run_radar_pipeline.py`, `tests/`) — existing
- ✓ Compartmentalized Jupyter Walkthroughs & Mermaid System Architecture (Phase 1 / Issue #4 closed)
- ✓ RadDet ICASSP 2025 Dataset Integration & Prototype (Phase 1.1)
- ✓ Full-Scale RadDet Benchmark on Kaggle GPU (Phase 1.2)
- ✓ Interactive Research Showcase & Presentation Website (Phase 01.2.1)
- ✓ Comprehensive BTP Thesis Report & Academic Publication Showcase Website in `docs/` (Phase 01.2.2)
- ✓ High-Coverage Deterministic Unit & Integration Testing achieving >=90% coverage with `pytest-cov` (Phase 1.3)

### Active

All exploratory thesis preparation phases are 100% complete and verified. Follow-up features are tracked as discrete GitHub issues:
- **Decoupled Data Ingestion**: Tracked in Issues [#17](https://github.com/aryanthepain/Radar-BTP/issues/17) and [#3](https://github.com/aryanthepain/Radar-BTP/issues/3).
- **Pipeline Integration & Verification**: Tracked in Issues [#18](https://github.com/aryanthepain/Radar-BTP/issues/18) and [#19](https://github.com/aryanthepain/Radar-BTP/issues/19).
- **Documentation Portal Enhancements**: Tracked in Issues [#20](https://github.com/aryanthepain/Radar-BTP/issues/20), [#21](https://github.com/aryanthepain/Radar-BTP/issues/21), and [#22](https://github.com/aryanthepain/Radar-BTP/issues/22).

### Out of Scope

- Full RadDet / CARRADA large-scale multi-gigabyte training pipeline (deferred to subsequent milestone after professor delivers formal problem statement).
- Real-time SDR hardware driver interfacing (deferred to future hardware phase).
- Web application / dashboard UI (rejected in favor of keeping existing notebooks clean and directly presentable).

## Context

- Project is in the exploratory phase of an undergraduate Bachelor Thesis Project (BTP).
- The student will present this exploratory foundation to their supervising professor, who will subsequently define the formal thesis problem statement.
- Linked GitHub Issues:
  - Closes #3: "make it so that we can directly put a df data (or some other variable). it does not depend on where the data comes from."
  - Closes #4: "make things easily presentable and compartmentalise so that if we have to show to professors then it is easy"

## Constraints

- **Language & Runtime**: Python 3.12+ (NumPy, SciPy, PyTorch 2.x, Matplotlib, Pandas, Scikit-Learn).
- **Radar Equation Standards**: Maintain physical correctness for FMCW parameters ($\Delta R = \frac{c}{2B}$, $\Delta v = \frac{\lambda}{2 N_c T_c}$, $a(\theta) = e^{-j 2\pi d \sin(\theta)/\lambda}$).
- **Zero Token Waste / Lean Footprint**: In accordance with the Ponytail Laziness Ladder, use standard library and existing dependencies; keep existing notebooks intact and enhance them with clear Mermaid flow diagrams and concise markdown.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Multi-level decoupled ingestion adapter | Accommodates raw ADC cubes, Range-Doppler / RadDet tensors, and point cloud DataFrames from any source | — Deferred to GitHub Issues #17 & #3 |
| Mermaid diagrams inside Jupyter notebooks | Maximizes presentation clarity for the professor without adding external UI dependencies | — Complete (Phase 1) |
| Academic publication showcase & thesis portal | 20-page IIT Guwahati thesis report with KaTeX & interactive reader UX in `docs/` | — Complete (Phase 01.2.2) |
| High-coverage test suite expansion | >=90% deterministic coverage with pytest-cov across core DSP and DL | — Complete (Phase 1.3) |
| Defer Phases 2, 3, 4 to GitHub Backlog | Frees active planning for thesis problem statement while preserving full issue tracking | — Complete (Issues #3, #17-#22) |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-09-23 after initialization*
