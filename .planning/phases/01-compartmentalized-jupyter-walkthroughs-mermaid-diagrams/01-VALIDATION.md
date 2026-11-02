---
phase: "1"
slug: "compartmentalized-jupyter-walkthroughs-mermaid-diagrams"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-23"
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x / unittest |
| **Config file** | None — standard pytest/unittest discover |
| **Quick run command** | `python -m pytest tests/test_walkthrough_notebooks.py -v` |
| **Full suite command** | `pwsh -File ./scripts/verify.ps1` |
| **Estimated runtime** | ~6 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_walkthrough_notebooks.py -v`
- **After every plan wave:** Run `pwsh -File ./scripts/verify.ps1`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | PRES-01, PRES-02 | — | N/A | unit/smoke | `python -m pytest tests/test_walkthrough_notebooks.py -k test_notebook_1 -v` | ❌ W0 | ⬜ pending |
| 01-02-01 | 02 | 1 | PRES-03, PRES-04 | — | N/A | unit/smoke | `python -m pytest tests/test_walkthrough_notebooks.py -k test_notebook_2 -v` | ❌ W0 | ⬜ pending |
| 01-02-02 | 02 | 2 | VERIF-02 | — | N/A | integration | `pwsh -File ./scripts/verify.ps1` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_walkthrough_notebooks.py` — balanced smoke and syntax validator for both notebooks

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Visual rendering in VS Code & GitHub | PRES-01, PRES-03 | Visual inspection of Mermaid diagrams and collapsible SVG fallbacks | Open both notebooks in VS Code notebook editor, verify native diagrams render, expand details tag to inspect SVG |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending 2026-09-23
