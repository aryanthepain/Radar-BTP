"""
Export Jupyter Walkthrough Notebooks to Publication-Grade PDFs.

Uses nbconvert to export notebooks to HTML with embedded assets and MathJax,
enriches the HTML with academic print CSS (vector SVGs expanded, syntax wrapping,
exact background colors for dark radar heatmaps, orphan heading prevention),
and renders high-fidelity PDFs via headless Edge/Chrome.
"""

import os
import sys
import shutil
import tempfile
import pathlib
import subprocess
from typing import List, Optional

import nbformat
from nbconvert import HTMLExporter
import PyPDF2


PRINT_ENHANCEMENT_CSS = """
<style>
@media print {
    @page {
        size: A4 portrait;
        margin: 15mm 12mm 15mm 12mm;
    }
    body {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    /* Expand all collapsible architecture SVG diagrams */
    details, details[open] {
        display: block !important;
    }
    details summary, summary {
        display: none !important;
    }
    /* Hide duplicate raw mermaid text code blocks */
    .jp-Mermaid {
        display: none !important;
    }
    /* Prevent orphan headings */
    h1, h2, h3, h4, h5, h6 {
        break-after: avoid !important;
        page-break-after: avoid !important;
    }
    /* Keep code input and output blocks cohesive */
    .jp-Cell-inputWrapper, .jp-OutputArea-child {
        break-inside: avoid !important;
        page-break-inside: avoid !important;
    }
    /* Prevent image truncation across page breaks */
    img, svg, figure {
        max-width: 100% !important;
        height: auto !important;
        break-inside: avoid !important;
        page-break-inside: avoid !important;
    }
    /* Ensure code wraps cleanly */
    pre, code {
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }
}

/* Fallback styling for non-print render engine pass */
details, details[open] {
    display: block !important;
}
details > summary, summary {
    display: none !important;
}
.jp-Mermaid {
    display: none !important;
}
img, svg {
    max-width: 100% !important;
    height: auto !important;
}
</style>
"""


def find_browser_executable() -> str:
    """Find Microsoft Edge or Google Chrome executable on the system."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    
    # Try which / where
    for name in ["msedge", "chrome", "google-chrome", "chromium"]:
        found = shutil.which(name)
        if found:
            return found
            
    raise RuntimeError(
        "Could not find Microsoft Edge, Google Chrome, or Chromium executable on the system."
    )


def export_notebook_to_pdf(
    notebook_path: str,
    output_pdf_path: str,
    browser_exe: Optional[str] = None
) -> str:
    """Convert an executed Jupyter notebook (.ipynb) to a publication-grade PDF."""
    if not os.path.exists(notebook_path):
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    browser = browser_exe or find_browser_executable()
    print(f"[PDF Export] Loading notebook: {notebook_path}")

    with open(notebook_path, "r", encoding="utf-8") as f:
        nb_node = nbformat.read(f, as_version=4)

    exporter = HTMLExporter()
    exporter.template_name = "lab"
    (html_body, _) = exporter.from_notebook_node(nb_node)

    # Transform collapsible details into expanded blocks
    modified_html = html_body.replace("<details>", "<details open>")

    # Inject print enhancements right before closing head tag
    if "</head>" in modified_html:
        modified_html = modified_html.replace("</head>", f"{PRINT_ENHANCEMENT_CSS}\n</head>")
    else:
        modified_html = f"{PRINT_ENHANCEMENT_CSS}\n{modified_html}"

    temp_html_path = os.path.abspath(f"{notebook_path}.tmp_export.html")
    try:
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(modified_html)

        abs_pdf_path = os.path.abspath(output_pdf_path)
        uri = pathlib.Path(temp_html_path).resolve().as_uri()

        print(f"[PDF Export] Rendering via headless browser: {os.path.basename(browser)}")
        cmd = [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=6000",
            f"--print-to-pdf={abs_pdf_path}",
            uri,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[Warning] Browser process returned code {result.returncode}")
            if result.stderr:
                print(f"[Stderr] {result.stderr.strip()}")

        if not os.path.exists(abs_pdf_path):
            raise RuntimeError(f"PDF failed to generate at {abs_pdf_path}")

        file_size_mb = os.path.getsize(abs_pdf_path) / (1024 * 1024)
        reader = PyPDF2.PdfReader(abs_pdf_path)
        page_count = len(reader.pages)
        print(f"[PDF Export] Successfully generated {output_pdf_path} ({page_count} pages, {file_size_mb:.2f} MB)")
        return abs_pdf_path

    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    notebooks = [
        ("01_radar_classical_dsp.ipynb", "01_radar_classical_dsp.pdf"),
        ("02_radar_deep_learning_detection.ipynb", "02_radar_deep_learning_detection.pdf"),
    ]

    browser = find_browser_executable()
    print(f"Using browser executable: {browser}")

    for nb_name, pdf_name in notebooks:
        nb_path = os.path.join(root_dir, nb_name)
        pdf_path = os.path.join(root_dir, pdf_name)
        export_notebook_to_pdf(nb_path, pdf_path, browser_exe=browser)

    print("\n[Complete] All walkthrough notebooks exported to publication-grade PDFs.")


if __name__ == "__main__":
    main()
