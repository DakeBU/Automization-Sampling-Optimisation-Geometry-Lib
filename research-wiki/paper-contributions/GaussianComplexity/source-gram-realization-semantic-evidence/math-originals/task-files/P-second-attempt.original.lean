import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram

/-! Actual original-experiment centered Gram realizations on the literal closed
all-row cutoff event. Actual means and cosine-frame sums are internal inputs;
no arbitrary B, mean, Gram, frame, bias or probability certificate is supplied. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceGramRealization

theorem actual_source_centered_gram_realizations
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let a : ℝ := (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L}
    (fun y : E => ‖y‖ ^ 2) x ∂stdGaussian E) / r
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let B : Ω → Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun ω i u =>
    (Real.sqrt (d : ℝ))⁻¹ * (row i ω) u.1 * t i u.2
  let G : Ω → Prop := fun ω => ∀ i : Fin d, ‖row i ω‖ ^ 2 ≤ L
  ∀ ω : Ω, G ω →
    ((∑ i : Fin d, Z i ω) =
      (B ω).transpose * B ω - a •
        (1 : Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)) ∧
    ((∑ i : Fin d, w i • Z i ω) =
      (B ω).transpose * Matrix.diagonal w * B ω)
 := by
  classical
  dsimp only
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let a : ℝ := (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L}
    (fun y : E => ‖y‖ ^ 2) x ∂stdGaussian E) / r
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let B : Ω → Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun ω i u =>
    (Real.sqrt (d : ℝ))⁻¹ * (row i ω) u.1 * t i u.2
  let G : Ω → Prop := fun ω => ∀ i : Fin d, ‖row i ω‖ ^ 2 ≤ L
  let M := Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let feature : Fin d → M := fun i => Matrix.vecMulVec (t i) (t i)
  let tensor : M →ₗ[ℝ] N :=
    (Matrix.kroneckerBilinear : M →ₗ[ℝ] M →ₗ[ℝ] N) (1 : M)
  let K : Fin d → N := fun i => tensor (feature i)
  have moments := FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means
    (d := d) (q := q) hq
  change (∀ i : Fin d, Integrable (Y i) μ) ∧
    (∀ i : Fin d, (∫ ω, Y i ω ∂μ) = (a / (d : ℝ)) • K i) at moments
  have half_grid (i : Fin d) :
      ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ) = θ i := by
    dsimp only [θ]
    ring
  have frame := FixedSpectrumCosineGram.actual_cosine_frame_gram (d := d) (q := q) hq
  dsimp only at frame
  simp_rw [half_grid] at frame
  change t.transpose * t = (d : ℝ) • (1 : M) ∧
    t.transpose * Matrix.diagonal w * t = 0 ∧ _ at frame
  have gram : (∑ i : Fin d, feature i) = (d : ℝ) • (1 : M) := by
    ext j k
    calc
      (∑ i : Fin d, feature i) j k = ∑ i : Fin d, t i j * t i k :=
        Matrix.sum_apply j k Finset.univ feature
      _ = ((d : ℝ) • (1 : M)) j k := by
        simpa only [Matrix.mul_apply, Matrix.transpose_apply] using
          congrFun (congrFun frame.1 j) k
  have weighted_gram : (∑ i : Fin d, w i • feature i) = 0 := by
    ext j k
    have weighted_entry := congrFun (congrFun frame.2.1 j) k
    change (∑ i : Fin d, (t.transpose * Matrix.diagonal w) j i * t i k) = 0 at weighted_entry
    simp only [Matrix.mul_diagonal, Matrix.transpose_apply] at weighted_entry
    calc
      (∑ i : Fin d, w i • feature i) j k = ∑ i : Fin d, w i * (t i j * t i k) :=
        Matrix.sum_apply j k Finset.univ (fun i => w i • feature i)
      _ = ∑ i : Fin d, t i j * w i * t i k := by
        apply Finset.sum_congr rfl
        intro i _
        ring
      _ = (0 : M) j k := weighted_entry
  have tensor_one : tensor (1 : M) = (1 : N) := by
    change Matrix.kronecker (1 : M) (1 : M) = (1 : N)
    dsimp only [Matrix.kronecker]
    exact Matrix.one_kronecker_one
  have tensor_gram : (∑ i : Fin d, K i) = (d : ℝ) • (1 : N) := by
    calc
      (∑ i : Fin d, K i) = tensor (∑ i : Fin d, feature i) := (map_sum tensor _ _).symm
      _ = (d : ℝ) • tensor (1 : M) := by rw [gram, map_smul]
      _ = (d : ℝ) • (1 : N) := by rw [tensor_one]
  have weighted_tensor : (∑ i : Fin d, w i • K i) = 0 := by
    calc
      (∑ i : Fin d, w i • K i) = tensor (∑ i : Fin d, w i • feature i) := by
        simp only [map_sum, map_smul]
        rfl
      _ = 0 := by rw [weighted_gram, map_zero]
  have hd : (d : ℝ) ≠ 0 := by exact_mod_cast (show d ≠ 0 by omega)
  have mean_sum : (∑ i : Fin d, ∫ ω, Y i ω ∂μ) = a • (1 : N) := by
    calc
      (∑ i : Fin d, ∫ ω, Y i ω ∂μ) = (a / (d : ℝ)) • (∑ i : Fin d, K i) := by
        simp_rw [moments.2]
        exact Finset.smul_sum.symm
      _ = a • (1 : N) := by
        rw [tensor_gram, smul_smul, div_mul_cancel₀ a hd]
  have weighted_mean_sum : (∑ i : Fin d, w i • (∫ ω, Y i ω ∂μ)) = 0 := by
    calc
      (∑ i : Fin d, w i • (∫ ω, Y i ω ∂μ)) =
          (a / (d : ℝ)) • (∑ i : Fin d, w i • K i) := by
        rw [Finset.smul_sum]
        apply Finset.sum_congr rfl
        intro i _
        rw [moments.2 i]
        exact smul_comm _ _ _
      _ = 0 := by rw [weighted_tensor, smul_zero]
  have inv_sqrt_square :
      (Real.sqrt (d : ℝ))⁻¹ * (Real.sqrt (d : ℝ))⁻¹ = (d : ℝ)⁻¹ := by
    calc
      _ = ((Real.sqrt (d : ℝ)) ^ 2)⁻¹ := by rw [pow_two, mul_inv]
      _ = _ := by rw [Real.sq_sqrt (by positivity)]
  have actual_row_outer (i : Fin d) (ω : Ω) (hi : ‖row i ω‖ ^ 2 ≤ L)
      (u v : Fin (q + 1) × Fin (q + 1)) :
      B ω i u * B ω i v = Y i ω u v := by
    calc
      _ = ((Real.sqrt (d : ℝ))⁻¹ * (Real.sqrt (d : ℝ))⁻¹) *
          ((row i ω u.1 * row i ω v.1) * (t i u.2 * t i v.2)) := by
        dsimp only [B]
        ring
      _ = _ := by
        rw [inv_sqrt_square]
        simp only [Y, if_pos hi, Matrix.smul_apply, Matrix.kronecker,
          Matrix.kroneckerMap_apply, Matrix.vecMulVec_apply, smul_eq_mul]
        rfl
  have actual_gram (ω : Ω) (hG : G ω) :
      (B ω).transpose * B ω = ∑ i : Fin d, Y i ω := by
    ext u v
    simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.sum_apply]
    apply Finset.sum_congr rfl
    intro i _
    exact actual_row_outer i ω (hG i) u v
  have actual_weighted_gram (ω : Ω) (hG : G ω) :
      (B ω).transpose * Matrix.diagonal w * B ω = ∑ i : Fin d, w i • Y i ω := by
    ext u v
    simp only [Matrix.mul_apply, Matrix.mul_diagonal, Matrix.transpose_apply,
      Matrix.sum_apply, Matrix.smul_apply, smul_eq_mul]
    apply Finset.sum_congr rfl
    intro i _
    calc
      B ω i u * w i * B ω i v = w i * (B ω i u * B ω i v) := by ring
      _ = w i * Y i ω u v := by rw [actual_row_outer i ω (hG i) u v]
  change ∀ ω : Ω, G ω →
    ((∑ i : Fin d, Z i ω) = (B ω).transpose * B ω - a • (1 : N)) ∧
    ((∑ i : Fin d, w i • Z i ω) = (B ω).transpose * Matrix.diagonal w * B ω)
  intro ω hG
  constructor
  · calc
      (∑ i : Fin d, Z i ω) = (∑ i : Fin d, Y i ω) - a • (1 : N) := by
        simp only [Z, mean, Finset.sum_sub_distrib, mean_sum]
      _ = _ := by rw [actual_gram ω hG]
  · calc
      (∑ i : Fin d, w i • Z i ω) =
          (∑ i : Fin d, w i • Y i ω) - (∑ i : Fin d, w i • mean i) := by
        simp only [Z, smul_sub, Finset.sum_sub_distrib]
      _ = (∑ i : Fin d, w i • Y i ω) := by
        change (∑ i : Fin d, w i • Y i ω) -
          (∑ i : Fin d, w i • (∫ ω, Y i ω ∂μ)) = _
        rw [weighted_mean_sum, sub_zero]
      _ = _ := (actual_weighted_gram ω hG).symm

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceGramRealization
