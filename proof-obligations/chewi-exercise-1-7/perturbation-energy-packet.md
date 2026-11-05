# Explicit square-root perturbation energy — Statement Seal v1

SAU `ASTIS-SA-20261105-BoundedPerturbationEnergy`; shared cell
`ASTIS-SHARED-bounded-perturbation-energy`. One writer: `agent-task:/root`.
This continues the same Bench Goal and the accepted source topology v2.

## Source and precise scope

Chewi, *Log-Concave Sampling*, August20 2026, Exercise1.7/(1.E.1),
printed43/PDF55, and the function-form LSI on printed48/PDF60.
The pinned PDF SHA256 is
`8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`.
This is an original proof of an omitted energy step, not copied textbook prose.

For genuinely differentiable real f on a real normed space, an a.e. uniform
bound and integrable actual squared derivative norm imply eventual integrability
of the explicit square-root perturbation's derivative energy, and

\[
\lim_{\varepsilon\to0,\ \varepsilon\ne0}
\frac{\int\|D\sqrt{1+\varepsilon f}(x)\|^2\,d\mu(x)}{\varepsilon^2}
=\frac14\int\|Df(x)\|^2\,d\mu(x).
\]

Here the derivative is the genuine derivative of the displayed function where
its argument is positive. No RN representative is differentiated by an a.e.
replacement. No centering, probability, finite total measure or LSI hypothesis
is needed for this analytic statement. It does not assert canonical Fisher
information or normalization of the affine perturbation.

## Frozen public signature

Owner: `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/BoundedPerturbationEnergy.lean`.
Namespace: `AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BoundedPerturbationEnergy`.
One public declaration, no private-helper leaf credit:

```lean
theorem eventually_integrable_and_tendsto_sqrt_perturbation_energy
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [MeasurableSpace E] [OpensMeasurableSpace E]
    (mu : Measure E) (f : E → ℝ) (hf : Differentiable ℝ f)
    {M : ℝ} (hbound : ∀ᵐ x ∂mu, |f x| ≤ M)
    (henergy : Integrable (fun x => ‖fderiv ℝ f x‖ ^ 2) mu) :
    (∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      Integrable (fun x => ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2) mu) ∧
    Tendsto (fun e : ℝ =>
      (∫ x, ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2 ∂mu) / e ^ 2)
      (𝓝[≠] (0 : ℝ)) (𝓝 ((∫ x, ‖fderiv ℝ f x‖ ^ 2 ∂mu) / 4))
```

The measurable-topology class makes continuous real f measurable. The actual
energy's integrability provides its own strong measurability. We do not assume
measurability or convergence of the perturbed derivatives as new certificates.
The uniform bound is a.e.; eventual global smoothness is NOT a conclusion.

## Reuse and proof route

Search covered the shared RelativeFisher/CanonicalRelativeFisher/
CanonicalDirichletFisher APIs, GaussianSqrtDensityDomain, the existing bounded
KL integral proof and fixed Mathlib sqrt/dominated-convergence APIs.
The Gaussian exponential-density domain is not an affine-density result;
canonical RN/score contracts cannot supply the missing genuine derivative.

Minimal starting imports: Mathlib Analysis.SpecialFunctions.Sqrt and
MeasureTheory.Integral.DominatedConvergence, plus only the tactics actually used.
Reuse `HasFDerivAt.sqrt`, ordinary derivative algebra, norm-smul/square-root
identities, and `tendsto_integral_filter_of_dominated_convergence`.

1. Choose the ordinary two-sided neighborhood |e|*|M| < 1/2, with no division by M.
2. On the fixed full-measure bounded-test set, derive 1+e*f >= 1/2.
3. Use actual derivative rules to identify energy as e²*H/[4(1+e*f)], H=||Df||².
4. Produce measurable normalized energies and a fixed integrable H dominator.
5. Derive eventual integrability of the actual energy, including e=0.
6. Pass the normalized energy through the integral and cancel e² only on the
   punctured filter. The value of a totalized quotient at zero is not its limit.

## Actual consumer and remaining obligations

This is the explicit square-root energy side of the accepted Exercise1.7
LSI-to-PI route. In the Euclidean consumer, Riesz isometry (`toDual_gradient`)
identifies the derivative norm with the gradient norm. The consumer must still
derive energy integrability from its actual smooth compact-gradient class.
The generic henergy binder is not an added hypothesis on the final exercise.
The eventual-integrability conclusion serves the actual finite-epsilon
LSI-test/domain route; the limit conclusion serves centered-test PI. These are
two mathematical consumers in the same exercise, not two independent exercises
or completed source results. Both actual integrations are still planned.

The existing law and KL nodes are sibling ingredients, not redundant mandatory
imports of this generic energy lemma. Actual LSI admissibility of the noncompact
square-root test, entropy/cutoff limits, uncentering and PI/form-domain closure
stay separate. A.e. positivity alone proves none of those. No old paper/cycle,
whole exercise, new admitted Bench QA or new Functor transport is closed here.

Focused module/signature/finite-energy tests precede independent anonymous
decoding and anti-anchored source/code/exposition review. Root imports, Registry
and graph truth stay untouched until the serialized stabilization lane.
