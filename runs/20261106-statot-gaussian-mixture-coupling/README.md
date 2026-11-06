# Statistical Optimal Transport, Chapter 1 Exercise 6 — upper witness

The [source seal](../../proof-obligations/statot-exercise-1-6/upper-coupling-seal-v1.md) and its
[independent pre-proof topology review](../../proof-obligations/statot-exercise-1-6/upper-coupling-source-review-v1.md)
pin the scope to the upper hint. The source supplies neither the plan nor its
cost. The new theorem builds an actual joint measure as three affine
pushforwards of the same standard Gaussian. Their weights are a left
diagonal quarter, a moving quarter, and a right diagonal half. Projecting
gives exactly the two given mixtures; the only nonzero branch costs
`(2m)²`, so the total cost is `m²`.

The [focused receipt](focused-receipt.json) records the successful 3107-job
build and the real squared Wasserstein upper-bound consumer. The first
attempts exposed explicit affine projection elaboration and ENNReal
rational-normalization issues. They were fixed by supplying the measurable
coordinate maps and computing the finite coefficients in NNReal before
embedding into ENNReal, without changing the sealed proposition.

The lower argument still needs a bound valid for every coupling, not for this
one witness. The actual finite moments and expectation comparison for
unbounded 1-Lipschitz tests, followed by the source's W₁/W₂ comparison,
are separate. No optimality, full exercise, aligned task, Registry credit,
or model measurement is asserted. Semantic round trip and stabilization are
separate from the focused build. The [independent source review](source-review.result.json)
accepted the actual upper witness after elaboration, not the full exercise.
“Left” and “right” refer to the source's positive-`m` regime; the exact formula
uses the center labels `−m` and `m` even when they reverse order or coincide.
Independent exact-commit VERIFIED admission is still separate.

## Next edge — lower comparison, not yet compiled

Use actual first moments (available from Gaussian second moments) to make
each 1-Lipschitz test integrable by its linear growth. For an arbitrary
coupling, the two marginal equalities turn the expectation difference into
the integral of `f(x) − f(y)`; the pointwise upper bound is `|x−y|`.
Pass this bound to the infimum of the linear cost. Separately apply
Cauchy–Schwarz on each probability coupling and pass to the quadratic
infimum for `W₁ ≤ W₂`; no optimal-plan existence is needed. Finally
`f(x) = −x` has the required sign: the two means are `0` and `m/2`,
so the resulting lower constant is `1/2`. The current bounded-feature
transport interface does not justify this unbounded test.
