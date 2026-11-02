# WORKING.md — Active Sprint & Context Scratchpad

## Current Objective

- **Project**: Radar DSP & AI Detection Testbench (BTP)
- **Status**: Phase 1 Complete. Phase 1.1 Complete (All 5 Waves verified, Kaggle GPU prototype executed to completion, 23/23 tests green).
- **Active Phase**: Phase 1.1 Complete. Ready for Phase 2: Multi-Level Decoupled Radar Data Ingestion.
- **Verification Gate**: `pwsh -File ./scripts/verify.ps1`
- **Context Note (2026-11-02)**:
  - Repository officially configured for Kaggle hybrid workflows (Local deterministic development + Kaggle cloud execution).
  - Kaggle workflows and telemetry rules imported into `AGENTS.md` and `CONSTITUTION.md`.
  - Declarative workspace skill manifest `.agents/skills.json` bound to `cloud-data` pack.
  - Workspace MCP configuration `.agents/mcp_config.json` configured with `kaggle` (remote `https://www.kaggle.com/mcp`), `notebooks`, and `data-agent-kit`.
  - In-container telemetry module `src/telemetry.py` implemented (`StageProgressTracker` with ETC/ETA calculation).
  - Kaggle kernel staging and push CLI `scripts/push_kaggle_kernel.py` implemented and verified.
  - RadDet local micro-slice populated at `data/raddet_sample/` (60 spectrograms, YOLO labels, `data.yaml`).
  - Decoupled `src/raddet/` package implemented (`config.py`, `dataset.py`, `visualize.py`).
  - Deterministic unit tests `tests/test_raddet.py` implemented and verified.
  - `03_raddet_spectrum_detection_kaggle.ipynb` generated via `scripts/build_raddet_notebook.py` with 7 comprehensive sections.
  - Universal verification gate passed with 23/23 tests green.
  - Cloud Execution: `aryanguptaji/raddet-phase-1-1-spectrum-detection-prototype` executed on Kaggle Tesla T4 GPU to status `KernelWorkerStatus.COMPLETE`.
  - Output artifacts retrieved into `data/kaggle_outputs/` (`best.pt`, `results.csv`, `eda_raddet_samples.png`, `validation_metrics_curves.png`, `unseen_frame_detections.png`).

---

## Acceptance Criteria

- [x] 1. Universal project structure scaffolded (`AGENTS.md`, `CONSTITUTION.md`, `WORKING.md`, `.githooks/`, `scripts/verify.ps1`, `scripts/agent-alarm.ps1`).
- [x] 2. Deterministic unit tests passed (23/23 in `tests/test_radar_dsp.py`, `tests/test_walkthrough_notebooks.py`, `tests/test_kaggle_integration.py`, and `tests/test_raddet.py`).
- [x] 3. Radar mathematical invariants documented in `CONSTITUTION.md`.
- [x] 4. Two-part academic walkthrough Jupyter notebooks generated with Dark Cyber-Radar Theme in root:
  - `01_radar_classical_dsp.ipynb` (Physics, Range FFT, MTI, Doppler FFT, 2D CA-CFAR, MUSIC AoA, DBSCAN BEV, Micro-Doppler).
  - `02_radar_deep_learning_detection.ipynb` (Range-Doppler CNN, Multi-task loss, Training curves, Unseen frame inference, Academic comparison).
- [x] 5. Kaggle Operating Rules & Telemetry codified:
  - `AGENTS.md`: Dual-path resolution (`/kaggle/input` vs `./data`), output redirection to `/kaggle/working`, output buffer crash protection, and in-container telemetry standard.
  - `CONSTITUTION.md`: Section 5 (Kaggle Cloud & In-Container Invariants).
  - Declarative manifests: `.agents/skills.json` and `.agents/mcp_config.json`.
  - Implementation: `src/telemetry.py` (`StageProgressTracker`) and `scripts/push_kaggle_kernel.py`.
- [x] 6. Phase 1.1 Local Deliverables & Staged Kaggle Walkthrough Notebook:
  - `data/raddet_sample/`: 60 spectrogram PNGs and normalized YOLO `.txt` labels across train/val/test splits with valid `data.yaml`.
  - `src/raddet/`: Decoupled dataset loader, YOLO parser, box denormalizer, and publication-grade spectrogram visualizer.
  - `tests/test_raddet.py`: 5 deterministic unit tests covering class mapping, coordinate math, and PyTorch forward pass.
  - `03_raddet_spectrum_detection_kaggle.ipynb`: Self-contained 13-cell notebook configured for Kaggle GPU with embedded `StageProgressTracker`.
- [x] 7. Phase 1.1 Cloud Deployment & Prototype Execution on Kaggle GPU:
  - Deployed `aryanguptaji/raddet-phase-1-1-spectrum-detection-prototype` with dataset `abcxyzi/raddet-icassp-2025`.
  - Completed 15-epoch YOLOv8n training run on Tesla T4 GPU.
  - Downloaded models (`best.pt`, `last.pt`), loss curves, metrics, and multi-panel detection plots to `data/kaggle_outputs/`.
- [x] 8. Phase 1.1 User Acceptance Testing (UAT) Certified:
  - Validated local dataset micro-slice, decoupled `src/raddet/` package, and deterministic unit tests.
  - Diagnosed and resolved notebook Mermaid diagram visualization by pre-compiling high-resolution SVG into markdown cell.
  - Certified Kaggle GPU model weights and figures.
  - Passed universal verification gate (`scripts/verify.ps1`, 23/23 tests green).
  - Formally recorded results in `.planning/phases/01.1-raddet-spectrum-detection/01.1-UAT.md`.
- [ ] 9. Next Phase: Phase 2 — Multi-Level Decoupled Radar Data Ingestion (`RadarDataAdapter` for ADC cubes, RDM tensors, and point cloud DataFrames).

---

## Active Verification Status

```text
🔍 [FLEET LOOP] Running Deterministic Verification...
--- [Python Gate] ---
Running pytest...
.......................                                                  [100%]
23 passed in 22.39s
✅ pytest tests passed.
🎉 [VERIFICATION PASSED] All deterministic gates green.
```

---

## Available Modules & Capabilities

1. **Radar Simulation (`src/sim/`)**: FMCW 77 GHz Chirp synthesizer, multi-target RCS/velocity/range/azimuth, micro-Doppler pedestrian modulation, ground clutter and receiver thermal noise.
2. **Signal Processing Chain (`src/dsp/`)**: Range FFT, MTI Clutter Subtraction, Doppler FFT, 2D CA/OS-CFAR Detector, MUSIC & Capon Angle-of-Arrival (AoA) estimation, DBSCAN Point Cloud clustering.
3. **Deep Learning Detector (`src/models/`)**: PyTorch `RadarObjectDetectorCNN` multi-task anchor-free heatmap and bounding box regressor.
4. **Kaggle Telemetry & Push Automation (`src/telemetry.py`, `scripts/push_kaggle_kernel.py`)**: Self-reporting in-container progress tracking with ETC/ETA calculation, kernel staging, and CLI push.
5. **End-to-End Testbench (`scripts/run_radar_pipeline.py`)**: Full simulation, DSP processing, CNN training & multi-panel publication-grade visualization export.
