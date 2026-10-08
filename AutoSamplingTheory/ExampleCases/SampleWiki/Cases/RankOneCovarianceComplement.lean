import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.Analysis.Real.Sqrt

/-!
# A positive rank-one covariance complement

The concrete covariance producer needed by the Gaussian center-noise absorption
step in the pinned OAI log-concave compiler (`lem:compiler-absorption`,
`openai/math` adc7f124). This is an authored algebraic prerequisite, not the
entire source lemma. A caller still has to supply normalized slot vectors,
block seed semantics and the pathwise translation/query identity.

The explicit construction uses a denominator at least one, including at zero
and at the singular boundary. No square-root existence is a premise.
-/

noncomputable section
open scoped RealInnerProductSpace
open InnerProductSpace ContinuousLinearMap

namespace AutoSamplingTheory.ExampleCases.SampleWiki.Cases.RankOneCovarianceComplement

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- A unit-ball vector has an actual positive covariance complement. No
invertibility, nonzero-vector or finite-dimensional premise is required. -/
theorem exists_positive_complement (u : E) (hu : ‖u‖ ≤ 1) :
    ∃ P : E →L[ℝ] E, P.IsPositive ∧
      P.adjoint.comp P + InnerProductSpace.rankOne ℝ u u =
        ContinuousLinearMap.id ℝ E := by
  let a : ℝ := Real.sqrt (1 - ‖u‖ ^ 2)
  let c : ℝ := 1 / (1 + a)
  let P : E →L[ℝ] E := ContinuousLinearMap.id ℝ E - c • rankOne ℝ u u
  have hn : 0 ≤ 1 - ‖u‖ ^ 2 := by nlinarith [norm_nonneg u]
  have ha : 0 ≤ a := Real.sqrt_nonneg _
  have ha2 : a ^ 2 = 1 - ‖u‖ ^ 2 := Real.sq_sqrt hn
  have hden : 0 < 1 + a := by positivity
  have hc0 : 0 ≤ c := by dsimp [c]; positivity
  have hc1 : c ≤ 1 := by
    dsimp [c]
    exact (div_le_one hden).2 (by linarith)
  have hc : 2 * c - c ^ 2 * ‖u‖ ^ 2 = 1 := by
    dsimp [c]
    field_simp
    nlinarith
  have hself : P.adjoint = P := by
    simp [P, ContinuousLinearMap.adjoint_id]
  refine ⟨P, ?_, ?_⟩
  · rw [ContinuousLinearMap.isPositive_iff']
    refine ⟨?_, fun x => ?_⟩
    · exact hself
    · have hcs := abs_real_inner_le_norm u x
      have hib : ⟪u, x⟫_ℝ ^ 2 ≤ ‖x‖ ^ 2 := by
        have habs : |⟪u, x⟫_ℝ| ≤ ‖x‖ :=
          hcs.trans (by nlinarith [norm_nonneg x])
        have hh := sq_le_sq₀ (abs_nonneg ⟪u, x⟫_ℝ) (norm_nonneg x) |>.2 habs
        simpa using hh
      have hci : c * ⟪u, x⟫_ℝ ^ 2 ≤ ⟪u, x⟫_ℝ ^ 2 :=
        mul_le_of_le_one_left (sq_nonneg _) hc1
      simp only [P, sub_apply, id_apply, smul_apply, rankOne_apply,
        inner_sub_left, inner_smul_left, real_inner_self_eq_norm_sq]
      change 0 ≤ ‖x‖ ^ 2 - c * (⟪u, x⟫_ℝ * ⟪u, x⟫_ℝ)
      nlinarith
  · rw [hself]
    ext x
    simp only [P, comp_apply, add_apply, sub_apply, id_apply, smul_apply,
      rankOne_apply, inner_sub_right, inner_smul_right, real_inner_self_eq_norm_sq]
    match_scalars <;> first | ring1 | linear_combination -⟪u, x⟫_ℝ * hc

end AutoSamplingTheory.ExampleCases.SampleWiki.Cases.RankOneCovarianceComplement
