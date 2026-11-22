---
name: add-question
description: Captures, formulates, and records academic thesis defense questions and rigorous mathematical answers into docs/ADVISOR-DEFENSE.md. Use whenever the user asks to add an advisor defense question, captures study queries, prepares professor defense Q&As, or mentions 'add question', 'advisor defense', 'defense question', 'store question in advisor defense', 'add study question', or 'professor challenge'. Do NOT use for general code troubleshooting or non-academic task tracking.
---

# Add Question Skill (Advisor Defense Dossier)

## Purpose & Scope

This skill enables rapid, rigorous capture of conceptual and mathematical questions encountered during study or research, formatting them as formal **Focus Questions** in `docs/ADVISOR-DEFENSE.md`.

It enforces a **Human Confirmation Gate**: the drafted answer is always presented directly in the chat first so the user can inspect, refine, or confirm it before it is committed to the advisor defense document.

---

## Operating Protocol

### Step 1: Inspect Current Dossier State

1. Read `docs/ADVISOR-DEFENSE.md` to identify:
   - The current highest question index (e.g., `Focus Question 6`).
   - Prevailing formatting patterns, mathematical notation, and citation conventions.
2. Ensure alignment with the project's core research invariants:
   - **Overarching Theme**: Resource-efficient AI for radar signal processing and detection.
   - **Candidate Approaches**: Preserve both Approach A (computational reduction via lightweight architectures, pruning, quantisation, distillation, adaptive computation) and Approach B (CPU-oriented model development and inference).
   - **Distinct Tracks**: Keep synthetic 77 GHz FMCW radar perception distinct from real-world RadDet wideband spectrum sensing.

### Step 2: Formulate Concise, Human-Relevant Defense (In Chat First)

1. Draft the question and response adhering strictly to a **spoken-ready, conversational yet technically sharp** defense structure:
   ```markdown
   ## Focus Question [N+1]: [Concise Title]

   ### Professor's Challenge
   > *"[Realistic question phrased as an advisor challenge]"*

   ### Direct Defense (Spoken-Ready)
   **Core Takeaway:** [1–2 clear, direct sentences answering the question head-on, exactly as you would speak it to the professor].

   **Key Points:**
   - **[Factor 1 (e.g. Bandwidth & Resolution)]:** [Punchy explanation with only the key formula if essential, e.g., $\Delta R = \frac{c}{2B}$].
   - **[Factor 2 (e.g. Physical Antenna Size)]:** [Practical hardware reality, e.g., $\lambda \approx 3.9\text{ mm}$ fits on a chip].
   - **[Factor 3 (e.g. Environmental / Regulatory)]:** [Real-world constraint, e.g., atmospheric window and global spectrum standards].

   **Summary:** [1 closing sentence wrapping up the engineering decision].
   ```

2. **Present the drafted answer in the chat to the user.**
3. Explicitly ask the user for confirmation:
   - *"Does this concise defense sound natural and ready for your viva, or would you like to adjust the tone or emphasis before writing to `docs/ADVISOR-DEFENSE.md`?"*

### Step 3: Append to `docs/ADVISOR-DEFENSE.md` Upon User Confirmation

1. Upon receiving the user's approval (or requested edits):
   - Append the finalized `Focus Question [N+1]` block to the end of `docs/ADVISOR-DEFENSE.md`.
   - Update the Executive Summary sentence mentioning the count of focus questions (e.g., update _"six critical focus questions"_ to _"seven critical focus questions"_).
2. Maintain clean Markdown formatting:
   - Use KaTeX math blocks (`$$...$$`) for multi-line derivations and inline `$...$` for scalar variables.
   - Ensure clean horizontal rules (`---`) between questions.

### Step 4: Deterministic Verification Gate

1. Notify the user with audible confirmation:
   ```powershell
   pwsh -File ./scripts/agent-alarm.ps1 -Type Success -Message "Advisor defense question added and verified."
   ```

---

## Technical Standards for Answers

- **Spoken-Ready & Human-Relevant**: Answers must sound like a natural, confident response during an oral viva/defense, not a copied textbook chapter. Avoid wall-of-text algebra and tedious multi-step proofs unless explicitly required.
- **Focus on the "Why"**: Highlight engineering trade-offs, physical intuition, and hardware reality rather than formula dumps. Use at most 1–2 essential governing relationships (e.g. $\Delta R = \frac{c}{2B}$, $\lambda = \frac{c}{f_c}$).
- **Distinguish Reality from Proposal**: Never claim unverified empirical speedups or completed experiments. Distinguish published benchmarks (e.g. RadDet ICASSP 2025 Table III) from proposed investigations.
- **Maintain Invariant Decoupling**: Keep synthetic 77 GHz FMCW automotive radar distinct from real-world RadDet wideband RF spectrum sensing.
