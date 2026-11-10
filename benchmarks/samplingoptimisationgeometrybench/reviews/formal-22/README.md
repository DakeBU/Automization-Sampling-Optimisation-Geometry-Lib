# Formal round 22: horizon-dependent value-gap sharpness

`sogb-047` is a selected component of [Chewi, *Lectures on Optimization*,
v1, Exercise 3.3 (p. 23)](https://arxiv.org/pdf/2605.07006v1#page=23).
It tests the order of the [convex specialization of Theorem 3.4 (p. 21)](https://arxiv.org/pdf/2605.07006v1#page=21)
at step \(1/\beta\), unit initial distance and positive horizon. Printed and
PDF page numbers agree. The witness, lower constant, and proof are original
exposition; the exercise does not state this lower constant.

- [Anonymous Lean input](packets/anonymous-input.json) and [independent
  reconstruction](decoder.json) pin all seven semantic slots.
- [Source review](source-review.json) checked the proof, fixed imports,
  Lean 4.33.0 reference and existing shared tests. It required one
  scoring-only repair: a valid energy or norm proof of the exact value
  need not derive the signed iterate recurrence.
- The [exact proposal](packets/repair-input.json) and [independent repair
  verdict](repair-review.json) allow any valid exact-gap proof for the
  specified trajectory. Only the second criterion changes; the mathematical
  statement, reference, hypotheses, family, L3/L3 levels, and proof steps stay fixed.

The Lean result certifies the finite-horizon quadratic, admissibility,
minimization and gap. The comparison with the source upper rate and the
little-o argument for each fixed scalar quadratic are explanatory, not new
Lean conclusions. This is the same public-dev Exercise 3.3 family as
`sogb-046` and linked to the existing compiled-body slice `sogb-g010`.
It does not complete the numbered exercise, prove an oracle lower bound,
claim an optimal constant or provide a measured model result.
