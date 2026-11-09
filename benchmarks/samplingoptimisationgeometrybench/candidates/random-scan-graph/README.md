# Draft graph QA: a real heat-bath path missing from a public slice

**Scope:** MCMC and Discrete Sampling; structural graph reasoning, provisional
L2. This candidate is outside the live catalog, training exports and public
reader. Compiler replay and the reference-scoring checks are not an
independent editorial verdict, empirical calibration or a model run.

## What is being compared?

The graph asks which of four compiled proofs reach the one-block pointwise
law `HeatBath.heatBathSnd_apply` **within the supplied slice**. An arrow points
from a consumer to a selected theorem constant occurring in its compiled
proof body. The intended distinction is:

- The random-scan singleton formula reaches the one-block law through
  `CoordinateHeatBath.heatBath_eq_cond`; the retained-coordinate theorem
  uses the one-block law directly.
- Fixed-site invariance follows a different selected route: transport of the
  one-block invariance theorem, which uses the joint-law reconstruction
  from disintegration. There is no selected path from that proof to the
  queried pointwise-law theorem.
- Random-scan reversibility calls the public singleton-balance bridge.
  Its proof of balance, however, is the **private** `singleton_balance`
  theorem. The compiled private theorem calls the singleton formula, so
  omitting that vertex hides an actual route. The supplied public graph
  neither disproves the route nor establishes logical independence.

The mathematical distinction is between conditional law, invariance and
reversibility. The positive-start formula is only used at positive atoms;
the private balance proof handles zero-mass atoms separately before applying
the reversibility bridge. None of this gives a convergence rate, an
irreducibility result, or an oracle cost.

The catalog anchor is the existing paired **sogb-021**
(`conditional-resampling-invariance`); its declaration is present in the
question slice. **sogb-006** and **sogb-013** are related public random-scan
views, not newly aligned Lean tasks; **sogb-001** is the public balance bridge.
Treat this draft and any close variant as public-exposed, not as a private
evaluation family. The public theorem modules and local probe are original
Samplinglib material under the [license scope](../../../../LICENSE_SCOPE.md);
the artifacts contain no textbook prose, private corpus, Mathlib proof
bodies or restricted ATLAS material.

## Reproduce and review

From the repository root with pinned Lean 4.33.0 and Mathlib:

```bash
python benchmarks/samplingoptimisationgeometrybench/candidates/random-scan-graph/check_candidate.py --export-review .astis/sog-bench/random-scan-graph-review
```

This replays [the allowlisted public selection](selection.json) using the
existing Bench compiler extractor, and follows the private constant with
[a separate trusted Lean probe](PrivateBalanceTrace.lean).
It checks both recorded artifacts, answer boundaries and four scorer cases
without running submissions. Only `agent/prompt.json` is an agent input.
For an unanchored editorial check, solve that input first, then compare
`review/packet.json` and replay the graph and trace. The operator preview is
under `review/`, never in the model input. It shortens three diagram labels
to fit the existing reader's boxes without altering the frozen prompt.

Before admission, record the independent reviewer and exact question/snapshot
binding; integrate through the canonical graph review, export and site checks.
Do not count the graph as a new theorem, change the existing graph IDs or
promote the draft simply because it compiles.
