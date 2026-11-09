# Roadmap: Radar-BTP

## Overview

A phased journey to prepare an undergraduate thesis exploratory presentation for the supervising professor, followed by internal architectural decoupling of radar data ingestion, and final testbench verification.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Compartmentalized Jupyter Walkthroughs & Mermaid Diagrams** - Structure notebooks with unified Mermaid flowcharts and academic narrative for the professor presentation.
- [x] **Phase 1.1: RadDet Dataset Integration & Spectrum Sensing Benchmark (Limited Slice)** (INSERTED) - Ingest real-world RadDet ICASSP 2025 dataset with minimal local micro-slice, YOLOv8/v9 spectrum detector, and limited Kaggle run.
- [x] **Phase 1.2: Full-Scale RadDet Benchmark on Kaggle (S-128 Variant)** (INSERTED) - Execute 20,000-frame full training run on S (128²) resolution across multi-SNR settings on Kaggle GPU for up to 100 epochs.
- [x] **Phase 01.2.1: Interactive Research Showcase & Thesis Presentation Website** (INSERTED) - Deliver a clean, responsive showcase website for the supervising professor synthesizing all three notebooks, experimental results, comparative radar data progression (toy -> synthetic -> real RadDet), architecture flowcharts, and key code snippets.
- [ ] **Phase 01.2.2: Comprehensive BTP Thesis Report & Academic Publication Showcase Website** (INSERTED) - Deliver publication-grade ~20-page IIT Guwahati BTP Report and rework GitHub Pages website into an academic reading experience for professor finalization.
- [ ] **Phase 1.3: High-Coverage Deterministic Unit & Integration Testing** (INSERTED) - Comprehensive test expansion achieving >=90% code coverage across DSP algorithms, PyTorch dataset/models, and pipeline scripts with pytest-cov.
- [ ] **Phase 2: Multi-Level Decoupled Radar Data Ingestion** - Implement internal data adapter decoupling pipeline from simulator (Raw ADC cubes, RDM/RAD tensors, Point Cloud DataFrames).
- [ ] **Phase 3: Pipeline Integration & Deterministic Verification Gates** - Integrate decoupled data flow into pipeline testbench and pass all deterministic gates.

## Phase Details

### Phase 1: Compartmentalized Jupyter Walkthroughs & Mermaid Diagrams

**Goal**: Equip `01_radar_classical_dsp.ipynb` and `02_radar_deep_learning_detection.ipynb` with clear academic markdown explanations and self-contained Mermaid flow diagrams (top-level end-to-end flow + single comprehensive diagram per section showing data source, functions, transformations, and outputs) so that each stage can be effortlessly explained to the professor.
**Mode**: mvp
**Depends on**: Nothing (first phase)
**Requirements**: PRES-01, PRES-02, PRES-03, PRES-04
**Success Criteria** (what must be TRUE):

1. Top-level end-to-end Mermaid flow diagram at the beginning of `01_radar_classical_dsp.ipynb`.
2. Section-level Mermaid flow diagrams for each discrete DSP block detailing inputs, functions, math, and outputs in one diagram per section.
3. Deep learning pipeline and architecture Mermaid diagrams embedded in `02_radar_deep_learning_detection.ipynb`.
4. Both notebooks execute cleanly end-to-end with high-contrast presentation figures and self-contained narrative.
   **Plans**: 2 plans

Plans:

- [x] 01-01: Structure and enrich `01_radar_classical_dsp.ipynb` with top-level and section-by-section Mermaid diagrams and academic markdown.
- [x] 01-02: Structure and enrich `02_radar_deep_learning_detection.ipynb` with deep learning Mermaid architecture diagrams and clear narrative explanations.

### Phase 1.1: RadDet Dataset Integration & Spectrum Sensing Benchmark (Limited Slice)

**Goal**: Integrate the real-world RadDet ICASSP 2025 dataset with a minimal local micro-slice (~50–100 samples) in `data/raddet_sample/`, a dedicated `src/raddet/` package with YOLO parser and visualizer, deterministic unit tests in `tests/test_raddet.py`, and a complete, self-contained Kaggle walkthrough notebook (`03_raddet_spectrum_detection_kaggle.ipynb`) trained on a limited subset of RadDet-9T-128, strictly preserving all existing synthetic radar assets.
**Mode**: mvp
**Depends on**: Phase 1
**Requirements**: RADDET-01, RADDET-02, RADDET-03, VERIF-RADDET
**Success Criteria** (what must be TRUE):

1. Local micro-slice in `data/raddet_sample/` with valid `data.yaml`, images, and YOLO `.txt` labels.
2. Decoupled `src/raddet/` package with dataset loader, bounding-box parsing, and spectrogram visualizer.
3. Deterministic unit tests in `tests/test_raddet.py` pass verifying coordinate math, label parsing, and PyTorch model forward pass.
4. Self-contained Kaggle notebook `03_raddet_spectrum_detection_kaggle.ipynb` configured for `abcxyzi/raddet-icassp-2025` limited run with validation mAP metrics and multi-panel detection plots.
5. All existing synthetic radar tests and notebooks continue to pass 100% without modification.

**Plans**: 5 plans

Plans:

- [x] 01.1-01: Establish local micro-slice dataset in `data/raddet_sample/` and automated fetcher `scripts/fetch_raddet_sample.py`.
- [x] 01.1-02: Implement dedicated `src/raddet/` package (`config.py`, `dataset.py`, `visualize.py`) and author deterministic unit tests in `tests/test_raddet.py`.
- [x] 01.1-03: Develop programmatic builder `scripts/build_raddet_notebook.py` and generate self-contained Kaggle walkthrough notebook `03_raddet_spectrum_detection_kaggle.ipynb`.
- [x] 01.1-04: Integrate notebook test runners into `tests/test_walkthrough_notebooks.py` and verify all deterministic gates via `scripts/verify.ps1`.
- [x] 01.1-05: Deploy and execute limited prototype on Kaggle GPU via Kaggle CLI (`aryanguptaji/raddet-phase1-1-prototype`), retrieve metrics, and validate detection figures.

### Phase 1.2: Full-Scale RadDet Benchmark on Kaggle (S-128 Variant)

**Goal**: Conduct full-scale training and benchmark evaluation of RadDet across the complete 20,000-frame training set on Kaggle GPU for the **S ($128^2$)** resolution variant for 100 epochs with early stopping safety, automated multi-SNR evaluation (-20 dB to +20 dB), and dedicated real-time latency/FPS benchmarking matching Table III of the ICASSP 2025 paper. (M-256 and L-512 resolutions deferred to subsequent phases).
**Mode**: mvp
**Depends on**: Phase 1.1
**Requirements**: RADDET-BENCH-01, RADDET-BENCH-02
**Success Criteria** (what must be TRUE):

1. Full training run executed on Kaggle GPU for up to 100 epochs on S (128²) with Ultralytics YOLOv9/v8.
2. Automated multi-SNR breakdown (-20 dB to +20 dB) reproducing paper benchmark trends and Fig 3(c) curves.
3. Final benchmark comparison table matching the S-128 row of Table III in the ICASSP 2025 paper.
4. Dedicated real-time inference latency pass (batch size 1, CUDA sync) reporting operational FPS.
5. All local deterministic test gates pass with 100% success under `verify.ps1`.
   **Plans**: 3 plans

Plans:

- [x] 01.2-01: In-place notebook upgrade with smart cached extraction, empirical batch smoke test, and 100-epoch YOLOv9 loop.
- [x] 01.2-02: Automated 6-bin multi-SNR evaluation loop, Table III exporter, and single-frame latency profiler.
- [x] 01.2-03: Kaggle CLI artifact pull/status automation and dual-mode CI verification.

### Phase 01.2.1: Interactive Research Showcase & Thesis Presentation Website (INSERTED)

**Goal:** Deliver a lightweight, clean, interactive presentation website for the supervising professor illustrating the end-to-end BTP journey across all three notebooks (`01_radar_classical_dsp`, `02_radar_deep_learning_detection`, `03_raddet_spectrum_detection_kaggle`), showcasing key DSP/DL code snippets, visual flowcharts, benchmark metrics, and clear comparative progression (analytical toy baseline -> synthetic FMCW radar simulation -> real-world RadDet ICASSP 2025 dataset).
**Requirements**: PRES-WEB-01, PRES-WEB-02, PRES-WEB-03
**Depends on:** Phase 1.2
**Plans:** 3 plans

Plans:
**Wave 1**

- [x] 01.2.1-01: Asset Pipeline, Automated Notebook Extraction & Vector Diagrams

**Wave 2**

- [x] 01.2.1-02: Zero-Build Static Website Implementation

**Wave 3**

- [x] 01.2.1-03: Deterministic Smoke Test Suite & Gate Verification

### Phase 01.2.2: Comprehensive BTP Thesis Report & Academic Publication Showcase Website (INSERTED)

**Goal:** Deliver a rigorous, publication-grade B.Tech Project (BTP-1) Report (~20 pages) adhering to IIT Guwahati thesis standards, addressing core professor focus areas (AI value-add vs DSP, close-object resolution limits, compute/memory trade-offs, realistic dataset benchmarks, raw data inversion, defense/automotive utilities), and rework the GitHub Pages site into an academic report reading interface for professor finalization.
**Requirements**: BTP-REP-01, BTP-REP-02, BTP-REP-03
**Depends on:** Phase 01.2.1
**Plans:** 4 plans

Plans:
**Wave 1**
- [ ] 01.2.2-01: Deep Research & Literature Synthesis with Interactive Clarification (RadDet, RAVEN, AdaRadar, Karlsson KTH/Saab, DRDO Pal).
- [ ] 01.2.2-02: BTP Experience, Timeline & Technical Journey Grilling (Aug 2026 to May 2027 calendar).
- [ ] 01.2.2-03: Two-Column Academic Paper Architecture, KaTeX Math & Reader UX in `docs/`.

**Wave 2**
- [ ] 01.2.2-04: Full Academic Report Content Synthesis & Verification (~20-page comprehensive report covering all 9 deliverables, professor defense, and test gates).

### Phase 1.3: High-Coverage Deterministic Unit & Integration Testing (INSERTED)

**Goal**: Expand deterministic test coverage using `pytest-cov` to achieve >=90% total coverage across core radar signal processing (`src/dsp/`), synthetic dataset generation (`src/models/radar_dataset.py`), real-world RadDet parsing (`src/raddet/`), and CLI pipeline execution scripts (`scripts/`).
**Mode**: standard
**Depends on**: Phase 1.1
**Requirements**: TEST-COV-01, TEST-COV-02, TEST-COV-03, TEST-COV-04
**Success Criteria** (what must be TRUE):

1. Dedicated modular test suites added: `tests/test_dsp_edge_cases.py`, `tests/test_radar_dataset.py`, and `tests/test_pipeline_scripts.py`.
2. Coverage for `src/models/radar_dataset.py` increases from 19% to >=90%.
3. Total core `src/` coverage reaches >=90% across all modules.
4. CLI pipeline runners and notebook builders are covered with non-interactive smoke tests.
5. All tests run deterministically in under 30 seconds with 100% pass rate.
   **Plans**: 3 plans

Plans:

- [ ] 01.3-01: Author `tests/test_dsp_edge_cases.py` targeting OS-CFAR, Capon/MUSIC AoA, MTI cancellers, Doppler windowing, and Range FFT scaling.
- [ ] 01.3-02: Author `tests/test_radar_dataset.py` targeting synthetic `RadarDataset` generation, box coordinate math, multi-task heatmap encoding, and DataLoader collate functions.
- [ ] 01.3-03: Author `tests/test_pipeline_scripts.py` targeting `scripts/run_radar_pipeline.py`, `scripts/push_kaggle_kernel.py`, and update `scripts/verify.ps1` with strict `pytest-cov` enforcement.

### Phase 2: Multi-Level Decoupled Radar Data Ingestion

**Goal**: Build a universal `RadarDataAdapter` allowing direct data injection at all pipeline levels (Level 1: Raw ADC cubes, Level 2: RDM/RAD tensors, Level 3: Point Cloud DataFrames) independently of the simulator for internal project flexibility.
**Mode**: mvp
**Depends on**: Phase 1
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, VERIF-01
**Success Criteria** (what must be TRUE):

1. Direct ingestion of 3D complex ADC cubes `(num_rx, num_chirps, num_samples)` from NumPy arrays or files without calling `FMCWRadarSimulator`.
2. Direct ingestion of Range-Doppler matrices or 3D RAD tensors (e.g. RadDet tensor format) into CFAR and CNN detector modules.
3. Direct ingestion of Pandas DataFrames with detection points into DBSCAN clustering and Cartesian coordinate mapping.
4. Unit test suite `tests/test_radar_data_adapter.py` passes deterministically covering all three ingestion levels.
   **Plans**: TBD

Plans:

- [ ] 02-01: Implement `RadarDataAdapter` and validation routines in `src/dsp/data_adapter.py`.
- [ ] 02-02: Author unit tests in `tests/test_radar_data_adapter.py` validating all ingestion levels.

### Phase 3: Pipeline Integration & Deterministic Verification Gates

**Goal**: Integrate the decoupled data adapters into the main end-to-end testbench (`scripts/run_radar_pipeline.py`) and ensure all deterministic gates and GitHub issue linkages pass cleanly.
**Mode**: mvp
**Depends on**: Phase 2
**Requirements**: VERIF-02
**Success Criteria** (what must be TRUE):

1. Testbench runs full pipeline with both simulated data and external adapter data.
2. Deterministic gate `pwsh -File ./scripts/verify.ps1` passes with zero errors.
3. Audio alert and verification logs confirm completion ready for presentation.
   **Plans**: TBD

Plans:

- [ ] 03-01: Update `scripts/run_radar_pipeline.py` to demonstrate both simulated and decoupled data paths.
- [ ] 03-02: Run universal verification gate (`scripts/verify.ps1`), confirm Closes #3 and Closes #4, and trigger completion audio alert.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase                                                                        | Plans Complete | Status      | Completed  |
| ---------------------------------------------------------------------------- | -------------- | ----------- | ---------- |
| 1. Compartmentalized Jupyter Walkthroughs & Mermaid Diagrams                 | 2/2            | Completed   | 2026-09-23 |
| 1.1. RadDet Dataset Integration & Spectrum Sensing Benchmark (Limited Slice) | 5/5            | Completed   | 2026-11-02 |
| 1.2. Full-Scale RadDet Benchmark on Kaggle (S-128 Variant)                   | 3/3            | Completed   | 2026-11-03 |
| 01.2.1. Interactive Research Showcase & Thesis Presentation Website          | 3/3            | Completed   | 2026-11-03 |
| 01.2.2. Comprehensive BTP Thesis Report & Academic Publication Showcase Website | 0/4            | In Progress | -          |
| 1.3. High-Coverage Deterministic Unit & Integration Testing                  | 0/3            | In Progress | -          |
| 2. Multi-Level Decoupled Radar Data Ingestion                                | 0/2            | Not started | -          |
| 3. Pipeline Integration & Deterministic Verification Gates                   | 0/2            | Not started | -          |
