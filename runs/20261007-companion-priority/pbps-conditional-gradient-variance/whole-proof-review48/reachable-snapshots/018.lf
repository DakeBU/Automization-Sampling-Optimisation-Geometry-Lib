import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.InnerProductSpace.Rayleigh
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-!
# Genuine Hessian segment integral

SPHMC arXiv:2609.06906v1 Lemma 4.6 uses the integral of the genuine Hessian
along a segment to represent a gradient difference. C² supplies symmetry and
continuous Bochner integrability. The complete real Hilbert-space statement
retains signed curvature bounds and includes the source's finite Euclidean case.
It does not construct the smoothed potential or prove the downstream kernel step.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.HessianSecantOperator

open Set InnerProductSpace MeasureTheory
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

set_option backward.isDefEq.respectTransparency false in
/-- The actual Riesz Hessian segment integral is a symmetric gradient secant
operator with inherited signed curvature bounds and the endpoint norm bound.
No operator, gradient identity, symmetry or integrability certificate is assumed. -/
theorem hessian_secant_operator {f : E → ℝ} {α β : ℝ}
    (hf : ContDiff ℝ 2 f)
    (hlo : ∀ z v, α * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ f) z v) v)
    (hup : ∀ z v, (fderiv ℝ (fderiv ℝ f) z v) v ≤ β * ‖v‖ ^ 2)
    (x y : E) :
    let φ := fun t : ℝ => continuousLinearMapOfBilin
      (fderiv ℝ (fderiv ℝ f) (y + t • (x - y)))
    let H := ∫ t : ℝ in 0..1, φ t
    IntervalIntegrable φ volume 0 1 ∧
      gradient f x - gradient f y = H (x - y) ∧
      H.IsSymmetric ∧
      (∀ v, α * ‖v‖ ^ 2 ≤ inner ℝ (H v) v ∧
        inner ℝ (H v) v ≤ β * ‖v‖ ^ 2) ∧
      ‖H‖ ≤ max |α| |β| := by
  let φ := fun t : ℝ => continuousLinearMapOfBilin
    (fderiv ℝ (fderiv ℝ f) (y + t • (x - y)))
  let H := ∫ t : ℝ in 0..1, φ t
  change IntervalIntegrable φ volume 0 1 ∧ _
  have hfd : ContDiff ℝ 1 (fderiv ℝ f) := hf.fderiv_right (by norm_num)
  have hc : Continuous φ := by
    unfold φ continuousLinearMapOfBilin
    exact continuous_const.clm_comp ((hfd.continuous_fderiv (by norm_num)).comp
      (continuous_const.add (continuous_id.smul continuous_const)))
  have hi : IntervalIntegrable φ volume 0 1 := hc.intervalIntegrable 0 1
  have hinner (v w : E) : inner ℝ (H v) w =
      ∫ t : ℝ in 0..1, (fderiv ℝ (fderiv ℝ f) (y + t • (x - y)) v) w := by
    change inner ℝ ((∫ t : ℝ in 0..1, φ t) v) w = _
    rw [ContinuousLinearMap.intervalIntegral_apply hi v, real_inner_comm]
    change (innerSL ℝ w) (∫ t : ℝ in 0..1, φ t v) = _
    rw [← (innerSL ℝ w).intervalIntegral_comp_comm
      (((hc.clm_apply continuous_const : Continuous (fun t => φ t v))).intervalIntegrable
        (μ := volume) 0 1)]
    apply intervalIntegral.integral_congr
    intro t _
    exact (real_inner_comm w (φ t v)).symm.trans
      (continuousLinearMapOfBilin_apply _ v w)
  have hgrad : gradient f x - gradient f y = H (x - y) := by
    apply ext_inner_right ℝ
    intro w
    rw [hinner]
    have hd (t : ℝ) : HasDerivAt
        (fun s : ℝ => fderiv ℝ f (y + s • (x - y)) w)
        ((fderiv ℝ (fderiv ℝ f) (y + t • (x - y)) (x - y)) w) t := by
      convert ((hfd.differentiable_one _).hasFDerivAt.comp_hasDerivAt t
        (((hasDerivAt_id t).smul_const (x - y)).const_add y)).clm_apply
        (hasDerivAt_const t w) using 1 <;> first | rfl | simp
    have hdcont : Continuous (fun t : ℝ =>
        (fderiv ℝ (fderiv ℝ f) (y + t • (x - y)) (x - y)) w) :=
      (((hfd.continuous_fderiv (by norm_num)).comp
        (continuous_const.add (continuous_id.smul continuous_const))).clm_apply
          continuous_const).clm_apply continuous_const
    simpa [inner_sub_left, gradient, Function.comp_def] using
      (intervalIntegral.integral_eq_sub_of_hasDerivAt
        (fun t _ => hd t) (hdcont.intervalIntegrable 0 1)).symm
  have hsym : H.IsSymmetric := by
    intro v w
    change inner ℝ (H v) w = inner ℝ v (H w)
    have hw : inner ℝ v (H w) =
        ∫ t : ℝ in 0..1, (fderiv ℝ (fderiv ℝ f) (y + t • (x - y)) w) v :=
      (real_inner_comm v (H w)).symm.trans (hinner w v)
    rw [hinner, hw]
    apply intervalIntegral.integral_congr
    intro t _
    exact hf.contDiffAt.isSymmSndFDerivAt (by norm_num) v w
  have hbound (v : E) : α * ‖v‖ ^ 2 ≤ inner ℝ (H v) v ∧
      inner ℝ (H v) v ≤ β * ‖v‖ ^ 2 := by
    have hvcont : Continuous (fun t : ℝ =>
        (fderiv ℝ (fderiv ℝ f) (y + t • (x - y)) v) v) :=
      (((hfd.continuous_fderiv (by norm_num)).comp
        (continuous_const.add (continuous_id.smul continuous_const))).clm_apply
          continuous_const).clm_apply continuous_const
    rw [hinner]
    constructor
    · simpa using intervalIntegral.integral_mono_on (by norm_num : (0 : ℝ) ≤ 1)
        (intervalIntegrable_const : IntervalIntegrable (fun _ : ℝ => α * ‖v‖ ^ 2) volume 0 1)
        (hvcont.intervalIntegrable 0 1) (fun t _ => hlo _ v)
    · simpa using intervalIntegral.integral_mono_on (by norm_num : (0 : ℝ) ≤ 1)
        (hvcont.intervalIntegrable 0 1)
        (intervalIntegrable_const : IntervalIntegrable (fun _ : ℝ => β * ‖v‖ ^ 2) volume 0 1)
        (fun t _ => hup _ v)
  refine ⟨hi, hgrad, hsym, hbound, ?_⟩
  rw [H.norm_eq_iSup_rayleighQuotient hsym]
  apply ciSup_le
  intro v
  change |inner ℝ (H v) v / ‖v‖ ^ 2| ≤ max |α| |β|
  by_cases hv : v = 0
  · simp [hv]
  · simp only [abs_div, abs_pow, abs_norm]
    apply (div_le_iff₀ (sq_pos_of_pos (norm_pos_iff.mpr hv))).mpr
    have hl := (hbound v).1
    have hu := (hbound v).2
    have hl' := mul_le_mul_of_nonneg_right
      ((neg_le_abs α).trans (le_max_left |α| |β|)) (sq_nonneg ‖v‖)
    have hu' := mul_le_mul_of_nonneg_right
      ((le_abs_self β).trans (le_max_right |α| |β|)) (sq_nonneg ‖v‖)
    exact abs_le.mpr ⟨by nlinarith, by nlinarith⟩

end AutoSamplingTheory.TechnicalLemmas.Analysis.HessianSecantOperator
