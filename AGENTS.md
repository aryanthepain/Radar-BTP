# AGENTS.md — Radar DSP & Deep Learning Detection Operating Context

> [!NOTE]
> Global behavioral invariants (Single-task delivery contract, Ponytail anti-bloat ladder, Karpathy surgical execution, Fleet loop verification) are inherited globally from `~/.gemini/config/rules/global_rules.md`.
> Repository-specific domain skills (`cloud-data`, `kaggle-gpu-fallback`, `schema-mapping`) and MCP servers (`kaggle`, `notebooks`, `data-agent-kit`) are declared in `.agents/skills.json` and `.agents/mcp_config.json`.

## 1. Project Commands & Deterministic Gates

- **Run Full Pipeline Testbench**: `python scripts/run_radar_pipeline.py`
- **Run Unit Test Suite**: `python -m unittest discover -s tests` or `pytest`
- **Run Targeted Test**: `python -m unittest tests/test_radar_dsp.py`
- **Run Kaggle Integration Test**: `pytest tests/test_kaggle_integration.py`
- **Universal Verification Gate**: `pwsh -File ./scripts/verify.ps1`
- **Stage & Push Kaggle Kernel**: `python scripts/push_kaggle_kernel.py --notebook <notebook.ipynb> --slug <slug> --push`
- **Check Kaggle Quota**: `kaggle quota`
- **Audio & Spoken Completion Alert**: `pwsh -File ./scripts/agent-alarm.ps1 -Type Success -Message "Task complete. All verification gates passed."`

## 2. Repository Architecture & Layout

- `src/sim/`: High-fidelity 77 GHz FMCW radar simulation (Chirp synthesizer, target RCS & kinematics, micro-Doppler pedestrian modulations, ground clutter & thermal noise).
- `src/dsp/`: Core Radar DSP primitives (1D Range FFT, MTI Clutter Filtering, 2D Slow-Time Doppler FFT, 2D CA/OS-CFAR, Spatial MUSIC/Capon AoA Estimator, DBSCAN Point Cloud Clustering).
- `src/models/`: AI/Deep Learning Radar Detectors (PyTorch `RadarObjectDetectorCNN` multi-task heatmap + bounding box regressor, `RadarDataset` generator, training routines).
- `src/telemetry.py`: In-container stage-wise progress tracker with dynamic ETC/ETA calculation conforming to global Kaggle telemetry rules.
- `scripts/`: End-to-end simulation, training, visualization testbenches (`run_radar_pipeline.py`), Kaggle kernel builder & push automation (`push_kaggle_kernel.py`), and verification scripts (`verify.ps1`, `agent-alarm.ps1`).
- `tests/`: Deterministic unit tests covering radar physics, DSP equations, clutter attenuation, CFAR detection, AoA resolution, CNN gradient propagation, and Kaggle telemetry/packaging.
- `data/`: Processed radar cubes, tensors, and datasets.
- `.agents/`: Repository-specific declarative skill manifest (`skills.json`) and MCP configuration (`mcp_config.json` enabling `kaggle`, `notebooks`, `data-agent-kit`).

## 3. Kaggle Operating Rules & Invariants

- **Dual-Environment Path Abstraction**:
  - **Inputs**: Check `/kaggle/input/<dataset>` first (Kaggle cloud runtime), fallback gracefully to `./data/<dataset>` (local workstation). NEVER write or mutate files in `/kaggle/input`.
  - **Outputs**: All checkpoints, exported weights, evaluation metrics, and figure plots must be written to `/kaggle/working/` (Kaggle cloud) or `./output/` / `./data/` (local workstation).
- **Mandatory In-Container Telemetry & Stage-Wise ETC/ETA**:
  - Any script or notebook running inside Kaggle or a container must self-report progress using `StageProgressTracker` from `src.telemetry`.
  - Logs must emit structured, timestamped progress (`[YYYY-MM-DD HH:MM:SS] [INFO] [STAGE X/Y: ...]`) with processed item count, percentage, elapsed duration, stage throughput, stage ETC, and ETA.
  - Never rely on external agents or external polling loops to calculate remaining time from outside.
- **Output Buffer Crash Prevention**:
  - Kaggle crashes web notebook frontends when cell output exceeds ~20MB.
  - Disable or throttle verbose progress bars (`tqdm(..., mininterval=5.0)` or step-based logging).
- **Headless Non-Interactive Rendering**:
  - Set `matplotlib.use('Agg')` in all non-interactive scripts and background Kaggle kernels to prevent GUI window deadlocks.
- **GPU Accelerator Guardrails**:
  - Optimize memory for Kaggle P100 (16GB VRAM) and dual T4 (15GB VRAM each).
  - Use PyTorch Automatic Mixed Precision (`torch.cuda.amp.autocast`) and explicit `torch.cuda.empty_cache()` where appropriate to prevent CUDA OOM.
- **Radar Equation Standards & Zero Disruption Invariant**:
  - Maintain strict adherence to FMCW radar principles (Range resolution $\Delta R = \frac{c}{2B}$, Velocity resolution $\Delta v = \frac{\lambda}{2 N_{chirps} T_c}$, Spatial array steering vectors $a(\theta) = e^{-j 2\pi d \sin(\theta)/\lambda}$).
  - 100% preservation of all existing synthetic radar simulation, DSP, and CNN code (`src/sim/*`, `src/dsp/*`, `src/models/*`, and notebooks `01_*`, `02_*`).

## 4. Ephemeral Memory (`WORKING.md`)

- Maintain active sprint objectives, test failure traces, hypotheses, and blockers in `WORKING.md`.
