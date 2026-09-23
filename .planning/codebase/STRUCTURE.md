# Codebase Structure

**Analysis Date:** 2026-09-23

## Directory Layout

```
BTP/
├── .githooks/                               # Local git hooks
│   └── pre-commit                           # Pre-commit test runner hook
├── data/                                    # Data artifacts and outputs
│   └── processed/                           # Processed figures and evaluation tensors
│       ├── .gitkeep
│       └── radar_pipeline_eda.png           # 9-panel radar pipeline visualization
├── scripts/                                 # CLI testbenches, verification, and utilities
│   ├── agent-alarm.ps1                      # Spoken voice and audio completion alert
│   ├── build_walkthrough_notebooks.py       # Notebook builder script
│   ├── run_radar_pipeline.py                # End-to-end simulation & DSP demo
│   └── verify.ps1                           # Universal deterministic verification gate
├── src/                                     # Source code root
│   ├── dsp/                                 # Classical Radar DSP modules
│   │   ├── aoa_estimation.py                # Spatial FFT, Capon MVDR, MUSIC AoA
│   │   ├── cfar_detector.py                 # 2D CA, OS, GOCA, SOCA CFAR detection
│   │   ├── clustering.py                    # Cartesian BEV DBSCAN point clustering
│   │   ├── clutter_removal.py               # MTI slow-time clutter suppression
│   │   ├── doppler_processing.py            # Slow-time Doppler FFT & micro-Doppler STFT
│   │   ├── radar_pipeline.py                # Unified classical DSP pipeline facade
│   │   └── range_processing.py              # Fast-time 1D Range FFT
│   ├── models/                              # Deep learning radar models
│   │   ├── radar_dataset.py                 # PyTorch synthetic radar dataset generator
│   │   ├── radar_detector_cnn.py            # Multi-task heatmap & box regressor FCN
│   │   └── train_detector.py                # Neural network training & validation loop
│   └── sim/                                 # High-fidelity FMCW radar simulation
│       ├── radar_config.py                  # Hardware parameters & radar equations
│       ├── radar_sim.py                     # Complex baseband I/Q raw ADC cube simulator
│       └── target.py                        # Kinematic radar targets & traffic scenarios
├── tests/                                   # Deterministic unit test suite
│   └── test_radar_dsp.py                    # Unit tests covering physics, DSP, & CNN
├── 01_radar_classical_dsp.ipynb             # Interactive Classical Radar DSP walkthrough
├── 02_radar_deep_learning_detection.ipynb   # Interactive Deep Learning Radar walkthrough
├── AGENTS.md                                # Agent operating context & invariants
├── CONSTITUTION.md                          # Non-negotiable math & architectural boundaries
├── WORKING.md                               # Active sprint scratchpad & status
└── *.pdf                                    # Academic literature reference papers
```

## Directory Purposes

**`src/sim/`:**
- Purpose: High-fidelity physical simulation of 77 GHz FMCW radar waveforms.
- Contains: Dataclasses for radar system configuration and kinematic targets, multi-channel I/Q beat signal synthesis.
- Key files:
  - `src/sim/radar_config.py` — Hardware constants and physical equations ($\Delta R$, $\Delta v$, $\lambda$, chirp slope).
  - `src/sim/target.py` — Multi-target scenario generator with pedestrian micro-Doppler kinematics.
  - `src/sim/radar_sim.py` — Vectorized 3D baseband radar cube synthesis `(num_rx, num_chirps, num_samples)`.

**`src/dsp/`:**
- Purpose: Classical Radar Signal Processing pipeline.
- Contains: Fast-time Range FFT, MTI Clutter Filtering, Doppler FFT, 2D CFAR detection, Spatial Angle-of-Arrival (AoA) estimation, and DBSCAN clustering.
- Key files:
  - `src/dsp/range_processing.py` — Windowed 1D Range FFT.
  - `src/dsp/clutter_removal.py` — Moving Target Indication (MTI) filter (>15 dB suppression).
  - `src/dsp/doppler_processing.py` — 2D Range-Doppler Matrix and micro-Doppler STFT.
  - `src/dsp/cfar_detector.py` — 2D CA/OS/GOCA/SOCA CFAR with 3x3 local peak extraction.
  - `src/dsp/aoa_estimation.py` — Spatial FFT, Capon, and Subspace MUSIC AoA.
  - `src/dsp/clustering.py` — Cartesian BEV projection and DBSCAN object grouping.
  - `src/dsp/radar_pipeline.py` — Unified end-to-end DSP orchestrator.

**`src/models/`:**
- Purpose: Deep learning perception and object detection on radar tensors.
- Contains: PyTorch synthetic dataset generator, convolutional multi-task architecture, and training routines.
- Key files:
  - `src/models/radar_dataset.py` — On-the-fly multi-target scene and heatmap generator.
  - `src/models/radar_detector_cnn.py` — Fully convolutional neural network with residual blocks and dual heads.
  - `src/models/train_detector.py` — Training loop with AdamW, Cosine Annealing, and validation metrics.

**`scripts/`:**
- Purpose: Executable testbenches, automated verification gates, and developer notification tooling.
- Key files:
  - `scripts/run_radar_pipeline.py` — End-to-end simulation, DSP, CNN training, and visualization export.
  - `scripts/verify.ps1` — Universal deterministic verification gate.
  - `scripts/agent-alarm.ps1` — Spoken audio notification generator.
  - `scripts/build_walkthrough_notebooks.py` — Regenerates interactive Jupyter notebooks.

**`tests/`:**
- Purpose: Deterministic regression tests.
- Key files:
  - `tests/test_radar_dsp.py` — 7 comprehensive unit tests verifying radar physics, range FFT, Doppler FFT, clutter attenuation, CFAR detection, MUSIC AoA accuracy, and CNN backpropagation.

**`data/processed/`:**
- Purpose: Stores generated visualization artifacts and exported models/tensors.
- Key files:
  - `data/processed/radar_pipeline_eda.png` — Publication-grade 9-panel dashboard.

## Key File Locations

**Entry Points:**
- Pipeline Testbench: `scripts/run_radar_pipeline.py`
- Verification Gate: `scripts/verify.ps1`
- Interactive DSP Notebook: `01_radar_classical_dsp.ipynb`
- Interactive CNN Notebook: `02_radar_deep_learning_detection.ipynb`

**Configuration:**
- Radar Hardware & Waveform: `src/sim/radar_config.py`
- Repository Operating Rules: `AGENTS.md`
- Non-Negotiable Math Invariants: `CONSTITUTION.md`
- Active Sprint Memory: `WORKING.md`

**Core Logic:**
- Radar Simulation: `src/sim/radar_sim.py`
- Unified DSP Chain: `src/dsp/radar_pipeline.py`
- Deep Learning Architecture: `src/models/radar_detector_cnn.py`

**Testing:**
- Unit Tests: `tests/test_radar_dsp.py`

## Naming Conventions

**Files:**
- `snake_case.py` for all Python modules (`range_processing.py`, `cfar_detector.py`).
- `test_*.py` for test files (`tests/test_radar_dsp.py`).
- `UPPERCASE.md` for project operating specifications (`AGENTS.md`, `CONSTITUTION.md`, `WORKING.md`).
- `kebab-case.ps1` for scripts (`agent-alarm.ps1`, `verify.ps1`).

**Classes & Functions:**
- `PascalCase` for classes (`RadarConfig`, `RadarTarget`, `CFARDetector2D`, `RadarObjectDetectorCNN`).
- `snake_case` for methods and functions (`process_radar_cube`, `estimate_aoa_music`).
- `UPPER_SNAKE_CASE` for physical constants and global maps (`SPEED_OF_LIGHT`, `CLASS_MAP`, `NUM_CLASSES`).

## Where to Add New Code

**New Radar DSP Algorithm (e.g., EKF Tracking / Doppler Disambiguation):**
- Implementation: `src/dsp/<feature_name>.py`
- Integration: Hook into `src/dsp/radar_pipeline.py`
- Unit tests: Add test case in `tests/test_radar_dsp.py`

**New Deep Learning Architecture (e.g., Transformer / PointNet on Radar):**
- Implementation: `src/models/<model_name>.py`
- Dataset / Loader: Extend `src/models/radar_dataset.py` if custom tensor representation needed
- Training script: Extend `src/models/train_detector.py`
- Tests: Add forward/loss test in `tests/test_radar_dsp.py`

**Real Dataset Ingestion (e.g., RADDet / CARRADA):**
- Loader / Parser: `src/sim/dataset_loaders/` or `src/models/datasets/`
- Data storage: Raw or converted tensors in `data/raw/` or `data/processed/`

---

*Structure analysis: 2026-09-23*
*Update when directory structure changes*
