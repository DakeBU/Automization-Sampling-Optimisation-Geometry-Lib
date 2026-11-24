import GC44GramUse
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias

/-! The coordinate-vector obstruction of Section 4.4 on the midpoint cosine grid. -/
noncomputable section
open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

/-- At each nonconstant frequency below d the mean squared cosine on this grid is one half. -/
theorem sum_sq_grid_mode {d n : ℕ} (hn : 0 < n) (hd : n < d) :
    ∑ i : Fin d, Real.cos ((n : ℝ) * gridAngle d i)^2 = (d : ℝ)/2 := by
  have hk : ¬ (2*(d : ℤ)) ∣ 2*(n : ℤ) := by
    intro h
    have hz := Int.eq_zero_of_dvd_of_nonneg_of_lt (show 0 ≤ 2*(n : ℤ) by omega)
      (show 2*(n : ℤ) < 2*(d : ℤ) by omega) h
    omega
  have h := FixedSpectrumGridAlias.actual_midpoint_grid_cosine_alias (d := d)
    (by omega) (2*(n : ℤ))
  change (∑ i : Fin d, Real.cos (((2*(n : ℤ) : ℤ) : ℝ) * gridAngle d i)) = _ at h
  rw [if_neg hk, mul_zero] at h
  push_cast at h
  have ht (i : Fin d) : Real.cos ((n : ℝ) * gridAngle d i)^2 =
      (Real.cos ((2*(n:ℝ)) * gridAngle d i) + 1)/2 := by
    rw [mul_assoc, Real.cos_two_mul]
    ring
  simp_rw [ht]
  simp [← Finset.sum_div, Finset.sum_add_distrib, h]

/-- One fixed coordinate unit vector has absolute cosine quadratic form at least 1/√2. -/
theorem unit_coordinate_obstruction {d q : ℕ} (hd : 2*q+1 < d) :
    ∃ u : Fin d → ℝ, ‖WithLp.toLp 2 u‖ = 1 ∧
      1 / Real.sqrt 2 ≤ |u ⬝ᵥ (cosineDiag d q *ᵥ u)| := by
  classical
  let n := 2*q+1
  let c (i : Fin d) := Real.cos ((n:ℝ) * gridAngle d i)
  have hm := sum_sq_grid_mode (d := d) (n := n) (by dsimp [n]; omega) hd
  have hex : ∃ i : Fin d, (1:ℝ)/2 ≤ (c i)^2 := by
    by_contra! H
    have hn : (Finset.univ : Finset (Fin d)).Nonempty := ⟨⟨0,by omega⟩, Finset.mem_univ _⟩
    have hlt := Finset.sum_lt_sum_of_nonempty hn (fun i _ => H i)
    change (∑ i : Fin d, (c i)^2) < ∑ _ : Fin d, (1:ℝ)/2 at hlt
    change (∑ i : Fin d, (c i)^2) = (d:ℝ)/2 at hm
    rw [hm] at hlt
    simp at hlt
    linarith
  obtain ⟨i,hi⟩ := hex
  let u : Fin d → ℝ := Pi.single i 1
  have hs : u ⬝ᵥ u = 1 := by simp [u, dotProduct, Pi.single_apply]
  have hform : u ⬝ᵥ (cosineDiag d q *ᵥ u) = c i := by
    simp [u, c, n, cosineDiag, Matrix.mulVec_diagonal, dotProduct, Pi.single_apply]
  refine ⟨u, ?_, ?_⟩
  · have hn := dot_self u
    rw [hs] at hn
    nlinarith [norm_nonneg (WithLp.toLp 2 u)]
  · rw [hform, ← Real.sqrt_one, ← Real.sqrt_div (by norm_num : (0:ℝ) ≤ 1)]
    exact (Real.sqrt_le_sqrt hi).trans_eq (Real.sqrt_sq_eq_abs _)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
