import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalBochner
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient

/-!
# Dense closable gradient for the actual PBPS conditional law

Analytic prerequisite to arXiv:2609.06905v1 Appendix C.1. The same common
conditional kernels retain their disintegration, reflection and normalized
density. The genuine C2 conditional potential and positive normalizer supply
the shared weighted-gradient construction, without any new paper hypothesis.
Inherited alpha<=beta and beta eta<=1 restrictions belong to the parent kernel
interface; the abstract gradient closure needs no curvature bound.
No generator operator core, resolvent regularity, Poincare, noncompact score
bound or complete-paper conclusion is asserted.
-/

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradient

open MeasureTheory ProbabilityTheory InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities
open scoped ContDiff NNReal RealInnerProductSpace Topology

/-- The actual conditional Gibbs gradient has a dense smooth compact domain
and a single-valued closed graph extension. The displayed graph equivalence
fixes the genuine gradient, not an arbitrary abstract closable operator. -/
theorem conditional_gradient_closable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : NNReal} {η : ℝ}
    (hα : 0 < (α:ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (α:ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β:ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β:ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2)) (μ.prod (stdGaussian E))
    let W := fun y u : E => V ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y = (volume : Measure E).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ Integrable (fun u => Real.exp (-W y u)) ∧
        0 < (∫ u, Real.exp (-W y u)) ∧
        ∃ D : Lp ℝ 2 (S y) →ₗ.[ℝ] Lp E 2 (S y),
          Dense (D.domain : Set (Lp ℝ 2 (S y))) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
          ∀ (u : Lp ℝ 2 (S y)) (v : Lp E 2 (S y)), (u,v) ∈ D.graph ↔
            ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
              u =ᵐ[S y] f ∧ v =ᵐ[S y] gradient f := by
  obtain ⟨R,S,hR,hS,hcond,hSR,hfiber⟩ :=
    ConditionalBochner.conditional_bochner_energy hα hαβ hV hH hη hβη
  dsimp only
  refine ⟨R,S,hR,hS,hcond,hSR,?_⟩
  intro y
  obtain ⟨hSy,hW,hI,hZ,_⟩ := hfiber y
  refine ⟨hSy,hW,hI,hZ,?_⟩
  rw [hSy]
  exact WeightedGradient.compact_gradient_closable _ (hW.of_le (by norm_num)) hI

end AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradient
