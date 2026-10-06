import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredGibbsResolventLimit
import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreClosedDomain
/-! Actual common Gaussian J/R/S and SAME original D_y before ALL meanzero forcing and positive epsilon sequences. Keep source C2 curvature/eta cap/reflected law/positive partitions; construct actual variational solutions and strong scaled residualzero. Fiberwise only: no jointselector/R2 identification/Poincare/BL/paper main or expectedcost composition. -/
set_option autoImplicit false
noncomputable section
open Filter InnerProductSpace MeasureTheory
open scoped Topology RealInnerProductSpace ContDiff
open ProbabilityTheory
open scoped NNReal
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalCenteredResolventLimit
theorem conditional_centered_resolvent_sequence
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : NNReal} {η : ℝ}
    (hα : 0 < (α:ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x a : E, (α:ℝ)*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ V) x a a ∧
      fderiv ℝ (fderiv ℝ V) x a a ≤ (β:ℝ)*‖a‖^2)
    (hη : 0 < η) (hβη : (β:ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2)) (μ.prod (stdGaussian E))
    let W := fun y u : E => V ((1/2:ℝ) • (y+u))+‖u-y‖^2/(8*η)
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y=(R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y=(volume : Measure E).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ Integrable (fun u => Real.exp (-W y u)) ∧
        0 < ∫ u, Real.exp (-W y u) ∧
        ∃ D : Lp ℝ 2 (S y) →ₗ.[ℝ] Lp E 2 (S y),
          Dense (D.domain : Set (Lp ℝ 2 (S y))) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
          (∀ (a : Lp ℝ 2 (S y)) (G : Lp E 2 (S y)), (a,G) ∈ D.graph ↔
            ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
              a =ᵐ[S y] φ ∧ G =ᵐ[S y] gradient φ) ∧
          ∀ f : Lp ℝ 2 (S y), (∫ x, f x ∂S y)=0 →
          ∀ (ε : ℕ → ℝ), (∀ n, 0 < ε n) → Tendsto ε atTop (𝓝 0) →
          ∃ u : ℕ → D.closure.domain,
            (∀ n, ∀ v : D.closure.domain,
              ε n*inner ℝ (u n : Lp ℝ 2 (S y)) (v : Lp ℝ 2 (S y))+
                inner ℝ (D.closure (u n)) (D.closure v)=inner ℝ f (v : Lp ℝ 2 (S y))) ∧
            Tendsto (fun n => ε n • (u n : Lp ℝ 2 (S y))) atTop (𝓝 0) := by
  obtain ⟨R,S,hR,hS,hcond,hSR,hfiber⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreClosedDomain.conditional_score_closed_gradient_domain
      hα hαβ hV hH hη hβη
  dsimp only
  refine ⟨R,S,hR,hS,hcond,hSR,?_⟩
  intro y
  obtain ⟨hSy,hW,hI,hZ,D,hd,hD,hDc,hgraph,_⟩ := hfiber y
  refine ⟨hSy,hW,hI,hZ,D,hd,hD,hDc,hgraph,?_⟩
  have hg := AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredGibbsResolventLimit.gibbs_centered_resolvent_sequence _ (hW.of_le (by norm_num)) hI
  rw [← hSy] at hg
  intro f hf ε hε hε0
  obtain ⟨_,u,hu,ht⟩ := hg D hD hgraph f hf ε hε hε0
  exact ⟨u,fun n => (hu n).1,ht⟩

end AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalCenteredResolventLimit
