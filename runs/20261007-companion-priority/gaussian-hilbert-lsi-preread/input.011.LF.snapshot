import AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.Tactic.FunProp

/-!
# Explicit density of isotropic Gaussian noise

The Gaussian-density dependency of the equivalence between equations (2.6)
and (2.7) in arXiv:2609.06905v1, Section 2.2. This module only identifies the
scaled noise law with its canonical-volume density. The joint augmentation,
conditional laws, and PBPS process invariance are separate obligations.

The result holds in every finite dimension, including zero; no potential or
curvature hypothesis is needed. Positivity of the variance excludes the
positive-dimensional singular Dirac case.
-/

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal

namespace AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- Scaling the standard Gaussian by `sqrt η` gives the explicit isotropic
Gaussian density relative to the canonical volume measure of `E`. The inverse
square-root normalizer is raised to the natural-number dimension, so the
statement also includes the zero-dimensional space without a separate case. -/
theorem map_sqrt_smul_stdGaussian_eq_withDensity (η : ℝ) (hη : 0 < η) :
    (stdGaussian E).map (fun z : E => Real.sqrt η • z) =
      (volume : Measure E).withDensity (fun z =>
        ENNReal.ofReal
          (((Real.sqrt (2 * Real.pi * η))⁻¹) ^ Module.finrank ℝ E *
            Real.exp (-‖z‖ ^ 2 / (2 * η)))) := by
  classical
  let ι := Fin (Module.finrank ℝ E)
  let b := stdOrthonormalBasis ℝ E
  let v : ℝ≥0 := ⟨η, hη.le⟩
  have hvcoe : (v : ℝ) = η := rfl
  have hv : v ≠ 0 := by
    intro h
    have : η = 0 := congrArg (fun x : ℝ≥0 => (x : ℝ)) h
    exact hη.ne' this
  let e : (ι → ℝ) ≃ᵐ E :=
    (MeasurableEquiv.toLp 2 (ι → ℝ)).trans b.measurableEquiv.symm
  let T : (ι → ℝ) → (ι → ℝ) := fun x i => Real.sqrt η * x i
  have he (x : ι → ℝ) : e x = ∑ i, x i • b i := by
    exact (b.sum_repr_symm (WithLp.toLp 2 x)).symm
  have hstd : stdGaussian E =
      (Measure.pi (fun _ : ι => gaussianReal 0 1)).map e := by
    rw [stdGaussian_eq_map_pi_orthonormalBasis b]
    congr 1
    funext x
    exact (he x).symm
  have hcomm : (fun z : E => Real.sqrt η • z) ∘ e = e ∘ T := by
    funext x
    change Real.sqrt η • b.repr.symm (WithLp.toLp 2 x) =
      b.repr.symm (WithLp.toLp 2 (T x))
    rw [← map_smul]
    rfl
  have hscalar : (gaussianReal 0 1).map (fun t : ℝ => Real.sqrt η * t) =
      gaussianReal 0 v := by
    rw [gaussianReal_map_const_mul]
    congr 1
    · simp
    · apply NNReal.eq
      change (Real.sqrt η) ^ 2 * 1 = η
      rw [mul_one, Real.sq_sqrt hη.le]
  have hpi : (Measure.pi (fun _ : ι => gaussianReal 0 1)).map T =
      Measure.pi (fun _ : ι => gaussianReal 0 v) := by
    rw [Measure.pi_map_pi (fun _ => by fun_prop)]
    simp_rw [hscalar]
  have hscaled : (stdGaussian E).map (fun z : E => Real.sqrt η • z) =
      (Measure.pi (fun _ : ι => gaussianReal 0 v)).map e := by
    rw [hstd, Measure.map_map (by fun_prop) e.measurable, hcomm,
      ← Measure.map_map e.measurable (by fun_prop : Measurable T), hpi]
  have : IsProbabilityMeasure ((volume : Measure ℝ).withDensity (gaussianPDF 0 v)) := by
    rw [← gaussianReal_of_var_ne_zero 0 hv]
    infer_instance
  have hproduct : Measure.pi (fun _ : ι => gaussianReal 0 v) =
      (volume : Measure (ι → ℝ)).withDensity (fun x => ∏ i, gaussianPDF 0 v (x i)) := by
    rw [volume_pi, RadonNikodym.pi_withDensity_prod (fun _ => measurable_gaussianPDF 0 v)]
    simp_rw [← gaussianReal_of_var_ne_zero 0 hv]
  have hvol : (volume : Measure (ι → ℝ)).map e = (volume : Measure E) :=
    (b.measurePreserving_repr_symm.comp (PiLp.volume_preserving_toLp ι)).map_eq
  rw [hscaled, hproduct,
    RadonNikodym.measurableEquiv_map_withDensity e _ (by fun_prop), hvol]
  congr 1
  funext z
  have hnorm : (∑ i, ((e.symm z) i) ^ 2) = ‖z‖ ^ 2 := by
    rw [← EuclideanSpace.real_norm_sq_eq (WithLp.toLp 2 (e.symm z))]
    change ‖b.repr z‖ ^ 2 = ‖z‖ ^ 2
    rw [b.repr.norm_map]
  simp only [gaussianPDF_def, gaussianPDFReal, sub_zero]
  rw [← ENNReal.ofReal_prod_of_nonneg (fun _ _ => by positivity)]
  congr 1
  rw [Finset.prod_mul_distrib, Finset.prod_const, Finset.card_univ, ← Real.exp_sum]
  simp only [ι, Fintype.card_fin, hvcoe]
  congr 1
  congr 1
  rw [← Finset.sum_div, Finset.sum_neg_distrib, hnorm]

end AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity
