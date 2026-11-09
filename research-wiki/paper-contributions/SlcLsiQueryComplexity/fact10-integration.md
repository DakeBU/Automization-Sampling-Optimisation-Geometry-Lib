# Gaussian odd-load comparison: analytic ingredient, not the paper theorem

## One proof, several reading contexts

The canonical declaration is
`AutoSamplingTheory.TechnicalLemmas.Probability.GaussianOddLoad.gaussian_odd_load_bound`.
Its owner is the shared Probability technical layer. The paper reader links it
from the Section 6.2 Fact 10 calculation; Lower Bounds and SampleWiki link that
same paper reader. Existing chapter-extension projections provide background
reading contexts, not copies of the theorem or additional formal dependencies.
It is not a Discrete Sampling result, an optimisation lower-bound reduction, or
an already certified Functor transport.

For measurable odd `U` with `|U(y)| ≤ β|y|`, `a∈[0,1]`, and Gaussian variance
`v≥0`, the theorem proves both exponential integrability and
`∫ exp(-a U(y)) dN(0,v) ≤ exp(β²v/2)`. It does not assume the desired moment or
integrability. Variance zero and both gate endpoints are retained.

The reader unfolds three mathematical moves before optional Lean details:
integrable Gaussian envelope → symmetry/cosh → exact Gaussian MGF comparison.
This compresses the argument without hiding the hypotheses permitting the
integral manipulations. Exact Lean and step-by-step explanations remain beside
the mathematical statement/proof, not in an unrelated final appendix.

## Exact acceptance boundary

The candidate `3890056ea8529ea9de8aaaa46a6f67cba0b7c0d6` passed focused compilation
and endpoint/exact-signature tests under Lean 4.33.0 and pinned Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`. See `fact10-compile-evidence.json`.
Independent compiler/semantic evidence, when admitted, lives in its own reports
and the existing Cell/SAU state; this prose does not create review or merge status.
Whole-library integration, actual deployment and post-merge purification remain
separate from the focused proof.

Only `integrability` and `symmetry-cosh-bound` are bound in the publication item.
`literal-load-adapter` remains open. The generic theorem is not advertised as
the complete source Fact 10 in context, Lemma 6.2, Theorem 7 or a query lower bound.

## Next dependency-ready route

1. Define the actual source truncated load and derive its measurability, oddness
   and linear bound from the source's function and positive scaling parameters.
   Apply the existing comparison, without adding those properties as public
   assumptions on a final source theorem. Reuse a pre-existing load definition
   if another collaborator has supplied one.
2. Express the actual independent Gaussian coefficients and measurable gates.
   Establish the conditional Gaussian law, freeze the appropriate gate, justify
   integration/factorization, and then iterate the level-wise estimate. A
   deterministic scalar gate is not automatically a random conditional gate.
3. Derive the first-moment bound for the actual normalizer in Lemma 6.2; retain
   the separate second-moment and bad-mass estimates needed by Theorem 7.
4. Join the actual positive normalizer/mass estimates to the already proved
   deterministic Fact 12. Only then is the normalization route closed. Oracle
   transcript, hard-family admissibility, warm-start information and expected
   query-cost conversions remain additional main-theorem obligations.

Recheck active ownership before each new packet. This lane neither duplicates
the four-paper SAUs nor transfers Huanjian/Andy/Ji/Bench responsibilities.
