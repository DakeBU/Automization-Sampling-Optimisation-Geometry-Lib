import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability
import AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.Tactic

/-!
# The actual source smoothed Gibbs potential

Chen, Chewi, Lu and Zhang, arXiv:2609.06906v1, equation1.1 and Section3.1:
<https://arxiv.org/html/2609.06906v1#S3.SS1>.
The source defines the UNNORMALIZED convolution exp(-V_eta). Its partition is
derived to equal the original positive Z_V, and the actual Gaussian add-noise
law is the Gibbs law of this source potential. The normalized negative-log
density differs by log Z_V; no literal equality of the two potentials is used.
Only the genuine positive lower Hessian and source C2 are required. The source
upper Hessian and eta cap are not needed, including the zero-dimensional case.
Score/covariance, curvature/higher estimates, stationarity, accuracy, query work
and both main/composition results remain separate.
-/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential

open MeasureTheory ProbabilityTheory
noncomputable section
set_option backward.isDefEq.respectTransparency false
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The actual source unnormalized smoothed Gibbs potential has preserved
partition and genuine smoothed Gibbs law. Regularity and normalization are
derived from the original Hessian hypotheses, not supplied certificates. -/
theorem smoothed_gibbs_potential {V : E → ℝ} {α η : ℝ} (hα : 0 < α) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, α*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v) (hη : 0 < η) :
    let ZV := ∫ x, Real.exp (-V x) ∂(volume : Measure E)
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
    let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
    0 < ZV ∧ IsProbabilityMeasure μ ∧
      (μ.prod (stdGaussian E)).map (fun p => p.1+Real.sqrt η • p.2) =
        (volume : Measure E).withDensity
          (fun y => ENNReal.ofReal (Real.exp (-(-Real.log (A y)))/ZV)) ∧
      Integrable A (volume : Measure E) ∧
      (∫ y, A y ∂(volume : Measure E)) = ZV ∧
      (μ.prod (stdGaussian E)).map (fun p => p.1+Real.sqrt η • p.2) =
        (volume : Measure E).tilted (fun y => -(-Real.log (A y))) ∧
      (∀ y, 0 < A y) ∧
      ContDiff ℝ 2 (fun y => -Real.log (A y)) ∧
      ∀ y, -Real.log (C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ) =
        -Real.log (A y)+Real.log ZV 