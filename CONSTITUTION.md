# CONSTITUTION.md — Architectural Invariants & Trust Boundaries

> **Purpose:** Non-negotiable technical, mathematical, and architectural constraints for this Radar DSP & AI Detection repository. All AI agents must strictly comply with these rules.

---

## 1. Technical Stack & Mathematical Invariants
- **Primary Language & Runtime**: Python 3.12+ (NumPy, SciPy, PyTorch 2.x, Matplotlib, Scikit-Learn).
- **Physical Radar Physics**:
  - Speed of light constant: $c = 299,792,458\text{ m/s}$.
  - Wavelength: $\lambda = c / f_c$.
  - Range bin calculation: $R = \frac{c \cdot f_b}{2 S}$ where slope $S = \text{Bandwidth} / T_c$.
  - Radial velocity: $v = \frac{\lambda \cdot f_d}{2}$.
- **Radar Tensors Shape Invariants**:
  - Raw ADC Cube: `(num_rx, num_chirps, num_samples)`
  - Range-Doppler Matrix: `(num_rx, num_doppler, num_range)`
  - CNN Input Tensor: `(batch_size, channels, num_doppler, num_range)`
- **Deterministic Testing**: Every DSP module must include unit tests with bounded error tolerances linked to theoretical radar resolutions ($\Delta R$, $\Delta v$, $\Delta \theta$).

---

## 2. Security Boundaries & Execution Safety
- **Zero Hardcoded Secrets**: No credentials or private paths in source code.
- **No Destructive File Deletions**: Never wipe processed radar data or test fixtures without confirmation.
- **Resource Attribution**: Optimize memory allocations when processing large 4D radar tensors (Rx × Tx × Chirps × Samples) to prevent OOM errors.

---

## 3. Dependency Management Policy
- **Zero Speculative Dependencies**: Stick to standard scientific computing stack (`numpy`, `scipy`, `torch`, `matplotlib`, `scikit-learn`). No redundant heavy frameworks.

---

## 4. Code Quality & Verification Gates
- **Deterministic Gate**: All code modifications must pass `./scripts/verify.ps1` before completion.
- **Backward Compatibility**: Preserve existing DSP primitive APIs (`RangeProcessor`, `DopplerProcessor`, `CFARDetector2D`, `AngleEstimator`, `ClutterFilter`).

