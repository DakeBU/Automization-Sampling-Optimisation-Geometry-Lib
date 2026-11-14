import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
import Mathlib.Analysis.Matrix.Order
import Mathlib.LinearAlgebra.Matrix.Kronecker

noncomputable section
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false

/-! The deterministic weighted coefficient comparison in arXiv2610.20492v1 C.2
EGx11. The canonical cosine-frame node supplies both Gram and norm conclusions.
Original-family Gaussian transport, centering and concentration remain separate. -/
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound

theorem actual_weighted_cosine_coefficient_bound
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let S : Fin d → ℝ := fun i => ∑ k : Fin (q + 1), (t i k) ^ 2
  let feature : Fin d → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun i => Matrix.vecMulVec (t i) (t i)
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let B : N := ((r + 2) / (d : ℝ) ^ 2) •
    ∑ i : Fin d, S i • Matrix.kronecker (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) (feature i)
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  Matrix.PosSemidef (C • (1 : N) - B) := by
  classical
  dsimp only
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let S : Fin d → ℝ := fun i => ∑ k : Fin (q + 1), (t i k) ^ 2
  let M := Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let feature : Fin d → M := fun i => Matrix.vecMulVec (t i) (t i)
  let K : Fin d → N := fun i => Matrix.kronecker (1 : M) (feature i)
  let α : ℝ := (r + 2) / (d : ℝ) ^ 2
  have frame := FixedSpectrumCosineGram.actual_cosine_frame_gram (d := d) (q := q) hq
  have norm_bound (i : Fin d) : S i ≤ 2 * r := by
    simpa only [r, Nat.cast_add, Nat.cast_one] using frame.2.2 i
  have gram : (∑ i : Fin d, feature i) = (d : ℝ) • (1 : M) := by
    have frame_gram : t.transpose * t = (d : ℝ) • (1 : M) := frame.1
    ext j k
    calc
      (∑ i : Fin d, feature i) j k = ∑ i : Fin d, t i j * t i k :=
        Matrix.sum_apply j k Finset.univ feature
      _ = ((d : ℝ) • (1 : M)) j k := by
        simpa only [Matrix.mul_apply, Matrix.transpose_apply] using
          congrFun (congrFun frame_gram j) k
  let tensor : M →ₗ[ℝ] N :=
    (Matrix.kroneckerBilinear : M →ₗ[ℝ] M →ₗ[ℝ] N) (1 : M)
  have tensor_gram : (∑ i : Fin d, K i) = (d : ℝ) • (1 : N) := by
    calc
      (∑ i : Fin d, K i) = tensor (∑ i : Fin d, feature i) := (map_sum tensor _ _).symm
      _ = (d : ℝ) • tensor (1 : M) := by rw [gram, map_smul]
      _ = (d : ℝ) • (1 : N) := by
        change (d : ℝ) • Matrix.kronecker (1 : M) (1 : M) = _
        dsimp only [Matrix.kronecker]
        rw [Matrix.one_kronecker_one]
  have K_positive (i : Fin d) : (K i).PosSemidef := by
    have F_positive : (feature i).PosSemidef := by
      simpa only [star_trivial] using Matrix.posSemidef_vecMulVec_self_star (t i)
    exact (Matrix.PosSemidef.one : (1 : M).PosSemidef).kronecker F_positive
  have residual_positive :
      (∑ i : Fin d, (2 * r - S i) • K i).PosSemidef :=
    Matrix.posSemidef_sum Finset.univ (fun i _ =>
      (K_positive i).smul (sub_nonneg.mpr (norm_bound i)))
  have scalar_nonnegative : 0 ≤ α := by
    exact div_nonneg (by dsimp [r]; positivity) (sq_nonneg _)
  have constant_sum :
      (∑ i : Fin d, (2 * r) • K i) = (2 * r * (d : ℝ)) • (1 : N) := by
    rw [← Finset.smul_sum, tensor_gram, smul_smul]
  have residual_identity :
      (2 * r * (r + 2) / (d : ℝ)) • (1 : N) -
        α • (∑ i : Fin d, S i • K i) =
          α • (∑ i : Fin d, (2 * r - S i) • K i) := by
    simp_rw [sub_smul]
    rw [Finset.sum_sub_distrib, constant_sum, smul_sub, smul_smul]
    congr 1
    have hd : (d : ℝ) ≠ 0 := by exact_mod_cast (show d ≠ 0 by omega)
    dsimp [α]
    field_simp
  change ((2 * r * (r + 2) / (d : ℝ)) • (1 : N) -
    α • (∑ i : Fin d, S i • K i)).PosSemidef
  rw [residual_identity]
  exact residual_positive.smul scalar_nonnegative

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound
