import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsGradientKernelEquality
import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientKernel
import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreDomain
/-! Actual PBPS common J/R/S and SAME original dense closable gradient before ALL constants/domain elements/directions. Produce constant domain/full kernel and the actual unnormalized parameter-y directional score in that SAME graph, using its genuine C1/L2/bounded-gradient producer and ONLY explicit reflected-density equality. Auxiliary R2/R kernels and separately chosen operators are never identified. SourceC2 alpha/beta eta cap/positive partitions/dimension0 retained; Poincare/main/composition remain open. -/
set_option autoImplicit false
noncomputable section
open MeasureTheory Filter InnerProductSpace
open scoped Topology RealInnerProductSpace ContDiff
open ProbabilityTheory
open scoped NNReal
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreClosedDomain
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
theorem conditional_score_closed_gradient_domain
    {V : E → ℝ} {α β : NNReal} {η : ℝ}
    (hα : 0 < (α:ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (α:ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β:ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β:ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2)) (μ.prod (stdGaussian E))
    let W := fun y u : E => V ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
    let s := fun y u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
      (1/(4*η)) • innerSL ℝ (y-u)
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y = (volume : Measure E).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ Integrable (fun u => Real.exp (-W y u)) ∧
        0 < (∫ u, Real.exp (-W y u)) ∧
        ∃ D : Lp ℝ 2 (S y) →ₗ.[ℝ] Lp E 2 (S y),
          Dense (D.domain : Set (Lp ℝ 2 (S y))) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
          (∀ (u : Lp ℝ 2 (S y)) (v : Lp E 2 (S y)), (u,v) ∈ D.graph ↔
            ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
              u =ᵐ[S y] f ∧ v =ᵐ[S y] gradient f) ∧
          (∀ c : ℝ, ∃ u : D.closure.domain,
            (u : Lp ℝ 2 (S y)) =ᵐ[S y] (fun _ => c) ∧ D.closure u=0) ∧
          (∀ u : D.closure.domain, D.closure u=0 ↔
            ∃ c : ℝ, (u : Lp ℝ 2 (S y)) =ᵐ[S y] (fun _ => c)) ∧
          ∀ a : E, ContDiff ℝ 1 (fun u => s y u a) ∧
            (∀ u, ‖gradient (fun z => s y z a) u‖ ≤ ((1/η-(α:ℝ))/4)*‖a‖) ∧
            ∃ hp : MemLp (fun u => s y u a) 2 (S y),
              ∃ hq : MemLp (gradient (fun u => s y u a)) 2 (S y),
                (hp.toLp _,hq.toLp _) ∈ D.closure.graph := by
  obtain ⟨R,S,hR,hS,hcond,hSR,hfiber⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientKernel.conditional_gradient_zero_ae_constant
      hα hαβ hV hH hη hβη
  obtain ⟨R2,S2,_,_,_,_,hfiber2⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreDomain.conditional_curvature_and_score_domain
      hα hαβ hV hH hη hβη
  dsimp only
  refine ⟨R,S,hR,hS,hcond,hSR,?_⟩
  intro y
  obtain ⟨hSy,hW,hI,hZ,D,hd,hD,hDc,hgraph,_⟩ := hfiber y
  obtain ⟨hS2y,_,_,_,_,_,hscore⟩ := hfiber2 y
  have hmeas : S2 y=S y := hS2y.trans hSy.symm
  let : IsMarkovKernel S := hS
  refine ⟨hSy,hW,hI,hZ,D,hd,hD,hDc,hgraph,?_,?_,?_⟩
  · intro c
    exact AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain.constants_in_closed_gradient (S y) D hD hgraph c
  · have hk := AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsGradientKernelEquality.closed_gradient_zero_iff_ae_constant _ (hW.of_le (by norm_num)) hI
    rw [← hSy] at hk
    exact hk D hD hgraph
  · intro a
    obtain ⟨hqa,hpa,_,hga⟩ := hscore a
    rw [hmeas] at hpa
    have hq : MemLp (gradient (fun u =>
        (-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
          (1/(4*η)) • innerSL ℝ (y-u)) a)) 2 (S y) :=
      MemLp.of_bound ((toDual ℝ E).symm.continuous.comp
        (hqa.continuous_fderiv one_ne_zero)).aestronglyMeasurable _ (Eventually.of_forall hga)
    exact ⟨hqa,hga,hpa,hq,AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain.c1_in_closed_gradient (S y) D hD hgraph hqa hpa hq⟩

end AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreClosedDomain
