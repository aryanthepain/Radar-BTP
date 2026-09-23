# Testing Patterns

**Analysis Date:** 2026-09-23

## Test Framework

**Runner:**
- `pytest` 9.1.1 (primary test engine executed by `scripts/verify.ps1`).
- Python standard library `unittest` (fully compatible runner).

**Run Commands:**
```powershell
# Universal deterministic verification gate (mypy + pytest/unittest):
pwsh -File ./scripts/verify.ps1

# Run full test suite with pytest:
pytest -q

# Run full test suite with standard library unittest:
python -m unittest discover -s tests

# Run targeted test file:
python -m unittest tests/test_radar_dsp.py

# Run targeted test case:
python -m unittest tests.test_radar_dsp.TestRadarDSP.test_range_fft_accuracy
```

## Test File Organization

**Location:**
- Dedicated `tests/` directory at the project root.
- File naming: `test_*.py`.

**Structure:**
```
tests/
└── test_radar_dsp.py        # Complete DSP primitives & deep learning regression suite
```

## Test Structure & Patterns

**Suite Organization:**
```python
import unittest
import numpy as np
import torch

from src.sim.radar_config import RadarConfig, SPEED_OF_LIGHT
from src.sim.target import RadarTarget
from src.sim.radar_sim import FMCWRadarSimulator
from src.dsp.range_processing import RangeProcessor
from src.dsp.radar_pipeline import ClassicalRadarPipeline
from src.models.radar_detector_cnn import RadarObjectDetectorCNN, NUM_CLASSES

class TestRadarDSP(unittest.TestCase):

    def setUp(self):
        """Initializes canonical 77 GHz radar configuration and simulator fixture."""
        self.config = RadarConfig(
            fc=77e9,
            bandwidth=1.0e9,
            chirp_duration=50e-6,
            num_samples=256,
            num_chirps=128,
            num_rx=4,
            sampling_rate=5.12e6
        )
        self.sim = FMCWRadarSimulator(self.config)
```

**Physics-Bound Deterministic Assertions:**
- Unlike typical software tests that assert exact equality on floating-point values, radar signal processing tests assert that estimation errors are bounded by theoretical physical resolutions:
  1. **Range Estimation Accuracy**:
     $$\text{Error}_R = |\hat{R} - R_{\text{true}}| < \Delta R = \frac{c}{2B}$$
  2. **Radial Velocity Estimation Accuracy**:
     $$\text{Error}_v = |\hat{v} - v_{\text{true}}| < 1.5 \times \Delta v = 1.5 \times \frac{\lambda}{2 N_c T_c}$$
  3. **Angle-of-Arrival (AoA) Resolution**:
     $$\text{Error}_\theta = |\hat{\theta} - \theta_{\text{true}}| < 2.0^\circ$$
  4. **Clutter Attenuation**:
     $$\text{CA}_{\text{dB}} = 10 \log_{10}\left(\frac{P_{\text{raw}}}{P_{\text{filtered}}}\right) > 15.0\text{ dB}$$
  5. **Neural Gradient Propagation**:
     $$\text{Norm}(\nabla_{\theta} \mathcal{L}) > 0.0$$

## Test Inventory in `tests/test_radar_dsp.py`

| Test Method | Physics / DSP Principle Verified | Pass Criteria |
| :--- | :--- | :--- |
| `test_radar_config_physics` | FMCW equations ($\lambda$, $\Delta R$, $\Delta v$) | Matches theoretical values to $10^{-4}$ precision |
| `test_range_fft_accuracy` | 1D Fast-Time Range FFT peak recovery | Range error $< \Delta R$ ($0.15\text{ m}$) |
| `test_doppler_fft_accuracy` | 2D Slow-Time Doppler FFT velocity recovery | Velocity error $< 1.5 \times \Delta v$ ($0.45\text{ m/s}$) |
| `test_clutter_filter_attenuation` | Slow-time MTI mean subtraction | Clutter attenuation $> 15.0\text{ dB}$ on stationary targets |
| `test_cfar_detector_2d` | 2D CA-CFAR adaptive threshold detection | Detects target at $(18\text{ m}, -6\text{ m/s})$ above noise |
| `test_music_aoa_estimation` | Subspace MUSIC algorithm on 4-element ULA | Azimuth angle error $< 2.0^\circ$ |
| `test_radar_cnn_forward_and_loss` | PyTorch FCN forward pass, composite loss, backprop | Valid tensor shapes, non-NaN loss, non-zero gradient norm |

## Mocking & Synthetic Fixtures

**Physics Simulation as Deterministic Fixture:**
- Instead of external mocks, the test suite uses `FMCWRadarSimulator.generate_radar_cube` with fixed random seeds (`seed=42`).
- Provides reproducible, exact signal-to-noise ratio (SNR) and clutter levels across all operating systems without network or file I/O dependencies.

## Coverage & Verification Gates

**Gate Integration:**
- Script: `scripts/verify.ps1` runs before any phase milestone is achieved.
- Pre-commit Hook: `.githooks/pre-commit` verifies that all 7 tests pass before allowing a git commit.
- Verification runtime: ~1.5–22s depending on Python process startup.

---

*Testing analysis: 2026-09-23*
*Update when test patterns change*
