import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity

noncomputable section

namespace Tests.GaussianConvolutionRegularity

-- Singular input exercises the actual Gaussian law/density and source potential;
-- no input density or moment certificate is passed to the producer.
theorem actual_dirac_potential {η : ℝ} (hη : 0 < η) (x : ℝ) :
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ ℝ
    let Z := fun y : ℝ => ∫ z, Real.exp (-‖y-z‖^2/(2*η)) ∂Measure.dirac x
    ((Measure.dirac x).prod (stdGaussian ℝ)).map (fun p => p.1+Real.sqrt η • p.2) =
      (volume : Measure ℝ).withDensity (fun y => ENNReal.ofReal (C*Z y)) ∧
      ContDiff ℝ 2 (fun y => -Real.log (C*Z y)) := by
  have h := gaussian_convolution_potential_c2 (Measure.dirac x) hη
  exact ⟨h.1,h.2.2.2⟩

-- The same genuine normalizer supplies the smooth potential of the actual
-- Gaussian augmentation whose backward conditional law is already certified.
theorem actual_backward_law_and_potential (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {η : ℝ} (hη : 0 < η) :
    let J := (μ.prod (stdGaussian ℝ)).map (fun p => (p.1,p.1+Real.sqrt η • p.2))
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ ℝ
    let Z := fun y : ℝ => ∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ
    ∃ R : Kernel ℝ ℝ, IsMarkovKernel R ∧
      (∀ y, R y = μ.tilted (fun x => -‖x-y‖^2/(2*η))) ∧
      (J.map Prod.swap).IsCondKernel R ∧ ContDiff ℝ 2 (fun y => -Real.log (C*Z y)) := by
  obtain ⟨R,hR,hfiber,hcond⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
  exact ⟨R,hR,hfiber,hcond,(gaussian_convolution_potential_c2 μ hη).2.2.2⟩

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_potential_c2
#print axioms actual_dirac_potential
#print axioms actual_backward_law_and_potential

end Tests.GaussianConvolutionRegularity
