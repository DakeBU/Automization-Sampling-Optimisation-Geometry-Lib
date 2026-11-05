# Statement Seal v1: Poincaré on the compact-gradient graph closure

Exact [fully quantified type](compact-gradient-closure-signature-v1.lean.txt)
raw SHA256 `2e0ba00a93179b965eba8122bbbac1034de3cfe3e99ddb91bf397ff91253b709`.
The complete proposition elaborated on pinned Lean 4.33.0 before implementation.
Target: `AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactGradientPoincareClosure.poincare_of_compact_logSobolev_on_gradient_closure`.

Source: Chewi, *Log-Concave Sampling*, August 20, 2026, PDF SHA256
`8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`.
Exercise 1.7, printed 43/PDF 55, and §2.1.1, printed 48–49/PDF 60–61.
This is an original ASTIS bridge for the omitted density step of the
compact Euclidean route, not a printed theorem or the complete exercise.
The independently checked source-only v2 topology remains unchanged.

The only functional premise is the verified compact packet's given compact
smooth function LSI with coefficient `2*C` on a probability measure, fixed
`C>0`, and the same finite-dimensional real Hilbert/Borel carrier. The target
quantifies over actual pairs of scalar and vector L² classes in the closure
of the compact smooth gradient pairs. Both equalities in the original graph
are with respect to the same μ, and closure is in the joint L² norm topology.
No unique or closable gradient operator is assumed or asserted for arbitrary μ.

The centered variance of the scalar class is Mathlib's real variance.
Here it is genuinely finite because the class belongs to L²; no infinite-
variance fallback is used. The right side is the squared norm of the vector
component, not a separately chosen energy or a claim of pointwise differentiability
of the limiting scalar. This is the pairwise bound with the same C.

Reuse search: the existing compact LSI-to-PI theorem supplies the bound on
each graph pair. Mathlib has variance decomposition, L² inner products and
closed order; no exact compact-LSI to joint closure theorem was found in the
pinned sources or Samplinglib. The original graph in `WeightedGradient` has
the same representative predicate; the test can identify its graph closure
and consume `WeightedC1GradientDomain.c1_in_closed_gradient` without replacing
the existing Gibbs operator. Do not import its two-curvature PI route as a
premise or infer abstract semigroup domains from this closed gradient graph.
The measure-role process guard was consulted: the same μ is used in the
compact estimate, both L² spaces, variance and mean. Whole-exercise,
optimal-constant, Bench and deployment claims remain separate.
