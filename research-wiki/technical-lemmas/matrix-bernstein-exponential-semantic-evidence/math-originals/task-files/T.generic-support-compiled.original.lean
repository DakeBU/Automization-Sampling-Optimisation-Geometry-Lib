import AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential
import AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure

open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder

noncomputable section

universe u

namespace AutoSamplingTheory.Tests.GaussianComplexityBernsteinMgf

private lemma one_sub_posSemidef_of_norm_le_one
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (hn : ‖A‖ ≤ 1) :
    (1 - A).PosSemidef := by
  have hspec : ∀ x ∈ spectrum ℝ A, x ≤ 1 := by
    intro x hx
    exact (Real.le_norm_self x).trans
      ((IsometricContinuousFunctionalCalculus.norm_spectrum_le A hx hA.isSelfAdjoint).trans hn)
  exact Matrix.le_iff.mp ((CFC.le_one_iff (R := ℝ) A hA.isSelfAdjoint).mpr hspec)

private lemma capped_matrix_exp_norm_le
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (hcap : (1 - A).PosSemidef)
    {s : ℝ} (hs : 0 < s) : ‖NormedSpace.exp (s • A)‖ ≤ Real.exp s := by
  have hSA : IsSelfAdjoint A := hA.isSelfAdjoint
  have hspec : ∀ x ∈ spectrum ℝ A, x ≤ 1 :=
    (CFC.le_one_iff (R := ℝ) A hSA).mp (Matrix.le_iff.mpr hcap)
  have heq : cfc (fun x : ℝ => Real.exp (s * x)) A = NormedSpace.exp (s • A) := by
    calc
      _ = cfc Real.exp (s • A) := cfc_comp_const_mul s Real.exp A (by fun_prop) hSA
      _ = _ := CFC.real_exp_eq_normedSpace_exp ((IsSelfAdjoint.all s).smul hSA)
  rw [← heq]
  apply norm_cfc_le (Real.exp_nonneg s)
  intro x hx
  rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
  apply Real.exp_le_exp.mpr
  simpa only [mul_one] using mul_le_mul_of_nonneg_left (hspec x hx) hs.le

private lemma exp_sub_one_add_posSemidef
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) :
    (NormedSpace.exp A - (1 + A)).PosSemidef := by
  have hSA : IsSelfAdjoint A := hA.isSelfAdjoint
  have hfc : cfc (fun x : ℝ => 1 + x) A ≤ cfc Real.exp A :=
    cfc_mono (a := A) (fun x _ => by linarith [Real.add_one_le_exp x])
      (by fun_prop) (by fun_prop)
  have hlin : cfc (fun x : ℝ => 1 + x) A = (1 : Matrix ι ι ℝ) + A := by
    rw [cfc_add (a := A) (fun _ : ℝ => 1) (fun x : ℝ => x) (by fun_prop) (by fun_prop),
      cfc_const (R := ℝ) 1 A hSA, cfc_id' ℝ A hSA, map_one]
  exact Matrix.le_iff.mp
    (by simpa only [hlin, CFC.real_exp_eq_normedSpace_exp hSA] using hfc)

end AutoSamplingTheory.Tests.GaussianComplexityBernsteinMgf
