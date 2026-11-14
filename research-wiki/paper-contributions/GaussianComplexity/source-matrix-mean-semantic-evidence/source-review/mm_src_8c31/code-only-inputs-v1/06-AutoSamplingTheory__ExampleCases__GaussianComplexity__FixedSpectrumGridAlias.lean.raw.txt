import Mathlib.Analysis.SpecialFunctions.Trigonometric.Complex
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Exact midpoint-grid cosine aliases, arXiv:2610.20492v1, Appendix C.3,
paragraph 3 / Ex139. Frequencies are arbitrary integers. The finite-grid
Gaussian expectation identification and closed moment sums are separate steps. -/

open scoped BigOperators

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias

/-- The literal midpoint cosine grid vanishes off multiples of `2*d` and
has the signed alias value at every multiple, including negative frequencies. -/
theorem actual_midpoint_grid_cosine_alias {d : ℕ} (hd : 2 ≤ d) (k : ℤ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  (∑ i : Fin d, Real.cos ((k : ℝ) * θ i)) =
    (d : ℝ) * (if (2 * (d : ℤ)) ∣ k then
      (-1 : ℝ) ^ (k / (2 * (d : ℤ))) else 0) := by
  classical
  dsimp only
  have hd0 : (d : ℝ) ≠ 0 := by exact_mod_cast (show d ≠ 0 by omega)
  by_cases hk : (2 * (d : ℤ)) ∣ k
  · rw [if_pos hk]
    let q : ℤ := k / (2 * (d : ℤ))
    have hq : k = 2 * (d : ℤ) * q := (Int.mul_ediv_cancel' hk).symm
    have hqr : (k : ℝ) = 2 * (d : ℝ) * (q : ℝ) := by exact_mod_cast hq
    have hterm (i : Fin d) :
        Real.cos ((k : ℝ) * (((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ))) =
          (-1 : ℝ) ^ q := by
      have hangle : (k : ℝ) * (((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)) =
          (q : ℝ) * Real.pi + ((q * (i.val : ℤ) : ℤ) : ℝ) * (2 * Real.pi) := by
        rw [hqr]
        push_cast
        field_simp
        ring
      rw [hangle, Real.cos_add_int_mul_two_pi, Real.cos_int_mul_pi]
    simp_rw [hterm]
    simp [q]
  · rw [if_neg hk, mul_zero]
    let a : ℝ := (k : ℝ) * Real.pi / (d : ℝ)
    have hsin : Real.sin (a / 2) ≠ 0 := by
      intro hz
      obtain ⟨m, hm⟩ := Real.sin_eq_zero_iff.mp hz
      have hm' : (m : ℝ) = (k : ℝ) / (2 * (d : ℝ)) := by
        apply mul_right_cancel₀ Real.pi_ne_zero
        calc
          (m : ℝ) * Real.pi = a / 2 := hm
          _ = ((k : ℝ) / (2 * (d : ℝ))) * Real.pi := by dsimp [a]; ring
      have hreal : (k : ℝ) = (2 * (d : ℝ)) * (m : ℝ) := by
        rw [hm']
        field_simp
      have hint : k = (2 * (d : ℤ)) * m := by exact_mod_cast hreal
      exact hk ⟨m, hint⟩
    have hgrid : (∑ i : Fin d,
        Real.cos ((k : ℝ) * (((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)))) =
        ∑ i ∈ Finset.range d, Real.cos (a * (i : ℝ) + a / 2) := by
      rw [← Fin.sum_univ_eq_sum_range]
      apply Finset.sum_congr rfl
      intro i _
      congr 1
      dsimp [a]
      ring
    rw [hgrid]
    have hsum := Real.sin_mul_sum_cos d a (a / 2)
    have harg : (d : ℝ) * a / 2 = (k : ℝ) * Real.pi / 2 := by
      dsimp [a]
      field_simp
    have harg' : ((d : ℝ) - 1) * a / 2 + a / 2 = (k : ℝ) * Real.pi / 2 := by
      calc
        _ = (d : ℝ) * a / 2 := by ring
        _ = _ := harg
    rw [harg, harg'] at hsum
    have hzero : Real.sin ((k : ℝ) * Real.pi / 2) *
        Real.cos ((k : ℝ) * Real.pi / 2) = 0 := by
      have hdouble := Real.sin_two_mul ((k : ℝ) * Real.pi / 2)
      rw [show 2 * ((k : ℝ) * Real.pi / 2) = (k : ℝ) * Real.pi by ring,
        Real.sin_int_mul_pi] at hdouble
      linarith
    rw [hzero] at hsum
    exact (mul_eq_zero.mp hsum).resolve_left hsin

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias
