import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolvent

#check AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolvent.weak_resolvent_distributional
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolvent.weak_resolvent_distributional

open MeasureTheory InnerProductSpace
open scoped ContDiff Topology

-- Construct the operator first, then solve every forcing/epsilon in its SAME closure.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∃ D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ,
      D.IsClosable ∧ ∀ ε : ℝ, 0 < ε → ∀ f : Lp ℝ 2 μ,
        ∃ u : D.closure.domain, ∀ ψ : E → ℝ,
          ContDiff ℝ ∞ ψ → HasCompactSupport ψ →
          Integrable (fun x => Real.exp (-W x) * ((u : Lp ℝ 2 μ) x * ψ x)) ∧
          Integrable (fun x => Real.exp (-W x) * inner ℝ (D.closure u x) (gradient ψ x)) ∧
          Integrable (fun x => Real.exp (-W x) * (f x * ψ x)) ∧
          ε * (∫ x, Real.exp (-W x) * ((u : Lp ℝ 2 μ) x * ψ x)) +
            (∫ x, Real.exp (-W x) * inner ℝ (D.closure u x) (gradient ψ x)) =
            ∫ x, Real.exp (-W x) * (f x * ψ x) := by
  obtain ⟨D,_,hD,_,hgraph⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient.compact_gradient_closable W hW hI
  refine ⟨D,hD,?_⟩
  intro ε hε f
  obtain ⟨u,_,_,_,_,hPDE⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolvent.weak_resolvent_distributional
      W hW hI D hD hgraph ε hε f
  exact ⟨u,hPDE⟩
