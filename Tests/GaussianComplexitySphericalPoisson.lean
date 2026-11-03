import AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedNumerator

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity

noncomputable section

-- n=2 exercises the logarithmic potential branch, explicitly beyond the
-- paper's trailing n>=3 clause. The n=3 test exercises the power branch.
example (n : ℕ) (hn : n = 2 ∨ n = 3) :
    let hn2 : 2 ≤ n := by rcases hn with rfl | rfl <;> omega
    let j0 : Fin n := ⟨0, by omega⟩
    let τ : Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
    let σ : Measure (EuclideanSpace ℝ (Fin n)) :=
      (τ Set.univ)⁻¹ • τ.map (fun y => y.val)
    let K : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
      (1 + (1 / 2 : ℝ) ^ 2 - 2 * (1 / 2 : ℝ) * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
    (∫ y : EuclideanSpace ℝ (Fin n), 1 / K y ∂σ) = 4 / 3 ∧
    (∫ y : EuclideanSpace ℝ (Fin n), WithLp.ofLp y j0 / K y ∂σ) = 2 / 3 := by
  have hn2 : 2 ≤ n := by rcases hn with rfl | rfl <;> omega
  have hm := SphericalPoisson.spherical_poisson_moments hn2 (1 / 2)
    (by norm_num) (by norm_num)
  constructor
  · convert hm.2.2.1 using 1 <;> norm_num
  · convert hm.2.2.2 using 1 <;> norm_num

#print axioms SphericalPoisson.spherical_poisson_moments
#print axioms selected_numerator_value

end
