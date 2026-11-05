/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Samplinglib contributors
-/
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation

/-!
# Compact-test log-Sobolev implies compact-test Poincaré

The compact Euclidean linearization in Chewi, *Log-Concave Sampling*,
Exercise 1.7 and §2.1.1. The variance is written as a centered second moment.
This is not a claim about an abstract reversible Dirichlet form or its core.
-/

set_option autoImplicit false

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare

open MeasureTheory Filter
open scoped Topology ContDiff RealInnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- On a Borel probability space over a finite-dimensional real Hilbert space,
compact smooth function LSI with coefficient `2 * C` gives compact smooth
Poincaré with constant `C`. The centered perturbation is constructed from the
given observable, not required to be compactly supported. -/
theorem poincare_of_compact_logSobolev (μ : Measure E) [IsProbabilityMeasure μ]
    (C : ℝ) (_hC : 0 < C)
    (hLSI : ∀ v : E → ℝ, ContDiff ℝ ∞ v → HasCompactSupport v →
      (∫ x, (v x)^2 * Real.log ((v x)^2) ∂μ) -
        (∫ x, (v x)^2 ∂μ) * Real.log (∫ x, (v x)^2 ∂μ) ≤
      2 * C * ∫ x, ‖gradient v x‖^2 ∂μ)
    (g : E → ℝ) (hg : ContDiff ℝ ∞ g) (hcompact : HasCompactSupport g) :
    (∫ x, (g x - ∫ y, g y ∂μ)^2 ∂μ) ≤
      C * ∫ x, ‖gradient g x‖^2 ∂μ := by
  let m : ℝ := ∫ x, g x ∂μ
  let f (x : E) := g x - m
  have hf : ContDiff ℝ ∞ f := hg.sub contDiff_const
  have hgI := hg.continuous.integrable_of_hasCompactSupport hcompact (μ := μ)
  have hfI : Integrable f μ := hgI.sub (integrable_const m)
  have hfmean : (∫ x, f x ∂μ) = 0 := by
    change (∫ x, g x - m ∂μ) = 0
    rw [integral_sub hgI (integrable_const m)]
    simp [m]
  have hd : fderiv ℝ f = fderiv ℝ g := by
    funext x
    exact fderiv_sub_const m
  have hfcompact : HasCompactSupport (fderiv ℝ f) := by
    rw [hd]
    exact hcompact.fderiv ℝ
  obtain ⟨M, hM⟩ := hcompact.exists_bound_of_continuous hg.continuous
  have hbound (x : E) : |f x| ≤ M + |m| :=
    (abs_sub (g x) m).trans (add_le_add (by simpa [Real.norm_eq_abs] using hM x) le_rfl)
  obtain ⟨hbaseEnergy, hdata⟩ :=
    CompactGradientSqrtPerturbation.eventually_contDiff_and_integrable_sqrt_perturbation
      μ f hf hbound hfcompact
  have hnorm (v : E → ℝ) (x : E) : ‖fderiv ℝ v x‖ = ‖gradient v x‖ := by
    rw [← toDual_gradient]
    exact (InnerProductSpace.toDual ℝ E).norm_map _
  let q (e : ℝ) (x : E) := 1 + e * f x
  let u (e : ℝ) (x : E) := Real.sqrt (q e x)
  let energy (e : ℝ) := ∫ x, ‖fderiv ℝ (u e) x‖^2 ∂μ
  have hmass (e : ℝ) : (∫ x, q e x ∂μ) = 1 := by
    change (∫ x, 1 + e * f x ∂μ) = 1
    rw [integral_add (integrable_const 1) (hfI.const_mul e), integral_const_mul, hfmean]
    simp
  have hscaled : ∀ᶠ e : ℝ in 𝓝[≠] (0 : ℝ),
      (∫ x, _root_.InformationTheory.klFun (q e x) ∂μ) / e^2 ≤
        2 * C * (energy e / e^2) := by
    filter_upwards [hdata.filter_mono nhdsWithin_le_nhds, self_mem_nhdsWithin] with e he he0
    obtain ⟨hlower, hsmooth, hu2, hlog, henergy⟩ := he
    have hgradMeas : AEStronglyMeasurable (gradient (u e)) μ :=
      (Gradient.continuous_gradient_of_contDiff_one
        (hsmooth.of_le (by norm_num))).aestronglyMeasurable
    have hgradI : Integrable (fun x => ‖gradient (u e) x‖^2) μ := by
      simpa only [← hnorm] using henergy
    have hgrad2 := (memLp_two_iff_integrable_sq_norm hgradMeas).mpr hgradI
    have hineq := LogSobolevCutoff.logSobolev_of_compact_test
      μ C hLSI (u e) hsmooth hu2 hgrad2 hlog
    have hsq (x : E) : (u e x)^2 = q e x :=
      Real.sq_sqrt (le_trans (by norm_num) (hlower x))
    have hlogq : Integrable (fun x => q e x * Real.log (q e x)) μ := by
      change Integrable (fun x => (u e x)^2 * Real.log ((u e x)^2)) μ at hlog
      simpa only [hsq] using hlog
    have hqI : Integrable (q e) μ := (integrable_const 1).add (hfI.const_mul e)
    have hcomp : (∫ x, _root_.InformationTheory.klFun (q e x) ∂μ) =
        ∫ x, q e x * Real.log (q e x) ∂μ := by
      simp only [_root_.InformationTheory.klFun_apply]
      rw [integral_sub (f := fun x => q e x * Real.log (q e x) + 1)
          (hlogq.add (integrable_const 1)) hqI,
        integral_add hlogq (integrable_const 1), hmass]
      simp
    have hraw : (∫ x, _root_.InformationTheory.klFun (q e x) ∂μ) ≤ 2 * C * energy e := by
      rw [hcomp]
      simpa only [hsq, hmass, Real.log_one, mul_zero, sub_zero, energy, ← hnorm] using hineq
    have he0' : e ≠ 0 := he0
    simpa only [mul_div_assoc] using
      (div_le_div_of_nonneg_right hraw (sq_pos_of_ne_zero he0').le)
  have hEnt :=
    InformationTheory.BoundedDensityPerturbation.tendsto_integral_klFun_one_add_mul_div_sq
      μ f hf.continuous.aestronglyMeasurable (ae_of_all μ hbound)
  have hEnergy := (BoundedPerturbationEnergy.eventually_integrable_and_tendsto_sqrt_perturbation_energy
    μ f (hf.differentiable (by simp)) (ae_of_all μ hbound) hbaseEnergy).2
  have hlim := le_of_tendsto_of_tendsto hEnt (hEnergy.const_mul (2*C)) hscaled
  have hPI : (∫ x, f x^2 ∂μ) ≤ C * ∫ x, ‖fderiv ℝ f x‖^2 ∂μ := by
    linarith only [hlim]
  simpa only [f, m, hd, hnorm] using hPI

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare
