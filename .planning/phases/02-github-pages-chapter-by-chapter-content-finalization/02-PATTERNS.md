# Phase 02: GitHub Pages Chapter-by-Chapter Content Finalization - Pattern Map

**Mapped:** 2026-11-18  
**Files analyzed:** 4  
**Analogs found:** 4 / 4 (100% coverage)  

This document catalogs existing code and document patterns within the repository to guide the authoring of Plan 02-08 (Repository Evidence Audit & Mathematical Physics Recovery) and Plan 02-09 (HTML Content Integration, Citation Renumbering & Deterministic Verification). All analog sources are strictly verified git-tracked files.

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `.planning/phases/02-github-pages-chapter-by-chapter-content-finalization/02-EVIDENCE-AUDIT.md` | documentation | file-I/O (batch report) | `data/benchmark_results/s128_full/COMPARATIVE_BENCHMARK_REPORT.md` (secondary: `docs/ADVISOR-DEFENSE.md`) | role-match (tracked) |
| `docs/index.html` | component / view | request-response (DOM) | `docs/index.html` (existing sections, tables, math blocks, and bibliography) | exact (self-analog) |
| `docs/app.js` | component / controller | event-driven (client DOM) | `docs/app.js` (`CITATIONS_DB` and `initCitationTooltips`) | exact (self-analog) |
| `tests/test_academic_website.py` | test | batch / file-I/O | `tests/test_academic_website.py` (DOM parsing & chapter assertions) | exact (self-analog) |

---

## Pattern Assignments

### 1. `.planning/phases/02-github-pages-chapter-by-chapter-content-finalization/02-EVIDENCE-AUDIT.md` (documentation, file-I/O)

**Role:** Forensic Technical Audit Dossier / Evidence Catalog  
**Data Flow:** File I/O batch synthesis (reads logs, checkpoints, code constants; writes structured markdown report)  
**Primary Analog:** `data/benchmark_results/s128_full/COMPARATIVE_BENCHMARK_REPORT.md`  
**Secondary Analog:** `docs/ADVISOR-DEFENSE.md`  

#### Imports / Metadata Block Pattern
*From `data/benchmark_results/s128_full/COMPARATIVE_BENCHMARK_REPORT.md:1-10`:*
```markdown
# RadDet-9T (S-128) Radar Spectrum Detection Benchmark
## Full-Scale Benchmark Run vs. Small Prototype Run — Comparative Report

> **Target Paper Reference**: *ICASSP 2025 Table III: Spectrum-based Radar Target Detection Benchmark*  
> **Evaluated Model**: Ultralytics YOLOv9-C (GELAN-C, 25.30M parameters)  
> **Dataset**: RadDet-9T $S=128\times 128$ Range-Doppler / Azimuth Spectral Cube (40,003 frames across 11 classes)  
> **Compute Platform**: NVIDIA Tesla T4 GPU (14.56 GB VRAM), CUDA 12.8, PyTorch 2.11.0  
> **Kaggle Kernel Execution**: `aryanguptaji/raddet-s-128-full-scale-benchmark` (`KernelWorkerStatus.COMPLETE`)
```
**Application to `02-EVIDENCE-AUDIT.md`:** Open the dossier with an authoritative header block declaring the audit date, auditor role, scope boundaries, git commit SHA, and formal reference to `02-SPEC.md` requirements R1–R6.

#### Comparative Benchmark Table & Delta Pattern
*From `data/benchmark_results/s128_full/COMPARATIVE_BENCHMARK_REPORT.md:30-42`:*
```markdown
| Model | Variant Size | Parameters (M) | RadDet-9T $\text{mAP}_{50}$ (%) | RadDet-9T $\text{mAP}_{50:95}$ (%) | $\text{FPS}_{\text{avg}}$ (Tesla T4) | Target Baseline / Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **YOLOv9-M** | S ($128^2$) | 20.02 | **25.93%** | **19.47%** | 896.6 FPS | ICASSP 2025 Table III SOTA |
| **YOLOv9-C (Ours — Full Run)** | S ($128^2$) | 25.30 | **25.25%** | **19.03%** | **892.9 FPS** | **Reproduced On Kaggle GPU** |
| **YOLOv8-M** | S ($128^2$) | 25.90 | 24.81% | 18.90% | 912.4 FPS | Comparative Baseline |
| **YOLOv9-C (Ours — Small Prototype)** | S ($128^2$) | 25.30 | 0.00% *(collapsed)* | 0.00% *(collapsed)* | 892.9 FPS | Synthetic 40-frame sanity run |

### Delta Analysis:
$$\Delta \text{mAP}_{50} = 25.25\% - 25.93\% = -0.68\%$$
$$\Delta \text{mAP}_{50:95} = 19.03\% - 19.47\% = -0.44\%$$
```
**Application to `02-EVIDENCE-AUDIT.md`:** Use this exact comparison structure in Section 3 to document the comparative framing between YOLOv9-C (25.3M params) and published YOLOv9-M (20.02M params), explicitly demarcating prototype smoke tests from full runs.

#### Multi-SNR Quantitative Breakdown Pattern
*From `data/benchmark_results/s128_full/COMPARATIVE_BENCHMARK_REPORT.md:48-59`:*
```markdown
| SNR Bin (dB) | Evaluation Frames | $\text{mAP}_{50}$ (%) | $\text{mAP}_{50:95}$ (%) | Clutter & RF Channel Condition |
| :---: | :---: | :---: | :---: | :--- |
| **$-20\text{ dB}$** | 3,333 | **3.90%** | **1.89%** | Severe multipath clutter; target RCS immersed in noise floor |
| **$-12\text{ dB}$** | 3,333 | **11.24%** | **7.81%** | Heavy clutter; weak Doppler signatures detectable |
| **$-4\text{ dB}$** | 3,333 | **22.78%** | **16.77%** | Moderate clutter; rapid detection inflection point |
| **$+4\text{ dB}$** | 3,333 | **35.38%** | **26.92%** | Typical suburban automotive driving conditions |
| **$+12\text{ dB}$** | 3,333 | **37.92%** | **29.48%** | Clear line-of-sight radar returns; high confidence |
| **$+20\text{ dB}$** | 3,333 | **40.28%** | **31.32%** | High-power point scatterers; maximum spatial localization |
| **Grand Mean** | **20,001** | **25.25%** | **19.03%** | **Final Table III Standard Evaluation Score** |
```
**Application to `02-EVIDENCE-AUDIT.md`:** Document the 19,998 evaluated frames ($6 \times 3,333$) from `scripts/build_raddet_notebook.py:721-726` and explain why 3 frames remained unbinned due to integer division of the 20,001 test split.

#### Discrepancy Defense & Human Triage Registry Pattern
*From `docs/ADVISOR-DEFENSE.md:23-43`:*
```markdown
## Focus Question 1: Sub-Rayleigh Limits & The Fourier Uncertainty Principle

### Professor's Challenge
> *"How can deep learning claim to resolve two targets separated by less than the physical Rayleigh range resolution $\Delta R = \frac{c}{2B}$ or Rayleigh angular beamwidth $\Delta \theta = \frac{\lambda}{D}$ without violating the fundamental Fourier Uncertainty Principle?"*

### Formal Mathematical Defense
The classical Rayleigh resolution limit $\Delta R = \frac{c}{2B}$ and angular beamwidth $\Delta \theta = \frac{\lambda}{D \cos\theta}$ govern **linear, shift-invariant, unconstrained Fourier spectral estimators**...
```
**Application to `02-EVIDENCE-AUDIT.md`:** In Section 8 (Human Confirmation Registry), structure each of the 5 discrepancy areas with a 4-field table: Why Confirmation is Necessary, Available Evidence, What Remains Uncertain, and Recommended Action, mapping items to a GitHub triage issue for oral defense preparation.

---

### 2. `docs/index.html` (component / view, request-response)

**Role:** Publication-Grade Academic Reading Portal  
**Data Flow:** DOM Presentation / Static HTML rendering  
**Analog:** `docs/index.html` (self-analog)  

#### Responsive Data Table Wrapper Pattern
*From `docs/index.html:442-454`:*
```html
<div style="margin: 2rem 0; background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 1.5rem; overflow-x: auto;">
  <div style="font-weight: 700; color: #38bdf8; font-size: 1rem; margin-bottom: 0.75rem; text-align: center;">
    Table 3.1: Classical Radar DSP Detection &amp; Estimation Algorithms Comparison
  </div>
  <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; line-height: 1.55; color: #cbd5e1;">
    <thead>
      <tr style="border-bottom: 2px solid #38bdf8; background: rgba(30, 41, 59, 0.6); text-align: left;">
        <th style="padding: 10px 14px; color: #f8fafc; font-weight: 700;">Method</th>
        <th style="padding: 10px 14px; color: #f8fafc; font-weight: 700;">Operating Principle</th>
        <th style="padding: 10px 14px; color: #f8fafc; font-weight: 700;">Mathematical Formulation</th>
        <th style="padding: 10px 14px; color: #f8fafc; font-weight: 700;">Statistical Assumptions</th>
        <th style="padding: 10px 14px; color: #f8fafc; font-weight: 700;">Computational Complexity</th>
        <th style="padding: 10px 14px; color: #f8fafc; font-weight: 700;">Known Failure Modes / Limitations</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid rgba(148, 163, 184, 0.1);">
        <td style="padding: 9px 14px; font-weight: 600; color: #38bdf8;">1D Range FFT</td>
        <td style="padding: 9px 14px;">Fast-time spectral channelization</td>
        <td style="padding: 9px 14px;">$X_R(k) = \sum_{n=0}^{N_s-1} x[n] e^{-j 2\pi k n / N_s}$</td>
        <td style="padding: 9px 14px;">Stationary scatterer phase over $T_c$</td>
        <td style="padding: 9px 14px;">$\mathcal{O}(N_s \log_2 N_s)$</td>
        <td style="padding: 9px 14px;">Bounded by $\Delta R = c/(2B)$; sidelobe leakage</td>
      </tr>
    </tbody>
  </table>
</div>
```
**Application to `docs/index.html`:** Use this exact container and table pattern to author the 6-column classical DSP synthesis table (Table 3.1) in Chapter 3, and Table 4.1 disclosure footnote in Chapter 4.

#### KaTeX Mathematical Equation Blocks Pattern
*From `docs/index.html:2813-2842`:*
```html
<p>
  A linear Frequency-Modulated Continuous-Wave (FMCW) radar synthesizes a transmit waveform whose instantaneous carrier frequency increases linearly across bandwidth $B$ during sweep duration $T_c$:
</p>
<div class="math-display-container">
  $$f(t) = f_c + S t = f_c + \frac{B}{T_c} t, \quad 0 \le t \le T_c$$
</div>
<p>
  where $f_c = 77\text{ GHz}$ represents the nominal start frequency, active chirp duration is $T_c = 50\ \mu\text{s}$, and sweep slope is $S = \frac{B}{T_c} = 2.0\times 10^{13}\text{ Hz/s} = 20\text{ THz/s}$...
</p>
<div class="math-display-container">
  $$\Delta R = \frac{c}{2 B} = \frac{299{,}792{,}458\text{ m/s}}{2 \times 1.0\times 10^9\text{ Hz}} \approx 0.15\text{ m}$$
</div>
<div class="math-display-container">
  $$\Delta v = \frac{\lambda}{2 N_{\text{chirp}} T_c} = \frac{0.003893\text{ m}}{2 \times 128 \times 50\times 10^{-6}\text{ s}} \approx 0.304\text{ m/s}$$
</div>
```
**Application to `docs/index.html`:** Recover complete FMCW derivations in Chapters 2 and 3 using authoritative `radar_config.py` constants ($T_c = 50\ \mu\text{s}$, $\Delta v = 0.304\text{ m/s}$, $R_{\max} = 38.4\text{ m}$), eliminating all legacy 58.8 μs and 0.258 m/s values.

#### Granular Individually-Linked Citation Anchors Pattern
*From `docs/index.html:2817, 2844, 2847`:*
```html
<!-- Single in-text citation -->
radar architectures <a href="#ref-1" class="citation-badge" data-citation="1">[1]</a>
<!-- Multiple consecutive in-text citations -->
signal processing principles <a href="#ref-1" class="citation-badge" data-citation="1">[1]</a>, <a href="#ref-2" class="citation-badge" data-citation="2">[2]</a>
```
**Application to `docs/index.html`:** When citing multiple references (e.g. `[1], [2]`), author them as individual `<a>` tags with discrete `data-citation` attributes so each reference independently activates its tooltip on hover.

#### Bibliography List with Archival Segregation Pattern
*From `docs/index.html:4120-4138` and Plan 02-09 Design:*
```html
<section id="references" class="section-block" style="margin-top: 4rem; padding-top: 2rem; border-top: 2px solid var(--border-color);">
  <h2>References &amp; Formal IEEE Bibliography</h2>
  <div style="font-size: 0.88rem; color: #94a3b8; margin-bottom: 1.75rem;">
    Formal IEEE citation records for all primary peer-reviewed works cited in Chapters 1 through 5.
  </div>

  <!-- Primary Active References [1..N] -->
  <ol class="references-list" style="padding-left: 1.5rem; font-size: 0.88rem; line-height: 1.68; color: #cbd5e1;">
    <li id="ref-1" style="margin-bottom: 0.85rem;">
      M. I. Skolnik, <em>Introduction to Radar Systems</em>, 3rd ed. New York, NY, USA: McGraw-Hill, 2001.
    </li>
    <!-- ... through ref-18 -->
  </ol>

  <!-- Archival Segregation Divider -->
  <hr class="archival-ref-divider" style="margin: 2.5rem 0 1.5rem 0; border: 0; border-top: 1px dashed #64748b;">
  <h3 style="color: #94a3b8; font-size: 1.05rem; font-weight: 600;">Archival Draft References</h3>
  <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 1.25rem;">
    Historical and exploratory citations referenced exclusively in the archived 7-chapter draft.
  </div>

  <ol class="references-list archival-list" start="19" style="padding-left: 1.5rem; font-size: 0.84rem; line-height: 1.65; color: #94a3b8;">
    <li id="ref-19" style="margin-bottom: 0.85rem;">
      A. Karlsson, "Radar Signal Processing using Artificial Neural Networks," Doctoral Dissertation, KTH Royal Institute of Technology &amp; Saab Surveillance, Stockholm, Sweden, 2023. [URN: nbn:se:kth:diva-324546]
    </li>
    <!-- ... through ref-32 -->
  </ol>
</section>
```
**Application to `docs/index.html`:** Segregate active citations [1..18] sequentially in the primary `<ol>`, insert the `<hr class="archival-ref-divider">`, and continue legacy citations [19..32] in the archival `<ol start="19">`.

---

### 3. `docs/app.js` (component / controller, event-driven)

**Role:** Client Application Engine & Citation Tooltip System  
**Data Flow:** Event-driven DOM interaction  
**Analog:** `docs/app.js` (self-analog)  

#### Citation Database Dictionary Entry Pattern
*From `docs/app.js:19-51`:*
```javascript
const CITATIONS_DB = {
  "1": {
    ref: 1,
    authors: "M. I. Skolnik",
    title: "Introduction to Radar Systems",
    venue: "3rd ed., New York, NY, USA: McGraw-Hill",
    year: "2001",
    doi: ""
  },
  "2": {
    ref: 2,
    authors: "M. A. Richards",
    title: "Fundamentals of Radar Signal Processing",
    venue: "2nd ed., New York, NY, USA: McGraw-Hill",
    year: "2014",
    doi: ""
  },
  // Archival reference pattern:
  "19": {
    ref: 19,
    authors: "A. Karlsson",
    title: "Radar Signal Processing using Artificial Neural Networks",
    venue: "Doctoral Dissertation, KTH Royal Institute of Technology & Saab Surveillance, Stockholm, Sweden",
    year: "2023",
    doi: "http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-324546",
    archival: true
  }
};
```
**Application to `docs/app.js`:** Re-index `CITATIONS_DB` keys "1" through "18" matching active order of appearance, verify Skolnik 2001 (3rd ed.) and RadDet ICASSP 2025 metadata, and populate keys "19" through "32" with `archival: true`.

#### XSS-Free Safe Tooltip DOM Generation Pattern
*From `docs/app.js:388-413`:*
```javascript
// Build tooltip safely without innerHTML (CWE-79 mitigation)
while (tooltipEl.firstChild) {
  tooltipEl.removeChild(tooltipEl.firstChild);
}

const refNum = document.createElement("div");
refNum.className = "tooltip-ref-num";
refNum.textContent = data.archival
  ? `Archival Reference [${data.ref}]`
  : `IEEE Reference [${data.ref}]`;

const title = document.createElement("div");
title.className = "tooltip-title";
title.textContent = data.title;

const authors = document.createElement("div");
authors.className = "tooltip-authors";
authors.textContent = data.authors;

const venue = document.createElement("div");
venue.className = "tooltip-venue";
venue.textContent = `${data.venue} (${data.year})`;

tooltipEl.appendChild(refNum);
tooltipEl.appendChild(title);
tooltipEl.appendChild(authors);
tooltipEl.appendChild(venue);

if (data.doi) {
  const link = document.createElement("a");
  link.className = "tooltip-doi";
  link.href = data.doi.startsWith("http") ? data.doi : `https://doi.org/${data.doi}`;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = data.doi;
  tooltipEl.appendChild(link);
}
```
**Application to `docs/app.js`:** Ensure all tooltip components continue to be constructed using `createElement` and `textContent`, adding support for the DOI link element and archival reference badge.

#### Viewport-Aware Tooltip Positioning Pattern
*From `docs/app.js:414-432`:*
```javascript
// Position tooltip relative to badge
const rect = badge.getBoundingClientRect();
const tooltipWidth = 360;
let left = rect.left + window.scrollX - 40;
let top = rect.top + window.scrollY - 110;

// Viewport edge collision handling
if (left + tooltipWidth > window.innerWidth - 20) {
  left = window.innerWidth - tooltipWidth - 20;
}
if (left < 10) left = 10;
if (rect.top < 120) {
  top = rect.bottom + window.scrollY + 10;
}

tooltipEl.style.left = `${left}px`;
tooltipEl.style.top = `${top}px`;
tooltipEl.classList.add("visible");
```
**Application to `docs/app.js`:** Retain viewport edge collision guards ensuring tooltips never overflow the screen or clip under the navigation header on desktop or mobile viewports.

---

### 4. `tests/test_academic_website.py` (test, batch / file-I/O)

**Role:** Deterministic Pytest Validation Suite  
**Data Flow:** Batch DOM and file inspection  
**Analog:** `tests/test_academic_website.py` (self-analog)  

#### Divider-Splitting & Text Assertion Pattern
*From `tests/test_academic_website.py:335-370`:*
```python
def test_chapter_finalization_phase2():
    """Verify Phase 2 finalized Chapters 1, 2, 3, 4, and 5 above the transition boundary."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Split by transition boundary
    assert '<div id="manuscript-transition-divider"' in html
    above_divider, below_divider = html.split('<div id="manuscript-transition-divider"', 1)

    # Chapter 3 Methodology present above divider
    assert '<section id="ch3-methodology"' in above_divider
    assert "Chapter 3: Methodology" in above_divider
    for algo in ["Algorithm 3.1", "Algorithm 3.2", "Algorithm 3.3", "Algorithm 3.4", "Algorithm 3.5"]:
        assert algo in above_divider, f"Missing {algo} in Chapter 3"
```
**Application to `tests/test_academic_website.py`:** Use `html.split('<div id="manuscript-transition-divider"', 1)` to partition active chapters from archival chapters for discrete verification.

#### Permanent Invariant Assertion 1: Zero Legacy FMCW Parameters
*To be implemented in Plan 02-09:*
```python
def test_no_legacy_radar_parameters():
    """Assert zero instances of legacy 58.8 μs or 0.258 m/s parameters in active chapters."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert '<div id="manuscript-transition-divider"' in html
    above_divider, _ = html.split('<div id="manuscript-transition-divider"', 1)

    assert "58.8" not in above_divider, "Found legacy 58.8 μs chirp duration in active chapters"
    assert "0.258" not in above_divider, "Found legacy 0.258 m/s velocity resolution in active chapters"
    assert "2.72" not in above_divider, "Found legacy 2.72 THz/s slope in active chapters"
    
    # Assert authoritative parameters are present
    assert "50\\ \\mu\\text{s}" in above_divider or "50 μs" in above_divider or "50\\,\\mu\\text{s}" in above_divider
    assert "0.304" in above_divider, "Missing authoritative 0.304 m/s velocity resolution"
```

#### Permanent Invariant Assertion 2: Citation Anchor & Tooltip Resolution
*To be implemented in Plan 02-09:*
```python
def test_active_citation_anchors_and_tooltips():
    """Verify all active in-text citations are sequential [1..N] and resolve in docs/app.js."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    above_divider, _ = html.split('<div id="manuscript-transition-divider"', 1)
    
    # Find all citation badge anchors above divider
    citation_refs = re.findall(r'href="#ref-(\d+)"', above_divider)
    assert len(citation_refs) > 0, "No citation anchors found above divider"
    
    # Check that first occurrences form an exact sequential range [1..N]
    seen = []
    for ref in citation_refs:
        if ref not in seen:
            seen.append(ref)
    
    expected_sequence = [str(i) for i in range(1, len(seen) + 1)]
    assert seen == expected_sequence, f"Citations not sequential in order of appearance: {seen} vs {expected_sequence}"

    # Verify each active citation exists in CITATIONS_DB in docs/app.js
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    for ref in seen:
        assert f'"{ref}":' in js or f"'{ref}':" in js, f"Reference [{ref}] missing from docs/app.js CITATIONS_DB"
        assert f'id="ref-{ref}"' in html, f"Target anchor #ref-{ref} missing from docs/index.html bibliography"
```

#### Permanent Invariant Assertion 3: Scope & Archival Integrity
*To be implemented in Plan 02-09:*
```python
def test_scope_and_archival_preservation():
    """Verify LaTeX templates are untouched and archived 7-chapter draft remains intact."""
    import subprocess
    
    # Git status check on Overleaf templates
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "templates/BTP_Report_Template_Overleaf/"],
        cwd=REPO_ROOT,
        text=True
    ).strip()
    assert status == "", f"templates/BTP_Report_Template_Overleaf/ was mutated: {status}"

    # Verify intact archival draft sections
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert '<div id="manuscript-transition-divider"' in html
    _, below_divider = html.split('<div id="manuscript-transition-divider"', 1)

    for arch_ch in ["#ch1-intro-original", "#ch2-physics", "#ch3-dsp-audit", "#ch4-methodology", "#ch5-benchmarks", "#ch6-timeline", "#ch7-conclusion"]:
        clean_id = arch_ch.replace("#", "")
        assert f'id="{clean_id}"' in below_divider, f"Missing archived draft section: {arch_ch}"
```

---

## Shared Patterns

### Pattern 1: XSS-Free Safe DOM Manipulation
- **Source:** `docs/app.js:388-413`
- **Apply to:** All dynamic HTML generation in client scripts.
- **Rules:** Never use `.innerHTML = "..."` with dynamic variables. Always instantiate elements using `document.createElement()`, assign textual content via `element.textContent = ...`, and set attributes using `element.setAttribute(...)` or property assignments.

### Pattern 2: Dual-Section Boundary & Archival Segregation
- **Source:** `docs/index.html:2756-2763` (`#manuscript-transition-divider`) and `tests/test_academic_website.py:341-343`
- **Apply to:** `docs/index.html` main chapters, bibliography, and `tests/test_academic_website.py`.
- **Rules:**
  1. Main document content is split at `<div id="manuscript-transition-divider">`. Active 5-chapter manuscript content lives strictly above; frozen 7-chapter original draft lives strictly below.
  2. Bibliography is split with `<hr class="archival-ref-divider">`. Active sequential IEEE references [1..N] reside in the primary `<ol class="references-list">`; legacy citations [N+1..M] reside in `<ol class="references-list archival-list" start="N+1">`.

### Pattern 3: Offline Vendored KaTeX Mathematical Engine
- **Source:** `docs/app.js:266-280`, `docs/styles.css:12-40`, and `tests/test_academic_website.py:67-87`
- **Apply to:** Mathematical physics formulations across Chapters 2, 3, and Appendix A.
- **Rules:**
  - Inline mathematics formatted as `$ ... $` or `<span class="math inline">\( ... \)</span>`.
  - Display equations formatted as `$$ ... $$` enclosed within `<div class="math-display-container">`.
  - Zero external CDN `<script>` or font fetches; engine is 100% vendored in `docs/assets/vendor/katex/`.

### Pattern 4: Authoritative Physical FMCW Radar Invariants
- **Source:** `src/sim/radar_config.py:22-69`
- **Apply to:** `docs/index.html` (Chapters 2 & 3), `02-EVIDENCE-AUDIT.md`, and `tests/test_academic_website.py`.
- **Constants:**
  - Center frequency: $f_c = 77\text{ GHz}$ ($\lambda \approx 3.896\text{ mm}$)
  - Sweep bandwidth: $B = 1.0\text{ GHz}$
  - Active chirp duration: $T_c = 50\ \mu\text{s}$ ($S = 20\text{ THz/s}$)
  - Range resolution: $\Delta R = \frac{c}{2B} \approx 0.15\text{ m}$
  - Velocity resolution: $\Delta v = \frac{\lambda}{2 N_{\text{chirp}} T_c} \approx 0.304\text{ m/s}$ (with $N_{\text{chirp}} = 128$)
  - Maximum unambiguous range: $R_{\max} = \frac{F_s c}{2 S} \approx 38.4\text{ m}$ (with $F_s = 5.12\text{ MHz}$)
  - Physical antenna spacing: 4-element ULA with $d = \lambda/2 \approx 1.948\text{ mm}$ ($\Delta \theta_{\text{Rayleigh}} \approx 28.6^\circ$)

### Pattern 5: Scope Protection & Deterministic Regression Gates
- **Source:** `AGENTS.md:Section 1`, `02-SPEC.md:Constraints`, and `tests/test_academic_website.py`
- **Apply to:** Git commits, plan executions, and test runners.
- **Rules:**
  - `git status --porcelain templates/BTP_Report_Template_Overleaf/` must be 100% empty at all times.
  - Sub-second unit test execution (`pytest tests/test_academic_website.py` completes in <0.5s).
  - Universal verification pass via `pwsh -File ./scripts/verify.ps1`.

---

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| *None* | — | — | All 4 files have strong, verified git-tracked analogs within the repository. |

---

## Metadata

- **Analog search scope:** `data/benchmark_results/`, `docs/`, `tests/`, `src/sim/`, `src/dsp/`, `.planning/`
- **Files scanned:** 12 tracked repository files
- **Pattern extraction date:** 2026-11-18
- **Verification status:** Validated against existing `pytest` suite (20 passed in 0.38s)
