import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy
import AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain

/-!
# The literal PBPS source mean in the actual closed-gradient domain

Source-specific analytic integration for PBPS arXiv:2609.06905v1 Appendix C.1,
its smooth compact reduction and C.2 estimate toward B.13. The original C2
potential, two-sided Hessian bounds, capped positive step and signed smooth
compact observer are retained. Finite real Hilbert spaces and rank zero are
explicit background extensions. The operator is the actual compact-gradient
core on the second marginal of the same independent Gaussian augmentation.

The source mean need not have compact support. Genuine L2 mean and gradient
bounds, whole-function C1 regularity and the uniform closable core are produced
internally. This closes its canonical graph pair only; equivalence to a separate
weak H1 definition, the all-L2 limit, B.13, Gamma, dynamics, main results,
implementation errors and query costs remain separate obligations.
-/

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain

open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology

noncomputable section
set_option autoImplicit false

theorem literal_source_mean_in_closed_gradient
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    let S := fun y : E => (volume : Measure E).tilted
      (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
    IsProbabilityMeasure ν ∧
      ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
        Dense (G.domain : Set (Lp ℝ 2 ν)) ∧ G.IsClosable ∧ G.closure.IsClosed ∧
        (∀ (u : Lp ℝ 2 ν) (v : Lp E 2 ν), (u,v) ∈ G.graph ↔
          ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
            u =ᵐ[ν] φ ∧ v =ᵐ[ν] gradient φ) ∧
        ∀ f : E → ℝ, ContDiff ℝ ∞ f → HasCompactSupport f →
          let Tf := fun y : E => ∫ u, f u ∂S y
          ∃ hTf : MemLp Tf 2 ν, ∃ hGrad : MemLp (gradient Tf) 2 ν,
            (hTf.toLp Tf,hGrad.toLp (gradient Tf)) ∈ G.closure.graph := by
  classical
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let S := fun y : E => (volume : Measure E).tilted
    (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
  obtain ⟨hμ,hJ,hν,R,S₀,hR,hS₀,hcond,hSR,hSd,hΛcond,hfst,
    U,hU,hUi,hUs,hBB,hBD,hblock,henergy⟩ :=
    MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks hα hαβ hV hH hη hβη
  letI : IsProbabilityMeasure μ := hμ
  letI : IsProbabilityMeasure ν := hν
  obtain ⟨G,hDense,hClosable,hClosed,hGraph⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient.
      gaussian_marginal_gradient_closable μ hη
  refine ⟨hν,G,hDense,hClosable,hClosed,hGraph,?_⟩
  intro f hf hfc
  let Tf := fun y : E => ∫ u, f u ∂S y
  have hsame : (fun y : E => ∫ u, f u ∂S₀ y) = Tf := by
    funext y
    exact congrArg (fun m : Measure E => ∫ u, f u ∂m) (hSd y)
  obtain ⟨_,_,hTf₀,hGrad₀,_,_⟩ := henergy f hf hfc
  have hTf : MemLp Tf 2 ν := by simpa only [hsame] using hTf₀
  have hGrad : MemLp (gradient Tf) 2 ν := by simpa only [hsame] using hGrad₀
  have hf1 : ContDiff ℝ 1 f := hf.of_le (by simp)
  obtain ⟨_,hC1⟩ := LiteralReflectedMean.reflected_gibbs_mean_c1
    hα hV (fun x v => (hH x v).1) hη hf1 hfc
  change ContDiff ℝ 1 Tf at hC1
  refine ⟨hTf,hGrad,?_⟩
  exact AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain.
    c1_in_closed_gradient ν G hClosable hGraph hC1 hTf hGrad

end AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain
