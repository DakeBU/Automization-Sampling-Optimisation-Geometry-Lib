import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedLocalL2
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolvent

open MeasureTheory InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities
open scoped ContDiff Topology

#print axioms WeightedLocalL2.lp_locallyMemLp_volume

-- A genuine same-operator resolvent supplies u; local L2 is not a premise.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∃ D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ,
      D.IsClosable ∧ ∀ ε : ℝ, 0 < ε → ∀ f : Lp ℝ 2 μ,
        ∃ u : D.closure.domain,
          (∀ K : Set E, IsCompact K →
            MemLp (fun x => (u : Lp ℝ 2 μ) x) 2 (volume.restrict K) ∧
            MemLp (fun x => D.closure u x) 2 (volume.restrict K) ∧
            MemLp (fun x => f x) 2 (volume.restrict K)) ∧
          ∀ ψ : E → ℝ, ContDiff ℝ ∞ ψ → HasCompactSupport ψ →
            ε * (∫ x, Real.exp (-W x) * ((u : Lp ℝ 2 μ) x * ψ x)) +
              (∫ x, Real.exp (-W x) * inner ℝ (D.closure u x) (gradient ψ x)) =
              ∫ x, Real.exp (-W x) * (f x * ψ x) := by
  obtain ⟨D, _, hD, _, hgraph⟩ := WeightedGradient.compact_gradient_closable W hW hI
  refine ⟨D, hD, ?_⟩
  intro ε hε f
  obtain ⟨u, _, _, _, _, hPDE⟩ :=
    WeightedResolvent.weak_resolvent_distributional W hW hI D hD hgraph ε hε f
  refine ⟨u, ?_, ?_⟩
  · intro K hK
    exact ⟨(WeightedLocalL2.lp_locallyMemLp_volume W hW.continuous hI u.val).2 K hK,
      (WeightedLocalL2.lp_locallyMemLp_volume W hW.continuous hI (D.closure u)).2 K hK,
      (WeightedLocalL2.lp_locallyMemLp_volume W hW.continuous hI f).2 K hK⟩
  · intro ψ hψ hc
    exact (hPDE ψ hψ hc).2.2.2
