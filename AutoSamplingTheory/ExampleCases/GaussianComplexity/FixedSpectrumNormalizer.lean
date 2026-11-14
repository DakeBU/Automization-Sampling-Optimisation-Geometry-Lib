import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDeterminant
import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity

open Matrix MeasureTheory ProbabilityTheory
open scoped BigOperators
set_option autoImplicit false

/-!
# Actual fixed-spectrum Gaussian normalizing integral

Zhou--Suzuki, arXiv:2610.20492v1, Eq11 and Appendix C.4 Gaussian integration.
The source normalizer is interpreted as the actual unweighted Euclidean
Lebesgue mass, a disclosed source-implicit standard convention. Integrability
and the explicit value are outputs, derived from source inputs only.
Existing canonical precision admissibility, determinant and Gaussian density
nodes are reused; no new Gaussian constructor or normalization certificate.
Full C.4 calculus/minimizer, moments/Krylov, actual adaptive/oracle/precision/TV/
cost adapters and both complete main lower bounds remain separate.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumNormalizer
theorem actual_normalizing_integral {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let diagonalValue : Fin d → ℝ := fun i =>
    (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Matrix.diagonal diagonalValue *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let weight : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    Real.exp (- (∑ i : Fin d, x.ofLp i * (A.mulVec x.ofLp) i) / 2)
  Integrable weight (volume : Measure (EuclideanSpace ℝ (Fin d))) ∧
    (∫ x : EuclideanSpace ℝ (Fin d), weight x ∂volume) =
      (2 * Real.pi) ^ ((d : ℝ) / 2) / Real.sqrt (∏ i : Fin d, diagonalValue i) := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let diagonalValue : Fin d → ℝ := fun i =>
    (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Matrix.diagonal diagonalValue *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let weight : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    Real.exp (- (∑ i : Fin d, x.ofLp i * (A.mulVec x.ofLp) i) / 2)
  change Integrable weight volume ∧ (∫ x, weight x) =
    (2 * Real.pi) ^ ((d : ℝ) / 2) / Real.sqrt (∏ i, diagonalValue i)
  have hA : A.PosDef := (FixedSpectrumAdmissibility.actual_precision_admissible hd hκ O).1
  have hdet : A.det = ∏ i, diagonalValue i :=
    FixedSpectrumDeterminant.actual_precision_det hd hκ O
  let B : ℝ := (2 * Real.pi) ^ ((d : ℝ) / 2)
  let c : ℝ := Real.sqrt A.det / B
  have hB : 0 < B := Real.rpow_pos_of_pos (by positivity) _
  have hsqrt : 0 < Real.sqrt A.det := Real.sqrt_pos.2 hA.det_pos
  have hc : 0 < c := div_pos hsqrt hB
  have hdensity : multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹ =
      (volume : Measure (EuclideanSpace ℝ (Fin d))).withDensity
        (fun x => ENNReal.ofReal (c * weight x)) := by
    simpa only [c, B, weight, dotProduct] using
      AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity.multivariateGaussian_eq_withDensity_of_posDef A hA
  have hmass : (∫⁻ x, ENNReal.ofReal (c * weight x)) = 1 := by
    have h := congrArg (fun μ : Measure (EuclideanSpace ℝ (Fin d)) => μ Set.univ)
      hdensity.symm
    simpa only [withDensity_apply _ MeasurableSet.univ, Measure.restrict_univ,
      measure_univ] using h
  have hnonneg : 0 ≤ᵐ[volume] (fun x => c * weight x) :=
    Filter.Eventually.of_forall fun x => mul_nonneg hc.le (Real.exp_nonneg _)
  have hmeas : AEStronglyMeasurable (fun x => c * weight x) volume := by
    have hcont : Continuous (fun x => c * weight x) := by
      dsimp only [weight]
      fun_prop
    exact hcont.aestronglyMeasurable
  have hcw : Integrable (fun x => c * weight x) volume :=
    (lintegral_ofReal_ne_top_iff_integrable hmeas hnonneg).mp
      (by rw [hmass]; exact ENNReal.one_ne_top)
  have hw : Integrable weight volume :=
    (integrable_const_mul_iff (isUnit_iff_ne_zero.mpr hc.ne') weight).mp hcw
  have hscaled : c * (∫ x, weight x) = 1 := by
    rw [← integral_const_mul]
    rw [integral_eq_lintegral_of_nonneg_ae hnonneg hmeas, hmass]
    rfl
  refine ⟨hw, ?_⟩
  rw [← hdet]
  apply (eq_div_iff hsqrt.ne').2
  have hratio : Real.sqrt A.det * (∫ x, weight x) / B = 1 := by
    simpa only [c, div_mul_eq_mul_div] using hscaled
  have hproduct := (div_eq_iff hB.ne').mp hratio
  simpa only [B, one_mul, mul_comm] using hproduct
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumNormalizer
