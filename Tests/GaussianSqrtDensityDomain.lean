import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianSqrtDensityDomain
import Mathlib.Analysis.InnerProductSpace.PiL2

noncomputable section
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped RealInnerProductSpace NNReal
open AutoSamplingTheory.TechnicalLemmas.Measure.GaussianSqrtDensityDomain
namespace Tests.GaussianSqrtDensityDomain

-- Zero smoothness is legal, including on the zero dimensional Hilbert space.
-- The true tilt, normalized density and Dirichlet energy are all evaluated.
theorem zero_residual {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
    (stdGaussian E).tilted (fun _ => (0 : ℝ))=stdGaussian E ∧
      (∫ _ : E, (1 : ℝ) ∂stdGaussian E)=1 ∧
      MemLp (fun _ : E => (1 : ℝ)) 2 (stdGaussian E) ∧
      (∫ u : E, ‖gradient (fun _ : E => (1 : ℝ)) u‖^2 ∂stdGaussian E)=0 := by
  have hh : ∀ u v : E, 0 ≤ fderiv ℝ (fderiv ℝ (fun _ : E => (0 : ℝ))) u v v ∧
      fderiv ℝ (fderiv ℝ (fun _ : E => (0 : ℝ))) u v v ≤ ((0 : ℝ≥0):ℝ)*‖v‖^2 := by
    intro u v
    simp
  obtain ⟨_hZ,_hZone,_hvol,_hdensity,_hprob,_hfq,hqone,_hf,hflp,
      _hfg,_hρg,_he,_hdf,_hlog,henergy⟩ := gaussian_sqrt_density_domain
      contDiff_const rfl (by simp) hh
  refine ⟨by simp,?_,?_,?_⟩
  · simpa using hqone
  · simpa using hflp
  · simpa using henergy

abbrev E0 := EuclideanSpace ℝ (Fin 0)
theorem zero_dimension_zero_residual :
    (stdGaussian E0).tilted (fun _ => (0 : ℝ))=stdGaussian E0 ∧
      (∫ _ : E0, (1 : ℝ) ∂stdGaussian E0)=1 ∧
      MemLp (fun _ : E0 => (1 : ℝ)) 2 (stdGaussian E0) ∧
      (∫ u : E0, ‖gradient (fun _ : E0 => (1 : ℝ)) u‖^2 ∂stdGaussian E0)=0 :=
  zero_residual

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.GaussianSqrtDensityDomain.gaussian_sqrt_density_domain
#print axioms zero_residual
#print axioms zero_dimension_zero_residual
end Tests.GaussianSqrtDensityDomain
