import AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC2
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.ODE.Gronwall

/-!
# Convex gradient-flow Lyapunov and last-time rates

Chewi, arXiv:2605.07006v1, Exercise 2.1: Lyapunov monotonicity and its two
upper-bound consequences. The later nonsmooth sharpness example is separate.
The curve and global minimizer are supplied; normalized rates need positive time.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowLastIterate

open Set InnerProductSpace
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- The source Lyapunov decreases along an actual convex gradient trajectory,
yielding last-time gradient and improved objective upper bounds. -/
theorem lyapunov_and_rates {f : E → ℝ} {X : ℝ → E} {z : E} {T : ℝ}
    (hT : 0 ≤ T) (hf : ContDiff ℝ 2 f) (hc : ConvexOn ℝ univ f)
    (hz : IsMinOn f univ z) (hX : ContinuousOn X (Icc 0 T))
    (hflow : ∀ t ∈ Ico 0 T, HasDerivWithinAt X (-gradient f (X t)) (Ici t) t) :
    AntitoneOn (fun t => t ^ 2 * ‖gradient f (X t)‖ ^ 2 +
      2 * t * (f (X t) - f z) + ‖X t - z‖ ^ 2) (Icc 0 T) ∧
    ∀ t ∈ Ioc 0 T, ‖gradient f (X t)‖ ^ 2 ≤ ‖X 0 - z‖ ^ 2 / t ^ 2 ∧
      f (X t) - f z ≤ ‖X 0 - z‖ ^ 2 / (4 * t) := by
  have hdf : Differentiable ℝ f := hf.differentiable (by norm_num)
  have hsc : StrongConvexOn univ 0 f := strongConvexOn_zero.mpr hc
  have hH := (ConvexityC2.gradient_mono_iff_fderiv2_lower hf).mp (fun x y =>
    StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn hsc
      (fun w _ => (hdf w).hasGradientAt) (mem_univ x) (mem_univ y))
  let R : (E →L[ℝ] ℝ) →L[ℝ] E :=
    { toFun := (toDual ℝ E).symm
      map_add' := (toDual ℝ E).symm.map_add
      map_smul' := by intros; simp
      cont := (toDual ℝ E).symm.continuous }
  let H (x : E) : E →L[ℝ] E := R.comp (fderiv ℝ (fderiv ℝ f) x)
  have hfd : ContDiff ℝ 1 (fderiv ℝ f) := hf.fderiv_right (by norm_num)
  have hg (x : E) : HasFDerivAt (gradient f) (H x) x :=
    R.hasFDerivAt.comp x (hfd.differentiable_one x).hasFDerivAt
  have hpos (x v : E) : 0 ≤ inner ℝ (H x v) v := by
    have hi : inner ℝ (H x v) v = (fderiv ℝ (fderiv ℝ f) x v) v := toDual_symm_apply
    simpa only [hi, zero_mul] using hH x v
  have hsupp (x : E) : f x - f z ≤ inner ℝ (gradient f x) (x - z) := by
    have h := StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hsc
      (fun w _ => (hdf w).hasGradientAt) (mem_univ x) (mem_univ z)
    rw [show z - x = -(x - z) by abel, inner_neg_right] at h
    simp only [zero_div, zero_mul, add_zero] at h
    linarith
  let L : ℝ → ℝ := fun t => t ^ 2 * ‖gradient f (X t)‖ ^ 2 +
    2 * t * (f (X t) - f z) + ‖X t - z‖ ^ 2
  let D : ℝ → ℝ := fun t => -2 * t ^ 2 * inner ℝ (H (X t) (gradient f (X t)))
    (gradient f (X t)) + 2 * (f (X t) - f z) - 2 * inner ℝ (gradient f (X t)) (X t - z)
  have hcont : ContinuousOn L (Icc 0 T) :=
    ((continuousOn_id.pow 2).mul (((continuous_iff_continuousAt.mpr (fun x => (hg x).continuousAt)).comp_continuousOn hX).norm.pow 2)).add
      (((continuousOn_const.mul continuousOn_id).mul ((hf.continuous.comp_continuousOn hX).sub continuousOn_const))) |>.add
        ((hX.sub continuousOn_const).norm.pow 2)
  have hd (t : ℝ) (ht : t ∈ Ico 0 T) : HasDerivWithinAt L (D t) (Ici t) t := by
    have hn := ((hg (X t)).comp_hasDerivWithinAt t (hflow t ht)).norm_sq
    have he : HasDerivWithinAt (fun s => f (X s)) (-‖gradient f (X t)‖ ^ 2) (Ici t) t := by
      have h : HasFDerivAt f (toDual ℝ E (gradient f (X t))) (X t) := (hdf (X t)).hasGradientAt
      simpa only [Function.comp_def, toDual_apply_apply, inner_neg_right,
        real_inner_self_eq_norm_sq] using h.comp_hasDerivWithinAt t (hflow t ht)
    have hr := ((hflow t ht).sub_const z).norm_sq
    have hid := (hasDerivAt_id t).hasDerivWithinAt (s := Ici t)
    convert (((hid.pow 2).mul hn).add ((hid.const_mul 2).mul (he.sub_const (f z)))).add hr using 1 <;>
      first | rfl | (simp only [D, Function.comp_def, id_eq, Pi.pow_apply, Nat.cast_ofNat,
        show (2 : ℕ) - 1 = 1 by decide, pow_one, mul_one, ContinuousLinearMap.map_neg,
        inner_neg_right, real_inner_comm]; ring)
  have hneg (t : ℝ) : D t ≤ 0 := by
    have hh := mul_nonneg (sq_nonneg t) (hpos (X t) (gradient f (X t)))
    have hs := hsupp (X t)
    dsimp [D]
    nlinarith
  have hm : AntitoneOn L (Icc 0 T) := by
    intro a ha b hb hab
    have h := le_gronwallBound_of_liminf_deriv_right_le (f' := D)
      (δ := L a) (K := 0) (ε := 0)
      (hcont.mono (show Icc a b ⊆ Icc 0 T from fun u hu => ⟨ha.1.trans hu.1, hu.2.trans hb.2⟩))
      (fun u hu r hr => by simpa [slope] using
        (hd u ⟨ha.1.trans hu.1, hu.2.trans_le hb.2⟩).liminf_right_slope_le hr)
      le_rfl (fun u _ => by simpa using hneg u) b ⟨hab, le_rfl⟩
    simpa [gronwallBound_K0] using h
  refine ⟨hm, ?_⟩
  intro t ht
  have hL := hm ⟨le_rfl, hT⟩ ⟨ht.1.le, ht.2⟩ ht.1.le
  simp only [L, zero_pow (by decide : 2 ≠ 0), zero_mul, zero_add] at hL
  have he : 0 ≤ f (X t) - f z := sub_nonneg.mpr (hz (mem_univ _))
  have hte := mul_nonneg ht.1.le he
  refine ⟨(le_div_iff₀ (sq_pos_of_pos ht.1)).mpr (by nlinarith [sq_nonneg ‖X t - z‖]), ?_⟩
  have hs := hsupp (X t)
  have hcs := real_inner_le_norm (gradient f (X t)) (X t - z)
  have hts := mul_le_mul_of_nonneg_left (hs.trans hcs) ht.1.le
  have hy := sq_nonneg (t * ‖gradient f (X t)‖ - ‖X t - z‖)
  apply (le_div_iff₀ (mul_pos (by norm_num) ht.1)).mpr
  nlinarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowLastIterate
