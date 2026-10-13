import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.ScaledClosedGraphResolvent
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolvent
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsGradientKernel
import Mathlib.MeasureTheory.Measure.SeparableMeasure
/-! Actual normalized Gibbs original-gradient centered resolvent norm limit. Derive true L1/kernel orthogonality and scalarL2 separability from the actual probability; construct actual positive-epsilon variational solutions, retain local ordinary weak-gradient facts and prove scaled residualzero. No curvature/Poincare/unscaled uniform bound/range/core certificate or fiber selector. -/
set_option autoImplicit false
noncomputable section
open Filter InnerProductSpace MeasureTheory
open scoped Topology RealInnerProductSpace ContDiff
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredGibbsResolventLimit
theorem gibbs_centered_resolvent_sequence
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∀ (D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ), D.IsClosable →
      (∀ (a : Lp ℝ 2 μ) (G : Lp E 2 μ), (a,G) ∈ D.graph ↔
        ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
          a =ᵐ[μ] φ ∧ G =ᵐ[μ] gradient φ) →
      ∀ f : Lp ℝ 2 μ, (∫ x, f x ∂μ)=0 →
      ∀ (ε : ℕ → ℝ), (∀ n, 0 < ε n) → Tendsto ε atTop (𝓝 0) →
      Integrable (fun x => f x) μ ∧
      ∃ u : ℕ → D.closure.domain,
        (∀ n, (∀ v : D.closure.domain,
          ε n*inner ℝ (u n : Lp ℝ 2 μ) (v : Lp ℝ 2 μ)+
            inner ℝ (D.closure (u n)) (D.closure v)=inner ℝ f (v : Lp ℝ 2 μ)) ∧
          LocallyIntegrable (fun x => (u n : Lp ℝ 2 μ) x) ∧
          LocallyIntegrable (fun x => D.closure (u n) x) ∧
          (∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ a : E,
            Integrable (fun x => ψ x*inner ℝ (D.closure (u n) x) a) ∧
            Integrable (fun x => (u n : Lp ℝ 2 μ) x*fderiv ℝ ψ x a) ∧
            (∫ x, ψ x*inner ℝ (D.closure (u n) x) a)=
              -∫ x, (u n : Lp ℝ 2 μ) x*fderiv ℝ ψ x a)) ∧
        Tendsto (fun n => ε n • (u n : Lp ℝ 2 μ)) atTop (𝓝 0) := by
  let μ := (volume : Measure E).tilted (fun x => -W x)
  dsimp only
  intro D hD hgraph f hf ε hε hε0
  letI : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  have hfi : Integrable (fun x => f x) μ := (Lp.memLp f).integrable (by norm_num)
  letI : Fact ((2 : ENNReal) ≠ ⊤) := ⟨by norm_num⟩
  letI : SecondCountableTopology (Lp ℝ 2 μ) := inferInstance
  have hsol (n : ℕ) :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolvent.weak_resolvent_distributional
      W hW hI D hD hgraph (ε n) (hε n) f
  let u (n : ℕ) : D.closure.domain := Classical.choose (hsol n)
  have hu (n : ℕ) := Classical.choose_spec (hsol n)
  refine ⟨hfi,u,?_,?_⟩
  · intro n
    exact ⟨(hu n).1,(hu n).2.1,(hu n).2.2.1,(hu n).2.2.2.1⟩
  · have hk : ∀ v : D.closure.domain, D.closure v=0 → inner ℝ f (v : Lp ℝ 2 μ)=0 := by
      intro v hv
      obtain ⟨c,hc⟩ :=
        AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsGradientKernel.closed_gradient_zero_ae_constant
          W hW hI D hD hgraph v hv
      rw [L2.inner_def]
      calc
        _ = ∫ x, f x*c ∂μ := integral_congr_ae (by
          filter_upwards [hc] with x hx
          simp [hx,mul_comm])
        _ = 0 := by rw [integral_mul_const,hf,zero_mul]

    exact (AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.ScaledClosedGraphResolvent.scaled_resolvent_sequence_tendsto_zero
      D.closure hD.closure_isClosed f ε hε hε0 u (fun n => (hu n).1) hk).1

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredGibbsResolventLimit
