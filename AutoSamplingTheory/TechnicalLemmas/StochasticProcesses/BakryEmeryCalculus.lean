import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp

/-!
# The algebraic Bakry--Émery interpolation bound

For a linear generator, the definition of the iterated carré du champ gives

`2 Γ₂(f) = L Γ(f) - 2 Γ(f, Lf)`.

Combining this identity with `CD(κ, ∞)` supplies the lower derivative bound
used in the standard backward semigroup interpolation.  This file proves that
algebraic implication without assuming a concrete semigroup or its derivative
formula.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses

open CarreDuChamp

variable {X : Type*}

/-- The Bakry--Émery curvature condition gives the exact lower bound for the
generator expression appearing in backward gradient interpolation. -/
theorem interpolationDerivative_lower_bound_of_bakryEmery
    (generator : (X → ℝ) →ₗ[ℝ] (X → ℝ))
    {alpha : ℝ} (hBE : SatisfiesBakryEmery generator alpha)
    (f : X → ℝ) (x : X) :
    2 * alpha * carreDuChamp generator f f x ≤
      generator (carreDuChamp generator f f) x -
        2 * carreDuChamp generator f (generator f) x := by
  have hcurvature := hBE.2 f x
  rw [iteratedCarreDuChamp] at hcurvature
  nlinarith

end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
