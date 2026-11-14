import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumNormalizer

open Matrix MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity

private theorem actual_gaussian_density_consumer {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let diagonalValue : Fin d → ℝ := fun i =>
    (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Matrix.diagonal diagonalValue *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let weight : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    Real.exp (- (∑ i : Fin d, x.ofLp i * (A.mulVec x.ofLp) i) / 2)
  ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹ =
    (volume : Measure (EuclideanSpace ℝ (Fin d))).withDensity (fun x =>
      ENNReal.ofReal (weight x /
        (∫ y : EuclideanSpace ℝ (Fin d), weight y ∂volume))) := by
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
  change multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹ =
    volume.withDensity (fun x => ENNReal.ofReal (weight x / ∫ y, weight y))
  have hA : A.PosDef := (FixedSpectrumAdmissibility.actual_precision_admissible hd hκ O).1
  have hdet : A.det = ∏ i, diagonalValue i :=
    FixedSpectrumDeterminant.actual_precision_det hd hκ O
  have hmass : (∫ y, weight y) =
      (2 * Real.pi) ^ ((d : ℝ) / 2) / Real.sqrt (∏ i, diagonalValue i) :=
    (FixedSpectrumNormalizer.actual_normalizing_integral hd hκ O).2
  have hB : 0 < (2 * Real.pi) ^ ((d : ℝ) / 2) :=
    Real.rpow_pos_of_pos (by positivity) _
  have hsqrt : 0 < Real.sqrt A.det := Real.sqrt_pos.2 hA.det_pos
  have hmasspos : 0 < ∫ y, weight y := by
    rw [hmass, ← hdet]
    exact div_pos hB hsqrt
  rw [AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity.multivariateGaussian_eq_withDensity_of_posDef A hA]
  apply withDensity_congr_ae
  exact Filter.Eventually.of_forall fun x => by
    apply congrArg ENNReal.ofReal
    change Real.sqrt A.det / (2 * Real.pi) ^ ((d : ℝ) / 2) * weight x =
      weight x / (∫ y, weight y)
    apply (eq_div_iff hmasspos.ne').2
    rw [hmass, ← hdet]
    field_simp [hsqrt.ne', hB.ne']

#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumNormalizer.actual_normalizing_integral
#print axioms actual_gaussian_density_consumer
