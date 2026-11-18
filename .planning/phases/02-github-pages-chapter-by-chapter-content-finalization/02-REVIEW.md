---
phase: 02-github-pages-chapter-by-chapter-content-finalization
reviewed: 2026-11-18T21:38:00Z
depth: deep
files_reviewed: 5
files_reviewed_list:
  - docs/app.js
  - docs/index.html
  - scripts/verify.ps1
  - tests/test_academic_website.py
  - tests/test_showcase_website.py
findings:
  critical: 2
  warning: 5
  info: 1
  total: 8
  necessity: 1
status: issues_found
---

# Phase 02: Code Review Report

**Reviewed:** 2026-11-18T21:38:00Z  
**Depth:** deep  
**Files Reviewed:** 5  
**Status:** issues_found  

## Summary

An adversarial code review of PR #24 diff (`git diff main...HEAD`) was conducted across `docs/app.js`, `docs/index.html`, `scripts/verify.ps1`, `tests/test_academic_website.py`, and `tests/test_showcase_website.py`.

The review identified **2 BLOCKER** issues, **5 WARNINGS**, and **1 INFO** item:
1. **Critical Citation Inversion:** 17 out of 31 citations in `docs/app.js` (`CITATIONS_DB`) are desynchronized with the actual bibliography in `docs/index.html`, causing hover tooltips to show completely wrong paper titles, authors, and venues.
2. **Out-of-Scope LaTeX Modifications:** `templates/BTP_Report_Template_Overleaf/` was modified (`General_Report_Template.tex` and newly committed `timeline_gantt.pdf`), violating explicit SPEC boundaries and constraints.
3. **Flawed Scope Test:** `tests/test_academic_website.py` checks `git status --porcelain` on `templates/` rather than `git diff`, allowing committed template mutations to pass CI silently.
4. **DOM Traversal Bug:** `docs/app.js` `.closest("figure, div[style*='text-align: center'], div")` stops at inner divs, breaking caption retrieval in lightbox modals.
5. **Scroll-Spy Inactive on Bibliography:** `docs/app.js` observes a 0px-height `<div id="references"></div>`, causing scroll-spy to drop active state on bibliography reading.
6. **Weakened CDN Offline Test:** `tests/test_showcase_website.py` replaced protocol checks with a 5-CDN blacklist, creating blind spots for other CDNs.
7. **Ponytail Anti-Bloat Violation:** ~257 lines of duplicate metadata in `docs/app.js` violate SSoT principles.
8. **UTF-8 BOM:** Added to `scripts/verify.ps1`.

---

## Critical Issues

### CR-01: Citation Metadata Inversion & Desynchronization in Tooltip Database

**File:** `docs/app.js:19-276` (cross-referenced with `docs/index.html:2700-2920`)  
**Category:** correctness / bug  
**Issue:**  
`docs/app.js` defines a static dictionary `CITATIONS_DB` containing 32 citation objects. However, 17 of the 31 citations in `docs/index.html`'s active bibliography table (`#ref-1` through `#ref-31`) do not match `CITATIONS_DB`:
- `[1]`: `app.js` has Skolnik (*Introduction to Radar Systems*), while `index.html` text and bibliography have Bilik et al. (*Automotive radar sensing for autonomous vehicles*).
- `[4]`: `app.js` has Bilik et al., while `index.html` has Skolnik.
- `[9]`: `app.js` has Bochkovskiy (YOLOv4), while `index.html` has C. Y. Wang (YOLOv9).
- `[10]`: `app.js` has YOLOv7, while `index.html` has Redmon et al. (YOLOv1).
- `[11]`: `app.js` has YOLOv9, while `index.html` has Ultralytics YOLO.
- `[12]`: `app.js` has Ultralytics YOLOv8, while `index.html` has Focal Loss.
- `[17]`: `app.js` has Microsoft COCO, while `index.html` has Van Trees (*Optimum Array Processing*).
- `[18]`: `app.js` has Guan et al., while `index.html` has V. C. Chen (*The Micro-Doppler Effect*).
- `[23]`: `app.js` has DETRs Beat YOLOs, while `index.html` has Sun et al. (*Point-cloud deep learning*).
- `[29]`: `app.js` has O'Shea & Hoydis, while `index.html` has He et al. (ResNet).
- `[30]`: `app.js` has V. C. Chen, while `index.html` has Lin et al. (*RadDet Benchmark ICASSP 2025*).
- `[32]`: Exists in `app.js` (P. E. Pace), but does not exist in `docs/index.html`.

Because `window.ENABLE_CITATION_TOOLTIPS = true` is enabled in `docs/index.html:2939`, whenever a user hovers over any in-text citation badge, the tooltip displays false bibliographic information.

**Fix:**  
Update `CITATIONS_DB` in `docs/app.js` to match the exact bibliography order in `docs/index.html:2701-2918`, or eliminate `CITATIONS_DB` entirely and parse directly from the DOM (see WR-05).

---

### CR-02: Scope Boundary Violation — Unsanctioned Modifications in `templates/BTP_Report_Template_Overleaf/`

**File:** `templates/BTP_Report_Template_Overleaf/General_Report_Template.tex:304-309` and `templates/BTP_Report_Template_Overleaf/figures/timeline_gantt.pdf`  
**Category:** scope contract / integrity  
**Issue:**  
Phase 2 specification (`02-SPEC.md`) explicitly stipulates:
- *"Scope Restriction: Zero edits to .tex, .bib, or .pdf files in templates/BTP_Report_Template_Overleaf/."*
- *"Modifying PDF or LaTeX files in templates/BTP_Report_Template_Overleaf/ or build/ (e.g. timeline_gantt.pdf) — strictly deferred to a subsequent milestone/phase per explicit user decision."*

Despite this locked invariant, PR #24 diff (`git diff main...HEAD`) includes 7 added lines in `General_Report_Template.tex` and newly tracks `timeline_gantt.pdf` (77.5 KB) in the template directory.

**Fix:**  
Revert all modifications to `templates/BTP_Report_Template_Overleaf/` to match `main`:
```bash
git checkout main -- templates/BTP_Report_Template_Overleaf/
```

---

## Warnings

### WR-01: Ineffective Scope Preservation Test in `tests/test_academic_website.py`

**File:** `tests/test_academic_website.py:272-282`  
**Category:** test gap / false positive  
**Issue:**  
The test runs `git status --porcelain templates/BTP_Report_Template_Overleaf/`. `git status` only inspects uncommitted working copy changes. Because changes in `templates/` were committed in `9e94f03`, `git status --porcelain` returned empty, and the test passed despite committed modifications in `templates/`.
**Fix:**  
Check `git diff` against `main` instead:
```python
git_diff = subprocess.run(
    ["git", "diff", "main...HEAD", "--name-only", "templates/BTP_Report_Template_Overleaf/"],
    capture_output=True,
    text=True,
    check=True,
)
assert not git_diff.stdout.strip(), (
    f"templates/BTP_Report_Template_Overleaf/ has branch commits! Found:\n{git_diff.stdout}"
)
```

---

### WR-02: Lightbox Caption DOM Traversal Bug for Centered Figures

**File:** `docs/app.js:576-582`  
**Category:** bug / edge case  
**Issue:**  
In `initLightbox()`, the code queries:
```javascript
const figureWrapper = img.closest("figure, div[style*='text-align: center'], div");
```
Because `, div` matches any `div`, `.closest()` stops at the immediate wrapper `div` (e.g. `div` with background/border styling in Figure 3.1 and Figure 5.1). The inner `div` has no caption element (`p em`), so `captionEl` is always null. In addition, Figure 5.1 markup uses `<strong ...>` and `<span style="font-style: italic;">` rather than `p em`.
**Fix:**  
Remove trailing `, div` and expand caption selector:
```javascript
const figureWrapper = img.closest("figure, div[style*='text-align: center']");
if (figureWrapper) {
  const captionEl = figureWrapper.querySelector("figcaption, p em, p strong, p");
  if (captionEl) caption = captionEl.textContent.trim();
}
```

---

### WR-03: Scroll-Spy Desynchronization on Bibliography Section

**File:** `docs/app.js:337` and `docs/index.html:2681`  
**Category:** UI robustness / bug  
**Issue:**  
`academicTargets` contains `"#references"`. In `docs/index.html:2681`, `#references` is an empty `<div id="references"></div>` (0px height) at the top of `<section id="bibliography">`. When scrolled into view, the 0px element immediately leaves the observer margin, un-highlighting the active TOC item while reading the bibliography.
**Fix:**  
Change `"#references"` to `"#bibliography"` in `academicTargets` in `docs/app.js:337`, and map the TOC link accordingly.

---

### WR-04: Weakened Offline Resilience Test in `test_showcase_website.py`

**File:** `tests/test_showcase_website.py:216-234`  
**Category:** test coverage gap  
**Issue:**  
Replacing the `http://` / `https://` protocol check with a 5-CDN blacklist (`unpkg`, `cdnjs`, `jsdelivr`, `google fonts`, `google ajax`) permits any other external CDN or domain (e.g. `skypack`, `github.com/raw`, etc.) to be loaded in `<script src>` or `<link rel="stylesheet">` without triggering test failures.
**Fix:**  
Explicitly parse HTML tags and assert that `<script src>`, `<link rel="stylesheet">`, and `<img src>` do not start with `http://` or `https://`, while allowing `<a href="https://...">` hyperlinks for DOIs.

---

### WR-05: Ponytail Anti-Bloat Ladder Violation — Duplicate State in `docs/app.js`

**File:** `docs/app.js:19-276`  
**Category:** necessity  
**Issue:**  
Maintaining a 257-line static JavaScript dictionary `CITATIONS_DB` in `docs/app.js` violates Ponytail Ladder Level 1 (YAGNI) and Level 3 (Browser/DOM capability). All 31 references are already rendered into DOM table rows `#ref-1` through `#ref-31` in `docs/index.html`. Duplicating this state in JavaScript is the root cause of CR-01.
**Fix:**  
Extract citation metadata dynamically on hover directly from the DOM:
```javascript
function showTooltip(badge) {
  const citeKey = badge.getAttribute("data-citation") || badge.textContent.replace(/[\[\]]/g, "").trim();
  const targetEl = document.getElementById(`ref-${citeKey}`);
  if (!targetEl) return;
  const cells = targetEl.querySelectorAll("td");
  if (cells.length < 3) return;
  const authors = cells[1].textContent.trim();
  const title = cells[2].textContent.trim();
  const year = cells.length > 3 ? cells[3].textContent.trim() : "";
  // Render tooltip cleanly from DOM cells
}
```

---

## Info

### IN-01: UTF-8 Byte Order Mark (BOM) in `scripts/verify.ps1`

**File:** `scripts/verify.ps1:1`  
**Category:** code quality  
**Issue:**  
`scripts/verify.ps1` begins with bytes `EF BB BF` (UTF-8 BOM). While PowerShell on Windows handles BOM, it can cause parsing problems in cross-platform/Linux environments or POSIX shell wrappers.  
**Fix:** Save `scripts/verify.ps1` as UTF-8 without BOM.

---

_Reviewed: 2026-11-18T21:38:00Z_  
_Reviewer: gsd-code-reviewer_  
_Depth: deep_
