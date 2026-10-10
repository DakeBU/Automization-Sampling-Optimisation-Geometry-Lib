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
        -Real.log (A y)+Real.log ZV := by
  let ZV := ∫ x, Real.exp (-V x) ∂(volume : Measure E)
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
  let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
  have hi := AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn
    hα (hV.differentiable (by norm_num))
    (AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hV hH)
  have hZ : 0 < ZV := integral_exp_pos hi
  have : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hi
  have hc := AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_potential_c2 μ hη
  have he (y : E) : C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ = A y/ZV := by
    rw [show μ = (volume : Measure E).tilted (fun x => -V x) from rfl,integral_tilted]
    dsimp only [A,ZV]
    rw [show (C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E))/
        (∫ x, Real.exp (-V x) ∂(volume : Measure E)) =
      C*((∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E))/
        (∫ x, Real.exp (-V x) ∂(volume : Measure E))) by ring]
    congr 1
    rw [← integral_div]
    apply integral_congr_ae
    filter_upwards with x
    rw [smul_eq_mul,show Real.exp (-V x-‖y-x‖^2/(2*η)) =
      Real.exp (-V x)*Real.exp (-‖y-x‖^2/(2*η)) by
        rw [show -V x-‖y-x‖^2/(2*η) = -V x+(-‖y-x‖^2/(2*η)) by ring,Real.exp_add]]
    ring
  have hA (y : E) : 0 < A y :=
    (div_pos_iff_of_pos_right hZ).mp (he y ▸ hc.2.1 y)
  have hv (y : E) : -Real.log (C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ) =
      -Real.log (A y)+Real.log ZV := by
    rw [he,Real.log_div (hA y).ne' hZ.ne']; ring
  have hlaw : (μ.prod (stdGaussian E)).map (fun p => p.1+Real.sqrt η • p.2) =
      (volume : Measure E).withDensity (fun y => ENNReal.ofReal (A y/ZV)) := by
    convert hc.1 using 1
    congr 1
    funext y
    exact congrArg ENNReal.ofReal (he y).symm
  have hDcont : Continuous (fun y => A y/ZV) := by
    have hefun : (fun y => A y/ZV) =
        (fun y => C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ) :=
      funext (fun y => (he y).symm)
    rw [hefun]
    exact continuous_const.mul hc.2.2.1.continuous
  have hnonneg : ∀ y, 0 ≤ A y/ZV := fun y => (div_pos (hA y) hZ).le
  have : IsProbabilityMeasure ((μ.prod (stdGaussian E)).map
      (fun p => p.1+Real.sqrt η • p.2)) := Measure.isProbabilityMeasure_map (by fun_prop)
  have hm : ∫⁻ y, ENNReal.ofReal (A y/ZV) ∂(volume : Measure E) = 1 := by
    have hm := (congrArg (fun m : Measure E => m Set.univ) hlaw).symm
    simpa only [withDensity_apply _ MeasurableSet.univ,setLIntegral_univ,
      measure_univ] using hm
  have hiD : Integrable (fun y => A y/ZV) (volume : Measure E) :=
    (lintegral_ofReal_ne_top_iff_integrable hDcont.aestronglyMeasurable
      (Filter.Eventually.of_forall hnonneg)).mp (by rw [hm]; exact ENNReal.one_ne_top)
  have hIntD : (∫ y, A y/ZV ∂(volume : Measure E)) = 1 := by
    have hp := ofReal_integral_eq_lintegral_ofReal hiD (Filter.Eventually.of_forall hnonneg)
    rw [hm] at hp
    have ht := congrArg ENNReal.toReal hp
    simpa only [ENNReal.toReal_ofReal (integral_nonneg hnonneg),ENNReal.toReal_one] using ht
  have hiA : Integrable A (volume : Measure E) := by
    convert hiD.mul_const ZV using 1
    funext y
    exact (div_mul_cancel₀ (A y) hZ.ne').symm
  have hIntA : (∫ y, A y ∂(volume : Measure E)) = ZV := by
    rw [integral_div] at hIntD
    simpa only [one_mul] using (div_eq_iff hZ.ne').mp hIntD
  have hTilt : (μ.prod (stdGaussian E)).map (fun p => p.1+Real.sqrt η • p.2) =
      (volume : Measure E).tilted (fun y => -(-Real.log (A y))) := by
    rw [Measure.tilted]
    simp_rw [neg_neg,Real.exp_log (hA _)]
    rw [hIntA]
    exact hlaw
  refine ⟨hZ,inferInstance,?_,hiA,hIntA,hTilt,hA,?_,hv⟩
  · change (μ.prod (stdGaussian E)).map (fun p => p.1+Real.sqrt η • p.2) =
      (volume : Measure E).withDensity (fun y => ENNReal.ofReal (Real.exp (-(-Real.log (A y)))/ZV))
    convert hlaw using 1
    congr 1
    funext y
    rw [neg_neg,Real.exp_log (hA y)]
  have hg : (fun y => -Real.log (A y)) =
      (fun y => -Real.log (C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ)-Real.log ZV) := by
    funext y; rw [hv]; ring
  rw [hg]
  exact hc.2.2.2.sub contDiff_const

end
end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential
