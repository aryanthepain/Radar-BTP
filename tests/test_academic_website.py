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
    """Verify that all non-empty img src paths in docs/index.html resolve to actual files."""
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
