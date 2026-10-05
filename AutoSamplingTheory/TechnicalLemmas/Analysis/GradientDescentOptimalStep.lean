import AutoSamplingTheory.TechnicalLemmas.Analysis.SmoothnessEquivalences
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.InnerProductSpace.Rayleigh

/-!
# Optimal constant step for a gradient map

Chewi arXiv:2605.07006v1 Exercise 3.2. Genuine C² regularity supplies Hessian
symmetry and affine-segment integrability. The Rayleigh norm formula implements
the source spectral bound on a complete real Hilbert space. The endpoint
max-envelope is minimized at 2/(α+β); this is a uniform curvature bound, not
an assertion of an optimal step for every individual objective.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep

open Set InnerProductSpace MeasureTheory
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

set_option backward.isDefEq.respectTransparency false in
/-- Actual gradient maps satisfy the endpoint spectral bound for nonnegative steps.
The curvature moduli may be signed; all Hessians are derived from the C² objective. -/
theorem gradient_step_endpoint_bound {f : E → ℝ} {α β h : ℝ}
    (hf : ContDiff ℝ 2 f) (hsc : StrongConvexOn univ α f) (hh : 0 ≤ h)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    (x y : E) :
    ‖(y - h • gradient f y) - (x - h • gradient f x)‖ ≤
      max |1 - h * α| |1 - h * β| * ‖y - x‖ := by
  let M := max |1 - h * α| |1 - h * β|
  have hM : 0 ≤ M := (abs_nonneg _).trans (le_max_left _ _)
  have hlo := (ConvexityC2.gradient_mono_iff_fderiv2_lower hf).mp (fun a b =>
    StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn hsc
      (fun z _ => ((hf.of_le (by norm_num) : ContDiff ℝ 1 f).differentiable_one z).hasGradientAt)
      (mem_univ a) (mem_univ b))
  have hup := (SmoothnessEquivalences.upper_model_iff_fderiv2_upper hf).mp hu
  let R : (E →L[ℝ] ℝ) →L[ℝ] E :=
    { toFun := (toDual ℝ E).symm
      map_add' := (toDual ℝ E).symm.map_add
      map_smul' := by intros; simp
      cont := (toDual ℝ E).symm.continuous }
  let H (z : E) : E →L[ℝ] E := R.comp (fderiv ℝ (fderiv ℝ f) z)
  let A (z : E) : E →L[ℝ] E := ContinuousLinearMap.id ℝ E - h • H z
  let T : E → E := fun z => z - h • gradient f z
  have hfd : ContDiff ℝ 1 (fderiv ℝ f) := hf.fderiv_right (by norm_num)
  have hgrad (z : E) : HasFDerivAt (gradient f) (H z) z :=
    R.hasFDerivAt.comp z (hfd.differentiable_one z).hasFDerivAt
  have hTd (z : E) : HasFDerivAt T (A z) z :=
    (hasFDerivAt_id z).sub ((hgrad z).const_smul h)
  have hT : ContDiff ℝ 1 T := contDiff_id.sub ((R.contDiff.comp hfd).const_smul h)
  have hinner (z v w : E) : inner ℝ (H z v) w = (fderiv ℝ (fderiv ℝ f) z v) w :=
    toDual_symm_apply
  have hsym (z : E) : (A z).IsSymmetric := by
    intro v w
    change inner ℝ (v - h • H z v) w = inner ℝ v (w - h • H z w)
    rw [inner_sub_left, inner_sub_right, real_inner_smul_left, inner_smul_right]
    have hr : inner ℝ v (H z w) = (fderiv ℝ (fderiv ℝ f) z w) v :=
      (real_inner_comm v (H z w)).symm.trans (hinner z w v)
    rw [hinner, hr]
    rw [hf.contDiffAt.isSymmSndFDerivAt (by norm_num) v w]
  have hnorm (z : E) : ‖A z‖ ≤ M := by
    rw [(A z).norm_eq_iSup_rayleighQuotient (hsym z)]
    apply ciSup_le
    intro v
    change |inner ℝ (A z v) v / ‖v‖ ^ 2| ≤ M
    by_cases hv : v = 0
    · simp [hv]
      exact hM
    · simp only [abs_div, abs_pow, abs_norm]
      apply (div_le_iff₀ (sq_pos_of_pos (norm_pos_iff.mpr hv))).mpr
      change |inner ℝ (v - h • H z v) v| ≤ M * ‖v‖ ^ 2
      rw [inner_sub_left, real_inner_smul_left, real_inner_self_eq_norm_sq, hinner]
      have hl := mul_le_mul_of_nonneg_left (hlo z v) hh
      have hu' := mul_le_mul_of_nonneg_left (hup z v) hh
      have hleft : 1 - h * α ≤ M := (le_abs_self _).trans (le_max_left _ _)
      have hright : -(1 - h * β) ≤ M := (neg_le_abs _).trans (le_max_right _ _)
      have hleft' := mul_le_mul_of_nonneg_right hleft (sq_nonneg ‖v‖)
      have hright' := mul_le_mul_of_nonneg_right hright (sq_nonneg ‖v‖)
      exact abs_le.mpr ⟨by nlinarith, by nlinarith⟩
  let v := y - x
  have hpath (t : ℝ) : HasDerivAt (fun s : ℝ => T (x + s • v)) (A (x + t • v) v) t := by
    convert (hTd (x + t • v)).comp_hasDerivAt t
      (((hasDerivAt_id t).smul_const v).const_add x) using 1 <;> simp [Function.comp_def]
  have hc : Continuous (fun t : ℝ => A (x + t • v) v) := by
    have hA : A = fderiv ℝ T := funext (fun z => (hTd z).fderiv.symm)
    rw [hA]
    exact ((hT.continuous_fderiv (by norm_num)).comp
      (continuous_const.add (continuous_id.smul continuous_const))).clm_apply continuous_const
  have hFTC : (∫ t : ℝ in 0..1, A (x + t • v) v) = T y - T x := by
    simpa [v] using intervalIntegral.integral_eq_sub_of_hasDerivAt
      (fun t _ => hpath t) (hc.intervalIntegrable 0 1)
  change ‖T y - T x‖ ≤ M * ‖v‖
  rw [← hFTC]
  simpa using intervalIntegral.norm_integral_le_of_norm_le_const (a := (0 : ℝ)) (b := 1)
    (fun t _ => ((A (x + t • v)).le_opNorm v).trans
      (mul_le_mul_of_nonneg_right (hnorm _) (norm_nonneg v)))

/-- The step `2/(α+β)` gives the sharp uniform curvature-envelope contraction.
Its factor minimizes the endpoint max-envelope over every real step.
The `α=0` boundary is nonexpansive, and `α=β` is retained. -/
theorem optimal_gradient_step {f : E → ℝ} {α β : ℝ}
    (hf : ContDiff ℝ 2 f) (hsc : StrongConvexOn univ α f)
    (hα : 0 ≤ α) (hβ : 0 < β) (hαβ : α ≤ β)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    (x y : E) :
    ‖(y - (2 / (α + β)) • gradient f y) - (x - (2 / (α + β)) • gradient f x)‖ ≤
        ((β - α) / (α + β)) * ‖y - x‖ ∧
      ∀ h : ℝ, (β - α) / (α + β) ≤ max |1 - h * α| |1 - h * β| := by
  have hD : 0 < α + β := add_pos_of_nonneg_of_pos hα hβ
  have hq : 0 ≤ (β - α) / (α + β) := div_nonneg (sub_nonneg.mpr hαβ) hD.le
  have ha : 1 - 2 / (α + β) * α = (β - α) / (α + β) := by field_simp; ring
  have hb : 1 - 2 / (α + β) * β = -((β - α) / (α + β)) := by field_simp; ring
  constructor
  · have hc := gradient_step_endpoint_bound hf hsc (show 0 ≤ 2 / (α + β) by positivity) hu x y
    simpa only [ha, hb, abs_neg, abs_of_nonneg hq, max_self] using hc
  · intro h
    let M := max |1 - h * α| |1 - h * β|
    have ha' : 1 - h * α ≤ M := (le_abs_self _).trans (le_max_left _ _)
    have hb' : -(1 - h * β) ≤ M := (neg_le_abs _).trans (le_max_right _ _)
    apply (div_le_iff₀ hD).mpr
    have h1 := mul_le_mul_of_nonneg_left ha' hβ.le
    have h2 := mul_le_mul_of_nonneg_left hb' hα
    nlinarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep
