import AutoSamplingTheory.TechnicalLemmas.InformationTheory.AffinePerturbationKL
import Mathlib.Analysis.Calculus.ContDiff.Basic

open MeasureTheory Filter
open scoped Topology ContDiff Asymptotics

namespace Tests.Shared.AffinePerturbationKL

open AutoSamplingTheory.TechnicalLemmas.InformationTheory.AffinePerturbationKL

-- Specialize to the actual compact smooth test in (1.E.1) without supplying
-- the a.e. bound or measurability. Recover the positive-sided quotient used
-- in Corollary 2.1.2, without claiming its transport inequality.
example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ]
    (f : E → ℝ) (hf : ContDiff ℝ ∞ f) (hs : HasCompactSupport f)
    (hcenter : (∫ x, f x ∂μ) = 0) :
    let ν := fun e : ℝ => μ.withDensity (fun x => ENNReal.ofReal (1 + e * f x))
    (∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      IsProbabilityMeasure (ν e) ∧ InformationTheory.klDiv (ν e) μ < ⊤) ∧
    Tendsto (fun e : ℝ => (InformationTheory.klDiv (ν e) μ).toReal / e ^ 2)
      (𝓝[>] (0 : ℝ)) (𝓝 ((∫ x, f x ^ 2 ∂μ) / 2)) := by
  obtain ⟨B, hB⟩ := hs.isCompact.exists_bound_of_continuousOn hf.continuous.continuousOn
  have hb (x : E) : |f x| ≤ |B| := by
    by_cases hx : x ∈ tsupport f
    · exact (by simpa only [Real.norm_eq_abs] using hB x hx : |f x| ≤ B).trans (le_abs_self B)
    · simp [image_eq_zero_of_notMem_tsupport hx]
  let ν := fun e : ℝ => μ.withDensity (fun x => ENNReal.ofReal (1 + e * f x))
  let K := fun e : ℝ => (InformationTheory.klDiv (ν e) μ).toReal
  let Q := (∫ x, f x ^ 2 ∂μ) / 2
  obtain ⟨hprob, hsmall⟩ := klDiv_affine_perturbation_second_order
    μ f hf.continuous.aestronglyMeasurable (ae_of_all μ hb) hcenter
  refine ⟨hprob, ?_⟩
  change Tendsto (fun e => K e / e ^ 2) (𝓝[>] (0 : ℝ)) (𝓝 Q)
  have hR : Tendsto (fun e : ℝ => (K e - e ^ 2 * Q) / e ^ 2)
      (𝓝[>] (0 : ℝ)) (𝓝 0) := hsmall.tendsto_div_nhds_zero.mono_left nhdsWithin_le_nhds
  have hsum := hR.add (tendsto_const_nhds (x := Q) (f := 𝓝[>] (0 : ℝ)))
  rw [zero_add] at hsum
  apply hsum.congr'
  filter_upwards [self_mem_nhdsWithin] with e he
  have hne : e ≠ 0 := ne_of_gt he
  change (K e - e ^ 2 * Q) / e ^ 2 + Q = K e / e ^ 2
  rw [sub_div, mul_comm (e ^ 2) Q, mul_div_cancel_right₀ _ (pow_ne_zero 2 hne), sub_add_cancel]

#print axioms AutoSamplingTheory.TechnicalLemmas.InformationTheory.AffinePerturbationKL.klDiv_affine_perturbation_second_order

end Tests.Shared.AffinePerturbationKL
