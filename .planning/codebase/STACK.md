# Technology Stack

**Analysis Date:** 2026-09-23

## Languages

**Primary:**
- Python 3.12 (specifically 3.12.10 64-bit AMD64) — All core radar simulation, classical signal processing (DSP), neural network models, pipeline orchestration, and test suites.

**Secondary:**
- PowerShell 7 (`pwsh`) — Verification gate scripts (`scripts/verify.ps1`), speech and audio task completion alerts (`scripts/agent-alarm.ps1`).
- Bash / Shell — Git hooks (`.githooks/pre-commit`).

## Runtime

**Environment:**
- Python 3.12.10 local execution environment on Windows 11 AMD64 (x86_64).
- Offline / air-gapped capable; no external runtime microservices or cloud compute dependencies required.

**Package Manager:**
- pip 26.1.1 (standard Python package management).
- Lockfile / Environment: Global environment tracking with reproducible standard library and pre-installed scientific computing wheels.

## Frameworks

**Core & Deep Learning:**
- PyTorch 2.6.0+cpu (`torch`, `torchvision`, `torchaudio`) — Deep learning radar object detection framework, multi-task convolutional neural network architecture (`RadarObjectDetectorCNN`), BCE and Smooth L1 loss functions, and backpropagation engine.

**Scientific Computing & Signal Processing (DSP):**
- NumPy (v1.26+ / v2.x) — High-performance multidimensional arrays, raw 3D baseband radar cubes, fast-time and slow-time complex phase synthesis.
- SciPy 1.15.2 (`scipy.signal`, `scipy.fft`) — Digital signal processing primitives, Butterworth filter design, windowing functions, and STFT micro-Doppler time-frequency analysis.
- Scikit-Learn 1.8.0 (`sklearn.cluster.DBSCAN`) — Unsupervised density-based spatial clustering for radar point cloud grouping in Cartesian Bird's-Eye View (BEV).

**Visualization & Reporting:**
- Matplotlib 3.x (`matplotlib.pyplot`, `matplotlib.gridspec`) — Multi-panel publication-grade radar exploratory data analysis (EDA) and diagnostic dashboards.

**Testing:**
- Python `unittest` — Standard library deterministic test framework.
- Pytest 9.1.1 (`pytest`) — Primary test runner utilized by the universal verification gate (`scripts/verify.ps1`).

## Key Dependencies

**Critical:**
- `torch` 2.6.0+cpu — Multi-task anchor-free radar detection network for simultaneous classification and coordinate bounding box regression.
- `numpy` — Underpins all tensor structures: 3D complex baseband radar cubes `(num_rx, num_chirps, num_samples)`, 2D Range-Doppler matrices `(num_doppler, num_range)`, and spatial steering vectors.
- `scipy` 1.15.2 — Moving Target Indication (MTI) filtering, clutter attenuation, and time-frequency spectrogram computations.
- `scikit-learn` 1.8.0 — DBSCAN clustering of CFAR detection peaks into discrete object centroids with bounding boundaries.
- `matplotlib` — Automated generation of 9-panel radar dashboard artifacts (`data/processed/radar_pipeline_eda.png`).

**Infrastructure & Tooling:**
- `dataclasses` (Python standard library) — Strongly typed radar system parameters (`RadarConfig`) and target kinematics (`RadarTarget`).
- `System.Speech.Synthesis` (Windows PowerShell interop) — Spoken audio summaries for task completion and human checkpoints.

## Configuration

**Environment:**
- Device configuration: Default CPU execution (`device_str="cpu"`) with dynamic GPU fallback (`torch.cuda.is_available()`).
- No external environment variables or `.env` files required for core execution.

**Radar System Configuration:**
- Centralized hardware and waveform configuration defined in `src/sim/radar_config.py` (`RadarConfig` dataclass):
  - Carrier Frequency ($f_c$): 77.0 GHz
  - Chirp Sweep Bandwidth ($B$): 1.0 GHz (yielding $\Delta R = 0.15\text{ m}$)
  - Chirp Duration ($T_c$): 50.0 µs
  - ADC Fast-Time Samples ($N_s$): 256
  - Slow-Time Chirps ($N_c$): 128
  - Receiver Antennas ($N_{rx}$): 4 Uniform Linear Array (ULA) elements spaced at $\lambda / 2$
  - ADC Sampling Rate ($F_s$): 5.12 MHz

## Platform Requirements

**Development:**
- Windows 11 / Linux / macOS with Python 3.12+ and PowerShell 7+.
- No external hardware or dedicated radar physical transceivers required (all signals synthesized via high-fidelity physics simulator).

**Production / Evaluation:**
- Self-contained command-line pipeline execution: `python scripts/run_radar_pipeline.py`.
- Automated test gate: `pwsh -File ./scripts/verify.ps1`.

---

*Stack analysis: 2026-09-23*
*Update after major dependency changes*
