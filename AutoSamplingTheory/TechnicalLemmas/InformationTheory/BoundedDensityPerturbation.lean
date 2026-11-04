/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Samplinglib contributors
-/
import Mathlib.InformationTheory.KullbackLeibler.KLFun
import Mathlib.Analysis.Calculus.LHopital
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Bounded linear perturbations of a density

The compensated entropy `klFun (1 + ε * f)` has second-order integral
coefficient `(∫ f²) / 2`. The actual scalar limit and a uniform integrable
quadratic bound are proved, not supplied as assumptions.

This is a canonical analytic prerequisite for Chewi, *Log-Concave Sampling*
(August 20, 2026), Exercise 1.7 / (1.E.1), also used in Corollary 2.1.2.
No identification with a normalized probability-law KL, Fisher limit, LSI,
Poincaré test-domain extension or complete exercise is asserted here.
-/

open MeasureTheory Filter
open scoped Topology

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation

private theorem klFun_upper {x : ℝ} (hx : 0 ≤ x) :
    _root_.InformationTheory.klFun x ≤ (x - 1) ^ 2 := by
  rcases eq_or_lt_of_le hx with h | h
  · subst x
    norm_num [_root_.InformationTheory.klFun_zero]
  · have hlog := mul_le_mul_of_nonneg_left (Real.log_le_sub_one_of_pos h) hx
    rw [_root_.InformationTheory.klFun_apply]
    nlinarith

private theorem scalar_limit (a : ℝ) :
    Tendsto (fun e : ℝ => _root_.InformationTheory.klFun (1 + e * a) / e ^ 2)
      (𝓝[≠] (0 : ℝ)) (𝓝 (a ^ 2 / 2)) := by
  have hlin : ∀ e : ℝ, HasDerivAt (fun s : ℝ => 1 + s * a) a e := by
    intro e
    convert! (hasDerivAt_const e 1).add ((hasDerivAt_id e).mul_const a) using 1; simp
  have hlog : HasDerivAt (fun e : ℝ => Real.log (1 + e * a)) a 0 := by
    convert! (Real.hasDerivAt_log (by norm_num : (1 + (0 : ℝ) * a) ≠ 0)).comp 0 (hlin 0)
      using 1; simp
  have hlogslope : Tendsto (fun e : ℝ => Real.log (1 + e * a) / e)
      (𝓝[≠] (0 : ℝ)) (𝓝 a) := by
    simpa [smul_eq_mul, div_eq_mul_inv, mul_comm] using hlog.tendsto_slope_zero
  have hpos : ∀ᶠ e : ℝ in 𝓝 (0 : ℝ), 0 < 1 + e * a :=
    (isOpen_lt continuous_const (continuous_const.add (continuous_id.mul continuous_const))).mem_nhds
      (by norm_num)
  apply HasDerivAt.lhopital_zero_nhdsNE
    (f' := fun e => a * Real.log (1 + e * a)) (g' := fun e => 2 * e)
  · filter_upwards [hpos.filter_mono nhdsWithin_le_nhds] with e he
    convert! (_root_.InformationTheory.hasDerivAt_klFun (ne_of_gt he)).comp e (hlin e)
      using 1; simp [mul_comm]
  · exact .of_forall fun e => by
      convert! (hasDerivAt_id e).pow 2 using 1; simp
  · filter_upwards [self_mem_nhdsWithin] with e he
    exact mul_ne_zero (by norm_num) (by simpa using he)
  · have h := _root_.InformationTheory.continuous_klFun.continuousAt.tendsto.comp
      (hlin 0).continuousAt.tendsto
    simpa only [Function.comp_def, zero_mul, add_zero, _root_.InformationTheory.klFun_one] using
      h.mono_left nhdsWithin_le_nhds
  · have hd : ContinuousAt (fun e : ℝ => e ^ 2) 0 := by fun_prop
    simpa only [zero_pow (by decide : 2 ≠ 0)] using hd.tendsto.mono_left nhdsWithin_le_nhds
  · convert! hlogslope.const_mul (a / 2) using 1
    · ext e
      simp only [div_eq_mul_inv, mul_inv_rev]
      ring_nf
    · ring_nf

/-- Actual second-order compensated-entropy limit for a uniformly a.e.-bounded
real measurable perturbation of a finite measure.

The integral uses Mathlib's `klFun`, not an assumed KL asymptotic. The finite
uniform bound yields eventual positivity and an integrable `f²` dominator;
the scalar coefficient is obtained by genuine log differentiation and
L'Hôpital's rule. No centering/probability normalization is needed for this
compensated statement. Those are separate inputs to a probability-KL consumer.
-/
theorem tendsto_integral_klFun_one_add_mul_div_sq
    {X : Type*} [MeasurableSpace X] (mu : Measure X) [IsFiniteMeasure mu]
    (f : X → ℝ) (hf : AEStronglyMeasurable f mu) {M : ℝ}
    (hbound : ∀ᵐ x ∂mu, |f x| ≤ M) :
    Tendsto (fun e : ℝ => (∫ x, _root_.InformationTheory.klFun (1 + e * f x) ∂mu) / e ^ 2)
      (𝓝[≠] (0 : ℝ)) (𝓝 ((∫ x, f x ^ 2 ∂mu) / 2)) := by
  have hsq : Integrable (fun x => f x ^ 2) mu := by
    refine (integrable_const (|M| ^ 2)).mono' (hf.pow 2) ?_
    filter_upwards [hbound] with x hx
    simpa only [Real.norm_eq_abs, abs_pow] using
      pow_le_pow_left₀ (abs_nonneg (f x)) (hx.trans (le_abs_self M)) 2
  have hsmall : ∀ᶠ e : ℝ in 𝓝 (0 : ℝ), |e| * |M| < 1 :=
    (isOpen_lt (continuous_abs.mul continuous_const) continuous_const).mem_nhds (by simp)
  have hlimit := tendsto_integral_filter_of_dominated_convergence (μ := mu)
    (F := fun e : ℝ => fun x => _root_.InformationTheory.klFun (1 + e * f x) / e ^ 2)
    (f := fun x => f x ^ 2 / 2) (l := 𝓝[≠] (0 : ℝ)) (fun x => f x ^ 2)
    (Filter.Eventually.of_forall fun e =>
      (by simpa only [div_eq_mul_inv, Pi.add_apply] using
        (_root_.InformationTheory.continuous_klFun.comp_aestronglyMeasurable
          (aestronglyMeasurable_const.add (hf.const_mul e))).mul_const ((e ^ 2)⁻¹)))
    ?_ hsq (ae_of_all mu fun x => scalar_limit (f x))
  · simpa only [integral_div] using hlimit
  · filter_upwards [hsmall.filter_mono nhdsWithin_le_nhds, self_mem_nhdsWithin] with e he he0
    have hne : e ≠ 0 := by simpa using he0
    filter_upwards [hbound] with x hx
    have habs : |e * f x| < 1 := by
      rw [abs_mul]
      exact (mul_le_mul_of_nonneg_left (hx.trans (le_abs_self M)) (abs_nonneg e)).trans_lt he
    have hpos : 0 < 1 + e * f x := by linarith [neg_abs_le (e * f x)]
    have hn := _root_.InformationTheory.klFun_nonneg (le_of_lt hpos)
    have hu : _root_.InformationTheory.klFun (1 + e * f x) ≤ (e * f x) ^ 2 := by
      simpa using klFun_upper (le_of_lt hpos)
    rw [Real.norm_eq_abs, abs_of_nonneg (div_nonneg hn (sq_nonneg e))]
    calc
      _ ≤ (e * f x) ^ 2 / e ^ 2 := div_le_div_of_nonneg_right hu (sq_nonneg e)
      _ = f x ^ 2 := by rw [mul_pow, mul_div_cancel_left₀ _ (pow_ne_zero 2 hne)]

end AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation
