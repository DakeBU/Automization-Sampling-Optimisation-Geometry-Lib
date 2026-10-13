import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinGenerator
import Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries
import Mathlib.Analysis.Calculus.FDeriv.Mul

/-!
# Carre du champ of the Langevin differential expression

This file supplies the second-order product rule missing between the abstract
carre-du-champ interface and the concrete finite-dimensional Langevin
differential expression.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace LangevinCarreDuChamp

open scoped BigOperators RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]

/-- The Laplacian product rule for two globally `C²` real observables. -/
theorem laplacian_mul
    (f g : E → ℝ) (hf : ContDiff ℝ 2 f) (hg : ContDiff ℝ 2 g)
    (x : E) :
    Laplacian.laplacian (f * g) x =
      f x * Laplacian.laplacian g x +
      g x * Laplacian.laplacian f x +
      2 * inner ℝ (gradient f x) (gradient g x) := by
  have hf1 : Differentiable ℝ f := hf.differentiable (by norm_num)
  have hg1 : Differentiable ℝ g := hg.differentiable (by norm_num)
  have hDf : Differentiable ℝ (fun y => fderiv ℝ f y) :=
    (hf.fderiv_right (m := 1) (by norm_num)).differentiable one_ne_zero
  have hDg : Differentiable ℝ (fun y => fderiv ℝ g y) :=
    (hg.fderiv_right (m := 1) (by norm_num)).differentiable one_ne_zero
  have hfirst : fderiv ℝ (f * g) =
      fun y => f y • fderiv ℝ g y + g y • fderiv ℝ f y := by
    funext y
    exact fderiv_mul (hf1 y) (hg1 y)
  have hdiag (v : E) :
      iteratedFDeriv ℝ 2 (f * g) x ![v, v] =
        f x * iteratedFDeriv ℝ 2 g x ![v, v] +
        g x * iteratedFDeriv ℝ 2 f x ![v, v] +
        2 * (fderiv ℝ f x v) * (fderiv ℝ g x v) := by
    rw [iteratedFDeriv_two_apply, hfirst]
    change
      ((fderiv ℝ
        (f • (fun y => fderiv ℝ g y) +
          g • (fun y => fderiv ℝ f y)) x) v) v = _
    rw [fderiv_add ((hf1.smul hDg) x) ((hg1.smul hDf) x)]
    rw [fderiv_smul (hf1 x) (hDg x)]
    rw [fderiv_smul (hg1 x) (hDf x)]
    simp only [add_apply, smul_apply,
      ContinuousLinearMap.smulRight_apply, smul_eq_mul]
    have hsecondf :
        ((fderiv ℝ (fun y => fderiv ℝ f y) x) v) v =
          iteratedFDeriv ℝ 2 f x ![v, v] := by
      simpa using
        (iteratedFDeriv_two_apply (𝕜 := ℝ) f x ![v, v]).symm
    have hsecondg :
        ((fderiv ℝ (fun y => fderiv ℝ g y) x) v) v =
          iteratedFDeriv ℝ 2 g x ![v, v] := by
      simpa using
        (iteratedFDeriv_two_apply (𝕜 := ℝ) g x ![v, v]).symm
    rw [hsecondf, hsecondg]
    ring
  simp_rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
  simp_rw [hdiag]
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
  rw [← Finset.mul_sum, ← Finset.mul_sum]
  simp_rw [
    Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt
      (hf1 x),
    Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt
      (hg1 x)]
  have hcross :
      (∑ i,
        2 * inner ℝ (gradient f x) ((stdOrthonormalBasis ℝ E) i) *
          inner ℝ (gradient g x) ((stdOrthonormalBasis ℝ E) i)) =
        2 * inner ℝ (gradient f x) (gradient g x) := by
    calc
      (∑ i,
          2 * inner ℝ (gradient f x) ((stdOrthonormalBasis ℝ E) i) *
            inner ℝ (gradient g x) ((stdOrthonormalBasis ℝ E) i)) =
          2 * ∑ i,
            inner ℝ (gradient f x) ((stdOrthonormalBasis ℝ E) i) *
              inner ℝ (gradient g x) ((stdOrthonormalBasis ℝ E) i) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro i _
        ring
      _ = 2 * inner ℝ (gradient f x) (gradient g x) := by
        rw [← (stdOrthonormalBasis ℝ E).sum_inner_mul_inner
          (gradient f x) (gradient g x)]
        apply congrArg (fun r : ℝ => 2 * r)
        apply Finset.sum_congr rfl
        intro i _
        rw [real_inner_comm ((stdOrthonormalBasis ℝ E) i) (gradient g x)]
  rw [hcross]

/-- The gradient product rule used by the Langevin drift cancellation. -/
theorem gradient_mul
    (f g : E → ℝ) (hf : Differentiable ℝ f) (hg : Differentiable ℝ g)
    (x : E) :
    gradient (f * g) x =
      f x • gradient g x + g x • gradient f x := by
  rw [gradient, fderiv_mul (hf x) (hg x)]
  simp [gradient]

/-- Chewi Example 1.2.17: the carre-du-champ expression of the formal
Langevin differential operator equals the gradient inner product. -/
theorem langevinCarreDuChamp_eq_inner
    {n : ℕ}
    (V f g : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (hf : ContDiff ℝ 2 f) (hg : ContDiff ℝ 2 g)
    (x : EuclideanSpace ℝ (Fin (n + 1))) :
    (2 : ℝ)⁻¹ *
        (LangevinGenerator.operator V (f * g) x -
          f x * LangevinGenerator.operator V g x -
          g x * LangevinGenerator.operator V f x) =
      inner ℝ (gradient f x) (gradient g x) := by
  have hf1 : Differentiable ℝ f := hf.differentiable (by norm_num)
  have hg1 : Differentiable ℝ g := hg.differentiable (by norm_num)
  simp only [LangevinGenerator.operator]
  rw [laplacian_mul f g hf hg x, gradient_mul f g hf1 hg1 x]
  simp only [inner_add_right, real_inner_smul_right]
  ring

/-- Diagonal form of Chewi Example 1.2.17. -/
theorem langevinCarreDuChamp_self_eq_norm_sq
    {n : ℕ}
    (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (hf : ContDiff ℝ 2 f)
    (x : EuclideanSpace ℝ (Fin (n + 1))) :
    (2 : ℝ)⁻¹ *
        (LangevinGenerator.operator V (f * f) x -
          2 * f x * LangevinGenerator.operator V f x) =
      ‖gradient f x‖ ^ 2 := by
  have h := langevinCarreDuChamp_eq_inner V f f hf hf x
  rw [real_inner_self_eq_norm_sq] at h
  calc
    (2 : ℝ)⁻¹ *
        (LangevinGenerator.operator V (f * f) x -
          2 * f x * LangevinGenerator.operator V f x) =
      (2 : ℝ)⁻¹ *
        (LangevinGenerator.operator V (f * f) x -
          f x * LangevinGenerator.operator V f x -
          f x * LangevinGenerator.operator V f x) := by ring
    _ = ‖gradient f x‖ ^ 2 := h

end LangevinCarreDuChamp
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
