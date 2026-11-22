---
phase: "03"
slug: "academic-portal-priority-0-polish-mobile-ui-ieee-citation-ca"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-11-19"
---

# Phase 03 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest` 8.3.4 with `pytest-cov` |
| **Config file** | `pytest.ini` |
| **Quick run command** | `pytest tests/test_academic_website.py tests/test_showcase_website.py -q` |
| **Full suite command** | `pwsh -File ./scripts/verify.ps1` |
| **Estimated runtime** | ~5 seconds quick / ~25 seconds full suite |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_academic_website.py tests/test_showcase_website.py -q`
- **After every plan wave:** Run `pwsh -File ./scripts/verify.ps1`
- **Before `/gsd-verify-work`:** Full suite must be green (58+ tests, $\ge 90\%$ coverage, 0 failures)
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | PORTAL-VERIF-01 | — | Scaffold Wave 0 test stubs for mobile touch targets and overflow | unit / DOM | `pytest tests/test_academic_website.py -q` | ✅ Exists | ⬜ pending |
| 03-01-02 | 01 | 1 | PORTAL-MOB-01 | — | `#nav-toggle` and TOC links enforce $\ge 44\times 44\text{px}$ touch targets; drawer body scroll lock; morphing icon | unit / DOM | `pytest tests/test_academic_website.py -k test_mobile_drawer -q` | ❌ W0 | ⬜ pending |
| 03-01-03 | 01 | 1 | PORTAL-MOB-02, PORTAL-MOB-03 | — | Two-tier table/formula scroll wrappers with fluid font floor; single-column reflow below 900px; responsive media | unit / DOM | `pytest tests/test_academic_website.py -k test_overflow -q` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 2 | PORTAL-CITE-01 | T-03-01 | Safe DOM card construction without `innerHTML` (CWE-79); active globally by default | unit / DOM | `pytest tests/test_academic_website.py -k test_citation_popover -q` | ❌ W0 | ⬜ pending |
| 03-02-02 | 02 | 2 | PORTAL-CITE-02 | — | Mobile bottom-sheet modal card on <600px; desktop floating popover; Section 9 pulse jump (`.highlight-pulse`) | unit / DOM | `pytest tests/test_academic_website.py -k test_citation_bottom_sheet -q` | ❌ W0 | ⬜ pending |
| 03-02-03 | 02 | 2 | PORTAL-VERIF-01 | T-03-02 | Zero external CDN scripts or stylesheet leaks; 100% deterministic gate pass | integration | `pwsh -File ./scripts/verify.ps1` | ✅ Exists | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_academic_website.py` — Stubs for `test_mobile_drawer_and_touch_targets`, `test_overflow_containment_and_scroll_wrappers`, `test_citation_popover_active_by_default`, and `test_citation_bottom_sheet_and_pulse_jump`.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Touch drag / momentum scroll feel | PORTAL-MOB-02 | Subjective gesture smoothness cannot be fully verified via static AST parsing | Open `docs/index.html` on mobile device or Chrome DevTools Device Mode (360px viewport), swipe tables and formula wrappers horizontally, verify smooth momentum glide. |
| Visual appearance of glowing pulse jump | PORTAL-CITE-02 | Transient CSS keyframe animation | Click "View in Reference List" in citation card, verify smooth scroll to Section 9 and glowing sky-blue highlight pulse. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** Approved 2026-11-19
