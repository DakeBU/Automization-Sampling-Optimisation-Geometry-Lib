import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientDistribution

#check AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientDistribution.closed_gradient_distributional
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientDistribution.closed_gradient_distributional

open MeasureTheory InnerProductSpace
open scoped ContDiff Topology

-- The actual constructed weighted gradient acquires an ordinary weak derivative.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∃ D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ,
      D.IsClosable ∧ ∀ u : D.closure.domain,
        LocallyIntegrable (fun x => (u : Lp ℝ 2 μ) x) ∧
        LocallyIntegrable (fun x => D.closure u x) ∧
        ∀ (ψ : E → ℝ), ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ v : E,
          Integrable (fun x => ψ x * inner ℝ (D.closure u x) v) ∧
          Integrable (fun x => (u : Lp ℝ 2 μ) x * fderiv ℝ ψ x v) ∧
          (∫ x, ψ x * inner ℝ (D.closure u x) v) =
            - ∫ x, (u : Lp ℝ 2 μ) x * fderiv ℝ ψ x v := by
  obtain ⟨D,_,hD,_,hgraph⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient.compact_gradient_closable W hW hI
  refine ⟨D,hD,?_⟩
  intro u
  exact AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientDistribution.closed_gradient_distributional
    W hW hI D hD hgraph u (D.closure u) (D.closure.mem_graph u)
