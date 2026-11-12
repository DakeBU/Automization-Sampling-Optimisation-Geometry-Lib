import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp
import Mathlib.Tactic.Ring

/-!
# Algebraic reconstruction from the carré du champ

Chewi Definition 1.2.12 defines

`Γ(f,g) = 1/2 (L(fg) - f Lg - g Lf)`.

Many later diffusion calculations, including the proof of Theorem 8.3.1, use
the same identity in the solved-for-product form

`L(fg) = f Lg + g Lf + 2 Γ(f,g)`.

This file gives that rearrangement one canonical Lean name.  It assumes no
positivity, diffusion chain rule, invariant measure, reversibility, or
observable-domain closure beyond the total algebraic `carreDuChamp` definition.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace CarreDuChampAlgebra

noncomputable section

open CarreDuChamp

/-- Function-valued product reconstruction from the definition of the carré du
champ:

`L(fg) = f Lg + g Lf + 2 Γ(f,g)`.

This is purely algebraic and does not assert that `L` is a diffusion
generator. -/
theorem generator_mul_eq
    {X : Type*}
    (generator : (X → ℝ) →ₗ[ℝ] (X → ℝ))
    (f g : X → ℝ) :
    generator (f * g) =
      f * generator g + g * generator f +
        (2 : ℝ) • carreDuChamp generator f g := by
  funext x
  simp only [carreDuChamp, Pi.add_apply, Pi.mul_apply, Pi.smul_apply]
  ring

/-- Pointwise form of `generator_mul_eq`. -/
theorem generator_mul_apply_eq
    {X : Type*}
    (generator : (X → ℝ) →ₗ[ℝ] (X → ℝ))
    (f g : X → ℝ) (x : X) :
    generator (f * g) x =
      f x * generator g x + g x * generator f x +
        2 * carreDuChamp generator f g x := by
  exact congrFun (generator_mul_eq generator f g) x

end

end CarreDuChampAlgebra
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
