# Conversion window: arbitrary-$P_2$ displacement interpolation

## Source boundary

Primary source: Sinho Chewi, Jonathan Niles-Weed and Philippe Rigollet, *Statistical Optimal Transport*, Theorem 7.6, printed pp. 209--210 / PDF pp. 215--216, pinned SHA-256 `639ff16e79f4a32ade9c0595b0ed1d95490eb7e402949168895b6a6194a9c02f`.

For $\mu_0,\mu_1\in P_2(\mathbb R^d)$ and an optimal quadratic plan $\gamma\in\Gamma(\mu_0,\mu_1)$, define $\pi_t(x,y)=(1-t)x+ty$ and $\mu_t=(\pi_t)_\#\gamma$. The bounded target is

\begin{align*}
W_2(\mu_s,\mu_t)=(t-s)W_2(\mu_0,\mu_1),\qquad 0\le s\le t\le1.
\end{align*}

The source also proves optimal-plan existence and the geodesic-space conclusion. Those are not part of this packet.

Chewi's *Log-Concave Sampling* Theorem 1.3.23 is stated for $\mu_0,\mu_1\in P_{2,\mathrm{ac}}(\mathbb R^d)$. Removing absolute continuity is therefore a genuine generalization relative to that source, but it is the exact endpoint domain of *Statistical Optimal Transport* Theorem 7.6. The existing ASTIS $P_{2,\mathrm{ac}}$ theorem remains under its old name as a corollary.

## Symbol map

| Source | Lean |
|---|---|
| $\mathbb R^d$ | `E` with the existing finite-dimensional real inner-product Borel assumptions |
| $\mu_0,\mu_1\in P_2$ | endpoint `Measure E`, `IsProbabilityMeasure` instances, and `Integrable (fun x => ‖x‖ ^ 2)` |
| $\gamma\in\Gamma(\mu_0,\mu_1)$ optimal | `DisplacementInterpolation.IsQuadraticOptimalCoupling γ μ₀ μ₁` |
| $\pi_t$ | the affine point map inside `displacementInterpolation` |
| $\mu_t=(\pi_t)_\#\gamma$ | `DisplacementInterpolation.displacementInterpolation γ t` |
| $W_2$ | `WassersteinSpace.wassersteinDistance`, valued in `ℝ≥0∞` |

## Proof DAG

1. `DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_le` supplies the sharp upper bound from the canonical two-time coupling.
2. `DisplacementInterpolation.displacementInterpolation_zero` and `displacementInterpolation_one` identify the endpoint segments.
3. `WassersteinTriangleExact.wassersteinDistance_triangle` compares the endpoint distance with the three ordered pieces.
4. `DisplacementInterpolationConstantSpeed.interpolation_coefficients_sum_one` proves $s+(t-s)+(1-t)=1$ in `ℝ≥0∞`.
5. `WassersteinFiniteSecondMoment.wassersteinDistance_lt_top_of_integrable_norm_sq` proves the endpoint distance is finite from probability normalization and the two explicit second-moment hypotheses.
6. `ENNReal.add_le_add_iff_left` and `ENNReal.add_le_add_iff_right` cancel only the now-finite prefix and suffix; `le_antisymm` closes the equality.

## Truth and regularity audit

- Measurability of every affine point map is supplied by the existing Borel real-vector-space API.
- Probability of $\gamma$ follows from its probability first marginal; probability of each $\mu_t$ follows by measurable pushforward.
- Integrability is required only for the endpoint squared norms and is used through the existing finite-$W_2$ lemma.
- The proof stays in `ℝ≥0∞`; it does not cancel an infinite quantity or use a totalized real conversion.
- Optimal-coupling existence, uniqueness, an optimal map, absolute continuity, path continuity, continuity equations, and Benamou--Brenier are not conclusions.

## Local state

- Frontier Cell: `ASTIS-SHARED-displacement-interpolation-p2`.
- Canonical declaration: `AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_eq_of_le_of_integrable_norm_sq`.
- Compatibility corollary: the unchanged declaration `AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_eq_of_le`; the focused test independently derives its signature from the new arbitrary-$P_2$ theorem.
- Focused test: `Tests/DisplacementInterpolationConstantSpeed.lean`.
- Initial focused build: passed on the implementation worktree with Lean 4.33.0 and two threads; independent review and publication admission remain pending until the candidate is frozen.
