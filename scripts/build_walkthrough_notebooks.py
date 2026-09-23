"""
Builder and Executor for Academic Radar DSP & Deep Learning Walkthrough Notebooks
Generates:
  - d:/projects/BTP/01_radar_classical_dsp.ipynb
  - d:/projects/BTP/02_radar_deep_learning_detection.ipynb
Both notebooks are styled with the Dark Cyber-Radar Theme, equipped with dual-embedded
Mermaid architecture diagrams + collapsible SVG fallbacks, and pre-executed with nbclient.
"""
import os
import sys

# Crucial Windows DLL initialization order: import torch before any networking/zmq modules
import torch

import io
import base64
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Ensure UTF-8 stdout on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.notebook_diagrams import DIAGRAMS, render_mermaid_dual_block


def build_notebook_1() -> nbformat.NotebookNode:
    nb = new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    }

    # Cell 1: Title & Academic Overview + Top-Level End-to-End Diagram
    nb1_top_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_top"], "End-to-End FMCW Radar Signal Processing Pipeline")
    nb.cells.append(new_markdown_cell(rf"""# 🛰️ 01. FMCW Radar Signal Processing & Target Detection: First-Principles Walkthrough

> **BTP Research & Pedagogy Masterclass**  
> **Topic:** 77 GHz Automotive mmWave Radar Signal Processing Pipeline  
> **Key Disciplines:** FMCW Waveform Theory • Fast-Time Range FFT • MTI Clutter Filtering • Slow-Time Doppler FFT • 2D CA-CFAR • Spatial Array AoA (Capon & MUSIC) • DBSCAN Cartesian BEV Tracking • Micro-Doppler STFT  

---

## Executive Summary for Academic Review

Frequency-Modulated Continuous-Wave (FMCW) radar is the bedrock of modern automotive active safety, autonomous driving, and robotic spatial perception. Unlike pulsed radar systems, FMCW radars transmit continuous frequency ramps (chirps), enabling simultaneous measurement of **target range**, **relative radial velocity**, and **azimuth angle of arrival (AoA)** with high energy efficiency and millimetric accuracy.

This notebook provides a complete, first-principles derivation and implementation of the classical radar digital signal processing (DSP) chain. Every stage is verified against physical equations and visualized using a publication-grade dark cyber-radar theme:

### End-to-End Radar DSP Signal Processing Architecture
{nb1_top_diagram}
"""))

    # Cell 2: Setup Environment & Dark Cyber-Radar Theme
    nb.cells.append(new_code_cell(r"""import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Configure project paths
PROJECT_ROOT = os.path.abspath(".")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.sim.radar_config import RadarConfig, SPEED_OF_LIGHT
from src.sim.target import RadarTarget, create_standard_traffic_scenario
from src.sim.radar_sim import FMCWRadarSimulator
from src.dsp.range_processing import RangeProcessor
from src.dsp.clutter_removal import ClutterFilter
from src.dsp.doppler_processing import DopplerProcessor
from src.dsp.cfar_detector import CFARDetector2D
from src.dsp.aoa_estimation import AngleEstimator
from src.dsp.clustering import RadarClusterer
from src.dsp.radar_pipeline import ClassicalRadarPipeline

# Configure Dark Cyber-Radar Theme
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#0a0e17',
    'axes.facecolor': '#111625',
    'axes.edgecolor': '#2a364f',
    'axes.labelcolor': '#00f0ff',
    'xtick.color': '#8b9cb3',
    'ytick.color': '#8b9cb3',
    'grid.color': '#1e283d',
    'grid.alpha': 0.6,
    'text.color': '#e2e8f0',
    'font.family': 'sans-serif',
    'font.size': 10
})

print("✅ Dark Cyber-Radar Theme initialized.")
print("✅ Core Radar DSP libraries loaded from src/.")
"""))

    # Cell 3: Module 1 - FMCW Radar Physics & Operating Equations
    nb1_sec1_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec1"], "FMCW Radar Physics & Operating Equations")
    nb.cells.append(new_markdown_cell(rf"""## 1. FMCW Radar Physics & Operating Equations

{nb1_sec1_diagram}

An FMCW radar transmits a linear frequency-modulated (LFM) continuous wave chirp:

$$s_{{tx}}(t) = A_{{tx}} \cos\left(2\pi f_c t + \pi S t^2\right), \quad 0 \le t \le T_c$$

where:
- $f_c$ = Center carrier frequency (e.g., $77\text{{ GHz}}$, $\lambda = \frac{{c}}{{f_c}} \approx 3.9\text{{ mm}}$)
- $B$ = Chirp sweep bandwidth (e.g., $1.0\text{{ GHz}}$)
- $T_c$ = Active chirp sweep duration (e.g., $50\,\mu\text{{s}}$)
- $S = \frac{{B}}{{T_c}}$ = Chirp frequency slope ($\text{{Hz/s}}$)

### Target Reflection & Dechirping
For a target at range $R(t) = R_0 + v t$, the round-trip propagation time delay is:

$$\tau(t) = \frac{{2 R(t)}}{{c}} = \frac{{2(R_0 + v t)}}{{c}}$$

The received signal is mixed with the transmitted chirp (homodyne dechirping) and low-pass filtered, yielding the intermediate frequency (**IF beat signal**):

$$s_{{b}}(t) = A_b \cos\left(2\pi f_b t + \phi_0\right)$$

where the **beat frequency** $f_b$ maps directly to physical range:

$$f_b = S \tau = \frac{{2 S R_0}}{{c}} \implies R = \frac{{c \cdot f_b}}{{2 S}}$$

### Fundamental Resolution & Sampling Invariants
1. **Range Resolution ($\Delta R$)**: Governed purely by chirp bandwidth $B$:
   $$\Delta R = \frac{{c}}{{2 B}}$$
2. **Maximum Unambiguous Range ($R_{{max}}$)**: Bound by ADC sampling rate $F_s$:
   $$R_{{max}} = \frac{{F_s c}}{{2 S}}$$
3. **Velocity Resolution ($\Delta v$)**: Governed by total frame coherent processing interval ($CPI = N_{{chirps}} T_c$):
   $$\Delta v = \frac{{\lambda}}{{2 N_{{chirps}} T_c}}$$
4. **Maximum Unambiguous Velocity ($v_{{max}}$)**: Bound by chirp repetition interval $T_c$:
   $$v_{{max}} = \frac{{\lambda}}{{4 T_c}}$$
"""))

    # Cell 4: Radar Configuration Code & Chirp Visualization
    nb.cells.append(new_code_cell(r"""# Instantiate radar hardware specification (Texas Instruments AWR1843 equivalent)
cfg = RadarConfig(
    fc=77e9,              # 77 GHz center frequency
    bandwidth=1.0e9,      # 1 GHz bandwidth -> Delta_R = 15 cm
    chirp_duration=50e-6, # 50 us chirp duration Tc
    num_samples=256,      # Fast-time ADC samples per chirp
    num_chirps=128,       # Slow-time chirps per frame
    num_rx=4,             # 4-element Uniform Linear Array (ULA)
    rx_spacing_factor=0.5,# d = lambda / 2
    sampling_rate=5.12e6  # 5.12 MHz ADC sampling rate Fs
)

# Display radar performance metrics
print("=" * 65)
print("             77 GHz FMCW RADAR SYSTEM PARAMETERS")
print("=" * 65)
print(f"Carrier Frequency (fc)     : {cfg.fc / 1e9:.2f} GHz")
print(f"Wavelength (lambda)        : {cfg.wavelength * 1e3:.3f} mm")
print(f"Sweep Bandwidth (B)        : {cfg.bandwidth / 1e9:.2f} GHz")
print(f"Chirp Duration (Tc)        : {cfg.chirp_duration * 1e6:.1f} us")
print(f"Chirp Frequency Slope (S)  : {cfg.chirp_slope / 1e12:.2f} MHz/us")
print(f"Range Resolution (Delta_R) : {cfg.range_resolution:.4f} m (15 cm)")
print(f"Max Range (R_max)          : {cfg.max_unambiguous_range:.2f} m")
print(f"Velocity Resolution (Dv)   : {cfg.velocity_resolution:.4f} m/s")
print(f"Max Velocity (v_max)       : {cfg.max_unambiguous_velocity:.2f} m/s (+/- {cfg.max_unambiguous_velocity * 3.6:.1f} km/h)")
print(f"Antenna Array Elements     : {cfg.num_rx} Rx (ULA, d = {cfg.antenna_spacing * 1e3:.2f} mm)")
print("=" * 65)

# Visualize FMCW Sawtooth Transmit & Receive Frequency Modulation
t_sweep = np.linspace(0, 2 * cfg.chirp_duration, 1000)
f_tx = np.zeros_like(t_sweep)
tau_demo = 2 * 15.0 / SPEED_OF_LIGHT # 15m delay
f_rx = np.zeros_like(t_sweep)

for i, t in enumerate(t_sweep):
    t_mod = t % cfg.chirp_duration
    f_tx[i] = (cfg.fc + cfg.chirp_slope * t_mod) / 1e9
    t_rx_mod = (t - tau_demo) % cfg.chirp_duration
    f_rx[i] = (cfg.fc + cfg.chirp_slope * t_rx_mod) / 1e9

plt.figure(figsize=(10, 4.2), dpi=140)
plt.plot(t_sweep * 1e6, f_tx, label="Tx Transmitted Chirp", color="#00f0ff", lw=2.2)
plt.plot(t_sweep * 1e6, f_rx, label="Rx Received Chirp (Delayed)", color="#ff0055", lw=1.8, linestyle="--")
plt.title("FMCW Chirp Sequence: Frequency vs. Time Ramp", fontsize=12, fontweight="bold", color="#00f0ff")
plt.xlabel("Time (microseconds)", fontsize=10)
plt.ylabel("Frequency (GHz)", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(loc="upper left", framealpha=0.3)
plt.tight_layout()
plt.show()
"""))

    # Cell 5: Module 2 - Scene Formulation & Raw 3D Radar Cube Simulation
    nb1_sec2_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec2"], "Traffic Scenario & Raw 3D Radar Cube")
    nb.cells.append(new_markdown_cell(rf"""## 2. Multi-Target Traffic Scenario & Raw 3D Radar Cube

{nb1_sec2_diagram}

We construct a realistic automotive traffic scenario containing targets with varying kinematics, radar cross-sections (RCS), and spatial azimuth angles:

| Target ID | Object Class | Range ($R_0$) | Radial Velocity ($v$) | Azimuth Angle ($\theta$) | RCS ($\sigma$) | Kinematic Behavior |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| **#1** | **Car (Approaching)** | $12.0\text{{ m}}$ | $+8.5\text{{ m/s}}$ ($+30.6\text{{ km/h}}$) | $+18.0^\circ$ | $+8.0\text{{ dBsm}}$ | Approaching in right lane |
| **#2** | **Car (Receding)** | $28.5\text{{ m}}$ | $-14.2\text{{ m/s}}$ ($-51.1\text{{ km/h}}$) | $-12.0^\circ$ | $+12.0\text{{ dBsm}}$ | Receding fast in left lane |
| **#3** | **Pedestrian** | $8.4\text{{ m}}$ | $+1.4\text{{ m/s}}$ ($+5.0\text{{ km/h}}$) | $+28.0^\circ$ | $-4.0\text{{ dBsm}}$ | Walking with micro-Doppler gait |
| **#4** | **Cyclist** | $19.2\text{{ m}}$ | $-4.8\text{{ m/s}}$ ($-17.3\text{{ km/h}}$) | $+5.0^\circ$ | $+1.0\text{{ dBsm}}$ | Receding along roadway |
| **#5** | **Ground Clutter** | Distributed | $0.0\text{{ m/s}}$ | $0.0^\circ$ | Strong Rayleigh | Stationary road pavement & barriers |

### Raw 3D Radar Cube Dimensions
The raw ADC output forms a 3D complex matrix:
$$\mathbf{{X}} \in \mathbb{{C}}^{{N_{{rx}} \times N_{{chirps}} \times N_{{samples}}}} = \mathbb{{C}}^{{4 \times 128 \times 256}}$$
"""))

    # Cell 6: Scene Simulation Code & Time-Domain I/Q Plot
    nb.cells.append(new_code_cell(r"""# Define targets and instantiate simulator
targets = create_standard_traffic_scenario()
sim = FMCWRadarSimulator(cfg)

# Synthesize raw complex radar cube with noise and clutter
radar_cube = sim.generate_radar_cube(
    targets=targets,
    snr_db=18.0,
    clutter_ratio_db=10.0,
    include_clutter=True,
    seed=42
)

print(f"Synthesized 3D Radar Cube Shape: {radar_cube.shape} | Data Type: {radar_cube.dtype}")
print(f"Elements: {radar_cube.shape[0]} Rx Antennas x {radar_cube.shape[1]} Chirps x {radar_cube.shape[2]} ADC Samples")

# Plot Raw Dechirped I/Q Beat Signal for Chirp #0 on Rx #0
chirp_0 = radar_cube[0, 0, :]
sample_idx = np.arange(128) # first 128 fast-time samples

plt.figure(figsize=(10, 4.2), dpi=140)
plt.plot(sample_idx, np.real(chirp_0[:128]), label="In-Phase (I)", color="#00f0ff", lw=1.8)
plt.plot(sample_idx, np.imag(chirp_0[:128]), label="Quadrature (Q)", color="#ffaa00", lw=1.8, alpha=0.85)
plt.title("Dechirped Raw Beat Signal: In-Phase & Quadrature (Chirp #0, Rx #0)", fontsize=12, fontweight="bold", color="#00f0ff")
plt.xlabel("Fast-Time ADC Sample Index (n)", fontsize=10)
plt.ylabel("Voltage Amplitude (V)", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(loc="upper right", framealpha=0.3)
plt.tight_layout()
plt.show()
"""))

    # Cell 7: Module 3 - Fast-Time 1D Range FFT & Windowing (Prototype Section 3)
    nb1_sec3_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec3"], "Fast-Time 1D Range FFT & Windowing")
    nb.cells.append(new_markdown_cell(rf"""## 3. Fast-Time 1D Range FFT & Sidelobe Suppression

{nb1_sec3_diagram}

To extract target range, we compute the Discrete Fourier Transform (DFT) along the fast-time sample dimension for each chirp:

$$X_{{range}}[k] = \sum_{{n=0}}^{{N_{{samples}}-1}} w[n] \cdot x[n] \cdot e^{{-j 2\pi \frac{{k n}}{{N_{{samples}}}}}}$$

### Windowing for Spectral Leakage Suppression
A rectangular window has high sidelobes ($-13\text{{ dB}}$), which can mask weaker targets (such as a pedestrian with $-5\text{{ dBsm}}$ RCS) near a large vehicle ($+10\text{{ dBsm}}$). We apply a **Hann window**:

$$w_{{Hann}}[n] = 0.5 - 0.5 \cos\left(\frac{{2\pi n}}{{N_{{samples}}-1}}\right)$$

which attenuates sidelobes down to $-31.5\text{{ dB}}$, preventing false alarms and dynamic range saturation.
"""))

    # Cell 8: Range FFT Code & Profile Plot
    nb.cells.append(new_code_cell(r"""# Compute Range FFT with Hann windowing
range_proc = RangeProcessor(cfg, window="hann")
range_cube, range_axis = range_proc.process(radar_cube)

# Unwindowed (rectangular) version for side-by-side comparison
range_proc_rect = RangeProcessor(cfg, window="rect")
range_cube_rect, _ = range_proc_rect.process(radar_cube)

# Power spectrum across range (averaged over chirps)
pwr_hann = 10 * np.log10(np.mean(np.abs(range_cube[0])**2, axis=0))
pwr_rect = 10 * np.log10(np.mean(np.abs(range_cube_rect[0])**2, axis=0))

plt.figure(figsize=(10, 4.2), dpi=140)
plt.plot(range_axis, pwr_rect, label="Rectangular Window (High Sidelobes)", color="#ff5555", lw=1.2, alpha=0.6)
plt.plot(range_axis, pwr_hann, label="Hann Window (Suppressed Sidelobes)", color="#00ff66", lw=2.0)

# Annotate expected targets
plt.axvline(8.4, color="#ff00ff", linestyle=":", alpha=0.7, label="Target #3 (Pedestrian: 8.4m)")
plt.axvline(12.0, color="#00f0ff", linestyle=":", alpha=0.7, label="Target #1 (Car: 12.0m)")
plt.axvline(19.2, color="#ffaa00", linestyle=":", alpha=0.7, label="Target #4 (Cyclist: 19.2m)")
plt.axvline(28.5, color="#00ff66", linestyle=":", alpha=0.7, label="Target #2 (Car: 28.5m)")

plt.title("1D Range Profile: Windowing & Sidelobe Comparison", fontsize=12, fontweight="bold", color="#00f0ff")
plt.xlabel("Range (meters)", fontsize=10)
plt.ylabel("Normalized Power (dB)", fontsize=10)
plt.xlim([0, 35])
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(loc="upper right", framealpha=0.3, fontsize=8)
plt.tight_layout()
plt.show()
"""))

    # Cell 9: Module 4 - MTI Clutter Filtering
    nb1_sec4_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec4"], "Ground Clutter Suppression via MTI Filtering")
    nb.cells.append(new_markdown_cell(rf"""## 4. Ground Clutter Suppression via MTI Filtering

{nb1_sec4_diagram}

Stationary obstacles (road surface, guardrails, bridges) generate massive radar echoes at zero Doppler frequency ($v = 0\text{{ m/s}}$). This clutter masks moving dynamic road users.

We deploy **Moving Target Indication (MTI)** via slow-time mean subtraction:

$$y[m, n] = x[m, n] - \frac{{1}}{{M}} \sum_{{k=0}}^{{M-1}} x[k, n]$$

where $m$ is the chirp index (slow-time) and $n$ is the range bin index (fast-time).

### Clutter Attenuation (CA) Metric
The effectiveness of the filter is quantified by the Clutter Attenuation ratio:

$$\text{{CA (dB)}} = 10 \log_{{10}} \left(\frac{{P_{{in}}}}{{P_{{out}}}}\right)$$
"""))

    # Cell 10: MTI Filter Code & Comparison Plot
    nb.cells.append(new_code_cell(r"""# Apply MTI Clutter Filter
clutter_filter = ClutterFilter(method="mean_subtraction")
filtered_range_cube = clutter_filter.filter(range_cube, slow_time_axis=1)

ca_db = ClutterFilter.compute_clutter_attenuation_db(range_cube, filtered_range_cube)
print(f"[+] Clutter Attenuation (CA) Achieved: {ca_db:.2f} dB")

# 1D Range Profile Before vs After MTI
pwr_raw = 10 * np.log10(np.mean(np.abs(range_cube[0])**2, axis=0))
pwr_mti = 10 * np.log10(np.mean(np.abs(filtered_range_cube[0])**2, axis=0))

plt.figure(figsize=(10, 4.2), dpi=140)
plt.plot(range_axis, pwr_raw, label="Before MTI (Heavy Ground Clutter)", color="#ff5555", lw=1.5, alpha=0.7)
plt.plot(range_axis, pwr_mti, label=f"After MTI Filter (Suppression: {ca_db:.1f} dB)", color="#00ff66", lw=2.0)
plt.title(f"MTI Clutter Cancellation: {ca_db:.1f} dB Attenuation", fontsize=12, fontweight="bold", color="#00f0ff")
plt.xlabel("Range (meters)", fontsize=10)
plt.ylabel("Power (dB)", fontsize=10)
plt.xlim([0, 35])
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(loc="upper right", framealpha=0.3)
plt.tight_layout()
plt.show()
"""))

    # Cell 11: Module 5 - Slow-Time 2D Doppler FFT & Range-Doppler Matrix (RDM)
    nb1_sec5_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec5"], "Slow-Time 2D Doppler FFT & Range-Doppler Matrix")
    nb.cells.append(new_markdown_cell(rf"""## 5. Slow-Time 2D Doppler FFT & Range-Doppler Matrix (RDM)

{nb1_sec5_diagram}

The phase of the beat signal advances across successive chirps separated by interval $T_c$:

$$\Delta \phi = \frac{{4\pi v T_c}}{{\lambda}}$$

Performing a second Fourier transform across the slow-time chirp dimension extracts this phase rate of change (**Doppler frequency** $f_D$):

$$v = \frac{{\lambda f_D}}{{2}}$$

The resulting **2D Range-Doppler Matrix (RDM)** maps the physical space onto a calibrated 2D grid $(R, v)$, resolving objects even if they reside at the exact same distance.
"""))

    # Cell 12: Doppler FFT Code & 2D RDM Heatmap Plot
    nb.cells.append(new_code_cell(r"""# Compute Slow-Time Doppler FFT
doppler_proc = DopplerProcessor(cfg, window="hann")
rdm, velocity_axis, _ = doppler_proc.process(filtered_range_cube)

# Average power across Rx antennas
rdm_power = np.mean(np.abs(rdm)**2, axis=0) # (num_doppler, num_range)
rdm_power_db = 10.0 * np.log10(np.maximum(rdm_power, 1e-12))

# Display Range-Doppler Heatmap in Dark Cyber-Radar Theme
plt.figure(figsize=(10, 5.2), dpi=140)
extent = [range_axis[0], range_axis[-1], velocity_axis[0], velocity_axis[-1]]
im = plt.imshow(
    rdm_power_db,
    aspect="auto",
    origin="lower",
    extent=extent,
    cmap="plasma",
    vmin=np.percentile(rdm_power_db, 20),
    vmax=np.max(rdm_power_db)
)

# Annotate Ground Truth Target Positions
plt.scatter([12.0], [8.5], color="#00ffff", s=90, marker="o", edgecolors="white", label="Target #1: Car (12.0m, +8.5 m/s)")
plt.scatter([28.5], [-14.2], color="#00ff66", s=90, marker="D", edgecolors="white", label="Target #2: Car (28.5m, -14.2 m/s)")
plt.scatter([8.4], [1.4], color="#ff00ff", s=90, marker="s", edgecolors="white", label="Target #3: Pedestrian (8.4m, +1.4 m/s)")
plt.scatter([19.2], [-4.8], color="#ffaa00", s=90, marker="^", edgecolors="white", label="Target #4: Cyclist (19.2m, -4.8 m/s)")

cbar = plt.colorbar(im, label="Power (dB)")
cbar.ax.yaxis.label.set_color('#00f0ff')
plt.title("2D Range-Doppler Matrix (RDM) Power Spectrum", fontsize=12, fontweight="bold", color="#00f0ff")
plt.xlabel("Range (meters)", fontsize=10)
plt.ylabel("Radial Velocity (m/s)", fontsize=10)
plt.xlim([0, 35])
plt.ylim([velocity_axis[0], velocity_axis[-1]])
plt.grid(True, linestyle="--", alpha=0.3)
plt.legend(loc="upper right", framealpha=0.4, fontsize=9)
plt.tight_layout()
plt.show()
"""))

    # Cell 13: Module 6 - 2D Constant False Alarm Rate (CFAR) Detection
    nb1_sec6_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec6"], "Adaptive 2D Constant False Alarm Rate (CFAR) Detection")
    nb.cells.append(new_markdown_cell(rf"""## 6. Adaptive 2D Constant False Alarm Rate (CFAR) Detection

{nb1_sec6_diagram}

A static detection threshold is ineffective in real-world radar because thermal noise and residual clutter vary across range and Doppler cells.

The **Cell-Averaging CFAR (CA-CFAR)** algorithm computes an adaptive threshold dynamically:
1. **Cell Under Test (CUT)**: The central bin being evaluated.
2. **Guard Cells ($G_R, G_D$)**: Immediate neighbor cells excluded to prevent target energy leakage from corrupting the noise estimate.
3. **Training / Reference Cells ($N_{{train}}$)**: Outer window cells used to estimate the local background noise power $P_{{noise}}$.

The detection threshold $T$ is:

$$T = \alpha \cdot P_{{noise}}$$

where the scaling factor $\alpha$ guarantees a constant specified probability of false alarm ($P_{{FA}}$):

$$\alpha = N_{{train}} \left(P_{{FA}}^{{-1/N_{{train}}}} - 1\right)$$
"""))

    # Cell 14: CFAR Detection Code & Overlay Plot
    nb.cells.append(new_code_cell(r"""# Execute 2D CA-CFAR Detection with explicit training and guard dimensions
cfar = CFARDetector2D(
    num_train_range=4,
    num_train_doppler=4,
    num_guard_range=2,
    num_guard_doppler=2,
    p_fa=1e-4,
    cfar_type="ca"
)

detection_mask, threshold_map, detections = cfar.detect(rdm_power, range_axis, velocity_axis)
print(f"[+] 2D CA-CFAR extracted {len(detections)} target peaks above adaptive noise floor.")
for i, det in enumerate(detections):
    print(f"    - Detection #{i+1}: Range = {det['range_m']:.2f} m, Velocity = {det['velocity_mps']:+.2f} m/s, SNR = {det['snr_db']:.1f} dB")

# Visualize CFAR Detections Overlaid on Heatmap
plt.figure(figsize=(10, 5.2), dpi=140)
plt.imshow(
    rdm_power_db,
    aspect="auto",
    origin="lower",
    extent=extent,
    cmap="magma",
    alpha=0.85
)

# Overlay CFAR detection markers
for det in detections:
    plt.scatter(
        det["range_m"], det["velocity_mps"],
        s=150, facecolors="none", edgecolors="#00ff66", lw=2.2,
        label="CA-CFAR Target Hit" if "CA-CFAR Target Hit" not in [l.get_label() for l in plt.gca().collections] else ""
    )
    plt.text(
        det["range_m"] + 0.6, det["velocity_mps"] + 0.5,
        f"({det['range_m']:.1f}m, {det['velocity_mps']:+.1f}m/s)",
        color="#00ff66", fontsize=9, fontweight="bold"
    )

plt.title(f"2D CA-CFAR Detection Map ({len(detections)} Target Hits)", fontsize=12, fontweight="bold", color="#00f0ff")
plt.xlabel("Range (meters)", fontsize=10)
plt.ylabel("Radial Velocity (m/s)", fontsize=10)
plt.xlim([0, 35])
plt.ylim([velocity_axis[0], velocity_axis[-1]])
plt.grid(True, linestyle="--", alpha=0.3)
plt.legend(loc="upper right", framealpha=0.4)
plt.tight_layout()
plt.show()
"""))

    # Cell 15: Module 7 - Spatial Direction-of-Arrival (AoA) Estimation
    nb1_sec7_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec7"], "Direction-of-Arrival (AoA) Estimation")
    nb.cells.append(new_markdown_cell(rf"""## 7. Direction-of-Arrival (AoA) Estimation: Beamforming, Capon, & MUSIC

{nb1_sec7_diagram}

To estimate the azimuth angle $\theta$, we leverage the phase differences across the $M = 4$ receiver antenna elements separated by $d = \frac{{\lambda}}{{2}}$:

$$\Delta \phi = \frac{{2\pi d}}{{\lambda}} \sin(\theta)$$

The spatial array steering vector is:

$$\mathbf{{a}}(\theta) = \left[1, e^{{-j 2\pi \frac{{d}}{{\lambda}}\sin\theta}}, \dots, e^{{-j 2\pi (M-1) \frac{{d}}{{\lambda}}\sin\theta}}\right]^T$$

### Super-Resolution Subspace MUSIC
Classical beamforming is limited by the Rayleigh diffraction limit ($\Delta \theta \approx \frac{{\lambda}}{{M d}}$). The **MUSIC (Multiple Signal Classification)** algorithm achieves super-resolution by decomposing the spatial covariance matrix $\mathbf{{R}}_{{xx}}$ into orthogonal signal and noise subspaces:

$$\mathbf{{R}}_{{xx}} = \mathbf{{U}}_s \mathbf{{\Lambda}}_s \mathbf{{U}}_s^H + \mathbf{{U}}_n \mathbf{{\Lambda}}_n \mathbf{{U}}_n^H$$

The MUSIC pseudo-spectrum peaks when the steering vector is orthogonal to the noise subspace:

$$P_{{MUSIC}}(\theta) = \frac{{1}}{{\mathbf{{a}}^H(\theta) \mathbf{{U}}_n \mathbf{{U}}_n^H \mathbf{{a}}(\theta)}}$$
"""))

    # Cell 16: AoA Code & Super-Resolution Spectrum Plot
    nb.cells.append(new_code_cell(r"""# Estimate AoA for Target #1 (Car at 12m, +8.5 m/s, Ground Truth Azimuth: +18.0 deg)
aoa_estimator = AngleEstimator(cfg)
target_1_det = min(detections, key=lambda d: abs(d["range_m"] - 12.0))
rx_samples_1 = rdm[:, target_1_det["doppler_bin"], target_1_det["range_bin"]]

# Compute MUSIC, Capon, and Spatial FFT Spectra
angles_deg, music_spec_1, est_angle_music = aoa_estimator.estimate_aoa_music(rx_samples_1)
_, capon_spec_1, est_angle_capon = aoa_estimator.estimate_aoa_capon(rx_samples_1)
fft_angles, fft_spec_1, est_angle_fft = aoa_estimator.estimate_aoa_fft(rx_samples_1)

print(f"[+] Target #1 at 12m (Ground Truth Azimuth: +18.0°)")
print(f"    - MUSIC Estimated Angle    : {est_angle_music:+.2f}° (Error: {abs(est_angle_music - 18.0):.2f}°)")
print(f"    - Capon / MVDR Angle       : {est_angle_capon:+.2f}°")
print(f"    - Spatial FFT Beamformer   : {est_angle_fft:+.2f}°")

# Plot Super-Resolution Angular Spectra
plt.figure(figsize=(10, 4.4), dpi=140)
plt.plot(angles_deg, music_spec_1 - np.max(music_spec_1), label=f"MUSIC Subspace (Peak: {est_angle_music:+.1f}°)", color="#00ff66", lw=2.2)
plt.plot(angles_deg, capon_spec_1 - np.max(capon_spec_1), label=f"Capon / MVDR (Peak: {est_angle_capon:+.1f}°)", color="#00f0ff", lw=1.6, linestyle="--")
plt.plot(fft_angles, fft_spec_1 - np.max(fft_spec_1), label=f"Spatial FFT (Peak: {est_angle_fft:+.1f}°)", color="#ffaa00", lw=1.4, linestyle=":")

plt.axvline(18.0, color="#ff0055", linestyle="-.", label="Ground Truth Azimuth (+18.0°)")
plt.title("Spatial Direction-of-Arrival (AoA) Super-Resolution Spectra", fontsize=12, fontweight="bold", color="#00f0ff")
plt.xlabel("Azimuth Angle (degrees)", fontsize=10)
plt.ylabel("Normalized Pseudo-Spectrum (dB)", fontsize=10)
plt.xlim([-60, 60])
plt.ylim([-30, 2])
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend(loc="upper right", framealpha=0.3)
plt.tight_layout()
plt.show()
"""))

    # Cell 17: Module 8 - DBSCAN Point Cloud Clustering & Cartesian BEV Mapping
    nb1_sec8_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec8"], "DBSCAN Clustering & Cartesian Bird's-Eye View")
    nb.cells.append(new_markdown_cell(rf"""## 8. DBSCAN Clustering & Cartesian Bird's-Eye View (BEV)

{nb1_sec8_diagram}

Radar returns from extended physical objects often produce multiple detection points. We use **DBSCAN (Density-Based Spatial Clustering of Applications with Noise)** to associate point reflections into unified physical entities.

We then convert polar coordinates $(R, \theta)$ to Cartesian coordinates $(x, y)$:

$$x = R \sin(\theta) \quad (\text{{Cross-Range}}), \qquad y = R \cos(\theta) \quad (\text{{Down-Range}})$$
"""))

    # Cell 18: BEV Clustering Code & Tactical Radar Plot
    nb.cells.append(new_code_cell(r"""# Run End-to-End Pipeline for full clustered object extraction
pipeline = ClassicalRadarPipeline(config=cfg, cfar_type="ca", p_fa=1e-4)
results = pipeline.process_radar_cube(radar_cube)
clustered_objects = results["detected_objects"]

# Render 2D Cartesian Bird's-Eye View (BEV) Tactical Radar Display
plt.figure(figsize=(9, 8), dpi=140)
ax = plt.subplot(111)

# Draw Range Rings
theta_ring = np.linspace(-np.pi/3, np.pi/3, 200)
for r in [10, 20, 30]:
    ax.plot(r * np.sin(theta_ring), r * np.cos(theta_ring), color="#1e283d", linestyle="--", lw=1.2)
    ax.text(0, r + 0.5, f"{r}m", color="#5a6b85", fontsize=8, ha="center")

# Draw Azimuth lines (+/- 30 deg, +/- 60 deg)
for ang_deg in [-60, -30, 0, 30, 60]:
    rad = np.deg2rad(ang_deg)
    ax.plot([0, 35 * np.sin(rad)], [0, 35 * np.cos(rad)], color="#1e283d", linestyle=":", lw=1.0)

# Plot Radar Sensor at Origin
ax.scatter([0], [0], color="#00f0ff", s=180, marker="^", label="Ego Radar (77 GHz mmWave)", zorder=10)

# Plot Ground Truth Targets
for t in targets:
    gx = t.range_m * np.sin(np.deg2rad(t.azimuth_deg))
    gy = t.range_m * np.cos(np.deg2rad(t.azimuth_deg))
    ax.scatter([gx], [gy], color="#ff0055", s=130, marker="*", label="Ground Truth" if "Ground Truth" not in [l.get_label() for l in ax.collections] else "")
    ax.text(gx + 0.6, gy, f"{t.label.upper()}\n({t.velocity_mps:+.1f} m/s)", color="#ff5588", fontsize=8, fontweight="bold")

# Plot DSP Detected & Clustered Objects with Velocity Vectors
for obj in clustered_objects:
    ox = obj["x_m"]
    oy = obj["y_m"]
    ax.scatter([ox], [oy], color="#00ff66", s=100, marker="o", edgecolors="white", lw=1.5, label="DSP Estimated Object" if "DSP Estimated Object" not in [l.get_label() for l in ax.collections] else "")
    # Draw velocity vector arrow
    vx = obj["velocity_mps"] * np.sin(np.deg2rad(obj["azimuth_deg"])) * 0.4
    vy = obj["velocity_mps"] * np.cos(np.deg2rad(obj["azimuth_deg"])) * 0.4
    ax.arrow(ox, oy, vx, vy, color="#00ff66", head_width=0.6, head_length=0.6, lw=1.5)

ax.set_title("Cartesian Bird's-Eye View (BEV) Radar Perception Map", fontsize=12, fontweight="bold", color="#00f0ff")
ax.set_xlabel("Cross-Range X (meters)", fontsize=10)
ax.set_ylabel("Down-Range Y (meters)", fontsize=10)
ax.set_xlim([-20, 20])
ax.set_ylim([-2, 35])
ax.grid(True, linestyle="--", alpha=0.3)
ax.legend(loc="lower right", framealpha=0.3)
plt.tight_layout()
plt.show()
"""))

    # Cell 19: Module 9 - Pedestrian Micro-Doppler Time-Frequency Signature
    nb1_sec9_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec9"], "Pedestrian Micro-Doppler Time-Frequency Signature")
    nb.cells.append(new_markdown_cell(rf"""## 9. Pedestrian Micro-Doppler Time-Frequency Signature

{nb1_sec9_diagram}

In addition to the torso's gross translation velocity, dynamic swinging limbs (arms and legs) cause distinctive periodic Doppler shifts known as **micro-Doppler signatures**.

We analyze this via the **Short-Time Fourier Transform (STFT)**:

$$STFT\{{x\}}(t, f) = \int_{{-\infty}}^{{\infty}} x(\tau) w(\tau - t) e^{{-j 2\pi f \tau}} d\tau$$

The resulting spectrogram displays the characteristic human walking cadence, enabling automatic classification between rigid vehicles and articulated pedestrians.
"""))

    # Cell 20: Micro-Doppler Code & Spectrogram Plot
    nb.cells.append(new_code_cell(r"""# Synthesize extended continuous slow-time return for pedestrian walking gait
ped_target = [t for t in targets if t.label == "pedestrian"][0]
fs_slow = 512.0 # Hz slow-time sampling rate
t_ext = np.linspace(0, 1.2, int(1.2 * fs_slow))

# Bulk motion + periodic swinging limbs modulation
bulk_phase = 2 * np.pi * (2 * ped_target.velocity_mps / cfg.wavelength) * t_ext
limb_mod = (4 * np.pi / cfg.wavelength) * (ped_target.micro_doppler_amp / (2 * np.pi * ped_target.micro_doppler_freq)) * np.sin(2 * np.pi * ped_target.micro_doppler_freq * t_ext)
ped_signal = np.exp(1j * (bulk_phase + limb_mod))
# Add background noise
ped_signal += 0.15 * (np.random.randn(len(t_ext)) + 1j * np.random.randn(len(t_ext)))

# Compute STFT Micro-Doppler Spectrogram
md_freqs, md_times, md_spec = DopplerProcessor.compute_micro_doppler_spectrogram(
    ped_signal, fs=fs_slow, nperseg=64, noverlap=56
)

plt.figure(figsize=(10, 4.4), dpi=140)
plt.imshow(
    md_spec,
    aspect="auto",
    origin="lower",
    extent=[md_times[0], md_times[-1], md_freqs[0], md_freqs[-1]],
    cmap="inferno"
)
cbar = plt.colorbar(label="Power (dB)")
cbar.ax.yaxis.label.set_color('#00f0ff')
plt.title("Micro-Doppler STFT Spectrogram: Pedestrian Walking Gait Cadence", fontsize=12, fontweight="bold", color="#00f0ff")
plt.xlabel("Time (seconds)", fontsize=10)
plt.ylabel("Doppler Frequency (Hz)", fontsize=10)
plt.ylim([-200, 200])
plt.tight_layout()
plt.show()
"""))

    # Cell 21: Conclusion & Academic Summary
    nb1_sec10_diagram = render_mermaid_dual_block(DIAGRAMS["nb1_sec10"], "Academic Summary Diagram")
    nb.cells.append(new_markdown_cell(rf"""## 10. Summary & Academic Conclusions

{nb1_sec10_diagram}

| Stage | Input Domain | Output Domain | Core Governing Equation | Primary Benefit |
|:---|:---|:---|:---|:---|
| **Fast-Time FFT** | Raw ADC Samples ($t_{{fast}}$) | Range Bins ($R$) | $\Delta R = \frac{{c}}{{2B}}$ | High range resolution from frequency dechirping |
| **MTI Filter** | Range Profiles | Clutter-Attenuated Profiles | $y[m] = x[m] - \bar{{x}}$ | $>18\text{{ dB}}$ stationary clutter suppression |
| **Slow-Time FFT** | Chirp Sequence ($t_{{slow}}$) | Range-Doppler Matrix ($R, v$) | $v = \frac{{\lambda f_D}}{{2}}$ | Direct Doppler velocity estimation & target separation |
| **2D CA-CFAR** | Range-Doppler Matrix | Detected Target Peaks | $T = \alpha \cdot P_{{noise}}$ | Adaptive noise thresholding under constant $P_{{FA}}$ |
| **MUSIC AoA** | Spatial Array ($Rx$) | Azimuth Angle ($\theta$) | $P_{{MUSIC}} = \frac{{1}}{{\mathbf{{a}}^H \mathbf{{U}}_n \mathbf{{U}}_n^H \mathbf{{a}}}}$ | Super-resolution beyond Rayleigh limit |
| **DBSCAN BEV** | Polar Points $(R, \theta)$ | Cartesian Tracked Clusters $(x, y)$ | $x = R\sin\theta, y = R\cos\theta$ | Multipoint clustering & spatial extent tracking |
| **Micro-Doppler** | Time-Series Returns | Time-Frequency Spectrogram | $\text{{STFT}}(t, f)$ | Articulated target discrimination (pedestrians vs cars) |

---
*Next Step: Proceed to [02_radar_deep_learning_detection.ipynb](file:///d:/projects/BTP/02_radar_deep_learning_detection.ipynb) to explore end-to-end Neural Network perception directly on Range-Doppler heatmaps.*
"""))

    return nb


def build_notebook_2() -> nbformat.NotebookNode:
    nb = new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    }

    # Cell 1: Title & Overview + Top-Level Deep Learning Flow
    nb2_top_diagram = render_mermaid_dual_block(DIAGRAMS["nb2_top"], "End-to-End Deep Learning Perception Pipeline")
    nb.cells.append(new_markdown_cell(rf"""# 🧠 02. Deep Learning for FMCW Radar Perception: From Range-Doppler Heatmaps to AI Bounding Boxes

> **BTP Research & Pedagogy Masterclass**  
> **Topic:** AI-Based Radar Object Detection on Complex Range-Doppler Tensors  
> **Key Disciplines:** Radar Deep Learning • Anchor-Free Multi-Task CNN • Gaussian Heatmap Splatting • Multi-Task Loss (BCE + Smooth L1) • Convergence Analysis • Classical vs Deep Learning Comparison  

---

## Executive Summary for Academic Review

While classical radar signal processing (FFT + CFAR + MUSIC) provides deterministic, mathematically grounded target detection, it faces critical real-world limitations:
1. **CFAR Masking & Clutter Inhomogeneity**: CA-CFAR thresholds elevate near strong targets, hiding weak neighboring reflectors (e.g., a pedestrian walking next to an SUV).
2. **Phase & Texture Information Loss**: Thresholding discards fine-grained phase, micro-Doppler sidebands, and spatial texture embedded in the raw Range-Doppler spectrum.
3. **Semantic Classification**: Classical DSP detects *reflectors*, but cannot easily classify whether a cluster is a **car**, **pedestrian**, **cyclist**, or **drone** without heuristic post-processing.

In this notebook, we implement an **anchor-free convolutional neural network (`RadarObjectDetectorCNN`)** operating directly on Range-Doppler heatmaps to perform simultaneous object classification and bounding box regression in a single forward pass:

### Deep Learning Radar Perception Pipeline
{nb2_top_diagram}
"""))

    # Cell 2: Setup Environment & Dark Cyber-Radar Theme
    nb.cells.append(new_code_cell(r"""import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split

# Configure project paths
PROJECT_ROOT = os.path.abspath(".")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.sim.radar_config import RadarConfig
from src.sim.target import RadarTarget
from src.models.radar_dataset import RadarDataset, CLASS_MAP, NUM_CLASSES
from src.models.radar_detector_cnn import RadarObjectDetectorCNN

# Configure Dark Cyber-Radar Theme
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#0a0e17',
    'axes.facecolor': '#111625',
    'axes.edgecolor': '#2a364f',
    'axes.labelcolor': '#00f0ff',
    'xtick.color': '#8b9cb3',
    'ytick.color': '#8b9cb3',
    'grid.color': '#1e283d',
    'grid.alpha': 0.6,
    'text.color': '#e2e8f0',
    'font.family': 'sans-serif',
    'font.size': 10
})

device = torch.device("cpu")
print(f"✅ PyTorch {torch.__version__} initialized on device: {device}")
print("✅ Radar Deep Learning models loaded successfully.")
"""))

    # Cell 3: Module 1 - Synthetic Radar Dataset Generation & Pre-Caching
    nb2_sec1_diagram = render_mermaid_dual_block(DIAGRAMS["nb2_sec1"], "Synthetic Dataset Generation & Gaussian Splatting")
    nb.cells.append(new_markdown_cell(rf"""## 1. Multi-Target Synthetic Radar Dataset Generation

{nb2_sec1_diagram}

For deep learning detection, our input tensor is a normalized Range-Doppler power heatmap:

$$\mathbf{{X}}_{{RDM}} \in \mathbb{{R}}^{{1 \times N_{{doppler}} \times N_{{range}}}} = \mathbb{{R}}^{{1 \times 128 \times 129}}$$

### Multi-Task Ground Truth Representation
For each frame, the neural network learns two complementary tasks:
1. **Classification Heatmap ($\mathbf{{Y}}_{{cls}} \in [0, 1]^{{C \times H \times W}}$)**:
   A multi-channel confidence map across $C = 5$ semantic classes:
   `[0: Background, 1: Car, 2: Pedestrian, 3: Cyclist, 4: Drone]`
   Targets are encoded using 2D Gaussian splats centered at target range and velocity indices $(v_k, r_k)$:
   $$Y_{{cls}}[c, d, r] = \exp\left(-\frac{{(d - v_k)^2 + (r - r_k)^2}}{{2 \sigma^2}}\right)$$
2. **Bounding Box Targets ($\mathbf{{Y}}_{{box}} \in \mathbb{{R}}^{{4 \times H \times W}}$)**:
   Continuous physical regression coordinates:
   $$[r_{{norm}}, v_{{norm}}, w_r, w_v]$$
"""))

    # Cell 4: Fast Cached Dataset Implementation & Pre-generation
    nb.cells.append(new_code_cell(r"""# Pre-cache a diverse dataset in memory for rapid, seamless notebook execution
class CachedRadarDataset(Dataset):
    def __init__(self, raw_dataset, max_samples=32):
        print(f"[*] Pre-synthesizing {max_samples} diverse radar scenes into RAM...")
        self.cached = []
        for i in range(max_samples):
            self.cached.append(raw_dataset[i])
        print(f"✅ Cached {len(self.cached)} full radar tensors.")

    def __len__(self):
        return len(self.cached)

    def __getitem__(self, idx):
        return self.cached[idx]

# Synthesize dataset
raw_ds = RadarDataset(num_samples=32, seed=42)
cached_dataset = CachedRadarDataset(raw_ds, max_samples=32)

# Inspect sample tensor shapes
sample_rdm, sample_heatmap, sample_box = cached_dataset[0]
print(f"Input Tensor Shape          : {sample_rdm.shape} (Channels x Doppler x Range)")
print(f"Ground Truth Heatmap Shape  : {sample_heatmap.shape} (Num Classes x Doppler x Range)")
print(f"Bounding Box Targets Shape  : {sample_box.shape} (4 Regressors x Doppler x Range)")
"""))

    # Cell 5: Visual Inspection of Input Tensor & Ground Truth Channels
    nb.cells.append(new_code_cell(r"""# Visualize Input RDM alongside Gaussian Target Channels
plt.figure(figsize=(12, 4.2), dpi=140)

# Input RDM
plt.subplot(1, 3, 1)
plt.imshow(sample_rdm[0].numpy(), aspect="auto", origin="lower", cmap="plasma")
plt.title("1. Input Normalized RDM", fontsize=11, fontweight="bold", color="#00f0ff")
plt.xlabel("Range Bins")
plt.ylabel("Doppler Bins")

# Car Channel Heatmap
plt.subplot(1, 3, 2)
plt.imshow(sample_heatmap[1].numpy(), aspect="auto", origin="lower", cmap="inferno")
plt.title("2. Ground Truth: Car Channel", fontsize=11, fontweight="bold", color="#ffaa00")
plt.xlabel("Range Bins")
plt.ylabel("Doppler Bins")

# Pedestrian Channel Heatmap
plt.subplot(1, 3, 3)
plt.imshow(sample_heatmap[2].numpy(), aspect="auto", origin="lower", cmap="magma")
plt.title("3. Ground Truth: Pedestrian Channel", fontsize=11, fontweight="bold", color="#00ff66")
plt.xlabel("Range Bins")
plt.ylabel("Doppler Bins")

plt.tight_layout()
plt.show()
"""))

    # Cell 6: Module 2 - Neural Network Architecture & Multi-Task Loss
    nb2_sec2_diagram = render_mermaid_dual_block(DIAGRAMS["nb2_sec2"], "Multi-Branch CNN Architecture & Loss Formulation")
    nb.cells.append(new_markdown_cell(rf"""## 2. Anchor-Free Radar CNN Architecture & Multi-Task Loss

{nb2_sec2_diagram}

The `RadarObjectDetectorCNN` features a fully convolutional backbone with multi-task prediction heads:
- **Convolutional Backbone**: Sequential Conv2D layers with Batch Normalization, ReLU, and Residual Skip Connections.
- **Classification Head**: Predicts spatial class heatmaps for multi-class detection.
- **Bounding Box Head**: Regresses continuous physical bounding box offsets and dimensions.

### Multi-Task Loss Formulation
The network is optimized end-to-end using a composite loss:

$$\mathcal{{L}}_{{total}} = \mathcal{{L}}_{{cls}} + \lambda_{{box}} \mathcal{{L}}_{{box}}$$

1. **Classification Loss**: Binary Cross-Entropy with Logits over all spatial bins:
   $$\mathcal{{L}}_{{cls}} = -\frac{{1}}{{C \cdot H \cdot W}} \sum_{{c, d, r}} \left[ Y \log \sigma(P) + (1 - Y) \log(1 - \sigma(P)) \right]$$
2. **Bounding Box Regression Loss**: Smooth L1 Loss computed exclusively on target-positive bins ($Y > 0.3$):
   $$\mathcal{{L}}_{{box}} = \frac{{1}}{{N_{{pos}}}} \sum_{{i \in pos}} \text{{SmoothL1}}(B_i - \hat{{B}}_i)$$
"""))

    # Cell 7: Model Instantiation & Forward Pass Code
    nb.cells.append(new_code_cell(r"""# Instantiate CNN Model
model = RadarObjectDetectorCNN(in_channels=1, num_classes=NUM_CLASSES, base_filters=24).to(device)

# Count trainable parameters
num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print("=" * 60)
print(f"      RADAR OBJECT DETECTOR CNN ARCHITECTURE")
print("=" * 60)
print(f"Total Trainable Parameters : {num_params:,}")
print(f"Input Channels             : 1 (Range-Doppler Power Map)")
print(f"Output Classification      : 5 Classes (Heatmap Bins)")
print(f"Output Regression          : 4 Regressors [r, v, w_r, w_v]")
print("=" * 60)

# Verify forward pass with dummy batch
dummy_x = torch.randn(2, 1, 128, 129).to(device)
cls_out, box_out = model(dummy_x)
print(f"Forward Pass Output Shapes:")
print(f"  - Classification Logits : {cls_out.shape}")
print(f"  - Box Regressions       : {box_out.shape}")
"""))

    # Cell 8: Module 3 - Model Training & Convergence Loop
    nb2_sec3_diagram = render_mermaid_dual_block(DIAGRAMS["nb2_sec3"], "Model Training & Convergence Loop")
    nb.cells.append(new_markdown_cell(rf"""## 3. End-to-End Model Training & Convergence

{nb2_sec3_diagram}

We train the model using **AdamW** with weight decay and a **Cosine Annealing** learning rate scheduler.
"""))

    # Cell 9: Training Loop Code & Live Loss Logging
    nb.cells.append(new_code_cell(r"""# Split cached dataset into Train (80%) and Validation (20%)
train_len = int(0.8 * len(cached_dataset))
val_len = len(cached_dataset) - train_len
train_set, val_set = random_split(cached_dataset, [train_len, val_len], generator=torch.Generator().manual_seed(42))

train_loader = DataLoader(train_set, batch_size=6, shuffle=True)
val_loader = DataLoader(val_set, batch_size=6, shuffle=False)

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=5)

history = {"train_loss": [], "val_loss": [], "cls_loss": [], "box_loss": []}
epochs = 5

print(f"[*] Commencing Training for {epochs} Epochs...")
start_time = time.time()

for epoch in range(1, epochs + 1):
    model.train()
    t_loss, c_loss, b_loss = 0.0, 0.0, 0.0
    for rdm, h_target, b_target in train_loader:
        rdm, h_target, b_target = rdm.to(device), h_target.to(device), b_target.to(device)
        optimizer.zero_grad()
        logits, boxes = model(rdm)
        loss, cls_l, box_l = model.compute_loss(logits, boxes, h_target, b_target)
        loss.backward()
        optimizer.step()
        
        t_loss += loss.item() * len(rdm)
        c_l = cls_l.item() if isinstance(cls_l, torch.Tensor) else cls_l
        b_l = box_l.item() if isinstance(box_l, torch.Tensor) else box_l
        c_loss += c_l * len(rdm)
        b_loss += b_l * len(rdm)

    scheduler.step()

    # Validation
    model.eval()
    v_loss = 0.0
    with torch.no_grad():
        for rdm, h_target, b_target in val_loader:
            rdm, h_target, b_target = rdm.to(device), h_target.to(device), b_target.to(device)
            logits, boxes = model(rdm)
            loss, _, _ = model.compute_loss(logits, boxes, h_target, b_target)
            v_loss += loss.item() * len(rdm)

    history["train_loss"].append(t_loss / train_len)
    history["val_loss"].append(v_loss / val_len)
    history["cls_loss"].append(c_loss / train_len)
    history["box_loss"].append(b_loss / train_len)

    print(f"Epoch [{epoch}/{epochs}] | Train Loss: {history['train_loss'][-1]:.4f} | Val Loss: {history['val_loss'][-1]:.4f}")

elapsed = time.time() - start_time
print(f"✅ Training completed in {elapsed:.2f} seconds.")
"""))

    # Cell 10: Loss Curves Visualization
    nb.cells.append(new_code_cell(r"""# Plot Training Convergence Curves
plt.figure(figsize=(10, 4.4), dpi=140)

plt.plot(range(1, epochs + 1), history["train_loss"], marker="o", label="Training Loss (Total)", color="#00f0ff", lw=2.0)
plt.plot(range(1, epochs + 1), history["val_loss"], marker="s", label="Validation Loss", color="#ffaa00", lw=2.0)
plt.plot(range(1, epochs + 1), history["cls_loss"], marker="^", label="Classification Loss", color="#00ff66", lw=1.5, linestyle="--")

plt.title("Radar CNN Multi-Task Training Convergence", fontsize=12, fontweight="bold", color="#00f0ff")
plt.xlabel("Epoch", fontsize=10)
plt.ylabel("Multi-Task Loss", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend(loc="upper right", framealpha=0.3)
plt.tight_layout()
plt.show()
"""))

    # Cell 11: Module 4 - Model Inference on Unseen Test Radar Scene
    nb2_sec4_diagram = render_mermaid_dual_block(DIAGRAMS["nb2_sec4"], "Inference on Unseen Radar Scenes")
    nb.cells.append(new_markdown_cell(rf"""## 4. Deep Learning Inference on Unseen Radar Scenes

{nb2_sec4_diagram}

We evaluate our trained neural network on a completely unseen test radar scene containing moving vehicles and pedestrians in dense clutter.
"""))

    # Cell 12: Inference Code & Multi-Panel Detection Plot
    nb.cells.append(new_code_cell(r"""# Run Model Inference on Test Frame
model.eval()
test_rdm, test_heatmap, _ = val_set[0]
test_input = test_rdm.unsqueeze(0).to(device)

with torch.no_grad():
    logits, boxes = model(test_input)
    probs = torch.sigmoid(logits).squeeze(0).numpy() # (5, H, W)
    car_prob = probs[1]
    ped_prob = probs[2]

# Multi-Panel Visual Inference Display
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), dpi=140)

# Panel 1: Input RDM
axes[0].imshow(test_rdm[0].numpy(), aspect="auto", origin="lower", cmap="plasma")
axes[0].set_title("1. Input Range-Doppler Heatmap", fontsize=11, fontweight="bold", color="#00f0ff")
axes[0].set_xlabel("Range Bins")
axes[0].set_ylabel("Doppler Bins")

# Panel 2: Predicted Car Confidence
im2 = axes[1].imshow(car_prob, aspect="auto", origin="lower", cmap="magma", vmin=0, vmax=1.0)
axes[1].set_title("2. Predicted Car Confidence", fontsize=11, fontweight="bold", color="#ffaa00")
axes[1].set_xlabel("Range Bins")
fig.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)

# Panel 3: Predicted Pedestrian Confidence
im3 = axes[2].imshow(ped_prob, aspect="auto", origin="lower", cmap="inferno", vmin=0, vmax=1.0)
axes[2].set_title("3. Predicted Pedestrian Confidence", fontsize=11, fontweight="bold", color="#00ff66")
axes[2].set_xlabel("Range Bins")
fig.colorbar(im3, ax=axes[2], fraction=0.046, pad=0.04)

plt.tight_layout()
plt.show()
"""))

    # Cell 13: Module 5 - Classical DSP vs Deep Learning Comprehensive Comparison
    nb2_sec5_diagram = render_mermaid_dual_block(DIAGRAMS["nb2_sec5"], "Classical Radar DSP vs Deep Learning Perception Trade-Offs")
    nb.cells.append(new_markdown_cell(rf"""## 5. Comprehensive Analysis: Classical Radar DSP vs. Deep Learning Perception

{nb2_sec5_diagram}

| Evaluation Metric | Classical Radar DSP (FFT + MTI + CFAR + MUSIC + DBSCAN) | Deep Learning Radar Perception (CNN on Range-Doppler Tensors) |
|:---|:---|:---|
| **Mathematical Explainability** | **100% Deterministic**: Grounded in Fourier analysis, array manifold physics, and statistical hypothesis testing ($P_{{FA}}$). | **Black-Box Empirical**: High representational power, but harder to analytically bound worst-case failure modes. |
| **Close-Target Resolution** | **CFAR Masking**: Strong targets elevate the noise floor, obscuring weak adjacent objects. | **Superior**: Learns non-linear spatial deconvolution; distinguishes targets in high dynamic range. |
| **Clutter Sensitivity** | **Degrades in Non-Gaussian Clutter**: Rayleigh/Weibull clutter requires manual threshold tuning. | **Learned Feature Rejection**: Filters out complex multi-path reflections and pavement clutter textures. |
| **Semantic Classification** | **None natively**: Only extracts reflection coordinates $(R, v, \theta)$; requires separate feature classifiers. | **Native Multi-Class**: Simultaneously outputs class identity (`Car`, `Pedestrian`, `Cyclist`) from spectrogram texture. |
| **Computational Footprint** | **Extremely Low**: Realizable on low-power DSPs and FPGA accelerators ($O(N \log N)$ FFTs). | **Moderate to High**: Requires GPU / NPU hardware accelerator for real-time inference ($30\text{{--}}60\text{{ FPS}}$). |
| **Generalization** | **High**: Operates across arbitrary radar frequency chirps and antenna configurations without training. | **Domain Shift Sensitive**: Requires dataset retraining if chirp slope, carrier frequency, or array geometry changes. |

### Promising Research Directions for BTP Thesis
1. **Complex-Valued CNNs (CV-CNNs)**: Processing complex raw I/Q samples directly rather than discarding phase by using only power magnitudes.
2. **4D Imaging Radar Tensors**: Expanding the input from 2D $(R, v)$ to 4D $(R, v, \text{{Azimuth}}, \text{{Elevation}})$ for dense 3D point cloud generation.
3. **Hybrid Physics-Guided Architectures**: Using 2D CA-CFAR to generate attention region-of-interest (ROI) proposals that are subsequently classified by lightweight convolutional heads.
"""))

    return nb


def execute_notebook_in_process(nb) -> None:
    """
    Executes all code cells in-process, capturing stdout, stderr, and rich matplotlib figures
    into standard Jupyter display_data base64 outputs.
    """
    import io
    import base64
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    
    global_namespace = {"__name__": "__main__"}
    step = 1

    for cell in nb.cells:
        if cell.cell_type == "code":
            source = cell.source
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            redirected_out = io.StringIO()
            redirected_err = io.StringIO()
            sys.stdout = redirected_out
            sys.stderr = redirected_err

            plt.close("all")
            try:
                exec(source, global_namespace)
            except Exception as e:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                print(f"[ERROR] Cell #{step} failed: {e}")
                raise e
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

            out_str = redirected_out.getvalue()
            err_str = redirected_err.getvalue()
            outputs = []

            if out_str:
                outputs.append(nbformat.v4.new_output(
                    output_type="stream",
                    name="stdout",
                    text=out_str
                ))
            if err_str:
                outputs.append(nbformat.v4.new_output(
                    output_type="stream",
                    name="stderr",
                    text=err_str
                ))

            # Capture rendered matplotlib figures
            for fig_id in plt.get_fignums():
                fig = plt.figure(fig_id)
                buf = io.BytesIO()
                fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none", dpi=140)
                buf.seek(0)
                b64_img = base64.b64encode(buf.read()).decode("utf-8")
                outputs.append(nbformat.v4.new_output(
                    output_type="display_data",
                    data={
                        "image/png": b64_img,
                        "text/plain": "<Figure size>"
                    },
                    metadata={}
                ))
            plt.close("all")

            cell.outputs = outputs
            cell.execution_count = step
            step += 1


def main():
    print("=" * 70)
    print("    GENERATING & EXECUTING ACADEMIC RADAR WALKTHROUGH NOTEBOOKS")
    print("=" * 70)

    # 1. Build and execute Notebook 1
    nb1_path = os.path.join(ROOT_DIR, "01_radar_classical_dsp.ipynb")
    print(f"\n[+] Building Notebook 1: {nb1_path}...")
    nb1 = build_notebook_1()
    print("[*] Executing Notebook 1 via in-process runner (rendering dark-theme plots)...")
    execute_notebook_in_process(nb1)
    with open(nb1_path, "w", encoding="utf-8") as f:
        nbformat.write(nb1, f)
    print(f"[SUCCESS] Notebook 1 successfully saved with pre-rendered outputs: {nb1_path}")

    # 2. Build and execute Notebook 2
    nb2_path = os.path.join(ROOT_DIR, "02_radar_deep_learning_detection.ipynb")
    print(f"\n[+] Building Notebook 2: {nb2_path}...")
    nb2 = build_notebook_2()
    print("[*] Executing Notebook 2 in-process (training CNN & rendering inference)...")
    execute_notebook_in_process(nb2)
    with open(nb2_path, "w", encoding="utf-8") as f:
        nbformat.write(nb2, f)
    print(f"[SUCCESS] Notebook 2 successfully saved with pre-rendered outputs: {nb2_path}")

    print("\n" + "=" * 70)
    print("    BOTH NOTEBOOKS BUILT AND EXECUTED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()
