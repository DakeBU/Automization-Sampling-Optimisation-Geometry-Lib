# Affine gradient prerequisite — recoverable local checkpoint

Owner: `andi-affine-root`; contribution branch: `codex/andi-boumal-affine-gradient`.
Parent main: `c05de12e6a8ca7af8ce2df8608836f8d4e90f617`.

One canonical theorem derives the genuine gradient of `v ↦ f(a + v)` on a
complete real subspace with inherited inner product. It projects the ambient
gradient into the direction space. The translation is never added to the
gradient vector. The statement seal predates the proof and the independent
source-only topology review predates implementation.

Focused checks passed on Lean 4.33.0 / pinned Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`:

- `lake build AutoSamplingTheory.TechnicalLemmas.Geometry.AffineGradient`
- `lake build Tests.Shared.AffineGradient`: actual translated linear objective
  and elimination of an ambient normal gradient.
- `#print axioms`: only `propext`, `Classical.choice`, `Quot.sound`.

This checkpoint is **locally compiled, review pending**, not independently
verified or ready to merge. Publication binds the theorem as a **prerequisite**
for Boumal §3.8; no Proposition 3.61 proof progress is awarded. The Hilbert-space
and pointwise-regularity generalizations are explicit. Nonlinear tangent-space
identification, differential restriction, extension independence, and smooth
gradient fields remain open. No unanchored Chewi consumer is claimed.

Independent decoder and source review evidence will be saved from real runs.
The audit is honestly `draft` at this checkpoint. Reader/graph rendering,
visual inspection, strict changed-declaration gates and the full ASTIS gate
are pending.

The existing global stabilization lane belongs to
`ASTIS-SA-20261005-SPHMCImplementedPhaseKernel`. Consequently this owner has not
changed shared root imports, `Tests.lean`, Registry or canonical site/graph
aggregations. Before final integration the sole stabilization owner must add
`import Tests.Shared.AffineGradient` to `Tests.lean` (and the shared module to
the appropriate umbrella), then run the full gates. A standalone green build
does not mean root CI exercises the test.

The pre-existing `.DS_Store` files and optimisation reuse-audit note are
preserved and excluded from this contribution.
