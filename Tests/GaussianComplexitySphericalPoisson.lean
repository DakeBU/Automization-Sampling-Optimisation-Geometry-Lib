import AutoSamplingTheory.ExampleCases.GaussianComplexity.SphericalPoisson
import AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity

noncomputable section

-- Both actual A1 moments are consumed by the literal selected numerator.
-- This is the line immediately before Eq24, not an evaluated Gaussian law.
theorem selected_numerator_value {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let s : ℝ := Real.sqrt κ
    let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let τ : Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
    let σ : Measure (EuclideanSpace ℝ (Fin n)) :=
      (τ Set.univ)⁻¹ • τ.map (fun y => y.val)
    let f : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
      ((s + 1) * WithLp.ofLp y j0 - (s - 1)) /
        (1 + r ^ 2 - 2 * r * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
    Integrable f σ ∧ (∫ y, f y ∂σ) = -(s - 1) / ((n : ℝ) * (1 - r ^ 2)) := by
  let s : ℝ := Real.sqrt κ
  let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let τ : Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
    (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
  let σ : Measure (EuclideanSpace ℝ (Fin n)) :=
    (τ Set.univ)⁻¹ • τ.map (fun y => y.val)
  let K : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
    (1 + r ^ 2 - 2 * r * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
  let g0 : EuclideanSpace ℝ (Fin n) → ℝ := fun y => 1 / K y
  let g1 : EuclideanSpace ℝ (Fin n) → ℝ := fun y => WithLp.ofLp y j0 / K y
  let f : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
    ((s + 1) * WithLp.ofLp y j0 - (s - 1)) / K y
  change Integrable f σ ∧ (∫ y, f y ∂σ) = -(s - 1) / ((n : ℝ) * (1 - r ^ 2))
  have ht := SelectedTilt.selected_tilt hn hκ
  have hm := SphericalPoisson.spherical_poisson_moments (by omega : 2 ≤ n)
    r ht.1 ht.2.1
  change Integrable g0 σ ∧ Integrable g1 σ ∧
    (∫ y, g0 y ∂σ) = 1 / (1 - r ^ 2) ∧
    (∫ y, g1 y ∂σ) = r / (1 - r ^ 2) at hm
  have heq : f = (fun y => (s + 1) * g1 y - (s - 1) * g0 y) := by
    funext y
    dsimp [f, g0, g1]
    ring
  have hf : Integrable f σ := by
    rw [heq]
    exact (hm.2.1.const_mul (s + 1)).sub (hm.1.const_mul (s - 1))
  have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast (by omega : n ≠ 0)
  have hs : s + 1 ≠ 0 := ne_of_gt (by dsimp [s]; positivity)
  have hnum : (s + 1) * r - (s - 1) = -(s - 1) / (n : ℝ) := by
    dsimp [r]
    field_simp
    ring
  refine ⟨hf, ?_⟩
  rw [heq, integral_sub (hm.2.1.const_mul _) (hm.1.const_mul _),
    integral_const_mul, integral_const_mul, hm.2.2.1, hm.2.2.2]
  calc
    _ = ((s + 1) * r - (s - 1)) / (1 - r ^ 2) := by ring
    _ = _ := by rw [hnum, div_div]

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
