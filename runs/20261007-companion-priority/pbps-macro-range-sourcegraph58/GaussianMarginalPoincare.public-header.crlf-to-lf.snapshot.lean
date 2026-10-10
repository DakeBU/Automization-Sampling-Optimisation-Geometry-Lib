import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredDomainPoincare
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsLinearCovarianceUpper
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedHessianUpper

/-!
# Actual centered Poincare for the Gaussian Gibbs marginal

PBPS arXiv:2609.06905v1 Eq2.13, D.6/D.10 and C.3. The positive C2
normalized marginal is derived from the actual Gibbs/Gaussian law. Posterior
covariance upper and the existing exact smoothed Hessian upper producer give
alpha/(1+alpha eta) and beta/(1+beta eta); all moment, partition and law
adapters are internal. Existing original-domain Poincare is consumed on one
genuine smooth-compact gradient closure selected before all centered inputs.
Original C2/two Hessian bounds and positive capped eta remain. Finite Hilbert,
Borel and rank0 are explicit extensions. This does not identify full weighted
H1, macro range, Gamma/inverses, dynamics, mixing, main results or query costs.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare
open Set MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology
noncomputable section
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false
set_option maxHeartbeats 1600000

theorem actual_gaussian_marginal_centered_poincare
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
    IsProbabilityMeasure ν ∧
      ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
        Dense (G.domain : Set (Lp ℝ 2 ν)) ∧ G.IsClosable ∧ G.closure.IsClosed ∧
        (∀ (u : Lp ℝ 2 ν) (v : Lp E 2 ν), (u,v) ∈ G.graph ↔
          ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
            u =ᵐ[ν] φ ∧ v =ᵐ[ν] gradient φ) ∧
        ∀ z : G.closure.domain,
          (∫ x, (z : Lp ℝ 2 ν) x ∂ν) = 0 →
          ((α : ℝ)/(1+(α : ℝ)*η))*‖(z : Lp ℝ 2 ν)‖^2 ≤ ‖G.closure z‖^2 