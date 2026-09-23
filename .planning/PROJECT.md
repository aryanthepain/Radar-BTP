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

### Active

- [ ] **Multi-Level Decoupled Radar Data Ingestion (GitHub Issue #3 / Closes #3)**:
  - Create a universal data adapter interface that allows directly passing data at any stage, independent of the simulator:
    - **Level 1 (Raw ADC Cube)**: Complex NumPy array / tensor of shape `(num_rx, num_chirps, num_samples)` or file loader (`.npy`, `.npz`, `.mat`).
    - **Level 2 (Range-Doppler Matrix / RAD Tensor)**: 2D/3D tensor of shape `(num_doppler, num_range)` or RadDet-style RAD tensor `(range, azimuth, doppler)`.
    - **Level 3 (Tabular DataFrame / Point Cloud)**: Pandas DataFrame or structured array with columns `['range', 'velocity', 'azimuth', 'rcs']` or `['x', 'y', 'z', 'doppler']`.
  - Ensure pipeline functions accept these data structures directly without requiring an active `FMCWRadarSimulator` instance.

- [ ] **Compartmentalized Professor Presentation & Mermaid System Architecture (GitHub Issue #4 / Closes #4)**:
  - Update `01_radar_classical_dsp.ipynb` with clear academic markdown summaries, an end-to-end Mermaid pipeline diagram at the top, and modular Mermaid flow diagrams for each DSP section showing data inputs, functions, mathematical transformations, and outputs.
  - Update `02_radar_deep_learning_detection.ipynb` with clear narrative markdown, an end-to-end deep learning workflow diagram, and section diagrams detailing data preprocessing, neural network architecture, loss calculation, and detection visualization.
  - Maintain all existing working functionality and verification gates without introducing unnecessary external tools or bloated frameworks.

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
| Multi-level decoupled ingestion adapter | Accommodates raw ADC cubes, Range-Doppler / RadDet tensors, and point cloud DataFrames from any source | — Pending |
| Mermaid diagrams inside Jupyter notebooks | Maximizes presentation clarity for the professor without adding external UI dependencies | — Pending |
| Focus strictly on Issues #3 and #4 | Scopes current milestone directly to presentation readiness before receiving formal BTP problem | — Pending |

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
