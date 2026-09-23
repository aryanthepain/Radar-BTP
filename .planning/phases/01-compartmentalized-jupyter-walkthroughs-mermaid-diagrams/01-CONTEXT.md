# Phase 1: Compartmentalized Jupyter Walkthroughs & Mermaid Diagrams - Context

**Gathered:** 2026-09-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Equip `01_radar_classical_dsp.ipynb` and `02_radar_deep_learning_detection.ipynb` with clear academic markdown explanations and self-contained Mermaid flow diagrams (top-level end-to-end flow + single comprehensive diagram per section showing data source, functions, transformations, and outputs) so that each stage can be effortlessly explained to the supervising professor during the exploratory thesis presentation.

</domain>

<decisions>
## Implementation Decisions

### Mermaid Diagram Rendering & Platform Compatibility
- **D-01:** Dual embedding: Native ````mermaid ```` code blocks paired with collapsible (`<details>`) high-resolution SVG fallback cells. Do not hardcode custom themes or colours inside Mermaid syntax (keep styling theme-neutral / standard). — **Reversibility:** reversible.
- **D-02:** Positioning: Immediately under each section header as a pre-execution visual map before equations and code cells. — **Reversibility:** reversible.
- **D-03:** Fallback UX: The SVG fallback must be placed in a collapsible `<details>` block (default collapsed) with the prompt: *"Click here to expand fallback diagram if the Mermaid graph above does not render in your environment"*. — **Reversibility:** reversible.
- **D-04:** Coverage & Invariant: Comprehensive coverage with 1 top-level system diagram + 1 dedicated diagram for every substantive technical module (7 in Classical DSP, 5 in Deep Learning). **Mandatory Invariant:** Whenever Python code or function signatures change, the corresponding Mermaid graphs must be maintained and updated in sync. — **Reversibility:** one-way — Broken diagram-code parity invalidates the presentation contract.

### Diagram Topology, Tensor Dimensions & Function Annotations
- **D-05:** Diagram orientation: Hybrid topology — Top-Down (`graph TD`) for top-level end-to-end system architecture flows, and Left-to-Right (`graph LR`) for compact single-stage input-to-output data transforms. — **Reversibility:** reversible.
- **D-06:** Edge and data annotations: Combined representation displaying both the physical domain name and explicit tensor shape & dtype on edges and nodes (e.g., `Raw ADC Time Series [N_rx, N_chirps, N_samples] (complex64)`). — **Reversibility:** reversible.
- **D-07:** Operation node contents: Triple combination of high-level conceptual action label, exact Python class/method signature from `src/dsp/` or `src/models/`, and key mathematical formulation. **Execution Protocol:** Prototype on one section first to visually verify that text does not overlap and remains cleanly readable. — **Reversibility:** reversible.
- **D-08:** Deep Learning architecture diagram: Multi-branch architecture flowchart showing Input RDM `[1, 128, 129]` ──► Conv Backbone ──► Fork into Classification Head (5 classes) & Bounding Box Head (4 coordinates) ──► Join at Multi-Task Loss with Ground Truth Gaussian Splats. — **Reversibility:** reversible.

### Academic Presentation Narrative & Theoretical Rigor
- **D-09:** Mathematical narrative depth: Keep the mathematical narrative grounded, intuitive, and practical with operational radar equations ($\Delta R = \frac{c}{2B}$, $v = \frac{\lambda f_D}{2}$, $T = \alpha P_{noise}$, MUSIC pseudo-spectrum) without heavy textbook theoretical derivations or multi-page proof boxes. — **Reversibility:** reversible.
- **D-10:** Academic discussion notes: Position discussion notes at the end of each section (or natural transition points) modeled as clear, natural narrative explanations of engineering parameter trade-offs rather than rigid exam-style Q&A callouts. — **Reversibility:** reversible.
- **D-11:** Classical DSP vs. Deep Learning comparison: Compact summary table comparing the implemented CNN against the classical pipeline without extending to speculative future thesis directions. — **Reversibility:** reversible.
- **D-12:** Pedestrian micro-Doppler framing: Present micro-Doppler in Section 9 strictly as a self-contained radar kinematic phenomenon without forced connections to deep learning classifiers. — **Reversibility:** reversible.

### Execution Pipeline, Build Automation & Visual Aesthetic
- **D-13:** Notebook maintenance workflow: Primary editing and maintenance on the `.ipynb` files directly as first-class citizens in Jupyter/VS Code, with `scripts/build_walkthrough_notebooks.py` retained as an automated sync/rebuild utility. — **Reversibility:** reversible.
- **D-14:** Execution state: Committed with pre-rendered execution outputs and figures saved in the notebooks so the professor can immediately view all plots and spectra on GitHub or VS Code without needing to execute PyTorch and radar simulations first. — **Reversibility:** reversible.
- **D-15:** Visual theme: Maintain the Dark Cyber-Radar aesthetic (`#0a0e17` background, vibrant neon data curves, high-contrast labels) across all Matplotlib outputs. — **Reversibility:** reversible.
- **D-16:** Test verification: Implement a balanced smoke test in `tests/test_walkthrough_notebooks.py` that executes the underlying radar DSP and CNN code blocks to guarantee they work without error, avoiding superficial JSON-only checks while also skipping excessive long training loops. — **Reversibility:** costly — Verification gate run on every verify.ps1 invocation.

### the agent's Discretion
- Prototype section diagram layout: Selected Section 3 (Fast-Time Range FFT) as the initial visual prototype to validate node spacing, text wrapping, and SVG fallback generation.
- Specific SVG export tooling: Automated headless SVG rendering via Mermaid CLI (`npx @mermaid-js/mermaid-cli`) or Python SVG generator integrated into the build pipeline.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Notebook Files & Generator
- `01_radar_classical_dsp.ipynb` — Primary classical radar DSP walkthrough notebook.
- `02_radar_deep_learning_detection.ipynb` — Primary deep learning radar perception walkthrough notebook.
- `scripts/build_walkthrough_notebooks.py` — Programmatic notebook generator, runner, and dark-theme figure renderer.

### Radar Physics & DSP Modules
- `src/sim/radar_config.py` — Radar hardware configuration, physical constants, resolution formulas.
- `src/sim/target.py` — Standard traffic scenario, kinematics, and pedestrian micro-Doppler gait parameters.
- `src/sim/radar_sim.py` — 3D FMCW radar cube synthesizer with thermal noise and Rayleigh clutter.
- `src/dsp/range_processing.py` — 1D Range FFT, Hann windowing, spectral leakage suppression.
- `src/dsp/clutter_removal.py` — MTI mean subtraction clutter filter, clutter attenuation metric.
- `src/dsp/doppler_processing.py` — Slow-time 2D Doppler FFT, Range-Doppler Matrix (RDM), STFT micro-Doppler.
- `src/dsp/cfar_detector.py` — 2D CA-CFAR adaptive thresholding, guard cells, training cells, P_fa scaling.
- `src/dsp/aoa_estimation.py` — Spatial array beamforming, Capon MVDR, and super-resolution MUSIC AoA.
- `src/dsp/clustering.py` — DBSCAN multipoint clustering and polar-to-Cartesian BEV conversion.
- `src/dsp/radar_pipeline.py` — End-to-end ClassicalRadarPipeline orchestrator.

### Deep Learning Models
- `src/models/radar_detector_cnn.py` — Multi-task anchor-free CNN architecture, forward pass, and composite loss.
- `src/models/radar_dataset.py` — Synthetic RDM dataset generator with Gaussian heatmap splats and box regressors.

### Verification & Quality Gates
- `tests/test_walkthrough_notebooks.py` — Deterministic test suite verifying notebook integrity and execution.
- `scripts/verify.ps1` — Universal project verification script.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/build_walkthrough_notebooks.py`: Already contains complete code cell definitions, dark theme configuration, and `execute_notebook_in_process` runner. It provides the foundation for injecting the Mermaid blocks and SVG fallbacks.
- `ClassicalRadarPipeline`: Unified pipeline interface connecting all 7 DSP modules with standard dictionary outputs.
- `RadarObjectDetectorCNN`: Clean multi-task PyTorch module with separated `cls_head` and `box_head`.

### Established Patterns
- **Dark Cyber-Radar Theme**: `#0a0e17` background with `#00f0ff` cyan, `#ff0055` red/magenta, `#ffaa00` orange, and `#00ff66` green accents.
- **Fast In-Process Execution**: Using `exec()` inside `execute_notebook_in_process` with Matplotlib `Agg` backend and base64 PNG capture.

### Integration Points
- Section headers in `01_radar_classical_dsp.ipynb`: Sections 1 through 10.
- Section headers in `02_radar_deep_learning_detection.ipynb`: Sections 1 through 5.
- Test runner in `scripts/verify.ps1`: Discovers all tests under `tests/`.

</code_context>

<specifics>
## Specific Ideas

- **Prototype Section Diagram**: Create and validate Section 3 (Fast-Time 1D Range FFT) first to ensure nodes with formulas (`X[k] = \sum w[n]x[n]e^{-j2\pi kn/N}`) and method signatures (`RangeProcessor.process()`) do not suffer from text clipping.
- **Collapsible SVG Syntax**:
  ```html
  <details>
  <summary><i>Click here to expand fallback diagram if the Mermaid graph above does not render in your environment</i></summary>
  <br/>
  <img src="data:image/svg+xml;base64,..." alt="Fallback Diagram"/>
  </details>
  ```
- **Code Parity Invariant**: Maintain Mermaid diagram nodes in 1-to-1 sync with codebase method names.

</specifics>

<deferred>
## Deferred Ideas

- **Deeper Mathematical Proofs**: Multi-page formal derivations and Neyman-Pearson lemma proof boxes deferred until professor explicitly requests them.
- **Speculative Thesis Research Proposals**: Long discussions on Complex-Valued CNNs and 4D Imaging Radar tensors deferred to future research phases.

</deferred>

---

*Phase: 1-Compartmentalized Jupyter Walkthroughs & Mermaid Diagrams*
*Context gathered: 2026-09-23*
