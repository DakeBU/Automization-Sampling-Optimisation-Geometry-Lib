/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Samplinglib contributors
-/
import Mathlib.InformationTheory.KullbackLeibler.Basic
import Mathlib.Analysis.Normed.Group.Bounded
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Actual bounded centered perturbation laws

For sufficiently small real `e`, the literal density `1 + e * f` is positive
and has mass one. Its canonical KL divergence is finite and equals its
compensated entropy integral. Measurability, normalization, Radon--Nikodym
identification and entropy integrability are proved, not public premises.

This supplies a measure-theoretic step in Chewi, *Log-Concave Sampling*
(August 20, 2026), Exercise 1.7 / (1.E.1), also used by Corollary 2.1.2.
It does not prove the full exercise, Fisher limit, LSI-domain extension or PI.
-/

open MeasureTheory Filter
open scoped Topology

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw

/-- Bounded centered perturbations define actual probability laws near zero.
Their canonical extended-real KL, not just its totalized real value, is the
finite compensated entropy integral. The lower bound includes `e = 0`. -/
theorem eventually_isProbabilityMeasure_and_klDiv_eq_one_add_mul
    {X : Type*} [MeasurableSpace X] (mu : Measure X) [IsProbabilityMeasure mu]
    (f : X → ℝ) (hf : AEStronglyMeasurable f mu) {M : ℝ}
    (hbound : ∀ᵐ x ∂mu, |f x| ≤ M) (hcenter : (∫ x, f x ∂mu) = 0) :
    ∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      (∀ᵐ x ∂mu, (1 : ℝ) / 2 ≤ 1 + e * f x) ∧
      IsProbabilityMeasure (mu.withDensity (fun x => ENNReal.ofReal (1 + e * f x))) ∧
      _root_.InformationTheory.klDiv
        (mu.withDensity (fun x => ENNReal.ofReal (1 + e * f x))) mu =
        ENNReal.ofReal (∫ x, _root_.InformationTheory.klFun (1 + e * f x) ∂mu) := by
  have hfi : Integrable f mu := (integrable_const |M|).mono' hf (by
    filter_upwards [hbound] with x hx
    simpa only [Real.norm_eq_abs] using hx.trans (le_abs_self M))
  have hsmall : ∀ᶠ e : ℝ in 𝓝 (0 : ℝ), |e| * |M| < 1 / 2 :=
    (isOpen_lt (continuous_abs.mul continuous_const) continuous_const).mem_nhds (by norm_num)
  filter_upwards [hsmall] with e he
  let p : X → ℝ := fun x => 1 + e * f x
  let nu := mu.withDensity (fun x => ENNReal.ofReal (p x))
  have hp : AEStronglyMeasurable p mu := aestronglyMeasurable_const.add (hf.const_mul e)
  have hpI : Integrable p mu := (integrable_const 1).add (hfi.const_mul e)
  have hinterval : ∀ᵐ x ∂mu, p x ∈ Set.Icc ((1 : ℝ) / 2) (3 / 2) := by
    filter_upwards [hbound] with x hx
    have hprod : |e * f x| < 1 / 2 := by
      rw [abs_mul]
      exact (mul_le_mul_of_nonneg_left (hx.trans (le_abs_self M)) (abs_nonneg e)).trans_lt he
    obtain ⟨hlo, hhi⟩ := abs_lt.mp hprod
    constructor <;> dsimp [p] <;> linarith
  have hpos : ∀ᵐ x ∂mu, 0 ≤ p x := hinterval.mono fun _ hx => by linarith [hx.1]
  have hmass : (∫ x, p x ∂mu) = 1 := by
    rw [integral_add (integrable_const 1) (hfi.const_mul e), integral_const_mul, hcenter]
    simp
  have hprob : IsProbabilityMeasure nu := by
    constructor
    change mu.withDensity (fun x => ENNReal.ofReal (p x)) Set.univ = 1
    rw [withDensity_apply _ MeasurableSet.univ, Measure.restrict_univ,
      ← ofReal_integral_eq_lintegral_ofReal hpI hpos, hmass]
    norm_num
  let : IsProbabilityMeasure nu := hprob
  have hrn : (fun x => (nu.rnDeriv mu x).toReal) =ᵐ[mu] p := by
    filter_upwards [Measure.rnDeriv_withDensity₀ mu hp.aemeasurable.ennreal_ofReal, hpos]
      with x hx hxpos
    exact (congrArg ENNReal.toReal hx).trans (ENNReal.toReal_ofReal hxpos)
  obtain ⟨B, hB⟩ := (isCompact_Icc : IsCompact (Set.Icc ((1 : ℝ) / 2) (3 / 2))).exists_bound_of_continuousOn
    _root_.InformationTheory.continuous_klFun.continuousOn
  have hq : Integrable (fun x => _root_.InformationTheory.klFun (p x)) mu :=
    (integrable_const B).mono'
      (_root_.InformationTheory.continuous_klFun.comp_aestronglyMeasurable hp)
      (hinterval.mono fun x hx => hB (p x) hx)
  have hqRN : Integrable (fun x => _root_.InformationTheory.klFun (nu.rnDeriv mu x).toReal) mu :=
    hq.congr (hrn.mono fun x hx => congrArg _root_.InformationTheory.klFun hx.symm)
  have hac : nu ≪ mu := withDensity_absolutelyContinuous mu _
  have hllr := (_root_.InformationTheory.integrable_klFun_rnDeriv_iff hac).mp hqRN
  refine ⟨hinterval.mono fun _ hx => hx.1, hprob, ?_⟩
  rw [_root_.InformationTheory.klDiv_eq_integral_klFun, if_pos ⟨hac, hllr⟩]
  congr 1
  exact integral_congr_ae (hrn.mono fun x hx => congrArg _root_.InformationTheory.klFun hx)

end AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw
