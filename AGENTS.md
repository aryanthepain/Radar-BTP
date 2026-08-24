# AGENTS.md — Radar DSP & Deep Learning Detection Operating Context

> [!NOTE]
> Global behavioral invariants (Single-task delivery contract, Ponytail anti-bloat ladder, Karpathy surgical execution, Fleet loop verification) are inherited globally from `~/.gemini/config/rules/global_rules.md`.

## 1. Project Commands & Deterministic Gates
- **Run Full Pipeline Testbench**: `python scripts/run_radar_pipeline.py`
- **Run Unit Test Suite**: `python -m unittest discover -s tests`
- **Run Targeted Test**: `python -m unittest tests/test_radar_dsp.py`
- **Universal Verification**: `pwsh -File ./scripts/verify.ps1`
- **Audio Completion Alert**: `pwsh -File ./scripts/agent-alarm.ps1 -Type Success -SoundOnly`

## 2. Repository Architecture & Layout
- `src/sim/`: High-fidelity 77 GHz FMCW radar simulation (Chirp synthesizer, target RCS & kinematics, micro-Doppler pedestrian modulations, ground clutter & thermal noise).
- `src/dsp/`: Core Radar DSP primitives (1D Range FFT, MTI Clutter Filtering, 2D Slow-Time Doppler FFT, 2D CA/OS-CFAR, Spatial MUSIC/Capon AoA Estimator, DBSCAN Point Cloud Clustering).
- `src/models/`: AI/Deep Learning Radar Detectors (PyTorch `RadarObjectDetectorCNN` multi-task heatmap + bounding box regressor, `RadarDataset` generator, training routines).
- `scripts/`: End-to-end simulation, training, visualization testbenches (`run_radar_pipeline.py`), and verification scripts (`verify.ps1`, `agent-alarm.ps1`).
- `tests/`: Deterministic unit tests covering radar physics, DSP equations, clutter attenuation, CFAR detection, AoA resolution, and CNN gradient propagation.
- `data/`: Processed radar cubes, tensors, and datasets.

## 3. Project-Specific Invariants & Conventions
- **Language / Runtime**: Python 3.12+ (NumPy, SciPy, PyTorch 2.x, Matplotlib, Scikit-Learn).
- **Radar Equation Standards**: Maintain strict adherence to FMCW radar principles (Range resolution $\Delta R = \frac{c}{2B}$, Velocity resolution $\Delta v = \frac{\lambda}{2 N_{chirps} T_c}$, Spatial array steering vectors $a(\theta) = e^{-j 2\pi d \sin(\theta)/\lambda}$).
- **Skills & Rules**: Inherit global skills and rules (`~/.gemini/config/`) by default.

## 4. Ephemeral Memory (`WORKING.md`)
- Maintain active sprint objectives, test failure traces, hypotheses, and blockers in `WORKING.md`.

