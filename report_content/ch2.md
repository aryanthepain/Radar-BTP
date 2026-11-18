# Instructions

- Reuse existing bibliography entries wherever possible.
- Preserve existing citation numbering when practical.
- Add RAVEN as reference [31].
- Add AdaRadar as reference [32].
- Correct the existing TransRAD [15] bibliographic metadata.
- Use IEEE-style numerical citations consistently.
- Maintain a single master bibliography.
- Do not invent DOIs, publication details, authors, or URLs.
- The existing research dossier and GitHub Pages manuscript contain some numerical claims and proposed experimental results that require further verification.

  Do not automatically reproduce them as established facts.

  Use published results with proper attribution. Use locally verified results only when supported by experiment logs, notebooks or benchmark outputs.

# Chapter 2: Literature Review

## 2.1 Radar Signal Processing and FMCW Radar

Radar systems estimate the properties of objects by transmitting electromagnetic signals and analysing their reflected returns. Conventional radar processing involves extracting target information such as range, radial velocity, and direction of arrival from the received signals. The fundamental principles of radar detection and estimation are discussed extensively in standard references such as Skolnik [4] and Richards [5].

Frequency-Modulated Continuous-Wave (FMCW) radar is particularly relevant to modern automotive and short-range sensing applications. In an FMCW system, the transmitted signal undergoes a continuous frequency sweep over a specified bandwidth. The received echo is mixed with the transmitted waveform to produce an intermediate-frequency beat signal. The beat frequency provides information about target range, while phase variations across successive chirps enable estimation of radial velocity. Multiple receiving antennas additionally provide spatial information that can be used for angle estimation.

The use of Fourier-based processing is fundamental to conventional FMCW radar systems. A Fast Fourier Transform (FFT) applied along the fast-time dimension estimates target range, while processing across the slow-time dimension extracts Doppler information. Spatial processing across antenna channels provides estimates of target direction. These operations produce structured radar representations such as Range-Doppler maps and Range-Azimuth-Doppler data.

Although Fourier-based methods provide an efficient and physically interpretable approach, their resolution and detection capabilities depend on signal bandwidth, coherent processing duration, antenna aperture, and the underlying assumptions of the estimator. These limitations motivate the investigation of additional processing techniques for challenging radar environments.

## 2.2 Classical Radar Detection and Estimation Techniques

Traditional radar systems use a combination of deterministic signal-processing and statistical detection techniques. These methods provide established baselines against which more recent data-driven approaches can be evaluated.

**Fourier-based Range and Doppler Estimation:** Range and Doppler estimation are generally performed using one-dimensional FFT operations along the corresponding radar data dimensions. Windowing functions, including Hann windows, are commonly applied to control spectral leakage. However, reducing sidelobes through windowing generally introduces a trade-off involving main-lobe width and effective resolution. These characteristics are discussed in detail by Richards [5].

**Moving Target Indication (MTI):** MTI filters suppress stationary or slowly varying background returns by exploiting changes across successive radar pulses or chirps. Delay-line cancellers are common implementations. While these filters can improve the visibility of moving targets against stationary clutter, their frequency response contains blind-speed regions where certain moving targets may also be attenuated.

**Constant False Alarm Rate (CFAR) Detection:** CFAR algorithms estimate the local background level around a Cell Under Test (CUT) and establish an adaptive detection threshold. Cell-Averaging CFAR (CA-CFAR) uses the average power of surrounding reference cells, while Ordered-Statistic CFAR (OS-CFAR) uses a selected order statistic. Rohling [6] examined CFAR thresholding in clutter and multiple-target situations, highlighting the importance of selecting an appropriate detection strategy for non-homogeneous environments.

A limitation of local CFAR approaches is their sensitivity to the composition of the reference window. In dense multi-target environments, strong neighbouring targets can influence the estimated background level and increase the detection threshold. Similarly, transitions between different clutter regions can cause deviations from the statistical assumptions used in threshold selection.

**Direction-of-Arrival Estimation:** High-resolution spatial estimation techniques such as Multiple Signal Classification (MUSIC) use the eigenstructure of a spatial covariance matrix to distinguish signal and noise subspaces. Schmidt [7] introduced the MUSIC approach for multiple-emitter location and signal parameter estimation. Capon's minimum-variance approach [20] provides another important method for spatial spectrum estimation.

These techniques can provide high angular resolution under suitable conditions. However, their performance depends on factors such as signal-to-noise ratio, the number of available antenna elements, covariance estimation quality, and the statistical relationship between received signals. Their computational requirements can also become significant when repeated covariance estimation and eigendecomposition are required.

**Spatial Clustering:** Algorithms such as Density-Based Spatial Clustering of Applications with Noise (DBSCAN), introduced by Ester et al. [21], can group spatially neighbouring radar detections into clusters. This provides a useful intermediate representation for downstream perception. However, clustering operates on extracted detections and does not inherently provide semantic classification of objects.

Together, these techniques constitute an established and interpretable radar processing pipeline. They also provide important reference baselines for evaluating whether learned detection methods offer practical improvements.

## 2.3 Deep Learning for Radar Signal Processing

Deep learning has emerged as an important research direction for radar signal processing because neural networks can learn complex representations from measured or simulated radar data. Geng et al. [10] provide a broad survey of deep learning applications in radar, covering waveform recognition, antenna and waveform design, automatic target recognition, and clutter or jamming-related tasks.

One important application is radar target classification and recognition. Radar measurements can be represented using high-resolution range profiles, Doppler signatures, spectrograms, or spatial radar tensors. These representations provide different forms of information about the observed scene and can be processed using neural architectures suited to the corresponding data structure.

Convolutional Neural Networks (CNNs) are particularly useful for extracting local spatial and frequency-domain features. Their convolutional filters and hierarchical feature representations allow networks to learn patterns from radar maps without requiring every detection rule to be manually specified. Patel et al. [11], for example, investigated deep learning-based object classification using automotive radar spectra.

Karlsson [1] presents several applications of artificial neural networks to radar signal processing in an industrial radar research context. The thesis examines data-driven approaches to problems including stepped-frequency pulse compression, track-before-detect processing, micro-Doppler classification, and target tracking in multipath environments. An important observation from this work is that learned approaches can provide alternatives to computationally demanding conventional estimators when the underlying signal models are difficult to represent analytically or are computationally expensive to solve.

More recent work has explored architectures beyond conventional CNNs. TransRAD, proposed by Cheng and Cao [15], uses a Retentive Vision Transformer to process Range-Azimuth-Doppler radar representations. Its Retentive Manhattan Self-Attention mechanism incorporates spatial structure into feature extraction, while location-aware non-maximum suppression is used to address duplicate detections.

The broader literature indicates that deep learning can support multiple radar processing tasks, including detection, classification, waveform recognition, clutter suppression, and tracking. However, its practical effectiveness depends on the quality and diversity of training data, the representativeness of the test environment, and the computational resources required for inference.

Geng et al. [10] also discuss limitations such as insufficient training data and vulnerability to adversarial examples. Consequently, high performance on a particular dataset should not automatically be interpreted as evidence of generalisation to different radar systems or operating environments.

## 2.4 Radar Datasets and Benchmarking Approaches

The development and evaluation of radar AI systems depend heavily on the availability of suitable datasets. Different datasets represent different sensing configurations and research tasks, and their results should therefore be interpreted within their respective application contexts.

The CARRADA dataset, introduced by Ouaknine et al. [12], provides camera and automotive radar data with Range-Angle-Doppler annotations. It supports research on automotive radar perception and multimodal learning. Other datasets, including nuScenes [13] and TJ4D [14], provide additional resources for autonomous driving and radar-based environmental perception.

Karlsson's thesis [1] also provides an industrial research perspective on the use of radar measurements and simulated data for developing neural signal-processing methods. Such research highlights the importance of understanding the relationship between the physical sensing configuration, the signal representation, and the learning task.

A particularly relevant resource for the second experimental track of the present project is RadDet, introduced by Huang et al. [2] at IEEE ICASSP 2025. RadDet addresses wideband radar spectrum detection and provides annotated time-frequency representations for identifying radar signals.

The dataset contains approximately 40,000 frames generated from one million in-phase and quadrature samples across a 500 MHz frequency band. It includes eleven radar signal classes, six signal-to-noise ratio settings, and multiple radar density conditions. The benchmark also provides three spectrogram resolution configurations: S-128, M-256, and L-512.

The authors evaluate multiple real-time object detection architectures, including YOLOv3, YOLOv6-M, YOLOv9-M, and RT-DETR-L. Their experiments provide a basis for studying the trade-off between detection performance, input resolution, and inference cost.

An important aspect of RadDet is that its task differs from automotive object detection. It focuses on detecting and classifying radar signals in a wideband radio-frequency spectrum, rather than identifying vehicles, pedestrians, or other physical objects in road scenes.

This distinction is important for the present project because the repository contains two separate experimental tracks. The synthetic FMCW pipeline investigates automotive radar processing and spatial target detection, whereas the RadDet workflow investigates wideband RF spectrum detection and modulation classification. Results from these tracks are useful for different aspects of the research and must not be treated as directly interchangeable.

## 2.5 Computationally Efficient and Edge-Oriented Radar AI

Although deep learning has demonstrated its potential for radar processing, computational efficiency remains an important consideration for practical deployment. Radar systems may need to process successive measurements within strict time constraints, while operating with limited memory, processing power, and energy availability.

The computational cost of a neural network depends on several factors, including the number of parameters, input resolution, network depth, feature-map dimensions, and the operations performed by the architecture. Consequently, comparing models solely by parameter count or FLOPs does not provide a complete picture of their deployment efficiency.

Several research directions address this challenge.

**Lightweight Neural Architectures:** Efficient architectures aim to reduce the number of parameters and computational operations while retaining useful feature-extraction capabilities. Such approaches are relevant when radar models must operate on embedded processors or systems with restricted memory and processing capacity.

**Model Quantisation:** Quantisation represents model parameters and activations using reduced numerical precision. For example, INT8 inference can reduce the memory required to store weights and may improve execution efficiency on hardware with suitable integer-operation support. However, the actual speed improvement depends on the processor, runtime, and availability of optimised kernels. The DRDO survey by Pal [3] discusses AI-related radar developments, including the relevance of efficient edge-oriented implementations.

**Knowledge Distillation:** Knowledge distillation transfers information from a larger teacher network to a smaller student network. The student is trained to reproduce selected outputs or intermediate representations of the teacher. This provides a potential means of reducing model complexity while retaining useful detection capabilities.

**Pruning and Efficient Feature Processing:** Pruning removes selected parameters or computational structures from a trained network. Combined with efficient feature representations, this can reduce model size and potentially inference cost. The benefits depend on whether the resulting sparsity is supported by the target hardware and execution framework.

**Adaptive Computation:** Instead of allocating the same computational resources to every input, adaptive methods attempt to vary the processing effort according to input complexity or prediction confidence. Examples include early-exit architectures, cascaded models, conditional computation, and adaptive input-resolution selection.

Recent work demonstrates that computational efficiency in radar systems can be addressed at multiple levels.

RAVEN, presented by Sen et al. at CVPR 2026 [31], introduces an adaptive chirp-wise processing architecture for FMCW radar. It uses receiver-specific state-space encoders, a learnable antenna-mixing module, and calibrated early-exit inference. Rather than processing every chirp with the same computational depth, it can terminate processing after a subset of chirps when sufficient information is available. This provides a relevant example of adaptive computation applied directly to radar perception.

AdaRadar, presented by Park et al. at CVPR 2026 [32], investigates adaptive spectral compression for radar-based perception. It combines frequency-domain coefficient selection, adaptive compression, and quantisation to reduce the amount of radar data that must be transferred to a downstream computing engine. This work demonstrates that computational efficiency can also be addressed before neural inference, at the radar data representation and communication stages.

These studies indicate that efficient radar AI is not limited to reducing neural network size. It can involve optimising the representation, processing pipeline, numerical precision, computation allocation, and data movement.

An additional consideration is the choice of inference hardware. GPUs provide parallel processing capabilities and are commonly used for training and accelerating neural networks. However, dedicated GPU hardware may not always be available or economically practical for a particular demonstration or deployment environment. Commodity CPUs offer a more widely accessible alternative, although their performance depends strongly on the architecture of the model and the availability of optimised inference libraries.

The CPU-oriented deployment problem should therefore be treated as a hardware-specific experimental question rather than assuming that a model with fewer FLOPs will automatically run faster on a CPU. Comparisons between CPU and GPU execution must account for inference latency, throughput, memory consumption, numerical precision, and the hardware and software configurations used.

### 2.6 Research Gaps and Project Motivation

The literature reviewed above establishes the potential of combining conventional radar signal processing with deep learning. However, several questions remain relevant when considering practical deployment under limited computational resources.

**Research Gaps**

- **Computational cost of radar AI:** Radar-specific deep learning research demonstrates a range of applications, but computational requirements such as model size, memory consumption, inference latency, and throughput must also be considered when evaluating deployment feasibility.
- **Limited comparison of efficiency strategies:** Lightweight network architectures, pruning, quantisation, knowledge distillation, and adaptive computation offer different ways to reduce computational requirements. Their relative trade-offs in radar applications need to be evaluated under consistent experimental conditions.
- **Hardware dependence:** A model that performs efficiently on a GPU may not have the same practical performance on a CPU. Hardware-specific inference behaviour, memory constraints, and runtime overhead therefore need to be considered alongside model accuracy.
- **Training and inference requirements:** The resources required to train a model can differ substantially from those required to execute it. A practical radar demonstration may have modest inference requirements even when model development or training uses GPU resources.
- **Task and dataset differences:** Radar perception and radar spectrum detection are related but distinct problems. Results obtained using automotive FMCW radar data should not be treated as directly interchangeable with results obtained using wideband RF spectrum datasets. Evaluation must account for the input representation, target task, dataset, and metrics used.
- **Robustness and reproducibility:** Improvements in computational efficiency should be evaluated together with detection performance and reliability. Comparisons should use clearly specified datasets, hardware, input resolutions, and measurement procedures so that the resulting trade-offs can be interpreted meaningfully.

**Project Motivation**

- **Establish a common radar processing foundation:** This study draws upon a modular radar-processing framework encompassing FMCW radar simulation, conventional signal-processing techniques, and deep-learning-based detection. This provides a foundation for examining both conventional and learning-based approaches to radar processing.
- **Study complementary radar tasks:** This study examines two complementary radar settings: synthetic 77 GHz FMCW automotive radar perception and wideband radar spectrum detection using the RadDet dataset. Since these settings address different tasks and use different data representations, they are analysed separately using task-appropriate evaluation procedures.
- **Investigate algorithm-level efficiency:** Candidate approaches include lightweight model architectures, pruning, quantisation, knowledge distillation, and adaptive computation. Their suitability will be assessed rather than assumed in advance.
- **Investigate hardware-oriented efficiency:** CPU and GPU inference will be considered as separate deployment settings. Where possible, comparisons will distinguish the performance of the same model across hardware from the performance of architectures designed specifically for resource-constrained inference.
- **Make the next-stage demonstration feasible:** The work will identify the computational and hardware requirements for a practical demonstration in the following semester, including the distinction between model-development resources and deployment-time resources.
- **Keep the research direction evidence-driven:** The project adopts resource-efficient AI for radar signal processing and detection as its overarching direction. The relative importance of reducing total computation and enabling CPU-oriented inference will be determined from the results of the planned experiments.
