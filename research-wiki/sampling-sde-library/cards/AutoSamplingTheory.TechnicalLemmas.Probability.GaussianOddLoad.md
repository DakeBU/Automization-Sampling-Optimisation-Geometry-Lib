# AutoSamplingTheory.TechnicalLemmas.Probability.GaussianOddLoad

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/GaussianOddLoad.lean`
- Layer: generic probability technical lemma; one confirmed paper consumer.
- Declaration: `gaussian_odd_load_bound` in this module's namespace.
- Source: Zhou–Suzuki arXiv:2611.05813v1 §6.2 Fact 10, generalized analytic ingredient.
- Canonical evidence: Cell `ASTIS-SW-SLC-LSI-gaussian-odd-load`, audit
  `ASTIS-RT-20261109-SlcLsiGaussianOddLoad`, and the Registry entry
  `probability.gaussian-odd-load`; this card is not another status registry.

## Reuse contract

For Borel measurable odd `U : ℝ → ℝ`, a pointwise bound `|U y| ≤ β * |y|`,
`a ∈ [0,1]`, and variance `v : ℝ≥0`, obtain actual integrability of `exp(-a U)`
and its `gaussianReal 0 v` integral bound `exp(β²v/2)`. No supplied exponential
integrability or strict positivity of variance is needed. `β≥0` is derived.

The proof uses Mathlib Gaussian symmetry, exponential integrability and MGF,
Bochner integral transport/linearity, and monotonicity of real cosh in absolute
value. There are no ASTIS-owned theorem parents and no duplicated Gaussian MGF.
The three-step reader is authored once in
`website/content/declaration_lessons/slc-lsi-gaussian-odd-load.json`.

## Consumer boundary

The actual truncated `U_i` and its positive scaling parameters must produce the
structural hypotheses before applying this theorem. A deterministic scalar gate
cannot be treated as an arbitrary dependent random gate. Conditional Gaussian
laws, freezing, independence, product iteration and Tonelli remain separate.
This is not Lemma 6.2, Theorem 7 or any query lower-bound theorem.
