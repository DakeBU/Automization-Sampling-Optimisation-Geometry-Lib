import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.Deriv.AffineMap
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Tactic.Module

/-!
# C¹ convexity equivalences and the affine-segment integral proof

Source: Sinho Chewi, Lectures on Optimization, arXiv:2605.07006v1,
Proposition 1.6 part 1, equations (1.3)–(1.5). The shared integral leaves
retain a complete real inner-product space and signed modulus. The final
declaration specializes to the source's Euclidean C¹, nonnegative-modulus
setting. The C²/Hessian part is not asserted here.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC1

open Set MeasureTheory
open scoped RealInnerProductSpace

set_option backward.isDefEq.respectTransparency false

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- The fundamental theorem of calculus along an affine segment. Continuity
and interval integrability of the genuine gradient pairing follow from C¹. -/
theorem sub_eq_integral_gradient {f : E → ℝ} (hf : ContDiff ℝ 1 f) (x v : E) :
    f (x + v) - f x = ∫ s : ℝ in 0..1, inner ℝ (gradient f (x + s • v)) v := by
  have hc : Continuous (fun s : ℝ => inner ℝ (gradient f (x + s • v)) v) := by
    simpa [gradient, Function.comp_def] using
      ((hf.continuous_fderiv (by norm_num)).comp
        (continuous_const.add (continuous_id.smul continuous_const))).clm_apply continuous_const
  have hd (s : ℝ) : HasDerivAt (fun t : ℝ => f (x + t • v))
      (inner ℝ (gradient f (x + s • v)) v) s := by
    convert! (hf.differentiable_one (x + s • v)).hasGradientAt.hasFDerivAt.comp_hasDerivAt s
      (((hasDerivAt_id s).smul_const v).const_add x) using 1
    simp
  simpa using (intervalIntegral.integral_eq_sub_of_hasDerivAt
    (fun s _ => hd s) (hc.intervalIntegrable 0 1)).symm

/-- Quantitative gradient monotonicity implies the chord inequality by the
source's two affine-segment FTC identities and integration of their difference.
The modulus can be signed; no Hessian or extra integrability is assumed. -/
theorem strongConvexOn_univ_of_gradient_mono_integral
    {f : E → ℝ} {m : ℝ} (hf : ContDiff ℝ 1 f)
    (hm : ∀ x y : E, m * ‖y - x‖ ^ 2 ≤
      inner ℝ (gradient f y - gradient f x) (y - x)) :
    StrongConvexOn (univ : Set E) m f := by
  refine ⟨convex_univ, ?_⟩
  intro x _ y _ a t ha ht hat
  have hat' : a = 1 - t := by linarith
  subst a
  have ht1 : t ≤ 1 := by linarith
  rcases eq_or_lt_of_le ht1 with ht1 | ht1
  · subst t
    simp
  let v := y - x
  let A : ℝ → ℝ := fun s => inner ℝ (gradient f (x + s • v)) v
  let B : ℝ → ℝ := fun s => inner ℝ (gradient f (x + (s * t) • v)) v
  have hA : Continuous A := by
    simpa [A, gradient, Function.comp_def] using
      ((hf.continuous_fderiv (by norm_num)).comp
        (continuous_const.add (continuous_id.smul continuous_const))).clm_apply continuous_const
  have hB : Continuous B := by
    simpa [B, gradient, Function.comp_def] using
      ((hf.continuous_fderiv (by norm_num)).comp
        (continuous_const.add ((continuous_id.mul continuous_const).smul continuous_const))).clm_apply continuous_const
  have hbound : ∫ s : ℝ in 0..1, m * s * (1 - t) * ‖v‖ ^ 2 ≤
      ∫ s : ℝ in 0..1, (A s - B s) := by
    apply intervalIntegral.integral_mono_on_of_le_Ioo (by norm_num)
      ((show Continuous (fun s : ℝ => m * s * (1 - t) * ‖v‖ ^ 2) by fun_prop).intervalIntegrable 0 1)
      ((hA.sub hB).intervalIntegrable 0 1)
    intro s hs
    have h := hm (x + (s * t) • v) (x + s • v)
    have hdis : (x + s • v) - (x + (s * t) • v) = (s * (1 - t)) • v := by module
    rw [hdis, norm_smul, Real.norm_eq_abs, mul_pow, sq_abs, inner_smul_right] at h
    have hscaled : (s * (1 - t)) * (m * s * (1 - t) * ‖v‖ ^ 2) ≤
        (s * (1 - t)) * inner ℝ
          (gradient f (x + s • v) - gradient f (x + (s * t) • v)) v := by nlinarith [h]
    have hcancel := le_of_mul_le_mul_left hscaled (mul_pos hs.1 (sub_pos.mpr ht1))
    simpa [A, B, inner_sub_left] using hcancel
  have hpoly : (∫ s : ℝ in 0..1, m * s * (1 - t) * ‖v‖ ^ 2) =
      m / 2 * (1 - t) * ‖v‖ ^ 2 := by
    rw [intervalIntegral.integral_mul_const, intervalIntegral.integral_mul_const,
      intervalIntegral.integral_const_mul, integral_id]
    norm_num only [one_pow, zero_pow, sub_zero]
    ring
  rw [hpoly, intervalIntegral.integral_sub (hA.intervalIntegrable 0 1)
    (hB.intervalIntegrable 0 1)] at hbound
  have hy := sub_eq_integral_gradient hf x v
  have hz := sub_eq_integral_gradient hf x (t • v)
  have hpoint : (1 - t) • x + t • y = x + t • v := by dsimp [v]; module
  have hys : x + v = y := by simp [v]
  rw [hys] at hy
  change f y - f x = ∫ s : ℝ in 0..1, A s at hy
  simp only [smul_smul, inner_smul_right, intervalIntegral.integral_const_mul] at hz
  change f (x + t • v) - f x = t * ∫ s : ℝ in 0..1, B s at hz
  change f ((1 - t) • x + t • y) ≤ (1 - t) * f x + t * f y -
    (1 - t) * t * (m / 2 * ‖x - y‖ ^ 2)
  rw [hpoint, norm_sub_rev]
  change f (x + t • v) ≤ (1 - t) * f x + t * f y -
    (1 - t) * t * (m / 2 * ‖v‖ ^ 2)
  nlinarith [mul_le_mul_of_nonneg_left hbound ht]

/-- Proposition 1.6, part 1: on all of Euclidean space, the C¹ chord,
quadratic lower-model and gradient-monotonicity conditions are equivalent.
The nonnegative modulus is retained exactly as in the source. -/
theorem convexity_equivalences {d : ℕ} {f : EuclideanSpace ℝ (Fin d) → ℝ}
    {m : ℝ} (_hm : 0 ≤ m) (hf : ContDiff ℝ 1 f) :
    (StrongConvexOn univ m f ↔ ∀ x y,
      f x + inner ℝ (gradient f x) (y - x) + m / 2 * ‖y - x‖ ^ 2 ≤ f y) ∧
    (StrongConvexOn univ m f ↔ ∀ x y,
      m * ‖y - x‖ ^ 2 ≤ inner ℝ (gradient f y - gradient f x) (y - x)) := by
  have hg : ∀ z ∈ (univ : Set (EuclideanSpace ℝ (Fin d))),
      HasGradientAt f (gradient f z) z := fun z _ => (hf.differentiable_one z).hasGradientAt
  have hforward := fun (hsc : StrongConvexOn univ m f) x y =>
    StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hsc hg
      (mem_univ x) (mem_univ y)
  have hsum : (∀ x y, f x + inner ℝ (gradient f x) (y - x) +
      m / 2 * ‖y - x‖ ^ 2 ≤ f y) → ∀ x y,
      m * ‖y - x‖ ^ 2 ≤ inner ℝ (gradient f y - gradient f x) (y - x) := by
    intro hl x y
    have hxy := hl x y
    have hyx := hl y x
    rw [show x - y = -(y - x) by abel, inner_neg_right, norm_neg] at hyx
    rw [inner_sub_left]
    linarith
  exact ⟨⟨hforward, fun h => strongConvexOn_univ_of_gradient_mono_integral hf (hsum h)⟩,
    ⟨fun h => hsum (hforward h), strongConvexOn_univ_of_gradient_mono_integral hf⟩⟩

end AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC1
