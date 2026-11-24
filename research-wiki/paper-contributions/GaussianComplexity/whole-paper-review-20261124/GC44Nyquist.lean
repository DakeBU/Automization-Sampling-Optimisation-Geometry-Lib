import GC47Limitation
/-! The frequency range in the Section 4.4 detector obstruction matters.
At the excluded endpoint n=d every entry of the midpoint-grid cosine diagonal vanishes. -/
open Matrix Real
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
open FixedSpectrumRotation

theorem endpoint_cosine_zero {d q : ℕ} (hd : 2*q+1 = d) : cosineDiag d q = 0 := by
  have hd0 : (d : ℝ) ≠ 0 := by exact_mod_cast (show d ≠ 0 by omega)
  have h (i : Fin d) : cos ((d : ℝ)*gridAngle d i) = 0 := by
    rw [gridAngle,show (d : ℝ)*(((i.val : ℝ)+1/2)*π/d) = π/2+(i.val : ℝ)*π by field_simp; ring,
      cos_add_nat_mul_pi,cos_pi_div_two,mul_zero]
  unfold cosineDiag
  rw [hd]
  simp [h]

theorem endpoint_full_span_zero_statistic (q : ℕ) {κ : ℝ} (hk : κ ≠ 1) :
    ∀ᵐ g ∂gaussianStarts (2*q+1) q, krylov (2*q+1) q κ g = ⊤ ∧
      ∀ u : Fin (2*q+1) → ℝ, u ⬝ᵥ (cosineDiag (2*q+1) q *ᵥ u) = 0 := by
  have hd : 2*q+1 ≤ (q+1)^2 := by nlinarith [Nat.zero_le (q*q)]
  filter_upwards [gaussian_krylov_eq_top hk hd] with g hg
  exact ⟨hg,fun u => by simp [endpoint_cosine_zero (q := q) rfl]⟩

#print axioms endpoint_full_span_zero_statistic
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
