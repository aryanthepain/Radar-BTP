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

| Feature | Reason |
|---------|--------|
| Downloading multi-GB RadDet datasets in v1 | Deferred until professor delivers formal thesis problem statement. |
| External web app dashboard (Streamlit / React) | Excluded to keep existing Jupyter notebooks self-contained and directly presentable. |
| Real-time physical radar SDR streaming in v1 | Requires physical hardware setup; exploratory phase focuses on algorithmic perception and data decoupling. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PRES-01 | Phase 1 | Pending |
| PRES-02 | Phase 1 | Pending |
| PRES-03 | Phase 1 | Pending |
| PRES-04 | Phase 1 | Pending |
| DATA-01 | Phase 2 | Pending |
| DATA-02 | Phase 2 | Pending |
| DATA-03 | Phase 2 | Pending |
| DATA-04 | Phase 2 | Pending |
| VERIF-01 | Phase 2 | Pending |
| VERIF-02 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 10 total
- Mapped to phases: 10
- Unmapped: 0 ✓

---
*Requirements defined: 2026-09-23*
*Last updated: 2026-09-23 after initial definition*
