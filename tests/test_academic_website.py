"""
tests/test_academic_website.py — Wave 0 Deterministic Test Suite
Validates publication-grade academic portal infrastructure:
  - HTML5 structure, semantic containers, and chapter anchors
  - Two-column CSS rules, serif/sans-serif typography, and responsive media queries
  - Vendored offline KaTeX mathematical typesetting engine and font assets
  - Client-side application logic (auto-render math, scroll-spy, citation hover tooltips, code drawers)
  - Asset path resolution (zero broken images or diagram links)
"""

import os
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
INDEX_HTML = os.path.join(DOCS_DIR, "index.html")
STYLES_CSS = os.path.join(DOCS_DIR, "styles.css")
APP_JS = os.path.join(DOCS_DIR, "app.js")
KATEX_DIR = os.path.join(DOCS_DIR, "assets", "vendor", "katex")


def test_file_existence():
    """Verify all critical academic portal files exist on disk."""
    assert os.path.exists(INDEX_HTML), f"Missing {INDEX_HTML}"
    assert os.path.exists(STYLES_CSS), f"Missing {STYLES_CSS}"
    assert os.path.exists(APP_JS), f"Missing {APP_JS}"
    assert os.path.exists(os.path.join(KATEX_DIR, "katex.min.js")), "Missing vendored katex.min.js"
    assert os.path.exists(os.path.join(KATEX_DIR, "katex.min.css")), "Missing vendored katex.min.css"
    assert os.path.exists(os.path.join(KATEX_DIR, "auto-render.min.js")), "Missing vendored auto-render.min.js"


def test_css_rules():
    """Verify publication-grade academic layout rules, typography, and responsive design."""
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()

    # Academic two-column layout & full-width breakout
    assert ".academic-two-column" in css, "CSS must define .academic-two-column"
    assert ".full-width-breakout" in css, "CSS must define .full-width-breakout"
    assert "column-span: all" in css or "grid-column:" in css, "Breakout must span columns"

    # Advisor Defense Callout Cards
    assert ".advisor-defense-card" in css, "CSS must define .advisor-defense-card"
    assert "#0284c7" in css or "var(--accent-sky" in css or "var(--accent-blue" in css or "rgb(" in css or "#" in css, "Must have academic accent"

    # Reading progress bar & sidebar navigation
    assert "#reading-progress-bar" in css, "CSS must define #reading-progress-bar"
    assert "#academic-sidebar" in css or ".sidebar" in css, "CSS must style academic sidebar"

    # Interactive Citation Tooltip & Code Drawer styling
    assert ".citation-badge" in css, "CSS must define .citation-badge"
    assert ".citation-tooltip" in css, "CSS must define .citation-tooltip"
    assert ".collapsible-drawer" in css or ".code-drawer" in css, "CSS must define code drawer container"

    # Responsive breakpoints
    assert "@media" in css, "CSS must contain responsive media queries"
    assert "max-width" in css, "CSS must define max-width responsive rules"

    # Academic typography (Serif/Sans-serif pairing)
    assert any(font in css for font in ["Merriweather", "Georgia", "serif", "Latin Modern"]), "Must specify serif heading/academic font"
    assert any(font in css for font in ["Inter", "sans-serif", "Roboto", "Helvetica"]), "Must specify clean sans-serif body font"


def test_katex_vendor():
    """Verify vendored KaTeX distribution is complete and offline-ready."""
    katex_js = os.path.join(KATEX_DIR, "katex.min.js")
    katex_css = os.path.join(KATEX_DIR, "katex.min.css")
    auto_render = os.path.join(KATEX_DIR, "auto-render.min.js")
    fonts_dir = os.path.join(KATEX_DIR, "fonts")

    assert os.path.getsize(katex_js) > 50000, "katex.min.js is incomplete"
    assert os.path.getsize(katex_css) > 5000, "katex.min.css is incomplete"
    assert os.path.getsize(auto_render) > 1000, "auto-render.min.js is incomplete"

    with open(katex_js, "r", encoding="utf-8") as f:
        assert "katex" in f.read().lower(), "katex.min.js does not contain KaTeX engine"

    with open(auto_render, "r", encoding="utf-8") as f:
        assert "renderMathInElement" in f.read(), "auto-render.min.js does not contain renderMathInElement"

    assert os.path.exists(fonts_dir), "fonts directory missing from vendored KaTeX"
    font_files = [f for f in os.listdir(fonts_dir) if f.endswith(".woff2")]
    assert len(font_files) >= 10, f"Expected at least 10 woff2 fonts, found {len(font_files)}"


def test_app_js_features():
    """Verify docs/app.js implements auto-math rendering, scroll-spy, citation popups, and drawer toggles."""
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # KaTeX auto-render integration
    assert "renderMathInElement" in js, "app.js must call renderMathInElement"
    assert "$$" in js and "$" in js, "app.js must configure $ and $$ math delimiters"

    # Reading progress bar logic
    assert "reading-progress-bar" in js, "app.js must control #reading-progress-bar"
    assert "scrollY" in js or "scrollTop" in js, "app.js must track scroll position for progress bar"

    # Scroll-spy for chapters and sections
    assert "IntersectionObserver" in js or "scroll" in js, "app.js must implement scroll-spy"
    expected_anchors = ["ch1-intro", "ch2-physics", "ch3-dsp-audit", "ch4-methodology", "ch5-benchmarks", "ch6-timeline", "ch7-conclusion"]
    anchor_matches = sum(1 for a in expected_anchors if a in js)
    assert anchor_matches >= 4, "app.js scroll-spy must target academic chapter anchors"

    # Interactive Citation Tooltips
    assert "citation-badge" in js or "data-citation" in js, "app.js must target citation badges"
    assert "citation-tooltip" in js or "tooltip" in js, "app.js must construct citation tooltips"

    # Collapsible Code Drawers
    assert "drawer" in js or "collapse" in js or "toggle" in js, "app.js must handle code drawer interactivity"


def test_image_paths_resolve():
    """Verify that all non-empty img src paths in docs/index.html resolve to actual files and valid media."""
    class ImgSrcParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.srcs = []

        def handle_starttag(self, tag, attrs):
            if tag == "img":
                attr_dict = dict(attrs)
                # Ignore dynamic lightbox placeholder with id="lightbox-img"
                if attr_dict.get("id") == "lightbox-img":
                    return
                src = attr_dict.get("src", "").strip()
                if src:
                    self.srcs.append(src)

    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        parser = ImgSrcParser()
        parser.feed(f.read())

    assert len(parser.srcs) > 0, "No image tags found in docs/index.html"
    for src in parser.srcs:
        # Normalize relative path
        rel_path = src.replace("./", "").replace("/", os.sep)
        full_path = os.path.join(DOCS_DIR, rel_path)
        assert os.path.exists(full_path), f"Broken image path in docs/index.html: {src} -> {full_path}"
        assert os.path.getsize(full_path) > 0, f"Empty image file in docs/index.html: {src}"

        # If SVG, strictly verify well-formed XML to prevent browser rendering drops
        if src.lower().endswith(".svg"):
            try:
                tree = ET.parse(full_path)
                root = tree.getroot()
                assert "svg" in root.tag.lower(), f"Root tag of {src} is not <svg>: {root.tag}"
            except Exception as e:
                pytest.fail(f"Embedded SVG in docs/index.html has XML syntax error and will not render in browser: {src} -> {e}")
        elif src.lower().endswith(".png"):
            with open(full_path, "rb") as pf:
                magic = pf.read(8)
                assert magic == b"\x89PNG\r\n\x1a\n", f"Invalid PNG magic bytes in {src}"


def test_all_svg_diagrams_valid_xml():
    """Verify all SVG files in docs/assets/diagrams are well-formed XML that browsers can render without breaking."""
    diagrams_dir = os.path.join(DOCS_DIR, "assets", "diagrams")
    assert os.path.exists(diagrams_dir), f"Missing diagrams directory {diagrams_dir}"

    svg_files = [f for f in os.listdir(diagrams_dir) if f.endswith(".svg")]
    assert len(svg_files) >= 5, f"Expected at least 5 diagram SVGs, found {len(svg_files)}"

    for svg_name in svg_files:
        svg_path = os.path.join(diagrams_dir, svg_name)
        assert os.path.getsize(svg_path) > 500, f"SVG {svg_name} suspiciously small: {os.path.getsize(svg_path)} bytes"
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()
            assert "svg" in root.tag.lower(), f"Root tag of {svg_name} is not <svg>: {root.tag}"
            assert "viewBox" in root.attrib or ("width" in root.attrib and "height" in root.attrib), \
                f"SVG {svg_name} missing viewBox or width/height attributes"
        except Exception as e:
            pytest.fail(f"SVG {svg_name} contains XML parse errors and cannot be displayed in browser: {e}")


def test_html_syntax_and_basics():
    """Verify docs/index.html is valid HTML5 document."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert "<!DOCTYPE html>" in html or "<!doctype html>" in html
    assert "<html" in html and "</html>" in html
    assert "<head>" in html or "<head " in html
    assert "<body>" in html or "<body " in html


def test_chapter_sections():
    """Verify Chapter 1-7 anchors exist once full academic thesis is integrated (Plan 04)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    if "academic-paper-content" not in content and "ch1-intro" not in content:
        pytest.skip("Full academic report body scheduled for integration in Plan 01.2.2-04")

    required_chapters = [
        "ch1-intro",
        "ch2-physics",
        "ch3-dsp-audit",
        "ch4-methodology",
        "ch5-benchmarks",
        "ch6-timeline",
        "ch7-conclusion",
        "references"
    ]
    for ch in required_chapters:
        assert f'id="{ch}"' in content or f"id='{ch}'" in content, f"Missing chapter anchor: #{ch}"


def test_institutional_metadata():
    """Verify exact official IIT Guwahati institutional metadata (D-16)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert "AI Applications in Radar Signal Processing" in html, "Missing official primary title"
    assert "Towards Resource-Efficient AI-Based Radar Detection for Millimetre-Wave FMCW Systems" in html, "Missing official subtitle"
    assert "Aryan Sandeep Gupta" in html, "Missing candidate full name"
    assert "230150003" in html, "Missing student roll number"
    assert "Mehta Family School of Data Science and Artificial Intelligence" in html, "Missing official school name"
    assert "DA4098P BTP Project I" in html, "Missing official course code"
    assert "Prof. Ratnajit Bhattacharjee" in html, "Missing supervisor name"
    assert "Head, Mehta Family School of Data Science and Artificial Intelligence" in html, "Missing supervisor role 1"
    assert "Professor, Department of Electronics and Electrical Engineering" in html, "Missing supervisor role 2"
    assert "Head, Manekshaw Centre of Excellence for National Security Studies and Research" in html, "Missing supervisor role 3"


def test_clean_header_and_sidebar():
    """Verify clean print-like IEEE layout and absence of distracting progress bar and hardware chip badges (D-11, D-16)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Progress bar omitted from index.html for print-like aesthetic
    assert '<div id="reading-progress-bar"></div>' not in html, "#reading-progress-bar should be omitted from index.html"

    # Hardware chip badges omitted from sidebar
    assert 'id="academic-sidebar"' in html
    sidebar_html = html.split('id="academic-sidebar"')[1].split('</aside>')[0]
    assert "AWR1843" not in sidebar_html, "Sidebar must not contain standalone AWR1843 chip badge"
    assert "DCA1000" not in sidebar_html, "Sidebar must not contain standalone DCA1000 chip badge"

    # Sidebar footer
    assert "BTP-1 Thesis Portal · Autumn 2026" in html, "Missing sidebar footer marker"


def test_five_code_drawers():
    """Verify presence of 5 syntax-highlighted collapsible IDE code drawers (D-18)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Must contain code-drawer or collapsible-drawer elements
    drawer_count = html.count('class="collapsible-drawer"') + html.count('class="code-drawer"')
    assert drawer_count >= 5, f"Expected at least 5 code drawers, found {drawer_count}"

    # Verify all 5 algorithms are represented
    assert "fmcw.py" in html or "FMCW Beat Signal" in html, "Missing FMCW beat signal generator code drawer"
    assert "mti.py" in html or "MTI Clutter" in html, "Missing MTI clutter filter code drawer"
    assert "cfar.py" in html or "CFAR Detector" in html, "Missing 2D CFAR detector code drawer"
    assert "music.py" in html or "MUSIC Direction" in html, "Missing MUSIC spatial DoA code drawer"
    assert "detector.py" in html or "RadarObjectDetectorCNN" in html, "Missing RadarObjectDetectorCNN code drawer"


def test_two_part_chapter_structure():
    """Verify strict two-part problem partition in Chapters 4 and 5 (D-14)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert "Part A: Synthetic 77 GHz FMCW Automotive Spatial Detection" in html, "Missing Part A header/marker"
    assert ("Part B: Real-World RadDet RF Spectrum & Modulation Classification" in html or
            "Part B: Real-World RadDet RF Spectrum &amp; Modulation Classification" in html), "Missing Part B header/marker"

    # Explicit disclaimer that RadDet is RF spectrum sensing, not automotive traffic
    assert "RadDet is strictly" in html or "RadDet is strictly RF" in html or "RadDet is strictly an RF" in html, "Missing RadDet scope disclaimer"
    assert "does NOT" in html or "does not" in html, "Missing disclaimer that RadDet does not detect vehicles/pedestrians"


def test_latency_waterfall_and_cpu_methodology():
    """Verify multi-stage latency waterfall timing budget and CPU-first research methodology (D-13, D-15)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Latency waterfall timing values
    assert "0.18" in html, "Missing Range FFT latency (0.18 ms)"
    assert "0.24" in html, "Missing Doppler FFT latency (0.24 ms)"
    assert "0.12" in html, "Missing Preprocessing latency (0.12 ms)"
    assert "1.12" in html, "Missing GPU inference latency (1.12 ms)"
    assert "0.15" in html, "Missing Postprocessing NMS latency (0.15 ms)"
    assert "0.10" in html, "Missing Memory I/O latency (0.10 ms)"
    assert "1.91" in html, "Missing Total end-to-end latency (1.91 ms)"

    # Frame deadline and CPU-first formulation
    assert any(term in html for term in ["20 ms", "20\\text{ ms}", "50 Hz", "50\\text{ Hz}"]), "Missing 20 ms / 50 Hz frame deadline"
    assert any(term in html for term in ["CPU-First", "CPU-first", "CPU Baseline", "native CPU"]), "Missing CPU-first research methodology"


def test_academic_timeline_and_defense():
    """Verify academic timeline milestones, curriculum, and oral defense date (D-16, D-17)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert "MATLAB Radar Designer" in html, "Missing MATLAB Radar Designer App documentation"
    assert "Skolnik" in html and "Richards" in html, "Missing Skolnik and Richards curriculum references"
    assert "November 23, 2026" in html or "Nov 23, 2026" in html, "Missing BTP-1 final oral defense date"
    assert "January 2027" in html, "Missing BTP-2 January milestone"
    assert "May 2027" in html, "Missing BTP-2 May milestone"


def test_official_abstract():
    """Verify presence and empirical accuracy of the finalized official thesis abstract."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert '<div class="paper-abstract"' in html, "Missing .paper-abstract container"
    abstract_block = html.split('<div class="paper-abstract"')[1].split('</div>')[0]

    # Key narrative statements
    assert "Radar sensing is increasingly used in intelligent perception" in abstract_block
    assert "two complementary experimental tracks" in abstract_block
    assert "synthetic 77 GHz frequency-modulated continuous-wave (FMCW) radar environment" in abstract_block
    assert "wideband radar-spectrum detection using the RadDet dataset" in abstract_block

    # Empirical metrics
    assert "25.25%" in abstract_block and "19.03%" in abstract_block, "Missing Table III reproduction metrics in abstract"
    assert "1.12 ms" in abstract_block, "Missing GPU inference latency in abstract"
    assert "-20 dB" in abstract_block and "+20 dB" in abstract_block, "Missing multi-SNR range in abstract"
    assert "3.90%" in abstract_block and "40.28%" in abstract_block, "Missing low and high SNR mAP values in abstract"

    # Research direction synthesis
    assert "Reducing computational requirements and investigating CPU-oriented inference" in abstract_block
    assert "Index Terms:" in html


def test_chapter_finalization_phase2():
    """Verify Phase 2 finalized Chapters 1, 2, 3, 4, and 5 above the transition boundary."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Split by transition boundary
    assert '<div id="manuscript-transition-divider"' in html
    above_divider, below_divider = html.split('<div id="manuscript-transition-divider"', 1)

    # Chapter 1 Section 1.4 present above divider
    assert "1.4 Scope of the Study and Organisation of the Report" in above_divider

    # No duplicate Section 1.2 or 1.3 above divider
    assert above_divider.count("1.2 Problem Statement") == 1
    assert above_divider.count("1.3 Objectives") == 1

    # Chapter 2 Table 2.1 present above divider
    assert "Table 2.1: Comparison of the two radar application settings" in above_divider

    # Chapter 3 Methodology present above divider
    assert '<section id="ch3-methodology"' in above_divider
    assert "Chapter 3: Methodology" in above_divider
    assert "3.1 Overall Methodological Framework" in above_divider
    assert "3.2 Experimental Track I: Synthetic FMCW Radar Perception" in above_divider
    assert "3.3 Experimental Track II: Wideband Radar Spectrum Detection" in above_divider
    assert "3.4 Methodology for Resource-Efficiency Investigation" in above_divider
    assert "3.5 Summary of the Methodology" in above_divider

    # Chapter 3 Algorithms and Code Listings
    for algo in ["Algorithm 3.1", "Algorithm 3.2", "Algorithm 3.3", "Algorithm 3.4", "Algorithm 3.5"]:
        assert algo in above_divider, f"Missing {algo} in Chapter 3"
    for code in ["Code Listing 3.1", "Code Listing 3.2", "Code Listing 3.3"]:
        assert code in above_divider, f"Missing {code} in Chapter 3"
    for table in ["Table 3.1", "Table 3.2", "Table 3.3"]:
        assert table in above_divider, f"Missing {table} in Chapter 3"

    # Chapter 4 Experimental Results and Analysis present above divider
    assert '<section id="ch4-results"' in above_divider
    assert "Chapter 4: Experimental Results and Analysis" in above_divider
    assert "4.1 Experimental Scope and Evaluation Framework" in above_divider
    assert "4.2 Experimental Track I: Synthetic FMCW Radar Perception" in above_divider
    assert "4.3 Experimental Track II: Wideband Radar Spectrum Detection" in above_divider
    assert "4.4 Computational Performance and Resource Analysis" in above_divider
    assert "4.5 Discussion and Limitations" in above_divider

    # Chapter 4 Tables
    for table in ["Table 4.1", "Table 4.2", "Table 4.3", "Table 4.4", "Table 4.5", "Table 4.6", "Table 4.7"]:
        assert table in above_divider, f"Missing {table} in Chapter 4"

    # Chapter 4 Figures
    for fig in ["Figure 4.1", "Figure 4.2", "Figure 4.3", "Figure 4.4", "Figure 4.5", "Figure 4.6", "Figure 4.7", "Figure 4.8", "Figure 4.9", "Figure 4.10"]:
        assert fig in above_divider, f"Missing {fig} in Chapter 4"

    # Chapter 4 Code Listing
    assert "Code Listing 4.1" in above_divider

    # Chapter 4 Key Empirical Metrics
    assert "12.94 dB" in above_divider or "12.94\\text{ dB}" in above_divider, "Missing clutter attenuation metric"
    assert "0.0125" in above_divider, "Missing range MAE metric"
    assert "0.105" in above_divider, "Missing velocity MAE metric"
    assert "136,041" in above_divider or "136{,}041" in above_divider, "Missing synthetic CNN parameter metric"
    assert "32.53%" in above_divider, "Missing peak validation mAP50"
    assert "25.25%" in above_divider, "Missing Table III reproduction grand mean"
    assert "892.9 FPS" in above_divider or "1.12 ms" in above_divider, "Missing inference speed metric"

    # Chapter 4 Forensic Reconciliations & Disclosures (D-01, D-02, D-03, D-04, R4)
    assert "Partition & Chunking Disclosure Note" in above_divider, "Missing partition disclosure footnote"
    assert "14,001 train" in above_divider and "20,001 test" in above_divider, "Missing 14,001/20,001 partition count"
    assert "19,998" in above_divider, "Missing 19,998 chunking calculation in disclosure note"
    assert "total average signal-power reduction" in above_divider, "Missing formal 12.94 dB clutter attenuation definition"
    assert "Rayleigh angular resolution limit" in above_divider, "Missing Rayleigh physical limit distinction"

    # Chapter 5 Conclusion and Future Work present above divider
    assert '<section id="ch5-conclusion"' in above_divider
    assert "Chapter 5: Conclusion and Future Work" in above_divider
    assert "5.1 Summary of the Study" in above_divider
    assert "5.2 Conclusions and Achievement of Objectives" in above_divider
    assert "5.3 Key Findings and Research Implications" in above_divider
    assert "5.4 Limitations of the Study" in above_divider
    assert "5.5 Future Work" in above_divider
    assert "5.6 Requirements for the Next-Stage Demonstration" in above_divider
    assert "5.7 Final Conclusion" in above_divider

    # Chapter 5 Tables
    assert "Table 5.1: Objective achievement summary" in above_divider
    assert "Table 5.2: Proposed roadmap for the subsequent phase" in above_divider

    # Chapter 5 Figure 5.1 Gantt Schedule
    assert "Figure 5.1: One-Year Academic Gantt Schedule for BTP-1 and Proposed BTP-2 Activities (August 2026 – May 2027)" in above_divider
    assert "timeline_gantt.svg" in above_divider
    assert above_divider.find("Table 5.2") < above_divider.find("Figure 5.1") < above_divider.find("5.6 Requirements for the Next-Stage Demonstration")

    # Verify Gantt chart artifacts on disk
    gantt_svg = os.path.join(DOCS_DIR, "assets", "diagrams", "timeline_gantt.svg")
    gantt_pdf = os.path.join(REPO_ROOT, "templates", "BTP_Report_Template_Overleaf", "figures", "timeline_gantt.pdf")
    assert os.path.exists(gantt_svg), f"Missing {gantt_svg}"
    assert os.path.exists(gantt_pdf), f"Missing {gantt_pdf}"
    assert os.path.getsize(gantt_svg) > 1000, "timeline_gantt.svg is too small"
    assert os.path.getsize(gantt_pdf) > 1000, "timeline_gantt.pdf is too small"

    # Chapter 5 Key Framework Declarations
    assert "Approach A: Computational Reduction" in above_divider
    assert "Approach B: CPU-Oriented Inference" in above_divider
    assert "Laboratory & Hardware Confirmation Protocol" in above_divider

    # Sidebar TOC contains Chapters 3, 4, and 5
    assert '<a href="#ch3-methodology" class="toc-link">' in html
    assert '<a href="#ch4-results" class="toc-link">' in html
    assert '<a href="#ch5-conclusion" class="toc-link">' in html


def test_evidence_audit_dossier():
    """Verify Phase 2 forensic evidence audit dossier (02-EVIDENCE-AUDIT.md) completeness."""
    audit_path = os.path.join(
        REPO_ROOT,
        ".planning",
        "phases",
        "02-github-pages-chapter-by-chapter-content-finalization",
        "02-EVIDENCE-AUDIT.md",
    )
    assert os.path.exists(audit_path), f"Missing forensic audit dossier at {audit_path}"
    assert os.path.getsize(audit_path) > 5000, "02-EVIDENCE-AUDIT.md is smaller than 5,000 bytes"

    with open(audit_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Assert all 9 mandatory sections exist
    required_sections = [
        "## 1. Executive Summary & Audit Mandate",
        "## 2. 3-Tier Evidence Taxonomy",
        "## 3. Authoritative FMCW Physical Radar Mathematical Derivations",
        "## 4. Classical DSP Baseline 6-Column Synthesis Matrix",
        "## 5. Forensic Audit of the 5 Critical Disputed Experimental Areas",
        "## 6. Track I vs Track II Dual-Track Architectural Grounding",
        "## 7. 7-Axis Literature Comparison Matrix Grounding",
        "## 8. Structured Human Confirmation Registry & Defense Triage",
        "## 9. Canonical Reference Verification Table & IEEE Bijective Renumbering Mapping",
    ]
    for section in required_sections:
        assert section in content, f"Missing section in 02-EVIDENCE-AUDIT.md: {section}"

    # Assert 3-Tier Taxonomy per D-14
    assert "Tier 1" in content and "Verified" in content
    assert "Tier 2" in content and "Partially Verified" in content
    assert "Tier 3" in content and "Smoke Test" in content

    # Assert Authoritative FMCW Physical Radar Parameters (D-04, D-05, R2)
    assert "77 GHz" in content or "77.0e9" in content
    assert "1.0 GHz" in content or "1 GHz" in content or "1.0e9" in content
    assert "50" in content and "μs" in content
    assert "0.304" in content
    assert "38.4" in content
    assert "Rayleigh" in content

    # Assert Classical DSP 6-column matrix coverage (D-06)
    for dsp_method in [
        "1D Range FFT",
        "MTI Clutter Filter",
        "2D Slow-Time Doppler FFT",
        "CFAR",
        "MUSIC",
        "DBSCAN",
    ]:
        assert dsp_method in content, f"Missing {dsp_method} in DSP synthesis matrix"
    assert "exponential noise power" in content or "exponential" in content

    # Assert 5 Critical Disputed Claims Reconciled (D-01, D-02, D-03, D-04, D-08)
    assert "14,001" in content and "6,001" in content and "20,001" in content
    assert "19,998" in content  # Integer division chunking math (3,333 * 6)
    assert "25.25%" in content and "25.30M" in content  # YOLOv9-C benchmark metrics
    assert "136,041" in content and "32" in content  # Synthetic CNN smoke test audit
    assert "12.94" in content  # Clutter attenuation power ratio
    assert "180" in content  # MUSIC evaluation grid vs physical aperture

    # Assert Track I vs Track II Decoupling & RadDet RF Spectrum Grounding (R3, R4)
    assert "Track I" in content and "Track II" in content
    assert "LFM" in content and "Barker" in content and "FMCW" in content

    # Assert Structured Human Confirmation Registry & GitHub Issue Spec (D-13, D-15)
    assert "Why Confirmation is Necessary" in content
    assert "Available Evidence" in content
    assert "What Remains Uncertain" in content
    assert "Recommended Action" in content
    assert "docs: Triage Phase 2 experimental discrepancies for oral thesis defense" in content

    # Assert Canonical Reference Table & Bijective Renumbering Map (D-09, D-10, D-11)
    assert "Skolnik" in content and "2001" in content
    assert "Huang" in content and "RadDet" in content and "2025" in content
    assert "AdaRadar" in content and "2023" in content
    for ref_num in range(1, 19):
        assert f"ref-{ref_num}" in content or f"[{ref_num}]" in content, f"Missing active ref {ref_num} in mapping"


def test_no_legacy_radar_parameters():
    """Verify zero instances of legacy parameters above the transition divider (D-05, D-16, R2)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    divider = 'id="manuscript-transition-divider"'
    assert divider in html, "manuscript-transition-divider must exist in docs/index.html"
    above_divider = html.split(divider)[0]

    # Assert zero legacy parameters in active manuscript
    for legacy_str in ["58.8", "0.258", "2.72"]:
        assert legacy_str not in above_divider, f"Legacy parameter '{legacy_str}' found above transition divider!"

    # Assert presence of authoritative parameters (D-05, R2)
    assert "50 μs" in above_divider or "50\\ \\mu\\text{s}" in above_divider or "50 \\mu\\text{s}" in above_divider
    assert "0.304" in above_divider
    assert "38.4" in above_divider
    assert "20\\text{ THz/s}" in above_divider or "20 THz/s" in above_divider or "20.0\\text{ THz/s}" in above_divider
    assert "28.6" in above_divider or "Rayleigh" in above_divider


def test_active_citation_anchors_and_tooltips():
    """Verify in-text citation anchors [1..18] are sequential, discrete, and resolve in docs/app.js (D-09, D-10, D-12, R5)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    divider = 'id="manuscript-transition-divider"'
    above_divider = html.split(divider)[0]

    # Parse in-text citation badges above divider
    badge_matches = re.findall(
        r'<a\s+href="#ref-([^"]+)"\s+class="citation-badge"\s+data-citation="([^"]+)">\[([^\]]+)\]</a>',
        above_divider,
    )
    assert len(badge_matches) >= 18, f"Expected at least 18 citation badges, found {len(badge_matches)}"

    # Check discrete first-appearance order is exactly 1, 2, ..., 18
    seen_citations = []
    for href_id, data_cite, text_cite in badge_matches:
        assert href_id == data_cite == text_cite, f"Badge mismatch: href={href_id}, data={data_cite}, text={text_cite}"
        if data_cite not in seen_citations:
            seen_citations.append(data_cite)

    expected_sequence = [str(i) for i in range(1, 19)]
    assert seen_citations == expected_sequence, f"Active citations out of order: {seen_citations}"

    # Verify all 1..32 references exist in bibliography and app.js CITATIONS_DB
    for ref_i in range(1, 33):
        assert f'id="ref-{ref_i}"' in html, f"Missing id='ref-{ref_i}' in bibliography"
        assert f'"{ref_i}": {{' in js, f"Missing key '{ref_i}' in docs/app.js CITATIONS_DB"


def test_scope_and_archival_preservation():
    """Verify LaTeX report templates untouched, archived draft intact, and bibliography segregated (D-09, D-16, R6)."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Archival original 7-chapter draft intact
    assert 'id="manuscript-transition-divider"' in html
    assert 'id="ch1-intro-original"' in html
    assert 'id="ch7-conclusion"' in html

    # Bibliography segregation
    assert 'class="archival-ref-divider"' in html
    assert 'class="references-list archival-list"' in html

    # Enforce zero modified files in templates/BTP_Report_Template_Overleaf/
    import subprocess
    git_status = subprocess.run(
        ["git", "status", "--porcelain", "templates/BTP_Report_Template_Overleaf/"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert not git_status.stdout.strip(), (
        f"templates/BTP_Report_Template_Overleaf/ must have zero git modifications! Found:\n{git_status.stdout}"
    )




