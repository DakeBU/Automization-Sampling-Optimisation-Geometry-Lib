# Exact weighted radial Gaussian and Eq. (51)

[The source Eq. (51)](https://arxiv.org/html/2611.05813v1#S6.E51)
takes expectation over the actual coefficient vector at one fixed x.
`WeightedRadialMGF.weightedRadialLevels_gaussian_mgf` proves the weighted
centered law, integrability of its negative exponential, and the precise
expectation `exp (V / 2)` with `V = n * ∑ i, β_i² * C_i(x)² * v_i`.
It uses the original full carrier, the literal fields and the same location
throughout. The source's deterministic positive weights specialize the
theorem's arbitrary deterministic real weights; no estimate on their
recursion, large-n bound or admissibility is generalized.

The implementation extracts exact marginals and independence from
`radialLevels_hasLaw`, applies Mathlib's deterministic Gaussian scaling
and finite independent Gaussian sum, derives all needed moments, and
evaluates `mgf_gaussianReal` at −1. Positivity plus `mgf_pos_iff`
verifies the real integral is not a default value for a nonintegrable
function. There is no positive-variance premise and no new generic wrapper.

The signature/source review was sealed at
`0e4eacb18`; candidate
`9792e5925` passed focused Tests3195 and the
exact anonymous proposition check under Lean4.33.0 / pinned Mathlib.
The Cell and accepted audit carry current state.

## Integration boundary

The exact reviewed Lean module, test, lesson and publication binding
are unchanged on the `3fe9ab07`-based release candidate. The canonical
ASTIS gate passed (including Tests, 9650 jobs), with one new Registry
entry (617 candidate). The exact graph lookup and desktop/mobile reader
checks passed, including visible formulae and adjacent Lean folds.
The reference from the actual joint radial law is a scanner edge;
source and audit relations do not prove another declaration. Remote
acceptance, merge, deployment and postmerge purification are separate.

## Next mathematical consumers

The §6.1 consumer is the literal cutoff envelope: `0 ≤ C_i(x) ≤ 1`
and its unit plateau on the good shell, followed by the pointwise
envelope and plateau for m(x). Separately verified local packets cover
those steps, the product-space integral of Eq. (70) and the normalized
reference location marginal of Eq. (71); none is part of this release.
For the next shell estimate, §7 uses the actual coordinate Gaussian
law, chi-square Chernoff bounds and a union bound over the source
blocks. The coefficient shift in Eq. (65) requires a separate
conditional-law argument.

The §6.2 conditional comparison is a different branch: show the actual
gate and earlier load factors are measurable in the earlier coefficient
blocks; then derive conditional independence and the iterative estimate.
The linear weight is not the full nonlinear weight outside the good event.
No mass estimate or main lower bound is closed.
