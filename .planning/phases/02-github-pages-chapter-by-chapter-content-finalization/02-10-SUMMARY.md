# Plan 02-10 Summary: Modernize Timeline Gantt Schedule in Figure 5.1 with Canva Design

**Phase:** Phase 2: GitHub Pages Chapter-by-Chapter Content Finalization  
**Plan:** 02-10  
**Status:** Completed & Deterministically Verified  

---

### Accomplishments
1. **Canva High-Resolution Graphic Export & Asset Generation (Task 1, R7):**
   - Successfully called the Canva MCP tool `export-design` for design `DAHbQ0tvIMc` (`Academic Research Schedule | Radar BTP` / `https://canva.link/fwfwsa30miuwne6`).
   - Downloaded and verified the high-resolution PNG graphic (3780 × 1890 px, 438,027 bytes, valid `\x89PNG\r\n\x1a\n` magic header).
   - Saved the raw export to `docs/assets/diagrams/timeline_gantt.png`.
   - Generated a standards-compliant XML SVG wrapper `docs/assets/diagrams/timeline_gantt.svg` embedding the base64-encoded image with proper `viewBox="0 0 3780 1890"`, `xmlns`, and `xmlns:xlink` attributes.
   - Verified that `timeline_gantt.svg` parses without error using Python's `xml.etree.ElementTree` and exceeds 1,000 bytes in size (1,168,414 bytes).
2. **Synchronized Figure 5.1 Caption, Alt Text, and Section 5.5 Narrative (Task 2, R7):**
   - Updated Figure 5.1 `alt` attribute and caption in `docs/index.html` to: `Figure 5.1: Academic Research Schedule for BTP-1 and Proposed BTP-2 Activities (August 2026 – May 2027)`.
   - Updated the figure caption description to detail the complete A1–A9 milestone breakdown:
     - Completed BTP-1 milestones: A1 (Literature review & MATLAB/Karlsson thesis), A2 (77 GHz FMCW simulation & classical DSP suite), A3 (PyTorch multi-task radar CNN), and A4 (RadDet dataset ingestion, 40k-frame GPU benchmark, with oral presentation on 23 November 2026).
     - December 2026: Academic semester break.
     - Proposed BTP-2 milestones: A5 (CARRADA dataset & adaptive compute formulations), A6 (Teacher-student knowledge distillation & early-exit gating), A7 (CPU-oriented INT8 quantization & edge optimization), A8 (Conditional research paper submission & lab trials), and A9 (Final thesis submission & departmental viva voce defense in May 2027).
   - Updated Section 5.5 narrative text cross-referencing the nine discrete engineering milestones (A1 through A9) and the academic research schedule in Figure 5.1.
3. **Deterministic Verification & Invariant Audit (Task 3, R6, R7):**
   - Updated `tests/test_academic_website.py` to assert the modernized Figure 5.1 caption, A1 and A9 milestone mentions, and 23 November 2026 presentation date.
   - Ran complete deterministic website test suites (`tests/test_academic_website.py` and `tests/test_showcase_website.py`), passing 24/24 tests in 0.87s.
   - Verified that `templates/BTP_Report_Template_Overleaf/` remains completely unmodified (0 modified files, strictly obeying R6).
