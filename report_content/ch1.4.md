## 1.4 Scope of the Study and Organisation of the Report

The scope of this study covers the development and evaluation of a foundation for AI-based radar signal processing and detection, with particular emphasis on computational requirements and practical deployment considerations.

The completed experimental work covers two distinct radar applications. The first involves the simulation of 77 GHz FMCW radar measurements, the implementation of conventional signal processing techniques, and the development of a convolutional neural network for synthetic automotive target detection. The second involves wideband radar spectrum detection using the RadDet dataset, including dataset preparation, YOLO-based detection, and GPU-based benchmark evaluation.

The resource-efficiency aspect of the study is addressed through the examination of model complexity, computational requirements, inference latency, and potential deployment constraints. More advanced approaches, including model quantisation, pruning, knowledge distillation, adaptive computation, and CPU-oriented inference, are considered as directions for further investigation. Their effectiveness is not assumed in advance.

The scope does not include the deployment of a complete radar system on physical radar hardware or the claim that all proposed computational optimisation techniques have already been experimentally validated.

The remainder of this report is organised as follows. Chapter 2 reviews the relevant literature on radar signal processing, learning-based radar detection, available datasets, and computationally efficient AI methods. Chapter 3 describes the methodology adopted in the two experimental tracks and the proposed framework for evaluating resource efficiency. Chapter 4 presents and discusses the experimental results, including the synthetic FMCW experiments and the RadDet benchmark. Finally, Chapter 5 summarises the findings, discusses the limitations of the study, and identifies directions for future work.
