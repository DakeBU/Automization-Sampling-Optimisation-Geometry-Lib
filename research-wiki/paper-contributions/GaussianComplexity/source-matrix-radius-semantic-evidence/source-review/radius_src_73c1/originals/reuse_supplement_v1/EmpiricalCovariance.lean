import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Analysis.InnerProductSpace.Symmetric
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Algebra.BigOperators.Field
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability
import Mathlib.MeasureTheory.Function.L2Space

/-!
# Finite-sample empirical covariance algebra

This file exposes the deterministic and expectation-level interface needed
immediately before a matrix concentration theorem: the empirical second-moment
operator, the exact norm of a rank-one summand, the centered finite-sum
decomposition, and the first two operator moments of unit-vector rank-one
covariances. No concentration or target tail bound is assumed.
-/

noncomputable section

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Probability
namespace EmpiricalCovariance

open MeasureTheory
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

private theorem rankOne_self_sq_of_norm_one
    [CompleteSpace E] (x : E) (hx : ‖x‖ = 1) :
    (InnerProductSpace.rankOne ℝ x x) ^ (2 : ℕ) =
      InnerProductSpace.rankOne ℝ x x := by
  have hidem : IsIdempotentElem (InnerProductSpace.rankOne ℝ x x) :=
    (InnerProductSpace.isStarProjection_rankOne_self hx).isIdempotentElem
  simpa [IsIdempotentElem, pow_two] using hidem

/-- Expectation-level covariance identities for a unit-vector random variable.

If `X` takes values on the unit sphere and
`C = ∫ ω, X(ω) X(ω)ᵀ ∂μ`, then this theorem proves together that

1. `C` is self-adjoint;
2. `‖C‖ ≤ 1`;
3. `∫ (X Xᵀ - C)² = C - C²`;
4. `‖C - C²‖ ≤ 2‖C‖`.

This is the complete model-independent moment calculation used before a
self-adjoint matrix Bernstein theorem. Independence, a matrix moment-generating
function estimate, and every probability tail bound remain outside this result. -/
theorem unitRankOneCovariance_momentPackage
    [CompleteSpace E]
    {Omega : Type*} [MeasurableSpace Omega]
    {mu : Measure Omega} [IsProbabilityMeasure mu]
    (sample : Omega → E) (population : E →L[ℝ] E)
    (hsampleUnit : ∀ omega, ‖sample omega‖ = 1)
    (hRankOneIntegrable :
      Integrable (fun omega =>
        InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) mu)
    (hPopulation :
      ∫ omega, InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu =
        population) :
    IsSelfAdjoint population ∧
      ‖population‖ ≤ 1 ∧
      (∫ omega,
          (InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
            population) ^ (2 : ℕ) ∂mu =
        population - population ^ (2 : ℕ)) ∧
      ‖population - population ^ (2 : ℕ)‖ ≤ 2 * ‖population‖ := by
  let A := E →L[ℝ] E
  have hSelfAdjoint : IsSelfAdjoint population := by
    rw [ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric]
    intro x y
    have hx : Integrable
        (fun omega =>
          (InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) x) mu :=
      (ContinuousLinearMap.apply ℝ E x).integrable_comp hRankOneIntegrable
    have hy : Integrable
        (fun omega =>
          (InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) y) mu :=
      (ContinuousLinearMap.apply ℝ E y).integrable_comp hRankOneIntegrable
    rw [← hPopulation]
    calc
      inner ℝ ((∫ omega,
          InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) x) y =
          inner ℝ (∫ omega,
            (InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) x ∂mu) y := by
        rw [ContinuousLinearMap.integral_apply hRankOneIntegrable]
      _ = inner ℝ y (∫ omega,
            (InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) x ∂mu) :=
        real_inner_comm _ _
      _ = ∫ omega,
            inner ℝ y
              ((InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) x) ∂mu :=
        (integral_inner hx y).symm
      _ = ∫ omega,
            inner ℝ x
              ((InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) y) ∂mu := by
        apply integral_congr_ae
        filter_upwards with omega
        calc
          inner ℝ y
              ((InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) x) =
              inner ℝ
                ((InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) x) y :=
            real_inner_comm _ _
          _ = inner ℝ x
                ((InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) y) :=
            (InnerProductSpace.isSymmetric_rankOne_self
              (𝕜 := ℝ) (sample omega)) x y
      _ = inner ℝ x (∫ omega,
            (InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) y ∂mu) :=
        integral_inner hy x
      _ = inner ℝ x ((∫ omega,
          InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) y) := by
        rw [ContinuousLinearMap.integral_apply hRankOneIntegrable]
  have hNorm : ‖population‖ ≤ 1 := by
    rw [← hPopulation]
    calc
      ‖∫ omega,
          InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu‖ ≤
          1 * mu.real Set.univ := by
        apply norm_integral_le_of_norm_le_const
        filter_upwards with omega
        rw [norm_rankOne_self_eq_sq, hsampleUnit omega]
        norm_num
      _ = 1 := by simp
  have hright : Integrable
      (fun omega =>
        InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population) mu :=
    ((ContinuousLinearMap.mul ℝ A).flip population).integrable_comp
      hRankOneIntegrable
  have hleft : Integrable
      (fun omega =>
        population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) mu :=
    (ContinuousLinearMap.mul ℝ A population).integrable_comp
      hRankOneIntegrable
  have hconst : Integrable (fun _ : Omega => population ^ (2 : ℕ)) mu :=
    integrable_const _
  have hSecondMoment :
      ∫ omega,
          (InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
            population) ^ (2 : ℕ) ∂mu =
        population - population ^ (2 : ℕ) := by
    calc
      (∫ omega,
          (InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
            population) ^ (2 : ℕ) ∂mu) =
          ∫ omega,
            InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
              InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population -
              population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) +
              population ^ (2 : ℕ) ∂mu := by
        apply integral_congr_ae
        filter_upwards with omega
        have hp := rankOne_self_sq_of_norm_one (sample omega) (hsampleUnit omega)
        calc
          (InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
              population) ^ (2 : ℕ) =
              (InnerProductSpace.rankOne ℝ (sample omega) (sample omega)) ^ (2 : ℕ) -
                InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population -
                population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) +
                population ^ (2 : ℕ) := by
            noncomm_ring
          _ = _ := by rw [hp]
      _ = (∫ omega,
            InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) -
            (∫ omega,
              InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population ∂mu) -
            (∫ omega,
              population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) +
            (∫ _ : Omega, population ^ (2 : ℕ) ∂mu) := by
        have hthree :
            (∫ omega,
              InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
                InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population -
                population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) =
              (∫ omega,
                InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) -
              (∫ omega,
                InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population ∂mu) -
              (∫ omega,
                population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) := by
          have houter := integral_sub (hRankOneIntegrable.sub hright) hleft
          have hinner := integral_sub hRankOneIntegrable hright
          calc
            (∫ omega,
                InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
                  InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population -
                  population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) =
                (∫ omega,
                  InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
                    InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population ∂mu) -
                (∫ omega,
                  population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) := by
              simpa only [Pi.sub_apply] using houter
            _ = _ := by rw [hinner]
        have hadd := integral_add
          (hRankOneIntegrable.sub hright |>.sub hleft) hconst
        calc
          (∫ omega,
              InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
                InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population -
                population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) +
                population ^ (2 : ℕ) ∂mu) =
              (∫ omega,
                InnerProductSpace.rankOne ℝ (sample omega) (sample omega) -
                  InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population -
                  population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) +
              (∫ _ : Omega, population ^ (2 : ℕ) ∂mu) := by
            simpa only [Pi.add_apply, Pi.sub_apply] using hadd
          _ = _ := by rw [hthree]
      _ = population - population ^ (2 : ℕ) := by
        have hrightInt :
            (∫ omega,
              InnerProductSpace.rankOne ℝ (sample omega) (sample omega) * population ∂mu) =
              (∫ omega,
                InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) *
                population := by
          simpa [A, mul_apply_eq_comp] using
            ContinuousLinearMap.integral_comp_comm
              ((ContinuousLinearMap.mul ℝ A).flip population)
              hRankOneIntegrable
        have hleftInt :
            (∫ omega,
              population * InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) =
              population *
                (∫ omega,
                  InnerProductSpace.rankOne ℝ (sample omega) (sample omega) ∂mu) := by
          simpa [A, mul_apply_eq_comp] using
            ContinuousLinearMap.integral_comp_comm
              (ContinuousLinearMap.mul ℝ A population) hRankOneIntegrable
        rw [hPopulation, hrightInt, hleftInt]
        simp [hPopulation]
        noncomm_ring
  have hVariance :
      ‖population - population ^ (2 : ℕ)‖ ≤ 2 * ‖population‖ := by
    calc
      ‖population - population ^ (2 : ℕ)‖ ≤
          ‖population‖ + ‖population ^ (2 : ℕ)‖ := norm_sub_le _ _
      _ ≤ ‖population‖ + ‖population‖ ^ (2 : ℕ) := by
        gcongr
        exact norm_pow_le' _ (by norm_num)
      _ ≤ 2 * ‖population‖ := by
        nlinarith [norm_nonneg population]
  exact ⟨hSelfAdjoint, hNorm, hSecondMoment, hVariance⟩

end EmpiricalCovariance
end Probability
end TechnicalLemmas
end AutoSamplingTheory
