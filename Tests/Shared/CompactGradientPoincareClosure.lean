import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactGradientPoincareClosure
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain

open MeasureTheory InnerProductSpace
open scoped ContDiff RealInnerProductSpace

namespace Tests.Shared.CompactGradientPoincareClosure

open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities

-- Construct the original closable Gibbs gradient and use the established
-- C¹ membership theorem. This is not an assumed graph-limit certificate.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 1 W) (hI : Integrable (fun x => Real.exp (-W x)))
    (C : ℝ) (hC : 0 < C)
    (hLSI : let μ := (volume : Measure E).tilted (fun x => -W x)
      ∀ v : E → ℝ, ContDiff ℝ ∞ v → HasCompactSupport v →
        (∫ x, (v x)^2 * Real.log ((v x)^2) ∂μ) -
          (∫ x, (v x)^2 ∂μ) * Real.log (∫ x, (v x)^2 ∂μ) ≤
        2 * C * ∫ x, ‖gradient v x‖^2 ∂μ)
    (f : E → ℝ) (hf : ContDiff ℝ 1 f) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    MemLp f 2 μ → MemLp (gradient f) 2 μ →
      (∫ x, (f x - ∫ y, f y ∂μ)^2 ∂μ) ≤ C * ∫ x, ‖gradient f x‖^2 ∂μ := by
  let μ := (volume : Measure E).tilted (fun x => -W x)
  let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  change MemLp f 2 μ → MemLp (gradient f) 2 μ → _
  intro hpf hq
  obtain ⟨D, _, hD, _, hgraph⟩ := WeightedGradient.compact_gradient_closable W hW hI
  have hpair := WeightedC1GradientDomain.c1_in_closed_gradient μ D hD hgraph hf hpf hq
  have hsets : (D.graph : Set (Lp ℝ 2 μ × Lp E 2 μ)) =
      {r | ∃ g : E → ℝ, ContDiff ℝ ∞ g ∧ HasCompactSupport g ∧
        r.1 =ᵐ[μ] g ∧ r.2 =ᵐ[μ] gradient g} := by
    ext ⟨a, b⟩
    exact hgraph a b
  rw [← hD.graph_closure_eq_closure_graph] at hpair
  change _ ∈ closure (D.graph : Set (Lp ℝ 2 μ × Lp E 2 μ)) at hpair
  rw [hsets] at hpair
  have h := CompactGradientPoincareClosure.poincare_of_compact_logSobolev_on_gradient_closure
    μ C hC hLSI _ hpair
  have hnorm : ‖hq.toLp (gradient f)‖^2 = ∫ x, ‖gradient f x‖^2 ∂μ := by
    rw [← real_inner_self_eq_norm_sq, L2.inner_def]
    apply integral_congr_ae
    filter_upwards [hq.coeFn_toLp] with x hx
    rw [hx, real_inner_self_eq_norm_sq]
  simpa only [ProbabilityTheory.variance_congr hpf.coeFn_toLp,
    ProbabilityTheory.variance_eq_integral hf.continuous.measurable.aemeasurable, hnorm] using h

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactGradientPoincareClosure.poincare_of_compact_logSobolev_on_gradient_closure

end Tests.Shared.CompactGradientPoincareClosure
