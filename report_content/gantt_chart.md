# Agent Instructions — Integrate the 1-Year Gantt Chart into Chapter 5

## Critical instructions

Create a month-level Gantt chart using the timeline specified in the existing source:

**Chapter 6: Project Timeline, 1-Year Gantt Schedule & Risk Audit**

However, the chart must be integrated into the new five-chapter academic report. Do not add a standalone Chapter 6 to the new report.

**Do not rewrite, paraphrase, delete, or restructure any of the existing Chapter 1–5 content.** The only addition to the report should be the Gantt figure, its caption, and the necessary figure-insertion instruction.

## 1. Exact placement in the new report

Insert the Gantt chart in:

- **Chapter:** 5 — Conclusion and Future Work
- **Section:** 5.5 — Future Work
- **Position:** Immediately after the discussion of the proposed BTP-2 research directions and before Section 5.6 — Requirements for Next-Stage Demonstration.

The chart should provide a visual summary of the transition from completed BTP-1 activities to the proposed BTP-2 schedule.

Do not place it in Chapter 4, because Chapter 4 is reserved for experimental results and their discussion.

Do not create a new chapter or modify the existing chapter numbering.

## 2. Figure numbering and caption

Use the next available figure number in Chapter 5. If no earlier Chapter 5 figure exists, use:

**Figure 5.1: One-Year Academic Gantt Schedule for BTP-1 and Proposed BTP-2 Activities (August 2026 – May 2027).**

Caption:

_Month-level Gantt schedule showing the completed BTP-1 milestones from August to November 2026 and the proposed BTP-2 research and implementation activities from January to May 2027. December 2026 is shown without a scheduled milestone because none is specified in the current plan._

## 3. Timeline source and activities

Use the milestone descriptions from the existing Chapter 6 source. Preserve their intended meaning and do not introduce additional activities.

<table>
  <tr><th>Phase</th><th>Month</th><th>Activity</th></tr>
  <tr><td>BTP-1 — Completed</td><td>August 2026</td><td>Academic inception, radar literature study, MATLAB Radar Designer prototyping, FMCW chirp synthesis and link-budget analysis</td></tr>
  <tr><td>BTP-1 — Completed</td><td>September 2026</td><td>77 GHz FMCW simulation and classical DSP pipeline: Range FFT, MTI, Doppler FFT, CFAR, MUSIC and DBSCAN</td></tr>
  <tr><td>BTP-1 — Completed</td><td>October 2026</td><td>PyTorch radar CNN, synthetic dataset generation and multi-task loss convergence experiments</td></tr>
  <tr><td>BTP-1 — Completed</td><td>November 2026</td><td>RadDet benchmark ingestion and full-scale GPU evaluation across approximately 40,000 frames and six SNR tiers; BTP-1 final presentation and oral defense on 23 November 2026</td></tr>
  <tr><td>BTP-2 — Proposed</td><td>January 2027</td><td>Automated MATLAB synthetic data-cube generation under non-Gaussian clutter; prototype cascaded multi-resolution triage (128² → 256² → 512²) with entropy-gated routing</td></tr>
  <tr><td>BTP-2 — Proposed</td><td>February 2027</td><td>Cross-resolution knowledge distillation from a 512² teacher to a compact 128² student and dynamic layer early-exit mechanisms</td></tr>
  <tr><td>BTP-2 — Proposed</td><td>March 2027</td><td>CPU-first INT8 quantisation, OpenVINO / ONNX Runtime CPU profiling, and accuracy–latency–memory Pareto analysis</td></tr>
  <tr><td>BTP-2 — Proposed</td><td>April 2027</td><td>IEEE conference/journal paper submission and conditional laboratory software-defined radar (SDR) hardware exploration</td></tr>
  <tr><td>BTP-2 — Proposed</td><td>May 2027</td><td>Comprehensive B.Tech thesis manuscript submission and oral viva voce defense</td></tr>
</table>

## 4. Visual requirements

Create a proper horizontal Gantt chart.

- Horizontal axis: August 2026 to May 2027, with each month displayed separately.
- Vertical axis: the nine activities listed above.
- Group the rows into BTP-1 — Completed and BTP-2 — Proposed.
- Clearly distinguish completed and proposed work using separate colours and a legend.
- Include a milestone marker for 23 November 2026.
- Mark April 2027 SDR exploration as conditional.
- Show December 2026 as an unassigned month. Do not invent a milestone for it.
- Do not invent exact task start dates, end dates, completion percentages, or durations within a month.

Use a clean, publication-quality academic style. The chart must remain readable when printed at approximately full text width in the report.

## 5. Source files and output files

Create a reproducible chart-generation script:

`scripts/generate_timeline_gantt.py`

Generate:

- `docs/assets/diagrams/timeline_gantt.svg`
- `templates/BTP_Report_Template_Overleaf/figures/timeline_gantt.pdf`

A PNG preview may also be generated for inspection.

Keep the generation source and timeline data together so that the figure can be regenerated without manually editing SVG coordinates.

## 6. Integration into the two report formats

**Overleaf / LaTeX**

Insert the figure at the specified position in Section 5.5 using `\includegraphics`, preferably at approximately `0.95\textwidth` or `\textwidth`.

Use a standard `figure` environment with a centred image, caption and label. Ensure the figure does not float past Section 5.6.

**Academic website**

Insert the SVG at the same logical position in Chapter 5. Preserve the existing figure-card styling, responsive layout and image zoom behaviour.

## 7. Validation

Verify that:

1. The chart is located in Chapter 5, Section 5.5.
2. It appears before Section 5.6.
3. All nine activities appear in the correct month.
4. Completed BTP-1 and proposed BTP-2 activities are clearly distinguished.
5. The 23 November 2026 milestone is visible.
6. April's SDR activity is marked conditional.
7. December is shown without an invented milestone.
8. No existing Chapter 1–5 prose has been modified.
9. The chart renders correctly in both Overleaf and the academic website.
10. Figure numbering and cross-references are consistent.

Do not add a standalone Chapter 6 to the new five-chapter report. Do not alter the source Chapter 6 content. Do not commit or push changes unless separately instructed.

Return the chart preview, generated files and a brief integration summary.
