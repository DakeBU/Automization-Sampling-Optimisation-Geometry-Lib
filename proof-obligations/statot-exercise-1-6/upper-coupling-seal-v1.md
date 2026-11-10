# Statement seal candidate — Statistical Optimal Transport, Exercise 6 upper-bound witness

Source: Sinho Chewi, Jonathan Niles-Weed and Philippe Rigollet,
*Statistical Optimal Transport*, July 2024 preface, 290-page public PDF,
[Chapter 1 §1.8, Exercise 6, printed p. 44 / PDF p. 50](https://chewisinho.github.io/st_flour.pdf#page=50),
SHA-256 `639ff16e79f4a32ade9c0595b0ed1d95490eb7e402949168895b6a6194a9c02f`. Original mathematical restatement;
do not redistribute the page or source prose in Bench data.

## Exact interface v1

`AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureCoupling.exists_gaussian_mixture_coupling_cost`, pinned Lean 4.33.0 / project manifest.
The [signature probe](upper-coupling-signature-v1.lean.txt) contains the exact
proposition. For real `m`, let `Gₐ = N(a,1)`,
`μ = G₋ₘ/2 + Gₘ/2` and `ν = G₋ₘ/4 + 3Gₘ/4`.
There is a coupling `γ` with these exact marginals and squared cost
`∫(x−y)² dγ = m²`. The cost is the owned extended-nonnegative
quadratic cost, with right-hand side `ENNReal.ofReal (m ^ 2)`.

- `m : ℝ`: source parameter/carrier. The source asks for `m>0`; the witness
  gives the squared cost `m²` for every real `m`, including `m=0`.
  The original upper inequality uses the positive specialization.
- The marginals are literal combinations of actual Mathlib Gaussian measures,
  not law-valued inputs or assumptions. Variance one and all weights are fixed.
- `Transport.IsCoupling` unfolds to exactly the two pushforward identities.
  `quadraticCost` unfolds to the nonnegative squared Euclidean distance.
- There are no auxiliary binder hypotheses. Construct the coupling and all
  required measurability, and compute its finite cost inside the proof. The
  construction is not assumed optimal; no lower bound or exact value of
  W₂ is claimed. The general lower hint uses a different all-coupling edge.

## Source-only proof graph (draft for independent coverage review)

1. **NODE S0** — §1.8 Exercise 6 specifies the two weighted unit-variance
   Gaussian laws with positive `m`.
   **NODE T** — The requested two-sided comparison, uniform in `m>0`.
2. **NODE U** — Upper hint requires a feasible coupling. The general
   definition of W₂ consumes the candidate cost as an upper bound;
   no existence of a minimizing coupling is needed.
3. **SOURCE_GAP U1** — The hint does not give the coupling, its marginals
   or its finite cost. This is the only region closed by the sealed witness.
4. **NODE L** — Lower hint asks for the expectation comparison for
   1-Lipschitz tests via W₁, then W₁ ≤ W₂.
5. **SOURCE_GAP L1** — The source does not specify the test, prove its
   integrability or prove the two inequalities. These remain downstream.
6. **EXCLUDED** — Exercise 5, Exercise 7, and the adjacent preceding
   centering/optimality questions have no stated use in Exercise 6.

Source edges: S0 supplies the two laws to U1 and L1; U1 supplies the feasible
finite-cost plan used in U; L1 supplies the expectations and comparisons in L;
U and L jointly supply the two-sided comparison T. The upper-hint
implementation is not printed. Do not ascribe an authored coupling to the
source or infer a Lean edge from these records.
