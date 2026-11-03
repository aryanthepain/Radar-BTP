#!/usr/bin/env python3
"""
Automated Showcase Asset Pipeline (scripts/export_showcase_assets.py)
--------------------------------------------------------------------
Extracts and synchronizes all visual figures, pre-rendered vector diagrams,
benchmark tables, and offline vendor libraries for the BTP Radar Perception
showcase presentation website in docs/assets/.

Adheres to:
  - Requirement: PRES-WEB-01
  - Security Mitigations: T-01.2.1-01 (Path Traversal / Canonicalization),
    T-01.2.1-02 (Missing Asset Fallback & PNG Magic Byte Verification)
"""

import base64
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Base repository root and output directory
REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"

PNG_MAGIC_BYTES = b"\x89PNG\r\n\x1a\n"


def _safe_resolve_target(base_dir: Path, filename: str) -> Path:
    """Canonicalize destination path and prevent path traversal outside base_dir (T-01.2.1-01)."""
    base_resolved = base_dir.resolve()
    target_path = (base_dir / filename).resolve()
    if not str(target_path).startswith(str(base_resolved)):
        raise ValueError(f"Path traversal detected: {filename} resolves outside {base_dir}")
    return target_path


def extract_notebook_images(
    notebook_path: Path, output_dir: Path, figure_mapping: Dict[int, str]
) -> List[Path]:
    """
    Extracts base64 encoded PNG images from designated cell outputs of a Jupyter notebook.
    Validates PNG magic bytes and verifies minimum file size threshold (>10 KB).
    """
    notebook_path = notebook_path.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not notebook_path.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    with open(notebook_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)

    extracted_files = []
    cells = nb_data.get("cells", [])

    for cell_idx, filename in figure_mapping.items():
        target_path = _safe_resolve_target(output_dir, filename)

        if cell_idx >= len(cells):
            raise IndexError(f"Cell index {cell_idx} exceeds notebook cell count ({len(cells)})")

        cell = cells[cell_idx]
        png_b64 = None

        for out in cell.get("outputs", []):
            data = out.get("data", {})
            if "image/png" in data:
                img_data = data["image/png"]
                if isinstance(img_data, list):
                    png_b64 = "".join(img_data)
                else:
                    png_b64 = img_data
                break

        if not png_b64:
            raise ValueError(f"No image/png output found in cell {cell_idx} for {filename}")

        # Decode base64
        image_bytes = base64.b64decode(png_b64)

        # Validate PNG magic bytes (T-01.2.1-01 / T-01.2.1-02)
        if not image_bytes.startswith(PNG_MAGIC_BYTES):
            raise ValueError(f"Extracted image {filename} fails PNG magic bytes check!")

        if len(image_bytes) < 10240:
            raise ValueError(f"Extracted image {filename} is suspiciously small ({len(image_bytes)} bytes)")

        with open(target_path, "wb") as f_out:
            f_out.write(image_bytes)

        extracted_files.append(target_path)
        print(f"  [OK] Extracted {filename} ({len(image_bytes) / 1024:.1f} KB) -> {target_path.name}")

    return extracted_files


def sync_benchmark_assets(source_dir: Path, output_dir: Path) -> List[Path]:
    """
    Copies pre-computed benchmark artifacts from data/benchmark_results/s128_full/
    into docs/assets/nb3/.
    """
    source_dir = source_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    benchmark_files = [
        "eda_raddet_samples.png",
        "validation_metrics_curves.png",
        "multi_snr_map_curves.png",
        "multi_snr_qualitative_grid.png",
        "unseen_frame_detections.png",
        "raddet_s128_table_iii.csv",
    ]

    synced = []
    for fname in benchmark_files:
        src = source_dir / fname
        dst = _safe_resolve_target(output_dir, fname)

        if not src.exists():
            raise FileNotFoundError(f"Required benchmark asset not found: {src}")

        shutil.copy2(src, dst)

        # Integrity checks
        if fname.endswith(".png"):
            with open(dst, "rb") as f:
                header = f.read(8)
                if header != PNG_MAGIC_BYTES:
                    raise ValueError(f"Benchmark file {fname} fails PNG header check")
            if dst.stat().st_size < 10240:
                raise ValueError(f"Benchmark PNG {fname} is smaller than 10 KB")
        elif fname.endswith(".csv"):
            if dst.stat().st_size < 200:
                raise ValueError(f"Benchmark CSV {fname} is suspiciously small")

        synced.append(dst)
        print(f"  [OK] Synced {fname} ({dst.stat().st_size / 1024:.1f} KB)")

    return synced


def sync_architecture_diagrams(output_dir: Path) -> List[Path]:
    """
    Synchronizes cached Mermaid architecture SVG diagrams into docs/assets/diagrams/.
    """
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    cache_dir = REPO_ROOT / ".cache" / "mermaid"
    diagram_mapping = {
        "nb1_top.svg": "788875972ad3236a.svg",
        "nb2_top.svg": "2dc9a708c48151bb.svg",
        "nb3_top.svg": "1f5d78de94a882db.svg",
        "nb2_comparison.svg": "3a007cbc70692910.svg",
    }

    synced = []
    for target_name, hash_file in diagram_mapping.items():
        src = cache_dir / hash_file
        dst = _safe_resolve_target(output_dir, target_name)

        if not src.exists():
            raise FileNotFoundError(f"Cached diagram SVG not found: {src}")

        with open(src, "r", encoding="utf-8") as f:
            svg_content = f.read()

        if "<svg" not in svg_content or "</svg>" not in svg_content:
            raise ValueError(f"Cached diagram {hash_file} is not valid SVG")

        with open(dst, "w", encoding="utf-8") as f:
            f.write(svg_content)

        synced.append(dst)
        print(f"  [OK] Synced diagram {target_name} ({len(svg_content) / 1024:.1f} KB)")

    return synced


def generate_timeline_svg(output_path: Path) -> Path:
    """
    Renders the 3-Stage Evolution Timeline SVG (timeline_evolution.svg) in Dark Cyber-Radar aesthetic.
    Dimensions: 1200 x 360 viewBox.
    """
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" width="100%" height="100%">
  <defs>
    <!-- Dark Cyber-Radar Gradients & Glow Filters -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0e17" />
      <stop offset="100%" stop-color="#070a10" />
    </linearGradient>

    <linearGradient id="card-grad-1" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#111c30" />
      <stop offset="100%" stop-color="#0b1220" />
    </linearGradient>

    <linearGradient id="card-grad-2" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#171e38" />
      <stop offset="100%" stop-color="#0d1224" />
    </linearGradient>

    <linearGradient id="card-grad-3" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10252b" />
      <stop offset="100%" stop-color="#0a171c" />
    </linearGradient>

    <linearGradient id="line-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="50%" stop-color="#818cf8" />
      <stop offset="100%" stop-color="#00f0ff" />
    </linearGradient>

    <filter id="cyan-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="pulse-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .title-text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 800; font-size: 14px; letter-spacing: 2px; text-transform: uppercase; fill: #94a3b8; }
    .stage-title { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 16px; fill: #f8fafc; }
    .stage-sub { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; fill: #94a3b8; }
    .bullet-text { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; fill: #cbd5e1; }
    .badge-text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; }
    .limit-title { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; fill: #f43f5e; }
    .culm-title { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; fill: #10b981; }
    .limit-text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; fill: #fda4af; }
    .culm-text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; fill: #6ee7b7; }
  </style>

  <!-- Background Canvas -->
  <rect width="1200" height="360" rx="12" fill="url(#bg-grad)" stroke="#1e293b" stroke-width="1.5" />

  <!-- Radar Grid Background Pattern -->
  <g opacity="0.12" stroke="#00f0ff" stroke-width="0.75" stroke-dasharray="3 3">
    <line x1="50" y1="50" x2="1150" y2="50" />
    <line x1="50" y1="310" x2="1150" y2="310" />
    <line x1="220" y1="20" x2="220" y2="340" />
    <line x1="600" y1="20" x2="600" y2="340" />
    <line x1="980" y1="20" x2="980" y2="340" />
  </g>

  <!-- Header Banner -->
  <text x="600" y="34" text-anchor="middle" class="title-text">End-to-End Radar Perception Architectural Evolution</text>

  <!-- Connecting Backbone Line -->
  <line x1="220" y1="56" x2="980" y2="56" stroke="url(#line-grad)" stroke-width="3" filter="url(#cyan-glow)" />

  <!-- Node 1 Pulse -->
  <circle cx="220" cy="56" r="10" fill="#0f172a" stroke="#38bdf8" stroke-width="3" filter="url(#cyan-glow)" />
  <circle cx="220" cy="56" r="4" fill="#38bdf8" />

  <!-- Node 2 Pulse -->
  <circle cx="600" cy="56" r="10" fill="#0f172a" stroke="#818cf8" stroke-width="3" filter="url(#cyan-glow)" />
  <circle cx="600" cy="56" r="4" fill="#818cf8" />

  <!-- Node 3 Pulse -->
  <circle cx="980" cy="56" r="12" fill="#0f172a" stroke="#00f0ff" stroke-width="3.5" filter="url(#pulse-glow)" />
  <circle cx="980" cy="56" r="5" fill="#00f0ff" />

  <!-- ==================== STAGE 1 CARD ==================== -->
  <g transform="translate(40, 80)">
    <rect width="350" height="252" rx="10" fill="url(#card-grad-1)" stroke="#1e293b" stroke-width="1.5" />
    
    <!-- Stage Badge -->
    <rect x="16" y="14" width="112" height="20" rx="4" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1" />
    <text x="72" y="28" text-anchor="middle" class="badge-text" fill="#38bdf8">Stage 1 · Zero Data</text>

    <!-- Stage Title -->
    <text x="16" y="54" class="stage-title">Analytical Point Targets</text>
    <text x="16" y="70" class="stage-sub">01_radar_classical_dsp · First-Principles Physics</text>

    <!-- Divider -->
    <line x1="16" y1="80" x2="334" y2="80" stroke="#1e293b" stroke-width="1" />

    <!-- Feature Bullets -->
    <text x="16" y="100" class="bullet-text"><tspan fill="#38bdf8">▶</tspan> Deterministic 77 GHz FMCW signal physics</text>
    <text x="16" y="118" class="bullet-text"><tspan fill="#38bdf8">▶</tspan> Fast-Time Range FFT &amp; 2D Slow-Time Doppler</text>
    <text x="16" y="136" class="bullet-text"><tspan fill="#38bdf8">▶</tspan> MTI 2-pulse stationary clutter suppression</text>
    <text x="16" y="154" class="bullet-text"><tspan fill="#38bdf8">▶</tspan> 2D CA-CFAR adaptive sliding threshold</text>
    <text x="16" y="172" class="bullet-text"><tspan fill="#38bdf8">▶</tspan> Spatial MUSIC sub-degree super-resolution</text>

    <!-- Limitation Box -->
    <rect x="16" y="190" width="318" height="48" rx="6" fill="#881337" fill-opacity="0.2" stroke="#e11d48" stroke-width="1" />
    <text x="26" y="206" class="limit-title">⚠ Fundamental Bottleneck</text>
    <text x="26" y="224" class="limit-text">Hand-crafted CFAR thresholds; zero semantic classification.</text>
  </g>

  <!-- ==================== STAGE 2 CARD ==================== -->
  <g transform="translate(425, 80)">
    <rect width="350" height="252" rx="10" fill="url(#card-grad-2)" stroke="#1e293b" stroke-width="1.5" />
    
    <!-- Stage Badge -->
    <rect x="16" y="14" width="138" height="20" rx="4" fill="#4338ca" fill-opacity="0.25" stroke="#818cf8" stroke-width="1" />
    <text x="85" y="28" text-anchor="middle" class="badge-text" fill="#818cf8">Stage 2 · Synthetic Data</text>

    <!-- Stage Title -->
    <text x="16" y="54" class="stage-title">Synthetic FMCW Simulation</text>
    <text x="16" y="70" class="stage-sub">02_radar_deep_learning_detection · Multi-Task CNN</text>

    <!-- Divider -->
    <line x1="16" y1="80" x2="334" y2="80" stroke="#1e293b" stroke-width="1" />

    <!-- Feature Bullets -->
    <text x="16" y="100" class="bullet-text"><tspan fill="#818cf8">▶</tspan> High-fidelity 3D radar cube simulation</text>
    <text x="16" y="118" class="bullet-text"><tspan fill="#818cf8">▶</tspan> Kinematic pedestrian micro-Doppler gait STFT</text>
    <text x="16" y="136" class="bullet-text"><tspan fill="#818cf8">▶</tspan> Continuous 2D Gaussian heatmap splatting</text>
    <text x="16" y="154" class="bullet-text"><tspan fill="#818cf8">▶</tspan> RadarObjectDetectorCNN anchor-free multi-task</text>
    <text x="16" y="172" class="bullet-text"><tspan fill="#818cf8">▶</tspan> Joint focal heatmap &amp; Smooth-L1 box loss</text>

    <!-- Limitation Box -->
    <rect x="16" y="190" width="318" height="48" rx="6" fill="#881337" fill-opacity="0.2" stroke="#e11d48" stroke-width="1" />
    <text x="26" y="206" class="limit-title">⚠ Sim-to-Real Domain Gap</text>
    <text x="26" y="224" class="limit-text">Idealized Gaussian target splats; misses multi-path clutter.</text>
  </g>

  <!-- ==================== STAGE 3 CARD ==================== -->
  <g transform="translate(810, 80)">
    <rect width="350" height="252" rx="10" fill="url(#card-grad-3)" stroke="#00f0ff" stroke-width="1.8" filter="url(#cyan-glow)" />
    
    <!-- Stage Badge -->
    <rect x="16" y="14" width="138" height="20" rx="4" fill="#065f46" fill-opacity="0.3" stroke="#00f0ff" stroke-width="1" />
    <text x="85" y="28" text-anchor="middle" class="badge-text" fill="#00f0ff">Stage 3 · Real Benchmark</text>

    <!-- Stage Title -->
    <text x="16" y="54" class="stage-title">RadDet ICASSP 2025</text>
    <text x="16" y="70" class="stage-sub">03_raddet_spectrum_detection · YOLOv9 Line-Rate</text>

    <!-- Divider -->
    <line x1="16" y1="80" x2="334" y2="80" stroke="#1e293b" stroke-width="1" />

    <!-- Feature Bullets -->
    <text x="16" y="100" class="bullet-text"><tspan fill="#00f0ff">▶</tspan> 20,000 real automotive radar spectrograms</text>
    <text x="16" y="118" class="bullet-text"><tspan fill="#00f0ff">▶</tspan> 11 contested radar waveform modulations</text>
    <text x="16" y="136" class="bullet-text"><tspan fill="#00f0ff">▶</tspan> Ultralytics YOLOv9-C with PGI backbone</text>
    <text x="16" y="154" class="bullet-text"><tspan fill="#00f0ff">▶</tspan> Automated multi-SNR sweep (-20 dB to +20 dB)</text>
    <text x="16" y="172" class="bullet-text"><tspan fill="#00f0ff">▶</tspan> 892.9 FPS (1.12 ms) single-frame latency profile</text>

    <!-- Culmination Box -->
    <rect x="16" y="190" width="318" height="48" rx="6" fill="#064e3b" fill-opacity="0.3" stroke="#10b981" stroke-width="1" />
    <text x="26" y="206" class="culm-title">★ Research Culmination</text>
    <text x="26" y="224" class="culm-text">Line-rate real-time cognitive EW; Table III verified.</text>
  </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"  [OK] Generated timeline vector graphic: {output_path.name} ({len(svg_content) / 1024:.1f} KB)")
    return output_path


def vendor_prism_assets(output_dir: Path) -> Tuple[Path, Path]:
    """
    Vendors offline Prism.js syntax highlighter and Dark Cyber-Radar theme CSS
    into docs/assets/vendor/ to eliminate external network dependencies (D-08).
    """
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    prism_js_path = _safe_resolve_target(output_dir, "prism.min.js")
    prism_css_path = _safe_resolve_target(output_dir, "prism.min.css")

    # Production-grade self-contained Prism.js core + Python, Bash, JSON grammar highlighters
    prism_js_content = """/* Prism.js 1.29.0 - Offline Vendored Core + Python/Bash/JSON/Line-Numbers */
var _self="undefined"!=typeof window?window:"undefined"!=typeof WorkerGlobalScope&&self instanceof WorkerGlobalScope?self:{},Prism=function(e){var n=/(?:^|\\s)lang(?:uage)?-([\\w-]+)(?=\\s|$)/i,t=0,r={},a={manual:e.Prism&&e.Prism.manual,disableWorkerMessageHandler:e.Prism&&e.Prism.disableWorkerMessageHandler,util:{encode:function e(n){return n instanceof s?new s(n.type,e(n.content),n.alias):Array.isArray(n)?n.map(e):n.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/\\u00a0/g," ")},type:function(e){return Object.prototype.toString.call(e).slice(8,-1)},objId:function(e){return e.__id||Object.defineProperty(e,"__id",{value:++t}),e.__id},clone:function e(n,t){var r,s;switch(t=t||{},a.util.type(n)){case"Object":if(s=a.util.objId(n),t[s])return t[s];for(var i in r={},t[s]=r,n)n.hasOwnProperty(i)&&(r[i]=e(n[i],t));return r;case"Array":return s=a.util.objId(n),t[s]?t[s]:(r=[],t[s]=r,n.forEach((function(n,a){r[a]=e(n,t)})),r);default:return n}}},languages:{plain:r,plaintext:r,text:r,txt:r,extend:function(e,n){var t=a.util.clone(a.languages[e]);for(var r in n)t[r]=n[r];return t},insertBefore:function(e,n,t,r){var s=(r=r||a.languages)[e],i={};for(var l in s)if(s.hasOwnProperty(l)){if(l==n)for(var o in t)t.hasOwnProperty(o)&&(i[o]=t[o]);t.hasOwnProperty(l)||(i[l]=s[l])}var u=r[e];return r[e]=i,a.languages.DFS(a.languages,(function(n,t){t===u&&n!=e&&(this[n]=i)})),i},DFS:function e(n,t,r,s){s=s||{};var i=a.util.objId;for(var l in n)if(n.hasOwnProperty(l)){t.call(n,l,n[l],r||l);var o=n[l],u=a.util.type(o);"Object"!==u||s[i(o)]?"Array"!==u||s[i(o)]||(s[i(o)]=!0,e(o,t,l,s)):(s[i(o)]=!0,e(o,t,l,s))}}},plugins:{},highlightAll:function(e,n){a.highlightAllUnder(document,e,n)},highlightAllUnder:function(e,n,t){var r=a.util.currentScript();if(r){var s=r.hasAttribute("data-manual");if(s)return}for(var i,l=e.querySelectorAll('code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code'),o=0;i=l[o++];)a.highlightElement(i,!0===n,t)},highlightElement:function(n,t,r){var s=a.util.getLanguage(n),i=a.languages[s];a.util.setLanguage(n,s);var l=n.parentElement;l&&"pre"===l.nodeName.toLowerCase()&&a.util.setLanguage(l,s);var o=n.textContent,u={element:n,language:s,grammar:i,code:o};function c(e){u.highlightedCode=e,a.hooks.run("before-insert",u),u.element.innerHTML=u.highlightedCode,a.hooks.run("after-highlight",u),a.hooks.run("complete",u),r&&r.call(u.element)}if(a.hooks.run("before-sanity-check",u),(l=u.element.parentElement)&&"pre"===l.nodeName.toLowerCase()&&!l.hasAttribute("tabindex")&&l.setAttribute("tabindex","0"),!u.code)return a.hooks.run("complete",u),void(r&&r.call(u.element));if(a.hooks.run("before-highlight",u),u.grammar)if(t&&e.Worker){var g=new Worker(a.filename);g.onmessage=function(e){c(e.data)},g.postMessage(JSON.stringify({language:u.language,code:u.code,immediateClose:!0}))}else c(a.highlight(u.code,u.grammar,u.language));else c(a.util.encode(u.code))},highlight:function(e,n,t){var r={code:e,grammar:n,language:t};if(a.hooks.run("before-tokenize",r),!r.grammar)throw new Error('The language "'+r.language+'" has no grammar.');return r.tokens=a.tokenize(r.code,r.grammar),a.hooks.run("after-tokenize",r),s.stringify(a.util.encode(r.tokens),r.language)},tokenize:function(e,n){var t=n.rest;if(t){for(var r in t)n[r]=t[r];delete n.rest}var a=new i;return l(a,a.head,e),o(e,a,n,a.head,0),function(e){var n=[],t=e.head.next;for(;t!==e.tail;)n.push(t.value),t=t.next;return n}(a)},hooks:{all:{},add:function(e,n){var t=a.hooks.all;t[e]=t[e]||[],t[e].push(n)},run:function(e,n){var t=a.hooks.all[e];if(t&&t.length)for(var r,s=0;r=t[s++];)r(n)}}};function s(e,n,t,r){this.type=e,this.content=n,this.alias=t,this.length=0|(r||"").length}function i(){var e={value:null,prev:null,next:null},n={value:null,prev:e,next:null};e.next=n,this.head=e,this.tail=n,this.length=0}function l(e,n,t){var r=n.next,a={value:t,prev:n,next:r};n.next=a,r.prev=a,e.length++}function o(e,n,t,r,s){for(var i in t)if(t.hasOwnProperty(i)&&t[i]){var l=t[i];l=Array.isArray(l)?l:[l];for(var o=0;o<l.length;++o){if(s>=e.length)return;var u=l[o],c=u.pattern||u,g=u.inside,p=Boolean(u.lookbehind),d=u.greedy,m=u.alias;if(d&&!c.global){var h=c.toString().match(/[imsuy]*$/)[0];c=RegExp(c.source,h+"g")}for(var f=r.next;f!==n.tail;f=f.next){if(e.length<=s)return;if(!(f.value.length<=0)){var b=f.value;if(d){c.lastIndex=s;var v=c.exec(e);if(!v||v.index>=s+b.length)break;var k=v.index+(p&&v[1]?v[1].length:0),y=v[0].length-(p&&v[1]?v[1].length:0),w=s;for(;w+f.value.length<=k;)w+=f.value.length,f=f.next;if(s=w,f.value instanceof s)continue;var _=f;for(;w<k+y;)w+=_.value.length,_.next!==n.tail&&(_=_.next);var x=e.slice(k,k+y);b=x}else{var v=c.exec(b);if(!v)continue;var k=v.index+(p&&v[1]?v[1].length:0),y=v[0].length-(p&&v[1]?v[1].length:0)}var C=b.slice(0,k),S=b.slice(k+y),A=g?a.tokenize(b.slice(k,k+y),g):new s(i,g?a.tokenize(b.slice(k,k+y),g):b.slice(k,k+y),m,b.slice(k,k+y));if(C&&l(n,f.prev,C),f.value=A,S&&l(n,f,S),d&&(_=f.next,f!==_))for(;f.next!==_;)f=f.next,f.prev.next=f.next,f.next.prev=f.prev,n.length--;s+=k+y}}}}}return a.Token=s,a.util.currentScript=function(){if("undefined"==typeof document)return null;if("currentScript"in document)return document.currentScript;try{throw new Error}catch(r){var e=(/at [^(\\r\\n]*\\((.*):(?:\\d+):(?:\\d+)\\)$/i.exec(r.stack)||[])[1];if(e){var n=document.getElementsByTagName("script");for(var t in n)if(n[t].src==e)return n[t]}return null}},a.util.getLanguage=function(e){for(;e;){var t=n.exec(e.className);if(t)return t[1].toLowerCase();e=e.parentElement}return"none"},a.util.setLanguage=function(e,t){e.className=e.className.replace(RegExp(n,"gi"),""),e.classList.add("language-"+t)},e.Prism=a,a}();"undefined"!=typeof module&&module.exports&&(module.exports=Prism),"undefined"!=typeof global&&(global.Prism=Prism);

/* Python Grammar */
Prism.languages.python={
  'comment':{pattern:/(^|[^\\])#.*/,lookbehind:!0,greedy:!0},
  'string-interpolation':{pattern:/(?:f|fr|rf)(?:(\"\"\"|\'\'\')[\\s\\S]*?\\1|([\"'])(?:\\\\.|(?!\\2)[^\\\\\\r\\n])*\\2)/i,greedy:!0,inside:{'interpolation':{pattern:/((?:^|[^{])(?:\\{\\{)*)\\{(?!\\{)(?:[^{}]|\\{[^{}]*\\})*\\}/,lookbehind:!0,inside:{'rest':null}},'string':/[\\s\\S]+/}},
  'triple-quoted-string':{pattern:/(?:[rub]|rb|br)?(\"\"\"|\'\'\')[\\s\\S]*?\\1/i,greedy:!0,alias:'string'},
  'string':{pattern:/(?:[rub]|rb|br)?(["'])(?:\\\\.|(?!\\1)[^\\\\\\r\\n])*\\1/i,greedy:!0},
  'function':{pattern:/((?:def|class)\\s+)[a-zA-Z_]\\w*(?=\\s*\\()/,lookbehind:!0},
  'class-name':{pattern:/(\\bclass\\s+)\\w+/i,lookbehind:!0},
  'decorator':{pattern:/(^[\\t ]*)@\\w+(?:\\.\\w+)*/m,lookbehind:!0,alias:'annotation',inside:{'punctuation':/\\./}},
  'keyword':/\\b(?:and|as|assert|async|await|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|print|raise|return|try|while|with|yield)\\b/,
  'builtin':/\\b(?:__import__|abs|all|any|apply|ascii|basestring|bin|bool|buffer|bytearray|bytes|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|file|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|memoryview|min|next|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\\b/,
  'boolean':/\\b(?:False|None|True)\\b/,
  'number':/\\b0(?:b(?:_?[01])+|o(?:_?[0-7])+|x(?:_?[a-f0-9])+)\\b|(?:\\b\\d+(?:_\\d+)*(?:\\.(?:\\d+(?:_\\d+)*)?)?|\\B\\.\\d+(?:_\\d+)*)(?:e[+-]?\\d+(?:_\\d+)*)?j?(?!\\w)/i,
  'operator':/[-+%=]=?|!=|\\*{1,2}=?|\\/{1,2}=?|<[<=>]?|>[=>]?|&[&=]?|\\|[|=]?|\\^[=]?|~|\\b(?:and|as|in|is|not|or)\\b/,
  'punctuation':/[{}[\\];(),.:]/
};
Prism.languages.python['string-interpolation'].inside['interpolation'].inside['rest']=Prism.languages.python;
Prism.languages.py=Prism.languages.python;

/* Bash / Shell Grammar */
Prism.languages.bash={
  'comment':{pattern:/(^|[\\s#])#.*/,lookbehind:!0,greedy:!0},
  'string':{pattern:/(["'])(?:\\\\.|(?!\\1)[^\\\\\\r\\n])*\\1/,greedy:!0},
  'variable':/\\$[a-zA-Z_]\\w*|\\$\\{[^}]+\\}/,
  'function':{pattern:/(^|\\s)[a-zA-Z_]\\w*(?=\\s*\\(\\))/,lookbehind:!0},
  'keyword':/\\b(?:if|then|else|elif|fi|for|while|in|do|done|case|esac|function)\\b/,
  'boolean':/\\b(?:true|false)\\b/,
  'number':/\\b\\d+(?:\\.\\d+)?\\b/,
  'operator':/&&|\\|\\||>>|>|<|==|!=|=~|[-+*/=]/,
  'punctuation':/[{}[\\];(),.:]/
};
Prism.languages.shell=Prism.languages.bash;
Prism.languages.sh=Prism.languages.bash;

/* JSON Grammar */
Prism.languages.json={
  'property':{pattern:/(^|[^\\\\])"(?:\\\\.|[^\\\\"\\r\\n])*"(?=\\s*:)/,lookbehind:!0,greedy:!0},
  'string':{pattern:/(^|[^\\\\])"(?:\\\\.|[^\\\\"\\r\\n])*"(?!\\s*:)/,lookbehind:!0,greedy:!0},
  'comment':{pattern:/\\/\\/.*|\\/\\*[\\s\\S]*?\\*\\//,greedy:!0},
  'number':/-?\\b\\d+(?:\\.\\d+)?(?:e[+-]?\\d+)?\\b/i,
  'punctuation':/[{}[\\];,:]/,
  'operator':/:/,
  'boolean':/\\b(?:false|true)\\b/,
  'null':{pattern:/\\bnull\\b/,alias:'keyword'}
};

// Line numbers plugin
Prism.hooks.add('complete', function(env) {
  if (!env.code) return;
  var pre = env.element.parentNode;
  var cls = ' ' + pre.className + ' ';
  if (cls.indexOf(' line-numbers ') === -1) return;
  
  var match = env.code.match(/\\n(?!$)/g);
  var linesNum = match ? match.length + 1 : 1;
  var lineNumbersWrapper = document.createElement('span');
  lineNumbersWrapper.setAttribute('aria-hidden', 'true');
  lineNumbersWrapper.className = 'line-numbers-rows';
  
  var lines = new Array(linesNum + 1).join('<span></span>');
  lineNumbersWrapper.innerHTML = lines;
  
  if (pre.hasAttribute('data-start')) {
    pre.style.counterReset = 'linenumber ' + (parseInt(pre.getAttribute('data-start'), 10) - 1);
  }
  env.element.appendChild(lineNumbersWrapper);
});
"""

    # Custom Dark Cyber-Radar Prism Theme matching website tokens
    prism_css_content = """/* Dark Cyber-Radar Prism.js Syntax Theme */
code[class*="language-"],
pre[class*="language-"] {
  color: #f8fafc;
  background: #0b1120;
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  font-size: 0.86rem;
  line-height: 1.6;
  direction: ltr;
  text-align: left;
  white-space: pre;
  word-spacing: normal;
  word-break: normal;
  -moz-tab-size: 4;
  -o-tab-size: 4;
  tab-size: 4;
  -webkit-hyphens: none;
  -moz-hyphens: none;
  -ms-hyphens: none;
  hyphens: none;
}

pre[class*="language-"] {
  padding: 1.25rem 1.5rem;
  margin: 0;
  overflow: auto;
  border-radius: 0 0 8px 8px;
}

:not(pre) > code[class*="language-"] {
  padding: 0.15rem 0.35rem;
  border-radius: 4px;
  background: #172033;
  color: #00f0ff;
}

/* Token Colors */
.token.comment,
.token.prolog,
.token.doctype,
.token.cdata {
  color: #64748b;
  font-style: italic;
}

.token.punctuation {
  color: #94a3b8;
}

.token.property,
.token.tag,
.token.boolean,
.token.number,
.token.constant,
.token.symbol,
.token.deleted {
  color: #38bdf8;
}

.token.selector,
.token.attr-name,
.token.string,
.token.char,
.token.builtin,
.token.inserted {
  color: #10b981;
}

.token.operator,
.token.entity,
.token.url,
.language-css .token.string,
.style .token.string {
  color: #f59e0b;
}

.token.atrule,
.token.attr-value,
.token.keyword {
  color: #00f0ff;
  font-weight: 600;
}

.token.function,
.token.class-name {
  color: #818cf8;
}

.token.regex,
.token.important,
.token.variable {
  color: #f43f5e;
}

.token.important,
.token.bold {
  font-weight: bold;
}

.token.italic {
  font-style: italic;
}

/* Line Numbers Styling */
pre[class*="language-"].line-numbers {
  position: relative;
  padding-left: 3.8em;
  counter-reset: linenumber;
}

pre[class*="language-"].line-numbers > code {
  position: relative;
  white-space: inherit;
}

.line-numbers .line-numbers-rows {
  position: absolute;
  pointer-events: none;
  top: 0;
  font-size: 100%;
  left: -3.8em;
  width: 3em;
  letter-spacing: -1px;
  border-right: 1px solid #1e293b;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.line-numbers-rows > span {
  display: block;
  counter-increment: linenumber;
}

.line-numbers-rows > span:before {
  content: counter(linenumber);
  color: #475569;
  display: block;
  padding-right: 0.8em;
  text-align: right;
}
"""

    with open(prism_js_path, "w", encoding="utf-8") as f:
        f.write(prism_js_content)

    with open(prism_css_path, "w", encoding="utf-8") as f:
        f.write(prism_css_content)

    print(f"  [OK] Vendored prism.min.js ({len(prism_js_content) / 1024:.1f} KB)")
    print(f"  [OK] Vendored prism.min.css ({len(prism_css_content) / 1024:.1f} KB)")
    return prism_js_path, prism_css_path


def export_all() -> Dict[str, List[Path]]:
    """
    Main orchestration routine for exporting all assets into docs/assets/.
    """
    print("=" * 70)
    print("🚀 [ASSET PIPELINE] Starting Showcase Asset Export & Synchronization...")
    print("=" * 70)

    results: Dict[str, List[Path]] = {}

    # 1. Notebook 01: Classical Radar DSP
    nb1_path = REPO_ROOT / "01_radar_classical_dsp.ipynb"
    nb1_out = ASSETS_DIR / "nb1"
    nb1_mapping = {
        3: "fig1_fmcw_chirp_physics.png",
        6: "fig2_raw_3d_cube_signal.png",
        9: "fig3_range_fft_windowing.png",
        12: "fig4_mti_clutter_suppression.png",
        15: "fig5_doppler_fft_rdm.png",
        18: "fig6_cfar_adaptive_detection.png",
        21: "fig7_aoa_music_super_res.png",
        24: "fig8_dbscan_clustering_bev.png",
        27: "fig9_pedestrian_micro_doppler.png",
    }
    print("\n[Stage 1/5] Extracting Notebook 01 figures...")
    results["nb1"] = extract_notebook_images(nb1_path, nb1_out, nb1_mapping)

    # 2. Notebook 02: Deep Learning Perception
    nb2_path = REPO_ROOT / "02_radar_deep_learning_detection.ipynb"
    nb2_out = ASSETS_DIR / "nb2"
    nb2_mapping = {
        4: "plot1_synthetic_dataset_sample.png",
        10: "plot2_training_convergence.png",
        13: "plot3_model_inference_unseen.png",
    }
    print("\n[Stage 2/5] Extracting Notebook 02 figures...")
    results["nb2"] = extract_notebook_images(nb2_path, nb2_out, nb2_mapping)

    # 3. Notebook 03: Real-World RadDet S-128 Benchmark
    nb3_src = REPO_ROOT / "data" / "benchmark_results" / "s128_full"
    nb3_out = ASSETS_DIR / "nb3"
    print("\n[Stage 3/5] Synchronizing Notebook 03 benchmark artifacts...")
    results["nb3"] = sync_benchmark_assets(nb3_src, nb3_out)

    # 4. Diagrams & 3-Stage Evolution Timeline
    diagrams_out = ASSETS_DIR / "diagrams"
    print("\n[Stage 4/5] Synchronizing architecture diagrams & rendering timeline...")
    results["diagrams"] = sync_architecture_diagrams(diagrams_out)
    timeline_path = diagrams_out / "timeline_evolution.svg"
    generate_timeline_svg(timeline_path)
    results["diagrams"].append(timeline_path)

    # 5. Offline Vendor Libraries (Prism.js)
    vendor_out = ASSETS_DIR / "vendor"
    print("\n[Stage 5/5] Vendoring offline Prism.js assets...")
    p_js, p_css = vendor_prism_assets(vendor_out)
    results["vendor"] = [p_js, p_css]

    # Summary verification
    total_files = sum(len(v) for v in results.values())
    print("\n" + "=" * 70)
    print(f"✨ [ASSET PIPELINE COMPLETE] Successfully exported {total_files} assets to docs/assets/")
    print("=" * 70)
    return results


if __name__ == "__main__":
    export_all()
