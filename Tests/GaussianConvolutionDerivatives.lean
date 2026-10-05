import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import Mathlib.Tactic

namespace Tests.GaussianConvolutionDerivatives
open MeasureTheory ProbabilityTheory
noncomputable section
set_option backward.isDefEq.respectTransparency false
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

-- Actual source unnormalized potential and the same augmentation's selected
-- backward kernel, with original Gibbs probability and moments derived.
theorem actual_source_score_covariance {V : E → ℝ} {α η : ℝ}
    (hα : 0 < α) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, α*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v) (hη : 0 < η) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
    let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
    let Vη := fun y => -Real.log (A y)
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    let J := (μ.prod (stdGaussian E)).map (fun p => (p.1,p.1+Real.sqrt η • p.2))
    (∀ y, MemLp (fun x : E => x) 2 (R y)) ∧
      (∀ y v, fderiv ℝ Vη y v = inner ℝ (y-∫ x, x ∂(R y)) v/η) ∧
      (∀ y v w, fderiv ℝ (fderiv ℝ Vη) y v w =
        inner ℝ v w/η - covarianceBilin (R y) v w/η^2) ∧
      ∃ Q : Kernel E E, IsMarkovKernel Q ∧ (∀ y, Q y = R y) ∧
        (J.map Prod.swap).IsCondKernel Q := by
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
  let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
  let Vη := fun y => -Real.log (A y)
  let U := fun y : E => -Real.log (C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ)
  let ZV := ∫ x, Real.exp (-V x) ∂(volume : Measure E)
  obtain ⟨_hZ,hμ,_hlaw,_hI,_hInt,_hTilt,_hA,_hC2,hshift⟩ :=
    AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential.smoothed_gibbs_potential
      hα hV hH hη
  haveI : IsProbabilityMeasure μ := hμ
  have hC : 0 < C := by dsimp only [C]; positivity
  obtain ⟨hR,hD,hDD⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_derivatives
      μ hη hC
  have he : U = fun y => Vη y+Real.log ZV := funext hshift
  have hd : fderiv ℝ U = fderiv ℝ Vη := by
    rw [he]
    funext y
    exact fderiv_add_const _
  change ∀ y v, fderiv ℝ U y v = _ at hD
  change ∀ y v w, fderiv ℝ (fderiv ℝ U) y v w = _ at hDD
  rw [hd] at hD hDD
  obtain ⟨Q,hQ,hfiber,hcond⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
  exact ⟨fun y => (hR y).2,hD,hDD,Q,hQ,hfiber,hcond⟩

#print axioms actual_source_score_covariance
#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_derivatives

end
end Tests.GaussianConvolutionDerivatives
