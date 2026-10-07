import AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC1
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.Deriv.Slope

/-!
# C² convexity and genuine Hessian lower bounds

Chewi, Lectures on Optimization, arXiv:2605.07006v1, Proposition 1.6
part 2. The two directions follow the source's positive-direction derivative
limit and affine-segment Hessian integral. Existing scalar-convexity proofs
remain separate. Shared leaves allow signed modulus on complete real
inner-product spaces; the final theorem restores the Euclidean source domain.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC2

open Set Filter MeasureTheory
open scoped Topology RealInnerProductSpace

set_option backward.isDefEq.respectTransparency false

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- The genuine Hessian integrates to the gradient difference paired with the
segment direction. C² supplies continuity and integrability. -/
theorem gradient_sub_inner_eq_integral_fderiv2
    {f : E → ℝ} (hf : ContDiff ℝ 2 f) (x v : E) :
    inner ℝ (gradient f (x + v) - gradient f x) v =
      ∫ t : ℝ in 0..1, (fderiv ℝ (fderiv ℝ f) (x + t • v) v) v := by
  have hfd : ContDiff ℝ 1 (fderiv ℝ f) := hf.fderiv_right (by norm_num)
  have hd (t : ℝ) : HasDerivAt (fun s : ℝ => fderiv ℝ f (x + s • v) v)
      ((fderiv ℝ (fderiv ℝ f) (x + t • v) v) v) t := by
    convert ((hfd.differentiable_one _).hasFDerivAt.comp_hasDerivAt t
      (((hasDerivAt_id t).smul_const v).const_add x)).clm_apply
      (hasDerivAt_const t v) using 1 <;> first | rfl | simp
  have hc : Continuous (fun t : ℝ => (fderiv ℝ (fderiv ℝ f) (x + t • v) v) v) :=
    (((hfd.continuous_fderiv (by norm_num)).comp
      (continuous_const.add (continuous_id.smul continuous_const))).clm_apply
        continuous_const).clm_apply continuous_const
  simpa [inner_sub_left, gradient, Function.comp_def] using
    (intervalIntegral.integral_eq_sub_of_hasDerivAt
      (fun t _ => hd t) (hc.intervalIntegrable 0 1)).symm

/-- Global quantitative gradient monotonicity is equivalent to the genuine
Hessian diagonal lower bound, by a right derivative limit and the FTC. -/
theorem gradient_mono_iff_fderiv2_lower
    {f : E → ℝ} {m : ℝ} (hf : ContDiff ℝ 2 f) :
    (∀ x y : E, m * ‖y - x‖ ^ 2 ≤
      inner ℝ (gradient f y - gradient f x) (y - x)) ↔
    ∀ x v : E, m * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ f) x v) v := by
  have hfd : ContDiff ℝ 1 (fderiv ℝ f) := hf.fderiv_right (by norm_num)
  constructor
  · intro hm x v
    let g : ℝ → ℝ := fun t => fderiv ℝ f (x + t • v) v
    have hdAll (t : ℝ) : HasDerivAt g
        ((fderiv ℝ (fderiv ℝ f) (x + t • v) v) v) t := by
      convert ((hfd.differentiable_one _).hasFDerivAt.comp_hasDerivAt t
        (((hasDerivAt_id t).smul_const v).const_add x)).clm_apply
        (hasDerivAt_const t v) using 1 <;> first | rfl | simp
    have hd : HasDerivAt g ((fderiv ℝ (fderiv ℝ f) x v) v) 0 := by
      simpa using hdAll 0
    apply ge_of_tendsto hd.tendsto_slope_zero_right
    filter_upwards [self_mem_nhdsWithin] with t ht
    have ht : 0 < t := ht
    have h := hm x (x + t • v)
    rw [add_sub_cancel_left, norm_smul, Real.norm_eq_abs, mul_pow, sq_abs,
      inner_smul_right, inner_sub_left] at h
    have hscaled : t * (m * ‖v‖ ^ 2) ≤ g t - g 0 := by
      apply le_of_mul_le_mul_left (a := t) _ ht
      simpa [g, gradient, Function.comp_def, pow_two, mul_assoc, mul_left_comm, mul_comm] using h
    simpa [smul_eq_mul, div_eq_inv_mul] using
      (le_div_iff₀ ht).mpr (by simpa [mul_comm] using hscaled)
  · intro hH x y
    let v := y - x
    have hc : Continuous (fun t : ℝ => (fderiv ℝ (fderiv ℝ f) (x + t • v) v) v) :=
      (((hfd.continuous_fderiv (by norm_num)).comp
        (continuous_const.add (continuous_id.smul continuous_const))).clm_apply
          continuous_const).clm_apply continuous_const
    have h := intervalIntegral.integral_mono_on (by norm_num : (0 : ℝ) ≤ 1)
      (intervalIntegrable_const : IntervalIntegrable (fun _ : ℝ => m * ‖v‖ ^ 2) volume 0 1)
      (hc.intervalIntegrable 0 1) (fun t _ => hH (x + t • v) v)
    rw [← gradient_sub_inner_eq_integral_fderiv2 hf x v] at h
    simpa [v] using h

/-- Proposition 1.6 part 2, with the source's whole Euclidean domain,
nonnegative modulus and C² regularity. Together with the C¹ theorem this
connects all four source conditions. -/
theorem strongConvexOn_iff_fderiv2_lower
    {d : ℕ} {f : EuclideanSpace ℝ (Fin d) → ℝ} {m : ℝ}
    (hm : 0 ≤ m) (hf : ContDiff ℝ 2 f) :
    StrongConvexOn univ m f ↔
      ∀ x v, m * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ f) x v) v := by
  exact (ConvexityC1.convexity_equivalences hm (hf.of_le (by norm_num))).2.trans
    (gradient_mono_iff_fderiv2_lower hf)

end AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC2
