# Radar BTP — Comprehensive Academic Report Revision & Verification

## Role

Act as a senior academic researcher, radar signal-processing specialist, machine-learning researcher, and technical thesis editor.

You are responsible for bringing the current B.Tech Project-I report at IIT Guwahati to a high standard of academic quality, technical accuracy, reproducibility, and presentation.

The project is titled:

**AI Applications in Radar Signal Processing**

_Towards Resource-Efficient AI-Based Radar Detection for Millimetre-Wave FMCW Systems_

Your task is to examine the existing report, recover valuable content from the original draft, verify every technical and experimental claim against the actual repository, and implement the necessary improvements.

This is not merely a proofreading task. It is an academic and technical audit followed by a carefully controlled revision.

---

# PART 1 — UNDERSTAND THE REPOSITORY BEFORE EDITING

## 1.1 Identify the report versions

The repository contains two versions of the report:

- **New section:** The current five-chapter report intended for the final BTP report.
- **Old section:** The original seven-chapter report preserved below the new section as reference material.

The new report is the authoritative manuscript.

The old report is a source of potentially useful mathematical derivations, technical discussions, research comparisons, experimental explanations, figures, and planning material.

Inspect both completely before making changes.

Primary report file:

`docs/index.html`

Also inspect:

- `docs/app.js`
- `docs/styles.css`
- `docs/ADVISOR-DEFENSE.md`
- `WORKING.md`
- `AGENTS.md`
- Relevant files in `.planning/`
- `src/sim/`
- `src/dsp/`
- `src/models/`
- `src/raddet/`
- `notebooks/`
- `data/benchmark_results/`
- Relevant Kaggle notebooks and output artifacts
- `tests/`
- `templates/BTP_Report_Template_Overleaf/`

Do not base decisions on `docs/index.html` alone.

## 1.2 Understand what was actually implemented

Trace the technical claims in the report to their corresponding source code, notebooks, execution logs, experiment configurations, and results.

For important experiments, establish:

1. What was implemented?
2. What was actually executed?
3. What data were used?
4. What configurations were used?
5. What results were obtained?
6. Where are the supporting artifacts?
7. What limitations or errors occurred?
8. What remains incomplete?

Use Git history, branches, commits, Kaggle notebook versions, logs, checkpoint metadata, CSV files, and other available evidence where necessary.

**Important verification rule:**

The absence of an artifact in one repository location does not establish that an experiment was never conducted.

Likewise, the presence of a planned implementation, a code definition, a research proposal, or an anticipated result does not establish that the experiment was successfully executed.

When an experiment or result cannot be verified:

- Investigate other available sources.
- Record the available evidence.
- Determine exactly what remains uncertain.
- Do not assume either success or failure.
- Do not invent missing details.
- Do not silently remove the relevant discussion.
- Use appropriately qualified wording in the report.

For example:

If an experiment was conducted but its full execution log is unavailable, report the result only to the extent that the remaining evidence supports it, and document the reproducibility limitation.

If an experiment was planned but never executed, identify it as proposed future work.

If an experiment was executed and failed, document what happened, the observed failure, and its implications.

The report must describe the actual project history, not the idealised version of what the project was supposed to achieve.

Note:-  
you can also go through the previous context as wel in gsd to take care of few of the things. use subagents if necessary.

---

# PART 2 — RECOVER AND INTEGRATE VALUABLE CONTENT FROM THE OLD REPORT

Do not copy the original seven chapters wholesale.

Extract only material that genuinely improves the new five-chapter report.

## 2.1 Original Chapter 1 — Introduction and Research Motivation

Recover useful material concerning:

- Motivation for AI-based radar processing.
- Limitations of conventional radar processing.
- The importance of computational efficiency.
- The original research motivation and project evolution.

Integrate relevant material into the new Chapter 1.

Avoid historical details that do not contribute to the academic argument.

Do not introduce unsupported statements such as claims that conventional radar universally discards more than 90% of raw signal information.

## 2.2 Original Chapter 2 — FMCW Radar Mathematical Physics

This is an important section that should be substantially recovered.

Add an appropriate subsection to the new Chapter 2 covering:

1. FMCW chirp generation.
2. Transmitted signal equation.
3. Received signal and round-trip delay.
4. Dechirping and beat-frequency derivation.
5. Range estimation.
6. Doppler frequency and velocity estimation.
7. Range resolution.
8. Velocity resolution.
9. Uniform Linear Array geometry.
10. Angle-of-arrival estimation.
11. Maximum unambiguous range and velocity.

Derive the mathematics step by step and explain the physical meaning of the variables.

Use the current simulator configuration as the authoritative reference unless another configuration is explicitly identified as belonging to a separate experiment.

Current values in `src/sim/radar_config.py` include:

- Carrier frequency: 77 GHz.
- Chirp bandwidth: 1 GHz.
- Chirp duration: 50 μs.
- ADC samples: 256.
- Chirps per frame: 128.
- Receive antennas: 4.
- Antenna spacing: half-wavelength.
- ADC sampling frequency: 5.12 MHz.

For this configuration, the expected theoretical quantities are approximately:

- Wavelength: 3.893 mm.
- Chirp slope: 20 × 10¹² Hz/s.
- Range resolution: 0.15 m.
- Velocity resolution: 0.304 m/s, subject to the assumed chirp repetition interval.
- Maximum unambiguous range: approximately 38.4 m under the configured sampling and slope assumptions.

Recalculate these quantities independently.

**Do not carry forward the old 58.8 μs chirp duration, 0.258 m/s velocity resolution, or inconsistent angular-aperture calculations without justification.**

Explicitly distinguish active chirp duration from chirp repetition interval if idle time is present or assumed.

Do not claim that the CNN achieves sub-Rayleigh target resolution unless a dedicated experiment demonstrates it using a defensible resolution criterion, appropriate ground truth, and quantitative evaluation.

## 2.3 Original Chapter 3 — Classical DSP Baseline

Recover the useful theoretical explanation of:

- Range FFT.
- Windowing and spectral leakage.
- MTI and mean-subtraction clutter suppression.
- Doppler FFT.
- CA-CFAR and OS-CFAR.
- MUSIC and Capon/MVDR.
- DBSCAN clustering.

Create a comparison table showing the purpose, operating principle, assumptions, and limitations of the methods.

Distinguish theoretical explanations from actual project implementations.

Important implementation checks:

- The dataset-generation pipeline uses mean-subtraction clutter filtering by default. Do not describe it as a two-pulse MTI experiment unless that operation was actually used.
- Inspect the implementation of CA-CFAR, OS-CFAR, GOCA-CFAR and SOCA-CFAR.
- The current OS-CFAR implementation appears to use the CA-CFAR threshold factor. Verify this, investigate whether the configuration was used experimentally, and either correct and test it or restrict the claims to what is validated.
- Ensure CFAR threshold equations state the appropriate statistical assumptions for linear power samples, rather than confusing Rayleigh-distributed amplitudes with exponentially distributed square-law noise power.
- Do not present MUSIC or Capon outputs as validated angular accuracy measurements if target association was incorrect.

Where implementation defects exist, determine their effect on reported results before correcting or changing the report.

## 2.4 Original Chapter 4 — Literature and Adaptive Computation

Recover:

- The useful research-gap discussion.
- The seven-axis literature comparison.
- The computational-efficiency methodology.
- Knowledge distillation, quantisation, pruning, lightweight architectures, and adaptive computation.
- Relevant adaptive radar research.

Create a rigorous literature comparison table using dimensions such as:

- Input representation.
- Radar application/task.
- Dataset.
- Model architecture.
- Computational strategy.
- Hardware evaluation.
- Reported performance.
- Limitations.

Include RAVEN and AdaRadar only after independently verifying their publications, technical descriptions, and bibliographic details.

Do not repeat the old claim that AdaRadar adapts transmitter chirp duration unless the actual paper supports that description.

Do not populate comparisons with invented latency, accuracy, or computational values.

Use "Not reported" or "Not evaluated" wherever necessary.

## 2.5 Original Chapter 5 — Empirical Results

Recover the useful structure of the experimental comparison tables and result interpretation.

Do not copy numerical findings blindly.

Every experimental figure, number, and interpretation must pass the evidence-verification procedure in Part 3.

## 2.6 Original Chapter 6 — Timeline and Risk Assessment

Recover the useful BTP-1/BTP-2 milestones and technical risks.

Preserve the useful project timeline and Gantt-chart material, subject to verifying the actual dates and project requirements.

Do not automatically introduce an additional chapter if the final report is intended to have five chapters.

Determine the most appropriate placement for the Gantt schedule, preferably within a relevant project-planning or future-work subsection, or an appendix if appropriate.

Accurately distinguish completed milestones from planned milestones.

The existing August 2026–May 2027 schedule spans ten calendar months, not twelve. Do not call it a twelve-month schedule unless the timeline is genuinely extended.

Recover relevant risks, including:

- Limited synthetic-to-real generalisation.
- Limited training data.
- Incorrect target association.
- CPU inference bottlenecks.
- Quantisation-related accuracy loss.
- Multi-resolution feature misalignment.
- Adaptive-routing overhead.
- Hardware and deployment constraints.

## 2.7 Original Chapter 7 — Conclusions

Use this chapter only as a source of useful context.

Do not carry forward unsupported conclusions, exaggerated contributions, or duplicated summaries.

The new Chapter 5 should remain authoritative.

---

# PART 3 — EXPERIMENTAL AND TECHNICAL VERIFICATION

This is the most important part of the task.

Before changing numerical claims, inspect the actual underlying experiments.

## 3.1 RadDet dataset identity and description

The RadDet dataset represents wideband radar-spectrum detection and radar-emission classification using time-frequency spectrograms.

It is not an automotive road-scene dataset containing physical vehicle and pedestrian radar captures.

Correct every misleading description across all five chapters.

Use terminology that accurately describes:

- Wideband RF radar-spectrum detection.
- Radar-emission localisation.
- Modulation classification.
- Time-frequency spectrograms.
- SNR-dependent detection performance.

Maintain a clear distinction between:

**Track I:** Synthetic 77 GHz FMCW automotive spatial-target perception.

**Track II:** Wideband RadDet spectrum detection and modulation classification.

They may contribute to a broader investigation of AI-based radar processing and computation, but their results must not be treated as interchangeable.

Check the original RadDet publication and the actual dataset documentation.

## 3.2 Resolve the dataset split discrepancy

Investigate the following conflicting records:

The original RadDet documentation describes:

- Training: 20,000 frames.
- Validation: 14,000 frames.
- Test: 6,000 frames.
- Total: 40,000 frames.

The current benchmark summary reports:

- Training: 14,001 frames.
- Validation: 6,001 frames.
- Test: 20,001 frames.
- Total: 40,003 frames.

The old benchmark planning documentation also describes the original 20,000/14,000/6,000 partition.

Determine what actually happened.

Inspect:

- Dataset extraction scripts.
- Dataset directory contents, where accessible.
- Notebook split logic.
- YAML configuration files.
- Training and testing logs.
- Evaluation scripts.
- SNR metadata.
- Git history and archived experiment records.

Establish whether:

1. The official partitions were used.
2. The dataset was re-partitioned.
3. A custom split was created.
4. The reported counts refer to a different evaluation run.
5. The discrepancy arose from an error in documentation or counting.

Also resolve the six-SNR-bin inconsistency: six bins containing 3,333 frames each account for 19,998 frames, not 20,001.

Do not force the results to match the original paper's partition merely to make the report look consistent.

Describe the actual split, justify any custom partition, disclose any deviation from the original benchmark, and correct all tables and statements accordingly.

If the original run cannot be reconstructed, document the discrepancy and the evidence limitation explicitly.

## 3.3 Verify the benchmark reproduction claim

The project reports:

- YOLOv9-C.
- 25.30 million parameters.
- 25.25% mAP@0.5.
- 19.03% mAP@0.5:0.95.
- 892.9 FPS.
- NVIDIA Tesla T4 GPU.

The published RadDet result being used for comparison reports:

- YOLOv9-M.
- 20.02 million parameters.
- 25.93% mAP@0.5.
- 19.47% mAP@0.5:0.95.
- 896.6 FPS.

Verify both sources and the actual project run.

Investigate differences in:

- Model architecture and size.
- Dataset partition.
- Training duration.
- Pretrained initialisation.
- Input resolution.
- Optimiser.
- Augmentations.
- Precision.
- Evaluation method.
- Hardware.

Unless the relevant experimental conditions are sufficiently aligned, describe the result as a comparative benchmark against published RadDet results, rather than an exact reproduction.

Do not call a numerically similar result an exact reproduction simply because its metrics are close.

Verify whether YOLOv8-M was actually trained by the project or was taken from an external source. Do not attribute it to the RadDet paper's Table III if it is not included there.

include the relevant graphs that are there in the github pages as well.

## 3.4 Resolve the YOLOv9-C experiment evidence

The report describes a 66-epoch full-scale YOLOv9-C experiment.

Investigate the actual evidence for this run.

The tracked prototype notebook and `data/kaggle_outputs/runs/raddet_yolo/args.yaml` appear to describe a different YOLOv8n, 15-epoch configuration.

This discrepancy must be investigated without assuming that the full YOLOv9-C experiment did or did not happen.

Search:

- Kaggle notebooks and their saved versions.
- Execution configurations.
- Git commits and branches.
- Model checkpoint metadata.
- Benchmark CSV files.
- Run-specific logs.
- Uploaded or archived outputs.
- External artifact references already documented in the repository.

Establish the connection between the reported numbers and the exact experiment that generated them.

If the full-scale run is verified, document its actual configuration and connect the report to the corresponding artifacts.

If the run happened but some artifacts are unavailable, describe the verified evidence and acknowledge the reproducibility limitation.

If it was not executed, clearly distinguish the completed prototype from the planned experiment and remove any unsupported full-scale claims.

Do not fabricate logs, checkpoints, configurations, or results.

## 3.5 Resolve the synthetic FMCW CNN dataset discrepancy

The current training utility defaults to:

- 150 generated samples.
- 80% training split.
- 20% validation split.
- Five epochs.
- Batch size eight.
- AdamW.

The results and conclusion sections also refer to a 32-sample experiment.

Determine which configuration was actually used for the reported 136,041-parameter CNN result and 26.89-second training duration.

Inspect the executed notebook, experiment output and model checkpoint.

Correct every reference to the sample count, split, execution time, training configuration and validation loss.

Do not assume that the utility's default values equal the values used during the actual run.

## 3.6 Verify the clutter attenuation result

The report gives a 12.94 dB clutter-attenuation result.

Inspect `src/dsp/clutter_removal.py` and the experiment that generated this result.

The current utility calculates the ratio of total average power before and after filtering.

Determine whether the measurement represents:

- Actual clutter attenuation.
- Overall signal-power attenuation.
- Zero-Doppler suppression.
- Another quantity.

Use a metric name and explanation that accurately reflect the calculation.

If the experiment does not isolate clutter power, do not claim that the result measures pure clutter suppression.

## 3.7 Verify angle-estimation results

Inspect:

- `src/dsp/aoa_estimation.py`
- `src/dsp/radar_pipeline.py`
- The relevant notebooks.
- The target association procedure.
- Experimental outputs.

The report already identifies a possible range-only association problem.

Verify what happened, its effect on the angular estimates, and whether any correction was implemented.

Distinguish:

- Angular search-grid spacing.
- Physical array beamwidth.
- Angular resolution.
- Angular estimation error.

Do not equate the 180-point angular search grid with one-degree physical radar resolution.

## 3.8 Correct implementation descriptions

Audit the simulator and processing code against the report.

In particular:

- The current simulator uses Rayleigh-distributed stationary clutter amplitudes and additive complex Gaussian noise.
- The current CNN data-generation pipeline uses mean subtraction.
- Proposed Weibull or compound K-distributed clutter should not be described as implemented unless verified.
- Antenna coupling and other advanced physical models must not be claimed unless verified.
- Proposed quantisation, pruning, distillation and adaptive computation must remain proposed unless experiments demonstrate otherwise.

For every relevant method, identify whether it is:

1. Implemented.
2. Executed.
3. Experimentally evaluated.
4. Proposed for future work.

These categories must not be conflated.

---

# PART 4 — IMPROVE THE NEW FIVE-CHAPTER REPORT

Maintain the five-chapter structure.

Do not create unnecessary additional chapters.

## Chapter 1 — Introduction

Improve the problem formulation and academic motivation.

Add a focused research-question subsection aligned with the actual experiments.

Suggested questions:

1. How effectively can a conventional processing pipeline recover target properties under controlled synthetic FMCW conditions?
2. What can a compact CNN learn from synthetic Range-Doppler representations, and what limits its current evaluation?
3. How does YOLO-based radar-spectrum detection perform on the RadDet benchmark under different SNR conditions?
4. What computational baselines have been established, and which resource-efficiency questions remain unresolved?

Clearly separate completed BTP-I work from proposed BTP-II research.

Remove repetition and broad unsupported statements.

Clarify why the two experimental tracks belong in the same project while explaining their different sensing objectives.

Maintain the approved project title unless there is a genuine institutional or supervisor-approved reason to change it.

## Chapter 2 — Literature Review

Strengthen this chapter with:

- FMCW mathematical foundations.
- Classical DSP theory.
- Critical comparison of traditional and learning-based approaches.
- Radar dataset comparison.
- Efficient and edge-oriented radar AI literature.
- The seven-axis research-gap matrix.
- A concise synthesis identifying the specific project gap.

Use appropriate primary academic references.

Do not turn the literature review into a collection of disconnected paper summaries.

Compare approaches critically and explain their relevance to the project.

## Chapter 3 — Methodology

Strengthen the technical reproducibility of this chapter.

Include:

**FMCW experimental configuration**

A definitive table with carrier frequency, bandwidth, chirp duration, sampling frequency, samples, chirps, receive antennas and antenna spacing.

**DSP methodology**

Explain the actual processing sequence and the exact variants executed.

**Synthetic CNN**

Explain:

- Dataset generation.
- Input representation.
- Target annotation.
- Architecture.
- Loss function.
- Training procedure.
- Validation procedure.

**RadDet experiment**

Explain:

- Dataset source and variant.
- Actual dataset split.
- Preprocessing.
- Class mapping.
- YOLO architecture and model size.
- Training configuration.
- Augmentation.
- SNR evaluation.
- Benchmark methodology.

**Resource-efficiency methodology**

Explain the planned comparison of:

- Parameters.
- FLOPs/MACs.
- Model size.
- Latency.
- Throughput.
- RAM/VRAM.
- Energy where available.
- CPU versus GPU execution.

Do not present proposed optimisations as completed work.

## Chapter 4 — Experimental Results and Analysis

This chapter must distinguish verified results from incomplete experiments.

Use separate sections for synthetic FMCW and RadDet.

For synthetic FMCW, include actual:

- Range and velocity recovery.
- Detection performance.
- Ground-truth comparisons.
- False alarms.
- Clutter-filter observations.
- Angle-estimation limitations.
- CNN evaluation and its limitations.

For RadDet, include verified:

- Training and validation metrics.
- Test-set performance.
- Per-SNR performance.
- Per-class performance.
- Confusion matrix.
- Precision-recall curves.
- Qualitative predictions.
- Published benchmark comparison.

For resource efficiency, distinguish measured quantities from those not yet evaluated.

Always identify the hardware, software, precision, batch size and measurement protocol associated with latency measurements.

Do not use GPU measurements as evidence of CPU or automotive ECU performance.

Separate isolated model inference latency from end-to-end processing latency.

Do not infer model superiority from training loss or parameter count alone.

## Chapter 5 — Conclusion and Future Work

Preserve the objective-achievement table and the honest discussion of limitations.

Reduce repeated findings and duplicated conclusions.

Use a concise structure:

1. Summary of work.
2. Achievement of objectives.
3. Main experimental findings.
4. Limitations and threats to validity.
5. Future work.
6. Brief conclusion.

Include the project timeline and Gantt schedule at the most appropriate location, if required by the approved BTP format.

Recover the useful technical risk register from the old chapter.

Clearly identify the BTP-II deliverables as future work.

---

# PART 5 — REFERENCES AND CITATION AUDIT

The current report uses numerical, IEEE-like references.

Perform a complete bibliography and in-text citation audit.

## 5.1 Verify each source

For every source, verify:

- Authors.
- Exact title.
- Publication year.
- Journal or conference.
- Volume and issue.
- Page numbers.
- DOI or official permanent URL.
- Publication status.

Prefer:

1. Original research publications.
2. Official conference and journal records.
3. Official dataset documentation.
4. Reputable institutional research sources.
5. Secondary surveys where appropriate.

Do not invent DOIs or use generic placeholder links.

Resolve discrepancies involving:

- RadDet.
- Skolnik's edition and publication year.
- TJ4DRadSet.
- TransRAD.
- RAVEN.
- AdaRadar.
- The other references currently present in the bibliography.

The new and old manuscript versions currently contain inconsistent citation metadata for some of these works.

## 5.2 Synchronise HTML and JavaScript citations

Audit:

- `docs/index.html`
- `docs/app.js`

The formal bibliography and citation-tooltip database must represent the same source records.

Verify:

- Every in-text reference points to the correct bibliography item.
- Citation popovers show the correct authors, title, year and publication.
- No placeholder DOI is displayed.
- No citation references a missing bibliography entry.
- The declared bibliography count is correct.

Preserve existing IDs where necessary to avoid breaking the archived old section.

## 5.3 Unused references

The new five-chapter manuscript uses fewer references than the full bibliography.

Do not blindly delete references that are still required by the archived old section.

Instead:

- Establish which references are required by the final five-chapter manuscript.
- Establish which are used only in the archived original manuscript.
- Keep archival references separate where appropriate.
- Ensure the final submitted report contains only the bibliography required by its retained content.

Follow IEEE numerical citation conventions: references should be numbered by first appearance in the final manuscript.

change the bibliography to hold for only the new references and add the old references in a new section in the bibliography itself with a horizontal line distinguishing.

---

# PART 6 — FORMAL BTP REPORT REQUIREMENTS

Make changes only to the content On Github pages And not to the actual Pdf or latex report that needs to be generated. The goal currently is to finalise the content using the Github pages And then later on we will move on to Creating the actual latex report.

---

# PART 7 — ACADEMIC INTEGRITY AND WRITING RULES

These rules are mandatory throughout the revision.

1. Never fabricate an experiment, result, metric, citation, publication, dataset property, or hardware specification.
2. Never claim that a planned method was implemented or evaluated unless evidence supports it.
3. Never silently discard a failed experiment if it is important to understanding the actual research process.
4. Never describe a generated dataset as physical real-world measurements.
5. Never claim exact benchmark reproduction when the experimental conditions differ.
6. Never state that a model is real-time on an edge device based solely on datacenter GPU measurements.
7. Never present a theoretical resolution limit as a measured result.
8. Never retain an incorrect equation merely because it appears in the original draft.
9. Never overstate the significance of small synthetic experiments.
10. Never pad the report with repeated explanations or irrelevant historical material.

Use formal academic English.

Avoid marketing language such as:

- Revolutionary.
- Unprecedented.
- Catastrophic.
- Guaranteed.
- Mathematically impossible.

Prefer measured, technically precise statements.

Clearly distinguish:

- Established theory.
- Findings from published literature.
- Implemented methodology.
- Experimentally observed results.
- Interpretation.
- Limitations.
- Proposed future work.

---

# PART 8 — IMPLEMENTATION AND VALIDATION WORKFLOW

Carry out the work in this sequence.

### Stage 1: Repository and evidence audit

Inspect both report versions and relevant technical artifacts.

Produce an internal claim-to-evidence mapping.

Before editing, identify all material discrepancies and determine which can be resolved from existing evidence.

### Stage 2: Technical corrections

Resolve the FMCW equations, implementation descriptions, experimental configurations, dataset description, data splits, benchmark comparisons, and reported metrics.

Investigate uncertain experimental history instead of assuming what happened.

### Stage 3: Content integration

Bring suitable material from the old report into the new five chapters.

Remove repetitive, exaggerated or irrelevant content from the new manuscript.

Keep the original seven-chapter section preserved as archival material. Do not unnecessarily modify or delete it.

### Stage 4: Citation and bibliography audit

Correct reference metadata and synchronise citation numbering, HTML anchors and JavaScript citation tooltips.

Preserve archival links where required.

### Stage 5: Academic report formatting

Improve the manuscript's structure, mathematical presentation, figure captions, tables, nomenclature, references and front matter.

Do not silently alter the approved report title or supervisor information.

### Stage 6: Validation

Run the relevant existing tests.

At minimum, inspect and execute the available website tests and other relevant deterministic checks.

Validate:

- Mathematical consistency.
- Citation links.
- HTML navigation.
- Figures and tables.
- KaTeX equation rendering.
- Responsive and print styling.
- LaTeX compilation, if the PDF source has been modified.

Do not claim that a test passed unless it was actually executed.

If a check cannot be performed, record the reason.

### Stage 7: Git and deployment considerations

Do not overwrite or discard unrelated work.

---

# PART 9 — FINAL DELIVERABLES

Complete the repository changes and provide a final revision report containing:

## A. Changes implemented

List the exact chapters, subsections, equations, figures, tables, references and formatting that were modified.

## B. Material recovered from the old report

Identify what was retained, where it was integrated, and why.

## C. Experimental verification findings

For each disputed experiment, state:

- What actually happened.
- What evidence was located.
- Which configuration was used.
- Which results are verified.
- Which details remain unverified.
- How the final report describes the experiment.

Do not hide unresolved discrepancies. store it in somewhere in the files in gsd for the current phase.

## D. Technical corrections

List the equations, implementation descriptions, dataset details and claims that were corrected.

## E. Reference audit

Report:

- Number of references retained.
- References added.
- References removed from the final manuscript.
- Metadata corrections.
- Unresolved source-verification issues.

## F. Formatting and academic improvements

Explain the final structure, front matter, nomenclature, figures, tables, bibliography and appendices.

## G. Validation report

Provide actual test results, LaTeX compilation status and any remaining failures.

## H. Outstanding items requiring human confirmation

Create a separate list of questions that genuinely require confirmation from the student, supervisor, or laboratory.

Examples include:

- Was a particular Kaggle experiment actually executed?
- Which checkpoint corresponds to the reported metrics?
- Was the dataset re-partitioned intentionally?
- Which experimental run should be considered authoritative?
- What hardware is available for the next-stage demonstration?
- Does the School require a specific certificate or declaration format?
- Is the current project title the formally approved title?

For every such item:

1. Explain why confirmation is necessary.
2. State the available evidence.
3. State what remains uncertain.
4. Recommend the exact information or artifact needed.

Do not make an assumption just to complete the report.

If a question can be resolved by examining available repository evidence, resolve it yourself rather than asking unnecessarily.

---

# FINAL STANDARD

The objective is to produce an academically credible B.Tech Project report, not simply a longer or more visually impressive manuscript.

The finished report must be:

- Technically correct.
- Experimentally honest.
- Properly referenced.
- Reproducible to the extent permitted by the available artifacts.
- Logically structured.
- Consistent with the actual implementation.
- Appropriate for an IIT Guwahati BTP submission.
- Clear about the distinction between completed BTP-I contributions and proposed BTP-II research.

**Prioritise correctness and evidence over impressive claims. Preserve valid original work, improve weak explanations, and never fill an evidentiary gap with an assumption.**

Execute the revisions, validate the result, and report all completed and outstanding work explicitly.
