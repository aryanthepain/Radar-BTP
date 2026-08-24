# WORKING.md — Active Sprint & Context Scratchpad

## Current Objective
- **Project**: Radar DSP & AI Detection Testbench (BTP)
- **Status**: Initialized & Verified (7/7 Deterministic Unit Tests Passing)
- **Verification Gate**: `pwsh -File ./scripts/verify.ps1`

---

## Acceptance Criteria
- [x] 1. Universal project structure scaffolded (`AGENTS.md`, `CONSTITUTION.md`, `WORKING.md`, `.githooks/`, `scripts/verify.ps1`, `scripts/agent-alarm.ps1`).
- [x] 2. Deterministic unit tests passed (7/7 in `tests/test_radar_dsp.py`).
- [x] 3. Radar mathematical invariants documented in `CONSTITUTION.md`.
- [ ] 4. Select next milestone (RadDet Dataset Integration / Multi-Target EKF Tracking / 3D Radar Point Cloud Dashboard).

---

## Active Verification Status
```text
🔍 [FLEET LOOP] Running Deterministic Verification...
--- [Python Gate] ---
Running python unittest suite...
.......
----------------------------------------------------------------------
Ran 7 tests in 1.447s
OK
✅ unit tests passed.
🎉 [VERIFICATION PASSED] All deterministic gates green.
```

---

## Available Modules & Capabilities
1. **Radar Simulation (`src/sim/`)**: FMCW 77 GHz Chirp synthesizer, multi-target RCS/velocity/range/azimuth, micro-Doppler pedestrian modulation, ground clutter and receiver thermal noise.
2. **Signal Processing Chain (`src/dsp/`)**: Range FFT, MTI Clutter Subtraction, Doppler FFT, 2D CA/OS-CFAR Detector, MUSIC & Capon Angle-of-Arrival (AoA) estimation, DBSCAN Point Cloud clustering.
3. **Deep Learning Detector (`src/models/`)**: PyTorch `RadarObjectDetectorCNN` multi-task anchor-free heatmap and bounding box regressor.
4. **End-to-End Testbench (`scripts/run_radar_pipeline.py`)**: Full simulation, DSP processing, CNN training & multi-panel publication-grade visualization export.
