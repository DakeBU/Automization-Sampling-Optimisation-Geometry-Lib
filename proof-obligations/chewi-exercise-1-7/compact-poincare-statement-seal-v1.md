# Statement Seal v1: compact-test LSI implies compact-test PI

Frozen before proof implementation. Exact fully quantified Lean type:
[signature probe](compact-poincare-signature-v1.lean.txt), raw SHA256
`990a3f14e8a29cb440ca5b7751175ef05416fbd6cf2437a90c08f806a108b476`.
`lake env lean` elaborated that proposition as `Prop` on Lean 4.33.0; the
probe is not proof evidence. Target:
`AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare.poincare_of_compact_logSobolev`.

- Source: Chewi, *Log-Concave Sampling*, August 20, 2026, PDF SHA256
  `8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`;
  Exercise 1.7 and (1.E.1), printed 43/PDF 55, with the compact Langevin
  specialization in §2.1.1, printed 48–49/PDF 60–61. Original restatement;
  not a quotation or a claim of the full abstract exercise.
- Source binders: one probability measure, one fixed positive real constant
  `C`, compact smooth function LSI with coefficient `2*C` for all tests,
  and any compact smooth observable `g`. The conclusion is its actual
  centered second moment bounded by `C` times genuine gradient energy.
- Carrier adapters: a finite-dimensional complete real inner-product space
  with Borel measurable structure instead of chosen coordinates on ℝᵈ.
  `ContDiff ℝ ∞` is smoothness; `HasCompactSupport` is compact topological
  support. Gradient is Mathlib's Riesz gradient. Entropy and variance here
  are literal real integrals, not certificate predicates.
- Produce internally: boundedness, exact centering, unchanged derivative,
  compact derivative support, genuine square-root analytic domains,
  mass one, entropy-compensator cancellation, both scaled limits and the
  closed-order step. None is an extra premise. A.e. density equality does
  not identify derivatives of representatives.
- Reuse search: the pinned Mathlib and owned Lean inventories did not expose
  the exact compact-test LSI-to-PI consumer. Use the verified cutoff extension,
  compact-gradient square-root data, bounded-density entropy and square-root
  energy limits without duplicating any of their proofs.
- Source coverage: use the accepted independent source-only v2 review and
  topology in this directory. The compact application/linearization/uncentering
  segment is the implementation target; the same-witness law, canonical RN
  derivative, abstract reversible form-domain, wider core closure, optimal
  constant passage and numbered-exercise admission are separate.
- Process constraint: the measure-role guard
  `ASTIS-PM-QUADRATIC-TILT-MEASURE-ROLES` was consulted. Here the two limits
  use the same probability base and actual square-root perturbation, not a
  tilted-expectation energy imported from a different measure.
