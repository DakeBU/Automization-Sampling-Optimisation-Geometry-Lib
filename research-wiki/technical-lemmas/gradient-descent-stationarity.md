# Gradient descent: accumulated descent and approximate stationarity

Source: Chewi, *Lectures on Optimization*, arXiv:2605.07006v1,
Theorem 3.7 and proof; Section 2 attained-minimum convention; Lemma 3.1.

SAU: `ANDI-OPT-gd-stationarity-001`.
Cells: `ASTIS-SHARED-gradient-descent-sum-sq` and
`ASTIS-SHARED-gradient-descent-stationarity`.
Candidate proof commit: `c592c86bd16024618fab58a27a00f296bb2c8a34`.

For a complete real Hilbert space, actual gradient update `T(x)=x-h∇f(x)`,
and the global quadratic upper model with `βh≤1`, the new shared module
`Analysis/GradientDescentStationarity.lean` supplies:

- `gradient_descent_sum_sq_bound`: for `h≥0` and any natural `N`,
  `(h/2) Σ_{k<N} ‖∇f(T^k x₀)‖² ≤ f(x₀)-f(T^N x₀)`.
- `exists_gradient_descent_norm_le`: for `h>0`, `N≥1` and a supplied global
  minimizer `z`, some `k<N` satisfies
  `‖∇f(T^k x₀)‖ ≤ sqrt(2(f(x₀)-f(z))/(N*h))`.

The mathematical increment is cumulative dissipation and a nonconvex
best-iterate certificate for actual updates. It does not assume convexity, PL,
a scalar recurrence, or a small-gradient witness. It does not construct the
minimizer, prove last-iterate convergence or global optimality, or close a
companion-paper theorem. The generic stopping consumer in the cell is planned,
not an existing Lean dependency.

## Retrieval and reuse

- Reuse `GradientDescentBasic.gradient_step_descent_of_quadratic_upper_bound`.
  Its production file and existing audits are unchanged.
- Pinned Mathlib `db584cd`: `Finset.mul_sum`, `Finset.sum_le_sum`,
  `Finset.sum_range_sub'`, `Finset.exists_le_of_sum_le`,
  `Real.le_sqrt_of_sq_le` and actual iterate successor identities.
- Existing `GradientDescentPL` needs PL; `GradientDescentValue` uses convexity.
  Neither is the nonconvex stationary-iterate bound.
- SPHMC `TerminalReferenceGradientDescent.gradient_decay` is a private,
  strongly-convex geometric bound with stronger hypotheses. It is not a duplicate
  of the present result and is not modified or used as a parent.
- Scoped pinned Optlib `5da27c5` GD and CvxLean `c62c2f` searches did not locate
  the exact nonconvex bound. This is a bounded retrieval result, not a claim of
  exhaustive absence across formal libraries. No external code is ported.

## Source and regularity boundary

The source's smooth Euclidean problem supplies the upper model. The local proof
consumes that model algebraically on a complete real Hilbert space and uses the
actual, totalized Lean gradient. It makes no claim that notation alone supplies
differentiability. Signed `β` are an explicit model-domain extension; the
reciprocal source restriction agrees with the product restriction when `β>0`.

The printed normalized theorem omits explicit `h>0,N≥1`. The zero-step and empty
range expressions are not valid ordinary normalized bounds. With
`f(t)=t²/2,β=1,z=0,x₀=1,N=1`, steps `h=0` and `h=-1` yield the false Lean-totalized
comparison `1≤0`. The original source, local proposition, semantic mismatch and
independently reviewed source overlay remain distinct in the publication audit.
The unnormalized cumulative theorem legitimately includes `h=0,N=0`.

## Verification and next boundary

Focused test `Tests.Shared.GradientDescentStationarity` passes (2436 jobs),
with only `propext`, `Classical.choice`, `Quot.sound`. Tests instantiate the actual
quadratic gradient, a constant objective with `β=0`, and zero-step accumulation.
Independent proof/source/repair artifacts are stored in
`runs/semantic-roundtrip/andi-opt-gd-stationarity/`.

Conceptual-mirror audit: none-found. Accumulated energy dissipation is already
represented in `family:metric-gradient-flow`; no new cross-space transport or
PL/coercivity implication is asserted by the averaging argument.

Admission complete: independent proof reviewer `gds_integration_review`,
source-blind decoder `gds_blind`, source reviewer `gds_source`, and independent
exact-domain-overlay reviewer `gds_repair`. Source acceptance retains
`domain-mismatch` for the disclosed algebraic/Hilbert generalization. Root imports
and Registry entries are integrated; the count is 416, not a paper-completion count.
Do not repeat the historical missing-root-test mistake: put the new import in
`Tests.lean`'s initial import block, before module documentation.

Next optimization target is selected only after this source boundary is admitted;
Chewi Exercise 3.2 optimal-step contraction is a candidate requiring a fresh
reuse/source audit. The unmerged curvature proposal remains separate.


## Integration notes

- Frozen aggregate candidate: `ce646467901c8b0d143411782f340716fb6b3637`.
  Canonical gate PASS9202 at `2026-09-13T01:07:51.631548+00:00`, including root
  Tests, ATLAS 36469 declarations/26 books, and fake-closure checks. Exact copied
  source-digest evidence: `runs/semantic-roundtrip/andi-opt-gd-stationarity/canonical-gate-evidence.json`.
- Publication PASS77 source items, semantic registry PASS92 audits/6 repairs,
  frontier protocol PASS100 cells. Whole-module publication fingerprints and
  independent packet/run hashes checked; unchanged prior source/audit objects
  and the old Basic/PL/Value proofs preserved.
- Website build/check PASS671 modules, 3993 declarations and 77 reviewed teaching
  declarations. Both affected `graph-check --cell` calls passed. Added one module
  and two compiled declarations, their chapter03 bindings, two source audits and
  the separately accepted domain overlay. Existing shared descent is reused.
- Reader: `libraries/optimisation/chapter-03.html#chewi-opt-v1-theorem-3-7`.
  Graph focus: `lean-foundations.html?view=lean&focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentStationarity.exists_gradient_descent_norm_le&q=AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentStationarity.exists_gradient_descent_norm_le`.
  Root inspected actual rendered reader at desktop1280/mobile390: formulas,
  explicit hypotheses, source mismatch/accepted overlay, all four initially
  closed Lean disclosures, and opened stationary statement/proof. No KaTeX
  errors or document overflow. The focused branch has 9 nodes/12 edges and 4
  direct relations highlighted. Solid module `declares` and dashed incomplete
  scanner/source correspondence are distinct; both new theorem nodes appear.
  Mobile fit-view graph labels are small; the node detail panel shows the full
  wrapped declaration, compiled badge and source/reference evidence. This is
  root visual evidence, not an independent reviewer screenshot claim.
- Integrated the exact original-owner historical PR301 MERGED event and the two
  metadata-file updates from `f0fd96f035cd320f32ded0f7befdc5cb68376aa4`, following
  independent preservation review. No new transition impersonates that owner,
  no duplicate event, and no old mathematical evidence is overwritten.
- Remaining boundary: best-iterate certificate in the explicit model only;
  neither companion paper is complete. No new conceptual transport is claimed.
  Next candidate: fresh source/reuse audit of optimal-step contraction,
  Chewi Exercise3.2. Do not repeat this now-admitted Theorem3.7 work.

Merged and pushed directly to `main` at `b00c64ad810af0449bb3c0fae38ff3df8eeed59c` under the standing user authorization. SAU is `MERGED`; its stabilization reservation is released. Remote post-push CI/deployment is separate from the local gate evidence above.


Successor checkpoint (2026-09-13): Exercise3.2 source/reuse audit and optimal-step
SAU now passed independent admission and aggregate checks; see
[gradient-descent-optimal-step.md](gradient-descent-optimal-step.md). Do not
schedule the same endpoint/minimax target again. Further work requires a new
bounded source/DAG delta. This note does not change the Theorem3.7 evidence.
