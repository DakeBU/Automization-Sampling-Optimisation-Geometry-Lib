/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Samplinglib contributors
-/
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation

/-!
# The compact Euclidean log-Sobolev-to-Poincaré implication

Chewi, *Log-Concave Sampling* (August 20, 2026), Exercise 1.7, in the
compact smooth function-form setting of §2.1.1. The original observable
is centered inside the proof; only its derivative retains compact support.
The cutoff extension allows the actual square-root perturbation as an LSI
test, and the two quadratic limits preserve the constant. The broader
closed-form/semigroup implication and the standalone probability-KL expansion
are separate statements.
-/

set_option autoImplicit false
noncomputable section
open MeasureTheory Filter
open scoped Topology ContDiff RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare

open Analysis.Calculus.CompactGradientSqrtPerturbation
open Analysis.Calculus.BoundedPerturbationEnergy
open Analysis.Calculus.Gradient (continuous_gradient_of_contDiff_one)
open InformationTheory.BoundedDensityPerturbation
open LogSobolevCutoff

/-- A compact smooth function-form LSI implies the Poincaré inequality on the
same test class and with the same constant. The observable and both real
integrands in the conclusion are integrable, not merely totalized. -/
theorem variance_le_of_compact_logSobolev
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] (C : ℝ)
    (hLSI : ∀ (v : E → ℝ), ContDiff ℝ ∞ v → HasCompactSupport v →
      (∫ x, (v x)^2 * Real.log ((v x)^2) ∂μ) -
        (∫ x, (v x)^2 ∂μ) * Real.log (∫ x, (v x)^2 ∂μ) ≤
      2 * C * ∫ x, ‖gradient v x‖^2 ∂μ)
    (f : E → ℝ) (hf : ContDiff ℝ ∞ f) (hs : HasCompactSupport f) :
    Poincare.Admissible μ f ∧ Poincare.variance μ f ≤ C * Poincare.dirichletEnergy μ f := by
  have hfi : Integrable f μ := hf.continuous.integrable_of_hasCompactSupport hs
  let c : ℝ := ∫ x, f x ∂μ
  let g : E → ℝ := fun x => f x - c
  have hg : ContDiff ℝ ∞ g := hf.sub contDiff_const
  have hgi : Integrable g μ := hfi.sub (integrable_const c)
  have hmean : (∫ x, g x ∂μ) = 0 := by
    rw [integral_sub hfi (integrable_const c), integral_const]
    simp [c]
  obtain ⟨B, hB⟩ := hs.isCompact.exists_bound_of_continuousOn hf.continuous.continuousOn
  have hfb (x : E) : |f x| ≤ |B| := by
    by_cases hx : x ∈ tsupport f
    · exact (by simpa only [Real.norm_eq_abs] using hB x hx : |f x| ≤ B).trans (le_abs_self B)
    · simp [image_eq_zero_of_notMem_tsupport hx]
  have hgb (x : E) : |g x| ≤ |B| + |c| := by
    calc
      |g x| ≤ |f x| + |c| := by
        simpa only [g, sub_eq_add_neg, abs_neg] using abs_add_le (f x) (-c)
      _ ≤ |B| + |c| := add_le_add (hfb x) le_rfl
  have hga : AEStronglyMeasurable g μ := hg.continuous.aestronglyMeasurable
  have hgsq : Integrable (fun x => (g x)^2) μ :=
    (MemLp.of_bound hga (|B| + |c|)
      (ae_of_all μ (fun x => by simpa only [Real.norm_eq_abs] using hgb x)) :
      MemLp g 2 μ).integrable_sq
  have hgd : fderiv ℝ g = fderiv ℝ f := by
    funext x
    simp only [g, fderiv_sub_const]
  have hgc : HasCompactSupport (fderiv ℝ g) := hgd.symm ▸ hs.fderiv ℝ
  have hnorm (v : E → ℝ) (x : E) : ‖fderiv ℝ v x‖ = ‖gradient v x‖ := by
    rw [← toDual_gradient]
    exact (InnerProductSpace.toDual ℝ E).norm_map _
  obtain ⟨henergy, hdata⟩ := eventually_contDiff_and_integrable_sqrt_perturbation μ g hg hgb hgc
  have hentropyLimit := tendsto_integral_klFun_one_add_mul_div_sq μ g hga (ae_of_all μ hgb)
  have henergyLimit := (eventually_integrable_and_tendsto_sqrt_perturbation_energy μ g
    (hg.differentiable (by simp)) (ae_of_all μ hgb) henergy).2
  have hscaled : ∀ᶠ e : ℝ in 𝓝[≠] (0 : ℝ),
      (∫ x, _root_.InformationTheory.klFun (1 + e * g x) ∂μ) / e^2 ≤
        2 * C * ((∫ x, ‖fderiv ℝ (fun y => Real.sqrt (1 + e * g y)) x‖^2 ∂μ) / e^2) := by
    filter_upwards [hdata.filter_mono nhdsWithin_le_nhds, self_mem_nhdsWithin] with e he he0
    have hne : e ≠ 0 := by simpa using he0
    obtain ⟨hpos, hu, hu2, hui, hud⟩ := he
    let p : E → ℝ := fun x => 1 + e * g x
    let u : E → ℝ := fun x => Real.sqrt (p x)
    have husq (x : E) : (u x)^2 = p x := Real.sq_sqrt (by
      have hx := hpos x
      dsimp [p]
      linarith)
    have hpi : Integrable p μ := (integrable_const 1).add (hgi.const_mul e)
    have hmass : (∫ x, p x ∂μ) = 1 := by
      rw [integral_add (integrable_const 1) (hgi.const_mul e), integral_const_mul, hmean]
      simp
    change Integrable (fun x => (u x)^2 * Real.log ((u x)^2)) μ at hui
    have hlog : Integrable (fun x => p x * Real.log (p x)) μ := by
      simpa only [husq] using hui
    have hkl : (∫ x, _root_.InformationTheory.klFun (p x) ∂μ) =
        ∫ x, p x * Real.log (p x) ∂μ := by
      simp only [_root_.InformationTheory.klFun_apply]
      have hplus : Integrable (fun x => p x * Real.log (p x) + 1) μ :=
        hlog.add (integrable_const 1)
      rw [integral_sub hplus hpi,
        integral_add hlog (integrable_const 1), hmass]
      simp
    change ContDiff ℝ ∞ u at hu
    change Integrable (fun x => ‖fderiv ℝ u x‖^2) μ at hud
    have hug : MemLp (gradient u) 2 μ :=
      (memLp_two_iff_integrable_sq_norm
        (continuous_gradient_of_contDiff_one (hu.of_le (by simp))).aestronglyMeasurable).mpr
        (by simpa only [hnorm u] using hud)
    have hle := logSobolev_of_compact_smooth_tests μ C hLSI u hu hu2 hug hui
    simp only [husq, hmass, Real.log_one, mul_zero, sub_zero] at hle
    change (∫ x, _root_.InformationTheory.klFun (p x) ∂μ) / e^2 ≤
      2 * C * ((∫ x, ‖fderiv ℝ u x‖^2 ∂μ) / e^2)
    rw [hkl, ← mul_div_assoc]
    exact div_le_div_of_nonneg_right (by simpa only [hnorm u] using hle)
      (sq_pos_of_ne_zero hne).le
  have hlim := le_of_tendsto_of_tendsto hentropyLimit (henergyLimit.const_mul (2 * C)) hscaled
  have henergyf : Integrable (fun x => ‖gradient f x‖^2) μ := by
    simpa only [hgd, hnorm f] using henergy
  refine ⟨⟨hfi, hgsq, henergyf⟩, ?_⟩
  rw [Poincare.variance, Poincare.dirichletEnergy]
  change (∫ x, (g x)^2 ∂μ) ≤ C * ∫ x, ‖gradient f x‖^2 ∂μ
  simp only [hgd, hnorm f] at hlim
  linarith

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare
