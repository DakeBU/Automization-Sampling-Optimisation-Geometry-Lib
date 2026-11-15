import Mathlib.Analysis.Matrix.Order
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.ExpLog.Basic

/-!
# Scalar trace-exponential envelope for finite real Hermitian matrices

The ordinary trace is strictly positive and bounded by the matrix dimension
times the exponential of the absolute parameter times the L2 operator norm.
This is a deterministic canonical library fact for every real parameter;
it does not assert a matrix-valued moment generating function or a tail bound.
-/

open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder
noncomputable section
universe u
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds

theorem trace_exp_pos_and_le_card_mul_exp_abs_mul_norm :
∀ {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι],
  ∀ (A : Matrix ι ι ℝ), A.IsHermitian → ∀ s : ℝ,
    0 < Matrix.trace (NormedSpace.exp (s • A)) ∧
      Matrix.trace (NormedSpace.exp (s • A)) ≤
        (Fintype.card ι : ℝ) * Real.exp (|s| * ‖A‖)
 := by
  classical
  intro ι _ _ _ A hA s
  have heq : cfc (fun x : ℝ => Real.exp (s * x)) A =
      NormedSpace.exp (s • A) := by
    calc
      _ = cfc Real.exp (s • A) :=
        cfc_comp_const_mul s Real.exp A (by fun_prop) hA.isSelfAdjoint
      _ = _ := CFC.real_exp_eq_normedSpace_exp
        ((IsSelfAdjoint.all s).smul hA.isSelfAdjoint)
  have hpos : IsStrictlyPositive (cfc (fun x : ℝ => Real.exp (s * x)) A) :=
    (cfc_isStrictlyPositive_iff (fun x : ℝ => Real.exp (s * x)) A
      (by fun_prop) hA.isSelfAdjoint).mpr (fun x _ => Real.exp_pos (s * x))
  have htracepos := (Matrix.isStrictlyPositive_iff_posDef.mp hpos).trace_pos
  let C : ℝ := Real.exp (|s| * ‖A‖)
  have hupper : cfc (fun x : ℝ => Real.exp (s * x)) A ≤
      algebraMap ℝ (Matrix ι ι ℝ) C := by
    apply (cfc_le_algebraMap_iff (fun x : ℝ => Real.exp (s * x)) C A
      (by fun_prop) hA.isSelfAdjoint).mpr
    intro x hx
    apply Real.exp_le_exp.mpr
    have hnormx : |x| ≤ ‖A‖ := by
      simpa only [Real.norm_eq_abs] using
        IsometricContinuousFunctionalCalculus.norm_spectrum_le A hx hA.isSelfAdjoint
    calc
      s * x ≤ |s * x| := le_abs_self _
      _ = |s| * |x| := abs_mul _ _
      _ ≤ |s| * ‖A‖ := mul_le_mul_of_nonneg_left hnormx (abs_nonneg _)
  have htrace := (Matrix.le_iff.mp hupper).trace_nonneg
  simp only [Matrix.trace_sub, Algebra.algebraMap_eq_smul_one,
    Matrix.trace_smul, Matrix.trace_one, smul_eq_mul] at htrace
  refine ⟨?_, ?_⟩
  · simpa only [heq] using htracepos
  · have hle := sub_nonneg.mp htrace
    simpa only [heq, C, mul_comm] using hle

end AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds
