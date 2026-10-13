import AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment
import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential

/-!
# Actual smoothed Hessian upper bound

SPHMC arXiv:2609.06906v1 Section4.1 Lemma4.1, Cramer-Rao half.
The genuine quadratic posterior has Hessian between alpha+eta^-1 and
beta+eta^-1. Its derived covariance lower bound and the true Gaussian
posterior Hessian identity imply the source UNNORMALIZED V_eta has Hessian
at most beta/(1+beta eta). This gives exactly (1+eta)^-1 for source beta=1.
Generic alpha/beta and every eta>0 are explicit extensions of the source.
No moment, normalizer, derivative or covariance estimate is an input.
Brascamp-Lieb/Hessian lower, full Lemma4.1, higher regularity, numerical
accuracy/history/expected work and both complete main/composition remain open.
-/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedHessianUpper

open Set MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal
noncomputable section
set_option backward.isDefEq.respectTransparency false
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] [CompleteSpace E]

/-- Cramer-Rao half of SPHMC Lemma4.1 for the actual RGO posterior and
source unnormalized smoothed potential. Generic alpha/beta and all eta>0
are explicit generalizations; covariance upper/Hessian lower is separate. -/
theorem smoothed_hessian_upper {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0<α) (hαβ : α≤β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (α:ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ (β:ℝ)*‖v‖^2) (hη : 0<η) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
    let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
    let Vη := fun y => -Real.log (A y)
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    (∀ y v, ‖v‖^2/((β:ℝ)+η⁻¹) ≤ covarianceBilin (R y) v v) ∧
      ∀ y v, fderiv ℝ (fderiv ℝ Vη) y v v ≤ ((β:ℝ)/(1+(β:ℝ)*η))*‖v‖^2 