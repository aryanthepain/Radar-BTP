# Codebase Concerns

**Analysis Date:** 2026-09-23

## Tech Debt

**Python Loop-Based 2D CFAR Detector:**
- **Issue**: `src/dsp/cfar_detector.py` uses nested Python `for` loops across Doppler and range dimensions to extract sliding training/guard windows for each Cell Under Test (CUT).
- **Why**: Implemented for clarity and mathematical transparency during initial prototyping of CA, OS, GOCA, and SOCA algorithms.
- **Impact**: Execution time scales with matrix size $O(N_d \times N_r \times W_d \times W_r)$. For $128 \times 256$ cells, it takes ~0.5–1.0s in pure Python, which is too slow for real-time 60 FPS streaming.
- **Fix approach**: Vectorize the 2D window summation using `scipy.signal.convolve2d` (or uniform 2D box filters) for CA-CFAR, or PyTorch 2D Average Pooling kernels.

**On-The-Fly In-Memory Synthetic Dataset Generation:**
- **Issue**: `src/models/radar_dataset.py` synthesizes complete raw FMCW radar cubes, runs Range FFT, MTI, and Doppler FFT dynamically during each `__getitem__` call.
- **Why**: Avoided committing large gigabyte-scale radar binary tensor datasets into Git.
- **Impact**: Limits training throughput when increasing epochs or batch sizes, as CPU cycles are consumed synthesizing beat signals rather than training neural weights.
- **Fix approach**: Add a disk-caching or offline pre-generation script saving precomputed RDM tensors to `.npy` or memory-mapped HDF5/Zarr archives in `data/processed/`.

## Known Bugs

**LOKY Physical Core Detection Warning on Windows:**
- **Symptoms**: `UserWarning: Could not find the number of physical cores for the following reason: [WinError 2] The system cannot find the file specified` logged during pytest runs from `joblib.externals.loky`.
- **Trigger**: Occurs when running `pytest` on Windows where `loky` attempts to query system utilities that are unavailable in certain PowerShell subshells.
- **Workaround**: Tests pass cleanly regardless (`7 passed, 1 warning`). Setting environment variable `LOKY_MAX_CPU_COUNT=4` suppresses the warning.
- **Root cause**: Internal scikit-learn / joblib platform detection quirk on Windows 11.
- **Fix**: Set `$env:LOKY_MAX_CPU_COUNT = [Environment]::ProcessorCount` in `scripts/verify.ps1`.

## Security Considerations

**Zero External Attack Surface:**
- **Risk**: Remote execution or credential leakage.
- **Current mitigation**: The repository runs 100% locally with zero external network socket listeners, zero cloud API credentials, and zero hardcoded secrets.
- **Recommendations**: Continue enforcing the rule that no secret credentials or external telemetry tokens are committed to this repository.

## Performance Bottlenecks

**MUSIC Azimuth Pseudo-Spectrum Scanning:**
- **Problem**: In `src/dsp/aoa_estimation.py`, `estimate_aoa_music` performs spatial steering vector inner products over 181 angular bins per detected CFAR peak.
- **Measurement**: Negligible for 1–5 targets (~15 ms), but scales linearly with the number of raw CFAR detections before clustering.
- **Cause**: Array-level loop across angle bins and unbatched eigenvalue decompositions.
- **Improvement path**: Batch all detected spatial snapshots into a single 3D tensor and compute the pseudo-spectrum across all detections simultaneously via matrix multiplication.

**High-Resolution 4D Radar Tensors Memory Footprint:**
- **Problem**: When expanding radar simulation to cascade radar configurations (e.g. 12 Tx × 16 Rx virtual array with 512 samples × 256 chirps), a single frame reaches hundreds of megabytes.
- **Measurement**: Current 4 Rx × 128 chirps × 256 samples complex128 array is compact (~4 MB per frame), but multi-frame scenarios in 32-bit complex can strain RAM.
- **Improvement path**: Downcast complex arrays from `complex128` (64-bit float I + 64-bit float Q) to `complex64` (32-bit float I + 32-bit float Q) across `src/sim/radar_sim.py` and `src/dsp/`.

## Fragile Areas

**Azimuth Sign and Coordinate System Conventions:**
- **Files**: `src/sim/radar_sim.py`, `src/dsp/aoa_estimation.py`, `src/dsp/clustering.py`.
- **Why fragile**: Radar coordinate conventions differ across robotics (ISO 8855 vs SAE vs standard Cartesian: X cross-range vs X forward). In `src/dsp/clustering.py`, $X = R \sin(\theta)$ and $Y = R \cos(\theta)$, which defines $Y$ as forward range. If a module swaps azimuth sign ($+\theta$ left vs $+\theta$ right), target tracks will mirror in Cartesian BEV.
- **Safe modification**: Always run `tests/test_radar_dsp.py::test_music_aoa_estimation` when altering antenna spacing, steering vectors, or Cartesian conversions.
- **Test coverage**: Unit test explicitly verifies that a $-20.0^\circ$ target resolves to $-20.0^\circ \pm 2^\circ$.

## Scaling Limits

**Hardware Scaling Limits:**
- **Current capacity**: Synthetic testbench runs comfortably on CPU (1.5s for 7 unit tests; 15s for full training demo).
- **Limit**: Training deep learning detectors on real-world raw ADC datasets (e.g., RADDet 10,000+ frames) will require GPU acceleration (`torch.cuda`).
- **Scaling path**: Introduce batch DataLoader GPU streaming and Mixed Precision (`torch.cuda.amp.autocast`).

## Missing Critical Features

**Extended Kalman Filter (EKF) / GNN Multi-Target Tracking:**
- **Problem**: Current pipeline stops at spatial clustering (`RadarClusterer` via DBSCAN), outputting single-frame object centroid estimates without temporal track association or velocity smoothing over time.
- **Blocks**: Multi-frame track continuity and track ID persistence across occlusions.
- **Implementation complexity**: Medium — implement a constant-velocity or coordinated turn 2D EKF with Hungarian / Global Nearest Neighbor (GNN) association.

**Real Dataset Ingestion & Hardware Packet Parsers:**
- **Problem**: Currently only supports simulated synthetic radar cubes. Cannot directly ingest binary ADC streams from Texas Instruments DCA1000EVM capture cards or open datasets (RADDet / CARRADA).
- **Blocks**: Validating detector models on real physical sensor data.
- **Implementation complexity**: Medium — build a DCA1000EVM raw LVDS packet parser in `src/sim/` and a RADDet dataset loader in `src/models/`.

## Test Coverage Gaps

**CFAR Detector Variants (OS, GOCA, SOCA):**
- **What's not tested**: `tests/test_radar_dsp.py` exercises CA-CFAR (`cfar_type="ca"`), but does not have dedicated automated assertions for `os`, `goca`, and `soca` branches in `src/dsp/cfar_detector.py`.
- **Risk**: Edge case bugs in ordered-statistic sorting or window splitting could go undetected.
- **Priority**: Medium.

**Micro-Doppler STFT Time-Frequency Extraction:**
- **What's not tested**: `DopplerProcessor.compute_micro_doppler_spectrogram` is verified visually in `scripts/run_radar_pipeline.py` (Panel 7), but lacks a standalone numerical assertion in `tests/test_radar_dsp.py`.
- **Risk**: Frequency shift or time grid calculation regressions.
- **Priority**: Low.

---

*Concerns audit: 2026-09-23*
*Update as issues are fixed or new ones discovered*
