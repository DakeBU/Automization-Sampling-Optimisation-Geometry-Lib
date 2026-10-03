import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Analysis.InnerProductSpace.Symmetric
import Mathlib.Algebra.BigOperators.Field

/-!
# Finite-sample empirical covariance algebra

This file exposes only the small public interface needed immediately before a
matrix concentration theorem: the empirical second-moment operator, the exact
norm of a rank-one summand, and one theorem packaging the centered finite-sum
decomposition with symmetry and a uniform summand bound. No concentration or
target tail bound is assumed.
-/

noncomputable section

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Probability
namespace EmpiricalCovariance

open scoped BigOperators RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
variable {κ : Type*} [Fintype κ]

/-- The normalized finite-sample second-moment operator. For an empty sample
the inverse-cardinality convention makes this zero; concentration consumers
normally assume `[Nonempty κ]`. -/
def empiricalSecondMoment (sample : κ → E) : E →L[ℝ] E :=
  (Fintype.card κ : ℝ)⁻¹ •
    ∑ i, InnerProductSpace.rankOne ℝ (sample i) (sample i)

/-- The operator norm of the rank-one second-moment operator `x xᵀ` is exactly
`‖x‖²`. -/
theorem norm_rankOne_self_eq_sq (x : E) :
    ‖InnerProductSpace.rankOne ℝ x x‖ = ‖x‖ ^ 2 := by
  simp [pow_two]

/-- Deterministic preconcentration package for an empirical second moment.

For a nonempty finite sample whose vectors have norm at most `B`, and a
symmetric population operator with norm at most `B²`, this proves together:

1. the exact normalized decomposition of the empirical error into centered
   rank-one summands;
2. symmetry of every centered summand;
3. the operator-norm bound `2 B²` for every centered summand.

These are the elementary obligations used to instantiate a standard matrix
concentration theorem later; no probabilistic tail conclusion occurs here. -/
theorem empiricalSecondMoment_preconcentration
    [Nonempty κ]
    (population : E →L[ℝ] E) (sample : κ → E) (B : ℝ)
    (hB : 0 ≤ B)
    (hpopulationSymmetric : LinearMap.IsSymmetric (population : E →ₗ[ℝ] E))
    (hpopulationNorm : ‖population‖ ≤ B ^ 2)
    (hsampleNorm : ∀ i, ‖sample i‖ ≤ B) :
    (empiricalSecondMoment sample - population =
      (Fintype.card κ : ℝ)⁻¹ •
        ∑ i, (InnerProductSpace.rankOne ℝ (sample i) (sample i) - population)) ∧
    (∀ i, LinearMap.IsSymmetric
      ((InnerProductSpace.rankOne ℝ (sample i) (sample i) - population : E →L[ℝ] E) :
        E →ₗ[ℝ] E)) ∧
    (∀ i,
      ‖InnerProductSpace.rankOne ℝ (sample i) (sample i) - population‖ ≤
        2 * B ^ 2) := by
  have hcard : (Fintype.card κ : ℝ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  constructor
  · rw [Finset.sum_sub_distrib]
    unfold empiricalSecondMoment
    rw [smul_sub]
    congr 1
    rw [Finset.sum_const, ← Nat.cast_smul_eq_nsmul ℝ]
    exact (inv_smul_smul₀ hcard population).symm
  constructor
  · intro i
    exact (InnerProductSpace.isSymmetric_rankOne_self (sample i)).sub
      hpopulationSymmetric
  · intro i
    have hsample_sq : ‖sample i‖ ^ 2 ≤ B ^ 2 :=
      (sq_le_sq₀ (norm_nonneg (sample i)) hB).2 (hsampleNorm i)
    calc
      ‖InnerProductSpace.rankOne ℝ (sample i) (sample i) - population‖
          ≤ ‖InnerProductSpace.rankOne ℝ (sample i) (sample i)‖ + ‖population‖ :=
        norm_sub_le _ _
      _ = ‖sample i‖ ^ 2 + ‖population‖ := by
        rw [norm_rankOne_self_eq_sq]
      _ ≤ B ^ 2 + B ^ 2 := add_le_add hsample_sq hpopulationNorm
      _ = 2 * B ^ 2 := by ring

end EmpiricalCovariance
end Probability
end TechnicalLemmas
end AutoSamplingTheory
