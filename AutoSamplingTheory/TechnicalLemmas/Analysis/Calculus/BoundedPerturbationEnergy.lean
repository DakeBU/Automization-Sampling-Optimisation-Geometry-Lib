/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Samplinglib contributors
-/
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Genuine square-root perturbation energy

For an actually differentiable bounded real function with integrable squared
derivative norm, the energy of `sqrt (1 + e * f)` is finite for small `e` and,
after division by `e^2`, tends to one quarter of the original energy.

This supplies the energy side of Chewi, *Log-Concave Sampling* (August20 2026),
Exercise1.7, printed43/PDF55, and the function-form LSI linearization on
printed48/PDF60. It is not an RN-representative substitution, canonical Fisher
identity, probability construction or LSI-domain extension. The exercise must
still derive the original energy integrability and justify its noncompact test.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BoundedPerturbationEnergy

open MeasureTheory Filter
open scoped Topology

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

private theorem energy_formula (f : E → ℝ) (hf : Differentiable ℝ f)
    (e : ℝ) {x : E} (hpos : 0 < 1 + e * f x) :
    ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2 =
      e ^ 2 * (‖fderiv ℝ f x‖ ^ 2 / (4 * (1 + e * f x))) := by
  have hd : HasFDerivAt (fun y => 1 + e * f y) (e • fderiv ℝ f x) x := by
    simpa only [Pi.smul_apply, smul_eq_mul] using
      ((hf x).hasFDerivAt.const_smul e).const_add 1
  rw [(hd.sqrt (ne_of_gt hpos)).fderiv]
  simp only [norm_smul, Real.norm_eq_abs, mul_pow, sq_abs, div_pow]
  rw [Real.sq_sqrt hpos.le]
  ring

/-- The actual derivative energy of a bounded affine square-root perturbation is
eventually integrable (including at zero), with normalized quadratic limit `1/4`.

The measure need not be finite: the unperturbed energy is explicitly integrable.
Differentiability is genuine. The a.e. bound yields positivity only on a fixed
full-measure set; no global smoothness or compact-test LSI admissibility follows.
All perturbed measurability, integrability and domination are derived here.
-/
theorem eventually_integrable_and_tendsto_sqrt_perturbation_energy
    [MeasurableSpace E] [OpensMeasurableSpace E]
    (mu : Measure E) (f : E → ℝ) (hf : Differentiable ℝ f)
    {M : ℝ} (hbound : ∀ᵐ x ∂mu, |f x| ≤ M)
    (henergy : Integrable (fun x => ‖fderiv ℝ f x‖ ^ 2) mu) :
    (∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      Integrable (fun x => ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2) mu) ∧
    Tendsto (fun e : ℝ =>
      (∫ x, ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2 ∂mu) / e ^ 2)
      (𝓝[≠] (0 : ℝ)) (𝓝 ((∫ x, ‖fderiv ℝ f x‖ ^ 2 ∂mu) / 4)) := by
  let H : E → ℝ := fun x => ‖fderiv ℝ f x‖ ^ 2
  let F : ℝ → E → ℝ := fun e x => H x / (4 * (1 + e * f x))
  have hsmall : ∀ᶠ e : ℝ in 𝓝 (0 : ℝ), |e| * |M| < 1 / 2 :=
    (isOpen_lt (continuous_abs.mul continuous_const) continuous_const).mem_nhds (by norm_num)
  have hhalf (e : ℝ) (he : |e| * |M| < 1 / 2) {x : E} (hx : |f x| ≤ M) :
      1 / 2 ≤ 1 + e * f x := by
    have hb : |e * f x| < 1 / 2 := by
      rw [abs_mul]
      exact (mul_le_mul_of_nonneg_left (hx.trans (le_abs_self M)) (abs_nonneg e)).trans_lt he
    linarith [neg_abs_le (e * f x)]
  have hmeas (e : ℝ) : AEStronglyMeasurable (F e) mu := by
    have hden : Measurable (fun x => 4 * (1 + e * f x)) :=
      (measurable_const.add (measurable_const.mul hf.continuous.measurable)).const_mul 4
    exact (henergy.aestronglyMeasurable.aemeasurable.div hden.aemeasurable).aestronglyMeasurable
  have hdom (e : ℝ) (he : |e| * |M| < 1 / 2) : ∀ᵐ x ∂mu, ‖F e x‖ ≤ H x := by
    filter_upwards [hbound] with x hx
    have hp := hhalf e he hx
    have hd : 0 < 4 * (1 + e * f x) := by linarith
    have hn : 0 ≤ H x := sq_nonneg _
    change ‖H x / (4 * (1 + e * f x))‖ ≤ H x
    rw [Real.norm_eq_abs, abs_of_nonneg (div_nonneg hn hd.le)]
    apply (div_le_iff₀ hd).2
    nlinarith [mul_nonneg hn (by linarith : 0 ≤ 4 * (1 + e * f x) - 1)]
  constructor
  · filter_upwards [hsmall] with e he
    refine ((henergy.mono' (hmeas e) (hdom e he)).const_mul (e ^ 2)).congr ?_
    filter_upwards [hbound] with x hx
    have hp : 0 < 1 + e * f x := by linarith [hhalf e he hx]
    exact (energy_formula f hf e hp).symm
  · have hlimit := tendsto_integral_filter_of_dominated_convergence (μ := mu)
      (F := F) (f := fun x => H x / 4) (l := 𝓝 (0 : ℝ)) H
      (Eventually.of_forall hmeas) (hsmall.mono hdom) henergy
      (ae_of_all mu fun x => by
        have hd : Tendsto (fun e : ℝ => 4 * (1 + e * f x)) (𝓝 (0 : ℝ)) (𝓝 (4 : ℝ)) := by
          simpa using ((((tendsto_id : Tendsto (fun e : ℝ => e) (𝓝 0) (𝓝 0)).mul_const
            (f x)).const_add 1).const_mul 4)
        exact tendsto_const_nhds.div hd (by norm_num))
    have heq : (fun e : ℝ =>
        (∫ x, ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2 ∂mu) / e ^ 2) =ᶠ[𝓝[≠] 0]
          (fun e => ∫ x, F e x ∂mu) := by
      filter_upwards [hsmall.filter_mono nhdsWithin_le_nhds, self_mem_nhdsWithin] with e he he0
      have hne : e ≠ 0 := by simpa using he0
      rw [← integral_div]
      apply integral_congr_ae
      filter_upwards [hbound] with x hx
      have hp : 0 < 1 + e * f x := by linarith [hhalf e he hx]
      rw [energy_formula f hf e hp]
      exact mul_div_cancel_left₀ _ (pow_ne_zero 2 hne)
    have ht : Tendsto (fun e : ℝ => ∫ x, F e x ∂mu) (𝓝[≠] (0 : ℝ))
        (𝓝 (∫ x, H x / 4 ∂mu)) := hlimit.mono_left nhdsWithin_le_nhds
    simpa only [integral_div] using ht.congr' heq.symm

end AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BoundedPerturbationEnergy
