# Coding Conventions

**Analysis Date:** 2026-09-23

## Naming Patterns

**Files:**
- `snake_case.py` for all Python modules (`radar_config.py`, `cfar_detector.py`, `aoa_estimation.py`).
- `test_*.py` for test suites (`tests/test_radar_dsp.py`).
- `*.ps1` (kebab-case) for PowerShell automation and alarms (`agent-alarm.ps1`, `verify.ps1`).
- `UPPERCASE.md` for repo-level governance contracts (`AGENTS.md`, `CONSTITUTION.md`, `WORKING.md`).

**Classes:**
- `PascalCase` for all classes (`RadarConfig`, `RadarTarget`, `FMCWRadarSimulator`, `RangeProcessor`, `ClutterFilter`, `DopplerProcessor`, `CFARDetector2D`, `AngleEstimator`, `RadarClusterer`, `ClassicalRadarPipeline`, `RadarDataset`, `RadarObjectDetectorCNN`).

**Functions & Methods:**
- `snake_case` for all functions and methods (`process_radar_cube`, `generate_radar_cube`, `estimate_aoa_music`, `cluster_detections`).
- `_prefix_snake_case` for private or internal helper methods (e.g., `_get_window`, `_generate_random_scene`).

**Variables & Attributes:**
- `snake_case` for standard variables and tensor identifiers (`radar_cube`, `range_axis`, `velocity_axis`, `rdm_power_db`).
- Suffix physical units explicitly where ambiguity could arise:
  - `_m` for meters (`range_m`, `x_m`, `y_m`)
  - `_mps` for meters per second (`velocity_mps`)
  - `_deg` for degrees (`azimuth_deg`)
  - `_rad` for radians (`theta_rad`, `angles_rad`)
  - `_db` or `_dbsm` for decibels (`snr_db`, `rcs_dbsm`, `clutter_attenuation_db`)
  - `_hz` for hertz (`sampling_rate`, `fc`, `bandwidth`)
  - `_s` for seconds (`chirp_duration`)

**Constants:**
- `UPPER_SNAKE_CASE` for global physical constants and dictionaries (`SPEED_OF_LIGHT`, `CLASS_MAP`, `NUM_CLASSES`).

## Code Style

**Formatting:**
- Standard Python PEP 8 formatting.
- 4-space indentation; no hard tabs.
- Line length target: 88–100 characters max, wrapping mathematical equations cleanly.

**Type Annotations:**
- Comprehensive type hints across all function and method signatures using Python `typing` (`Tuple`, `List`, `Dict`, `Optional`, `Literal`):
  ```python
  def process(self, radar_cube: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
  ```
- PyTorch tensors typed as `torch.Tensor`; multidimensional arrays typed as `np.ndarray`.

**Documentation & Docstrings:**
- Triple-quoted docstrings on all classes and public methods.
- Document input/output shapes, tensor dimensional semantics (e.g., `(num_rx, num_chirps, num_samples)`), and physical units.
- Include mathematical formulas in LaTeX or plain notation (e.g., $c / (2B)$, $\lambda / (2 N_c T_c)$).

## Import Organization

**Order:**
1. Standard library imports (`os`, `sys`, `time`, `dataclasses`, `typing`).
2. Third-party scientific & deep learning libraries (`numpy`, `scipy`, `torch`, `matplotlib`, `sklearn`).
3. Local project imports in dependency order (`src.sim.*` $\to$ `src.dsp.*` $\to$ `src.models.*`).

**Example:**
```python
import os
import sys
from typing import List, Dict, Tuple, Optional

import numpy as np
from scipy import signal
import torch
import torch.nn as nn
from sklearn.cluster import DBSCAN

from src.sim.radar_config import RadarConfig, SPEED_OF_LIGHT
from src.sim.target import RadarTarget
from src.dsp.range_processing import RangeProcessor
from src.dsp.cfar_detector import CFARDetector2D
```

**Path Management:**
- Workspace root added to `sys.path` in scripts and tests to support direct CLI invocation:
  ```python
  sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
  ```

## Error Handling & Numerical Stability

**Mathematical Guarding:**
- Never perform unconditional division or logarithm without protection:
  ```python
  # Log power in dB:
  power_db = 10.0 * np.log10(np.maximum(power_linear, 1e-12))
  
  # Matrix inversion diagonal loading:
  r_xx += 1e-6 * np.eye(num_rx)
  r_inv = np.linalg.pinv(r_xx)
  
  # Angular arcsin clipping:
  sin_theta = np.clip(sin_theta, -1.0, 1.0)
  ```

**Graceful Degradation:**
- In clustering and peak detection, return empty lists `[]` rather than crashing if zero targets are detected in an empty scene.

## Logging & Console Output

**Patterns:**
- Console printing formatted with stage prefixes for clear terminal UX:
  - `[*] Initializing ...`
  - `[+] Succeeded / Completed ...`
  - `[-] Warning / Filtered ...`
  - `❌ Failed ...`
- Key metrics logged with explicit units:
  ```python
  print(f"[+] Range Resolution: {cfg.range_resolution:.3f} m")
  print(f"[+] Clutter Attenuation: {dsp_results['clutter_attenuation_db']:.2f} dB")
  ```

## Function & Module Design

**Single Responsibility:**
- Each module in `src/dsp/` encapsulates exactly one radar signal processing primitive (Range FFT, Clutter Filtering, Doppler FFT, CFAR, AoA, Clustering).
- The `ClassicalRadarPipeline` facade ties them together without polluting individual primitives.

**Stateless Processing:**
- Processors accept input arrays and return transformed arrays and coordinate axes without modifying input tensors in-place.

---

*Convention analysis: 2026-09-23*
*Update when patterns change*
