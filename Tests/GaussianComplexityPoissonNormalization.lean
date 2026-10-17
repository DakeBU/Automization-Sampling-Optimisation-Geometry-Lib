import AutoSamplingTheory.ExampleCases.GaussianComplexity.PoissonNormalization
import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation
import Mathlib.Tactic.NormNum.RealSqrt

set_option autoImplicit false
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.PoissonNormalization

/-! The odd boundary dimension exercises a genuine real half-power. -/
example : Integrable (fun O : Matrix.orthogonalGroup (Fin 3) ℝ =>
    (3 * (O : Matrix (Fin 3) (Fin 3) ℝ) 0 0 - 1) /
      (1 + (2 / 9 : ℝ) ^ 2 - 2 * (2 / 9 : ℝ) *
        (O : Matrix (Fin 3) (Fin 3) ℝ) 0 0) ^ ((3 : ℝ) / 2)) (orthogonalHaar 3) := by
  have h := (selected_gaussian_normalization (n := 3) (κ := 4)
    (by norm_num) (by norm_num)).1
  convert h using 1 <;> norm_num

/-! An actual consumer: normalize the test expectation difference of the two
literal determinant-conditioned Gaussian bind mixtures, without a Poisson value. -/
example {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let s : ℝ := Real.sqrt κ
    let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
    let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let U : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
      fun O => (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
    let q : Matrix.orthogonalGroup (Fin n) ℝ → ℝ := fun O =>
      ((s + 1) * U O - (s - 1)) /
        (1 + r ^ 2 - 2 * r * U O) ^ ((n : ℝ) / 2)
    let β : ℝ := (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (s + 1) ^ n) *
      (1 - 1 / (n : ℝ)) ^ ((n : ℝ) / 2)
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    let t : EuclideanSpace ℝ (Fin n) → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
    (∫ x, t x ∂νpos.bind γ) - (∫ x, t x ∂νneg.bind γ) =
      2 * β * (∫ O, q O ∂μ) := by
  dsimp only
  have hℓ := (AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt.selected_tilt
    hn hκ).2.2.1
  have hm := AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation.actual_mixture_expectation_gap
    hn hκ hℓ.le
  have hg := (selected_gaussian_normalization hn hκ).2
  rw [hm.2.2.2.2.2.2, hg]
  ring

#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.PoissonNormalization.selected_gaussian_normalization
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.PoissonNormalization.selected_gaussian_normalization
    | throwError "Target missing"
  let some body := info.value? (allowOpaque := true) | throwError "Body missing"
  let parents := body.getUsedConstants.filter fun name =>
    name.toString.startsWith "Real." || name.toString.startsWith "Continuous." ||
    name.toString.startsWith "AutoSamplingTheory." ||
    name.toString.startsWith "MeasureTheory.integral"
  logInfo m!"ACTUAL COMPILED PARENTS {parents}"
