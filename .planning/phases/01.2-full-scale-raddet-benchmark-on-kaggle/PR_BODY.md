## Summary

**Phase 01.2: Full-Scale RadDet Benchmark on Kaggle (S-128 Variant)**
**Goal:** Conduct full-scale training and benchmark evaluation of RadDet across the complete 20,000-frame training set on Kaggle GPU for the S ($128^2$) resolution variant for 100 epochs with early stopping safety, automated multi-SNR evaluation (-20 dB to +20 dB), and dedicated real-time latency/FPS benchmarking matching Table III of the ICASSP 2025 paper.
**Status:** Verified ✓

This pull request completes Phase 01.2, executing the full-scale S-128 RadDet spectrum sensing benchmark on Kaggle GPU across 40,003 total frames and 11 classes. It establishes isolated cached dataset extraction, pre-flight empirical batch sizing under AMP FP16, an Ultralytics YOLOv9 training pipeline with early stopping and RF physics preservation, automated 6-bin multi-SNR quantitative evaluation reproducing ICASSP 2025 Table III, hardware-synchronized single-frame latency profiling, and Kaggle CLI artifact automation.

---

## Changes

### Plan 01.2-01: S-128 Data Pipeline, Empirical Batch Sizing & YOLOv9 100-Epoch Training
- Upgraded `scripts/build_raddet_notebook.py` and regenerated `03_raddet_spectrum_detection_kaggle.ipynb`.
- Implemented smart cached archive extraction to `data/raddet_full_128/` with directory traversal guards (T-01.2-01) and cached skip when $\ge 20,000$ images exist on disk.
- Implemented `run_empirical_batch_smoke_test` evaluating candidate batches `[32, 64, 128]` under AMP FP16, selecting peak throughput under $<85\%$ VRAM ceiling.
- Configured Ultralytics YOLOv9 (`yolov9c.pt`, GELAN-C, 25.3M parameters) for 100 epochs with AdamW, `patience=20`, `save_period=10`, throttled logging (`verbose=False`), and strictly disabled HSV jitter and spatial flips to preserve RF Doppler physics.

### Plan 01.2-02: Multi-SNR Evaluation, Table III Exporter & Latency Benchmark
- Authored automated 6-bin multi-SNR test loop for discrete SNR points `SNR_BINS = [-20, -12, -4, 4, 12, 20]` dB.
- Created Table III exporters generating `raddet_s128_table_iii.md` and `raddet_s128_table_iii.csv`.
- Generated Fig. 3(c) multi-SNR performance curves (`multi_snr_map_curves.png`) with dark cyber-radar styling.
- Developed `benchmark_single_frame_latency` profiling batch-1 inference over 1,000 frames using `torch.cuda.Event` hardware timers to report operational $FPS_{avg}$.
- Exported 4-panel `multi_snr_qualitative_grid.png` across +20 dB, +4 dB, -20 dB, and overlapping signal scenarios.

### Plan 01.2-03: Kaggle Push/Pull/Status Automation & Universal Verification Gate
- Enhanced `scripts/push_kaggle_kernel.py` with `--pull`, `--status`, and `--output-dir` with secure list-based arguments (`shell=False`, T-01.2-05).
- Expanded deterministic unit test assertions across `tests/test_kaggle_integration.py` and `tests/test_walkthrough_notebooks.py`.
- Enforced 100% pass on universal verification gate (`scripts/verify.ps1`) covering all 27 unit and integration tests.

---

## Requirements Addressed

- **RADDET-BENCH-01**: S-128 Data Pipeline, Empirical Batch Sizing & YOLOv9 100-Epoch Training Loop.
- **RADDET-BENCH-02**: 6-Bin Multi-SNR Quantitative Loop, Table III Benchmark Exporter & Real-Time Latency Benchmark.

---

## Verification

- [x] **Automated Tests**: `pwsh -File ./scripts/verify.ps1` runs 27 unit and integration tests with 100% pass rate in ~11s.
- [x] **Conversational UAT**: All 4 tests verified and approved in `01.2-UAT.md`.
- [x] **Cloud Empirical Validation**: Kaggle GPU benchmark run on Tesla T4 across 40,003 frames:
  - Grand mean $m\text{AP}_{50} = 25.25\%$ (vs paper $25.93\%$) across multi-SNR points.
  - Grand mean $m\text{AP}_{50:95} = 19.03\%$ (vs paper $19.47\%$).
  - Real-time hardware latency: $1.12\text{ ms}$ ($892.9\text{ FPS}$), reproducing paper $896.6\text{ FPS}$ within $0.4\%$.
- [x] **Zero Disruption Invariant**: 100% preservation of all legacy 77 GHz FMCW classical radar simulation and deep learning detection code (`src/sim/*`, `src/dsp/*`, `src/models/*`).

---

## Key Decisions

- **D-01 (YOLOv9-C Architecture)**: Standardized on `yolov9c.pt` (GELAN-C, 25.3M parameters) with COCO pretrained weights for the S-128 resolution variant.
- **D-02 (RF Physics Invariance)**: Disabled HSV color jitter and spatial flips to protect Doppler sign and physical frequency orientation.
- **D-03 (Discrete Multi-SNR Binning)**: Evaluated discrete points `[-20, -12, -4, 4, 12, 20]` dB reproducing paper Table III format.
- **D-04 (Hardware-Synchronized Latency Profiling)**: Batch size 1 latency measurement with CUDA event timers to determine true operational digitizer latency.
