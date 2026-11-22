# Integration Instructions

Use the following evidence hierarchy when integrating content:

1. Executed notebook cells and their actual saved outputs.
2. Saved experimental CSV files and genuine execution artifacts.
3. Source implementation, to verify configurations and algorithm behaviour.
4. Published papers, for external reference results.

you will need to write math properly. also look at agent instructions for good figures

for 4.3.2 take the metrics from the fully trained model

# Chapter 4: Experimental Results and Analysis

## 4.1 Experimental Scope and Evaluation Framework

The experimental investigation presented in this chapter evaluates the radar-processing and learning-based detection approaches developed during the first phase of the project. The experiments provide an initial assessment of the implemented signal-processing pipeline, synthetic radar detection models, and wideband radar spectrum-detection framework. The results also establish a foundation for investigating the computational requirements of AI-based radar detection.

The evaluation is divided into two experimental tracks, corresponding to the methodology described in Chapter 3.

**Track I: Synthetic FMCW Radar Perception.** This track investigates the generation and processing of synthetic 77 GHz FMCW radar measurements. It evaluates conventional radar signal-processing operations, including range estimation, clutter suppression, Doppler processing, CFAR detection, direction-of-arrival estimation, and spatial clustering. A convolutional neural network is additionally developed and trained on synthetic Range-Doppler representations.

**Track II: Wideband Radar Spectrum Detection.** This track investigates the detection and classification of radar emissions using the RadDet dataset introduced by Huang et al. [2]. The dataset represents radar activity through labelled time-frequency spectrograms. A YOLO-based object-detection pipeline is developed for localising individual radar emissions and identifying their modulation categories.

Although these tracks share the broader objective of investigating AI applications in radar signal processing, they address different detection problems. The FMCW experiments examine the spatial perception of automotive targets, whereas the RadDet experiments concern radar emission detection in a wideband frequency spectrum. Their results are consequently evaluated and reported independently.

The experimental assessment considers three broad dimensions:

1. **Detection and estimation performance:** Accuracy of recovered physical quantities in synthetic FMCW experiments, along with the available object-detection metrics for learning-based models.
2. **Training behaviour:** Model parameter count, training and validation losses, and convergence characteristics.
3. **Computational requirements:** Model complexity, execution platform, inference latency, memory consumption, and practical hardware requirements, wherever measurements are available.

The distinction between completed experiments, published reference measurements, and proposed but unverified experiments is maintained throughout this chapter. This is particularly important when comparing the present work against published radar-detection benchmarks.

## 4.2 Experimental Track I: Synthetic FMCW Radar Perception

### 4.2.1 Radar Simulation Configuration and Generated Scene

The first experiment evaluates the implemented 77 GHz FMCW radar simulator under a controlled multi-target automotive scenario. The simulation uses four receiving antenna elements arranged as a uniform linear array (ULA), with 128 chirps per frame and 256 fast-time ADC samples per chirp.

The principal radar parameters are summarised in Table 4.1.

**Table 4.1: Configuration of the simulated FMCW radar system**

<table>
  <tr><th>Parameter</th><th>Value</th></tr>
  <tr><td>Operating carrier frequency</td><td>77 GHz</td></tr>
  <tr><td>Sweep bandwidth</td><td>1.0 GHz</td></tr>
  <tr><td>Chirp duration</td><td>50 (\mu s)</td></tr>
  <tr><td>ADC sampling frequency</td><td>5.12 MHz</td></tr>
  <tr><td>Fast-time samples per chirp</td><td>256</td></tr>
  <tr><td>Chirps per frame</td><td>128</td></tr>
  <tr><td>Receive antenna elements</td><td>4</td></tr>
  <tr><td>Antenna spacing</td><td>(\lambda/2)</td></tr>
  <tr><td>Operating wavelength</td><td>3.893 mm</td></tr>
  <tr><td>Theoretical range resolution</td><td>0.1499 m</td></tr>
  <tr><td>Theoretical velocity resolution</td><td>0.3042 m/s</td></tr>
  <tr><td>Maximum unambiguous range</td><td>38.37 m</td></tr>
  <tr><td>Maximum unambiguous velocity</td><td>(\pm19.47) m/s</td></tr>
</table>

The theoretical range resolution is determined by the transmitted sweep bandwidth:

[

\Delta R=\frac{c}{2B},

]

where (c) is the speed of light and (B) represents the transmitted bandwidth. For the selected bandwidth of 1 GHz,

[

\Delta R \approx 0.1499\text{ m}.

]

Similarly, the theoretical velocity resolution is

[

\Delta v=\frac{\lambda}{2N_cT_c},

]

where (N_c) is the number of chirps and (T_c) denotes the chirp duration. The configured values give a velocity resolution of approximately (0.3042\text{ m/s}).

The simulated automotive scene contains four targets with different physical characteristics. Two cars, a pedestrian, and a cyclist are placed at different ranges, velocities, and azimuth angles. Pedestrian motion additionally includes a periodic micro-Doppler component.

The complex baseband signals generated from these targets are superimposed together with stationary clutter and additive complex Gaussian noise. The experiment uses an input SNR of 18 dB, a clutter-to-noise ratio of 10 dB, and a fixed random seed of 42 to make the scene reproducible.

The generated radar data cube has dimensions

[

\mathbf{X}\in\mathbb{C}^{N\_{\mathrm{rx}}\times N_c\times N_s}

]

with

[

\boxed{\mathbf{X}\in\mathbb{C}^{4\times128\times256}}.

]

This corresponds to four receiving channels, 128 successive chirps, and 256 fast-time samples per chirp.

The experiment successfully generated the expected complex radar cube, establishing the input to the subsequent conventional signal-processing stages.

**Figure 4.1: Synthetic FMCW radar measurements and Range-Doppler representation.**

[AGENT INSTRUCTION — FIGURE 4.1]

Use the existing notebook results:

- `docs/assets/nb1/fig2_raw_3d_cube_signal.png`
- `docs/assets/nb1/fig5_doppler_fft_rdm.png`

Combine the raw radar-cube or I/Q representation with the corresponding Range-Doppler heatmap in a two-panel figure. Preserve the original axes, scale, and legends.

Caption: _Figure 4.1: Simulated complex FMCW radar measurements and the corresponding Range-Doppler representation for the multi-target automotive scene._

### 4.2.2 Range Processing and Ground-Clutter Suppression

The generated radar cube is processed using a conventional FMCW signal-processing chain. The first stage applies a Hann window along the fast-time dimension, followed by a one-dimensional FFT to estimate target range.

The Hann window reduces spectral leakage caused by finite observation duration. Its use provides a more controlled representation of target-frequency peaks, although the resulting spectral main-lobe width must also be considered when interpreting resolution [5].

Following range processing, mean-subtraction MTI filtering is applied along the slow-time dimension. The objective is to suppress stationary or slowly varying components associated with ground and environmental clutter.

The clutter attenuation achieved during the experiment is calculated by comparing the power of the range profiles before and after filtering.

The executed notebook records:

[

\boxed{A\_{\mathrm{clutter}}=12.94\text{ dB}}.

]

This represents the measured clutter attenuation for the selected synthetic scene and configured MTI operation. It demonstrates that the filtering stage reduces the stationary clutter component while retaining the moving-target returns required by subsequent Doppler processing.

Following clutter suppression, a slow-time Doppler FFT is applied to obtain the Range-Doppler Matrix (RDM). The Doppler spectrum is shifted so that zero Doppler appears at the centre of the representation.

The resulting RDM contains information about both target range and radial velocity. This representation is subsequently used by the CFAR detector.

**Figure 4.2: Range processing and MTI clutter-suppression results.**

[AGENT INSTRUCTION — FIGURE 4.2]

Reuse:

- `docs/assets/nb1/fig3_range_fft_windowing.png`
- `docs/assets/nb1/fig4_mti_clutter_suppression.png`

The first image should illustrate the range-processing result, while the second should show the actual power profiles before and after clutter suppression.

Retain the measured attenuation of 12.94 dB in the figure annotation or caption.

Caption: _Figure 4.2: Fast-time range processing and mean-subtraction MTI filtering of the simulated FMCW radar returns._

### 4.2.3 CA-CFAR Target Detection Results

The Range-Doppler power matrix is supplied to the implemented two-dimensional CA-CFAR detector. The detector estimates the local noise background around each Cell Under Test (CUT) using training cells and applies an adaptive threshold to identify candidate target peaks [6].

The executed experiment uses the following configuration:

<table>
  <tr><th>Parameter</th><th>Value</th></tr>
  <tr><td>CFAR variant</td><td>CA-CFAR</td></tr>
  <tr><td>Range training cells</td><td>4</td></tr>
  <tr><td>Doppler training cells</td><td>4</td></tr>
  <tr><td>Range guard cells</td><td>2</td></tr>
  <tr><td>Doppler guard cells</td><td>2</td></tr>
  <tr><td>False-alarm probability</td><td>(10^{-4})</td></tr>
</table>

The detector successfully identifies five candidate peaks in the simulated Range-Doppler representation.

The recorded results are presented in Table 4.2.

**Table 4.2: CA-CFAR detection results for the synthetic automotive scene**

<table>
  <tr><th>Detection</th><th>Estimated range (m)</th><th>Estimated velocity (m/s)</th><th>Reported SNR (dB)</th></tr>
  <tr><td>1</td><td>28.48</td><td>-13.99</td><td>43.0</td></tr>
  <tr><td>2</td><td>19.19</td><td>-4.87</td><td>41.8</td></tr>
  <tr><td>3</td><td>11.99</td><td>0.00</td><td>16.2</td></tr>
  <tr><td>4</td><td>8.39</td><td>+1.52</td><td>40.0</td></tr>
  <tr><td>5</td><td>11.99</td><td>+8.52</td><td>52.8</td></tr>
</table>

The four target-associated detections can be matched to the simulated target locations using their range and velocity estimates:

- The receding car is detected near 28.48 m with an estimated velocity of -13.99 m/s, compared with its simulated values of 28.5 m and -14.2 m/s.
- The cyclist is detected near 19.19 m with an estimated velocity of -4.87 m/s, compared with its simulated values of 19.2 m and -4.8 m/s.
- The approaching car is detected near 11.99 m with an estimated velocity of +8.52 m/s, compared with its simulated values of 12.0 m and +8.5 m/s.
- The pedestrian is detected near 8.39 m with an estimated velocity of +1.52 m/s, compared with its simulated values of 8.4 m and +1.4 m/s.

For these four manually associated target detections, the absolute range and velocity estimation errors are calculated as

[

e*R=|\hat R-R*{\mathrm{GT}}|

]

and

[

e*v=|\hat v-v*{\mathrm{GT}}|.

]

The resulting mean absolute errors are

[

\mathrm{MAE}\_R

=\frac{0.02+0.01+0.01+0.01}{4}

=\boxed{0.0125\text{ m}},

]

and

[

\mathrm{MAE}\_v

=\frac{0.21+0.07+0.02+0.12}{4}

=\boxed{0.105\text{ m/s}}.

]

These values demonstrate close agreement between the estimated and simulated target parameters in the selected scene.

However, the detector also identifies an additional candidate at approximately 11.99 m with nearly zero radial velocity. Its physical origin cannot be established from the available experiment. It may be associated with stationary clutter, an additional reflection, or a false detection. It is therefore retained as an unassociated candidate rather than definitively classified as a false positive.

It is also important to distinguish these estimation errors from general detection performance. The results are based on a single synthetic scene and do not establish a statistically evaluated probability of detection or false-alarm rate across different scenarios.

**Code Listing 4.1: Calculation of range and velocity errors from matched CFAR detections.**

The following small post-processing excerpt reproduces the error calculations from the four associated detections. It is an evaluation helper, not an additional radar-detection algorithm.

```plaintext
import numpy as np

# Ground truth and estimated values:
# [range_gt, velocity_gt, range_est, velocity_est]
matched_detections = np.array([
    [28.50, -14.20, 28.48, -13.99],
    [19.20,  -4.80, 19.19,  -4.87],
    [12.00,   8.50, 11.99,   8.52],
    [ 8.40,   1.40,  8.39,   1.52],
])

range_error = np.abs(
    matched_detections[:, 2] - matched_detections[:, 0]
)

velocity_error = np.abs(
    matched_detections[:, 3] - matched_detections[:, 1]
)

print("Range MAE:", range_error.mean(), "m")
print("Velocity MAE:", velocity_error.mean(), "m/s")

```

The reported results are 0.0125 m range MAE and 0.105 m/s velocity MAE.

**Figure 4.3: Two-dimensional CA-CFAR detection results.**

[AGENT INSTRUCTION — FIGURE 4.3]

Reuse `docs/assets/nb1/fig6_cfar_adaptive_detection.png`.

The figure must show the executed Range-Doppler detection output, including the detected candidate peaks and the adaptive detection threshold where available.

Caption: _Figure 4.3: Two-dimensional CA-CFAR detection over the simulated Range-Doppler power representation._

### 4.2.4 Direction-of-Arrival Estimation

The next experiment examines the spatial estimation of target direction using the four receiving antenna channels. The implemented estimator supports MUSIC, Capon/MVDR, and conventional spatial FFT beamforming.

These methods use the spatial information available across antenna elements to estimate the direction from which a radar return arrives. MUSIC exploits the signal and noise subspaces of the spatial covariance matrix [7], whereas Capon/MVDR employs an adaptive minimum-variance beamforming criterion [20].

The executed notebook reports the following angular spectrum peaks:

**Table 4.3: Angular estimates returned by the AoA experiment**

<table>
  <tr><th>Estimation method</th><th>Returned angle</th></tr>
  <tr><td>MUSIC</td><td>(+18.60^\circ)</td></tr>
  <tr><td>Capon/MVDR</td><td>(+18.60^\circ)</td></tr>
  <tr><td>Spatial FFT beamformer</td><td>(+18.21^\circ)</td></tr>
</table>

The notebook compares these values against a nominal ground-truth direction of (+18^\circ). However, the current implementation selects the CFAR candidate using range alone:

```plaintext
target_1_det = min(
    detections,
    key=lambda d: abs(d["range_m"] - 12.0)
)

```

There are two CFAR candidates at approximately 11.99 m: one with zero Doppler velocity and another with a velocity of +8.52 m/s. The range-only selection chooses the first matching candidate, which is the zero-velocity return.

Consequently, the receiving-channel samples used for the angular estimation are not reliably associated with the intended approaching car. Although the notebook reports a MUSIC difference of (0.60^\circ) from the nominal (+18^\circ) direction, this value cannot be treated as a validated target-angle estimation error.

The angular estimates in Table 4.3 are therefore retained as the numerical outputs of the executed routine, but their physical association remains unresolved.

A subsequent evaluation should associate a CFAR detection using both range and Doppler information before extracting the corresponding antenna snapshots. This would allow the MUSIC, Capon, and spatial FFT estimates to be compared against the correct simulated target azimuth.

The experiment nevertheless demonstrates the execution of the spatial estimation routines and provides a basis for improving the target-association procedure.

**Figure 4.4: MUSIC, Capon/MVDR and spatial FFT angular spectra.**

[AGENT INSTRUCTION — FIGURE 4.4]

Reuse `docs/assets/nb1/fig7_aoa_music_super_res.png`.

Preserve the three angular spectra and the original estimated peaks. The caption and surrounding discussion must explicitly identify the range-only CFAR association limitation.

Caption: _Figure 4.4: Angular spectra generated using MUSIC, Capon/MVDR and spatial FFT beamforming for the selected Range-Doppler detection._

### 4.2.5 Spatial Clustering and Micro-Doppler Visualisation

Following candidate detection and spatial estimation, the processing pipeline converts the polar target measurements into Cartesian coordinates:

[

x=R\sin\theta,\qquad y=R\cos\theta.

]

DBSCAN is then applied to group spatially related detections into object-level clusters. The implementation uses Cartesian position and a scaled velocity component as the clustering features. For each cluster, quantities such as its centroid, mean velocity, estimated azimuth, total detection power, and spatial bounds are computed.

The resulting bird's-eye-view representation illustrates the transformation from individual radar detections into a spatial description of the surrounding scene. The experiment provides a qualitative demonstration of the implemented clustering pipeline, rather than a statistically evaluated object-separation result [21].

A separate micro-Doppler visualisation is also generated for the simulated pedestrian target. The representation illustrates the periodic modulation of the pedestrian's return caused by its simulated oscillatory motion.

Such time-frequency signatures provide additional information about target motion that is not directly captured by a single range or Doppler estimate [18]. However, the current experiment does not establish a numerical pedestrian-recognition or micro-Doppler classification accuracy.

**Figure 4.5: Spatial clustering and pedestrian micro-Doppler representations.**

[AGENT INSTRUCTION — FIGURE 4.5]

Reuse the existing figures:

- `docs/assets/nb1/fig8_dbscan_clustering_bev.png`
- `docs/assets/nb1/fig9_pedestrian_micro_doppler.png`

Use two panels showing the Cartesian bird's-eye view and the simulated pedestrian time-frequency signature.

Caption: _Figure 4.5: DBSCAN-based spatial clustering of radar detections and the simulated pedestrian micro-Doppler signature._

### 4.2.6 Deep Learning-Based FMCW Target Detection

Alongside the conventional radar processing chain, a compact convolutional neural network was implemented and trained using synthetic Range-Doppler data.

The network, `RadarObjectDetectorCNN`, contains a shared convolutional feature extractor with residual blocks, followed by separate classification and coordinate-regression heads. The classification head generates class heatmaps, while the regression head predicts four coordinate-related outputs.

The executed notebook instantiates the model with 24 base filters. The resulting architecture contains:

[

\boxed{136,041\text{ trainable parameters}}.

]

Its forward pass produces five-channel classification heatmaps and four-channel coordinate-regression outputs.

The experiment uses a cached dataset of 32 synthetic radar samples. An 80:20 split produces 25 training samples and seven validation samples. Training is performed over five epochs using a batch size of six.

The training environment uses PyTorch 2.6.0 with CPU execution. The notebook configures the AdamW optimiser with a learning rate of (2\times10^{-3}), weight decay of (10^{-4}), and a cosine annealing learning-rate scheduler.

The model uses a composite classification and regression loss, as described in Chapter 3:

\mathcal{L}_{\mathrm{BCE}}_

_+_

_2\mathcal{L}_{\mathrm{SmoothL1}}.

]

The recorded training and validation losses are presented in Table 4.4.

**Table 4.4: Synthetic FMCW CNN training and validation losses**

<table>
  <tr><th>Epoch</th><th>Training loss</th><th>Validation loss</th></tr>
  <tr><td>1</td><td>0.7788</td><td>0.7526</td></tr>
  <tr><td>2</td><td>0.5842</td><td>0.6024</td></tr>
  <tr><td>3</td><td>0.5422</td><td>0.4933</td></tr>
  <tr><td>4</td><td>0.5032</td><td>0.5125</td></tr>
  <tr><td>5</td><td>0.4908</td><td>0.5195</td></tr>
</table>

Training was completed in 26.89 seconds.

The training loss decreases throughout the five epochs, indicating that the network successfully optimises its parameters on the generated training samples. The validation loss reaches its minimum of 0.4933 at epoch 3, before increasing slightly during the remaining epochs.

This behaviour suggests that further improvements in training loss do not necessarily correspond to equivalent improvements in validation performance. Given the limited dataset size, the experiment should be treated as an initial demonstration of the training pipeline rather than evidence of robust generalisation.

The notebook also evaluates the network on a validation sample and visualises its classification probability maps and coordinate predictions. This provides a qualitative illustration of the model's output representation. However, no independent test-set evaluation or quantitative detection metrics are recorded.

In particular, the experiment does not report mAP, precision, recall, class-wise accuracy, or bounding-box localisation error. Consequently, the current CNN results establish the feasibility of training a compact neural architecture on synthetic Range-Doppler data, but do not yet establish its detection effectiveness relative to the conventional DSP pipeline.

**Figure 4.6: Synthetic FMCW CNN training convergence and qualitative validation output.**

[AGENT INSTRUCTION — FIGURE 4.6]

Use:

- `docs/assets/nb2/plot2_training_convergence.png`
- `docs/assets/nb2/plot3_model_inference_unseen.png`

Combine the five-epoch loss curves and the model's validation-sample visualisation.

The second panel must be identified as a validation-sample inference result, not an independent test-set result.

Caption: _Figure 4.6: Training and validation loss progression and qualitative validation-sample inference for the synthetic FMCW radar CNN._

## 4.3 Experimental Track II: Wideband Radar Spectrum Detection

### 4.3.1 RadDet Dataset and Local Data Preparation

The second experimental track considers wideband radar spectrum detection using the RadDet dataset introduced by Huang et al. [2].

Unlike the synthetic FMCW automotive experiments, RadDet represents radar emissions as two-dimensional time-frequency spectrograms. The task involves detecting radar emissions and identifying their corresponding modulation categories.

The S-128 representation uses a (128\times128) spectrogram over a 500 MHz frequency bandwidth and a 2 ms observation interval.

The eleven modulation categories considered are:

[

\begin{aligned}

\mathcal{C}={&

\mathrm{Rect},\mathrm{Barker},\mathrm{Frank},

\mathrm{P1},\mathrm{P2},\mathrm{P3},\

&\mathrm{P4},\mathrm{Px},\mathrm{ZadoffChu},

\mathrm{LFM},\mathrm{FMCW}}.

\end{aligned}

]

The repository includes a local RadDet sample dataset containing 40 training images, 15 validation images and five test images. This 60-image micro-slice provides a small environment for testing dataset ingestion, annotation parsing, and visualisation.

The dataset preparation module reads grayscale spectrograms and their corresponding YOLO-format annotations. Each annotation represents a modulation category and a normalised bounding box describing the temporal and frequency extent of the corresponding emission.

The local sample dataset demonstrates that the data-loading and annotation-processing components are available. However, the micro-slice is not a substitute for the full RadDet dataset required for a meaningful benchmark reproduction.

The representative spectrogram input and annotation workflow are already illustrated in Figure 3.4. They are therefore not duplicated in this chapter.

### 4.3.2 Saved YOLOv8n Training Experiment

The repository contains a saved preliminary RadDet training run under `data/kaggle_outputs/runs/raddet_yolo/`.

The associated training arguments identify the model as YOLOv8n, trained for 15 epochs using an input resolution of (128\times128) and batch size 16.

This is a separate preliminary experiment and must not be confused with the intended full-scale YOLOv9-C experiment.

The saved `results.csv` contains 15 training epochs. Across the recorded epochs, precision, recall, mAP@50 and mAP@50:95 remain zero.

**Table 4.5: Configuration and recorded validation metrics of the saved YOLOv8n run**

<table>
  <tr><th>Parameter</th><th>Recorded value</th></tr>
  <tr><td>Model</td><td>YOLOv8n</td></tr>
  <tr><td>Training epochs</td><td>15</td></tr>
  <tr><td>Input resolution</td><td>(128\times128)</td></tr>
  <tr><td>Batch size</td><td>16</td></tr>
  <tr><td>Validation enabled</td><td>Yes</td></tr>
  <tr><td>Precision</td><td>0.00</td></tr>
  <tr><td>Recall</td><td>0.00</td></tr>
  <tr><td>mAP@50</td><td>0.00</td></tr>
  <tr><td>mAP@50:95</td><td>0.00</td></tr>
</table>

The training log records reductions in the training box, classification and distribution-focal losses over the run. However, these reductions are not accompanied by non-zero validation detection metrics.

Therefore, the saved experiment does not establish successful radar emission detection. It demonstrates the existence of a preliminary YOLOv8n training artifact, but further investigation is required to understand the zero validation performance.

Potential factors that should be checked during a subsequent run include dataset configuration, class-index consistency, annotation interpretation, model prediction behaviour and validation preprocessing. These are possible investigation points, not established causes of the recorded result.

### 4.3.3 Intended YOLOv9-C Full-Scale Benchmark

The full-scale RadDet benchmark is designed around YOLOv9-C, using pretrained `yolov9c.pt` weights and a maximum training duration of 100 epochs. The configured training procedure includes the AdamW optimiser, automatic mixed precision, early stopping and radar-oriented data augmentation.

The intended evaluation includes six SNR levels:

[

\mathcal{S}=

{-20,-12,-4,+4,+12,+20}\text{ dB}.

]

The purpose of this experiment is to evaluate detection performance under different signal-quality conditions and compare the resulting model against the published RadDet benchmark [2].

However, inspection of the latest committed notebook reveals that several evaluation components do not use actual trained-model predictions.

The limitations are as follows:

1. The validation convergence plot is generated using synthetic loss and mAP curves rather than values obtained from the trained detector.
2. The multi-SNR evaluation adds random perturbations to reference values from the published paper instead of running model validation on each SNR-specific test subset.
3. The latency routine measures a dummy tensor multiplication rather than a YOLOv9-C forward pass. It also substitutes fixed latency values when the measured operation is below a threshold.
4. The qualitative multi-SNR detection grid uses artificially generated spectrograms and manually constructed bounding boxes.
5. The unseen-frame visualisation perturbs ground-truth annotations rather than obtaining predictions from the trained detector.

Furthermore, the full-scale notebook does not contain saved execution outputs demonstrating completed YOLOv9-C training and evaluation. Its exception-handling logic also permits simulated progress reporting when training encounters an error.

The benchmark summary files contain reported YOLOv9-C performance values, including a full-scale detection score and inference throughput. However, the notebook routines used to generate the corresponding figures and metrics do not independently measure those quantities.

Consequently, these reported values cannot be treated as verified results of the present investigation.

The distinction between the saved YOLOv8n preliminary experiment, the intended YOLOv9-C benchmark and the published YOLOv9-M reference is maintained in Table 4.6.

**Table 4.6: Evidence status of the RadDet detection experiments**

<table>
  <tr><th>Experiment</th><th>Model</th><th>Evidence available</th><th>Status</th></tr>
  <tr><td>Local preliminary training</td><td>YOLOv8n</td><td>Saved configuration, training CSV and model checkpoints</td><td>Executed run; zero recorded validation metrics</td></tr>
  <tr><td>Full-scale benchmark configuration</td><td>YOLOv9-C</td><td>Training and evaluation code</td><td>Configured, but completed execution not independently verified</td></tr>
  <tr><td>Full-scale performance report</td><td>YOLOv9-C</td><td>Exported Markdown and CSV claims</td><td>Not accepted as verified experimental measurements</td></tr>
  <tr><td>Published RadDet benchmark</td><td>YOLOv9-M</td><td>Published results in [2]</td><td>External reference</td></tr>
</table>

There is also an inconsistency between the sample-count information in the full-scale benchmark report and the different dataset partitions described in the associated experiment materials. In the absence of a consistent dataset manifest and execution log, the exact sample distribution used by the reported full-scale run cannot be established reliably.

The RadDet track therefore establishes the dataset-processing framework and a preliminary saved YOLOv8n training experiment. A genuine full-scale YOLOv9-C reproduction remains an outstanding experimental requirement.

## 4.4 Computational Performance and Resource Analysis

An important objective of this project is to investigate the relationship between AI-based radar detection performance and the computational resources required for execution.

The present experiments provide some initial measurements of model complexity and training behaviour. However, they do not yet provide a complete comparison of inference efficiency across CPU and GPU hardware.

It is therefore necessary to distinguish measured computational quantities from measurements that remain outstanding.

### 4.4.1 Synthetic CNN Model Complexity

The synthetic FMCW CNN contains 136,041 trainable parameters. Its five-epoch training experiment was completed in 26.89 seconds using CPU-based PyTorch execution.

These measurements demonstrate that the implemented CNN can be trained in the available CPU environment using a relatively small synthetic dataset.

However, training duration and inference latency are different quantities. The recorded 26.89 seconds describe the execution of the complete five-epoch training procedure. They do not represent the time required to process an individual radar frame.

The experiment also does not record FLOPs, MACs, peak memory consumption or energy usage. Consequently, the parameter count alone is insufficient to establish the model's suitability for a particular deployment platform.

### 4.4.2 Classical Signal-Processing Requirements

The classical FMCW processing pipeline involves a sequence of FFT operations, MTI filtering, CFAR detection, spatial angle estimation and clustering.

Although the pipeline has been executed successfully on the synthetic scene, its individual processing stages have not been systematically profiled for execution time or memory consumption.

A complete computational comparison would require separate measurements for range processing, Doppler processing, CFAR, angle estimation and DBSCAN clustering, followed by an end-to-end measurement of the complete pipeline.

The existing clutter-attenuation result of 12.94 dB is a signal-processing performance measurement. It should not be interpreted as a measure of computational efficiency.

### 4.4.3 Published RadDet Reference and Local Performance Status

The original RadDet paper reports a YOLOv9-M benchmark result for the S-128 configuration [2].

The published values include approximately 20.02 million model parameters, 25.93% mAP@50, 19.47% mAP@50:95 and 896.6 FPS.

These values provide an external reference for the wideband radar spectrum-detection task. They are not measurements obtained by the local YOLOv9-C experiment.

The available local training and evaluation artifacts do not establish a corresponding validated YOLOv9-C inference result. Therefore, a direct local comparison of detection accuracy and execution time cannot currently be made.

### 4.4.4 Summary of Available Computational Measurements

The current measurements and outstanding evaluation requirements are summarised in Table 4.7.

**Table 4.7: Summary of measured computational quantities and outstanding evaluations**

<table>
  <tr><th>Quantity</th><th>Available result</th><th>Evidence status</th></tr>
  <tr><td>Synthetic CNN parameters</td><td>136,041</td><td>Measured</td></tr>
  <tr><td>Synthetic CNN training duration</td><td>26.89 seconds for five epochs</td><td>Measured</td></tr>
  <tr><td>CNN training environment</td><td>CPU, PyTorch 2.6.0+cpu</td><td>Recorded</td></tr>
  <tr><td>CNN inference latency</td><td>Not available</td><td>Not measured</td></tr>
  <tr><td>Classical DSP stage-wise latency</td><td>Not available</td><td>Not measured</td></tr>
  <tr><td>Classical DSP memory consumption</td><td>Not available</td><td>Not measured</td></tr>
  <tr><td>YOLOv8n training duration and losses</td><td>15-epoch saved run</td><td>Recorded</td></tr>
  <tr><td>YOLOv8n validation mAP</td><td>Zero across recorded epochs</td><td>Recorded</td></tr>
  <tr><td>YOLOv9-C GPU inference latency</td><td>Not independently verified</td><td>Unavailable</td></tr>
  <tr><td>YOLOv9-C FLOPs and peak memory</td><td>Not independently verified</td><td>Unavailable</td></tr>
  <tr><td>CPU-versus-GPU inference comparison</td><td>Not available</td><td>Not evaluated</td></tr>
  <tr><td>Quantisation and pruning performance</td><td>Not available</td><td>Not evaluated</td></tr>
</table>

These findings indicate that the present investigation has established an initial computational baseline, but has not yet characterised the complete detection-performance versus resource-consumption trade-off.

### 4.4.5 Implications for Resource-Efficient AI

The current project direction preserves two complementary possibilities for improving the practical efficiency of AI-based radar detection.

**Approach A: Reduction of Overall Computational Requirements.**

The first possibility is to reduce the amount of computation and memory required by radar detection models while retaining acceptable detection performance.

Potential techniques include lightweight neural architectures, pruning, quantisation, knowledge distillation and adaptive computation. These methods aim to reduce model complexity, inference operations or the amount of computation performed for individual inputs.

Their suitability will depend on the detection task, model architecture and hardware environment. Any improvement must be established through quantitative experiments rather than assumed from model size alone.

**Approach B: CPU-Oriented Model Development and Inference.**

The second possibility is to investigate whether radar detection models can be developed or adapted for efficient execution on commodity CPUs.

This direction examines architectural choices, numerical representations, and inference implementations that may reduce dependence on dedicated GPU hardware. CPU performance must be measured directly rather than inferred from the fact that a model was trained in a CPU environment.

The two approaches are related but not mutually exclusive. A computationally reduced architecture may also improve CPU execution, while a CPU-oriented model may benefit from pruning, quantisation or other optimisation techniques.

The subsequent experimental comparison will therefore consider both possibilities without selecting either as the final solution at this stage.

## 4.5 Discussion and Limitations

### 4.5.1 Interpretation of the Synthetic FMCW Results

The synthetic FMCW experiments demonstrate the successful execution of a multi-stage radar signal-processing pipeline.

The simulator generated the expected four-channel complex radar cube, and the subsequent processing stages produced range and Doppler representations suitable for target detection. MTI filtering achieved 12.94 dB clutter attenuation under the selected conditions.

The CA-CFAR detector identified five candidate peaks. Four could be associated with the simulated objects through their range and velocity estimates. Their mean absolute range error was 0.0125 m, while their mean absolute velocity error was 0.105 m/s.

These results demonstrate that the implemented range, Doppler and detection stages can recover target-related information from the controlled synthetic scene. However, the additional zero-Doppler candidate and the limited scene diversity highlight the need for more comprehensive evaluation.

The AoA experiment also demonstrates the execution of multiple spatial estimation routines. Nevertheless, the range-only target-selection procedure prevents the returned angular estimates from being confidently associated with the intended moving car. Correct target association must therefore be established before drawing conclusions about angular estimation accuracy.

### 4.5.2 Interpretation of the Synthetic CNN Results

The synthetic CNN experiment demonstrates the implementation and training of a compact, multi-task radar detection architecture.

Its 136,041 trainable parameters and five-epoch training run provide an initial reference for further investigation of model complexity. The observed reduction in training loss indicates that the network learns from the generated training data.

However, the small dataset and the increase in validation loss after epoch 3 indicate that additional experiments are required to assess generalisation.

The absence of quantitative detection metrics also prevents a meaningful comparison between the CNN and the classical CA-CFAR pipeline. A common evaluation dataset and object-level metrics would be necessary for such a comparison.

### 4.5.3 Interpretation of the RadDet Results

The RadDet investigation provides a complementary setting for studying AI-based radar spectrum detection. Its wideband spectrogram representation and modulation-specific annotations enable the formulation of a multi-class object-detection task.

The present implementation establishes the data-processing framework and contains a preliminary saved YOLOv8n training run. However, the saved validation metrics remain zero, and the intended full-scale YOLOv9-C benchmark cannot be independently verified from the committed execution artifacts.

The reported full-scale benchmark values are therefore not used as empirical findings. In particular, the current evidence does not establish that the local implementation reproduces the YOLOv9-M results published in [2].

A completed YOLOv9-C experiment with genuine predictions on held-out test data remains necessary before a local benchmark comparison can be presented.

### 4.5.4 Overall Limitations

The experiments reveal several limitations that define the current scope of the investigation.

1. **Limited synthetic scene coverage:** The classical FMCW evaluation uses a controlled four-target scene. Its results do not establish general performance across diverse traffic conditions, clutter distributions, or target configurations.
2. **Target-association limitation in AoA evaluation:** The current range-only selection procedure does not distinguish between the two CFAR candidates located at approximately 12 m. The reported angular estimates therefore require a corrected target-association procedure and rerun before they can be used as validated accuracy measurements.
3. **Limited CNN training dataset:** The synthetic CNN is trained using only 32 samples for five epochs. Independent test-set evaluation and repeated experiments are necessary to establish its generalisation behaviour.
4. **Incomplete RadDet benchmark verification:** The local saved YOLOv8n run records zero validation detection metrics, while the full-scale YOLOv9-C result is not independently verifiable from the committed execution artifacts.
5. **Absence of a complete computational profile:** The present work does not establish model inference latency, FLOPs, memory consumption or energy usage across standardised hardware configurations.
6. **No systematic CPU-versus-GPU comparison:** CPU execution of the synthetic CNN training experiment does not establish efficient CPU inference. A separate controlled hardware evaluation is required.
7. **No completed resource-optimisation experiment:** Pruning, quantisation, knowledge distillation, lightweight architecture comparisons and adaptive computation remain candidate investigations rather than demonstrated improvements.

These limitations are important when interpreting the results. The current work establishes an experimental foundation and identifies the measurements required for a more rigorous evaluation.

### 4.5.5 Implications for the Subsequent Project Phase

The results provide the initial technical foundation for investigating resource-efficient AI-based radar signal processing and detection.

Two complementary research directions remain open. The first concerns reducing overall computational requirements through model-level optimisation and more efficient computation. The second concerns CPU-oriented model development and inference to reduce dependence on dedicated GPU resources.

The subsequent experimental investigation should compare these approaches using consistent datasets, documented hardware configurations and repeatable evaluation procedures.

Detection performance should be measured alongside model parameters, FLOPs or MACs, memory requirements, inference latency and throughput. CPU and GPU measurements should be conducted independently, with preprocessing, neural inference and post-processing costs clearly distinguished.

For the RadDet track, a genuine trained-model evaluation across the configured SNR conditions is required. For the synthetic FMCW track, further experiments should include additional target configurations, corrected AoA association, and an independent evaluation of the CNN's detection quality.

The findings of these experiments will determine whether model-level computational reduction, CPU-oriented inference, or a combination of both provides the most practical direction for the subsequent implementation.

The selection of a final approach is therefore deferred until comparative experimental evidence is available.

---

**Chapter Summary**

The present experiments establish two complementary foundations for AI applications in radar signal processing. The synthetic FMCW track demonstrates the operation of a conventional radar processing pipeline and initial training of a compact CNN. The RadDet track establishes a wideband spectrum-detection framework and identifies the requirements for completing a reproducible full-scale benchmark.

The experimental evidence highlights the importance of evaluating detection quality together with computational requirements. It also establishes the need for further quantitative comparisons between computationally reduced models and CPU-oriented inference implementations.
