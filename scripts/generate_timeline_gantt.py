#!/usr/bin/env python3
"""
scripts/generate_timeline_gantt.py — 1-Year Academic Gantt Schedule Generator
Generates:
  1. docs/assets/diagrams/timeline_gantt.svg (Publication-grade SVG for web showcase)
  2. templates/BTP_Report_Template_Overleaf/figures/timeline_gantt.pdf (Native vector PDF via pdflatex)
  3. docs/assets/diagrams/timeline_gantt.png (High-resolution raster preview via pdftoppm)

Adheres strictly to report_content/gantt_chart.md:
  - 10 Months: Aug 2026 to May 2027
  - 9 Activities grouped into BTP-1 Completed (4) and BTP-2 Proposed (5)
  - December 2026 is shown as an unassigned month (recess / zero scheduled milestone)
  - Prominent milestone marker for 23 November 2026 (BTP-1 Final Defense)
  - April 2027 SDR exploration marked [Conditional]
  - No synthetic start/end dates or intra-month duration inventions
"""

import os
import sys
import html
import xml.etree.ElementTree as ET
import subprocess
import tempfile
import shutil

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_ASSETS_DIR = os.path.join(REPO_ROOT, "docs", "assets", "diagrams")
OVERLEAF_FIG_DIR = os.path.join(REPO_ROOT, "templates", "BTP_Report_Template_Overleaf", "figures")


def xml_escape(text):
    """Escape text for valid XML embedding."""
    return html.escape(str(text), quote=True)

MONTHS = [
    {"label": "Aug 2026", "short": "Aug '26", "phase": "BTP-1", "is_break": False},
    {"label": "Sep 2026", "short": "Sep '26", "phase": "BTP-1", "is_break": False},
    {"label": "Oct 2026", "short": "Oct '26", "phase": "BTP-1", "is_break": False},
    {"label": "Nov 2026", "short": "Nov '26", "phase": "BTP-1", "is_break": False},
    {"label": "Dec 2026", "short": "Dec '26", "phase": "Break", "is_break": True},
    {"label": "Jan 2027", "short": "Jan '27", "phase": "BTP-2", "is_break": False},
    {"label": "Feb 2027", "short": "Feb '27", "phase": "BTP-2", "is_break": False},
    {"label": "Mar 2027", "short": "Mar '27", "phase": "BTP-2", "is_break": False},
    {"label": "Apr 2027", "short": "Apr '27", "phase": "BTP-2", "is_break": False},
    {"label": "May 2027", "short": "May '27", "phase": "BTP-2", "is_break": False},
]

ACTIVITIES = [
    {
        "id": "A1",
        "phase_group": "BTP-1",
        "phase_title": "BTP-1 — Completed",
        "month_idx": 0,
        "month_name": "August 2026",
        "title": "Academic Inception & FMCW Chirp Synthesis",
        "desc": "Academic inception, radar literature study, MATLAB Radar Designer prototyping, FMCW chirp synthesis and link-budget analysis",
        "is_conditional": False,
        "milestone": None,
    },
    {
        "id": "A2",
        "phase_group": "BTP-1",
        "phase_title": "BTP-1 — Completed",
        "month_idx": 1,
        "month_name": "September 2026",
        "title": "77 GHz Simulation & Classical Radar DSP Chain",
        "desc": "77 GHz FMCW simulation and classical DSP pipeline: Range FFT, MTI, Doppler FFT, CFAR, MUSIC and DBSCAN",
        "is_conditional": False,
        "milestone": None,
    },
    {
        "id": "A3",
        "phase_group": "BTP-1",
        "phase_title": "BTP-1 — Completed",
        "month_idx": 2,
        "month_name": "October 2026",
        "title": "PyTorch Radar CNN & Multi-Task Convergence",
        "desc": "PyTorch radar CNN, synthetic dataset generation and multi-task loss convergence experiments",
        "is_conditional": False,
        "milestone": None,
    },
    {
        "id": "A4",
        "phase_group": "BTP-1",
        "phase_title": "BTP-1 — Completed",
        "month_idx": 3,
        "month_name": "November 2026",
        "title": "RadDet Benchmark Evaluation & BTP-1 Oral Defense",
        "desc": "RadDet benchmark ingestion and full-scale GPU evaluation across approximately 40,000 frames and six SNR tiers; BTP-1 final presentation and oral defense on 23 November 2026",
        "is_conditional": False,
        "milestone": "23 Nov 2026: BTP-1 Presentation & Oral Defense",
    },
    {
        "id": "A5",
        "phase_group": "BTP-2",
        "phase_title": "BTP-2 — Proposed",
        "month_idx": 5,
        "month_name": "January 2027",
        "title": "Non-Gaussian Clutter Simulation & Multi-Resolution Triage",
        "desc": "Automated MATLAB synthetic data-cube generation under non-Gaussian clutter; prototype cascaded multi-resolution triage (128² → 256² → 512²) with entropy-gated routing",
        "is_conditional": False,
        "milestone": None,
    },
    {
        "id": "A6",
        "phase_group": "BTP-2",
        "phase_title": "BTP-2 — Proposed",
        "month_idx": 6,
        "month_name": "February 2027",
        "title": "Cross-Resolution Distillation & Layer Early-Exits",
        "desc": "Cross-resolution knowledge distillation from a 512² teacher to a compact 128² student and dynamic layer early-exit mechanisms",
        "is_conditional": False,
        "milestone": None,
    },
    {
        "id": "A7",
        "phase_group": "BTP-2",
        "phase_title": "BTP-2 — Proposed",
        "month_idx": 7,
        "month_name": "March 2027",
        "title": "CPU-First INT8 Quantisation & Pareto Profiling",
        "desc": "CPU-first INT8 quantisation, OpenVINO / ONNX Runtime CPU profiling, and accuracy–latency–memory Pareto analysis",
        "is_conditional": False,
        "milestone": None,
    },
    {
        "id": "A8",
        "phase_group": "BTP-2",
        "phase_title": "BTP-2 — Proposed",
        "month_idx": 8,
        "month_name": "April 2027",
        "title": "Paper Submission & SDR Hardware Exploration",
        "desc": "IEEE conference/journal paper submission and conditional laboratory software-defined radar (SDR) hardware exploration",
        "is_conditional": True,
        "milestone": None,
    },
    {
        "id": "A9",
        "phase_group": "BTP-2",
        "phase_title": "BTP-2 — Proposed",
        "month_idx": 9,
        "month_name": "May 2027",
        "title": "B.Tech Thesis Manuscript & Oral Viva Voce",
        "desc": "Comprehensive B.Tech thesis manuscript submission and oral viva voce defense",
        "is_conditional": False,
        "milestone": "May 2027: Final B.Tech Thesis Submission & Viva Voce",
    },
]


def wrap_text(text, max_chars=55):
    """Wrap text to fit comfortably inside table cells."""
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    for w in words:
        if current_len + len(w) + 1 <= max_chars:
            current_line.append(w)
            current_len += len(w) + 1
        else:
            lines.append(" ".join(current_line))
            current_line = [w]
            current_len = len(w)
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def generate_svg():
    """Generate high-fidelity, publication-grade dark-themed academic SVG Gantt chart."""
    # Geometry constants
    width = 1420
    height = 910
    
    # Left activity pane
    left_x = 24
    table_w = 510
    
    # Right timeline pane
    time_x = left_x + table_w + 16  # 550
    time_w = width - time_x - 24    # 1420 - 550 - 24 = 846
    col_w = time_w / 10.0           # 84.6 px per month
    
    # Header & row vertical coordinates
    hdr_y = 120
    hdr_h = 42
    
    # Row specifications
    # 4 rows BTP-1, 1 divider band for Dec break, 5 rows BTP-2
    row_h = 56
    row_gap = 6
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif; background: #090d16; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">')
    
    # Definitions: Gradients, Patterns, Filters
    svg_lines.append('''  <defs>
    <!-- Background subtle gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <!-- BTP-1 Completed Bar Gradient -->
    <linearGradient id="btp1BarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>

    <!-- BTP-2 Proposed Bar Gradient -->
    <linearGradient id="btp2BarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#4f46e5"/>
    </linearGradient>

    <!-- Conditional Bar Gradient -->
    <linearGradient id="condBarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#d97706"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>

    <!-- Dec Break Hatch Pattern -->
    <pattern id="hatchBreak" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#334155" stroke-width="2" stroke-opacity="0.35"/>
    </pattern>

    <!-- Drop Shadow Filter -->
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000000" flood-opacity="0.4"/>
    </filter>
    <filter id="pinGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>''')
    
    # Outer Background
    svg_lines.append(f'  <rect width="{width}" height="{height}" fill="url(#bgGrad)" rx="8" stroke="#1e293b" stroke-width="1.5"/>')
    
    # Title & Subtitle
    svg_lines.append(f'  <text x="32" y="44" font-size="21" font-weight="700" fill="#f8fafc" letter-spacing="-0.01em">BTP Academic Timeline &amp; One-Year Gantt Schedule</text>')
    svg_lines.append(f'  <text x="32" y="68" font-size="12.5" fill="#94a3b8">BTP-1 Completed Engineering Milestones (Aug–Nov 2026) vs. BTP-2 Proposed Research Thrusts (Jan–May 2027)</text>')
    
    # Legend Container
    leg_x = width - 660
    leg_y = 28
    svg_lines.append(f'  <g transform="translate({leg_x}, {leg_y})">')
    svg_lines.append('    <rect width="630" height="48" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1"/>')
    # Legend items
    # Item 1: BTP-1 Completed
    svg_lines.append('    <rect x="14" y="16" width="16" height="16" rx="3" fill="url(#btp1BarGrad)" stroke="#38bdf8" stroke-width="1"/>')
    svg_lines.append('    <text x="36" y="29" font-size="11.5" font-weight="600" fill="#cbd5e1">BTP-1 Completed</text>')
    # Item 2: BTP-2 Proposed
    svg_lines.append('    <rect x="150" y="16" width="16" height="16" rx="3" fill="url(#btp2BarGrad)" stroke="#a5b4fc" stroke-width="1" stroke-dasharray="2,2"/>')
    svg_lines.append('    <text x="172" y="29" font-size="11.5" font-weight="600" fill="#cbd5e1">BTP-2 Proposed</text>')
    # Item 3: Conditional
    svg_lines.append('    <rect x="282" y="16" width="16" height="16" rx="3" fill="url(#condBarGrad)" stroke="#fbbf24" stroke-width="1"/>')
    svg_lines.append('    <text x="304" y="29" font-size="11.5" font-weight="600" fill="#fbbf24">[Conditional] SDR</text>')
    # Item 4: Milestone Pin
    svg_lines.append('    <polygon points="426,16 433,24 426,32 419,24" fill="#f59e0b" stroke="#ffffff" stroke-width="1.2"/>')
    svg_lines.append('    <text x="440" y="29" font-size="11.5" font-weight="600" fill="#f59e0b">Milestone Marker</text>')
    # Item 5: Unassigned Break
    svg_lines.append('    <rect x="548" y="16" width="16" height="16" rx="3" fill="url(#hatchBreak)" stroke="#64748b" stroke-width="1"/>')
    svg_lines.append('    <text x="570" y="29" font-size="11.5" font-weight="600" fill="#94a3b8">Recess</text>')
    svg_lines.append('  </g>')

    # Phase Span Group Banners above month columns
    # BTP-1 columns 0..3: span x = time_x to time_x + 4*col_w
    btp1_w = 4 * col_w
    svg_lines.append(f'  <rect x="{time_x}" y="94" width="{btp1_w}" height="22" rx="4" fill="rgba(2, 132, 199, 0.18)" stroke="#0284c7" stroke-width="1"/>')
    svg_lines.append(f'  <text x="{time_x + btp1_w/2}" y="109" font-size="11" font-weight="700" fill="#38bdf8" text-anchor="middle" letter-spacing="0.04em">PHASE I: BTP-1 COMPLETED FOUNDATION</text>')

    # Dec break column 4: span x = time_x + 4*col_w to time_x + 5*col_w
    dec_x = time_x + 4 * col_w
    svg_lines.append(f'  <rect x="{dec_x}" y="94" width="{col_w}" height="22" rx="4" fill="rgba(100, 116, 139, 0.15)" stroke="#475569" stroke-width="1"/>')
    svg_lines.append(f'  <text x="{dec_x + col_w/2}" y="109" font-size="10.5" font-weight="600" fill="#94a3b8" text-anchor="middle">RECESS</text>')

    # BTP-2 columns 5..9: span x = time_x + 5*col_w to time_x + 10*col_w
    btp2_x = time_x + 5 * col_w
    btp2_w = 5 * col_w
    svg_lines.append(f'  <rect x="{btp2_x}" y="94" width="{btp2_w}" height="22" rx="4" fill="rgba(99, 102, 241, 0.18)" stroke="#6366f1" stroke-width="1"/>')
    svg_lines.append(f'  <text x="{btp2_x + btp2_w/2}" y="109" font-size="11" font-weight="700" fill="#a5b4fc" text-anchor="middle" letter-spacing="0.04em">PHASE II: BTP-2 PROPOSED RESEARCH ROADMAP</text>')

    # Left Table Header
    svg_lines.append(f'  <rect x="{left_x}" y="{hdr_y}" width="{table_w}" height="{hdr_h}" rx="5" fill="#0f172a" stroke="#334155" stroke-width="1"/>')
    svg_lines.append(f'  <text x="{left_x + 16}" y="{hdr_y + 26}" font-size="12" font-weight="700" fill="#f1f5f9" letter-spacing="0.03em">SCHEDULED RESEARCH &amp; IMPLEMENTATION ACTIVITIES</text>')
    svg_lines.append(f'  <text x="{left_x + table_w - 16}" y="{hdr_y + 26}" font-size="11" font-weight="600" fill="#94a3b8" text-anchor="end">MONTH &amp; PHASE</text>')

    # Right Month Header Grid
    for i, m in enumerate(MONTHS):
        cx = time_x + i * col_w
        is_break = m["is_break"]
        bg = "#1e293b" if not is_break else "#172033"
        border = "#475569" if not is_break else "#334155"
        txt_color = "#f8fafc" if not is_break else "#94a3b8"
        
        svg_lines.append(f'  <rect x="{cx}" y="{hdr_y}" width="{col_w}" height="{hdr_h}" fill="{bg}" stroke="{border}" stroke-width="1"/>')
        svg_lines.append(f'  <text x="{cx + col_w/2}" y="{hdr_y + 20}" font-size="11.5" font-weight="700" fill="{txt_color}" text-anchor="middle">{xml_escape(m["short"])}</text>')
        sub_text = m["phase"] if not is_break else "Unassigned"
        sub_col = "#38bdf8" if m["phase"] == "BTP-1" else ("#a5b4fc" if m["phase"] == "BTP-2" else "#64748b")
        svg_lines.append(f'  <text x="{cx + col_w/2}" y="{hdr_y + 34}" font-size="9.5" font-weight="600" fill="{sub_col}" text-anchor="middle">{xml_escape(sub_text)}</text>')

    # Vertical Grid Columns Background in timeline area (across all rows)
    grid_top_y = hdr_y + hdr_h
    grid_bottom_y = height - 70
    grid_total_h = grid_bottom_y - grid_top_y

    for i, m in enumerate(MONTHS):
        cx = time_x + i * col_w
        if m["is_break"]:
            # Shaded background for December
            svg_lines.append(f'  <rect x="{cx}" y="{grid_top_y}" width="{col_w}" height="{grid_total_h}" fill="url(#hatchBreak)" stroke="#334155" stroke-width="1" stroke-dasharray="4,4"/>')
        else:
            svg_lines.append(f'  <line x1="{cx}" y1="{grid_top_y}" x2="{cx}" y2="{grid_bottom_y}" stroke="#1e293b" stroke-width="1" stroke-dasharray="3,3"/>')
    # Right border line
    svg_lines.append(f'  <line x1="{time_x + 10*col_w}" y1="{grid_top_y}" x2="{time_x + 10*col_w}" y2="{grid_bottom_y}" stroke="#334155" stroke-width="1"/>')

    # Row Heights and Layout
    curr_y = grid_top_y + 6
    
    for idx, act in enumerate(ACTIVITIES):
        # Insert December Inter-Phase demarcation before A5
        if act["id"] == "A5":
            dec_band_h = 32
            svg_lines.append(f'  <!-- Inter-Semester Recess Demarcation -->')
            svg_lines.append(f'  <rect x="{left_x}" y="{curr_y}" width="{table_w + time_w + 16}" height="{dec_band_h}" rx="4" fill="rgba(15, 23, 42, 0.9)" stroke="#475569" stroke-width="1" stroke-dasharray="6,3"/>')
            svg_lines.append(f'  <text x="{width/2}" y="{curr_y + 20}" font-size="11.5" font-weight="600" fill="#94a3b8" text-anchor="middle">❄ December 2026: Academic Recess &amp; Inter-Semester Break (Zero Scheduled Milestone)</text>')
            curr_y += dec_band_h + 8

        row_y = curr_y
        is_btp1 = (act["phase_group"] == "BTP-1")
        is_cond = act["is_conditional"]
        has_milestone = (act["milestone"] is not None)
        
        # Row height adjusts for text lines
        lines = wrap_text(act["desc"], max_chars=54)
        computed_row_h = max(58, 24 + len(lines) * 14)
        
        # Left card background
        bg_card = "rgba(2, 132, 199, 0.05)" if is_btp1 else "rgba(99, 102, 241, 0.05)"
        border_card = "rgba(56, 189, 248, 0.25)" if is_btp1 else "rgba(165, 180, 252, 0.25)"
        svg_lines.append(f'  <rect x="{left_x}" y="{row_y}" width="{table_w}" height="{computed_row_h}" rx="5" fill="{bg_card}" stroke="{border_card}" stroke-width="1"/>')
        
        # Left Badge (A1..A9)
        badge_fill = "#0284c7" if is_btp1 else ("#d97706" if is_cond else "#6366f1")
        svg_lines.append(f'  <rect x="{left_x + 10}" y="{row_y + 10}" width="28" height="20" rx="4" fill="{badge_fill}"/>')
        svg_lines.append(f'  <text x="{left_x + 24}" y="{row_y + 24}" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">{act["id"]}</text>')
        
        # Month & Phase Tag on the right of card
        tag_col = "#38bdf8" if is_btp1 else ("#fbbf24" if is_cond else "#a5b4fc")
        svg_lines.append(f'  <text x="{left_x + table_w - 12}" y="{row_y + 23}" font-size="10.5" font-weight="700" fill="{tag_col}" text-anchor="end">{xml_escape(act["month_name"])}</text>')
        
        # Title of activity
        svg_lines.append(f'  <text x="{left_x + 46}" y="{row_y + 24}" font-size="12" font-weight="700" fill="#f8fafc">{xml_escape(act["title"])}</text>')
        
        # Multiline description
        for l_idx, line in enumerate(lines):
            line_y = row_y + 40 + l_idx * 14
            svg_lines.append(f'  <text x="{left_x + 12}" y="{line_y}" font-size="10.5" fill="#cbd5e1" line-height="1.4">{xml_escape(line)}</text>')
            
        # Timeline Gantt Bar on the right
        m_idx = act["month_idx"]
        bar_x = time_x + m_idx * col_w + 4
        bar_w = col_w - 8
        bar_h = 32
        bar_y = row_y + (computed_row_h - bar_h) / 2.0
        
        bar_grad = "url(#btp1BarGrad)" if is_btp1 else ("url(#condBarGrad)" if is_cond else "url(#btp2BarGrad)")
        bar_stroke = "#38bdf8" if is_btp1 else ("#fbbf24" if is_cond else "#a5b4fc")
        bar_dash = 'stroke-dasharray="3,2"' if (not is_btp1 and not is_cond) else ''
        
        # Render Gantt Bar
        svg_lines.append(f'  <g filter="url(#cardShadow)">')
        svg_lines.append(f'    <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="5" fill="{bar_grad}" stroke="{bar_stroke}" stroke-width="1.2" {bar_dash}/>')
        
        # Text label inside bar
        label_text = act["id"]
        if is_cond:
            label_text = f'{act["id"]}: Cond.'
        svg_lines.append(f'    <text x="{bar_x + bar_w/2}" y="{bar_y + 20}" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">{xml_escape(label_text)}</text>')
        svg_lines.append(f'  </g>')
        
        # Special Milestone / Markers
        if act["id"] == "A4":
            # 23 November 2026 Milestone Marker
            pin_x = bar_x + bar_w - 12
            pin_y = bar_y - 8
            # Diamond pin
            svg_lines.append(f'  <g filter="url(#pinGlow)">')
            svg_lines.append(f'    <polygon points="{pin_x},{pin_y} {pin_x+8},{pin_y+10} {pin_x},{pin_y+20} {pin_x-8},{pin_y+10}" fill="#f59e0b" stroke="#ffffff" stroke-width="1.5"/>')
            svg_lines.append(f'  </g>')
            # Callout Badge
            svg_lines.append(f'  <rect x="{pin_x - 110}" y="{pin_y - 22}" width="128" height="20" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1.2"/>')
            svg_lines.append(f'  <text x="{pin_x - 46}" y="{pin_y - 8}" font-size="10" font-weight="700" fill="#fbbf24" text-anchor="middle">★ 23 Nov: Oral Defense</text>')
            svg_lines.append(f'  <line x1="{pin_x - 8}" y1="{pin_y - 2}" x2="{pin_x}" y2="{pin_y}" stroke="#f59e0b" stroke-width="1.2"/>')

        if act["id"] == "A8":
            # Conditional Tag Pill above bar
            svg_lines.append(f'  <rect x="{bar_x - 12}" y="{bar_y - 18}" width="100" height="17" rx="3" fill="#0f172a" stroke="#d97706" stroke-width="1"/>')
            svg_lines.append(f'  <text x="{bar_x + 38}" y="{bar_y - 6}" font-size="9.5" font-weight="700" fill="#fbbf24" text-anchor="middle">⚠ [Conditional SDR]</text>')

        if act["id"] == "A9":
            # May 2027 Final Viva Voce Milestone Marker
            pin_x = bar_x + bar_w - 12
            pin_y = bar_y - 8
            svg_lines.append(f'  <g filter="url(#pinGlow)">')
            svg_lines.append(f'    <polygon points="{pin_x},{pin_y} {pin_x+8},{pin_y+10} {pin_x},{pin_y+20} {pin_x-8},{pin_y+10}" fill="#10b981" stroke="#ffffff" stroke-width="1.5"/>')
            svg_lines.append(f'  </g>')
            svg_lines.append(f'  <rect x="{pin_x - 120}" y="{pin_y - 22}" width="138" height="20" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="1.2"/>')
            svg_lines.append(f'  <text x="{pin_x - 51}" y="{pin_y - 8}" font-size="10" font-weight="700" fill="#34d399" text-anchor="middle">★ May \'27: Final Viva Voce</text>')
            svg_lines.append(f'  <line x1="{pin_x - 8}" y1="{pin_y - 2}" x2="{pin_x}" y2="{pin_y}" stroke="#10b981" stroke-width="1.2"/>')

        curr_y += computed_row_h + row_gap

    # Footer note at bottom
    foot_y = height - 24
    svg_lines.append(f'  <line x1="{left_x}" y1="{foot_y - 18}" x2="{width - 24}" y2="{foot_y - 18}" stroke="#1e293b" stroke-width="1"/>')
    svg_lines.append(f'  <text x="{left_x}" y="{foot_y - 2}" font-size="11" fill="#64748b" font-style="italic">Note: Strict month-level academic schedule. Intra-month task start/end interpolation omitted. December 2026 is intentionally unassigned (semester break). BTP-1 final presentation and oral defense milestone passed on 23 November 2026.</text>')
    
    svg_lines.append('</svg>')
    
    svg_content = "\n".join(svg_lines)

    # Validate XML well-formedness strictly before saving
    try:
        ET.fromstring(svg_content)
    except ET.ParseError as e:
        raise ValueError(f"Generated SVG is not well-formed XML: {e}")

    os.makedirs(DOCS_ASSETS_DIR, exist_ok=True)
    svg_path = os.path.join(DOCS_ASSETS_DIR, "timeline_gantt.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[SVG] Generated & verified valid XML: {svg_path} ({os.path.getsize(svg_path)} bytes)")
    return svg_path


def generate_tikz_tex():
    """Author a clean standalone LaTeX TikZ document for timeline_gantt.pdf."""
    tex_content = r"""\documentclass[border=8pt,11pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{shapes.geometric,arrows.meta,positioning,patterns,calc}
\usepackage[T1]{fontenc}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{xcolor}

% Define publication palette
\definecolor{btp1blue}{RGB}{2, 132, 199}
\definecolor{btp1light}{RGB}{224, 242, 254}
\definecolor{btp2indigo}{RGB}{79, 70, 229}
\definecolor{btp2light}{RGB}{238, 242, 255}
\definecolor{condorange}{RGB}{217, 119, 6}
\definecolor{condlight}{RGB}{254, 243, 199}
\definecolor{milestonegold}{RGB}{217, 119, 6}
\definecolor{grayborder}{RGB}{203, 213, 225}
\definecolor{graybg}{RGB}{248, 250, 252}

\begin{document}
\begin{tikzpicture}[x=1.85cm,y=-1.05cm]

  % Title and Subtitle
  \node[anchor=west,font=\large\bfseries] at (0,-1.4) {One-Year Academic Gantt Schedule for BTP-1 and Proposed BTP-2 Activities};
  \node[anchor=west,font=\small\color{black!70}] at (0,-0.9) {Completed Foundation (August--November 2026) vs.\ Proposed Research Roadmap (January--May 2027)};

  % Legend
  \begin{scope}[shift={(6.2,-1.5)}]
    \draw[fill=white,draw=grayborder,rounded corners=2pt] (0,0) rectangle (7.8,0.85);
    \fill[btp1blue,rounded corners=1pt] (0.2,0.2) rectangle (0.6,0.65);
    \node[anchor=west,font=\scriptsize\bfseries] at (0.65,0.42) {BTP-1 Completed};
    \fill[btp2indigo,rounded corners=1pt] (2.2,0.2) rectangle (2.6,0.65);
    \node[anchor=west,font=\scriptsize\bfseries] at (2.65,0.42) {BTP-2 Proposed};
    \fill[condorange,rounded corners=1pt] (4.1,0.2) rectangle (4.5,0.65);
    \node[anchor=west,font=\scriptsize\bfseries] at (4.55,0.42) {[Cond.] SDR};
    \node[diamond,fill=milestonegold,inner sep=2pt,draw=white] at (6.0,0.42) {};
    \node[anchor=west,font=\scriptsize\bfseries] at (6.15,0.42) {Milestone};
  \end{scope}

  % Column headers
  % Left header
  \draw[fill=graybg,draw=grayborder,thick] (0,0) rectangle (4.6,0.85);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.15,0.42) {Scheduled Activity \& Scope Description};

  % Month Column Coordinates: 4.8 to 13.8 (10 columns, step 0.9)
  % Aug=0, Sep=1, Oct=2, Nov=3, Dec=4, Jan=5, Feb=6, Mar=7, Apr=8, May=9
  \foreach \m [count=\i from 0] in {Aug '26, Sep '26, Oct '26, Nov '26, Dec '26, Jan '27, Feb '27, Mar '27, Apr '27, May '27} {
    \pgfmathsetmacro{\cx}{4.8 + \i*0.9}
    \ifnum \i=4
      \draw[fill=gray!15,draw=grayborder,thick] (\cx,0) rectangle (\cx+0.9,0.85);
      \node[font=\footnotesize\bfseries,align=center] at (\cx+0.45,0.32) {\m};
      \node[font=\tiny\color{black!60}] at (\cx+0.45,0.65) {Break};
    \else
      \draw[fill=graybg,draw=grayborder,thick] (\cx,0) rectangle (\cx+0.9,0.85);
      \node[font=\footnotesize\bfseries,align=center] at (\cx+0.45,0.32) {\m};
      \ifnum \i<4
        \node[font=\tiny\bfseries\color{btp1blue}] at (\cx+0.45,0.65) {BTP-1};
      \else
        \node[font=\tiny\bfseries\color{btp2indigo}] at (\cx+0.45,0.65) {BTP-2};
      \fi
    \fi
  }

  % Vertical grid lines and December background
  \fill[pattern=north east lines,pattern color=gray!30] (4.8+4*0.9,0.85) rectangle (4.8+5*0.9,10.6);
  \foreach \i in {0,...,10} {
    \pgfmathsetmacro{\cx}{4.8 + \i*0.9}
    \draw[dashed,gray!40] (\cx,0.85) -- (\cx,10.6);
  }

  % Rows
  % A1: Aug 2026
  \draw[fill=btp1light!40,draw=grayborder] (0,1.0) rectangle (4.6,1.9);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.1,1.25) {A1: Academic Inception \& FMCW Synthesiser};
  \node[anchor=west,font=\tiny\color{black!75},text width=4.3cm] at (0.1,1.6) {Literature study, MATLAB Radar Designer prototyping, FMCW chirp synthesis and link-budget analysis};
  \filldraw[btp1blue,rounded corners=2pt,draw=btp1blue!80!black] (4.85,1.15) rectangle (4.8+0.85,1.75);
  \node[font=\footnotesize\bfseries\color{white}] at (4.8+0.425,1.45) {A1};

  % A2: Sep 2026
  \draw[fill=btp1light!40,draw=grayborder] (0,2.0) rectangle (4.6,2.9);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.1,2.25) {A2: 77 GHz FMCW Simulation \& Classical DSP};
  \node[anchor=west,font=\tiny\color{black!75},text width=4.3cm] at (0.1,2.6) {Range FFT, MTI clutter filtering, Doppler FFT, 2D CA-CFAR, MUSIC AoA, and DBSCAN};
  \filldraw[btp1blue,rounded corners=2pt,draw=btp1blue!80!black] (4.8+0.9+0.05,2.15) rectangle (4.8+1.8-0.05,2.75);
  \node[font=\footnotesize\bfseries\color{white}] at (4.8+1.35,2.45) {A2};

  % A3: Oct 2026
  \draw[fill=btp1light!40,draw=grayborder] (0,3.0) rectangle (4.6,3.9);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.1,3.25) {A3: PyTorch Radar CNN \& Loss Convergence};
  \node[anchor=west,font=\tiny\color{black!75},text width=4.3cm] at (0.1,3.6) {Multi-task radar CNN architecture, synthetic data generation, and loss convergence};
  \filldraw[btp1blue,rounded corners=2pt,draw=btp1blue!80!black] (4.8+2*0.9+0.05,3.15) rectangle (4.8+3*0.9-0.05,3.75);
  \node[font=\footnotesize\bfseries\color{white}] at (4.8+2.55,3.45) {A3};

  % A4: Nov 2026
  \draw[fill=btp1light!40,draw=grayborder] (0,4.0) rectangle (4.6,4.9);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.1,4.25) {A4: RadDet Ingestion \& BTP-1 Oral Defense};
  \node[anchor=west,font=\tiny\color{black!75},text width=4.3cm] at (0.1,4.6) {GPU benchmark on ~40k frames, Table III reproduction; BTP-1 defense on 23 Nov 2026};
  \filldraw[btp1blue,rounded corners=2pt,draw=btp1blue!80!black] (4.8+3*0.9+0.05,4.15) rectangle (4.8+4*0.9-0.05,4.75);
  \node[font=\footnotesize\bfseries\color{white}] at (4.8+3.45,4.45) {A4};
  % Milestone marker on A4
  \node[diamond,fill=milestonegold,draw=white,inner sep=2.5pt] at (4.8+3.8,4.45) {};
  \node[anchor=south east,font=\tiny\bfseries\color{milestonegold!90!black}] at (4.8+4.0,4.2) {$\star$ 23 Nov: Defense};

  % December Demarcation Band
  \draw[fill=gray!10,draw=grayborder,dashed] (0,5.0) rectangle (13.8,5.45);
  \node[font=\footnotesize\itshape\color{black!70}] at (6.9,5.22) {--- December 2026: Academic Recess \& Inter-Semester Break (Zero Scheduled Milestone) ---};

  % A5: Jan 2027
  \draw[fill=btp2light!40,draw=grayborder] (0,5.6) rectangle (4.6,6.5);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.1,5.85) {A5: Clutter Simulation \& Multi-Resolution Triage};
  \node[anchor=west,font=\tiny\color{black!75},text width=4.3cm] at (0.1,6.2) {Non-Gaussian clutter data cubes; cascaded resolution triage (128$^2 \rightarrow 256^2 \rightarrow 512^2$)};
  \filldraw[btp2indigo,rounded corners=2pt,draw=btp2indigo!80!black] (4.8+5*0.9+0.05,5.75) rectangle (4.8+6*0.9-0.05,6.35);
  \node[font=\footnotesize\bfseries\color{white}] at (4.8+5.55,6.05) {A5};

  % A6: Feb 2027
  \draw[fill=btp2light!40,draw=grayborder] (0,6.6) rectangle (4.6,7.5);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.1,6.85) {A6: Knowledge Distillation \& Early-Exits};
  \node[anchor=west,font=\tiny\color{black!75},text width=4.3cm] at (0.1,7.2) {Cross-resolution distillation (512$^2$ teacher to 128$^2$ student) and early-exit gating};
  \filldraw[btp2indigo,rounded corners=2pt,draw=btp2indigo!80!black] (4.8+6*0.9+0.05,6.75) rectangle (4.8+7*0.9-0.05,7.35);
  \node[font=\footnotesize\bfseries\color{white}] at (4.8+6.55,7.05) {A6};

  % A7: Mar 2027
  \draw[fill=btp2light!40,draw=grayborder] (0,7.6) rectangle (4.6,8.5);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.1,7.85) {A7: CPU INT8 Quantisation \& Profiling};
  \node[anchor=west,font=\tiny\color{black!75},text width=4.3cm] at (0.1,8.2) {CPU-first INT8 quantisation, OpenVINO / ONNX Runtime profiling, and Pareto analysis};
  \filldraw[btp2indigo,rounded corners=2pt,draw=btp2indigo!80!black] (4.8+7*0.9+0.05,7.75) rectangle (4.8+8*0.9-0.05,8.35);
  \node[font=\footnotesize\bfseries\color{white}] at (4.8+7.55,8.05) {A7};

  % A8: Apr 2027
  \draw[fill=condlight!40,draw=grayborder] (0,8.6) rectangle (4.6,9.5);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.1,8.85) {A8: Paper Submission \& SDR Hardware [Cond.]};
  \node[anchor=west,font=\tiny\color{black!75},text width=4.3cm] at (0.1,9.2) {IEEE conference/journal manuscript and conditional laboratory SDR exploration};
  \filldraw[condorange,rounded corners=2pt,draw=condorange!80!black] (4.8+8*0.9+0.05,8.75) rectangle (4.8+9*0.9-0.05,9.35);
  \node[font=\footnotesize\bfseries\color{white}] at (4.8+8.55,9.05) {A8};
  \node[anchor=south,font=\tiny\bfseries\color{condorange}] at (4.8+8.55,8.7) {[Conditional]};

  % A9: May 2027
  \draw[fill=btp2light!40,draw=grayborder] (0,9.6) rectangle (4.6,10.5);
  \node[anchor=west,font=\footnotesize\bfseries] at (0.1,9.85) {A9: B.Tech Thesis Submission \& Viva Voce};
  \node[anchor=west,font=\tiny\color{black!75},text width=4.3cm] at (0.1,10.2) {Comprehensive thesis manuscript submission and oral viva voce defense};
  \filldraw[btp2indigo,rounded corners=2pt,draw=btp2indigo!80!black] (4.8+9*0.9+0.05,9.75) rectangle (4.8+10*0.9-0.05,10.35);
  \node[font=\footnotesize\bfseries\color{white}] at (4.8+9.55,10.05) {A9};
  % Milestone marker on A9
  \node[diamond,fill=milestonegold,draw=white,inner sep=2.5pt] at (4.8+9.8,10.05) {};
  \node[anchor=south east,font=\tiny\bfseries\color{milestonegold!90!black}] at (4.8+10.0,9.8) {$\star$ May '27: Viva Voce};

  % Footer
  \node[anchor=west,font=\scriptsize\color{black!60},text width=13.5cm] at (0,10.9) {Note: Month-level resolution without synthetic intra-month duration interpolation. December 2026 is intentionally unassigned (semester recess). BTP-1 final presentation and oral defense passed on 23 November 2026.};

\end{tikzpicture}
\end{document}
"""
    return tex_content


def compile_pdf(tex_str):
    """Compile TikZ TeX string with pdflatex into templates/BTP_Report_Template_Overleaf/figures/timeline_gantt.pdf."""
    os.makedirs(OVERLEAF_FIG_DIR, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix="gantt_pdf_")
    try:
        tex_path = os.path.join(temp_dir, "timeline_gantt_standalone.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_str)

        # Run pdflatex inside temp_dir
        res = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "timeline_gantt_standalone.tex"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )

        built_pdf = os.path.join(temp_dir, "timeline_gantt_standalone.pdf")
        if os.path.exists(built_pdf) and os.path.getsize(built_pdf) > 0:
            target_pdf = os.path.join(OVERLEAF_FIG_DIR, "timeline_gantt.pdf")
            shutil.copy2(built_pdf, target_pdf)
            print(f"[PDF] Compiled successfully: {target_pdf} ({os.path.getsize(target_pdf)} bytes)")

            # Also generate PNG preview using pdftoppm if available
            try:
                preview_stem = os.path.join(DOCS_ASSETS_DIR, "timeline_gantt")
                subprocess.run(
                    ["pdftoppm", "-png", "-r", "180", "-singlefile", built_pdf, preview_stem],
                    capture_output=True
                )
                preview_png = f"{preview_stem}.png"
                if os.path.exists(preview_png):
                    print(f"[PNG] Generated preview {preview_png} ({os.path.getsize(preview_png)} bytes)")
            except Exception as e:
                print(f"[PNG Preview Note] pdftoppm skipped: {e}")

            return target_pdf
        else:
            print("[PDF Error] pdflatex compilation failed:")
            print(res.stdout[-1000:] if res.stdout else "")
            print(res.stderr[-500:] if res.stderr else "")
            return None
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    print("=" * 60)
    print("Generating Academic 1-Year Gantt Chart Artifacts")
    print("=" * 60)

    # 1. Generate SVG for Academic Portal
    svg_file = generate_svg()

    # 2. Generate TeX and compile PDF for Overleaf
    tex_code = generate_tikz_tex()
    pdf_file = compile_pdf(tex_code)

    print("\nGeneration Summary:")
    print(f"  - SVG: {svg_file}")
    print(f"  - PDF: {pdf_file}")
    print("All Gantt chart assets successfully authored.")


if __name__ == "__main__":
    main()
