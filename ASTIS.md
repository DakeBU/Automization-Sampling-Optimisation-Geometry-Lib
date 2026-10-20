# ASTIS Dashboard

## Status

- Active textbook task: Chewi Chapter 1 faithful formalization and foundation closure
- Active research task: `ASTIS-SALD-001`
- Lean foundation target: `AutoSamplingTheory/TechnicalLemmas/StochasticProcesses/`
- Build gate: `python3 tools/astis.py check`

## Current Priorities

1. Keep Sinho Chewi's textbook as the primary theorem spine.  Every numbered
   Chewi definition/display/theorem keeps its exact source correspondence even
   when the published proof omits standard stochastic-analysis details.
2. Build the omitted SDE/stochastic-calculus layer once as reusable ASTIS-owned
   infrastructure.  The source policy and reference hierarchy are recorded in
   `research-wiki/sampling-sde-library/foundation_source_policy.md`.
3. For Chapter 1, finish the dependency chain
   `L² completion -> continuous Ito version -> pathwise congruence -> stopping ->
   localization overlap -> global local-martingale gluing`, then close the exact
   source-facing Chewi items and their focused tests/evidence/teaching pages.
4. Use Karatzas--Shreve as the default rigorous stochastic-calculus backbone,
   Protter for stochastic integration/localization, Shreve II and Øksendal for
   pedagogy, Revuz--Yor for deeper continuous-martingale facts, and
   Bakry--Gentil--Ledoux plus the cited Langevin papers for the later PI/LSI
   convergence layer.  These are supplementary foundation sources, never
   substitutes for Chewi's source statement.
5. Maintain an ASTIS-owned technical lemma memory for Mathlib-based
   probability tools.  The short entry point is
   `research-wiki/technical-lemma-memory/README.md`; external material is only
   a provenance/source aid until the corresponding local declaration builds.
6. Faithfully index and translate the original VA-SALD paper proofs, excluding
   `sald_version_2.tex`, while treating the Chewi program as the reusable SDE
   foundation consumed by SALD.
7. Create PRIVATE exploratory proof-route memory without attempting large theorem
   proofs prematurely.
8. Preserve Phase 1 faithful-source discipline before Phase 2 reusable API
   reorganization.
9. Keep the project-paper LaTeX export batch-based: update it after the final
   reviewer gate of a multi-hour run.
10. Adopt MathCode-style proof diagnostics where useful: theorem-reuse search
    before duplicate interfaces, hidden-assumption scans, placeholder scans,
    proof statistics, and subgoal decomposition as an internal work plan.

## Foundation-source rule

A citation to a classical textbook is never a proof closure.  For every hidden
Chewi prerequisite we record (i) the exact Chewi consumer, (ii) the fully
stated mathematical lemma and hypotheses, (iii) the best rigorous foundation
reference, (iv) an optional pedagogical companion, and (v) the exact Mathlib or
ASTIS Lean declaration.  The public website should expose the mathematical
statement/proof and foundation references before the optional Lean details.

## First Commands

```bash
python3 tools/astis.py init
python3 tools/astis.py source-index ASTIS-SALD-001
python3 tools/astis.py source-index ASTIS-PRIVATE-001
python3 tools/astis.py check
python3 tools/astis.py proof-diagnostics
python3 tools/astis.py launch-sald-6h
python3 tools/astis.py export-latex
```

Public automation reference:
https://github.com/DakeBU/Quantum-Computing-Block-Encoding/tree/wip/ghl2025-faithful-20260518-0201

MathCode workflow reference:
https://github.com/math-ai-org/mathcode
