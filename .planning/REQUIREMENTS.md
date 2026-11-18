# Requirements: Radar-BTP

**Defined:** 2026-09-23
**Core Value:** Modular, decoupled radar perception enabling multi-level data ingestion (raw ADC cubes, Range-Doppler tensors, or point cloud dataframes) and transparent academic presentation of radar signal processing.

## v1 Requirements

### Compartmentalized Professor Presentation & Architecture (PRES — Closes #4)

- [x] **PRES-01**: Top-level Mermaid flow diagram embedded at the beginning of `01_radar_classical_dsp.ipynb` depicting the complete end-to-end signal flow from raw data ingestion to clustered tracks.
- [x] **PRES-02**: Compartmentalized section-level Mermaid diagrams in `01_radar_classical_dsp.ipynb` for each discrete stage (Ingestion, Fast-Time FFT, MTI Clutter Filtering, Doppler FFT, 2D CFAR, MUSIC AoA, DBSCAN Clustering), detailing input data, function signatures, operations, and outputs in one diagram per section.
- [x] **PRES-03**: Top-level and section-level Mermaid architecture diagrams in `02_radar_deep_learning_detection.ipynb` covering dataset generation, convolutional backbone, multi-task prediction heads (heatmaps & boxes), loss functions, and evaluation.
- [x] **PRES-04**: Polished academic markdown documentation in both notebooks explaining physical principles, mathematical formulations, and engineering trade-offs for clear presentation to the thesis advisor.

### RadDet Full-Scale Benchmark on Kaggle (RADDET-BENCH)

- [x] **RADDET-BENCH-01**: Execute full 20,000-frame training run of RadDet S (128²) on Kaggle GPU for up to 100 epochs using Ultralytics YOLOv9 with early stopping, periodic checkpoints, and paper RF augmentations.
- [x] **RADDET-BENCH-02**: Automated multi-SNR evaluation loop across 6 discrete SNR bins (-20 dB to +20 dB) exporting Table III markdown/CSV benchmark metrics, Fig 3(c) curves, and real-time single-frame latency ($FPS_{avg}$) benchmarking.

### Interactive Research Showcase & Presentation Website (PRES-WEB)

- [x] **PRES-WEB-01**: Asset extraction pipeline and vector diagram builder (`scripts/export_showcase_assets.py`) programmatically exporting 17 primary PNG figures from notebooks and benchmark folders, 4 cached architecture SVGs, 3-stage evolution timeline SVG, and offline Prism.js assets into `docs/assets/`.
- [x] **PRES-WEB-02**: Zero-build standalone static presentation website (`docs/index.html`, `docs/styles.css`, `docs/app.js`) featuring Dark Cyber-Radar theme, sticky sidebar navigation, standardized 5-part blocks per notebook, 7-metric master comparison table, image lightbox modal, and professor takeaways without external CDN dependencies.
- [x] **PRES-WEB-03**: Deterministic smoke test suite (`tests/test_showcase_website.py`) validating HTML DOM structure, local asset integrity, zero external URLs, and universal verification gate sign-off via `scripts/verify.ps1`.

### Comprehensive BTP Thesis Report & Academic Publication Showcase Website (BTP-REP)

- [x] **BTP-REP-01**: Comprehensive ~20-page academic report content synthesizing FMCW radar physics, classical DSP failure analysis, synthetic deep learning, full-scale RadDet benchmarks, candidate adaptive computation formulations, and August 2026 – May 2027 Gantt roadmap.
- [x] **BTP-REP-02**: Two-column academic paper reading interface in `docs/` with sticky chapter navigation TOC, reading progress indicator, offline KaTeX equation rendering, collapsible code blocks, and interactive IEEE citation tooltips.
- [x] **BTP-REP-03**: Verification test suite `tests/test_academic_website.py` deterministically validating DOM structure, KaTeX math elements, and chapter navigation under `scripts/verify.ps1`.

### High-Coverage Test Suite & Pytest-Cov Integration (TEST-COV)

- [x] **TEST-COV-01**: Dedicated unit test suite `tests/test_dsp_edge_cases.py` targeting OS-CFAR, Capon/MUSIC AoA, MTI cancellers, Doppler windowing, and Range FFT scaling.
- [x] **TEST-COV-02**: Dedicated unit test suite `tests/test_radar_dataset.py` targeting synthetic `RadarDataset` generation, box coordinate math, multi-task heatmap encoding, and DataLoader collate functions (raising `src/models/radar_dataset.py` to >=90%).
- [x] **TEST-COV-03**: Automated integration smoke tests `tests/test_pipeline_scripts.py` covering `scripts/run_radar_pipeline.py`, `scripts/push_kaggle_kernel.py`, and notebook generators.
- [x] **TEST-COV-04**: Universal verification gate (`scripts/verify.ps1`) enforces `>=90%` code coverage with `pytest-cov` while maintaining deterministic, sub-30s local execution.

### Academic Portal Priority 0 Polish (PORTAL-P0 — Issues #21, #23)

- [x] **PORTAL-MOB-01**: Mobile navigation drawer (>=44x44px touch targets, smooth off-canvas transition, backdrop dismiss, body scroll lock, morphing toggle icon). *(Closes [#23](https://github.com/aryanthepain/Radar-BTP/issues/23))*
- [x] **PORTAL-MOB-02**: Two-tier KaTeX math & comparison table horizontal overflow containment (fluid font scaling with accessible floor 0.75rem / 11px tables, 0.85em KaTeX math, momentum scroll with edge-fade indicators, zero horizontal body scroll). *(Closes [#23](https://github.com/aryanthepain/Radar-BTP/issues/23))*
- [x] **PORTAL-MOB-03**: Single-column reflow & responsive media (two-column collapse below 900px, responsive typography scaling, `max-width: 100%; height: auto;` figure constraint). *(Closes [#23](https://github.com/aryanthepain/Radar-BTP/issues/23))*
- [ ] **PORTAL-CITE-01**: Always-active floating citation cards and bibliography previews for all 30 IEEE references in `CITATIONS_DB` without debug gate flag; renders title, authors, venue, year, direct DOI/arXiv hyperlink. *(Closes [#21](https://github.com/aryanthepain/Radar-BTP/issues/21))*
- [ ] **PORTAL-CITE-02**: Mobile touch tap-to-inspect & viewport collision avoidance: first tap opens preview; desktop (>600px) floating tooltip with boundary clamping; mobile (<600px) slide-up bottom-sheet with darkened backdrop, "View in Reference List" button with Section 9 pulse highlight (`.highlight-pulse`), and outside tap dismissal. *(Closes [#21](https://github.com/aryanthepain/Radar-BTP/issues/21))*
- [ ] **PORTAL-VERIF-01**: Deterministic unit and DOM smoke tests in `tests/test_showcase_website.py` and `tests/test_academic_website.py` verifying mobile viewport rules, overflow containment, touch targets, and citation preview rendering passing 100% under `scripts/verify.ps1`.

## Deferred to GitHub Issues (Post-Exploratory Backlog)

The following ingestion decoupling and verification expansion requirements have been migrated from active planning into dedicated GitHub issues:

### Multi-Level Decoupled Ingestion (DATA — Issues #17, #3)

- **DATA-01**: Pipeline can directly ingest raw 3D complex ADC radar cubes `(num_rx, num_chirps, num_samples)` from NumPy arrays, tensors, or `.npy`/`.npz`/`.mat` files without requiring `FMCWRadarSimulator`. *(Tracked in [#17](https://github.com/aryanthepain/Radar-BTP/issues/17))*
- **DATA-02**: Pipeline can directly ingest 2D Range-Doppler matrices (RDM) or 3D RAD tensors (e.g., RadDet tensor structure `(range, azimuth, doppler)`) directly into CFAR detection and deep learning modules, bypassing simulation and 1D/2D FFT processing. *(Tracked in [#17](https://github.com/aryanthepain/Radar-BTP/issues/17))*
- **DATA-03**: Pipeline can directly ingest tabular DataFrames or structured point clouds (`pd.DataFrame` with range, velocity, azimuth, power/rcs) directly into spatial clustering (DBSCAN) and downstream Cartesian tracking. *(Tracked in [#3](https://github.com/aryanthepain/Radar-BTP/issues/3))*
- **DATA-04**: Universal `RadarDataAdapter` abstraction providing schema inspection, shape validation, and automatic routing to the appropriate pipeline stage. *(Tracked in [#17](https://github.com/aryanthepain/Radar-BTP/issues/17))*

### Verification & Deterministic Gates (VERIF — Issues #3, #18, #19)

- **VERIF-01**: Unit test suite (`tests/test_radar_data_adapter.py`) validating decoupled ingestion across Level 1 (raw cube), Level 2 (RDM/RAD tensor), and Level 3 (point cloud DataFrame). *(Tracked in [#3](https://github.com/aryanthepain/Radar-BTP/issues/3))*
- **VERIF-02**: Universal deterministic verification gate (`pwsh -File ./scripts/verify.ps1`) passes cleanly with all unit tests, adapter smoke tests, and pipeline testbenches intact. *(Tracked in [#18](https://github.com/aryanthepain/Radar-BTP/issues/18) and [#19](https://github.com/aryanthepain/Radar-BTP/issues/19))*

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

| Requirement     | Phase        | Status                             |
| --------------- | ------------ | ---------------------------------- |
| PRES-01         | Phase 1      | Complete                           |
| PRES-02         | Phase 1      | Complete                           |
| PRES-03         | Phase 1      | Complete                           |
| PRES-04         | Phase 1      | Complete                           |
| RADDET-BENCH-01 | Phase 1.2    | Complete                           |
| RADDET-BENCH-02 | Phase 1.2    | Complete                           |
| PRES-WEB-01     | Phase 01.2.1 | Complete                           |
| PRES-WEB-02     | Phase 01.2.1 | Complete                           |
| PRES-WEB-03     | Phase 01.2.1 | Complete                           |
| BTP-REP-01      | Phase 01.2.2 | Complete                           |
| BTP-REP-02      | Phase 01.2.2 | Complete                           |
| BTP-REP-03      | Phase 01.2.2 | Complete                           |
| TEST-COV-01     | Phase 1.3    | Complete                           |
| TEST-COV-02     | Phase 1.3    | Complete                           |
| TEST-COV-03     | Phase 1.3    | Complete                           |
| TEST-COV-04     | Phase 1.3    | Complete                           |
| PORTAL-MOB-01   | Phase 3      | Complete (Plan 03-01, Issue #23)   |
| PORTAL-MOB-02   | Phase 3      | Complete (Plan 03-01, Issue #23)   |
| PORTAL-MOB-03   | Phase 3      | Complete (Plan 03-01, Issue #23)   |
| PORTAL-CITE-01  | Phase 3      | Pending (Issue #21)                |
| PORTAL-CITE-02  | Phase 3      | Pending (Issue #21)                |
| PORTAL-VERIF-01 | Phase 3      | Pending                            |
| DATA-01         | Backlog      | Deferred (Issue #17)               |
| DATA-02         | Backlog      | Deferred (Issue #17)               |
| DATA-03         | Backlog      | Deferred (Issue #3)                |
| DATA-04         | Backlog      | Deferred (Issue #17)               |
| VERIF-01        | Backlog      | Deferred (Issue #3)                |
| VERIF-02        | Backlog      | Deferred (Issues #18, #19)         |

**Coverage:**

- Completed exploratory requirements: 16 total (100% complete)
- Active Phase 3 requirements: 6 total (tracked in #21, #23)
- Deferred to GitHub Issues: 6 total (tracked in #3, #17, #18, #19)
- Unmapped: 0 ✓

---

_Requirements defined: 2026-09-23_
_Last updated: 2026-11-19 (Phase 3 added for GitHub Priority 0 Issues #21, #23)_
