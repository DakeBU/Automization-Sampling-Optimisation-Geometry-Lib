---
name: astis-conversion-window
description: Maintain synchronized LaTeX, Lean, proof-obligation, and human-readable views for one sampling/SDE proof target.
argument-hint: "[task id]"
---

# ASTIS Conversion Window

Use this whenever a theorem or proof fragment moves between paper notation,
Lean names, and human explanation.

## Steps

1. Open or create `conversion-windows/<task>.md`.
2. In Phase 1 faithful-paper work, treat the window as a transcript first:
   prioritize exact source-to-Lean mapping over reusable library
   reorganization.
3. Copy the exact source theorem, equation, or proof fragment.
4. Map each symbol to a Lean declaration or a planned declaration.
5. Add the sampling contract: state space, laws, velocity/score/drift,
   target path, guide/reward, discretization, and error metric.
6. Add a proof-DAG pane with block interfaces, dependencies, Lean names,
   source anchors, and reuse sites.
7. Add cited-result rows for every standard or external analytic fact.
8. If a proof block is blocked, run the source-dependency audit before
   assigning more lower-agent proof search.
9. Keep the window synchronized after Lean edits and after reviewer feedback.
10. Maintain two-way translation: source LaTeX/Markdown to Lean before lower
    work, and Lean/proof-obligation status back to Markdown/LaTeX after lower
    and reviewer work.

## Rule

If a symbol, assumption, or proof step cannot be mapped, record the missing
interface as a proof obligation. Do not silently weaken the theorem or replace
the source statement with an easier one.

During Phase 1, do not turn the window into a textbook or generalized API
design document.  Phase 2 can reorganize reusable SDE/Sampling interfaces after
the faithful transcript is complete.
