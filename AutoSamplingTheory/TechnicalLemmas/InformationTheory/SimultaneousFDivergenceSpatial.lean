import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.GradientAlgebra
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.SimultaneousFDivergenceGradient
import Mathlib.Tactic

/-!
# Source-shaped spatial identities for simultaneous f-divergence flow

Chewi Theorem 8.3.1 differentiates

`D_f(p || q) = ∫ q f(p / q)`

and, after inserting the two common Fokker--Planck equations, uses three
pointwise gradient identities.  Writing `rho = p / q`, these are

`grad (q rho) = rho grad q + q grad rho`,
`grad (f' ∘ rho) = f''(rho) grad rho`,
`grad(f(rho) - rho f'(rho)) = -rho f''(rho) grad rho`.

This file proves those identities from the reusable gradient product/chain
rules and assembles the exact pointwise pairing that remains after spatial
integration by parts.

The quotient identity `rho = p / q`, positivity of `q`, differentiability of
that quotient, the Fokker--Planck equations, integrability, and whole-space
integration by parts are deliberately **not** proved here.  They remain
separate analytic nodes in the underlying Lean graph.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace InformationTheory
namespace SimultaneousFDivergenceSpatial

open InnerProductSpace
open scoped RealInnerProductSpace

noncomputable section

/-- Gradient of the factorized numerator `p = q * rho`. -/
theorem HasGradientAt.factorizedNumerator
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {q rho : E → ℝ} {x gradQ gradRho : E}
    (hq : HasGradientAt q gradQ x)
    (hrho : HasGradientAt rho gradRho x) :
    HasGradientAt (fun y => q y * rho y)
      (rho x • gradQ + q x • gradRho) x := by
  simpa [add_comm] using
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.GradientAlgebra.HasGradientAt.mul
      hq hrho

/-- Chain rule for the spatial gradient of `f' ∘ rho`. -/
theorem HasGradientAt.fPrime_comp
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {rho : E → ℝ} {fPrime : ℝ → ℝ}
    {x gradRho : E} {fpp : ℝ}
    (hrho : HasGradientAt rho gradRho x)
    (hfPrime : HasDerivAt fPrime fpp (rho x)) :
    HasGradientAt (fun y => fPrime (rho y)) (fpp • gradRho) x :=
  AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.GradientAlgebra.HasGradientAt.comp_real
    hrho hfPrime

/-- One-dimensional derivative identity behind
`grad(f(rho) - rho f'(rho))`.

This theorem makes the cancellation of the two `f'` terms explicit rather
than hiding it in the later Hilbert-space algebra. -/
theorem hasDerivAt_f_sub_id_mul_fPrime
    {f fPrime : ℝ → ℝ} {r fpp : ℝ}
    (hf : HasDerivAt f (fPrime r) r)
    (hfPrime : HasDerivAt fPrime fpp r) :
    HasDerivAt (fun u => f u - u * fPrime u) (-r * fpp) r := by
  have hfun :
      (fun u : ℝ => f u - u * fPrime u) = f - id * fPrime := by
    funext u
    rfl
  have hsub :
      HasDerivAt (f - id * fPrime)
        (fPrime r - (1 * fPrime r + r * fpp)) r :=
    hf.sub ((hasDerivAt_id r).mul hfPrime)
  have hcoeff :
      fPrime r - (1 * fPrime r + r * fpp) = -r * fpp := by
    ring
  rw [hfun]
  simpa [hcoeff] using hsub

/-- Chain rule for the companion spatial gradient
`grad(f(rho) - rho f'(rho))`. -/
theorem HasGradientAt.f_sub_mul_fPrime_comp
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {rho : E → ℝ} {f fPrime : ℝ → ℝ}
    {x gradRho : E} {fpp : ℝ}
    (hrho : HasGradientAt rho gradRho x)
    (hf : HasDerivAt f (fPrime (rho x)) (rho x))
    (hfPrime : HasDerivAt fPrime fpp (rho x)) :
    HasGradientAt
      (fun y => f (rho y) - rho y * fPrime (rho y))
      ((-rho x * fpp) • gradRho) x := by
  exact
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.GradientAlgebra.HasGradientAt.comp_real
      hrho (hasDerivAt_f_sub_id_mul_fPrime hf hfPrime)

/-- Source-shaped pointwise spatial cancellation for Chewi Theorem 8.3.1.

Once `q`, `rho`, `f`, and `f'` satisfy the stated local differentiability
contracts, the two gradient pairings produced by common-diffusion integration
by parts reduce exactly to `q f''(rho) ||grad rho||^2`.

No PDE or integration theorem is used here. -/
theorem common_diffusion_pairing_source
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {q rho : E → ℝ} {f fPrime : ℝ → ℝ}
    {x gradQ gradRho : E} {fpp : ℝ}
    (hq : HasGradientAt q gradQ x)
    (hrho : HasGradientAt rho gradRho x)
    (hf : HasDerivAt f (fPrime (rho x)) (rho x))
    (hfPrime : HasDerivAt fPrime fpp (rho x)) :
    inner ℝ (gradient (fun y => fPrime (rho y)) x)
        (gradient (fun y => q y * rho y) x) +
      inner ℝ
        (gradient (fun y => f (rho y) - rho y * fPrime (rho y)) x)
        (gradient q x) =
      q x * fpp * ‖gradRho‖ ^ 2 := by
  rw [
    (HasGradientAt.fPrime_comp hrho hfPrime).gradient,
    (HasGradientAt.factorizedNumerator hq hrho).gradient,
    (HasGradientAt.f_sub_mul_fPrime_comp hrho hf hfPrime).gradient,
    hq.gradient
  ]
  exact SimultaneousFDivergenceGradient.common_diffusion_pairing_eq
    (q x) (rho x) fpp gradQ gradRho

end

end SimultaneousFDivergenceSpatial
end InformationTheory
end TechnicalLemmas
end AutoSamplingTheory
