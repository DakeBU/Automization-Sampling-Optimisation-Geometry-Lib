import GC31LowerBound

open Matrix

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

universe u v

/-- The admissible precisions are exactly the symmetric real matrices with
`I ≼ A ≼ κ I`, including in dimension zero. -/
theorem admissible_iff_posSemidef_bounds {d : ℕ} (κ : ℝ) (A : Precision d) :
    Admissible κ A ↔ A.IsHermitian ∧
      (A - 1).PosSemidef ∧ (κ • (1 : Precision d) - A).PosSemidef := by
  have lower (x : Fin d → ℝ) :
      star x ⬝ᵥ ((A - 1) *ᵥ x) = x ⬝ᵥ (A *ᵥ x) - x ⬝ᵥ x := by
    simp [Matrix.sub_mulVec, dotProduct_sub]
  have upper (x : Fin d → ℝ) :
      star x ⬝ᵥ ((κ • (1 : Precision d) - A) *ᵥ x) =
        κ * (x ⬝ᵥ x) - x ⬝ᵥ (A *ᵥ x) := by
    simp [Matrix.sub_mulVec, Matrix.smul_mulVec, dotProduct_sub, dotProduct_smul]
  constructor
  · rintro ⟨hA, hx⟩
    refine ⟨hA, .of_dotProduct_mulVec_nonneg (hA.sub isHermitian_one) (fun x => ?_),
      .of_dotProduct_mulVec_nonneg ((isHermitian_one.smul (show IsSelfAdjoint κ from rfl)).sub hA)
        (fun x => ?_)⟩
    · exact (lower x).symm ▸ sub_nonneg.mpr (hx x).1
    · exact (upper x).symm ▸ sub_nonneg.mpr (hx x).2
  · rintro ⟨hA, hL, hU⟩
    refine ⟨hA, fun x => ⟨?_, ?_⟩⟩
    · exact sub_nonneg.mp ((lower x) ▸ hL.dotProduct_mulVec_nonneg x)
    · exact sub_nonneg.mp ((upper x) ▸ hU.dotProduct_mulVec_nonneg x)

/-- At all three closed parameter endpoints, the minimum in equation (3) is one. -/
theorem gaussian_query_complexity_dimension_one :
    ENNReal.ofReal (1/256 : ℝ) ≤ gaussianQueryComplexity.{u,v} 1 4 (1/16) := by
  have hlog := Real.log_le_sub_one_of_pos (show 0 < (9 : ℝ)⁻¹ by norm_num)
  rw [Real.log_inv] at hlog
  have hl : 1 ≤ 2 * Real.log 9 := by linarith
  have hmin : min (1 : ℝ) (Real.sqrt 4 * Real.log (1 + 1 / (Real.sqrt 4 * (1/16)))) = 1 := by
    apply min_eq_left
    norm_num
    exact hl
  simpa only [Nat.cast_one, hmin, mul_one] using
    (gaussian_query_complexity_lower_bound.{u,v} (d := 1) (κ := 4) (ε := 1/16)
      (by decide) (by norm_num) (by norm_num) (by norm_num))

#print axioms admissible_iff_posSemidef_bounds
#print axioms gaussian_query_complexity_dimension_one

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
