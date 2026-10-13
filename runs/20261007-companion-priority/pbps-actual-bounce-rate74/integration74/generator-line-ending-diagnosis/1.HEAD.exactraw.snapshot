# Mathlib-Ready Leaf Reviewer Checklist

Reviewer agents use this checklist before marking a reusable SDE/Sampling leaf
as `formalized-local` or a plausible future Mathlib contribution.  The goal is
not only to make the current paper compile; the goal is a small, stable,
searchable theorem that later papers can call.

## Gate 1: Stable Statement

- The theorem is one leaf, not a bundled paper proof.
- The statement is domain-general unless a local ASTIS namespace is explicitly
  justified.
- All hidden regularity assumptions are explicit: measurability, integrability,
  domination, differentiability, boundedness, nonemptiness, positivity,
  compact support or boundary decay, and conditional representatives.
- Constants and conventions are named rather than buried in prose.
- The statement has not been repeatedly rewritten just to satisfy the current
  proof script.  Persistent failure triggers a statement audit.

## Gate 2: API And File Placement

- The file path matches the mathematical family: `Probability`,
  `ProbabilityDistributions`, `Analysis/Calculus`, `InformationTheory`, or
  `FunctionalInequalities`.
- Existing Mathlib declarations were searched first.
- External projects such as `lean-stat-learning-theory` or `lean-rademacher`
  are cited as port/reference memory, not treated as local proof certificates.
- Imports are the smallest reasonable imports for the family.
- The theorem name would still make sense outside SALD/RMFLD.

## Gate 3: Proof Quality

- The proof route is stable and described in the leaf packet.
- No `axiom`, `sorry`, `admit`, fake `Prop := True`, or fake `trivial` closure.
- No broad wrapper that merely repackages the parent theorem.
- If the proof depends on a large theorem, that theorem is either a compiled
  local declaration or a named proof obligation.
- The declaration is covered by `lake build` and `lake build Tests`.

## Gate 4: Retrieval And Memory

- The leaf is recorded in `AutoSamplingTheory/TechnicalLemmas/Registry.lean`
  if it is meant to be callable memory.
- The technical-lemma registry, retrieval index, module graph, and card are
  refreshed.
- The external source is recorded under `research-wiki/external-lean-libraries/`
  or the port queue.

Reviewer outcome should be one of:

- `accept-mathlib-ready-local`: compiled, small, reusable, and correctly placed;
- `accept-astis-local`: compiled but intentionally project-local;
- `split-required`: target too large for one lower agent;
- `regularity-gap`: hidden assumptions missing;
- `api-search-required`: likely already in Mathlib or nearby ASTIS memory;
- `statement-risk`: possible false statement, counterexample, or wrong version.
