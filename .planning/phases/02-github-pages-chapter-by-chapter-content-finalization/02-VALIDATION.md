---
phase: "02"
slug: "github-pages-chapter-by-chapter-content-finalization"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-18"
---

# Phase 02 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.1.1 |
| **Config file** | `pytest.ini` / default config |
| **Quick run command** | `pytest tests/test_academic_website.py tests/test_showcase_website.py` |
| **Full suite command** | `pwsh -File ./scripts/verify.ps1` |
| **Estimated runtime** | ~0.5 seconds (pytest) / ~15 seconds (full verify.ps1) |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_academic_website.py tests/test_showcase_website.py`
- **After every plan wave:** Run `pwsh -File ./scripts/verify.ps1`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-08-01 | 08 | 1 | R1 | — | Repository audit & artifact mapping | verification | `pytest tests/test_academic_website.py -k test_evidence_audit_dossier` | ❌ W0 | ⬜ pending |
| 02-08-02 | 08 | 1 | R1, R2 | — | FMCW math & reference metadata verification | verification | `pytest tests/test_academic_website.py -k test_evidence_audit_dossier` | ❌ W0 | ⬜ pending |
| 02-09-01 | 09 | 2 | R2 | — | Zero legacy 58.8 μs parameters in active chapters | unit / DOM | `pytest tests/test_academic_website.py -k test_no_legacy_radar_parameters` | ❌ W0 | ⬜ pending |
| 02-09-02 | 09 | 2 | R3, R4 | — | RadDet spectrum sensing terminology & split footnote | unit / DOM | `pytest tests/test_academic_website.py -k test_chapter_finalization_phase2` | ✅ | ⬜ pending |
| 02-09-03 | 09 | 2 | R5 | T-02-01 | Sequential citations [1..N] & DOM textContent tooltips | unit / DOM | `pytest tests/test_academic_website.py -k test_active_citation_anchors_and_tooltips` | ❌ W0 | ⬜ pending |
| 02-09-04 | 09 | 2 | R6 | — | Scope check: 0 LaTeX edits & 7-chapter draft intact | integration | `pytest tests/test_academic_website.py -k test_scope_and_archival_preservation` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_academic_website.py::test_evidence_audit_dossier` — validates `02-EVIDENCE-AUDIT.md` existence and mandatory sections
- [ ] `tests/test_academic_website.py::test_no_legacy_radar_parameters` — validates zero legacy $58.8\ \mu\text{s}$ or $0.258\text{ m/s}$ in active Chapters 1–5
- [ ] `tests/test_academic_website.py::test_active_citation_anchors_and_tooltips` — validates active citation numbering sequential [1..N] and presence in `docs/app.js`
- [ ] `tests/test_academic_website.py::test_scope_and_archival_preservation` — validates zero changes in `templates/BTP_Report_Template_Overleaf/` and archival draft intact

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| KaTeX visual math rendering | R2 | Visual display check | Open `docs/index.html` in browser, verify KaTeX formulas in Chapter 2/3 render cleanly without raw LaTeX artifacts |
| Tooltip hover interaction | R5 | User interaction | Hover over citation anchors `[1]`, `[2]`, etc. in browser, verify tooltip popovers appear with correct title, authors, and DOI link |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
