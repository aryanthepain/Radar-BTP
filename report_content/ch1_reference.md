# Instructions

The below contains the content And the References For chapter one. Create a subagent To Where all there needs to be reference In the original Slash the new version That is currently on the website. Make use of the references below In order to do that. No need to change the content for chapter one on the website. You need to only add references to chapter one and nothing else. Hence use the subagents to create instructions for another subagent To add the relevant references wherever necessary.

- Preserve the umbrella research positioning:
  - Resource-efficient AI for radar signal processing and detection.
  - Algorithmic reduction of computational requirements.
  - CPU-oriented inference and deployment.
- - Keep the two experimental tracks distinct throughout the report:
    - Synthetic 77 GHz FMCW automotive radar perception.
    - RadDet wideband radar spectrum detection.

    Do not describe RadDet as automotive object detection or combine its metrics with the FMCW perception track.

Distinguish model-training resources from inference-time deployment requirements. Do not claim that a CPU-only workflow is already achieved.

Do not invent performance values, hardware specifications, accuracy improvements, or completed efficiency experiments. Planned methods must be described as proposed or to be investigated.

Check the existing `docs/index.html` bibliography while consolidating references. Correct the Skolnik entry's publication year from 2008 to 2001 if that entry is retained. Do not propagate unverified bibliographic details from the old bibliography.

Do not modify unrelated source code, notebooks, experimental outputs, or project configuration.

# Chapter 1: Introduction

## 1.1 Background and Motivation

Radar is an important sensing technology used in applications such as surveillance, navigation, automotive sensing, and remote observation. Unlike optical sensing systems, radar operates by transmitting electromagnetic signals and analysing the signals reflected or scattered by objects. Information about a target can be inferred from properties of the received signal, including propagation delay, Doppler shift, and phase differences across receiving antennas. These principles form the basis of conventional radar detection, estimation, and tracking systems [\cite{skolnik2001introduction,richards2014fundamentals}].

Frequency-Modulated Continuous-Wave (FMCW) radar is widely studied for applications requiring continuous range and velocity estimation. In an FMCW system, the transmitted signal varies its frequency over time according to a defined chirp waveform. Mixing the received signal with a reference copy of the transmitted signal produces a beat signal whose frequency contains information about target range. Processing multiple chirps also enables estimation of target velocity through Doppler information. Conventional processing pipelines therefore employ operations such as range and Doppler transforms, threshold-based detection, and angle estimation to extract useful target information from the received measurements [\cite{skolnik2001introduction,richards2014fundamentals}].

Traditional radar systems rely extensively on mathematically derived signal processing algorithms. These methods provide interpretable and computationally structured solutions for tasks such as filtering, detection, parameter estimation, and tracking. However, radar environments can contain clutter, interference, multiple closely spaced targets, and variations in signal-to-noise ratio. Such conditions motivate the investigation of data-driven techniques that can learn useful representations directly from radar measurements.

In recent years, deep learning has been investigated for several radar processing tasks, including waveform recognition, antenna-array design, automatic target recognition, and clutter or jamming-related processing. Convolutional neural networks and recurrent architectures are among the approaches explored in this area [\cite{geng2021deepradar}]. Research such as Karlsson's doctoral work further investigates the use of artificial neural networks for radar signal processing [\cite{karlsson2023radar}]. These developments indicate that learning-based methods can complement conventional signal processing, although their practical performance depends on the availability of representative data and reliable evaluation.

The adoption of learning-based radar processing also introduces computational considerations. Model size, memory consumption, inference latency, and hardware requirements can affect whether a method is suitable for a practical radar system. The challenges of applying deep learning to radar include not only the learning task itself, but also limitations associated with data availability and the reliability of learned models [\cite{geng2021deepradar}]. Recent discussions of AI-enabled radar also identify computational complexity and edge-oriented deployment as relevant challenges [\cite{pal2025radarai}].

Consequently, this project focuses on **resource-efficient AI for radar signal processing and detection**. The central motivation is to study how learning-based radar methods can be evaluated and adapted under practical computational constraints. Two broad directions are considered: reducing the computational work required by the processing pipeline, and investigating models and inference strategies that can operate effectively on CPU-oriented platforms. These directions will be evaluated before selecting the emphasis for the subsequent stage of the project.

## 1.2 Problem Statement

Deep learning provides several possible approaches for radar signal processing and detection. However, the computational requirements of these approaches may create challenges when they are deployed in environments with limited processing capacity, memory, or access to specialised hardware. A model that achieves good detection performance during GPU-based experimentation may not necessarily be suitable for CPU-based inference or a resource-constrained demonstration.

The problem addressed in this project is therefore:

**How can AI-based radar signal processing and detection be made more resource-efficient while maintaining suitable task performance and supporting practical deployment under constrained computational resources?**

This problem is investigated through two complementary directions:

1. **Algorithmic reduction of computational requirements:** This direction considers whether the computational cost of radar AI can be reduced through approaches such as lightweight architectures, model pruning, quantisation, knowledge distillation, or adaptive computation. These methods are candidate techniques to be investigated rather than assumed solutions.
2. **CPU-oriented model inference:** This direction investigates the feasibility of executing radar AI models without depending exclusively on GPU-based inference. It includes evaluating model behaviour across CPU and GPU environments and considering architectures that may be more suitable for CPU execution.

The two directions are related but not identical. Reducing the number of operations required by a model does not automatically guarantee efficient execution on every hardware platform. Similarly, a model that executes efficiently on a CPU may not necessarily minimise the total computational requirements of the overall radar processing pipeline. The investigation must therefore consider model performance, computational cost, memory usage, and inference behaviour together.

The existing project provides two complementary experimental contexts. The first involves a synthetic 77 GHz FMCW radar perception pipeline, including conventional signal processing and learning-based detection. The second involves the RadDet wideband radar spectrum detection dataset, which addresses the detection of radar signals in a wideband frequency spectrum [\cite{huang2025raddet}]. These tracks represent different radar tasks and use different data representations. They will therefore be evaluated independently wherever their objectives and metrics differ, rather than treating their results as directly interchangeable.

The final research emphasis will be selected based on the experimental findings and the computational resources available for the subsequent-semester demonstration. In particular, model training requirements will be distinguished from inference-time requirements, since the hardware needed to develop a model may differ from the hardware needed to demonstrate its operation.

## 1.3 Objectives

The primary objective of this project is to investigate resource-efficient AI techniques for radar signal processing and detection. The specific objectives are:

1. **Establish a radar processing foundation:** Study conventional radar signal processing methods and learning-based approaches to understand their operating principles, capabilities, and computational requirements.
2. **Characterise the existing experimental pipelines:** Examine the synthetic FMCW radar perception pipeline and the RadDet-based wideband spectrum detection pipeline as separate experimental tracks.
3. **Evaluate algorithm-level efficiency techniques:** Investigate candidate methods such as lightweight neural network architectures, pruning, quantisation, knowledge distillation, and adaptive computation for reducing computational requirements.
4. **Investigate CPU-oriented inference:** Evaluate the feasibility of executing suitable radar AI models on CPU-based platforms and compare their inference behaviour with GPU-based execution under controlled conditions.
5. **Measure performance and resource requirements:** Consider task-appropriate detection performance alongside computational measures such as model parameters, memory usage, inference latency, and throughput. Comparisons should specify the hardware, input representation, and evaluation conditions.
6. **Identify requirements for the next-stage demonstration:** Determine the computational resources, model requirements, and deployment considerations necessary to implement and demonstrate the selected research direction in the subsequent semester.

The project will use these objectives to identify a technically feasible and experimentally supported direction for resource-efficient radar AI, without assuming in advance that either adaptive computation or CPU-oriented inference is the sole solution.

# References

```plaintext
@book{skolnik2001introduction,
  author    = {Skolnik, Merrill I.},
  title     = {Introduction to Radar Systems},
  edition   = {3},
  publisher = {McGraw-Hill},
  address   = {Boston, MA, USA},
  year      = {2001},
  isbn      = {007118189X}
}

@book{richards2014fundamentals,
  author    = {Richards, Mark A.},
  title     = {Fundamentals of Radar Signal Processing},
  edition   = {2},
  publisher = {McGraw-Hill},
  address   = {New York, NY, USA},
  year      = {2014},
  isbn      = {9780071798334}
}

@article{geng2021deepradar,
  author  = {Geng, Z. and Yan, H. and Zhang, J. and Zhu, D.},
  title   = {Deep-Learning for Radar: A Survey},
  journal = {IEEE Access},
  volume  = {9},
  pages   = {141800--141818},
  year    = {2021},
  doi     = {10.1109/ACCESS.2021.3119561}
}

@phdthesis{karlsson2023radar,
  author  = {Karlsson, Alexander},
  title   = {Radar Signal Processing using Artificial Neural Networks},
  school  = {KTH Royal Institute of Technology},
  address = {Stockholm, Sweden},
  year    = {2023},
  note    = {Doctoral dissertation}
}

@inproceedings{huang2025raddet,
  author    = {Huang, Zi and Denman, Simon and Pemasiri, Akila
               and Martin, Terrence and Fookes, Clinton},
  title     = {{RadDet}: A Wideband Dataset for Real-Time Radar
               Spectrum Detection},
  booktitle = {Proceedings of the IEEE International Conference
               on Acoustics, Speech and Signal Processing (ICASSP)},
  pages     = {1--5},
  year      = {2025},
  doi       = {10.1109/ICASSP49660.2025.10887772}
}

@inproceedings{pal2025radarai,
  author    = {Pal, T. K.},
  title     = {Artificial Intelligence based Radar Technology:
               Current Advancements, Future Directions and Challenges},
  booktitle = {2025 IEEE Space, Aerospace and Defence Conference (SPACE)},
  year      = {2025},
  doi       = {10.1109/SPACE65882.2025.11171388}
}

```
