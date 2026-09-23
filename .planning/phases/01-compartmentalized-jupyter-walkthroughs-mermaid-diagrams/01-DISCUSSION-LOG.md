# Phase 1: Compartmentalized Jupyter Walkthroughs & Mermaid Diagrams - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-23
**Phase:** 1-Compartmentalized Jupyter Walkthroughs & Mermaid Diagrams
**Areas discussed:** Mermaid Diagram Rendering & Platform Compatibility, Diagram Topology, Tensor Dimensions & Function Annotations, Academic Presentation Narrative & Theoretical Rigor, Execution Pipeline, Build Automation & Visual Aesthetic

---

## Mermaid Diagram Rendering & Platform Compatibility

### Question 1: How should Mermaid diagrams be embedded and formatted in the walkthrough notebooks (01 and 02)?
| Option | Description | Selected |
|---|---|:---:|
| Native Markdown ```mermaid code blocks with GitHub/VSCode dark theme styling | Renders natively in modern VS Code, JupyterLab 4+, and GitHub without external dependencies. | |
| Dual embedding: Native ```mermaid blocks plus high-resolution SVG fallback cells | Guarantees visual rendering on legacy Jupyter notebook viewers at the expense of notebook size. | ✓ |
| You decide | Choose the most standard, clean approach suitable for academic thesis presentation and code reviews. | |

**User's choice:** Dual embedding: Native ```mermaid blocks plus high-resolution SVG fallback cells, with theme-neutral / standard styling (do not hardcode custom themes or colors in Mermaid syntax).
**Notes:** Ensures clean rendering across all viewers without visual breakage.

### Question 2: Where should the section-level Mermaid diagrams be positioned in each module?
| Option | Description | Selected |
|---|---|:---:|
| Immediately under the section header as a pre-execution visual map | Provides the professor with an immediate mental model of inputs, functions, and outputs before diving into mathematical equations and code. | ✓ |
| At the end of each section as a summary recap | Solidifies understanding after reviewing the mathematical derivations and code output. | |
| You decide | Select the placement that maximizes pedagogical flow during a live academic walkthrough. | |

**User's choice:** Immediately under the section header as a pre-execution visual map.
**Notes:** Establishes mental anchor before seeing code.

### Question 3: How should the dual-embedded Mermaid code and rendered SVG fallback be packaged within the notebook markdown cells?
| Option | Description | Selected |
|---|---|:---:|
| Automated headless rendering via Mermaid CLI/Playwright in the build script with a collapsible <details> block | Keeps the raw Mermaid visible for inspection while embedding the rendered visual cleanly. | ✓ |
| Pure Markdown side-by-side: Native ```mermaid block followed directly by embedded inline SVG | Maximum accessibility across all static document renderers without HTML wrappers. | |
| You decide | Use the cleanest generation method that executes deterministically during scripts/build_walkthrough_notebooks.py. | |

**User's choice:** Collapsible `<details>` block (default collapsed) with message: *"Click here to expand fallback diagram if the Mermaid graph above does not render in your environment"*.
**Notes:** Provides a non-intrusive fallback if Mermaid JS fails to render.

### Question 4: What diagram coverage should be provided across both walkthrough notebooks?
| Option | Description | Selected |
|---|---|:---:|
| Comprehensive coverage: 1 top-level system diagram + 1 dedicated diagram for every substantive technical module | Fully satisfies PRES-01, PRES-02, and PRES-03. | ✓ |
| Selective coverage: Top-level system diagram + diagrams for only complex multi-step stages | Leaves simple steps purely in code and math. | |
| You decide | Optimize diagram granularity so every major data transformation has a visual map without visual redundancy. | |

**User's choice:** Comprehensive coverage: 1 top-level system diagram + 1 dedicated diagram for every substantive technical module.
**Notes:** User emphasized: *"also mention that if there are any changes in the code maintain the graphs as well"*.

---

## Diagram Topology, Tensor Dimensions & Function Annotations

### Question 1: What flowchart direction (TD vs. LR) should be used for the Mermaid diagrams?
| Option | Description | Selected |
|---|---|:---:|
| Top-Down flow (graph TD) throughout | Aligns with vertical notebook scrolling and prevents horizontal truncation on standard laptop screens. | |
| Left-to-Right flow (graph LR) for data transforms | Highlights sequential stage progression horizontally. | |
| Hybrid: Top-Down (graph TD) for end-to-end system flows, and Left-to-Right (graph LR) for compact single-stage input-to-output diagrams | Best of both worlds. | ✓ |
| You decide | Select the orientation that offers the cleanest rendering across various displays. | |

**User's choice:** Hybrid: Top-Down (`graph TD`) for end-to-end system flows, and Left-to-Right (`graph LR`) for compact single-stage input-to-output diagrams.

### Question 2: How should data representations and tensor shapes be annotated on diagram edges and nodes?
| Option | Description | Selected |
|---|---|:---:|
| Combined: Physical name + explicit tensor shape and dtype | Enables tracking both physical intuition and exact array memory layout. | ✓ |
| Physical domain labels only | Keeps diagrams high-level and focused strictly on radar physics. | ✓ |
| Pure array shapes and types on edges | Prioritizes data engineering and programmatic tensor tracking. | |
| You decide | Choose the level of detail that looks most professional for a thesis walkthrough. | |

**User's choice:** Combined: Physical domain name + explicit tensor shape and dtype (both 2 and 3).

### Question 3: How should Python codebase functions and class methods be referenced in the Mermaid operation nodes?
| Option | Description | Selected |
|---|---|:---:|
| Dedicated operation nodes showing exact Python class/method names alongside key parameters | Maps theory directly to codebase files in src/dsp/ and src/models/. | ✓ |
| Subgraphs grouping theoretical operation with Python implementation class side-by-side | Gives the complete dual perspective (math + code). | ✓ |
| High-level conceptual action labels without specific code class names | Keeps nodes abstract. | ✓ |
| You decide | Choose whatever best bridges the radar equations with the Python implementation. | |

**User's choice:** A combination of all three (action label, class/method signature, and key formula).
**Notes:** User specified: *"let us decide how this looks on one of the sections first. but also visually make sure that the text is not overlapping and everything is readable"*.

### Question 4: How should the Deep Learning architecture and multi-task pipeline be structured in notebook 02?
| Option | Description | Selected |
|---|---|:---:|
| Multi-branch architecture flowchart: Input RDM ──► Conv Backbone ──► Fork into Classification Head & Bounding Box Head ──► Join at Multi-Task Loss | Accurately diagrams multi-task learning with Gaussian splats. | ✓ |
| Dual diagram: High-level End-to-End ML Pipeline + Detailed CNN Head Splitting Diagram | Two separate diagrams. | |
| Sequential layer stack: Vertical block diagram detailing kernel sizes, strides, activations | Standard layer-by-layer stack. | |
| You decide | Select the structure that most clearly communicates multi-task learning. | |

**User's choice:** Multi-branch architecture flowchart.

---

## Academic Presentation Narrative & Theoretical Rigor

### Question 1: What level of mathematical and theoretical depth should be included in the markdown narrative?
| Option | Description | Selected |
|---|---|:---:|
| Comprehensive academic rigor: Full mathematical derivations with explicit variable definitions | Heavy multi-step proof boxes. | |
| Applied engineering formulas: Focus strictly on operational radar equations | Clean formulas without proofs. | ✓ |
| Layered pedagogical format: Core operational formula and physical intuition first | Multi-layered format. | |
| You decide | Choose the balance that best satisfies an academic thesis evaluation committee. | |

**User's choice:** Keep the mathematical narrative grounded and practical with operational equations; *"no need for that [heavy theoretical proofs] just yet"*.

### Question 2: Should each section include specific "Academic Discussion & Defense Notes" callouts for the professor walkthrough?
| Option | Description | Selected |
|---|---|:---:|
| Dedicated "Academic Discussion & Defense Notes" callout box in each module | Explicit exam/defense callout boxes. | |
| Inline discussion paragraphs embedded naturally within the narrative without explicit callout boxes | Natural narrative explanations. | ✓ |
| No extra defense callouts | Strictly algorithm description and results. | |
| You decide | Include defense prompts where they add maximum value. | |

**User's choice:** Inline discussion at the end of each section (or wherever fit), modeled as a natural narrative explanation.

### Question 3: How should the Classical DSP vs. Deep Learning comparative analysis and future thesis directions be presented in notebook 02?
| Option | Description | Selected |
|---|---|:---:|
| Comprehensive comparison table + detailed synthesis of hybrid architectures | Detailed springboard for thesis proposal. | |
| Compact summary table only | Focuses strictly on comparing implemented CNN against classical pipeline. | ✓ |
| You decide | Frame comparison to highlight exact gaps where deep learning excels. | |

**User's choice:** Compact summary table only.

### Question 4: How should the Pedestrian Micro-Doppler section (Section 9) connect the classical pipeline to notebook 02?
| Option | Description | Selected |
|---|---|:---:|
| Pedagogical bridge to deep learning: Explain how micro-Doppler STFT signatures extract limb kinematics | Links directly to neural network spectrogram classifiers. | |
| Self-contained radar physics topic: Present micro-Doppler strictly as an advanced kinematic effect | Self-contained. | ✓ |
| You decide | Frame to maximize coherence between the two notebooks. | |

**User's choice:** Self-contained radar physics topic presenting micro-Doppler strictly as an advanced kinematic effect.

---

## Execution Pipeline, Build Automation & Visual Aesthetic

### Question 1: Should scripts/build_walkthrough_notebooks.py remain the single source of truth for constructing both notebooks?
| Option | Description | Selected |
|---|---|:---:|
| scripts/build_walkthrough_notebooks.py as the deterministic single source of truth | Regenerates both notebooks cleanly. | |
| Direct notebook editing | Primary editing on .ipynb files directly in VS Code / Jupyter. | ✓ |
| You decide | Select development workflow that guarantees deterministic execution. | |

**User's choice:** Direct notebook editing if possible, with scripts/build_walkthrough_notebooks.py as a sync/rebuild utility.

### Question 2: Should the notebooks be committed with pre-rendered execution outputs and figures?
| Option | Description | Selected |
|---|---|:---:|
| Pre-rendered and saved in the notebooks | Allows professor to view plots immediately on GitHub/VS Code without executing first. | ✓ |
| Cleared outputs (code & markdown only) | Keeps repository size smaller and git diffs clean. | |
| You decide | Choose best state for academic submission. | |

**User's choice:** Pre-rendered and saved in the notebooks.

### Question 3: What visual styling and color theme should be maintained for the Matplotlib figures?
| Option | Description | Selected |
|---|---|:---:|
| Maintain the Dark Cyber-Radar aesthetic | Distinctive high-contrast tactical display. | ✓ |
| Clean Academic White/Light theme | Traditional publication styling for printed thesis. | |
| Dual-theme toggle variable | Toggle variable in Cell 2. | |
| You decide | Select visual styling that offers highest presentation impact. | |

**User's choice:** Maintain the Dark Cyber-Radar aesthetic.

### Question 4: How should the walkthrough notebooks and Mermaid diagrams be validated in the test suite?
| Option | Description | Selected |
|---|---|:---:|
| Fast deterministic validation test (tests/test_walkthrough_notebooks.py) | Verifies JSON structure and syntax in <2 seconds. | |
| Full end-to-end re-execution test | Re-runs all DSP and CNN training cells on every test execution. | |
| You decide | Implement verification that satisfies deterministic CI gates while maintaining snappy feedback loops. | ✓ |

**User's choice:** Balanced smoke test: *"make sure the code is working. not a full re run is required but not 1 either"*.
**Notes:** Actually executes key DSP and CNN code blocks to confirm no exceptions without running heavy 5-epoch training loops.

---

## the agent's Discretion

- Prototype section diagram: Section 3 (Fast-Time 1D Range FFT) will be created and verified first.
- Collapsible SVG rendering mechanism: Integrated into build script via headless SVG generation.

## Deferred Ideas

- In-depth theoretical proof boxes (Neyman-Pearson lemma, MUSIC asymptotic variance bounds) deferred until specifically requested by the thesis advisor.
- Speculative hybrid architectures (Complex-Valued CNNs, 4D Radar Point Clouds) deferred to future milestone.
