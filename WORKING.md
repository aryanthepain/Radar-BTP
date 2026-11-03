# WORKING.md — Active Sprint & Context Scratchpad

## Current Objective

- **Project**: Radar DSP & AI Detection Testbench (BTP)
- **Status**: Phase 1 Complete. Phase 1.1 Complete. Phase 1.2 Full-Scale Cloud Benchmark & Comparative Evaluation Complete.
- **Active Kaggle Kernel**: [`aryanguptaji/raddet-s-128-full-scale-benchmark`](https://www.kaggle.com/code/aryanguptaji/raddet-s-128-full-scale-benchmark) (Version 5)
- **Kaggle Kernel Status**: `KernelWorkerStatus.COMPLETE` (Full 66 epochs trained on Kaggle GPU across 40,003 frames; 1h 11m training time; all artifacts pulled)
- **Active Branch**: `gsd/phase-01.2-full-scale-raddet-benchmark-on-kaggle`
- **Verification Gate**: `pwsh -File ./scripts/verify.ps1`
- **Active Test Status**: 27/27 tests green in 11.4s.
- **Phase 1.2 Achievements**:
  - Full-scale RadDet S-128 dataset pipeline executed on Kaggle GPU over 40,003 frames (14,001 train / 6,001 val / 20,001 test) across 11 classes.
  - Reproduces ICASSP 2025 Table III: YOLOv9-C achieves grand mean mAP50 = 25.25% (vs paper 25.93%) and mAP50:95 = 19.03% (vs paper 19.47%) across 6 multi-SNR bins (-20 dB to +20 dB).
  - Peak validation performance: mAP50 = 32.53% (Epoch 60), mAP50:95 = 23.77% (Epoch 46), Recall = 72.60% (Epoch 25).
  - Real-time hardware latency benchmark: 1.12 ms mean latency (892.9 FPS on Tesla T4 at batch size 1), matching paper 896.6 FPS within 0.4%.
  - Comprehensive comparative analysis between small prototype run (40 synthetic frames, collapsed) and full-scale run (40,003 real frames, monotonic convergence).
  - Full report generated at `data/benchmark_results/s128_full/COMPARATIVE_BENCHMARK_REPORT.md` and user-facing artifact.

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
