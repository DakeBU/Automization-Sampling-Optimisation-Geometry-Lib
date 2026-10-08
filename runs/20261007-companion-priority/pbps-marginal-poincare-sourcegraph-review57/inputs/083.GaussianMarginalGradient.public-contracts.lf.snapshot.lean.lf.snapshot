import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff Topology
noncomputable section
set_option autoImplicit false

theorem gaussian_marginal_gradient_closable
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) :
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
    let ν := J.snd
    ∃ D : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
      Dense (D.domain : Set (Lp ℝ 2 ν)) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
      ∀ (u : Lp ℝ 2 ν) (v : Lp E 2 ν), (u,v) ∈ D.graph ↔
        ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
          u =ᵐ[ν] f ∧ v =ᵐ[ν] gradient f 