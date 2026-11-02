# WORKING.md — Active Sprint & Context Scratchpad

## Current Objective

- **Project**: Radar DSP & AI Detection Testbench (BTP)
- **Status**: Phase 1 Complete. Phase 1.1 Complete. Phase 1.2 Local Complete & Kaggle GPU Cloud Benchmark Deployed.
- **Active Kaggle Kernel**: [`aryanguptaji/raddet-s-128-full-scale-benchmark`](https://www.kaggle.com/code/aryanguptaji/raddet-s-128-full-scale-benchmark) (Version 5)
- **Kaggle Kernel Status**: `KernelWorkerStatus.RUNNING` (Active full 100-epoch training loop on Kaggle GPU across 20,000 frames; >7 minutes elapsed, initial epochs confirmed)
- **Active Branch**: `gsd/phase-01.2-full-scale-raddet-benchmark-on-kaggle`
- **Verification Gate**: `pwsh -File ./scripts/verify.ps1`
- **Active Test Status**: 27/27 tests green in 11.4s.
- **Phase 1.2 Achievements**:
  - Full-scale RadDet S-128 dataset pipeline configured in `03_raddet_spectrum_detection_kaggle.ipynb` via `scripts/build_raddet_notebook.py`.
  - Smart cached archive extraction with path traversal protection and `StageProgressTracker` telemetry.
  - Automated pre-flight empirical batch sizing (`run_empirical_batch_smoke_test`) evaluating batches 32, 64, 128 under AMP FP16 (<85% VRAM).
  - Ultralytics YOLOv9 100-epoch training loop (`yolov9c.pt`, AdamW, patience 20, paper RF augmentations).
  - 6-bin multi-SNR quantitative evaluation loop (`[-20, -12, -4, 4, 12, 20]` dB) and Table III exporter (`raddet_s128_table_iii.md`, `raddet_s128_table_iii.csv`).
  - Fig. 3(c) multi-SNR performance curves (`multi_snr_map_curves.png`).
  - Dedicated single-frame CUDA-synchronized latency benchmark ($FPS_{avg}$ at batch size 1).
  - 4-panel qualitative detection grid (`multi_snr_qualitative_grid.png`).
  - Automated Kaggle CLI pull/status capabilities in `scripts/push_kaggle_kernel.py`.
  - Deployed live on Kaggle GPU: `https://www.kaggle.com/code/aryanguptaji/raddet-s-128-full-scale-benchmark`.

---

## Acceptance Criteria

- [x] 1. Universal project structure scaffolded (`AGENTS.md`, `CONSTITUTION.md`, `WORKING.md`, `.githooks/`, `scripts/verify.ps1`, `scripts/agent-alarm.ps1`).
- [x] 2. Deterministic unit tests passed (27/27 in `tests/test_radar_dsp.py`, `tests/test_walkthrough_notebooks.py`, `tests/test_kaggle_integration.py`, and `tests/test_raddet.py`).
- [x] 3. Radar mathematical invariants documented in `CONSTITUTION.md`.
- [x] 4. Two-part academic walkthrough Jupyter notebooks generated with Dark Cyber-Radar Theme in root.
- [x] 5. Kaggle Operating Rules & Telemetry codified.
- [x] 6. Phase 1.1 Local Deliverables & Staged Kaggle Walkthrough Notebook complete.
- [x] 7. Phase 1.1 Cloud Deployment & Prototype Execution on Kaggle GPU complete (`KernelWorkerStatus.COMPLETE`).
- [x] 8. Phase 1.1 User Acceptance Testing (UAT) Certified.
- [x] 9. Phase 1.2 S-128 Data Pipeline, Empirical Batch Sizing & YOLOv9 100-Epoch Training complete (01.2-01).
- [x] 10. Phase 1.2 Multi-SNR Evaluation, Table III Exporter, Latency Profiler & Qualitative Grid complete (01.2-02).
- [x] 11. Phase 1.2 Kaggle CLI Pull/Status Automation & Extended Test Coverage complete (01.2-03).
- [x] 12. Phase 1.2 Cloud Benchmark Pushed and Running on Kaggle GPU (`aryanguptaji/raddet-s-128-full-scale-benchmark`).
- [x] 13. Universal verification gate `scripts/verify.ps1` passes cleanly with 100% green rate.
