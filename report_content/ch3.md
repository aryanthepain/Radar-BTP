# Instructions

you might need to write the formulae properly.

1. First inspect the existing notebooks and exported images. Reuse an existing figure if it accurately represents the described methodology.
2. If no suitable figure exists, create a Mermaid diagram and export it as an image suitable for inclusion in the report.
3. Do not use externally sourced generic radar illustrations when an implementation-specific diagram is required.
4. Do not fabricate spectrograms, detection outputs, network layers, or experimental results.
5. Maintain consistent typography, node shapes, arrow conventions, and visual style across all methodology diagrams.
6. Use vector output such as SVG where supported. Ensure the figures remain readable when printed on an A4 report page.
7. Every figure must have a numbered caption and be explicitly referenced in the corresponding paragraph, for example, "The overall methodology is illustrated in Figure 3.1."
8. Keep figure files in the report's designated figures directory and use descriptive filenames:
   - `fig3_1_overall_methodology.svg`
   - `fig3_2_fmcw_processing_pipeline.svg`
   - `fig3_3_fmcw_cnn_architecture.svg`
   - `fig3_4_raddet_spectrogram.png`
9. Do not duplicate an existing figure merely to satisfy the numbering. Reuse or adapt it when appropriate.
10. Verify all image paths, captions, references, and figure-list entries after compilation.

# Chapter 3: Methodology

## 3.1 Overall Methodological Framework

The methodology adopted in this study combines conventional radar signal processing, deep learning-based detection, and computational performance evaluation. The investigation is organised around two complementary experimental tracks.

The first track focuses on **synthetic 77 GHz FMCW automotive radar perception**. A radar simulation framework is used to generate complex baseband radar measurements from controlled target scenes. These measurements are processed using conventional digital signal processing techniques to obtain range, velocity, and angular information. A learning-based detector is also developed to perform target classification and coordinate regression on generated Range-Doppler representations.

The second track focuses on **wideband radar spectrum detection using the RadDet dataset**. This task treats radar signal detection as an object detection problem over time-frequency spectrograms. A YOLO-based detector is trained and evaluated to localise radar emissions and identify their modulation categories.

Although both tracks involve radar data and learning-based detection, they address different problems. The FMCW track considers the perception of spatial targets from simulated automotive radar measurements, whereas the RadDet track considers the detection and classification of radar emissions in a wideband spectrum. Their data representations, model outputs, and evaluation metrics are therefore treated separately.

The two tracks provide a foundation for investigating the broader question of resource-efficient AI for radar signal processing and detection. The computational evaluation considers both algorithm-level efficiency and hardware-oriented inference. Techniques such as lightweight architectures, quantisation, knowledge distillation, and adaptive computation are treated as candidate approaches for further investigation rather than completed contributions.

## 3.2 Experimental Track I: Synthetic FMCW Radar Perception

### 3.2.1 Radar Simulation and Data Generation

The first experimental track uses a software-based FMCW radar simulator to generate complex baseband measurements. This enables controlled experiments in which target positions, velocities, reflection strengths, and signal-to-noise ratios can be varied.

The default radar configuration represents a 77 GHz millimetre-wave radar system. Its principal simulation parameters are:

<table>
  <tr><th>Parameter</th><th>Value</th></tr>
  <tr><td>Carrier frequency</td><td>77 GHz</td></tr>
  <tr><td>Chirp bandwidth</td><td>1 GHz</td></tr>
  <tr><td>Chirp duration</td><td>50 μs</td></tr>
  <tr><td>Fast-time ADC samples per chirp</td><td>256</td></tr>
  <tr><td>Number of chirps per frame</td><td>128</td></tr>
  <tr><td>Number of receive antennas</td><td>4</td></tr>
  <tr><td>Receiver antenna spacing</td><td>Half-wavelength</td></tr>
  <tr><td>ADC sampling frequency</td><td>5.12 MHz</td></tr>
</table>

The simulated radar produces a complex-valued data cube of dimensions

$$
\mathbf{X}\in\mathbb{C}^{N_{\mathrm{rx}}\times
N*{\mathrm{chirp}}\times N*{\mathrm{sample}}}
$$

where the three dimensions correspond to receive antennas, slow-time chirps, and fast-time ADC samples, respectively. With the default configuration, the generated data cube has dimensions ($4\times128\times256$).

A target scene is represented by a collection of objects with attributes such as range, radial velocity, azimuth, radar cross-section, and target category. The scene generator produces between one and three targets, selected from four categories: car, pedestrian, cyclist, and drone. Pedestrian and drone targets can additionally include micro-Doppler modulation to represent periodic motion.

For every target, the received complex signal is constructed using contributions from its beat frequency, Doppler phase, spatial phase across the receiving antennas, and carrier-related phase. The signals from individual targets are superimposed to form the simulated radar cube.

Environmental effects are introduced through stationary clutter and additive complex Gaussian noise. The implemented simulator generates stationary clutter reflectors with Rayleigh-distributed amplitudes and adds complex additive white Gaussian noise at a configurable SNR. In the synthetic dataset generator, the SNR is sampled between 10 dB and 25 dB, and the clutter-to-noise ratio is configured as 8 dB.

This simulation-based approach provides labelled examples in which the underlying target locations and properties are known. It is therefore suitable for controlled evaluation of signal processing operations and the construction of learning-based detection targets.

### 3.2.2 Conventional Radar Signal Processing Pipeline

The simulated radar cube is processed using a sequence of conventional signal processing operations. The main stages are range processing, clutter suppression, Doppler processing, target detection, angle estimation, and spatial clustering. The processing structure follows established FMCW radar signal processing principles [4], [5].

**a) Range Processing**

Range processing is performed along the fast-time dimension of the radar cube. A Hann window is applied to reduce spectral leakage, followed by a one-dimensional Fast Fourier Transform (FFT):

$$

X_r(r,m,n)=

\mathrm{FFT}\_{n}\left{

w_r(n)X(r,m,n)

\right}


$$

where (w_r(n)) is the range window and the FFT is applied over ADC samples.

The resulting range profile provides frequency-domain information associated with target distances. The range axis is obtained from the beat-frequency relationship and the configured chirp slope.

**b) Clutter Suppression**

Stationary reflections from the surrounding environment can produce strong components near zero Doppler. A clutter suppression stage is therefore applied along the slow-time dimension.

The default synthetic dataset pipeline uses mean subtraction:

## X_r(r,m,n)

\frac{1}{N_c}

\sum\_{m=0}^{N_c-1} X_r(r,m,n),

]

where (N_c) denotes the number of chirps.

The implementation also provides alternative clutter suppression methods, including two-pulse MTI, three-pulse MTI, and high-pass filtering. These methods offer different ways of suppressing slowly varying or stationary components while retaining the returns associated with moving targets.

**c) Doppler Processing**

Doppler processing is performed over the slow-time chirp dimension. After applying a Hann window, an FFT is computed along the chirp axis:

\mathrm{FFT}\_{m}

\left{

w_d(m)\widetilde{X}\_r(r,m,n)

\right}.

]

The zero-Doppler component is shifted to the centre of the spectrum using an FFT shift operation. The resulting Range-Doppler representation maps target energy according to range and radial velocity.

The magnitude or power of the Range-Doppler representation can then be expressed in decibels for visualisation and subsequent detection.

**d) CFAR-Based Target Detection**

The processed Range-Doppler representation is supplied to a Constant False Alarm Rate (CFAR) detector. CFAR estimates the local background level around a Cell Under Test (CUT) and derives an adaptive detection threshold.

The implemented detector supports multiple CFAR variants:

- Cell-Averaging CFAR (CA-CFAR).
- Ordered-Statistic CFAR (OS-CFAR).
- Greatest-Of CFAR (GOCA-CFAR).
- Smallest-Of CFAR (SOCA-CFAR).

The detector identifies candidate target peaks whose signal levels exceed the estimated threshold. These detections provide range and Doppler-bin information for subsequent processing [6].

**e) Direction-of-Arrival Estimation**

Spatial angle estimation uses the phase information available across the multiple receiving antennas. The implemented module supports subspace-based MUSIC and Capon minimum-variance distortionless-response estimation.

These techniques use the spatial structure of the received signals to estimate the direction of arrival of detected targets. MUSIC estimates angular peaks using the signal and noise subspaces obtained from the spatial covariance matrix, while Capon estimates the spatial spectrum using an adaptive beamforming formulation [7], [20].

**f) Spatial Clustering**

The candidate detections are converted from polar coordinates into Cartesian coordinates:

[

x=R\sin\theta,\qquad

y=R\cos\theta,

]

where (R) denotes range and (\theta) denotes azimuth.

DBSCAN clustering is then applied to group spatially related detections. The implementation constructs clustering features using Cartesian position and a scaled velocity component. For each resulting cluster, the processing pipeline computes quantities such as the centroid, mean velocity, azimuth, total detection power, and spatial bounds.

This produces an object-level representation from the lower-level CFAR detections [21].

### 3.2.3 Deep Learning-Based FMCW Target Detection

Alongside the conventional processing pipeline, a convolutional neural network is implemented for learning-based target detection from synthetic Range-Doppler representations.

The synthetic dataset generator constructs radar scenes and processes them through the range FFT, mean-subtraction clutter filter, and Doppler FFT stages. The power across receiving antennas is averaged to obtain a two-dimensional Range-Doppler representation. The resulting power map is converted to a decibel scale and normalised to the range ([0,1]).

Each generated sample is paired with two types of supervision:

1. **Class heatmaps:** A multi-channel target map representing the background and the four target categories.
2. **Bounding-box regression targets:** Normalised range and velocity coordinates, together with target extent information.

For each simulated target, the nearest range and Doppler bins are identified. A local Gaussian response is placed around the target location in the corresponding class heatmap. The associated regression channels encode the normalised range centre, velocity centre, and target widths.

The implemented `RadarObjectDetectorCNN` uses a fully convolutional architecture with an initial feature extraction layer, residual convolutional blocks, a feature expansion stage, and two prediction heads. The classification head generates class heatmaps, while the regression head predicts four coordinate-related values for each spatial location.

The model uses a multi-task objective combining classification and bounding-box regression:

\mathcal{L}_{\mathrm{cls}}_

_+_

_2\mathcal{L}_{\mathrm{box}},

]

where the classification term is binary cross-entropy with logits and the regression term is a masked Smooth L1 loss. The mask restricts coordinate regression to locations associated with foreground targets.

The training utility uses an 80:20 training-validation split. Its default configuration uses 150 generated samples, a batch size of 8, five training epochs, and the AdamW optimiser with a learning rate of (10^{-3}) and weight decay of (10^{-4}). A cosine annealing learning-rate scheduler is used during training.

This CNN provides a learning-based approach to target localisation and classification on the synthetic FMCW data. Its results are interpreted within the synthetic experimental setting and are not treated as equivalent to results obtained on the separate RadDet spectrum-detection task.

## 3.3 Experimental Track II: Wideband Radar Spectrum Detection

### 3.3.1 Dataset and Input Representation

The second experimental track uses the RadDet wideband radar spectrum detection dataset introduced in [2]. Unlike the synthetic FMCW perception track, this dataset is concerned with the detection and classification of radar emissions in a wideband frequency spectrum.

The input representation consists of two-dimensional max-hold time-frequency spectrograms. The spectrogram represents radar activity over a time horizon of approximately 2 ms and a frequency bandwidth of 500 MHz.

The two axes have the following interpretation:

- The horizontal axis represents time dwell, indicating the duration and temporal position of a signal emission.
- The vertical axis represents frequency, indicating the location and bandwidth occupied by the emission.

The dataset contains eleven radar modulation categories:

[

\begin{aligned}

\mathcal{C}={&

\mathrm{Rect},\mathrm{Barker},\mathrm{Frank},\mathrm{P1},

\mathrm{P2},\mathrm{P3},\

&\mathrm{P4},\mathrm{Px},\mathrm{ZadoffChu},

\mathrm{LFM},\mathrm{FMCW}}.

\end{aligned}

]

The full-scale benchmark uses the S-128 input resolution, corresponding to a (128\times128) spectrogram. This resolution provides the lower-resolution setting for the initial detector benchmark.

The dataset is organised into training, validation, and test splits. The full-scale benchmark record contains approximately 40,000 frames distributed across these splits.

### 3.3.2 Annotation Processing and Dataset Preparation

Each spectrogram is associated with object-level annotations in the YOLO bounding-box format:

[

(c,x_c,y_c,w,h),

]

where (c) denotes the modulation class, (x_c) and (y_c) represent the normalised box centre, and (w) and (h) represent the normalised box width and height.

The dataset preparation stage organises images and annotations into separate training, validation, and test directories. The corresponding dataset configuration file specifies the paths to these splits and the mapping between class indices and modulation categories.

The RadDet data loader reads the spectrogram images, converts them to grayscale, and normalises the pixel intensities to the interval ([0,1]). It also parses the annotation files and returns bounding boxes and class labels in tensor form.

The resulting data can be supplied to an object detection model to jointly localise radar emissions in the time-frequency representation and classify their modulation types.

### 3.3.3 YOLO-Based Detection Architecture and Training

The wideband spectrum detection task is implemented using the Ultralytics YOLO framework. The full-scale benchmark uses a YOLOv9-C detector initialised from pretrained `yolov9c.pt` weights. The architecture uses the GELAN-C backbone and detection components to predict bounding boxes, object confidence, and modulation classes.

The primary full-scale experiment is configured for the S-128 input resolution. The training schedule allows up to 100 epochs, with early stopping configured using a patience value of 20 epochs. Periodic model checkpoints are saved during training.

The training configuration uses the AdamW optimiser with the following settings:

<table>
  <tr><th>Training parameter</th><th>Configuration</th></tr>
  <tr><td>Initial learning rate</td><td>0.01</td></tr>
  <tr><td>Final learning-rate factor</td><td>0.001</td></tr>
  <tr><td>Weight decay</td><td>0.0005</td></tr>
  <tr><td>Warm-up epochs</td><td>3</td></tr>
  <tr><td>Maximum epochs</td><td>100</td></tr>
  <tr><td>Early-stopping patience</td><td>20</td></tr>
  <tr><td>Input resolution</td><td>(128\times128)</td></tr>
</table>

Data augmentation is used to improve training diversity. The configured transformations include Mosaic, Mixup, Copy-Paste, Random Erasing, translation, and scaling. HSV-based colour augmentation and horizontal and vertical image flips are disabled to avoid introducing transformations that may not preserve the intended radar representation.

Before full-scale training, candidate GPU batch sizes are tested to estimate throughput and memory usage. This pre-flight procedure helps select a batch size compatible with the available GPU memory.

The training process uses the training split for parameter optimisation and the validation split for monitoring model performance and training progression. The held-out test split is used for the final benchmark evaluation.

It is important to distinguish the implemented YOLOv9-C detector from the YOLOv9-M model reported in the original RadDet benchmark. The former is the model used in the present full-scale training run, while the latter is retained as a published reference baseline for comparison. The two configurations are therefore not identical model variants.

### 3.3.4 Multi-SNR Evaluation and Performance Measurement

Radar spectrum detection performance is evaluated using object detection metrics. The principal accuracy measures are:

- **Precision:** The fraction of predicted detections that correspond to valid ground-truth detections.
- **Recall:** The fraction of ground-truth objects successfully detected by the model.
- **mAP(\_{50}):** Mean Average Precision computed at an Intersection over Union threshold of 0.50.
- **mAP(\_{50:95}):** Mean Average Precision averaged over multiple IoU thresholds from 0.50 to 0.95.

To examine the effect of signal quality, the evaluation procedure considers six SNR levels:

[

\mathrm{SNR}\in

{-20,-12,-4,+4,+12,+20}\ \mathrm{dB}.

]

The detection metrics are computed separately across these SNR conditions, allowing the change in detection performance to be studied as signal quality varies. Aggregate metrics are also calculated over the evaluated test frames.

Inference latency is measured separately from training performance. The benchmark uses batch-size-one inference to represent single-frame processing. After warm-up iterations, CUDA events are used to measure repeated inference executions, with device synchronisation applied to ensure that the recorded time reflects completed GPU operations.

Mean, median, and high-percentile latency are considered when characterising inference behaviour. Average throughput is derived from mean latency:

\frac{1000}{\mathrm{Latency}\_{\mathrm{mean}}(\mathrm{ms})}.

]

The benchmark also records model complexity measures such as parameter count and floating-point operations (FLOPs), enabling detection performance to be considered alongside computational cost.

## 3.4 Methodology for Resource-Efficiency Investigation

The two experimental tracks provide different settings in which computational efficiency can be studied. The resource-efficiency investigation is therefore designed to examine both the cost of the model and the hardware on which inference is executed.

Two complementary dimensions are considered:

1. **Algorithm-level efficiency:** Reducing the computation or model capacity required to perform a radar detection task while retaining acceptable detection performance.
2. **Hardware-oriented efficiency:** Understanding how the same model or alternative model architectures behave when executed on different processing platforms, particularly CPUs and GPUs.

### 3.4.1 Candidate Algorithm-Level Approaches

The following methods are considered as candidate approaches for further investigation:

- **Lightweight architectures:** Investigate smaller convolutional backbones and reduced channel configurations to decrease model parameters, operations, and memory requirements.
- **Pruning and quantisation:** Explore the removal of redundant model weights and the use of lower-precision numerical representations to reduce model size and inference cost.
- **Knowledge distillation:** Investigate whether a compact student model can learn useful representations from a higher-capacity teacher model, potentially reducing inference complexity.
- **Adaptive multi-resolution processing:** Explore a cascaded approach in which a lower-resolution detector processes routine inputs, while more computationally expensive processing is used for uncertain or complex cases.
- **Conditional computation and early exit:** Investigate whether inference can terminate at an intermediate network stage when the model has already produced a sufficiently confident prediction.
- **Alternative learning strategies:** Self-supervised representation learning and policy-based computation allocation may also be considered as exploratory extensions, depending on the outcomes and available computational resources.

These methods are not assumed to provide improvements in advance. Their suitability must be established experimentally for the selected radar task.

### 3.4.2 CPU and GPU Inference Comparison

A hardware-oriented evaluation is intended to examine whether radar detection models can execute effectively without relying exclusively on dedicated GPUs.

The comparison should use identical model weights and input samples wherever possible. Batch size, input resolution, numerical precision, preprocessing, and post-processing must also be recorded so that hardware comparisons are meaningful.

The proposed procedure consists of:

1. Establishing a native CPU inference baseline.
2. Measuring GPU inference for the same model and inputs.
3. Recording mean, median, and tail latency, together with throughput and memory consumption.
4. Investigating CPU optimisation approaches such as post-training quantisation and optimised inference runtimes.
5. Comparing the resulting accuracy, latency, and memory trade-offs.

Potential CPU execution routes include native PyTorch, ONNX Runtime, and OpenVINO. Quantised inference may also be investigated, with detection performance compared against the corresponding full-precision baseline.

At this stage, CPU-oriented deployment is treated as a proposed evaluation direction. The existing GPU benchmark does not establish CPU performance, and no CPU latency or memory improvement is assumed.

### 3.4.3 Computational Objective and Evaluation Criteria

The broader resource-efficiency problem can be formulated as a constrained optimisation objective. Let (f\_\theta) represent a detector parameterised by (\theta), and let (\pi) represent a possible computation-allocation or inference policy.

A candidate formulation is:

[

\min\_{\theta,\pi}

\mathbb{E}\_{x\sim\mathcal{D}}

\left[C(x,\pi(x))\right]

]

subject to

[

\mathrm{mAP}(f\_\theta,\pi)

\geq

\mathrm{mAP}\_{\mathrm{baseline}}-\epsilon,

]

and

[

\mathrm{Latency}_{P95}(f_\theta,\pi)

\leq \tau\_{\max},

]

where:

- (C(x,\pi(x))) represents the computational cost associated with processing input (x).
- (\mathcal{D}) denotes the evaluation data distribution.
- (\epsilon) specifies the acceptable loss in detection performance relative to a baseline.
- (\mathrm{Latency}\_{P95}) denotes the 95th-percentile inference latency.
- (\tau\_{\max}) represents the application-specific latency constraint.

The formulation captures the central trade-off between detection quality and computational requirements. It also allows static model compression and input-dependent computation allocation to be considered within a common framework.

The evaluation is intended to report the following dimensions:

<table>
  <tr><th>Evaluation dimension</th><th>Measures</th></tr>
  <tr><td>Detection performance</td><td>Precision, recall, mAP({50}), mAP({50:95}), where applicable</td></tr>
  <tr><td>Model complexity</td><td>Number of parameters and FLOPs</td></tr>
  <tr><td>Runtime performance</td><td>Mean, median, P95/P99 latency and throughput</td></tr>
  <tr><td>Memory requirements</td><td>GPU memory or CPU RAM usage</td></tr>
  <tr><td>Robustness</td><td>Performance across different SNR conditions</td></tr>
  <tr><td>Deployment feasibility</td><td>CPU/GPU compatibility and execution requirements</td></tr>
</table>

Metrics are selected according to the task. In particular, the detection measures obtained from the FMCW perception track are not combined with the RadDet spectrum-detection metrics.

## 3.5 Summary of the Methodology

The methodology establishes two complementary experimental foundations for the study of AI in radar signal processing and detection. The synthetic FMCW track provides a controlled environment for examining conventional signal processing and learning-based spatial target detection. The RadDet track provides a wideband spectrum-detection setting in which a YOLO-based detector is trained and evaluated using modulation-labelled spectrograms.

The resource-efficiency investigation builds on these foundations by considering model-level computation reduction and hardware-oriented inference evaluation. The distinction between implemented experimental methods and proposed future investigations is maintained throughout. This provides a basis for selecting a technically feasible direction for subsequent work using measured detection performance and computational requirements.

### Figure 3.1 — Overall Methodological Framework

**Placement:** Section 3.1, immediately after the paragraph introducing the two experimental tracks.

[AGENT INSTRUCTION — FIGURE 3.1]

Inspect the existing notebooks and documentation for an overall methodology or architecture diagram that can be reused.

The figure must communicate the overall methodology of the study using two clearly separated branches:

**Branch 1 — Synthetic FMCW Radar Perception**

- Synthetic 77 GHz FMCW radar simulation
- Complex radar data cube generation
- Conventional signal processing
- CFAR, MUSIC and DBSCAN-based detection
- CNN-based target detection

**Branch 2 — Wideband Radar Spectrum Detection**

- RadDet dataset
- Time-frequency spectrogram input
- Annotation and dataset preparation
- YOLOv9-C training
- Detection and modulation classification
- SNR-based benchmark evaluation

Both branches should lead towards a common final stage labelled **Computational and Resource-Efficiency Evaluation**.

Do not merge the two data pipelines or suggest that they share the same dataset, architecture, or detection task.

Prefer an existing architecture diagram from the notebooks. Otherwise, create a Mermaid flowchart with two distinct branches and a common evaluation stage.

Caption: _Figure 3.1: Overall methodological framework illustrating the two experimental tracks and their role in the investigation of resource-efficient AI for radar processing and detection._

### Figure 3.2 — FMCW Radar Signal Processing Pipeline

**Placement:** Section 3.2.2, immediately after the introductory paragraph describing the conventional signal processing stages.

[AGENT INSTRUCTION — FIGURE 3.2]

Inspect `01_radar_classical_dsp.ipynb`, its exported figures in `docs/assets/nb1/`, and the relevant source modules for an existing end-to-end radar processing diagram.

The figure should represent the following processing sequence:

1. Raw complex radar data cube, with dimensions `(num_rx, num_chirps, num_samples)`.
2. Hann windowing and fast-time Range FFT.
3. Clutter suppression along the slow-time dimension.
4. Slow-time Doppler FFT.
5. Range-Doppler representation.
6. CFAR target detection.
7. MUSIC/Capon angle estimation using antenna-array information.
8. DBSCAN spatial clustering.
9. Final clustered target detections.

Show the data flow with labelled intermediate representations wherever possible.

The diagram should make clear that angle estimation uses spatial information across receiving antennas and that DBSCAN operates on the extracted detections.

Prefer an existing notebook diagram. If none adequately represents this sequence, generate a Mermaid flowchart.

Caption: _Figure 3.2: Conventional FMCW radar signal processing pipeline from complex baseband data acquisition to spatial target detection and clustering._

### Figure 3.3 — CNN Architecture for Synthetic FMCW Target Detection

**Placement:** Section 3.2.3, immediately after the paragraph describing the fully convolutional CNN architecture and before discussing its prediction heads.

[AGENT INSTRUCTION — FIGURE 3.3]

Inspect `src/models/radar_detector_cnn.py` and the architecture visualisations in `02_radar_deep_learning_detection.ipynb`.

Create a model architecture diagram that reflects the actual implementation:

**Input**

- Single-channel normalised Range-Doppler representation.

**Feature extraction**

- Stem: convolution, batch normalisation and LeakyReLU.
- Two residual blocks with 32 channels.
- Expansion convolution from 32 to 64 channels.
- Two residual blocks with 64 channels.

**Two prediction heads**

- Classification head: convolutional layers producing five class heatmaps (background, car, pedestrian, cyclist and drone).
- Regression head: convolutional layers producing four channels for normalised range centre, velocity centre, range width and velocity width.

Show both heads receiving the shared backbone features.

Do not depict YOLO, transformer blocks, attention modules, or downsampling stages: these are not part of this CNN implementation.

Prefer the actual architecture diagram from the notebook if it agrees with the source code. Otherwise, create a Mermaid flowchart.

Caption: _Figure 3.3: Architecture of the convolutional neural network used for synthetic FMCW radar target classification and coordinate regression._

### Figure 3.4 — RadDet Spectrogram and Detection Workflow

**Placement:** Section 3.3.2, immediately after the paragraph explaining the two-dimensional time-frequency spectrogram representation and before introducing the eleven modulation classes.

[AGENT INSTRUCTION — FIGURE 3.4]

Inspect the RadDet notebook, `data/raddet_sample/`, `data/kaggle_outputs/`, and `docs/assets/nb3/` for an actual spectrogram image with ground-truth bounding-box annotations.

Prefer a representative real RadDet sample showing:

- Time on the horizontal axis.
- Frequency on the vertical axis.
- Radar signal emissions as visible time-frequency structures.
- Ground-truth bounding boxes around the annotated signal regions.
- Class labels where available.

The figure should help readers understand that the task is to localise radar emissions in a time-frequency representation rather than detect physical vehicles or pedestrians.

If an appropriate spectrogram is available, use that image rather than generating a synthetic illustration. If necessary, use the existing RadDet visualisation utilities to export a clean sample with annotations.

Caption: _Figure 3.4: Representative RadDet time-frequency spectrogram illustrating radar signal emissions and their ground-truth detection annotations._

**Optional workflow extension:** If the figure layout permits, place a small Mermaid workflow immediately below the spectrogram, showing:

RadDet dataset → Spectrogram loading → Annotation parsing → YOLOv9-C detector → Bounding boxes and modulation classes → SNR-stratified evaluation.

Do not make the workflow overly crowded; the spectrogram itself is the primary visual element.

# Additional Chapter 3 Content — Code Listings and Algorithms

## Section 3.2.2 — Conventional FMCW Signal Processing

[AGENT INSTRUCTION — ALGORITHM 3.1]

Include a numbered pseudocode algorithm titled:

**Algorithm 3.1: Conventional FMCW Radar Signal Processing and Detection**

The pseudocode should explain the complete implemented processing sequence:

1. Initialise the radar configuration and simulator.
2. Generate target scenes and the complex radar data cube.
3. Apply a Hann window and perform the fast-time Range FFT.
4. Apply mean-subtraction clutter filtering along the slow-time dimension.
5. Apply the slow-time Doppler FFT and shift the zero-Doppler bin.
6. Obtain the Range-Doppler power representation.
7. Apply the configured CFAR detector to extract candidate target detections.
8. Estimate target angles using the available receive-channel information and the selected AoA method.
9. Convert detections to Cartesian coordinates and perform DBSCAN clustering.
10. Return clustered target detections.

Clearly indicate the input and output of the algorithm, including the radar cube dimensions and detection representation.

The pseudocode must distinguish the main processing sequence from optional algorithms. Do not imply that all CFAR variants or all AoA estimators are executed simultaneously.

**Code Listing 3.1: Fast-Time Range FFT**

Include a short Python excerpt from `src/dsp/range_processing.py`:

```plaintext
def process(self, radar_cube):
    windowed = radar_cube * self.window[
        np.newaxis, np.newaxis, :
    ]

    range_profile = np.fft.fft(
        windowed,
        n=self.n_fft,
        axis=-1
    )

    return range_profile, self.range_axis

```

Explain that the FFT operates along the final dimension, corresponding to fast-time ADC samples, while preserving the receive-antenna and chirp dimensions.

Caption: _Code Listing 3.1: Hann-windowed fast-time FFT implementation for FMCW range processing._

Source: `src/dsp/range_processing.py`.

## Section 3.2.3 — Deep Learning-Based FMCW Target Detection

[AGENT INSTRUCTION — CODE LISTING 3.2]

Include a short Python excerpt illustrating the actual forward pass of `RadarObjectDetectorCNN`.

```plaintext
def forward(self, x):
    feat = self.stem(x)
    feat = self.res1(feat)
    feat = self.res2(feat)
    feat = self.expand(feat)
    feat = self.res3(feat)
    feat = self.res4(feat)

    cls_logits = self.cls_head(feat)
    box_preds = self.box_head(feat)

    return cls_logits, box_preds

```

Explain the shared convolutional feature extraction and the two independent prediction heads. Clearly identify the classification heatmap output and the four-channel coordinate regression output.

Caption: _Code Listing 3.2: Forward-pass implementation of the synthetic FMCW radar CNN._

Source: `src/models/radar_detector_cnn.py`.

[AGENT INSTRUCTION — ALGORITHM 3.2]

Include a numbered pseudocode algorithm titled:

**Algorithm 3.2: Synthetic FMCW Dataset Generation and CNN Training**

Describe the following operations:

1. Generate a deterministic target scene using the sample index and random seed.
2. Simulate the complex radar data cube with target returns, stationary clutter, and AWGN.
3. Apply Range FFT, mean-subtraction clutter filtering, and Doppler FFT.
4. Average power across receive antennas and normalise the resulting Range-Doppler map.
5. Create class heatmaps and coordinate regression targets using the known simulated target locations.
6. Split the dataset into training and validation subsets.
7. Initialise the CNN, AdamW optimiser and cosine annealing scheduler.
8. Perform forward propagation, calculate the multi-task loss, backpropagate gradients, and update model parameters.
9. Evaluate the validation loss after each training epoch.
10. Return the trained model and training history.

Include the actual loss formulation:

\mathcal{L}_{cls}_

_+_

_2\mathcal{L}_{box}

$$

Explain the classification loss, foreground mask and masked Smooth L1 regression loss.

Source files:

- `src/models/radar_dataset.py`
- `src/models/radar_detector_cnn.py`
- `src/models/train_detector.py`.

## Section 3.3.2 — RadDet Dataset Preparation

[AGENT INSTRUCTION — ALGORITHM 3.3]

Include a numbered pseudocode algorithm titled:

**Algorithm 3.3: RadDet Spectrogram and Annotation Preparation**

Describe:

1. Load the selected dataset split.
2. Read the spectrogram image.
3. Convert the image to grayscale.
4. Convert pixel values to floating point and normalise to [0, 1].
5. Read the corresponding YOLO annotation file.
6. Extract class indices and normalised bounding-box coordinates.
7. Convert the annotations into tensors.
8. Return the image and its corresponding targets.

Include the annotation format:


$$

(c,x_c,y_c,w,h)

$$

Explain that the coordinates are normalised relative to image dimensions.

An optional short source excerpt may show image normalisation:

```plaintext
with Image.open(img_path) as pil_img:
    pil_img = pil_img.convert("L")
    img_arr = np.array(pil_img, dtype=np.float32) / 255.0

img_tensor = torch.from_numpy(img_arr).unsqueeze(0)

```

Caption: *Code Listing 3.3: Grayscale spectrogram loading and normalisation.*

Source: `src/raddet/dataset.py`.

## Section 3.3.3 — YOLO-Based Detection Architecture and Training

[AGENT INSTRUCTION — ALGORITHM 3.4]

Include a numbered pseudocode algorithm titled:

**Algorithm 3.4: RadDet YOLO-Based Model Training**

Describe the experimental training workflow:

1. Initialise the YOLOv9-C model using pretrained weights.
2. Load the prepared training and validation datasets.
3. Configure input resolution and training hyperparameters.
4. Perform a pre-flight GPU batch-size test.
5. Train using the configured AdamW optimiser and augmentations.
6. Monitor validation performance.
7. Save periodic checkpoints.
8. Apply early stopping using the configured patience.
9. Retain the best-performing checkpoint.

Do not imply that the maximum configured epoch count was necessarily completed.

Refer to the actual benchmark notebook for the exact training arguments.

Source: `03_raddet_spectrum_detection_kaggle.ipynb`.

The architecture diagram should be based on the actual YOLOv9-C architecture, not the synthetic FMCW CNN.

## Section 3.3.4 — Multi-SNR Evaluation and Performance Measurement

[AGENT INSTRUCTION — ALGORITHM 3.5]

Include a numbered pseudocode algorithm titled:

**Algorithm 3.5: Multi-SNR Evaluation and GPU Inference Benchmarking**

Describe two parts:

**Part A — Multi-SNR Evaluation**

1. Load the selected trained checkpoint.
2. Load the held-out test dataset.
3. Evaluate the detector over the six configured SNR levels.
4. Calculate precision, recall, mAP50 and mAP50:95 for each evaluation condition.
5. Aggregate the evaluation metrics.
6. Export the comparison table and performance curves.

**Part B — Inference Latency**

1. Initialise the model and select the CUDA device.
2. Use batch-size-one inputs.
3. Execute warm-up iterations.
4. Synchronise the GPU.
5. Measure repeated forward passes using CUDA events.
6. Synchronise the GPU after execution.
7. Calculate mean, median and P95 latency.
8. Calculate average FPS from mean latency.

Include the throughput relationship:


$$

FPS*{avg}=\frac{1000}{Latency*{mean},(\mathrm{ms})}

$$

Caption: *Algorithm 3.5: SNR-stratified detection evaluation and single-frame GPU inference benchmarking.*

Source: `03_raddet_spectrum_detection_kaggle.ipynb`.

## Section 3.4 — Resource-Efficiency Investigation

Do not add implementation code for proposed approaches that have not yet been implemented.

Present their candidate methods through mathematical formulations and methodology descriptions. Actual code and pseudocode for quantisation, pruning, CPU inference, knowledge distillation or adaptive computation should be added only when those implementations are undertaken and verified.
$$
