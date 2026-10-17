import AutoSamplingTheory.ExampleCases.GaussianComplexity.ActualTotalVariation
import Lean.Util.FoldConsts
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.ActualTotalVariation

example :
    let μ := orthogonalHaar 4
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin 4) ℝ | (O : Matrix (Fin 4) (Fin 4) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin 4) ℝ | (O : Matrix (Fin 4) (Fin 4) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin 4) ℝ → Measure (EuclideanSpace ℝ (Fin 4)) :=
      fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin 4))
        (singleBlockPrecision 9 O)⁻¹
    let Ppos := νpos.bind γ
    let Pneg := νneg.bind γ
    let t : EuclideanSpace ℝ (Fin 4) → ℝ := fun x => Real.exp (-(1 : ℝ) * ‖x‖ ^ 2)
    let p : Matrix.orthogonalGroup (Fin 4) ℝ → EuclideanSpace ℝ (Fin 4) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision 9 O).det /
        (2 * Real.pi) ^ ((4 : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision 9 O *ᵥ WithLp.ofLp x)) / 2)
    2 * |∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
      (O : Matrix (Fin 4) (Fin 4) ℝ).det * (∫ x, t x * p O x) ∂μ| ≤
      sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin 4)),
        MeasurableSet B ∧ z = |Ppos.real B - Pneg.real B|} := by
  exact actual_radial_test_tv (n := 4) (κ := 9) (ℓ := 1) (by decide) (by norm_num) (by norm_num)

example :
    let μ := orthogonalHaar 4
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin 4) ℝ | (O : Matrix (Fin 4) (Fin 4) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin 4) ℝ | (O : Matrix (Fin 4) (Fin 4) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin 4) ℝ → Measure (EuclideanSpace ℝ (Fin 4)) :=
      fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin 4))
        (singleBlockPrecision 9 O)⁻¹
    let Ppos := νpos.bind γ
    let Pneg := νneg.bind γ
    let t : EuclideanSpace ℝ (Fin 4) → ℝ := fun x => Real.exp (-(0 : ℝ) * ‖x‖ ^ 2)
    let p : Matrix.orthogonalGroup (Fin 4) ℝ → EuclideanSpace ℝ (Fin 4) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision 9 O).det /
        (2 * Real.pi) ^ ((4 : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision 9 O *ᵥ WithLp.ofLp x)) / 2)
    2 * |∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
      (O : Matrix (Fin 4) (Fin 4) ℝ).det * (∫ x, t x * p O x) ∂μ| ≤
      sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin 4)),
        MeasurableSet B ∧ z = |Ppos.real B - Pneg.real B|} := by
  exact actual_radial_test_tv (n := 4) (κ := 9) (ℓ := 0) (by decide) (by norm_num) (by norm_num)

#print axioms actual_radial_test_tv
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.ActualTotalVariation.actual_radial_test_tv | throwError "Target missing"
  let some body := info.value? (allowOpaque := true) | throwError "Body missing"
  let parents := body.getUsedConstants.filter fun n =>
    n.toString.startsWith "AutoSamplingTheory" ||
    n.toString.contains "bernoulliMeasure" ||
    n.toString.contains "integral_toReal" ||
    n.toString.contains "integrableOn_union" ||
    n.toString.contains "withDensity" ||
    n.toString.contains "le_csSup"
  logInfo m!"ACTUAL COMPILED PARENTS {parents}"
