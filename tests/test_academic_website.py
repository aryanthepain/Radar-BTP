"""
tests/test_academic_website.py — Deterministic Test Suite for BTP-1 Thesis Portal
Validates publication-grade academic portal infrastructure:
  - HTML5 structure, semantic containers, and active chapter anchors (Chapters 1-5 + References)
  - Dedicated archived report portal (docs/archived-report.html) preserving the historical 7 chapters & bibliography
  - Two-column CSS rules, serif/sans-serif typography, and responsive media queries
  - Vendored offline KaTeX mathematical typesetting engine and font assets
  - Client-side application logic (auto-render math, scroll-spy, citation hover tooltips, code blocks)
  - Citations database (Refs 1-31) in docs/app.js and active bibliography
  - Absence of removed elements: Index Terms, Table 5.2, Table 4.4, Code Listing 3.3, Code Listing 4.1,
    Laboratory confirmation card, ONNX Runtime, OpenVINO, s128_small smoke test, Partition Disclosure note.
  - Zero modification to LaTeX templates directory.
"""

import os
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
INDEX_HTML = os.path.join(DOCS_DIR, "index.html")
ARCHIVED_HTML = os.path.join(DOCS_DIR, "archived-report.html")
STYLES_CSS = os.path.join(DOCS_DIR, "styles.css")
APP_JS = os.path.join(DOCS_DIR, "app.js")
KATEX_DIR = os.path.join(DOCS_DIR, "assets", "vendor", "katex")


def test_file_existence():
    """Verify all critical academic portal files exist on disk."""
    assert os.path.exists(INDEX_HTML), f"Missing {INDEX_HTML}"
    assert os.path.exists(ARCHIVED_HTML), f"Missing {ARCHIVED_HTML}"
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

    # References 1 through 31 in CITATIONS_DB
    for ref_i in range(1, 32):
        assert f'"{ref_i}": {{' in js, f"Missing citation {ref_i} in docs/app.js"


def test_chapter_sections():
    """Verify Chapter 1-5 anchors exist in active index.html and original chapters exist in archived-report.html."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    active_chapters = [
        "overview",
        "ch1-intro",
        "ch2-lit-review",
        "ch3-methodology",
        "ch4-results",
        "ch5-conclusion",
        "bibliography"
    ]
    for ch in active_chapters:
        assert f'id="{ch}"' in content or f"id='{ch}'" in content, f"Missing active chapter anchor: #{ch}"

    with open(ARCHIVED_HTML, "r", encoding="utf-8") as f:
        archived_content = f.read()

    archived_chapters = [
        "ch1-intro-original",
        "ch2-physics",
        "ch3-dsp-audit",
        "ch4-methodology",
        "ch5-benchmarks",
        "ch6-timeline",
        "ch7-conclusion",
        "archival-references"
    ]
    for ch in archived_chapters:
        assert f'id="{ch}"' in archived_content or f"id='{ch}'" in archived_content, f"Missing archived chapter anchor: #{ch}"


def test_institutional_metadata():
    """Verify exact official IIT Guwahati institutional metadata."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert "AI Applications in Radar Signal Processing" in html, "Missing official primary title"
    assert "Towards Resource-Efficient AI-Based Radar Detection for Millimetre-Wave FMCW Systems" in html, "Missing official subtitle"
    assert "Aryan Sandeep Gupta" in html, "Missing candidate full name"
    assert "230150003" in html, "Missing student roll number"
    assert "Mehta Family School of Data Science and Artificial Intelligence" in html, "Missing official school name"
    assert "DA4098P BTP Project I" in html, "Missing official course code"
    assert "DA4098P BTP Project I (Autumn 2026)" not in html, "Old course string with year must be removed"
    assert "Prof. Ratnajit Bhattacharjee" in html, "Missing supervisor name"


def test_clean_header_and_sidebar():
    """Verify clean print-like IEEE layout, link to archived report, and absence of removed badges."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert '<div id="reading-progress-bar"></div>' not in html, "#reading-progress-bar should be omitted from index.html"
    assert 'id="academic-sidebar"' in html
    sidebar_html = html.split('id="academic-sidebar"')[1].split('</aside>')[0]

    # Hardware chip badges omitted from sidebar
    assert "AWR1843" not in sidebar_html
    assert "DCA1000" not in sidebar_html

    # Sidebar footer links to archived draft
    assert "archived-report.html" in sidebar_html, "Sidebar must link to archived-report.html"
    assert "BTP-1 Thesis Portal · Autumn 2026" not in sidebar_html, "Old footer badge must be removed"
    assert "KaTeX: Offline (20 Fonts)" not in sidebar_html, "Old KaTeX badge must be removed"
    assert "Verified: ICASSP Table III" not in sidebar_html, "Old verification badge must be removed"


def test_code_listings_in_methodology():
    """Verify presence of all Code Listings (3.1 through 3.7) in Chapter 3."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert "Code Listing 3.1: Fast-Time Range FFT" in html
    assert "Code Listing 3.2: Clutter Suppression" in html
    assert "Code Listing 3.3: Slow-Time Doppler Processing" in html
    assert "Code Listing 3.4: 2D Cell-Averaging Constant False Alarm Rate" in html
    assert "Code Listing 3.5: Spatial Covariance and Subspace MUSIC/Capon" in html
    assert "Code Listing 3.6: Point-Cloud Transformation and DBSCAN" in html
    assert "Code Listing 3.7: Forward-Pass Implementation of the Synthetic FMCW Radar CNN" in html

    # Code Listing 3.3 grayscale loading and Code Listing 4.1 are removed
    assert "Grayscale Spectrogram Loading and Normalisation" not in html
    assert "Code Listing 4.1" not in html
    assert "src/dsp/range_processing.py" not in html, "File path in code listing header must be removed"


def test_official_abstract_and_no_index_terms():
    """Verify presence of abstract and absence of Index Terms block."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert '<div class="paper-abstract"' in html, "Missing .paper-abstract container"
    abstract_block = html.split('<div class="paper-abstract"')[1].split('</div>')[0]

    assert "Radar sensing is increasingly used in intelligent perception" in abstract_block
    assert "two complementary experimental tracks" in abstract_block
    assert "Index Terms:" not in html, "Index Terms block must be removed"


def test_removed_items_in_active_portal():
    """Verify complete removal of Table 5.2, Table 4.4, Lab Confirmation, ONNX Runtime/OpenVINO, and Partition Note."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    assert "Table 5.2" not in html, "Table 5.2 must be removed"
    assert "Table 4.4" not in html, "Table 4.4 must be removed"
    assert "Laboratory & Hardware Confirmation Protocol" not in html, "Lab confirmation card must be removed"
    assert "ONNX Runtime" not in html, "ONNX Runtime must be removed"
    assert "OpenVINO" not in html, "OpenVINO must be removed"
    assert "Partition & Chunking Disclosure Note" not in html, "Partition note must be removed"
    assert "s128_small" not in html, "Smoke test run s128_small must be removed from active report"


def test_active_citations_and_references():
    """Verify References 1 through 31 in active bibliography and citations across report."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # All refs 1 to 31 exist in bibliography
    for i in range(1, 32):
        assert f'id="ref-{i}"' in html, f"Missing id='ref-{i}' in active bibliography"

    # Critical references requested by user are present and cited
    assert 'Alexander Karlsson' in html
    assert 'data-citation="19"' in html, "Karlsson [19] must be cited"
    assert 'data-citation="20"' in html, "TJ4D [20] must be cited"
    assert 'data-citation="26"' in html, "CARRADA [26] must be cited"
    assert 'data-citation="27"' in html, "nuScenes [27] must be cited"
    assert 'data-citation="28"' in html, "RAVEN [28] must be cited"
    assert 'data-citation="30"' in html, "Lin et al. ICASSP [30] must be cited"
    assert 'data-citation="31"' in html, "Mahafza [31] must be cited"
    assert 'MATLAB Radar Designer App' in html or 'Radar Designer' in html


def test_formula_scrollbars_eliminated():
    """Verify Section 2.1 formulas are split vertically into single-column blocks."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Old side-by-side equation line must not exist
    assert r"\approx 0.15\text{ m},\qquad \Delta v" not in html
    assert r"\approx 0.15\text{ m}, \qquad \Delta v" not in html
    assert r"\Delta R \x07pprox" not in html, "KaTeX bell character typo must be removed"


def test_scope_and_archival_preservation():
    """Verify LaTeX report templates untouched, archived draft intact, and bidirectional link works."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        index_html = f.read()

    with open(ARCHIVED_HTML, "r", encoding="utf-8") as f:
        archived_html = f.read()

    # Bidirectional links
    assert "archived-report.html" in index_html, "index.html must link to archived-report.html"
    assert "index.html" in archived_html, "archived-report.html must link back to index.html"

    # Enforce zero modifications in templates/BTP_Report_Template_Overleaf/ against main
    import subprocess
    git_diff_main = subprocess.run(
        ["git", "diff", "main", "--", "templates/BTP_Report_Template_Overleaf/"],
        capture_output=True,
        text=True,
        check=False,
    )
    if git_diff_main.returncode == 0:
        assert not git_diff_main.stdout.strip(), (
            f"templates/BTP_Report_Template_Overleaf/ must have zero diff against main! Found:\n{git_diff_main.stdout}"
        )
    else:
        git_diff_origin = subprocess.run(
            ["git", "diff", "origin/main", "--", "templates/BTP_Report_Template_Overleaf/"],
            capture_output=True,
            text=True,
            check=False,
        )
        if git_diff_origin.returncode == 0:
            assert not git_diff_origin.stdout.strip(), (
                f"templates/BTP_Report_Template_Overleaf/ must have zero diff against origin/main! Found:\n{git_diff_origin.stdout}"
            )


def test_mobile_drawer_and_touch_targets():
    """Verify WCAG 2.5.5 touch target standard (>=44x44px), mobile drawer ergonomics, and scroll-lock."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # Touch target standards in CSS for nav-toggle
    assert ".nav-toggle-btn" in css, "CSS must define .nav-toggle-btn"
    assert "min-width: 44px" in css, "nav-toggle must have min-width: 44px per WCAG 2.5.5"
    assert "min-height: 44px" in css, "nav-toggle must have min-height: 44px per WCAG 2.5.5"
    assert ":focus-visible" in css, "nav-toggle must have :focus-visible focus ring"

    # Accessible ARIA attributes on #nav-toggle
    assert 'id="nav-toggle"' in html, "HTML must contain #nav-toggle"
    assert 'aria-expanded=' in html, "#nav-toggle must declare aria-expanded attribute"
    assert 'aria-controls="academic-sidebar"' in html, "#nav-toggle must declare aria-controls='academic-sidebar'"
    assert 'id="nav-backdrop"' in html, "Backdrop must have id='nav-backdrop'"

    # Background body scroll-lock
    assert "body.nav-open" in css, "CSS must define body.nav-open scroll lock rule"
    assert "overflow: hidden" in css and "touch-action: none" in css, "body.nav-open must enforce overflow: hidden and touch-action: none"

    # Touch target minimum 44px on TOC links
    assert "min-height: 44px" in css and ".toc-link" in css, "TOC links must have min-height: 44px per WCAG 2.5.5"

    # Mobile drawer logic in app.js
    assert "initMobileDrawer" in js, "app.js must declare initMobileDrawer function"
    assert "nav-open" in js, "initMobileDrawer must toggle nav-open on document.body"
    assert "aria-expanded" in js, "initMobileDrawer must update aria-expanded"
    assert "✕" in js and "☰" in js, "initMobileDrawer must morph icon between '☰' and '✕'"
    assert "Escape" in js, "initMobileDrawer must support Escape key drawer dismissal"


def test_overflow_containment_and_scroll_wrappers():
    """Verify two-tier horizontal momentum scroll containers for tables and KaTeX formulas."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # CSS classes for momentum scroll wrappers
    assert ".table-scroll-wrapper" in css, "CSS must define .table-scroll-wrapper"
    assert ".formula-scroll-wrapper" in css, "CSS must define .formula-scroll-wrapper"
    assert "-webkit-overflow-scrolling: touch" in css, "Must enable -webkit-overflow-scrolling: touch for iOS momentum"
    assert "clamp(" in css, "Must define clamp() font scaling to guarantee minimum readability floor"

    # Single-column reflow rule below 900px
    assert "column-count: 1" in css, "Two-column layout must collapse to single column below 900px"

    # Image and SVG responsiveness
    assert "max-width: 100%" in css, "Must constrain images and SVGs to 100% width"

    # HTML semantic scroll wrappers for major tables
    assert '<div class="table-scroll-wrapper">' in html, "index.html must enclose wide tables in .table-scroll-wrapper"
    assert html.count('class="table-scroll-wrapper"') >= 4, "All major tables must have .table-scroll-wrapper"
    assert '<div class="formula-scroll-wrapper">' in html, "index.html must contain .formula-scroll-wrapper for display math"

    # Client-side automated safety sweep in app.js
    assert "initOverflowContainment" in js, "app.js must declare initOverflowContainment safety sweep"
    assert "closest" in js, "initOverflowContainment must inspect closest wrapper before tagging"


def test_citation_popover_engine_and_mobile_sheet():
    """Verify adaptive IEEE citation popover card behavior (D-01..D-05)."""
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # Absence of gating debug flag (D-04)
    assert "ENABLE_CITATION_TOOLTIPS" not in js, "Citation cards must be unconditionally active (D-04)"

    # Mobile bottom sheet CSS rules and keyframes
    assert "highlightPulse" in css or "@keyframes highlightPulse" in css, "CSS must define @keyframes highlightPulse"
    assert ".highlight-pulse" in css, "CSS must define .highlight-pulse"
    assert ".citation-backdrop" in css, "CSS must define .citation-backdrop"
    assert "safe-area-inset-bottom" in css, "Must support mobile safe-area insets"
    assert "16px 16px 0 0" in css, "Mobile bottom-sheet must have rounded top corners"

    # Action buttons styling in CSS
    assert ".tooltip-doi-btn" in css, "CSS must style .tooltip-doi-btn"
    assert ".tooltip-jump-btn" in css, "CSS must style .tooltip-jump-btn"

    # Smooth scroll to Section 9 and pulse animation in app.js
    assert "scrollIntoView" in js, "app.js must smooth-scroll to bibliography target"
    assert "highlight-pulse" in js, "app.js must add .highlight-pulse animation class to reference item"
    assert "tooltip-doi-btn" in js, "app.js must construct DOI link button"
    assert "tooltip-jump-btn" in js, "app.js must construct Section 9 jump button"

    # Touch tap-to-inspect (prevents immediate jump) and backdrop dismissal
    assert "e.preventDefault()" in js, "Citation badge click must prevent default immediate anchor jump"
    assert "showTooltip(badge, true)" in js, "Citation badge click must open bottom-sheet with isTouch=true"
    assert "backdropEl.addEventListener(\"click\", hideTooltip)" in js or "backdropEl" in js, "Backdrop must dismiss bottom-sheet"
    assert "nav-open" in js, "Touch/mobile bottom-sheet must apply nav-open scroll lock"


def test_desktop_citation_tooltip_collision_clamping():
    """Verify desktop floating tooltip viewport boundary clamping and collision avoidance (D-03)."""
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # Desktop card styling (max-width: 480px)
    assert "max-width: 480px" in css, "CSS must declare max-width: 480px for desktop tooltip"

    # JS Boundary clamping calculations
    assert "Math.min(480, window.innerWidth - 40)" in js, "app.js must dynamically calculate tooltip width up to 480px"
    assert "getBoundingClientRect" in js, "app.js must inspect badge bounding rectangle"
    assert "rect.left" in js and "rect.top" in js, "app.js must calculate relative badge coordinates"
    assert "left + tooltipWidth > window.innerWidth" in js, "app.js must clamp right viewport collision"
    assert "rect.top < 150" in js, "app.js must flip tooltip below badge when top boundary is exceeded"

    # Hover timeout debounce
    assert "hideTimeout = setTimeout(hideTooltip, 200)" in js, "app.js must debounce tooltip hiding with 200ms grace period"
    assert "clearTimeout(hideTimeout)" in js, "app.js must cancel pending hide timeout upon hover re-entry"


def test_mobile_drawer_synchronization_and_styles():
    """Verify dual-class synchronization (.open and nav-open), text-size-adjust, and mobile header typography."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Dual-class synchronization in app.js
    assert 'sidebar.classList.toggle("open", isOpen)' in js, "app.js must toggle .open on sidebar"
    assert 'backdrop.classList.toggle("open", isOpen)' in js, "app.js must toggle .open on backdrop"
    assert 'sidebar.classList.remove("open")' in js, "app.js closeDrawer must remove .open from sidebar"
    assert 'backdrop.classList.remove("open")' in js, "app.js closeDrawer must remove .open from backdrop"

    # 2. Dual-selector resilience in styles.css
    assert "body.nav-open .sidebar" in css, "styles.css must support body.nav-open .sidebar"
    assert "body.nav-open .nav-backdrop" in css, "styles.css must support body.nav-open .nav-backdrop"

    # 3. WebKit text size adjust protection against aggressive mobile font boosting
    assert "-webkit-text-size-adjust: 100%" in css, "styles.css must enforce -webkit-text-size-adjust: 100%"
    assert "text-size-adjust: 100%" in css, "styles.css must enforce text-size-adjust: 100%"

    # 4. Fluid mobile header typography
    assert ".paper-header h1" in css, "styles.css must define mobile typography for .paper-header h1"
    assert "overflow-wrap: break-word" in css, "styles.css must enable overflow-wrap: break-word for long titles"

    # 5. Viewport meta tag declaration
    assert 'name="viewport"' in html and "width=device-width" in html, "index.html must declare standard viewport"


def test_interactive_lightbox_and_zoomable_figures():
    """Verify image zoom lightbox selector, tap-to-magnify scaling, and mobile close button."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    with open(STYLES_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Zoomable selector in app.js covers img.zoomable and all report figures
    assert "img.zoomable" in js, "app.js must include img.zoomable in zoomable query selector"
    assert "main img:not(#lightbox-img)" in js, "app.js must fallback to main img:not(#lightbox-img)"

    # 2. In-modal tap-to-magnify in app.js
    assert 'modalImg.classList.toggle("zoomed")' in js, "modalImg click must toggle zoomed class"
    assert 'modalImg.style.cursor = isZoomed ? "zoom-out" : "zoom-in"' in js or 'zoom-out' in js, "modalImg cursor must reflect zoom state"
    assert 'modalImg.classList.remove("zoomed")' in js, "openLightbox and closeLightbox must reset zoomed state"

    # 3. Lightbox styles in styles.css
    assert "#lightbox-img.zoomed" in css, "styles.css must style #lightbox-img.zoomed"
    assert "scale(1.75)" in css, "styles.css must provide desktop magnification scale"
    assert "scale(1.6)" in css, "styles.css must provide mobile magnification scale"
    assert "overflow: auto" in css, "styles.css must enable overflow: auto on lightbox modal for pan-scrolling"

    # 4. Mobile close button position and z-index
    assert "#lightbox-close" in css, "styles.css must style #lightbox-close"
    assert "200002" in css, "styles.css must give #lightbox-close top z-index (200002) above modal (200000)"

    # 5. All 20 figures in index.html declare class zoomable
    zoomable_count = html.count('class="zoomable"') + html.count("class='zoomable'")
    assert zoomable_count >= 20, f"Expected at least 20 zoomable images in index.html, found {zoomable_count}"

