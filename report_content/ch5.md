# Chapter 5: Conclusion and Future Work

## 5.1 Summary of the Study

This study investigated resource-efficient AI for radar signal processing and detection. The work was motivated by the need to balance detection performance with computational cost, memory requirements, and practical deployment constraints.

Two distinct experimental tracks were considered. The first focused on synthetic 77 GHz FMCW automotive radar perception, using conventional signal processing and a CNN-based detector. The second investigated wideband radar spectrum detection using the RadDet dataset and a YOLO-based detection workflow.

Together, these experiments established a foundation for studying learning-based radar detection and its computational requirements. The investigation retained two complementary directions for further work: reducing the computation required by AI models and enabling efficient inference on CPU-oriented platforms. Neither direction was selected as the final research pathway because further comparative experiments are required.

## 5.2 Conclusions and Achievement of Objectives

The objectives established in Chapter 1 are summarised below.

**Table 5.1: Objective achievement summary**

<table>
  <tr><th>Objective</th><th>Achievement</th></tr>
  <tr><td>Establish a radar processing foundation</td><td>Substantially achieved. The FMCW simulator and conventional DSP pipeline were implemented and experimentally examined.</td></tr>
  <tr><td>Study AI-based radar detection</td><td>Partially achieved. Initial CNN and YOLO-based workflows were established, but comprehensive and reproducible detection evaluation remains incomplete.</td></tr>
  <tr><td>Characterise computational requirements</td><td>Partially achieved. The FMCW CNN parameter count and training duration were recorded. Complete inference and memory profiling remains pending.</td></tr>
  <tr><td>Investigate computational reduction</td><td>Pending. Lightweight architectures, pruning, quantisation, distillation, and adaptive computation remain future experiments.</td></tr>
  <tr><td>Investigate CPU-oriented inference</td><td>Partially achieved. CPU-based CNN training was demonstrated, but controlled CPU inference evaluation has not been completed.</td></tr>
  <tr><td>Establish a comparative evaluation framework</td><td>Partially achieved. Evaluation criteria were defined, but consistent measurements across models and hardware are still required.</td></tr>
  <tr><td>Define a practical demonstration</td><td>Partially achieved. The requirements have been identified; hardware availability and application constraints must be confirmed.</td></tr>
  <tr><td>Select a feasible research pathway</td><td>Deferred. The final direction should be selected using comparative experimental evidence.</td></tr>
</table>

The study has therefore achieved its primary foundation-building objectives, while the central resource-efficiency objectives remain open. In particular, the present results do not establish that model compression or CPU-oriented inference provides a superior accuracy–efficiency trade-off. These questions form the main focus of the subsequent project phase.

## 5.3 Key Findings and Research Implications

### 5.3.1 Synthetic FMCW Radar Perception

The conventional FMCW processing experiment successfully recovered the range and radial velocity of four simulated targets. Mean-subtraction clutter suppression achieved 12.94 dB attenuation, while the four associated detections produced a range MAE of 0.0125 m and velocity MAE of 0.105 m/s.

These findings demonstrate that the implemented conventional processing pipeline provides a useful baseline under controlled simulation conditions. However, the additional CFAR candidate could not be conclusively classified as a false alarm. Furthermore, the angle-estimation experiment contained a target-association issue; its reported angular values should not be interpreted as validated accuracy measurements.

The CNN experiment established an initial learning-based baseline with 136,041 trainable parameters. It completed five training epochs on CPU in 26.89 seconds. Although the validation loss initially decreased, the small dataset and limited evaluation do not establish generalisation or reliable detection accuracy.

### 5.3.2 Wideband RadDet Spectrum Detection

The RadDet experiments established a separate spectrogram-based detection workflow. The executed YOLOv8n prototype recorded zero precision, recall, and mAP across its saved training results, and therefore did not establish a successful detection baseline.

The repository also contains documentation reporting full-scale YOLOv9-C benchmark results. However, these results could not be independently verified from the saved Phase 2 notebook execution. Published YOLOv9-M results remain external reference values and must not be presented as results obtained in this study.

A reproducible full-scale RadDet evaluation is therefore still required, including test-set metrics and SNR-stratified results generated directly from the trained detector.

### 5.3.3 Implications for Resource Efficiency

The experiments provide initial reference points for studying computational efficiency, but they do not yet establish a complete accuracy–complexity comparison. In particular, model size and training duration cannot substitute for inference latency, throughput, or memory measurements.

The main implication is that computational efficiency must be evaluated on the intended hardware and alongside task-specific detection performance. A reduction in model parameters or FLOPs does not necessarily translate into faster execution on every processor. Controlled CPU and GPU measurements will therefore be essential before selecting a deployment strategy.

## 5.4 Limitations of the Study

The main limitations are:

1. **Synthetic FMCW data:** The automotive perception experiments used simulated measurements. Validation on real radar data is necessary before drawing conclusions about practical deployment.
2. **Limited CNN evaluation:** The small training dataset and absence of independent detection metrics restrict conclusions about accuracy and generalisation.
3. **Angle-estimation association:** The range-only target selection in the AoA experiment prevents the reported angular values from serving as validated error measurements.
4. **RadDet reproducibility:** The executed YOLOv8n prototype did not achieve non-zero detection metrics, while the documented YOLOv9-C full-scale results require independent reproduction.
5. **Incomplete resource profiling:** Verified CPU inference latency, CPU-versus-GPU comparisons, peak memory usage, and energy measurements are not yet available.
6. **No physical radar deployment:** The study has not yet demonstrated the complete pipeline using a physical radar sensor or a constrained deployment platform.

These limitations define the experiments required to strengthen the results in the next phase.

## 5.5 Future Work

Future work will focus on three complementary areas.

### A. Reducing Computational Requirements

The first direction is to investigate methods that reduce model complexity and inference cost while retaining acceptable detection performance. Candidate experiments include:

- **Lightweight architectures:** Explore compact backbones and efficient convolutional operations.
- **Pruning:** Evaluate structured and unstructured removal of redundant model parameters.
- **Quantisation:** Investigate reduced-precision inference, particularly INT8, and measure its effect on detection quality and runtime.
- **Knowledge distillation:** Transfer useful detection behaviour from a larger teacher model to a smaller student model.
- **Adaptive computation:** Explore multi-resolution inference, conditional computation, and early exits to allocate computation according to input difficulty.

These techniques will be treated as experimental candidates rather than assumed improvements.

### B. CPU-Oriented Inference

The second direction is to establish whether selected models can meet deployment requirements on CPU platforms.

The proposed work includes native CPU inference baselines, followed by evaluation using ONNX Runtime CPU and OpenVINO where supported. Identical model weights and inputs should be used for CPU and GPU comparisons wherever possible.

Measurements should include batch-size-one latency, mean and tail latency, throughput, peak RAM and VRAM usage, and detection performance. The results will determine whether CPU execution is sufficient or whether GPU acceleration is necessary for the intended application.

### C. Further Experimental Validation

The experimental foundation should be strengthened before drawing final conclusions about efficiency.

For the FMCW track, this includes testing additional target scenes, SNR and clutter conditions, correcting the AoA association procedure, and evaluating against real-world radar measurements where available.

For RadDet, the full-scale detector evaluation should be reproduced using a documented data split, saved checkpoint, and independently generated test metrics. SNR-stratified performance should be measured directly.

Finally, controlled ablation studies should compare baseline models with selected optimisation techniques. The study should also examine whether model compression and CPU-oriented inference provide complementary benefits when combined.

**Table 5.2: Proposed roadmap for the subsequent phase**

<table>
  <tr><th>Stage</th><th>Main activity</th><th>Expected outcome</th></tr>
  <tr><td>1</td><td>Reproduce and consolidate experimental baselines</td><td>Reliable task-specific results</td></tr>
  <tr><td>2</td><td>Profile model complexity and resource usage</td><td>Baseline computational measurements</td></tr>
  <tr><td>3</td><td>Implement selected model-efficiency techniques</td><td>Accuracy–complexity comparisons</td></tr>
  <tr><td>4</td><td>Benchmark CPU and GPU inference</td><td>Hardware-specific performance results</td></tr>
  <tr><td>5</td><td>Evaluate combined optimisations</td><td>Selection of a feasible model and runtime</td></tr>
  <tr><td>6</td><td>Integrate and test the demonstration</td><td>Reproducible deployment prototype</td></tr>
</table>

## 5.6 Requirements for the Next-Stage Demonstration

The next-stage demonstration must distinguish between model training and inference. Training larger detectors and conducting repeated optimisation experiments may benefit from GPU acceleration. However, the final demonstration may be able to execute inference on a CPU if the selected model satisfies the application's latency and memory requirements.

The first requirement is to establish a batch-size-one inference baseline. Latency should be measured separately for preprocessing, model execution, post-processing, and the complete pipeline. Mean, median, P95, and P99 latency should be recorded alongside throughput and peak memory usage.

An application-specific latency budget must also be agreed upon. It should reflect the intended radar frame rate and the time available for downstream processing, rather than relying on an assumed real-time requirement.

Before finalising the implementation, the following information must be confirmed with the supervisor or laboratory:

- Available CPU model, core count, instruction-set support, and system RAM.
- Availability and specifications of a GPU, including accelerator memory.
- Target demonstration platform and supported operating system.
- Whether input will come from simulated data, recorded measurements, or a physical radar sensor.
- Expected processing rate and acceptable end-to-end latency.
- Available storage and permission to install optimised inference runtimes.

The exact hardware requirements cannot be fixed until the model and target platform are selected. A provisional approach may use GPU resources for training and CPU execution for deployment evaluation, but this must be validated experimentally. Additional laboratory resources should be requested only after the baseline requirements have been measured.

## 5.7 Final Conclusion

This study established an experimental foundation for investigating resource-efficient AI in radar signal processing and detection. The synthetic FMCW track demonstrated conventional radar processing and an initial CNN-based detection implementation, while the RadDet track established a separate wideband spectrum-detection workflow.

The results provide a starting point but do not yet establish a verified improvement through model compression or CPU-oriented inference. Reproducible detection evaluation, controlled computational profiling, and hardware-specific deployment tests remain necessary.

The central question—whether AI-based radar processing and detection can be made more computationally efficient while maintaining suitable detection performance and practical deployment feasibility—therefore remains open. The next phase will address it through controlled optimisation experiments and a practical demonstration on confirmed hardware.

The final research direction should be determined by measured evidence. Reducing overall computation and enabling CPU-oriented inference remain complementary possibilities, with the objective of developing a radar detection approach that balances performance, computational cost, and practical deployment requirements.
