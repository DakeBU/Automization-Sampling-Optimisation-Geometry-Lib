# Statement Seal — lower-bounds/chewi-opt-v1-exercise-4-1, v1

This prospective seal covers the exact source-facing interface, not the
earlier exploratory prototype, any Lean proof, or Bench admission.

- Source: Sinho Chewi, Lectures on Optimization, arXiv:2605.07006v1,
  §4.2, Exercise 4.1, printed/PDF p. 28, inheriting Def. 4.3 and Thm.
  4.4's setting and witness. PDF SHA-256
  9e28afeacb0121b79691fadc6af9c145ccd787bffd2cf9c3f2310806112e644b.
- Prospective declaration: AutoSamplingTheory.ExampleCases.LowerBounds.
  GradientSpanDistance.exercise_4_1, with explicit binders corresponding
  exactly to the outer universals/implications of the [type-only probe](chewi-exercise-4-1-signature-v3.lean).
  SHA-256 a3673fc1b0aad4d103e1ede08d803d627c4de2035c63b18dbc2ea7a206f9540f.
  Lean 4.33.0, lake env lean on that file, exit 0; no proof assertions.
- Independent prospective source acceptance: source-topology reviewer
  accepted [revision 2](chewi-exercise-4-1-source-topology-v2.md),
  packet SHA-256 24836c3fe2d07d00096c437bdb78adfa836162c69ca305717a9b443c172af70d;
  signature v2 SHA-256 e63d11ff7cfbeda444a69fde27726fe40a9c3f140dfddaacb45cc80bc38dd513.
  V2's standalone compile failed on a missing Mathlib gradient import.
  V3 restores that import and inlines the type-only aliases in the checked
  proposition; it makes no change to mathematical objects, binder scopes,
  endpoint values, or conclusions. V2's hashes and failed check are retained.

## Binders and meaning

- TYPING: d, N are natural numbers; D=d+1 is the dimension. EuclideanSpace
  uses the real finite-dimensional inner product and its Euclidean norm.
  Fin indices are zero-based; adjacent indices embed through castSucc/succ.
- SOURCE: 1 ≤ N, 2N+1 ≤ D, β>0, arbitrary prescribed start x₀.
- SOURCE (under the conclusion's universal trajectory): sequence of points
  in the same space, actual initial equality, affine-span rule of Def. 4.3
  for the true gradients. No algorithm independence/linearity assumptions
  beyond that model; no claim about unrestricted randomized oracle access.
- No STANDING, RULED or EXCESS premises. Convexity, C¹, upper model,
  minimizer, support propagation, and tail bound are proved, not given.
- The objective and affine minimizer are literal let-values and fixed before
  all trajectory quantifiers; no opaque project-owned definitions occur
  in the exported type. The first endpoint of the padded quadratic is one,
  the right endpoint is zero. WithLp.toLp 2 is a coordinate-preserving
  Euclidean wrapper. The chosen minimizer's centered kth coordinate is
  1−k/(D+1) in source indexing.
- Constant 1/8 is an explicit valid universal realization of the exercise,
  not a claim of source-attribution or sharpness. The value-gap conclusion
  of Thm. 4.4, Thm. 4.5, and Exercise 4.2 are excluded.

The unchanged proof-direction prototype is feasibility evidence only.
The new production candidate must match the exact sealed signature and
receive its own compile, blind decode and source review before publication.
