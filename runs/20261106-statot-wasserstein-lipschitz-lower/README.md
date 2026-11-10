# Statistical Optimal Transport Exercise 6: lower comparison

The generic statement proves the two one-sided comparisons in the lower
hint. It uses the actual linear-cost Kantorovich infimum, the existing
quadratic Wasserstein distance, and only the real probability/finite
second-moment domain and a 1-Lipschitz test. It makes no duality or
optimizer claim. The clipped ENNReal encoding is equivalent to the real
one-sided comparison with a nonnegative right-hand side.

`lake build Tests.Shared.WassersteinLipschitzLower` passed on Lean 4.33.0.
The test uses the concrete Gaussian laws: it discharges probability and
moment conditions, computes their two means, and combines the lower
comparison with the existing exact-cost witness. This proves the full
two-sided inequality as an anonymous focused example, not a new named
production declaration for the entire exercise.

See the byte-pinned [receipt](focused-receipt.json), the successful
[compiler output](focused-build.txt), and the separate
[source seal](../../proof-obligations/statot-exercise-1-6/lower-comparison-seal-v1.md).
The exercise's original attributed prompt, solution and provisional rubric
are a [Bench intake draft](../../proof-obligations/statot-exercise-1-6/bench-intake-v1.md).
The Cell, semantic audit and advance ledger track independent review and
integration; this receipt does not establish either, or editorial admission.
