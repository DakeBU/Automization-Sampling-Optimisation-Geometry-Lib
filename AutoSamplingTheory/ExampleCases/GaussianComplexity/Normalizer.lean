import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.LinearAlgebra.Matrix.DotProduct
import Mathlib.LinearAlgebra.Matrix.ToLinearEquiv
import Mathlib.Topology.Instances.Matrix
import Mathlib.Topology.Order.IntermediateValue

/-!
# The determinant family's normalization factor

Equations (16)--(18) in the proof of Lemma B.6 of Zhou--Suzuki,
arXiv:2610.20492v1. These are pointwise matrix identities. The Haar expectation
and principal-minor cancellation in the rest of Lemma B.6 remain separate.
-/

open Matrix Set

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

/-- Source equation (16), for the literal equation-(4) precision. -/
theorem singleBlockPrecision_factorization {n : ℕ} (_hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) (O : Matrix.orthogonalGroup (Fin n) ℝ) :
    singleBlockPrecision κ O = (1 / 4 : ℝ) •
      ((((Real.sqrt κ + 1) • (1 : Matrix (Fin n) (Fin n) ℝ) -
        (Real.sqrt κ - 1) • (O : Matrix (Fin n) (Fin n) ℝ)).transpose) *
       ((Real.sqrt κ + 1) • (1 : Matrix (Fin n) (Fin n) ℝ) -
        (Real.sqrt κ - 1) • (O : Matrix (Fin n) (Fin n) ℝ))) := by
  have horth : (O : Matrix (Fin n) (Fin n) ℝ).transpose *
      (O : Matrix (Fin n) (Fin n) ℝ) = 1 :=
    (Matrix.mem_orthogonalGroup_iff' (Fin n) ℝ).mp O.property
  simp only [Matrix.transpose_sub, Matrix.transpose_smul, Matrix.transpose_one,
    Matrix.sub_mul, Matrix.mul_sub, Matrix.smul_mul, Matrix.mul_smul,
    Matrix.one_mul, Matrix.mul_one, horth]
  ext i j
  simp only [singleBlockPrecision, Matrix.sub_apply, Matrix.add_apply,
    Matrix.smul_apply, smul_eq_mul]
  ring_nf
  rw [Real.sq_sqrt (by linarith : 0 ≤ κ)]
  ring

private theorem shiftedOrthogonal_det_pos {n : ℕ}
    (O : Matrix.orthogonalGroup (Fin n) ℝ) {a b : ℝ}
    (hb : 0 ≤ b) (hab : b < a) :
    0 < (a • (1 : Matrix (Fin n) (Fin n) ℝ) -
      b • (O : Matrix (Fin n) (Fin n) ℝ)).det := by
  let f : ℝ → ℝ := fun t =>
    (a • (1 : Matrix (Fin n) (Fin n) ℝ) -
      t • (O : Matrix (Fin n) (Fin n) ℝ)).det
  have horth : (O : Matrix (Fin n) (Fin n) ℝ).transpose *
      (O : Matrix (Fin n) (Fin n) ℝ) = 1 :=
    (Matrix.mem_orthogonalGroup_iff' (Fin n) ℝ).mp O.property
  have hiso (v : Fin n → ℝ) :
      ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v) ⬝ᵥ
        ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v) = v ⬝ᵥ v := by
    rw [dotProduct_comm, ← Matrix.dotProduct_transpose_mulVec,
      Matrix.mulVec_mulVec, horth, Matrix.one_mulVec]
  have hne (t : ℝ) (ht : t ∈ Icc 0 b) : f t ≠ 0 := by
    intro hz
    obtain ⟨v, hv, hker⟩ := Matrix.exists_mulVec_eq_zero_iff.mpr hz
    have hq : 0 < v ⬝ᵥ v :=
      lt_of_le_of_ne (Finset.sum_nonneg (fun i _ => mul_self_nonneg (v i)))
        (Ne.symm (fun hz => hv (dotProduct_self_eq_zero.mp hz)))
    have heq : a • v = t • ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v) := by
      simpa only [Matrix.sub_mulVec, Matrix.smul_mulVec, Matrix.one_mulVec,
        sub_eq_zero] using hker
    have hsq := congrArg (fun w : Fin n → ℝ => w ⬝ᵥ w) heq
    simp only [smul_dotProduct, dotProduct_smul, smul_eq_mul, hiso] at hsq
    have hfactor : 0 < a * a - t * t := by nlinarith [ht.1, ht.2]
    have := mul_pos hfactor hq
    nlinarith
  have hcont : Continuous f := by
    apply Continuous.matrix_det
    exact continuous_const.sub (continuous_id.smul continuous_const)
  have hzero : 0 < f 0 := by
    simpa [f, Matrix.det_smul] using pow_pos (lt_of_le_of_lt hb hab) n
  change 0 < f b
  by_contra! hnonpos
  obtain ⟨t, ht, hz⟩ := intermediate_value_Icc' hb hcont.continuousOn
    (show (0 : ℝ) ∈ Icc (f b) (f 0) from ⟨hnonpos, hzero.le⟩)
  exact hne t ht hz

/-- Source equation (17); the sign is proved through a nonsingular continuous path. -/
theorem singleBlockPrecision_sqrt_det {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) (O : Matrix.orthogonalGroup (Fin n) ℝ) :
    Real.sqrt (singleBlockPrecision κ O).det = (1 / (2 : ℝ) ^ n) *
      (((Real.sqrt κ + 1) • (1 : Matrix (Fin n) (Fin n) ℝ) -
        (Real.sqrt κ - 1) • (O : Matrix (Fin n) (Fin n) ℝ)).det) := by
  have hs : 2 ≤ Real.sqrt κ := by
    nlinarith [Real.sq_sqrt (by linarith : 0 ≤ κ), Real.sqrt_nonneg κ]
  have hpos := shiftedOrthogonal_det_pos O
    (show 0 ≤ Real.sqrt κ - 1 by linarith)
    (show Real.sqrt κ - 1 < Real.sqrt κ + 1 by linarith)
  apply (Real.sqrt_eq_iff_mul_self_eq_of_pos (mul_pos (by positivity) hpos)).2
  rw [singleBlockPrecision_factorization hn hκ O, Matrix.det_smul,
    Matrix.det_mul, Matrix.det_transpose, Fintype.card_fin]
  have hquarter : (1 / 4 : ℝ) = (1 / 2) * (1 / 2) := by norm_num
  rw [hquarter, mul_pow, _root_.one_div_pow]
  ring

/-- Both equalities of source equation (18), with its last transpose already taken. -/
theorem singleBlockPrecision_signed_sqrt_det {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) (O : Matrix.orthogonalGroup (Fin n) ℝ) :
    (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det =
      (1 / (2 : ℝ) ^ n) *
      (((Real.sqrt κ + 1) • (O : Matrix (Fin n) (Fin n) ℝ) -
        (Real.sqrt κ - 1) • (1 : Matrix (Fin n) (Fin n) ℝ)).det) := by
  have horth : (O : Matrix (Fin n) (Fin n) ℝ).transpose *
      (O : Matrix (Fin n) (Fin n) ℝ) = 1 :=
    (Matrix.mem_orthogonalGroup_iff' (Fin n) ℝ).mp O.property
  have hmatrix : (O : Matrix (Fin n) (Fin n) ℝ).transpose *
      ((Real.sqrt κ + 1) • (1 : Matrix (Fin n) (Fin n) ℝ) -
        (Real.sqrt κ - 1) • (O : Matrix (Fin n) (Fin n) ℝ)) =
      ((Real.sqrt κ + 1) • (O : Matrix (Fin n) (Fin n) ℝ) -
        (Real.sqrt κ - 1) • (1 : Matrix (Fin n) (Fin n) ℝ)).transpose := by
    simp only [Matrix.mul_sub, Matrix.mul_smul, Matrix.mul_one, horth,
      Matrix.transpose_sub, Matrix.transpose_smul, Matrix.transpose_one]
  have hdet := congrArg Matrix.det hmatrix
  rw [Matrix.det_mul, Matrix.det_transpose, Matrix.det_transpose] at hdet
  rw [singleBlockPrecision_sqrt_det hn hκ O]
  calc
    _ = (1 / (2 : ℝ) ^ n) *
        ((O : Matrix (Fin n) (Fin n) ℝ).det *
          ((Real.sqrt κ + 1) • (1 : Matrix (Fin n) (Fin n) ℝ) -
            (Real.sqrt κ - 1) • (O : Matrix (Fin n) (Fin n) ℝ)).det) := by ring
    _ = _ := by rw [hdet]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
