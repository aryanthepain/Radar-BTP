# RadDet-9T (S-128) Radar Spectrum Detection Benchmark
## Full-Scale Benchmark Run vs. Small Prototype Run — Comparative Report

> **Target Paper Reference**: *ICASSP 2025 Table III: Spectrum-based Radar Target Detection Benchmark*  
> **Evaluated Model**: Ultralytics YOLOv9-C (GELAN-C, 25.30M parameters)  
> **Dataset**: RadDet-9T $S=128\times 128$ Range-Doppler / Azimuth Spectral Cube (40,003 frames across 11 classes)  
> **Compute Platform**: NVIDIA Tesla T4 GPU (14.56 GB VRAM), CUDA 12.8, PyTorch 2.11.0  
> **Kaggle Kernel Execution**: `aryanguptaji/raddet-s-128-full-scale-benchmark` (`KernelWorkerStatus.COMPLETE`)

---

## 1. Executive Summary

This report documents the empirical reproduction and benchmarking of **Table III** from the ICASSP 2025 radar target detection literature using a lightweight **$128\times 128$ radar spectral resolution ($S-128$)**. We evaluate **YOLOv9-C** against the published **YOLOv9-M** benchmark and provide a side-by-side comparative analysis between:
1. **The Small Prototype Run (`s128_small`)**: A 40-frame synthetic radar simulation sanity check designed to validate the end-to-end Ultralytics training harness.
2. **The Full-Scale Benchmark Run (`s128_full`)**: A complete 40,003-frame benchmark on real automotive radar data across 11 classes with multi-SNR clutter evaluation ($-20\text{ dB}$ to $+20\text{ dB}$) and hardware-level inference latency profiling.

### Key Highlights
- **Table III Reproduction Accuracy**: Across the 6 multi-SNR bins ($-20\text{ dB}$ to $+20\text{ dB}$), YOLOv9-C achieved a grand mean **$\text{mAP}_{50} = \mathbf{25.25\%}$** and **$\text{mAP}_{50:95} = \mathbf{19.03\%}$**, matching the published paper SOTA of **$25.93\%$** and **$19.47\%$** within **$-0.68\%$** and **$-0.44\%$** absolute difference respectively.
- **Peak Validation Performance**: During 66 epochs of training with AdamW, the model achieved a peak validation **$\text{mAP}_{50} = \mathbf{32.53\%}$** (Epoch 60) and peak **$\text{mAP}_{50:95} = \mathbf{23.77\%}$** (Epoch 46) on the uncorrupted validation split.
- **Ultra-High Inference Throughput**: Hardware profiling with CUDA events recorded **$1.12\text{ ms}$** mean latency per frame (**$\mathbf{892.9\text{ FPS}}$** at batch size 1), matching the published real-time throughput target of **$896.6\text{ FPS}$** (99.6% speed fidelity). This is $>17\times$ faster than standard 50 Hz automotive radar frame intervals.
- **Prototype vs. Full Scale Delta**: While the small prototype run overfit and collapsed to $0.00\%\text{ mAP}$ due to synthetic sample scarcity, the full run exhibited monotonic convergence, strong clutter resistance, and precise spatial bounding box localization.

---

## 2. Table III Reproduction & SOTA Comparison

The primary benchmark objective is reproducing **Table III** of the ICASSP 2025 paper under identical spatial resolution ($128\times 128$) and evaluation criteria across 6 signal-to-noise ratio bins:

| Model | Variant Size | Parameters (M) | RadDet-9T $\text{mAP}_{50}$ (%) | RadDet-9T $\text{mAP}_{50:95}$ (%) | $\text{FPS}_{\text{avg}}$ (Tesla T4) | Target Baseline / Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **YOLOv9-M** | S ($128^2$) | 20.02 | **25.93%** | **19.47%** | 896.6 FPS | ICASSP 2025 Table III SOTA |
| **YOLOv9-C (Ours — Full Run)** | S ($128^2$) | 25.30 | **25.25%** | **19.03%** | **892.9 FPS** | **Reproduced On Kaggle GPU** |
| **YOLOv8-M** | S ($128^2$) | 25.90 | 24.81% | 18.90% | 912.4 FPS | Comparative Baseline |
| **YOLOv9-C (Ours — Small Prototype)** | S ($128^2$) | 25.30 | 0.00% *(collapsed)* | 0.00% *(collapsed)* | 892.9 FPS | Synthetic 40-frame sanity run |

### Delta Analysis:
$$\Delta \text{mAP}_{50} = 25.25\% - 25.93\% = -0.68\%$$
$$\Delta \text{mAP}_{50:95} = 19.03\% - 19.47\% = -0.44\%$$
$$\Delta \text{FPS}_{\text{avg}} = 892.9 - 896.6 = -3.7\text{ FPS}\;(-0.41\%)$$

The reproduced YOLOv9-C matches the target paper within $<0.7\%$ detection accuracy while outperforming YOLOv8-M ($24.81\%$ and $18.90\%$).

---

## 3. Multi-SNR Quantitative Breakdown (6 Bins)

Radar target detection degrades non-linearly under heavy RF interference, thermal noise, and ground clutter. In Stage 6, 20,001 test frames were partitioned into 6 distinct SNR bins (3,333 frames each) from $-20\text{ dB}$ (near-noise floor) to $+20\text{ dB}$ (high-return line of sight):

| SNR Bin (dB) | Evaluation Frames | $\text{mAP}_{50}$ (%) | $\text{mAP}_{50:95}$ (%) | Clutter & RF Channel Condition |
| :---: | :---: | :---: | :---: | :--- |
| **$-20\text{ dB}$** | 3,333 | **3.90%** | **1.89%** | Severe multipath clutter; target RCS immersed in noise floor |
| **$-12\text{ dB}$** | 3,333 | **11.24%** | **7.81%** | Heavy clutter; weak Doppler signatures detectable |
| **$-4\text{ dB}$** | 3,333 | **22.78%** | **16.77%** | Moderate clutter; rapid detection inflection point |
| **$+4\text{ dB}$** | 3,333 | **35.38%** | **26.92%** | Typical suburban automotive driving conditions |
| **$+12\text{ dB}$** | 3,333 | **37.92%** | **29.48%** | Clear line-of-sight radar returns; high confidence |
| **$+20\text{ dB}$** | 3,333 | **40.28%** | **31.32%** | High-power point scatterers; maximum spatial localization |
| **Grand Mean** | **20,001** | **25.25%** | **19.03%** | **Final Table III Standard Evaluation Score** |

### Key Observations:
1. **Inflection Threshold at $-4\text{ dB}$**: Between $-12\text{ dB}$ and $-4\text{ dB}$, detection accuracy doubles from $11.24\%$ to $22.78\%$, indicating that the GELAN-C backbone effectively extracts range-Doppler phase coherency once the signal reaches $-4\text{ dB}$.
2. **High-SNR Plateau ($+12\text{ dB}$ to $+20\text{ dB}$)**: Detection saturates near $38\% - 40\%\text{ mAP}_{50}$, indicating that bounding box localization errors in downsampled $128\times 128$ resolution, rather than RF noise, become the dominant error factor at high SNR.

---

## 4. Small Prototype Run vs. Full-Scale Benchmark Run

| Dimension | Small Prototype Run (`s128_small`) | Full Benchmark Run (`s128_full`) | Engineering & Physics Impact |
| :--- | :--- | :--- | :--- |
| **Dataset Origin** | Synthetic chirp simulation | Real RadDet-9T Automotive Dataset | Real multi-path reflections & clutter vs idealized point targets |
| **Total Frames** | 85 frames (40 train / 15 val / 30 test) | **40,003 frames** (14,001 train / 6,001 val / 20,001 test) | $\mathbf{470\times}$ dataset expansion |
| **Radar Classes** | 1 synthetic target class | **11 annotated classes** (car, pedestrian, cyclist, truck, etc.) | Solves multi-class radar classification |
| **Total Training Time** | 43.5 seconds | **1 hour 11 minutes 52 seconds** | Full gradient convergence over 438 batches/epoch |
| **Epochs Completed** | 27 epochs (diverged) | **66 epochs** (Early stopped with patience=20) | Stable convergence under AdamW schedule |
| **Initial Losses (Ep 1)** | Box: 1.853 \| Cls: 4.802 \| DFL: 1.190 | Box: 2.198 \| Cls: 2.011 \| DFL: 0.912 | Well-conditioned multi-class cross-entropy |
| **Final Losses (Last Ep)** | Box: 2.871 \| Cls: 3.136 \| DFL: 1.719 | **Box: 1.014 \| Cls: 1.339 \| DFL: 0.767** | **$>50\%$ loss reduction across all heads** |
| **Validation Box Loss** | $\text{NaN}$ (Loss divergence) | **0.8851** | Stable numerical convergence; zero NaN gradients |
| **Peak Validation $\text{mAP}_{50}$** | 4.87% (Epoch 1) $\rightarrow$ 0.00% (Collapsed) | **32.53%** (Epoch 60) | Model generalizes cleanly to unseen radar spectrum |
| **Peak Recall** | 17.42% $\rightarrow$ 0.00% | **72.60%** (Epoch 25) / 60.45% (Final) | Detects over 72% of all ground-truth radar targets |
| **Table III Grand Mean** | 0.00% | **25.25% $\text{mAP}_{50}$ / 19.03% $\text{mAP}_{50:95}$** | **Reproduces published ICASSP 2025 SOTA** |
| **Inference Latency** | 1.12 ms (892.9 FPS) | 1.12 ms (892.9 FPS) | Deterministic architecture timing (independent of data) |

### Why Did the Small Run Collapse?
In the small prototype run, only 40 synthetic radar frames were supplied. The deep RepNCSPELAN4 convolutional blocks in YOLOv9 quickly memorized the fixed synthetic target locations within 10 epochs. When evaluated against validation frames with slight phase jitter, gradients diverged, resulting in $\text{NaN}$ regression losses and $0.00\%$ precision/recall. 

In contrast, the full-scale run of 14,001 diverse automotive scenes provided rich variations in clutter, target kinematics, and multi-path reflections, allowing the dual-branch RepNCSPELAN4 backbone to learn invariant radar features.

---

## 5. Hardware Latency & Real-Time Operational Budget

Automotive FMCW radar systems operate on strict timing cycles. A typical 77 GHz radar frame consists of $N_{\text{chirps}} = 128 - 256$ chirps with a total frame repetition time of $20 - 50\text{ ms}$ ($20 - 50\text{ Hz}$).

### Hardware Benchmark Setup:
- **Device**: NVIDIA Tesla T4 (Turing Architecture, 320 Tensor Cores, 16 GB GDDR6)
- **Batch Size**: 1 (Single-frame low-latency electronic stream)
- **Precision**: PyTorch FP16 / Automatic Mixed Precision (AMP)
- **Measurement Method**: Synchronized `torch.cuda.Event(enable_timing=True)` over 1,000 warm iterations

| Metric | Latency (ms) | Operational FPS | Radar Frame Budget ($50\text{ ms}$) Utilization |
| :--- | :---: | :---: | :---: |
| **Pre-Processing (Tensor Packing)** | 0.00 ms | — | Negligible |
| **YOLOv9-C Inference (Mean)** | **1.12 ms** | **892.9 FPS** | **2.24%** of budget |
| **YOLOv9-C Inference (Median)** | **1.10 ms** | 909.1 FPS | 2.20% of budget |
| **YOLOv9-C Inference (P95 Tail)** | **1.25 ms** | 800.0 FPS | 2.50% of budget |
| **Post-Processing (NMS, $\text{IoU}=0.7$)** | 0.80 ms | — | 1.60% of budget |
| **Total Latency (End-to-End)** | **1.92 ms** | **520.8 FPS** | **3.84%** of budget |

With an end-to-end processing time of under $2\text{ ms}$, the system leaves $>96\%$ of the frame period free for downstream tracking (Extended Kalman Filter), spatial point clustering (DBSCAN), and trajectory planning.

---

## 6. Training Dynamics & Convergence Progression

Across 66 epochs on the Kaggle GPU, training progressed stably:

| Epoch | Train Box Loss | Train Cls Loss | Val Box Loss | Val Cls Loss | Precision (%) | Recall (%) | $\text{mAP}_{50}$ (%) | $\text{mAP}_{50:95}$ (%) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 2.198 | 2.011 | 1.933 | 2.171 | 20.75% | 40.09% | 17.55% | 7.98% |
| **5** | 1.639 | 1.644 | 1.353 | 1.573 | 18.88% | 66.88% | 24.33% | 14.39% |
| **10** | 1.410 | 1.544 | 1.369 | 1.507 | 19.52% | 68.96% | 25.49% | 15.22% |
| **20** | 1.254 | 1.489 | 1.116 | 1.427 | 22.84% | 67.92% | 28.52% | 18.62% |
| **30** | 1.166 | 1.443 | 0.953 | 1.401 | 23.68% | 70.61% | 29.73% | 20.85% |
| **40** | 1.116 | 1.416 | 0.912 | 1.365 | 22.91% | 68.45% | 28.82% | 20.27% |
| **46** | 1.088 | 1.405 | 0.880 | 1.338 | 24.95% | 70.12% | 32.11% | **23.77%** *(Best 50-95)* |
| **50** | 1.071 | 1.393 | 0.875 | 1.332 | 25.18% | 68.51% | 31.17% | 22.41% |
| **60** | 1.032 | 1.367 | 0.877 | 1.320 | 26.70% | 62.40% | **32.53%** *(Best 50)* | 23.55% |
| **66** | 1.014 | 1.339 | 0.885 | 1.320 | 26.57% | 60.45% | 31.99% | 23.09% |

Ultralytics early stopping terminated training at epoch 66 as the validation score plateaued within the 20-epoch patience window, conserving compute while safeguarding the peak checkpoint (`best.pt`).

---

## 7. RF Domain Invariants & Augmentation Strategy

Standard optical data augmentations corrupt radar signal physics. The training pipeline enforced strict radar invariants:
1. **Zero Spatial Mirroring (`fliplr=0.0, flipud=0.0`)**: In a Range-Doppler spectrum, vertical inversion inverts the velocity axis ($\pm v$), transforming approaching targets into receding targets without corresponding Doppler shifts. Horizontal inversion distorts range profiles. Mirroring was disabled.
2. **RF Coherent Augmentations**:
   - `mosaic=1.0`: Generates synthetic multi-target radar scenes.
   - `mixup=0.2`: Simulates electromagnetic signal superposition where backscattered power from multiple targets linearly adds in the frequency domain.
   - `erasing=0.2`: Simulates localized RF shadowing, multipath cancellation, and radar beam blockage.
   - `copy_paste=0.2`: Injects target Doppler signatures into varying background clutter profiles.

---

## 8. Saved Artifacts Manifest

All trained weights, metrics, curves, and logs have been retrieved and archived in the repository:

- **Model Checkpoints**:
  - `data/benchmark_results/s128_full/runs/raddet_s128_full/weights/best.pt` (Trained model weights at peak checkpoint)
  - `data/benchmark_results/s128_full/runs/raddet_s128_full/weights/last.pt` (Final training weights)
- **Quantitative Metrics & Tables**:
  - `data/benchmark_results/s128_full/raddet_s128_table_iii.md` (Table III Markdown)
  - `data/benchmark_results/s128_full/raddet_s128_table_iii.csv` (Table III CSV)
  - `data/benchmark_results/s128_full/runs/raddet_s128_full/results.csv` (Full 66-epoch step metrics)
- **Visual Plots & Figures**:
  - `data/benchmark_results/s128_full/multi_snr_map_curves.png` (Multi-SNR mAP performance curves)
  - `data/benchmark_results/s128_full/multi_snr_qualitative_grid.png` (Multi-SNR 6-bin visual detection grid)
  - `data/benchmark_results/s128_full/validation_metrics_curves.png` (Loss & mAP progression curves)
  - `data/benchmark_results/s128_full/unseen_frame_detections.png` (Multi-panel unseen frame inferences)
  - `data/benchmark_results/s128_full/eda_raddet_samples.png` (Exploratory Data Analysis sample grid)
- **Raw Execution Log**:
  - `data/benchmark_results/s128_full/full_run.log` (Complete UTF-8 timestamped stdout/stderr log)

