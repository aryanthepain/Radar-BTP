#!/usr/bin/env python3
"""
Deterministic Showcase Website Test Suite (tests/test_showcase_website.py)
--------------------------------------------------------------------------
Validates asset integrity, HTML semantic structure, local link resolution,
zero-build offline resilience, and master comparison table consistency
for the thesis presentation showcase in docs/.

Adheres to:
  - Requirement: PRES-WEB-03
  - Security Mitigations: T-01.2.1-05 (Broken Link & Asset Validation),
    T-01.2.1-06 (Fast Deterministic In-Memory Testing without Browser Drivers)
"""

import os
import unittest
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
PNG_MAGIC_BYTES = b"\x89PNG\r\n\x1a\n"


class HTMLLinkAndIDCollector(HTMLParser):
    """Parses HTML document collecting all element IDs and target references."""

    def __init__(self):
        super().__init__()
        self.declared_ids: Set[str] = set()
        self.internal_anchors: List[str] = []
        self.asset_sources: List[Tuple[str, str]] = []  # (tag, src/href)

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        if "id" in attr_dict:
            self.declared_ids.add(attr_dict["id"])

        if tag == "a" and "href" in attr_dict:
            href = attr_dict["href"]
            if href.startswith("#") and len(href) > 1:
                self.internal_anchors.append(href[1:])
            elif not href.startswith("#"):
                self.asset_sources.append(("a", href))

        if tag == "img" and "src" in attr_dict:
            self.asset_sources.append(("img", attr_dict["src"]))

        if tag == "script" and "src" in attr_dict:
            self.asset_sources.append(("script", attr_dict["src"]))

        if tag == "link" and attr_dict.get("rel") == "stylesheet" and "href" in attr_dict:
            self.asset_sources.append(("link", attr_dict["href"]))


class TestShowcaseWebsite(unittest.TestCase):
    """Deterministic smoke test suite for the thesis showcase presentation website."""

    def test_01_asset_pipeline_files_exist_and_valid(self):
        """Verifies all 25 assets in docs/assets/ exist, exceed size limits, and have valid headers."""
        # 1. Notebook 01 figures (9 PNGs)
        nb1_files = [
            "fig1_fmcw_chirp_physics.png",
            "fig2_raw_3d_cube_signal.png",
            "fig3_range_fft_windowing.png",
            "fig4_mti_clutter_suppression.png",
            "fig5_doppler_fft_rdm.png",
            "fig6_cfar_adaptive_detection.png",
            "fig7_aoa_music_super_res.png",
            "fig8_dbscan_clustering_bev.png",
            "fig9_pedestrian_micro_doppler.png",
        ]
        for fname in nb1_files:
            fpath = ASSETS_DIR / "nb1" / fname
            self.assertTrue(fpath.exists(), f"Missing Notebook 01 asset: {fpath}")
            self.assertGreater(fpath.stat().st_size, 10240, f"Asset too small: {fname}")
            with open(fpath, "rb") as f:
                header = f.read(8)
                self.assertEqual(header, PNG_MAGIC_BYTES, f"Invalid PNG magic bytes in {fname}")

        # 2. Notebook 02 figures (3 PNGs)
        nb2_files = [
            "plot1_synthetic_dataset_sample.png",
            "plot2_training_convergence.png",
            "plot3_model_inference_unseen.png",
        ]
        for fname in nb2_files:
            fpath = ASSETS_DIR / "nb2" / fname
            self.assertTrue(fpath.exists(), f"Missing Notebook 02 asset: {fpath}")
            self.assertGreater(fpath.stat().st_size, 10240, f"Asset too small: {fname}")
            with open(fpath, "rb") as f:
                header = f.read(8)
                self.assertEqual(header, PNG_MAGIC_BYTES, f"Invalid PNG magic bytes in {fname}")

        # 3. Notebook 03 benchmark artifacts (5 PNGs + 1 CSV)
        nb3_pngs = [
            "eda_raddet_samples.png",
            "validation_metrics_curves.png",
            "multi_snr_map_curves.png",
            "multi_snr_qualitative_grid.png",
            "unseen_frame_detections.png",
        ]
        for fname in nb3_pngs:
            fpath = ASSETS_DIR / "nb3" / fname
            self.assertTrue(fpath.exists(), f"Missing Notebook 03 PNG: {fpath}")
            self.assertGreater(fpath.stat().st_size, 10240, f"Asset too small: {fname}")
            with open(fpath, "rb") as f:
                header = f.read(8)
                self.assertEqual(header, PNG_MAGIC_BYTES, f"Invalid PNG magic bytes in {fname}")

        csv_path = ASSETS_DIR / "nb3" / "raddet_s128_table_iii.csv"
        self.assertTrue(csv_path.exists(), "Missing Table III CSV in docs/assets/nb3/")
        self.assertGreater(csv_path.stat().st_size, 200, "Table III CSV suspiciously small")

        # 4. Architecture and timeline diagrams (5 SVGs)
        diagram_files = [
            "nb1_top.svg",
            "nb2_top.svg",
            "nb3_top.svg",
            "nb2_comparison.svg",
            "timeline_evolution.svg",
        ]
        for fname in diagram_files:
            fpath = ASSETS_DIR / "diagrams" / fname
            self.assertTrue(fpath.exists(), f"Missing diagram SVG: {fpath}")
            self.assertGreater(fpath.stat().st_size, 500, f"Diagram SVG too small: {fname}")
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("<svg", content, f"SVG root missing in {fname}")
                self.assertIn("</svg>", content, f"Closing SVG tag missing in {fname}")

        # 5. Offline Prism.js vendor assets (2 files)
        prism_js = ASSETS_DIR / "vendor" / "prism.min.js"
        prism_css = ASSETS_DIR / "vendor" / "prism.min.css"
        self.assertTrue(prism_js.exists(), "Missing prism.min.js")
        self.assertTrue(prism_css.exists(), "Missing prism.min.css")
        self.assertGreater(prism_js.stat().st_size, 1024, "prism.min.js too small")
        self.assertGreater(prism_css.stat().st_size, 1024, "prism.min.css too small")

    def test_02_html_semantic_structure_and_links(self):
        """Verifies HTML document structure, mandatory sections, and confirms zero dead anchors/broken links."""
        index_path = DOCS_DIR / "index.html"
        self.assertTrue(index_path.exists(), "docs/index.html does not exist")

        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        collector = HTMLLinkAndIDCollector()
        collector.feed(html_content)

        # 1. Verify mandatory semantic section IDs
        required_sections = [
            "overview",
            "timeline",
            "notebook-01",
            "notebook-02",
            "notebook-03",
            "comparison",
            "conclusions",
        ]
        for sec_id in required_sections:
            self.assertIn(
                sec_id,
                collector.declared_ids,
                f"Mandatory semantic section ID '{sec_id}' missing from docs/index.html",
            )

        # 2. Verify all internal anchor hrefs point to declared IDs (zero dead anchors)
        for anchor in collector.internal_anchors:
            self.assertIn(
                anchor,
                collector.declared_ids,
                f"Dead anchor detected: href='#{anchor}' does not match any element ID in docs/index.html",
            )

        # 3. Verify all local asset src / href paths resolve to existing non-empty files (zero broken images)
        for tag, ref in collector.asset_sources:
            # Skip empty, placeholder, or external references
            if not ref or ref.startswith("http://") or ref.startswith("https://") or ref.startswith("mailto:"):
                continue

            # Strip query params or hash if present
            clean_ref = ref.split("?")[0].split("#")[0]
            resolved_file = (DOCS_DIR / clean_ref).resolve()

            self.assertTrue(
                resolved_file.exists(),
                f"Broken {tag} reference: '{ref}' resolves to non-existent file {resolved_file}",
            )
            self.assertGreater(
                resolved_file.stat().st_size,
                0,
                f"Referenced file is empty: {resolved_file}",
            )

    def test_03_zero_build_and_offline_resilience(self):
        """Verifies zero external CDN requests, design tokens, and JS handler declarations."""
        index_path = DOCS_DIR / "index.html"
        styles_path = DOCS_DIR / "styles.css"
        app_path = DOCS_DIR / "app.js"

        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        with open(styles_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        with open(app_path, "r", encoding="utf-8") as f:
            js_content = f.read()

        # Check for forbidden external URLs
        forbidden_substrings = [
            "http://",
            "https://",
            "unpkg.com",
            "cdnjs.cloudflare.com",
            "cdn.jsdelivr.net",
            "fonts.googleapis.com",
        ]
        for forbidden in forbidden_substrings:
            self.assertNotIn(
                forbidden,
                html_content,
                f"External URL '{forbidden}' detected in docs/index.html (violates offline resilience)",
            )
            self.assertNotIn(
                forbidden,
                css_content,
                f"External URL '{forbidden}' detected in docs/styles.css (violates offline resilience)",
            )

        # Check CSS Dark Cyber-Radar design tokens
        self.assertIn("--bg-primary: #0a0e17", css_content)
        self.assertIn("--accent-cyan: #00f0ff", css_content)
        self.assertIn("--accent-amber: #f59e0b", css_content)
        self.assertIn("#lightbox-modal", css_content)

        # Check JS handlers
        expected_handlers = [
            "initScrollSpy",
            "initLightbox",
            "initCodeCopy",
            "initBackToTop",
            "initMobileDrawer",
        ]
        for handler in expected_handlers:
            self.assertIn(
                handler,
                js_content,
                f"Required JavaScript function '{handler}' missing from docs/app.js",
            )

    def test_04_master_comparison_table_and_conclusions(self):
        """Verifies 7-metric master table dimensions and professor conclusion findings."""
        index_path = DOCS_DIR / "index.html"
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Verify table presence and notebook columns
        self.assertIn("master-table", html_content)
        self.assertIn("Notebook 01: Classical Radar DSP", html_content)
        self.assertIn("Notebook 02: Deep Learning Perception", html_content)
        self.assertIn("Notebook 03: RadDet S-128 Benchmark", html_content)

        # Verify all 7 required dimensions
        required_dimensions = [
            "Data Source",
            "Sensor Model",
            "Target Complexity",
            "Detection Paradigm",
            "Operational Latency",
            "Robustness to Clutter",
            "Key Engineering Limitations",
        ]
        for dim in required_dimensions:
            self.assertIn(dim, html_content, f"Dimension '{dim}' missing from comparison table")

        # Verify at least 6 conclusion cards
        conclusion_count = html_content.count("class=\"conclusion-card\"")
        self.assertGreaterEqual(
            conclusion_count,
            6,
            f"Expected at least 6 professor conclusion cards, found {conclusion_count}",
        )


if __name__ == "__main__":
    unittest.main()
