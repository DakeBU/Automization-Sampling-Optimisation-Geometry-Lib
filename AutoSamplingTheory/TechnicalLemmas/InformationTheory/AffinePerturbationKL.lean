/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Samplinglib contributors
-/
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw
import Mathlib.Analysis.Asymptotics.Lemmas

/-!
# Second-order KL for bounded centered affine probability perturbations

This is the actual-law expansion in Chewi, *Log-Concave Sampling* (August 20,
2026), Exercise 1.7, (1.E.1), also used in Corollary 2.1.2. The probability
normalization and finiteness of extended-real KL are proved near zero before
the real-valued expansion is used. The proof reuses the actual-law identity
and the compensated-integral limit; it does not claim a transport or PI bound.
-/

set_option autoImplicit false
noncomputable section

open MeasureTheory Filter
open scoped Topology Asymptotics

namespace AutoSamplingTheory.TechnicalLemmas.InformationTheory.AffinePerturbationKL

open BoundedDensityPerturbation BoundedPerturbationLaw

/-- For a bounded centered observable, the actual affine perturbation of a
probability law is a probability with finite KL near zero. Its real KL differs
from `e ^ 2 * ((∫ f²) / 2)` by `o(e ^ 2)`, including the zero endpoint. -/
theorem klDiv_affine_perturbation_second_order
    {X : Type*} [MeasurableSpace X] (μ : Measure X) [IsProbabilityMeasure μ]
    (f : X → ℝ) (hf : AEStronglyMeasurable f μ) {M : ℝ}
    (hbound : ∀ᵐ x ∂μ, |f x| ≤ M) (hcenter : (∫ x, f x ∂μ) = 0) :
    let ν := fun e : ℝ => μ.withDensity (fun x => ENNReal.ofReal (1 + e * f x))
    (∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      IsProbabilityMeasure (ν e) ∧ _root_.InformationTheory.klDiv (ν e) μ < ⊤) ∧
    (fun e : ℝ => (_root_.InformationTheory.klDiv (ν e) μ).toReal -
      e ^ 2 * ((∫ x, f x ^ 2 ∂μ) / 2)) =o[𝓝 (0 : ℝ)] (fun e : ℝ => e ^ 2) := by
  let ν := fun e : ℝ => μ.withDensity (fun x => ENNReal.ofReal (1 + e * f x))
  let K := fun e : ℝ => (_root_.InformationTheory.klDiv (ν e) μ).toReal
  let Q := (∫ x, f x ^ 2 ∂μ) / 2
  let R := fun e : ℝ => K e - e ^ 2 * Q
  change (∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
    IsProbabilityMeasure (ν e) ∧ _root_.InformationTheory.klDiv (ν e) μ < ⊤) ∧
    R =o[𝓝 (0 : ℝ)] (fun e : ℝ => e ^ 2)
  have hlaw := eventually_isProbabilityMeasure_and_klDiv_eq_one_add_mul μ f hf hbound hcenter
  constructor
  · filter_upwards [hlaw] with e he
    refine ⟨he.2.1, ?_⟩
    dsimp only [ν]
    rw [he.2.2]
    exact ENNReal.ofReal_lt_top
  have hreal : ∀ᶠ e : ℝ in 𝓝 (0 : ℝ), K e =
      ∫ x, _root_.InformationTheory.klFun (1 + e * f x) ∂μ := by
    filter_upwards [hlaw] with e he
    dsimp only [K, ν]
    rw [he.2.2, ENNReal.toReal_ofReal]
    exact integral_nonneg_of_ae (he.1.mono fun x hx =>
      _root_.InformationTheory.klFun_nonneg (by linarith))
  have hnorm : Tendsto (fun e : ℝ => K e / e ^ 2) (𝓝[≠] (0 : ℝ)) (𝓝 Q) :=
    (tendsto_integral_klFun_one_add_mul_div_sq μ f hf hbound).congr'
      ((hreal.filter_mono nhdsWithin_le_nhds).mono fun e he =>
        congrArg (fun z : ℝ => z / e ^ 2) he.symm)
  have hRdiv : Tendsto (fun e : ℝ => R e / e ^ 2) (𝓝[≠] (0 : ℝ)) (𝓝 0) := by
    have hsub := hnorm.sub (tendsto_const_nhds (x := Q) (f := 𝓝[≠] (0 : ℝ)))
    rw [sub_self] at hsub
    apply hsub.congr'
    filter_upwards [self_mem_nhdsWithin] with e he
    have hne : e ≠ 0 := by simpa using he
    change K e / e ^ 2 - Q = (K e - e ^ 2 * Q) / e ^ 2
    rw [sub_div, mul_comm (e ^ 2) Q, mul_div_cancel_right₀ _ (pow_ne_zero 2 hne)]
  have hν0 : ν 0 = μ := by
    have hd : (fun x : X => ENNReal.ofReal (1 + (0 : ℝ) * f x)) = (1 : X → ENNReal) := by
      ext x
      simp
    change μ.withDensity (fun x => ENNReal.ofReal (1 + (0 : ℝ) * f x)) = μ
    rw [hd, withDensity_one]
  have hR0 : R 0 = 0 := by
    simp [R, K, hν0, _root_.InformationTheory.klDiv_self]
  apply Asymptotics.isLittleO_of_tendsto
  · intro e he
    have he0 : e = 0 := by
      by_contra hne
      exact (pow_ne_zero 2 hne) he
    simpa only [he0] using hR0
  · have hpure : Tendsto (fun e : ℝ => R e / e ^ 2) (pure (0 : ℝ)) (𝓝 0) := by
      apply tendsto_pure_left.mpr
      intro s hs
      simpa [hR0] using mem_of_mem_nhds hs
    simpa only [nhdsNE_sup_pure] using hRdiv.sup hpure

end AutoSamplingTheory.TechnicalLemmas.InformationTheory.AffinePerturbationKL
