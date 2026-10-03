import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BakryEmeryInterpolation
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BakryEmeryCalculus

/-!
# Abstract Bakry--Émery gradient contraction

This module joins the three reusable parts of the backward interpolation
argument: the curvature inequality, positivity of the evolution operator, and
the scalar endpoint comparison.  A concrete Markov semigroup still has to
provide the interpolation derivative identity and its analytic regularity.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses

open Filter Set
open CarreDuChamp
open FunctionalInequalities.SemigroupDecay

noncomputable section

variable {X : Type*}

/-- A positive linear evolution operator and the standard backward
interpolation derivative identity turn `CD(alpha, infinity)` into pointwise
gradient contraction.

The theorem does not construct the evolution, prove its positivity, or derive
the displayed derivative identity.  Those are the remaining analytic inputs
for a concrete semigroup. -/
theorem backwardInterpolation_contraction_of_expandedBakryEmery
    (generator : (X → ℝ) →ₗ[ℝ] (X → ℝ))
    {alpha : ℝ} (halpha : 0 < alpha)
    (hcurvature : ∀ (g : X → ℝ) (y : X),
      alpha * carreDuChamp generator g g y ≤
        (2 : ℝ)⁻¹ *
          (generator (carreDuChamp generator g g) y -
            carreDuChamp generator g (generator g) y -
            carreDuChamp generator g (generator g) y))
    (evolution : ℝ → (X → ℝ) →ₗ[ℝ] (X → ℝ))
    (orbit : ℝ → X → ℝ) (x : X)
    (hpositive : ∀ u : ℝ, ∀ {f g : X → ℝ},
      (∀ y, f y ≤ g y) → ∀ z, evolution u f z ≤ evolution u g z)
    (hcontinuous : Continuous (fun u =>
      evolution u (carreDuChamp generator (orbit u) (orbit u)) x))
    (hderiv : ∀ u : ℝ,
      HasDerivWithinAt
        (fun v => evolution v
          (carreDuChamp generator (orbit v) (orbit v)) x)
        (evolution u
          (generator (carreDuChamp generator (orbit u) (orbit u)) -
            (2 : ℝ) • carreDuChamp generator (orbit u) (generator (orbit u))) x)
        (Ici u) u)
    {s t : ℝ} (hst : s ≤ t) :
    evolution s (carreDuChamp generator (orbit s) (orbit s)) x ≤
      evolution t (carreDuChamp generator (orbit t) (orbit t)) x *
        Real.exp (-(2 * alpha) * (t - s)) := by
  apply backward_interpolation_contraction_of_growth hcontinuous hderiv ?_ hst
  intro u
  let gamma : X → ℝ := carreDuChamp generator (orbit u) (orbit u)
  let mixed : X → ℝ :=
    carreDuChamp generator (orbit u) (generator (orbit u))
  have hpointwise : ∀ y,
      ((2 * alpha) • gamma) y ≤
        (generator gamma - (2 : ℝ) • mixed) y := by
    intro y
    simpa [gamma, mixed] using
      interpolationDerivative_lower_bound_of_expandedBakryEmery
        generator halpha hcurvature (orbit u) y
  have hmapped := hpositive u hpointwise x
  simpa [gamma, mixed] using hmapped

/-- Convenience form of the abstract contraction theorem using the packaged
`SatisfiesBakryEmery` predicate. -/
theorem backwardInterpolation_contraction_of_bakryEmery
    (generator : (X → ℝ) →ₗ[ℝ] (X → ℝ))
    {alpha : ℝ} (hBE : SatisfiesBakryEmery generator alpha)
    (evolution : ℝ → (X → ℝ) →ₗ[ℝ] (X → ℝ))
    (orbit : ℝ → X → ℝ) (x : X)
    (hpositive : ∀ u : ℝ, ∀ {f g : X → ℝ},
      (∀ y, f y ≤ g y) → ∀ z, evolution u f z ≤ evolution u g z)
    (hcontinuous : Continuous (fun u =>
      evolution u (carreDuChamp generator (orbit u) (orbit u)) x))
    (hderiv : ∀ u : ℝ,
      HasDerivWithinAt
        (fun v => evolution v
          (carreDuChamp generator (orbit v) (orbit v)) x)
        (evolution u
          (generator (carreDuChamp generator (orbit u) (orbit u)) -
            (2 : ℝ) • carreDuChamp generator (orbit u) (generator (orbit u))) x)
        (Ici u) u)
    {s t : ℝ} (hst : s ≤ t) :
    evolution s (carreDuChamp generator (orbit s) (orbit s)) x ≤
      evolution t (carreDuChamp generator (orbit t) (orbit t)) x *
        Real.exp (-(2 * alpha) * (t - s)) := by
  apply backwardInterpolation_contraction_of_expandedBakryEmery
    generator hBE.1 ?_ evolution orbit x hpositive hcontinuous hderiv hst
  intro g y
  simpa only [iteratedCarreDuChamp] using hBE.2 g y

end

end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
