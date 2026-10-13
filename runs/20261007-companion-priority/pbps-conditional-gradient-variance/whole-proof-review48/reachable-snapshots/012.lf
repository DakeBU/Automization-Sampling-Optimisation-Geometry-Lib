/-
Copyright (c) 2026 Yuanhe Zhang. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yuanhe Zhang, Jason D. Lee, Fanghui Liu
-/
import Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension
import Mathlib.Analysis.Calculus.ContDiff.Bounds
import Mathlib.Analysis.Calculus.LocalExtr.Basic

/-!
# Smooth radial cutoff functions

This file adapts the smooth cutoff construction from
`SLT.GaussianSobolevDense.Defs` in `lean-stat-learning-theory`, at commit
`d0f506f0a695018265dccb33bcb05e2f5ca1c876`, and generalizes its radial cutoff
from Euclidean coordinate spaces to real normed spaces, adding inner-product
and finite-dimensional hypotheses only where smoothness and compactness need
them.

The radial cutoff is one on the closed ball of radius `R`, vanishes outside the closed
ball of radius `2 * R`, takes values in `[0, 1]`, is smooth for `0 < R`, has
compact support in finite dimension, and converges pointwise to one as
`R -> infinity`.  The final theorem constructs a smooth compactly supported
plateau equal to one on a compact set inside any prescribed open neighborhood.

The first derivative of the radial family has a scale-uniform `C / R` bound.
This module does not provide second-derivative bounds, box-shaped `tsupport`
bounds, weighted integration by parts, or invariance statements.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Analysis
namespace Calculus
namespace Cutoff

open Filter Set Topology
open scoped Topology

/-- A smooth real cutoff equal to one on `[-1, 1]` and zero outside `(-2, 2)`. -/
noncomputable def smoothUnitCutoff : ℝ → ℝ :=
  (ContDiffBumpBase.ofInnerProductSpace ℝ).toFun 2

/-- The unit cutoff written using Mathlib's smooth transition function. -/
theorem smoothUnitCutoff_eq_smoothTransition (x : ℝ) :
    smoothUnitCutoff x = Real.smoothTransition (2 - |x|) := by
  have hden : (2 : ℝ) - 1 = 1 := by norm_num
  simp [smoothUnitCutoff, ContDiffBumpBase.ofInnerProductSpace, Real.norm_eq_abs, hden]

/-- The unit cutoff is infinitely differentiable. -/
theorem smoothUnitCutoff_contDiff : ContDiff ℝ (⊤ : ℕ∞) smoothUnitCutoff := by
  rw [contDiff_iff_contDiffAt]
  intro x
  have hmem :
      ((2 : ℝ), x) ∈ (Set.Ioi (1 : ℝ) ×ˢ (Set.univ : Set ℝ)) := by
    exact ⟨by norm_num, Set.mem_univ x⟩
  have hnhds :
      (Set.Ioi (1 : ℝ) ×ˢ (Set.univ : Set ℝ)) ∈ 𝓝 ((2 : ℝ), x) := by
    exact (isOpen_Ioi.prod isOpen_univ).mem_nhds hmem
  have hbase :
      ContDiffAt ℝ (⊤ : ℕ∞)
        (Function.uncurry (ContDiffBumpBase.ofInnerProductSpace ℝ).toFun)
        ((2 : ℝ), x) :=
    (ContDiffBumpBase.ofInnerProductSpace ℝ).smooth.contDiffAt hnhds
  have hpair : ContDiffAt ℝ (⊤ : ℕ∞) (fun y : ℝ => ((2 : ℝ), y)) x :=
    (contDiffAt_const (c := (2 : ℝ))).prodMk contDiffAt_id
  change ContDiffAt ℝ (⊤ : ℕ∞)
    (fun y : ℝ =>
      Function.uncurry (ContDiffBumpBase.ofInnerProductSpace ℝ).toFun ((2 : ℝ), y)) x
  exact hbase.comp x hpair

/-- The unit cutoff is one when `|x| <= 1`. -/
theorem smoothUnitCutoff_eq_one_of_abs_le_one {x : ℝ} (hx : |x| ≤ 1) :
    smoothUnitCutoff x = 1 := by
  have h : (1 : ℝ) ≤ 2 - |x| := by linarith
  simpa [smoothUnitCutoff_eq_smoothTransition] using
    (Real.smoothTransition.one_of_one_le (x := 2 - |x|) h)

/-- The unit cutoff vanishes when `2 <= |x|`. -/
theorem smoothUnitCutoff_eq_zero_of_two_le_abs {x : ℝ} (hx : 2 ≤ |x|) :
    smoothUnitCutoff x = 0 := by
  have h : 2 - |x| ≤ 0 := by linarith
  simpa [smoothUnitCutoff_eq_smoothTransition] using
    (Real.smoothTransition.zero_of_nonpos (x := 2 - |x|) h)

/-- The unit cutoff takes values in `[0, 1]`. -/
theorem smoothUnitCutoff_mem_Icc (x : ℝ) : smoothUnitCutoff x ∈ Set.Icc (0 : ℝ) 1 := by
  exact (ContDiffBumpBase.ofInnerProductSpace ℝ).mem_Icc 2 x

/-- The one-dimensional unit cutoff has compact support. -/
theorem smoothUnitCutoff_hasCompactSupport : HasCompactSupport smoothUnitCutoff := by
  apply HasCompactSupport.of_support_subset_isCompact
    (K := Set.Icc (-2 : ℝ) 2) isCompact_Icc
  intro x hx
  rw [Function.mem_support] at hx
  simp only [Set.mem_Icc]
  constructor
  · by_contra hleft
    push Not at hleft
    apply hx
    apply smoothUnitCutoff_eq_zero_of_two_le_abs
    rw [abs_of_nonpos (by linarith : x ≤ 0)]
    linarith
  · by_contra hright
    push Not at hright
    apply hx
    apply smoothUnitCutoff_eq_zero_of_two_le_abs
    rw [abs_of_nonneg (by linarith : 0 ≤ x)]
    linarith

/-- The derivative of the one-dimensional unit cutoff is bounded by one
positive constant.  The constant is chosen before any radial scale. -/
theorem smoothUnitCutoff_deriv_bounded :
    ∃ C : ℝ, 0 < C ∧ ∀ x : ℝ, ‖deriv smoothUnitCutoff x‖ ≤ C := by
  have hcont : Continuous (deriv smoothUnitCutoff) :=
    smoothUnitCutoff_contDiff.continuous_deriv
      (WithTop.coe_le_coe.mpr (le_top : (1 : ℕ∞) ≤ ⊤))
  obtain ⟨C, hC⟩ :=
    smoothUnitCutoff_hasCompactSupport.deriv.exists_bound_of_continuous hcont
  exact ⟨max C 1, lt_max_of_lt_right one_pos, fun x =>
    (hC x).trans (le_max_left C 1)⟩

/-- The second derivative of the unit cutoff is continuous. -/
theorem smoothUnitCutoff_secondDeriv_continuous :
    Continuous (deriv (deriv smoothUnitCutoff)) := by
  have htwo : ContDiff ℝ 2 smoothUnitCutoff :=
    smoothUnitCutoff_contDiff.of_le
      (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))
  have hzero : ContDiff ℝ 0 (deriv^[2] smoothUnitCutoff) :=
    htwo.iterate_deriv' 0 2
  simp only [Function.iterate_succ, Function.iterate_zero, Function.comp_apply] at hzero
  exact hzero.continuous

/-- The second derivative of the unit cutoff has compact support. -/
theorem smoothUnitCutoff_secondDeriv_hasCompactSupport :
    HasCompactSupport (deriv (deriv smoothUnitCutoff)) :=
  smoothUnitCutoff_hasCompactSupport.deriv.deriv

/-- One positive constant bounds the second derivative of the fixed unit
cutoff.  The constant is chosen before any radial scale, which is the compact
support input needed for a later `C / R^2` radial Hessian bound. -/
theorem smoothUnitCutoff_secondDeriv_bounded :
    ∃ C : ℝ, 0 < C ∧ ∀ x : ℝ, ‖deriv (deriv smoothUnitCutoff) x‖ ≤ C := by
  obtain ⟨C, hC⟩ :=
    smoothUnitCutoff_secondDeriv_hasCompactSupport.exists_bound_of_continuous
      smoothUnitCutoff_secondDeriv_continuous
  exact ⟨max C 1, lt_max_of_lt_right one_pos, fun x =>
    (hC x).trans (le_max_left C 1)⟩

section Radial

variable {E : Type*} [NormedAddCommGroup E]

/-- The radial cutoff at scale `R`, given by `x ↦ smoothUnitCutoff (‖x‖ / R)`. -/
noncomputable def radialSmoothCutoff (R : ℝ) (x : E) : ℝ :=
  smoothUnitCutoff (‖x‖ / R)

/-- The radial cutoff is one on the closed ball of radius `R`. -/
theorem radialSmoothCutoff_eq_one_of_norm_le {R : ℝ} (hR : 0 < R) {x : E}
    (hx : ‖x‖ ≤ R) : radialSmoothCutoff R x = 1 := by
  apply smoothUnitCutoff_eq_one_of_abs_le_one
  rw [abs_of_nonneg (div_nonneg (norm_nonneg x) hR.le)]
  exact div_le_one_of_le₀ hx hR.le

/-- The radial cutoff vanishes when `2 * R <= ||x||`. -/
theorem radialSmoothCutoff_eq_zero_of_two_mul_le_norm {R : ℝ} (hR : 0 < R) {x : E}
    (hx : 2 * R ≤ ‖x‖) : radialSmoothCutoff R x = 0 := by
  apply smoothUnitCutoff_eq_zero_of_two_le_abs
  rw [abs_of_nonneg (div_nonneg (norm_nonneg x) hR.le)]
  calc
    (2 : ℝ) = 2 * R / R := by field_simp
    _ ≤ ‖x‖ / R := div_le_div_of_nonneg_right hx hR.le

/-- Every radial cutoff value lies in `[0, 1]`, for any scale `R`. -/
theorem radialSmoothCutoff_mem_Icc (R : ℝ) (x : E) :
    radialSmoothCutoff R x ∈ Set.Icc (0 : ℝ) 1 :=
  smoothUnitCutoff_mem_Icc _

/-- Scaling the norm by a positive radius gives an operator-norm derivative
bound of `1 / R`.  Mathlib's totalized `fderiv` makes the statement valid at
the origin as well. -/
theorem fderiv_norm_div_bound [NormedSpace ℝ E] {R : ℝ} (hR : 0 < R) (x : E) :
    ‖fderiv ℝ (fun y : E => ‖y‖ / R) x‖ ≤ 1 / R := by
  have hLip : LipschitzWith ⟨1 / R, by positivity⟩ (fun y : E => ‖y‖ / R) :=
    LipschitzWith.of_dist_le_mul fun y z => by
      have hnorm : |‖y‖ - ‖z‖| ≤ ‖y - z‖ := abs_norm_sub_norm_le y z
      simp only [Real.dist_eq]
      have hdiv : ‖y‖ / R - ‖z‖ / R = (‖y‖ - ‖z‖) / R := by ring
      rw [hdiv, abs_div, abs_of_pos hR]
      calc
        |‖y‖ - ‖z‖| / R ≤ ‖y - z‖ / R :=
          div_le_div_of_nonneg_right hnorm hR.le
        _ = 1 / R * ‖y - z‖ := by ring
        _ = 1 / R * dist y z := by rw [dist_eq_norm]
  exact norm_fderiv_le_of_lipschitz ℝ hLip

/-- For positive scale, the radial cutoff is infinitely differentiable. -/
theorem radialSmoothCutoff_contDiff [InnerProductSpace ℝ E] {R : ℝ} (hR : 0 < R) :
    ContDiff ℝ (⊤ : ℕ∞) (radialSmoothCutoff R : E → ℝ) := by
  rw [contDiff_iff_contDiffAt]
  intro x
  by_cases hx : ‖x‖ < R
  · have heq : ∀ᶠ y in 𝓝 x, radialSmoothCutoff R y = 1 := by
      have hball : Metric.ball x (R - ‖x‖) ∈ 𝓝 x :=
        Metric.ball_mem_nhds x (sub_pos.mpr hx)
      filter_upwards [hball] with y hy
      apply radialSmoothCutoff_eq_one_of_norm_le hR
      rw [Metric.mem_ball, dist_eq_norm] at hy
      have hynorm : ‖y‖ ≤ ‖x‖ + ‖y - x‖ := by
        calc
          ‖y‖ = ‖x + (y - x)‖ := by congr 1; abel
          _ ≤ ‖x‖ + ‖y - x‖ := norm_add_le x (y - x)
      linarith
    have hconst : ContDiffAt ℝ (⊤ : ℕ∞) (fun _ : E => (1 : ℝ)) x :=
      contDiffAt_const
    apply hconst.congr_of_eventuallyEq
    filter_upwards [heq] with y hy
    simp [hy]
  · push Not at hx
    have hx_ne : x ≠ 0 := by
      intro hzero
      rw [hzero, norm_zero] at hx
      linarith
    have hnorm : ContDiffAt ℝ (⊤ : ℕ∞) (fun y : E => ‖y‖) x :=
      contDiffAt_norm ℝ hx_ne
    have hdiv : ContDiff ℝ (⊤ : ℕ∞) (fun t : ℝ => t / R) :=
      contDiff_id.div_const R
    have hscaled : ContDiffAt ℝ (⊤ : ℕ∞) (fun y : E => ‖y‖ / R) x :=
      hdiv.contDiffAt.comp x hnorm
    exact smoothUnitCutoff_contDiff.contDiffAt.comp x hscaled

/-- A single positive constant controls the first derivative of every
positive-scale radial cutoff by `C / R`.  The quantifier order records the
scale-uniformity needed by cutoff exhaustion arguments. -/
theorem radialSmoothCutoff_fderiv_bound [InnerProductSpace ℝ E] :
    ∃ C : ℝ, 0 < C ∧ ∀ R : ℝ, 0 < R → ∀ x : E,
      ‖fderiv ℝ (radialSmoothCutoff R : E → ℝ) x‖ ≤ C / R := by
  obtain ⟨C, hC_pos, hC_bound⟩ := smoothUnitCutoff_deriv_bounded
  refine ⟨C, hC_pos, ?_⟩
  intro R hR x
  by_cases hxR : ‖x‖ < R
  · have h_eq : ∀ᶠ y in 𝓝 x, radialSmoothCutoff R y = 1 := by
      have hradius : 0 < R - ‖x‖ := sub_pos.mpr hxR
      refine Metric.eventually_nhds_iff.mpr ⟨R - ‖x‖, hradius, ?_⟩
      intro y hy
      apply radialSmoothCutoff_eq_one_of_norm_le hR
      rw [dist_eq_norm] at hy
      have hynorm : ‖y‖ ≤ ‖x‖ + ‖y - x‖ := by
        calc
          ‖y‖ = ‖x + (y - x)‖ := by congr 1; abel
          _ ≤ ‖x‖ + ‖y - x‖ := norm_add_le x (y - x)
      linarith
    have hfderiv_eq : fderiv ℝ (radialSmoothCutoff R : E → ℝ) x = 0 := by
      have hconst : fderiv ℝ (fun _ : E => (1 : ℝ)) x = 0 := by simp
      exact (Filter.EventuallyEq.fderiv_eq h_eq).trans hconst
    rw [hfderiv_eq, norm_zero]
    exact div_nonneg hC_pos.le hR.le
  · push Not at hxR
    have hx_ne : x ≠ 0 := by
      intro hzero
      rw [hzero, norm_zero] at hxR
      linarith
    have hnorm_diff : DifferentiableAt ℝ (fun y : E => ‖y‖ / R) x := by
      have hnorm : DifferentiableAt ℝ (fun y : E => ‖y‖) x :=
        (contDiffAt_norm ℝ hx_ne).differentiableAt WithTop.top_ne_zero
      simpa only [div_eq_mul_inv] using hnorm.mul_const R⁻¹
    have hcutoff_diff : DifferentiableAt ℝ smoothUnitCutoff (‖x‖ / R) :=
      smoothUnitCutoff_contDiff.differentiable
        (WithTop.coe_ne_zero.mpr WithTop.top_ne_zero) (‖x‖ / R)
    have hchain :
        fderiv ℝ (radialSmoothCutoff R : E → ℝ) x =
          fderiv ℝ smoothUnitCutoff (‖x‖ / R) ∘L
            fderiv ℝ (fun y : E => ‖y‖ / R) x := by
      unfold radialSmoothCutoff
      exact fderiv_comp x hcutoff_diff hnorm_diff
    rw [hchain]
    calc
      ‖fderiv ℝ smoothUnitCutoff (‖x‖ / R) ∘L
          fderiv ℝ (fun y : E => ‖y‖ / R) x‖
          ≤ ‖fderiv ℝ smoothUnitCutoff (‖x‖ / R)‖ *
              ‖fderiv ℝ (fun y : E => ‖y‖ / R) x‖ :=
            ContinuousLinearMap.opNorm_comp_le _ _
      _ ≤ C * (1 / R) := by
        apply mul_le_mul
        · rw [← norm_deriv_eq_norm_fderiv]
          exact hC_bound _
        · exact fderiv_norm_div_bound hR x
        · exact norm_nonneg _
        · exact hC_pos.le
      _ = C / R := by ring

/-- The totalized derivative of the radial cutoff vanishes throughout the
outer zero region, including its boundary sphere.  At the boundary the cutoff
is a global minimum rather than locally constant; `IsLocalMin.fderiv_eq_zero`
records that distinction. -/
theorem radialSmoothCutoff_fderiv_eq_zero_of_two_mul_le_norm [NormedSpace ℝ E]
    {R : ℝ} (hR : 0 < R) {x : E} (hx : 2 * R ≤ ‖x‖) :
    fderiv ℝ (radialSmoothCutoff R : E → ℝ) x = 0 := by
  apply IsLocalMin.fderiv_eq_zero
  change ∀ᶠ y in 𝓝 x, radialSmoothCutoff R x ≤ radialSmoothCutoff R y
  rw [radialSmoothCutoff_eq_zero_of_two_mul_le_norm hR hx]
  exact Filter.Eventually.of_forall fun y => (radialSmoothCutoff_mem_Icc R y).1

/-- The support of the radial cutoff lies in the closed ball of radius `2 * R`. -/
theorem radialSmoothCutoff_support_subset_closedBall {R : ℝ} (hR : 0 < R) :
    Function.support (radialSmoothCutoff R : E → ℝ) ⊆
      Metric.closedBall 0 (2 * R) := by
  intro x hx
  rw [Metric.mem_closedBall, dist_zero_right]
  by_contra hout
  push Not at hout
  have hzero : radialSmoothCutoff R x = 0 :=
    radialSmoothCutoff_eq_zero_of_two_mul_le_norm hR hout.le
  exact hx hzero

/-- The topological support of the radial cutoff lies in the same closed ball. -/
theorem radialSmoothCutoff_tsupport_subset_closedBall {R : ℝ} (hR : 0 < R) :
    tsupport (radialSmoothCutoff R : E → ℝ) ⊆
      Metric.closedBall 0 (2 * R) := by
  exact closure_minimal
    (radialSmoothCutoff_support_subset_closedBall hR) Metric.isClosed_closedBall

/-- In finite dimension, a positive-scale radial cutoff has compact support. -/
theorem radialSmoothCutoff_hasCompactSupport [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    {R : ℝ} (hR : 0 < R) :
    HasCompactSupport (radialSmoothCutoff R : E → ℝ) := by
  rw [hasCompactSupport_def]
  exact IsCompact.of_isClosed_subset
    (isCompact_closedBall (0 : E) (2 * R)) isClosed_closure
    (radialSmoothCutoff_tsupport_subset_closedBall hR)

/-- A single positive constant controls the second iterated Fréchet
derivative of every positive-scale radial cutoff by `C / R^2`.

The proof first bounds the second derivative of the unit-scale radial cutoff
using continuity and compact support.  It then writes the radius-`R` cutoff as
the unit cutoff composed with scalar dilation and applies Mathlib's exact
iterated-derivative composition rule for continuous linear maps. -/
theorem radialSmoothCutoff_iteratedFDeriv_two_bound
    [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] [Nontrivial E] :
    ∃ C : ℝ, 0 < C ∧ ∀ R : ℝ, 0 < R → ∀ x : E,
      ‖iteratedFDeriv ℝ 2 (radialSmoothCutoff R : E → ℝ) x‖ ≤ C / R ^ 2 := by
  have hunit_smooth : ContDiff ℝ (⊤ : ℕ∞)
      (radialSmoothCutoff 1 : E → ℝ) :=
    radialSmoothCutoff_contDiff one_pos
  have hunit_continuous : Continuous
      (iteratedFDeriv ℝ 2 (radialSmoothCutoff 1 : E → ℝ)) :=
    hunit_smooth.continuous_iteratedFDeriv
      (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))
  have hunit_support : HasCompactSupport
      (iteratedFDeriv ℝ 2 (radialSmoothCutoff 1 : E → ℝ)) :=
    (radialSmoothCutoff_hasCompactSupport one_pos).iteratedFDeriv 2
  obtain ⟨C, hC⟩ :=
    hunit_support.exists_bound_of_continuous hunit_continuous
  let C' : ℝ := max C 1
  have hC'_pos : 0 < C' := lt_max_of_lt_right one_pos
  refine ⟨C', hC'_pos, ?_⟩
  intro R hR x
  let L : E →L[ℝ] E := R⁻¹ • ContinuousLinearMap.id ℝ E
  have hL_norm : ‖L‖ ≤ 1 / R := by
    refine L.opNorm_le_bound (by positivity) ?_
    intro y
    simp only [L, smul_apply, ContinuousLinearMap.id_apply]
    rw [norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos hR]
    simp [one_div]
  have hfun : (radialSmoothCutoff R : E → ℝ) =
      (radialSmoothCutoff 1 : E → ℝ) ∘ L := by
    funext y
    simp only [radialSmoothCutoff, Function.comp_apply, L,
      smul_apply, ContinuousLinearMap.id_apply, div_one]
    rw [norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos hR]
    ring_nf
  rw [hfun]
  rw [L.iteratedFDeriv_comp_right hunit_smooth x
    (i := 2) (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))]
  calc
    ‖(iteratedFDeriv ℝ 2 (radialSmoothCutoff 1 : E → ℝ) (L x)).compContinuousLinearMap
        (fun _ => L)‖ ≤
        ‖iteratedFDeriv ℝ 2 (radialSmoothCutoff 1 : E → ℝ) (L x)‖ *
          ∏ _ : Fin 2, ‖L‖ :=
      ContinuousMultilinearMap.norm_compContinuousLinearMap_le _ _
    _ = ‖iteratedFDeriv ℝ 2 (radialSmoothCutoff 1 : E → ℝ) (L x)‖ * ‖L‖ ^ 2 := by
      simp
    _ ≤ C' * (1 / R) ^ 2 := by
      gcongr
      exact (hC (L x)).trans (le_max_left C 1)
    _ = C' / R ^ 2 := by ring

/-- At each fixed point, the positive-scale radial cutoffs tend to one as the scale diverges. -/
theorem radialSmoothCutoff_tendsto_one (x : E) :
    Tendsto (fun R : ℝ => radialSmoothCutoff R x) atTop (𝓝 1) := by
  apply tendsto_atTop_of_eventually_const (i₀ := ‖x‖ + 1)
  intro R hR
  have hR_pos : 0 < R := by
    calc
      0 < ‖x‖ + 1 := by positivity
      _ ≤ R := hR
  apply radialSmoothCutoff_eq_one_of_norm_le hR_pos
  linarith

end Radial

section Plateau

/-- A compact subset of an open set admits a smooth compactly supported plateau in that set.

The function takes values in `[0, 1]` and is identically one on the compact set. -/
theorem exists_contDiff_eq_one_tsupport_subset
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    {K U : Set E} (hK : IsCompact K) (hU : IsOpen U) (hKU : K ⊆ U) :
    ∃ χ : E → ℝ,
      Function.support χ ⊆ U ∧ tsupport χ ⊆ U ∧ HasCompactSupport χ ∧
        ContDiff ℝ (⊤ : ℕ∞) χ ∧ Set.range χ ⊆ Set.Icc 0 1 ∧ Set.EqOn χ 1 K := by
  obtain ⟨L, hL, hK_intL, hL_U⟩ := exists_compact_between hK hU hKU
  obtain ⟨g, hg_support, hg_contDiff, hg_range⟩ :=
    (isOpen_interior : IsOpen (interior L)).exists_contDiff_support_eq
      (E := E) (n := (⊤ : ℕ∞))
  have hg_pos : ∀ x ∈ K, 0 < g x := by
    intro x hx
    have hx_support : x ∈ Function.support g := by
      rw [hg_support]
      exact hK_intL hx
    exact lt_of_le_of_ne
      (hg_range (Set.mem_range_self x)).1 (Ne.symm hx_support)
  obtain ⟨m, hm_pos, hm_le⟩ :=
    hK.exists_forall_le' hg_contDiff.continuous.continuousOn hg_pos
  have hm_half_pos : 0 < m / 2 := half_pos hm_pos
  let χ : E → ℝ := fun x =>
    Real.smoothTransition ((g x - m / 2) / (m / 2))
  have hχ_support_superlevel :
      Function.support χ ⊆ {x : E | m / 2 ≤ g x} := by
    intro x hx
    change χ x ≠ 0 at hx
    have harg : 0 < (g x - m / 2) / (m / 2) := by
      apply lt_of_not_ge
      intro hnonpos
      apply hx
      exact Real.smoothTransition.zero_of_nonpos hnonpos
    have hnum : 0 < g x - m / 2 :=
      (div_pos_iff_of_pos_right hm_half_pos).mp harg
    exact (sub_pos.mp hnum).le
  have hsuperlevel_closed : IsClosed {x : E | m / 2 ≤ g x} :=
    isClosed_le continuous_const hg_contDiff.continuous
  have hχ_tsupport_superlevel :
      tsupport χ ⊆ {x : E | m / 2 ≤ g x} := by
    exact closure_minimal hχ_support_superlevel hsuperlevel_closed
  have hsuperlevel_intL : {x : E | m / 2 ≤ g x} ⊆ interior L := by
    intro x hx
    have hgx_pos : 0 < g x := hm_half_pos.trans_le hx
    have hx_support : x ∈ Function.support g := hgx_pos.ne'
    rwa [hg_support] at hx_support
  have hχ_tsupport_L : tsupport χ ⊆ L :=
    hχ_tsupport_superlevel.trans (hsuperlevel_intL.trans interior_subset)
  have hχ_tsupport_U : tsupport χ ⊆ U := hχ_tsupport_L.trans hL_U
  have hχ_support_U : Function.support χ ⊆ U :=
    (subset_tsupport χ).trans hχ_tsupport_U
  have hχ_compact : HasCompactSupport χ := by
    rw [hasCompactSupport_def]
    exact hL.of_isClosed_subset isClosed_closure hχ_tsupport_L
  have hχ_contDiff : ContDiff ℝ (⊤ : ℕ∞) χ := by
    apply Real.smoothTransition.contDiff.comp
    exact (hg_contDiff.sub contDiff_const).div_const (m / 2)
  have hχ_range : Set.range χ ⊆ Set.Icc (0 : ℝ) 1 := by
    rintro _ ⟨x, rfl⟩
    exact ⟨Real.smoothTransition.nonneg _, Real.smoothTransition.le_one _⟩
  have hχ_one : Set.EqOn χ 1 K := by
    intro x hx
    apply Real.smoothTransition.one_of_one_le
    rw [one_le_div hm_half_pos]
    linarith [hm_le x hx]
  exact ⟨χ, hχ_support_U, hχ_tsupport_U, hχ_compact,
    hχ_contDiff, hχ_range, hχ_one⟩

end Plateau

end Cutoff
end Calculus
end Analysis
end TechnicalLemmas
end AutoSamplingTheory
