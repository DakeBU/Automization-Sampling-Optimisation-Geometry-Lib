# Native Optlib admission: nonsmooth subgradient method

This is mathematical assimilation, not a bibliography entry or a dependency on
Optlib's old toolchain. The native module is
[`SubgradientMethod.lean`](../AutoSamplingTheory/TechnicalLemmas/Analysis/SubgradientMethod.lean),
over the existing `ConvexSubgradient.SupportsAt` definition and the repository's
Lean 4.33.0 / fixed Mathlib. It is imported by the analysis aggregate, Registry,
root library and root Tests.

## Actual admitted mathematical edges

1. `norm_le_of_supportsAt`: global Lipschitz growth bounds every supplied global
   supporting vector. Its consumer is the next theorem, not a hypothetical use.
2. `sum_weighted_gap_le`: the actual recurrence telescopes weighted function-value
   gaps while retaining the terminal squared distance. It calls the norm bound.
3. `exists_gap_le`: a nonempty finite run and positive steps give a best-index
   objective-gap bound for any comparator. It calls the weighted telescope.

No separate convexity hypothesis is needed once global supporting vectors are
supplied. This does not assert that they exist. Completeness, differentiability
and a minimizer are not used. Zero steps and the empty horizon are permitted only
in the division-free intermediate; division in the best-index result requires
positive total step. The intermediate is an explicitly proved generalization,
not a claim of equivalence to the upstream normalized theorem.

## Source, proof and reader

- Primary source: [Optlib, immutable revision
  `5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3`](https://github.com/optsuite/optlib/blob/5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3/Optlib/Algorithm/SubgradientMethod.lean#L80-L232).
  The original Apache-2.0 notices are retained.
- The source-only topology review is distinct from the implementation graph:
  [v3 acceptance](../runs/20261103-optlib-intake/source-topology-review-v3.json)
  retains the earlier revisions and the exact use-site obligations.
- Canonical human formula proofs, assumptions and Lean walkthroughs live in
  `website/content/declaration_lessons/optlib-subgradient-method.json`; source
  bindings are in `website/content/publications/optlib-subgradient-method.json`.
  The generated Optlib reuse page and Optimisation chapter 6 link those readers.
  Exact Lean statements and proofs are folded immediately beside the mathematics.
- Three anonymous inputs under `runs/blind/` were decoded without source access.
  The subsequent independent source/code reviews are under
  `runs/20261103-optlib-intake/reviewer-*.result.json`; accepted decisions are
  recorded in the corresponding semantic audit fragments. These decisions do
  not themselves mean that a chapter or paper is complete.
- Canonical cells: `ASTIS-OPT-optlib-subgradient-norm`,
  `ASTIS-OPT-optlib-subgradient-energy`, `ASTIS-OPT-optlib-subgradient-method`.
  One connected substantive advance owns the packet; three cells identify three
  distinct real declarations, not three wrapper copies.

## Reproduce

```bash
lake build Tests.Shared.SubgradientMethod
lake build Tests
python tools/astis.py check
python tools/astis_semantic_roundtrip.py check
python tools/astis_frontier_cells.py check
python -m unittest tools.tests.test_research_resources tools.tests.test_project_authors_footer
python website/scripts/build_site.py
python website/scripts/check_site.py
python tools/astis_publication.py graph-check --cell ASTIS-OPT-optlib-subgradient-method
python -m py_compile tools/astis.py tools/astis_site.py
git diff --check
```

The focused test applies the actual theorem to the nonconstant nonsmooth
objective `abs`, with iterates `(1/2)^k`, supporting vectors `1` and steps
`(1/2)^(k+1)`. It also exercises the empty-horizon telescope and prints the
axioms of all three public theorems (only the standard Lean logical axioms).
The integration test's Registry baseline is 593; this number is not source or
chapter completion coverage.

## Still open

No subgradient existence/selection, random/measurable oracle, specialized
step-policy complexity, asymptotic iterate convergence or sampling theorem has
been obtained here. The other inventoried Optlib modules and Forum papers are
still external references unless individually admitted through the same source,
compiler, consumer and independent-review chain. Bibliographic completeness is
not mathematical completion. The existing four-paper Goal and its red
boundaries are unchanged.
