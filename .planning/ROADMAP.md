# Roadmap: Radar-BTP

## Overview

A phased journey to prepare an undergraduate thesis exploratory presentation for the supervising professor, followed by internal architectural decoupling of radar data ingestion, and final testbench verification.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: Compartmentalized Jupyter Walkthroughs & Mermaid Diagrams** - Structure notebooks with unified Mermaid flowcharts and academic narrative for the professor presentation.
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
**Plans**: TBD

Plans:
- [ ] 01-01: Structure and enrich `01_radar_classical_dsp.ipynb` with top-level and section-by-section Mermaid diagrams and academic markdown.
- [ ] 01-02: Structure and enrich `02_radar_deep_learning_detection.ipynb` with deep learning Mermaid architecture diagrams and clear narrative explanations.

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

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Compartmentalized Jupyter Walkthroughs & Mermaid Diagrams | 0/2 | Not started | - |
| 2. Multi-Level Decoupled Radar Data Ingestion | 0/2 | Not started | - |
| 3. Pipeline Integration & Deterministic Verification Gates | 0/2 | Not started | - |
