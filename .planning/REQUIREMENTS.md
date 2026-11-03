# Requirements: Radar-BTP

**Defined:** 2026-09-23
**Core Value:** Modular, decoupled radar perception enabling multi-level data ingestion (raw ADC cubes, Range-Doppler tensors, or point cloud dataframes) and transparent academic presentation of radar signal processing.

## v1 Requirements

### Multi-Level Decoupled Ingestion (DATA — Closes #3)

- [ ] **DATA-01**: Pipeline can directly ingest raw 3D complex ADC radar cubes `(num_rx, num_chirps, num_samples)` from NumPy arrays, tensors, or `.npy`/`.npz`/`.mat` files without requiring `FMCWRadarSimulator`.
- [ ] **DATA-02**: Pipeline can directly ingest 2D Range-Doppler matrices (RDM) or 3D RAD tensors (e.g., RadDet tensor structure `(range, azimuth, doppler)`) directly into CFAR detection and deep learning modules, bypassing simulation and 1D/2D FFT processing.
- [ ] **DATA-03**: Pipeline can directly ingest tabular DataFrames or structured point clouds (`pd.DataFrame` with range, velocity, azimuth, power/rcs) directly into spatial clustering (DBSCAN) and downstream Cartesian tracking.
- [ ] **DATA-04**: Universal `RadarDataAdapter` abstraction providing schema inspection, shape validation, and automatic routing to the appropriate pipeline stage.

### Compartmentalized Professor Presentation & Architecture (PRES — Closes #4)

- [ ] **PRES-01**: Top-level Mermaid flow diagram embedded at the beginning of `01_radar_classical_dsp.ipynb` depicting the complete end-to-end signal flow from raw data ingestion to clustered tracks.
- [ ] **PRES-02**: Compartmentalized section-level Mermaid diagrams in `01_radar_classical_dsp.ipynb` for each discrete stage (Ingestion, Fast-Time FFT, MTI Clutter Filtering, Doppler FFT, 2D CFAR, MUSIC AoA, DBSCAN Clustering), detailing input data, function signatures, operations, and outputs in one diagram per section.
- [ ] **PRES-03**: Top-level and section-level Mermaid architecture diagrams in `02_radar_deep_learning_detection.ipynb` covering dataset generation, convolutional backbone, multi-task prediction heads (heatmaps & boxes), loss functions, and evaluation.
- [ ] **PRES-04**: Polished academic markdown documentation in both notebooks explaining physical principles, mathematical formulations, and engineering trade-offs for clear presentation to the thesis advisor.

### RadDet Full-Scale Benchmark on Kaggle (RADDET-BENCH)

- [x] **RADDET-BENCH-01**: Execute full 20,000-frame training run of RadDet S (128²) on Kaggle GPU for up to 100 epochs using Ultralytics YOLOv9 with early stopping, periodic checkpoints, and paper RF augmentations.
- [x] **RADDET-BENCH-02**: Automated multi-SNR evaluation loop across 6 discrete SNR bins (-20 dB to +20 dB) exporting Table III markdown/CSV benchmark metrics, Fig 3(c) curves, and real-time single-frame latency ($FPS_{avg}$) benchmarking.

### Interactive Research Showcase & Presentation Website (PRES-WEB)

- [ ] **PRES-WEB-01**: Asset extraction pipeline and vector diagram builder (`scripts/export_showcase_assets.py`) programmatically exporting 17 primary PNG figures from notebooks and benchmark folders, 4 cached architecture SVGs, 3-stage evolution timeline SVG, and offline Prism.js assets into `docs/assets/`.
- [ ] **PRES-WEB-02**: Zero-build standalone static presentation website (`docs/index.html`, `docs/styles.css`, `docs/app.js`) featuring Dark Cyber-Radar theme, sticky sidebar navigation, standardized 5-part blocks per notebook, 7-metric master comparison table, image lightbox modal, and professor takeaways without external CDN dependencies.
- [ ] **PRES-WEB-03**: Deterministic smoke test suite (`tests/test_showcase_website.py`) validating HTML DOM structure, local asset integrity, zero external URLs, and universal verification gate sign-off via `scripts/verify.ps1`.

### High-Coverage Test Suite & Pytest-Cov Integration (TEST-COV)

- [ ] **TEST-COV-01**: Dedicated unit test suite `tests/test_dsp_edge_cases.py` targeting OS-CFAR, Capon/MUSIC AoA, MTI cancellers, Doppler windowing, and Range FFT scaling.
- [ ] **TEST-COV-02**: Dedicated unit test suite `tests/test_radar_dataset.py` targeting synthetic `RadarDataset` generation, box coordinate math, multi-task heatmap encoding, and DataLoader collate functions (raising `src/models/radar_dataset.py` to >=90%).
- [ ] **TEST-COV-03**: Automated integration smoke tests `tests/test_pipeline_scripts.py` covering `scripts/run_radar_pipeline.py`, `scripts/push_kaggle_kernel.py`, and notebook generators.
- [ ] **TEST-COV-04**: Universal verification gate (`scripts/verify.ps1`) enforces `>=90%` code coverage with `pytest-cov` while maintaining deterministic, sub-30s local execution.

### Verification & Deterministic Gates (VERIF)

- [ ] **VERIF-01**: Unit test suite (`tests/test_radar_data_adapter.py`) validating decoupled ingestion across Level 1 (raw cube), Level 2 (RDM/RAD tensor), and Level 3 (point cloud DataFrame).
- [ ] **VERIF-02**: Universal deterministic verification gate (`pwsh -File ./scripts/verify.ps1`) passes cleanly with all unit tests and pipeline testbenches intact.

## v2 Requirements

### Full Benchmark Dataset Integration (BENCH)

- **BENCH-01**: Automated batch loader for full multi-scene RadDet / CARRADA dataset sequences.
- **BENCH-02**: Pre-trained model weights fine-tuned on public automotive radar benchmarks.

### Hardware Interfacing (HW)

- **HW-01**: Real-time I/Q ADC packet parser for physical Texas Instruments (TI mmWave) DCA1000 EVM / SDR streaming.

## Out of Scope

| Feature                                        | Reason                                                                                                     |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Downloading multi-GB RadDet datasets in v1     | Deferred until professor delivers formal thesis problem statement.                                         |
| External web app dashboard (Streamlit / React) | Excluded to keep existing Jupyter notebooks self-contained and directly presentable.                       |
| Real-time physical radar SDR streaming in v1   | Requires physical hardware setup; exploratory phase focuses on algorithmic perception and data decoupling. |

## Traceability

| Requirement     | Phase        | Status   |
| --------------- | ------------ | -------- |
| PRES-01         | Phase 1      | Complete |
| PRES-02         | Phase 1      | Complete |
| PRES-03         | Phase 1      | Complete |
| PRES-04         | Phase 1      | Complete |
| RADDET-BENCH-01 | Phase 1.2    | Complete |
| RADDET-BENCH-02 | Phase 1.2    | Complete |
| PRES-WEB-01     | Phase 01.2.1 | Complete |
| PRES-WEB-02     | Phase 01.2.1 | Complete |
| PRES-WEB-03     | Phase 01.2.1 | Complete |
| TEST-COV-01     | Phase 1.3    | Pending  |
| TEST-COV-02     | Phase 1.3    | Pending  |
| TEST-COV-03     | Phase 1.3    | Pending  |
| TEST-COV-04     | Phase 1.3    | Pending  |
| DATA-01         | Phase 2      | Pending  |
| DATA-02         | Phase 2      | Pending  |
| DATA-03         | Phase 2      | Pending  |
| DATA-04         | Phase 2      | Pending  |
| VERIF-01        | Phase 2      | Pending  |
| VERIF-02        | Phase 3      | Pending  |

**Coverage:**

- v1 requirements: 19 total
- Mapped to phases: 19
- Unmapped: 0 ✓

---

_Requirements defined: 2026-09-23_
_Last updated: 2026-11-03 for Phase 01.2.1 additions_
