# WORKING.md — Active Sprint & Context Scratchpad

## Current Objective
- **Project**: Radar DSP & AI Detection Testbench (BTP)
- **Status**: Phase 1 Complete & Verified (12/12 Deterministic Unit Tests Passing)
- **Verification Gate**: `pwsh -File ./scripts/verify.ps1`

---

## Acceptance Criteria
- [x] 1. Universal project structure scaffolded (`AGENTS.md`, `CONSTITUTION.md`, `WORKING.md`, `.githooks/`, `scripts/verify.ps1`, `scripts/agent-alarm.ps1`).
- [x] 2. Deterministic unit tests passed (12/12 in `tests/test_radar_dsp.py` and `tests/test_walkthrough_notebooks.py`).
- [x] 3. Radar mathematical invariants documented in `CONSTITUTION.md`.
- [x] 4. Two-part academic walkthrough Jupyter notebooks generated with Dark Cyber-Radar Theme in root:
  - `01_radar_classical_dsp.ipynb` (Physics, Range FFT, MTI, Doppler FFT, 2D CA-CFAR, MUSIC AoA, DBSCAN BEV, Micro-Doppler).
  - `02_radar_deep_learning_detection.ipynb` (Range-Doppler CNN, Multi-task loss, Training curves, Unseen frame inference, Academic comparison).
- [x] 5. Phase 1 Equipped with 17 Dual-Embedded Mermaid Architecture Diagrams + Collapsible SVG Fallbacks:
  - 11 diagrams in `01_radar_classical_dsp.ipynb` (Top-level signal chain + 10 section flowcharts with tensor dimensions & function signatures).
  - 6 diagrams in `02_radar_deep_learning_detection.ipynb` (Top-level flow, Gaussian splatting, Multi-branch CNN architecture, Training loop, Inference flow, Classical vs DL trade-offs).
- [ ] 6. Next Phase: Phase 2 — Multi-Level Decoupled Radar Data Ingestion (`RadarDataAdapter` for ADC cubes, RDM tensors, and point cloud DataFrames).

---

## Active Verification Status
```text
🔍 [FLEET LOOP] Running Deterministic Verification...
--- [Python Gate] ---
Running pytest...
............                                                             [100%]
12 passed, 1 warning in 8.87s
✅ pytest tests passed.
🎉 [VERIFICATION PASSED] All deterministic gates green.
```

---

## Available Modules & Capabilities
1. **Radar Simulation (`src/sim/`)**: FMCW 77 GHz Chirp synthesizer, multi-target RCS/velocity/range/azimuth, micro-Doppler pedestrian modulation, ground clutter and receiver thermal noise.
2. **Signal Processing Chain (`src/dsp/`)**: Range FFT, MTI Clutter Subtraction, Doppler FFT, 2D CA/OS-CFAR Detector, MUSIC & Capon Angle-of-Arrival (AoA) estimation, DBSCAN Point Cloud clustering.
3. **Deep Learning Detector (`src/models/`)**: PyTorch `RadarObjectDetectorCNN` multi-task anchor-free heatmap and bounding box regressor.
4. **End-to-End Testbench (`scripts/run_radar_pipeline.py`)**: Full simulation, DSP processing, CNN training & multi-panel publication-grade visualization export.
