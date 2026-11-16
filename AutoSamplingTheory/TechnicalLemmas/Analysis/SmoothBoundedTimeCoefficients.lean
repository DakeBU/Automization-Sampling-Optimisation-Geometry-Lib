import Mathlib.Analysis.Calculus.BumpFunction.SmoothApprox
import Mathlib.MeasureTheory.Function.ContinuousMapDense
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.Tactic

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.SmoothBoundedTimeCoefficients

open MeasureTheory Set Metric
open scoped ContDiff

/-- A measurable coefficient in a bounded nonnegative range can be approximated
in time integral by a smooth strictly positive coefficient on the same horizon. -/
theorem exists_smooth_pos_of_ae_nonneg_bounded
    {a b C ε : ℝ} (hab : a ≤ b) (hC : 0 ≤ C) (hε : 0 < ε)
    (f : ℝ → ℝ) (hf : Measurable f)
    (hRange : ∀ᵐ t ∂volume.restrict (Icc a b), f t ∈ Icc 0 C) :
    ∃ g : ℝ → ℝ, ContDiff ℝ ∞ g ∧
      (∀ t ∈ Icc a b, 0 < g t ∧ g t ≤ C + ε) ∧
      (∫ t in Icc a b, ‖g t - f t‖) < ε := by
  let ν := volume.restrict (Icc a b)
  have hν : ∀ᵐ t ∂ν, t ∈ Icc a b := ae_restrict_mem measurableSet_Icc
  have hfI : Integrable f ν :=
    Integrable.of_bound hf.aestronglyMeasurable C
      (hRange.mono fun t ht => by simpa [Real.norm_eq_abs, abs_of_nonneg ht.1] using ht.2)
  obtain ⟨q, hq, hqI⟩ := hfI.exists_boundedContinuous_integral_sub_le (half_pos hε)
  let u (t : ℝ) := max 0 (min C (q t))
  have huC : Continuous u := continuous_const.max (continuous_const.min q.continuous)
  have huRange (t : ℝ) : u t ∈ Icc 0 C := ⟨le_max_left _ _, max_le hC (min_le_left _ _)⟩
  have huI : Integrable u ν :=
    Integrable.of_bound huC.aestronglyMeasurable C (ae_of_all _ fun t => by
      simpa [Real.norm_eq_abs, abs_of_nonneg (huRange t).1] using (huRange t).2)
  have hClip : ∀ᵐ t ∂ν, ‖u t - f t‖ ≤ ‖f t - q t‖ := hRange.mono fun t ht => by
    change 0 ≤ f t ∧ f t ≤ C at ht
    simp only [u, Real.norm_eq_abs]
    rcases le_or_gt (q t) 0 with hq0 | hq0
    · rw [max_eq_left ((min_le_right C (q t)).trans hq0)]
      rw [abs_of_nonpos (by linarith [ht.1]), abs_of_nonneg (by linarith [ht.1])]
      linarith
    rcases le_or_gt C (q t) with hqC | hqC
    · rw [min_eq_left hqC, max_eq_right hC]
      rw [abs_of_nonneg (sub_nonneg.mpr ht.2), abs_of_nonpos (by linarith [ht.2])]
      linarith
    rw [min_eq_right hqC.le, max_eq_right hq0.le, abs_sub_comm]
  have hApprox : (∫ t, ‖u t - f t‖ ∂ν) ≤ ε / 2 :=
    (integral_mono_ae (huI.sub hfI).norm (hfI.sub hqI).norm hClip).trans hq
  let δ := ε / (4 * (b - a + 1))
  have hLen := sub_nonneg.mpr hab
  have hDen : 0 < 4 * (b - a + 1) := by positivity
  have hδ : 0 < δ := div_pos hε hDen
  have hδEq : δ * (4 * (b - a + 1)) = ε := div_mul_cancel₀ _ hDen.ne'
  have hδE : 2 * δ ≤ ε := by nlinarith [mul_nonneg hδ.le hLen]
  have hδL : 2 * δ * (b - a) < ε / 2 := by nlinarith
  have hK : IsCompact (Metric.cthickening 1 (Icc a b)) := isCompact_Icc.cthickening
  obtain ⟨η, hη, hUniform⟩ := Metric.uniformContinuousOn_iff.mp
    (hK.uniformContinuousOn_of_continuous huC.continuousOn) (δ / 2) (half_pos hδ)
  obtain ⟨v, hv, hvNear⟩ :=
    huC.exists_contDiff_dist_le_of_forall_mem_ball_dist_le (lt_min one_pos hη)
  have hvClose (t : ℝ) (ht : t ∈ Icc a b) : dist (v t) (u t) ≤ δ / 2 := by
    apply hvNear t
    intro z hz
    rw [Metric.mem_ball, lt_min_iff] at hz
    exact (hUniform z (mem_cthickening_of_dist_le _ t _ _ ht hz.1.le) t
      (self_subset_cthickening _ ht) hz.2).le
  let w (t : ℝ) := v t + δ
  have hw : ContDiff ℝ ∞ w := hv.add contDiff_const
  have hwRange (t : ℝ) (ht : t ∈ Icc a b) : 0 < w t ∧ w t ≤ C + ε := by
    have h := abs_le.mp (by simpa [Real.dist_eq] using hvClose t ht)
    exact ⟨by dsimp [w]; linarith [h.1, (huRange t).1],
      by dsimp [w]; linarith [h.2, (huRange t).2]⟩
  have hwI : Integrable w ν :=
    Integrable.of_bound hw.continuous.aestronglyMeasurable (C + ε) (hν.mono fun t ht => by
      simpa [Real.norm_eq_abs, abs_of_nonneg (hwRange t ht).1.le] using (hwRange t ht).2)
  have hwClose : ∀ᵐ t ∂ν, ‖‖w t - u t‖‖ ≤ 2 * δ := hν.mono fun t ht => by
    have h := abs_le.mp (by simpa [Real.dist_eq] using hvClose t ht)
    rw [Real.norm_of_nonneg (norm_nonneg _), Real.norm_eq_abs]
    exact abs_le.mpr ⟨by dsimp [w]; linarith [h.1], by dsimp [w]; linarith [h.2]⟩
  have hνReal : ν.real univ = b - a := by
    rw [Measure.real_def, Measure.restrict_apply_univ, Real.volume_Icc, ENNReal.toReal_ofReal hLen]
  have hwU : (∫ t, ‖w t - u t‖ ∂ν) ≤ 2 * δ * (b - a) := by
    calc
      _ ≤ ‖∫ t, ‖w t - u t‖ ∂ν‖ := le_abs_self _
      _ ≤ 2 * δ * (b - a) := hνReal ▸ norm_integral_le_of_norm_le_const hwClose
  refine ⟨w, hw, hwRange, ?_⟩
  change (∫ t, ‖w t - f t‖ ∂ν) < ε
  calc
    _ ≤ ∫ t, ‖w t - u t‖ + ‖u t - f t‖ ∂ν := integral_mono_ae (hwI.sub hfI).norm
      ((hwI.sub huI).norm.add (huI.sub hfI).norm)
      (ae_of_all _ fun t => by simpa [Real.dist_eq, Real.norm_eq_abs] using dist_triangle (w t) (u t) (f t))
    _ = (∫ t, ‖w t - u t‖ ∂ν) + ∫ t, ‖u t - f t‖ ∂ν :=
      integral_add (hwI.sub huI).norm (huI.sub hfI).norm
    _ < ε := by linarith

private theorem sq_sqrt_sub_sqrt_le_abs_sub {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) :
    (Real.sqrt x - Real.sqrt y) ^ 2 ≤ |x - y| := by
  rcases le_total x y with h | h
  · rw [abs_of_nonpos (sub_nonpos.mpr h)]
    nlinarith [Real.sq_sqrt hx, Real.sq_sqrt hy,
      mul_nonneg (Real.sqrt_nonneg x) (sub_nonneg.mpr (Real.sqrt_le_sqrt h))]
  · rw [abs_of_nonneg (sub_nonneg.mpr h)]
    nlinarith [Real.sq_sqrt hx, Real.sq_sqrt hy,
      mul_nonneg (Real.sqrt_nonneg y) (sub_nonneg.mpr (Real.sqrt_le_sqrt h))]

/-- One smooth positive approximation controls the time integral of the coefficient
error and the square-integral error of the associated noise scale. -/
theorem exists_smooth_pos_with_noise_scale_approx
    {a b C ε : ℝ} (hab : a ≤ b) (hC : 0 ≤ C) (hε : 0 < ε)
    (f : ℝ → ℝ) (hf : Measurable f)
    (hRange : ∀ᵐ t ∂volume.restrict (Icc a b), f t ∈ Icc 0 C) :
    ∃ g : ℝ → ℝ, ContDiff ℝ ∞ g ∧
      (∀ t ∈ Icc a b, 0 < g t ∧ g t ≤ C + ε) ∧
      (∫ t in Icc a b, ‖g t - f t‖) < ε ∧
      (∫ t in Icc a b, ‖Real.sqrt (2 * g t) - Real.sqrt (2 * f t)‖ ^ 2) < ε := by
  obtain ⟨g, hg, hgRange, hgL1⟩ :=
    exists_smooth_pos_of_ae_nonneg_bounded hab hC (half_pos hε) f hf hRange
  let ν := volume.restrict (Icc a b)
  have hν : ∀ᵐ t ∂ν, t ∈ Icc a b := ae_restrict_mem measurableSet_Icc
  have hgI : Integrable g ν :=
    Integrable.of_bound hg.continuous.aestronglyMeasurable (C + ε / 2)
      (hν.mono fun t ht => by
        simpa [Real.norm_eq_abs, abs_of_nonneg (hgRange t ht).1.le] using (hgRange t ht).2)
  have hfI : Integrable f ν :=
    Integrable.of_bound hf.aestronglyMeasurable C
      (hRange.mono fun t ht => by simpa [Real.norm_eq_abs, abs_of_nonneg ht.1] using ht.2)
  let A (t : ℝ) := ‖Real.sqrt (2 * g t) - Real.sqrt (2 * f t)‖ ^ 2
  have hA : Measurable A :=
    ((Real.continuous_sqrt.measurable.comp (measurable_const.mul hg.continuous.measurable)).sub
      (Real.continuous_sqrt.measurable.comp (measurable_const.mul hf))).norm.pow_const 2
  have hABound : ∀ᵐ t ∂ν, A t ≤ 2 * ‖g t - f t‖ := by
    filter_upwards [hν, hRange] with t ht hft
    have hs := sq_sqrt_sub_sqrt_le_abs_sub (x := 2 * g t) (y := 2 * f t)
      (mul_nonneg (by norm_num) (hgRange t ht).1.le)
      (mul_nonneg (by norm_num) hft.1)
    simpa only [A, Real.norm_eq_abs, sq_abs, ← mul_sub, abs_mul, abs_of_nonneg (show 0 ≤ (2 : ℝ) by norm_num)] using hs
  have hDI : Integrable (fun t => 2 * ‖g t - f t‖) ν := (hgI.sub hfI).norm.const_mul 2
  have hAI : Integrable A ν := hDI.mono' hA.aestronglyMeasurable
    (hABound.mono fun t ht => by simpa [Real.norm_of_nonneg (sq_nonneg _), A] using ht)
  refine ⟨g, hg, fun t ht => ⟨(hgRange t ht).1, by linarith [(hgRange t ht).2]⟩, ?_, ?_⟩
  · exact hgL1.trans (half_lt_self hε)
  have hAInt := integral_mono_ae hAI hDI hABound
  rw [integral_const_mul] at hAInt
  change (∫ t, A t ∂ν) < ε
  linarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.SmoothBoundedTimeCoefficients

