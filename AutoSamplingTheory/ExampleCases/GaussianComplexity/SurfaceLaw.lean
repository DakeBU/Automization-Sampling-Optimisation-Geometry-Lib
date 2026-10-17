import AutoSamplingTheory.ExampleCases.GaussianComplexity.ColumnTransport
import AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar
open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.SurfaceLaw
set_option autoImplicit false
/-!
Actual normalized Euclidean surface law in the selected signed Gaussian expectation.
The canonical shared column/surface identity is consumed without assuming a
Poisson value, a conditional sphere law or an evaluated Eq24.
-/
theorem selected_surface_transport {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) :
    let s : ℝ := Real.sqrt κ
    let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
    let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let c : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) :=
      fun O => WithLp.toLp 2 (fun i => (O : Matrix (Fin n) (Fin n) ℝ) i j0)
    let ν : Measure (EuclideanSpace ℝ (Fin n)) := (orthogonalHaar n).map c
    let τ : Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
    let σ : Measure (EuclideanSpace ℝ (Fin n)) :=
      (τ Set.univ)⁻¹ • τ.map (fun y => y.val)
    let f : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
      ((s + 1) * WithLp.ofLp y j0 - (s - 1)) /
        (1 + r ^ 2 - 2 * r * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    ν = σ ∧ IsProbabilityMeasure σ ∧ Integrable f σ ∧
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det *
          (∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-ℓ * ‖x‖ ^ 2) ∂γ O)
        ∂orthogonalHaar n) =
        (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (s + 1) ^ n) *
          (1 - 1 / (n : ℝ)) ^ ((n : ℝ) / 2) * (∫ y, f y ∂σ) := by
  classical
  let s : ℝ := Real.sqrt κ
  let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
  let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let c : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) :=
      fun O => WithLp.toLp 2 (fun i => (O : Matrix (Fin n) (Fin n) ℝ) i j0)
  let ν : Measure (EuclideanSpace ℝ (Fin n)) := (orthogonalHaar n).map c
  let τ : Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
  let σ : Measure (EuclideanSpace ℝ (Fin n)) :=
      (τ Set.univ)⁻¹ • τ.map (fun y => y.val)
  let f : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
      ((s + 1) * WithLp.ofLp y j0 - (s - 1)) /
        (1 + r ^ 2 - 2 * r * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
  let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
  change ν = σ ∧ IsProbabilityMeasure σ ∧ Integrable f σ ∧ _
  have he : ν = σ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar.column_map_eq_normalized_surface j0
  have hp := ColumnTransport.selected_column_transport hn hκ
  refine ⟨he, ?_, ?_, ?_⟩
  · rw [← he]
    exact hp.1
  · rw [← he]
    exact hp.2.2.2.1
  · change (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det *
          (∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-ℓ * ‖x‖ ^ 2) ∂γ O)
        ∂orthogonalHaar n) =
        (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (s + 1) ^ n) *
          (1 - 1 / (n : ℝ)) ^ ((n : ℝ) / 2) * (∫ y, f y ∂σ)
    rw [← he]
    exact hp.2.2.2.2

end AutoSamplingTheory.ExampleCases.GaussianComplexity.SurfaceLaw
