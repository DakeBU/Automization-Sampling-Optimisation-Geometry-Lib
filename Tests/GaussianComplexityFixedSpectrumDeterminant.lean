import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDeterminant
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility
import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity
open scoped BigOperators
set_option autoImplicit false

/-- Actual same-A source Gaussian density. The coefficient consumes the new
determinant producer; positivity is produced internally by existing source
admissibility. No supplied determinant/PosDef/density certificate. -/
private theorem actual_gaussian_density_consumer {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let diagonalValue : Fin d → ℝ := fun i =>
      (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
    let A : Matrix (Fin d) (Fin d) ℝ :=
      (O : Matrix (Fin d) (Fin d) ℝ) * Matrix.diagonal diagonalValue *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹ =
      (volume : Measure (EuclideanSpace ℝ (Fin d))).withDensity (fun x =>
        ENNReal.ofReal (Real.sqrt (∏ i : Fin d, diagonalValue i) /
          (2 * Real.pi) ^ ((d : ℝ) / 2) *
          Real.exp (-((WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x)) / 2))) := by
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let diagonalValue : Fin d → ℝ := fun i =>
    (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Matrix.diagonal diagonalValue *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  change ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹ =
    (volume : Measure (EuclideanSpace ℝ (Fin d))).withDensity (fun x =>
      ENNReal.ofReal (Real.sqrt (∏ i : Fin d, diagonalValue i) /
        (2 * Real.pi) ^ ((d : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x)) / 2)))
  have hA : A.PosDef :=
    (FixedSpectrumAdmissibility.actual_precision_admissible (d := d) hd (κ := κ) hκ O).1
  have hdet : A.det = ∏ i : Fin d, diagonalValue i :=
    FixedSpectrumDeterminant.actual_precision_det (d := d) hd (κ := κ) hκ O
  have hμ := multivariateGaussian_eq_withDensity_of_posDef (n := d) A hA
  rw [hdet] at hμ
  exact hμ

#print axioms FixedSpectrumDeterminant.actual_precision_det
#print axioms FixedSpectrumAdmissibility.actual_precision_admissible
#print axioms multivariateGaussian_eq_withDensity_of_posDef
#print axioms actual_gaussian_density_consumer
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDeterminant.actual_precision_det | throwError "Missing actual source determinant theorem"
  let some proof := info.value? (allowOpaque := true) | throwError "Missing actual determinant proof"
  let parents := proof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  logInfo m!"ACTUAL COMPILED ASTIS PRODUCER PARENTS {parents}"
  let some consumer := env.find? ``actual_gaussian_density_consumer | throwError "Missing private actual Gaussian consumer"
  let some consumerProof := consumer.value? (allowOpaque := true) | throwError "Missing actual Gaussian consumer proof"
  let consumerParents := consumerProof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  unless consumerParents.contains `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDeterminant.actual_precision_det do
    throwError "Actual Gaussian consumer must consume the new determinant producer"
  logInfo m!"ACTUAL COMPILED ASTIS GAUSSIAN CONSUMER PARENTS {consumerParents}"
