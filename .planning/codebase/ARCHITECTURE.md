# Architecture

**Analysis Date:** 2026-09-23

## Pattern Overview

**Overall:** Hybrid Classical Radar DSP & Deep Learning Detection Pipeline

**Key Characteristics:**
- **Physics-Grounded Modular Architecture**: Strict separation of concerns between radar waveform physics simulation, classical signal processing primitives, PyTorch neural network detection, and spatial clustering.
- **Dual-Phase Target Detection**: Supports both classical CFAR thresholding with subspace Angle-of-Arrival (AoA) estimation and modern deep learning anchor-free heatmap and bounding box regression on Range-Doppler representations.
- **Deterministic Mathematical Guarantees**: Core algorithms are bounded by closed-form FMCW radar resolution physics ($\Delta R = \frac{c}{2B}$, $\Delta v = \frac{\lambda}{2 N_c T_c}$, $a(\theta) = e^{-j 2\pi d \sin(\theta)/\lambda}$).

## Layers

```
┌─────────────────────────────────────────────────────────────┐
│                 Orchestration & Presentation                │
│    scripts/run_radar_pipeline.py, 01_classical_dsp.ipynb,   │
│         02_deep_learning.ipynb, scripts/verify.ps1          │
└──────────────────────────────┬──────────────────────────────┘
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼                                               ▼
┌──────────────────────────────┐       ┌──────────────────────────────┐
│     Classical DSP Layer      │       │     Deep Learning Layer      │
│         (`src/dsp/`)         │       │        (`src/models/`)       │
│  - RangeProcessor (1D FFT)   │       │  - RadarDataset (Loader)     │
│  - ClutterFilter (MTI)       │       │  - RadarObjectDetectorCNN    │
│  - DopplerProcessor (2D FFT) │       │  - train_radar_detector      │
│  - CFARDetector2D (CA/OS)    │       │  - Multi-task Loss (BCE/L1)  │
│  - AngleEstimator (MUSIC)    │       │                              │
│  - RadarClusterer (DBSCAN)   │       │                              │
└──────────────┬───────────────┘       └──────────────┬───────────────┘
               │                                      │
               └───────────────────────┬──────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      Simulation Layer                       │
│                        (`src/sim/`)                         │
│  - RadarConfig (Hardware constants, radar equations)        │
│  - RadarTarget (Kinematics, RCS, micro-Doppler gait)        │
│  - FMCWRadarSimulator (Raw baseband I/Q ADC cube generator) │
└─────────────────────────────────────────────────────────────┘
```

### 1. Simulation Layer (`src/sim/`)
- **Purpose**: High-fidelity synthesis of 77 GHz FMCW baseband dechirped beat signals for multi-target scenarios with environmental clutter and thermal noise.
- **Modules**:
  - `src/sim/radar_config.py`: Defines the `RadarConfig` dataclass storing physical constants ($c, f_c, B, T_c, N_s, N_c, N_{rx}, F_s$) and calculating derived properties ($\lambda, S, \Delta R, R_{max}, \Delta v, v_{max}$).
  - `src/sim/target.py`: Defines `RadarTarget` representing kinematic properties (range, velocity, azimuth angle, RCS in dBsm, class label) and micro-Doppler gait parameters (`micro_doppler_freq`, `micro_doppler_amp`). Provides `create_standard_traffic_scenario()`.
  - `src/sim/radar_sim.py`: `FMCWRadarSimulator` generates a 3D complex baseband radar cube of shape `(num_rx, num_chirps, num_samples)` via vector broadcasting over fast-time, slow-time, and spatial antenna indices. Injects Rayleigh ground clutter and complex AWGN thermal noise.

### 2. Classical DSP Layer (`src/dsp/`)
- **Purpose**: Executes deterministic radar signal processing transformations from raw time-domain ADC data to clustered Cartesian Bird's-Eye View (BEV) targets.
- **Modules**:
  - `src/dsp/range_processing.py`: `RangeProcessor` applies Hann windowing and 1D Fast-Time FFT along the ADC sample dimension to produce calibrated 1D range profiles.
  - `src/dsp/clutter_removal.py`: `ClutterFilter` implements slow-time Moving Target Indication (MTI) via slow-time mean subtraction, 2-pulse, 3-pulse delay-line cancelers, or Butterworth high-pass filters (>15 dB static clutter suppression).
  - `src/dsp/doppler_processing.py`: `DopplerProcessor` applies Hann windowing and 2D Slow-Time Doppler FFT with `fftshift` to produce 2D Range-Doppler Matrices (RDMs). Also computes Short-Time Fourier Transform (STFT) for pedestrian micro-Doppler spectrograms.
  - `src/dsp/cfar_detector.py`: `CFARDetector2D` applies 2D Cell-Averaging (CA), Ordered-Statistic (OS), Greatest-Of (GOCA), or Smallest-Of (SOCA) adaptive noise floor estimation with guard/training cells and 3x3 local peak extraction.
  - `src/dsp/aoa_estimation.py`: `AngleEstimator` estimates target azimuth across the Uniform Linear Array (ULA) using Spatial FFT, Capon (MVDR), and high-resolution Subspace MUSIC ($P_{MUSIC}(\theta) = \frac{1}{\| U_n^H a(\theta) \|^2}$).
  - `src/dsp/clustering.py`: `RadarClusterer` projects polar detections $(R, \theta)$ to Cartesian coordinates $(X, Y)$ and clusters detections into discrete objects using DBSCAN.
  - `src/dsp/radar_pipeline.py`: `ClassicalRadarPipeline` serves as the unified facade chaining the full DSP workflow.

### 3. Deep Learning Layer (`src/models/`)
- **Purpose**: Neural network detection and semantic classification directly from Range-Doppler heatmaps.
- **Modules**:
  - `src/models/radar_dataset.py`: PyTorch `Dataset` that generates diverse multi-target radar scenes on the fly with ground-truth 2D Gaussian splat heatmaps and bounding box targets `[range_center, velocity_center, width_r, width_v]`.
  - `src/models/radar_detector_cnn.py`: `RadarObjectDetectorCNN` fully convolutional network featuring residual blocks and dual prediction heads: class heatmap logits and box coordinate regressions. Implements multi-task loss (BCE + Masked Smooth L1).
  - `src/models/train_detector.py`: `train_radar_detector` implements training and validation loops with AdamW and Cosine Annealing learning rate scheduling.

### 4. Orchestration & Presentation Layer (`scripts/`, notebooks)
- **Purpose**: End-to-end integration, visualization, interactive research notebooks, and verification gates.
- **Modules**:
  - `scripts/run_radar_pipeline.py`: Comprehensive testbench running full simulation, classical DSP, CNN training, and 9-panel EDA visualization generation saved to `data/processed/radar_pipeline_eda.png`.
  - `01_radar_classical_dsp.ipynb`: Interactive Jupyter walkthrough for classical FMCW physics and DSP.
  - `02_radar_deep_learning_detection.ipynb`: Interactive Jupyter walkthrough for deep learning radar detection.
  - `scripts/verify.ps1`: Zero-cost deterministic test gate executing `pytest` or `unittest`.
  - `scripts/agent-alarm.ps1`: Spoken audio completion alert utility.

## Data Flow

### Classical Radar DSP Lifecycle:
1. **Waveform Synthesis**: `FMCWRadarSimulator` generates 3D complex baseband radar cube `(num_rx, num_chirps, num_samples)`.
2. **Fast-Time Range FFT**: `RangeProcessor` windows ADC samples and performs 1D FFT along the sample axis $\to$ Range Cube `(num_rx, num_chirps, num_range)`.
3. **Clutter Suppression**: `ClutterFilter` subtracts slow-time mean across chirps $\to$ Filtered Range Cube.
4. **Slow-Time Doppler FFT**: `DopplerProcessor` windows across chirps and performs FFT with `fftshift` $\to$ Range-Doppler Matrix (RDM) `(num_rx, num_doppler, num_range)`.
5. **Adaptive CFAR Thresholding**: `CFARDetector2D` slides over the 2D power map to identify target peaks exceeding the adaptive noise floor $\to$ candidate detections.
6. **Subspace AoA Estimation**: `AngleEstimator` takes the complex Rx snapshot across antenna elements for each detected bin and computes the MUSIC pseudo-spectrum $\to$ Azimuth angle $\theta$.
7. **Spatial Clustering**: `RadarClusterer` converts $(R, \theta)$ to Cartesian $(X, Y)$ and clusters points via DBSCAN $\to$ discrete tracked object entities.

### Deep Learning Detection Lifecycle:
1. **Input Map**: Normalized Range-Doppler power map $\to$ PyTorch tensor `(batch_size, 1, num_doppler, num_range)`.
2. **Backbone & Stem**: Convolutional stem followed by residual blocks extract multi-scale spatial-Doppler features.
3. **Multi-Task Heads**:
   - Class Heatmap Head: Outputs class probabilities for background, car, pedestrian, cyclist, drone.
   - Box Head: Sigmoid-activated coordinates `[r_norm, v_norm, width_r, width_v]`.
4. **Loss & Backpropagation**: Total Loss = BCE(heatmap) + $2.0 \times$ Smooth L1(box coordinates over foreground mask).

## Key Abstractions

- `RadarConfig` (`src/sim/radar_config.py`): Immutable system parameter configuration encapsulating all physical radar parameters.
- `RadarTarget` (`src/sim/target.py`): Physics and kinematic representation of a reflecting object in 3D radar space.
- `ClassicalRadarPipeline` (`src/dsp/radar_pipeline.py`): High-level facade pattern orchestrating the 6 sequential DSP primitives.
- `RadarObjectDetectorCNN` (`src/models/radar_detector_cnn.py`): PyTorch `nn.Module` implementing multi-task anchor-free radar perception.

## Entry Points

- **Full Pipeline Demonstration**: `python scripts/run_radar_pipeline.py`
  - Runs simulation, DSP, neural network training, and exports the 9-panel figure.
- **Deterministic Test Gate**: `pwsh -File ./scripts/verify.ps1`
  - Runs pytest/unittest suite across all DSP physics equations and CNN gradient propagation.
- **Targeted Test Execution**: `python -m unittest tests/test_radar_dsp.py`
- **Interactive Academic Notebooks**:
  - `01_radar_classical_dsp.ipynb`
  - `02_radar_deep_learning_detection.ipynb`

## Error Handling

- **Numerical Guarding**:
  - Power in dB: `10.0 * np.log10(np.maximum(power, 1e-12))` protects against `log(0)`.
  - Matrix Inversion: Diagonal loading (`1e-6 * np.eye(num_rx)`) added to sample covariance matrix $R_{xx}$ before pseudoinverse calculation in Capon and MUSIC.
  - Spatial Frequency Clipping: `arcsin` input clipped to $[-1.0, 1.0]$ to eliminate invalid spatial frequencies.
- **Deterministic Assertions**:
  - Unit tests verify estimation accuracy relative to physical radar resolution ($\Delta R, \Delta v$).

## Cross-Cutting Concerns

- **Reproducibility**: Explicit random seeding (`seed=42`) across simulation and dataset generation.
- **Tensor Shape Contracts**: Strict invariant validation of tensor dimensions across all transformations (`(num_rx, num_chirps, num_samples)` $\to$ `(num_rx, num_doppler, num_range)` $\to$ `(batch, channels, H, W)`).
- **Zero-Waste Execution**: Fast, self-contained CPU execution (<25 seconds for the complete test suite).

---

*Architecture analysis: 2026-09-23*
*Update when major patterns change*
