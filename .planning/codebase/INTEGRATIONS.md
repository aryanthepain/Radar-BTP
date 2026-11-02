# External Integrations

**Analysis Date:** 2026-09-23

## APIs & External Services

**Autonomous Air-Gapped Simulation:**
- The radar testbench is entirely self-contained. It operates with zero dependencies on external web services, proprietary cloud APIs, or external SaaS endpoints.
- All radar I/Q ADC data, multi-target scenarios, ground clutter, and noise are synthesized on-demand in `src/sim/radar_sim.py`.

**Academic Datasets & Research References:**
- `RadDet_A_Wideband_Dataset_for_Real-Time_Radar_Spectrum_Detection.pdf` — Reference specification for automotive FMCW radar dataset benchmarking (Range-Doppler-Azimuth tensors).
- `Artificial_Intelligence_based_Radar_Technology_Current_Advancements_Future_Directions_and_Challenges.pdf` — Survey literature on radar signal processing and neural architectures.
- `FULLTEXT01_AI_radar.pdf` — Deep learning methods in FMCW radar perception.

## Data Storage

**Local File Storage:**
- Directory: `data/processed/`
  - Output visualization dashboard: `data/processed/radar_pipeline_eda.png` (9-panel high-resolution publication-ready diagnostic figure).
  - Tracked via `.gitkeep` (`data/processed/.gitkeep`).
- In-Memory Data Tensors:
  - Raw complex 3D radar cube: `(num_rx, num_chirps, num_samples)` complex128 NumPy array.
  - Range-Doppler Matrix (RDM): `(num_rx, num_doppler, num_range)` complex128 NumPy array.
  - Deep Learning Tensors: `(batch_size, 1, num_doppler, num_range)` float32 PyTorch tensors.

**Databases:**
- None required. The project uses in-memory tensor pipelines and filesystem artifacts.

**Caching:**
- None. Waveform synthesis and DSP transforms are computed on the fly (<2 seconds per scenario).

## Authentication & Identity

**Auth Provider:**
- None required (no external user accounts, logins, or API keys).

**Local Development & Git Identity:**
- Version control is integrated with local Git configuration.
- Remote repository link: `aryanthepain/Radar-BTP` on GitHub.

## Monitoring & Observability

**Audio & Spoken Completion Alerts:**
- Script: `scripts/agent-alarm.ps1`
  - Platform hook: Windows PowerShell interop with SAPI (`System.Speech.Synthesis.SpeechSynthesizer`).
  - Terminal audio fallback: `[System.Media.SystemSounds]::Asterisk` / `Hand`.
  - Used for audible developer feedback upon completion of verification gates or pipeline runs.

**Deterministic Verification Gate:**
- Script: `scripts/verify.ps1`
  - Runs automated test suites (`pytest` / `unittest`) and outputs colored pass/fail status with exit codes.

**Logging:**
- Standard output (`stdout`) and error streams (`stderr`).
- Formatted console tables and section headers for real-time stage progression.

## CI/CD & Deployment

**Version Control:**
- Git repository tracked on branch `main`.
- Remote: `origin/main` (`https://github.com/aryanthepain/Radar-BTP`).

**Local Git Hooks:**
- Hook: `.githooks/pre-commit`
  - Triggers pre-commit validation to guarantee tests pass before commits are finalized.

**Hosting & Distribution:**
- Local academic research repository; executable directly via Python scripts and Jupyter notebooks.

## Environment Configuration

**Development:**
- No API keys, tokens, or secret credentials needed (`.env` is not required).
- Zero risk of cloud credential leakage.

## Webhooks & Callbacks

**Incoming:**
- None.

**Outgoing:**
- None.

---

*Integration audit: 2026-09-23*
*Update when adding/removing external services*
