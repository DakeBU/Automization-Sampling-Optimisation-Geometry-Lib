import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientWeak

#check AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientWeak.closed_gradient_weighted_ibp
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientWeak.closed_gradient_weighted_ibp

open MeasureTheory InnerProductSpace
open scoped ContDiff Topology

-- Consume the real constructor, then apply the new identity on its same closure.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∃ D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ,
      D.IsClosable ∧ ∀ u : D.closure.domain,
      ∀ (φ : E → ℝ), ContDiff ℝ 1 φ → HasCompactSupport φ → ∀ v : E,
        Integrable (fun x => φ x * inner ℝ (D.closure u x) v) μ ∧
        Integrable (fun x => (u : Lp ℝ 2 μ) x *
          (fderiv ℝ φ x v - φ x * fderiv ℝ W x v)) μ ∧
        (∫ x, φ x * inner ℝ (D.closure u x) v ∂μ) =
          - ∫ x, (u : Lp ℝ 2 μ) x * (fderiv ℝ φ x v - φ x * fderiv ℝ W x v) ∂μ := by
  obtain ⟨D,_,hD,_,hgraph⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient.compact_gradient_closable W hW hI
  refine ⟨D,hD,?_⟩
  intro u φ hφ hc v
  exact AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientWeak.closed_gradient_weighted_ibp
    W hW hI D hD hgraph u (D.closure u) (D.closure.mem_graph u) φ hφ hc v
