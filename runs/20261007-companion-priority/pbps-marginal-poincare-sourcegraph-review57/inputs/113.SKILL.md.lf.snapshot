---
name: astis-source-dependency-audit
description: Audit a blocked faithful-paper proof step against local TeX, bibliography, Mathlib, and SLT reuse status before more proof search.
argument-hint: "[paper key or task id]"
---

# ASTIS Source Dependency Audit

Use this when a faithful-paper proof block is blocked or appears to need an
analytic theorem that is not already formalized locally.

## Audit Workflow

1. Identify the blocked Lean statement and the exact source theorem, lemma,
   equation, or proof paragraph.
2. Read local TeX around the anchor. For SALD, the source root is
   `/home/nitanda_sub/mark/repos/sald/paper`, excluding `sald_version_2.tex`
   for `ASTIS-SALD-001`.
3. Inspect nearby citations and the bibliography when the paper says
   "standard", "by LSI", "by DV", "by Gronwall", or similar.
4. Classify the missing ingredient:
   - `internal-paper-step`
   - `external-cited-result`
   - `mathlib-available`
   - `slt-port-candidate`
   - `local-lemma`
   - `source-contract-gap`
   - `contract-drift`
5. Update `research-wiki/cited-results/` or `proof-obligations/` with the exact
   statement, source, dependencies, and local Lean target.
6. Write the next allowed lower-agent packet. It should be one declaration or
   one obligation refinement, not broad theorem search.

## Reviewer Rule

Reviewer rejects continued proof search after a blocked faithful-paper step
unless this audit exists and classifies the dependency.

