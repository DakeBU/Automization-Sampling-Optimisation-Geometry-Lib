import AutoSamplingTheory.ExampleCases.GaussianComplexity.SurfaceLaw
import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation
import Mathlib.Tactic.NormNum.RealSqrt
set_option autoImplicit false
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity

/-! Distinct coordinates have the same ACTUAL column law, via the one shared surface node. -/
example :
    (orthogonalHaar 3).map (fun O : Matrix.orthogonalGroup (Fin 3) ℝ =>
      WithLp.toLp 2 (fun i : Fin 3 => (O : Matrix (Fin 3) (Fin 3) ℝ) i 0)) =
    (orthogonalHaar 3).map (fun O : Matrix.orthogonalGroup (Fin 3) ℝ =>
      WithLp.toLp 2 (fun i : Fin 3 => (O : Matrix (Fin 3) (Fin 3) ℝ) i 2)) := by
  exact (AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar.column_map_eq_normalized_surface
    (n := 3) 0).trans
      (AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar.column_map_eq_normalized_surface
        (n := 3) 2).symm

/-! Actual consumer: determinant-conditioned Gaussian bind-mixture gap transported
to the ACTUAL normalized Euclidean surface law, without a Poisson value. -/
example {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let s : ℝ := Real.sqrt κ
    let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
    let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let τ : Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
    let σ : Measure (EuclideanSpace ℝ (Fin n)) :=
      (τ Set.univ)⁻¹ • τ.map (fun y => y.val)
    let f : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
      ((s + 1) * WithLp.ofLp y j0 - (s - 1)) /
        (1 + r ^ 2 - 2 * r * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
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
      2 * β * (∫ y, f y ∂σ) := by
  dsimp only
  have hℓ := (AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt.selected_tilt
    hn hκ).2.2.1
  have hm := AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation.actual_mixture_expectation_gap
    hn hκ hℓ.le
  have hg := (SurfaceLaw.selected_surface_transport hn hκ).2.2.2
  rw [hm.2.2.2.2.2.2, hg]
  ring


#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.SurfaceLaw.selected_surface_transport
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.SurfaceLaw.selected_surface_transport
    | throwError "Target missing"
  let some body := info.value? (allowOpaque := true) | throwError "Body missing"
  logInfo m!"ACTUAL COMPILED PARENTS {body.getUsedConstants}"

#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar.column_map_eq_normalized_surface
