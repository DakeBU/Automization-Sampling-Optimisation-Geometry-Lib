import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.LinearMap

/-!
# Actual truncated Gaussian summand and mean norms

The literal original product experiment and closed cutoff are unchanged.
All moment, sign and operator-norm estimates are internal proof obligations.
-/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius

private theorem matrix_outer_norm {n : Type*} [Fintype n] [DecidableEq n]
    (u : EuclideanSpace ℝ n) :
    ‖Matrix.vecMulVec u.ofLp u.ofLp‖ = ‖u‖ ^ 2 := by
  have he : Matrix.toEuclideanLin.symm
      (InnerProductSpace.rankOne ℝ u u : EuclideanSpace ℝ n →ₗ[ℝ] EuclideanSpace ℝ n) =
      Matrix.vecMulVec u.ofLp u.ofLp := by
    simpa only [star_trivial] using InnerProductSpace.symm_toEuclideanLin_rankOne u u
  have hl : Matrix.toEuclideanLin (Matrix.vecMulVec u.ofLp u.ofLp) =
      (InnerProductSpace.rankOne ℝ u u : EuclideanSpace ℝ n →ₗ[ℝ] EuclideanSpace ℝ n) := by
    rw [← he, LinearEquiv.apply_symm_apply]
  have hc : Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) (Matrix.vecMulVec u.ofLp u.ofLp) =
      InnerProductSpace.rankOne ℝ u u := by
    apply ContinuousLinearMap.ext
    intro x
    exact congrArg (fun f : EuclideanSpace ℝ n →ₗ[ℝ] EuclideanSpace ℝ n => f x) hl
  rw [Matrix.cstar_norm_def, hc, InnerProductSpace.norm_rankOne, ← pow_two]

private theorem rankone_tensor_norm {m n : Type*} [Fintype m] [Fintype n]
    [DecidableEq m] [DecidableEq n]
    (u : EuclideanSpace ℝ m) (v : EuclideanSpace ℝ n) :
    ‖Matrix.kronecker (Matrix.vecMulVec u.ofLp u.ofLp)
        (Matrix.vecMulVec v.ofLp v.ofLp)‖ = ‖u‖ ^ 2 * ‖v‖ ^ 2 := by
  let z : EuclideanSpace ℝ (m × n) := WithLp.toLp 2 (fun ij => u ij.1 * v ij.2)
  have hz : Matrix.kronecker (Matrix.vecMulVec u.ofLp u.ofLp)
      (Matrix.vecMulVec v.ofLp v.ofLp) = Matrix.vecMulVec z.ofLp z.ofLp := by
    ext i j
    dsimp [Matrix.kronecker, Matrix.kroneckerMap, Matrix.vecMulVec, z]
    ring
  rw [hz, matrix_outer_norm, EuclideanSpace.norm_sq_eq, EuclideanSpace.norm_sq_eq,
    EuclideanSpace.norm_sq_eq, Fintype.sum_prod_type]
  simp only [z, Real.norm_eq_abs, sq_abs, mul_pow]
  rw [Finset.sum_mul_sum]

private theorem identity_rankone_norm {m n : Type*} [Fintype m] [Fintype n]
    [DecidableEq m] [DecidableEq n] [Nonempty m] (v : n → ℝ) :
    ‖Matrix.kronecker (1 : Matrix m m ℝ) (Matrix.vecMulVec v v)‖ =
      ∑ j : n, (v j) ^ 2 := by
  classical
  let F : Matrix n n ℝ := Matrix.vecMulVec v v
  let K : Matrix (m × n) (m × n) ℝ := Matrix.kronecker (1 : Matrix m m ℝ) F
  let S : ℝ := ∑ j : n, (v j) ^ 2
  change ‖K‖ = S
  have hS : 0 ≤ S := Finset.sum_nonneg (fun _ _ => sq_nonneg _)
  have hF : F * F = S • F := by
    ext j k
    change (∑ a : n, (v j * v a) * (v a * v k)) =
      (∑ a : n, (v a) ^ 2) * (v j * v k)
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro a _
    ring
  have hstar : K.conjTranspose = K := by
    dsimp only [K, Matrix.kronecker]
    rw [Matrix.conjTranspose_kronecker, Matrix.conjTranspose_one]
    simp [F]
  have hKsq : K * K = S • K := by
    dsimp only [K, Matrix.kronecker]
    rw [← Matrix.mul_kronecker_mul, Matrix.one_mul, hF, Matrix.kronecker_smul]
  have hn : S * ‖K‖ = ‖K‖ * ‖K‖ := by
    have h := Matrix.l2_opNorm_conjTranspose_mul_self K
    rw [hstar, hKsq, norm_smul, Real.norm_eq_abs, abs_of_nonneg hS] at h
    exact h
  by_cases hv : v = 0
  · simp [K, F, S, hv]
  · obtain ⟨j, hj⟩ : ∃ j : n, v j ≠ 0 := by
      by_contra! h
      exact hv (funext h)
    let i : m := Classical.choice inferInstance
    have hKne : K ≠ 0 := by
      intro hzero
      have hentry := congrArg
        (fun A : Matrix (m × n) (m × n) ℝ => A (i, j) (i, j)) hzero
      have hsq : v j * v j = 0 := by
        simpa [K, F, Matrix.kronecker, Matrix.vecMulVec] using hentry
      exact (mul_ne_zero hj hj) hsq
    have hnorm : ‖K‖ ≠ 0 := norm_ne_zero_iff.mpr hKne
    have hp : (‖K‖ - S) * ‖K‖ = 0 := by nlinarith [hn]
    rcases mul_eq_zero.mp hp with hs | hz
    · exact sub_eq_zero.mp hs
    · exact (hnorm hz).elim


theorem actual_source_truncated_matrix_norm_bounds
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
  (∀ i : Fin d, ∀ ω : Ω, ‖Y i ω‖ ≤ 2 * r * L / (d : ℝ)) ∧
    (∀ i : Fin d, ‖∫ ω, Y i ω ∂μ‖ ≤ 2 * r / (d : ℝ))
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
  let S : Fin d → ℝ := fun i => ∑ k : Fin (q + 1), (t i k) ^ 2
  let F : Fin d → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun i => Matrix.vecMulVec (t i) (t i)
  let K : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => Matrix.kronecker (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) (F i)
  let a : ℝ := (∫ x : E, {y : E | ‖y‖ ^ 2 ≤ L}.indicator
    (fun y => ‖y‖ ^ 2) x ∂stdGaussian E) / r
  change (∀ i : Fin d, ∀ ω : Ω, ‖Y i ω‖ ≤ 2 * r * L / (d : ℝ)) ∧
    (∀ i : Fin d, ‖∫ ω, Y i ω ∂μ‖ ≤ 2 * r / (d : ℝ))
  have hd : (0 : ℝ) < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have hr : 0 < r := by dsimp [r]; positivity
  have hscale : (1 : ℝ) ≤ 1000 * (d : ℝ) := by
    have hd2 : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast (show 2 ≤ d by omega)
    linarith
  have hL : 0 ≤ L := by
    have hlog := Real.log_nonneg hscale
    dsimp only [L]
    linarith
  have hS0 (i : Fin d) : 0 ≤ S i := Finset.sum_nonneg (fun _ _ => sq_nonneg _)
  have frame := FixedSpectrumCosineGram.actual_cosine_frame_gram (d := d) (q := q) hq
  have hS (i : Fin d) : S i ≤ 2 * r := by
    simpa only [S, t, θ, r, Nat.cast_add, Nat.cast_one, add_sub_assoc,
      show (1 : ℝ) - 1 / 2 = 1 / 2 by norm_num] using frame.2.2 i
  have hm := FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means
    (d := d) (q := q) hq
  change (∀ i : Fin d, Integrable (Y i) μ) ∧
    (∀ i : Fin d, (∫ ω, Y i ω ∂μ) = (a / (d : ℝ)) • K i) at hm
  have moment := AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian
    (E := E)
  have hgood : MeasurableSet {y : E | ‖y‖ ^ 2 ≤ L} :=
    measurableSet_le (by fun_prop) measurable_const
  have hret := moment.1.indicator hgood
  have hret0 : 0 ≤ ∫ x : E, {y : E | ‖y‖ ^ 2 ≤ L}.indicator
      (fun y => ‖y‖ ^ 2) x ∂stdGaussian E := by
    apply integral_nonneg
    intro x
    by_cases hx : ‖x‖ ^ 2 ≤ L
    · simpa [Set.indicator, hx] using sq_nonneg ‖x‖
    · simp [Set.indicator, hx]
  have hretle : (∫ x : E, {y : E | ‖y‖ ^ 2 ≤ L}.indicator
      (fun y => ‖y‖ ^ 2) x ∂stdGaussian E) ≤ r := by
    calc
      _ ≤ ∫ x : E, ‖x‖ ^ 2 ∂stdGaussian E := by
        apply integral_mono hret moment.1
        intro x
        by_cases hx : ‖x‖ ^ 2 ≤ L
        · simp [Set.indicator, hx]
        · simpa [Set.indicator, hx] using sq_nonneg ‖x‖
      _ = r := by simpa [E, r] using moment.2
  have ha0 : 0 ≤ a := div_nonneg hret0 hr.le
  have ha1 : a ≤ 1 := (div_le_one hr).2 hretle
  have hK (i : Fin d) : ‖K i‖ = S i := identity_rankone_norm
    (m := Fin (q + 1)) (t i)
  constructor
  · intro i ω
    have htnorm : ‖(WithLp.toLp 2 (t i) : E)‖ ^ 2 = S i := by
      simp [EuclideanSpace.norm_sq_eq, S, Real.norm_eq_abs, sq_abs]
    have hTensor : ‖Matrix.kronecker
        (Matrix.vecMulVec (row i ω).ofLp (row i ω).ofLp)
        (Matrix.vecMulVec (t i) (t i))‖ = ‖row i ω‖ ^ 2 * S i := by
      simpa only [WithLp.ofLp_toLp, htnorm] using
        rankone_tensor_norm (row i ω) (WithLp.toLp 2 (t i) : E)
    by_cases hx : ‖row i ω‖ ^ 2 ≤ L
    · dsimp only [Y]
      rw [if_pos hx, norm_smul, Real.norm_eq_abs,
        abs_of_nonneg (inv_nonneg.mpr hd.le), hTensor]
      calc
        _ ≤ (d : ℝ)⁻¹ * (L * (2 * r)) :=
          mul_le_mul_of_nonneg_left (mul_le_mul hx (hS i) (hS0 i) hL)
            (inv_nonneg.mpr hd.le)
        _ = 2 * r * L / (d : ℝ) := by rw [div_eq_mul_inv]; ring
    · simp only [Y, if_neg hx, norm_zero]
      exact div_nonneg (mul_nonneg (mul_nonneg (by norm_num) hr.le) hL) hd.le
  · intro i
    rw [hm.2 i, norm_smul, Real.norm_eq_abs,
      abs_of_nonneg (div_nonneg ha0 hd.le), hK]
    calc
      _ ≤ (1 / (d : ℝ)) * (2 * r) :=
        mul_le_mul ((div_le_div_iff_of_pos_right hd).2 ha1) (hS i) (hS0 i)
          (div_nonneg zero_le_one hd.le)
      _ = 2 * r / (d : ℝ) := by ring

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
