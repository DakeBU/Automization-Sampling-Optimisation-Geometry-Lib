import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Analysis.Convex.Integral

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped Matrix.Norms.L2Operator
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment
set_option autoImplicit false

namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumRadialFourthMoment

private theorem actual_truncated_summand_second_moment_bound
    {d q : ℕ} (hq : 2 * q + 1 < d) (i : Fin d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun j => ((j.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun j k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ j)
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let feature : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    Matrix.vecMulVec (t i) (t i)
  let Y : E → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    Set.indicator {y : E | R y ≤ L}
      (fun x => (d : ℝ)⁻¹ • Matrix.kronecker (G x) feature)
  let squared := fun x => Y x * Y x
  let upper : Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    (((r + 2) * (∑ k : Fin (q + 1), (t i k) ^ 2)) / (d : ℝ) ^ 2) •
      Matrix.kronecker (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) feature
  Integrable squared μ ∧ Matrix.PosSemidef (upper - (∫ x, squared x ∂μ)) := by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun j => ((j.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun j k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ j)
  let M := Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let G : E → M := fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let weighted : E → M := fun x => R x • G x
  let feature : M := Matrix.vecMulVec (t i) (t i)
  let S : ℝ := ∑ k : Fin (q + 1), (t i k) ^ 2
  let c : ℝ := S / (d : ℝ) ^ 2
  let good : Set E := {y | R y ≤ L}
  let Y : E → N := good.indicator (fun x => (d : ℝ)⁻¹ • Matrix.kronecker (G x) feature)
  let squared : E → N := fun x => Y x * Y x
  let upper : N := (((r + 2) * S) / (d : ℝ) ^ 2) • Matrix.kronecker (1 : M) feature
  let tensor : M →ₗ[ℝ] N :=
    (Matrix.kroneckerBilinear : M →ₗ[ℝ] M →ₗ[ℝ] N).flip feature
  let scaled : M →L[ℝ] N := c • tensor.toContinuousLinearMap
  let W : E → N := fun x => scaled (weighted x)
  have moment := actual_radial_fourth_moment_matrix (d := d) (q := q) hq
  change Integrable weighted μ ∧ (∫ x, weighted x ∂μ) = (r + 2) • (1 : M) at moment
  have W_integrable : Integrable W μ := scaled.integrable_comp moment.1
  have good_measurable : MeasurableSet good := by
    dsimp [good, R]
    exact measurableSet_le (by fun_prop) measurable_const

  -- The two rank-one square identities give the exact source matrix square.
  have rank_square (v : Fin (q + 1) → ℝ) :
      Matrix.vecMulVec v v * Matrix.vecMulVec v v =
        (∑ k : Fin (q + 1), (v k) ^ 2) • Matrix.vecMulVec v v := by
    rw [Matrix.vecMulVec_mul_vecMulVec, Matrix.vecMulVec_smul]
    congr 1
    simp [dotProduct, pow_two]
  have gram_square (x : E) : G x * G x = R x • G x := by
    have h := rank_square (WithLp.ofLp x)
    have radius_sum : (∑ k : Fin (q + 1), (x k) ^ 2) = R x :=
      (EuclideanSpace.real_norm_sq_eq x).symm
    simpa only [radius_sum] using h
  have feature_square : feature * feature = S • feature := rank_square (t i)
  have squared_as_indicator : squared = good.indicator W := by
    funext x
    by_cases hx : x ∈ good
    · simp only [squared, Y, Set.indicator_of_mem hx]
      change ((d : ℝ)⁻¹ • Matrix.kronecker (G x) feature) *
        ((d : ℝ)⁻¹ • Matrix.kronecker (G x) feature) =
          c • Matrix.kronecker (R x • G x) feature
      dsimp only [Matrix.kronecker]
      rw [smul_mul_assoc, mul_smul_comm, ← Matrix.mul_kronecker_mul,
        gram_square x, feature_square]
      ext a b
      change (d : ℝ)⁻¹ * ((d : ℝ)⁻¹ *
        ((R x * G x a.1 b.1) * (S * feature a.2 b.2))) =
          c * ((R x * G x a.1 b.1) * feature a.2 b.2)
      dsimp [c]
      simp only [div_eq_mul_inv]
      ring
    · simp [squared, Y, Set.indicator_of_notMem hx]
  have squared_integrable : Integrable squared μ := by
    rw [squared_as_indicator]
    exact W_integrable.indicator good_measurable

  -- W is a nonnegative multiple of the tensor vector's rank-one matrix.
  have W_positive (x : E) : (W x).PosSemidef := by
    let v : Fin (q + 1) × Fin (q + 1) → ℝ := fun a => x a.1 * t i a.2
    have rank_positive : (Matrix.vecMulVec v v).PosSemidef := by
      simpa only [star_trivial] using Matrix.posSemidef_vecMulVec_self_star v
    have W_rank : W x = (c * R x) • Matrix.vecMulVec v v := by
      ext a b
      change c * (R x * (x a.1 * x b.1) * (t i a.2 * t i b.2)) =
        (c * R x) * ((x a.1 * t i a.2) * (x b.1 * t i b.2))
      ring
    rw [W_rank]
    apply rank_positive.smul
    exact mul_nonneg (div_nonneg (Finset.sum_nonneg (fun _ _ => sq_nonneg _))
      (sq_nonneg (d : ℝ))) (sq_nonneg ‖x‖)
  have residual_positive (x : E) : (W x - squared x).PosSemidef := by
    rw [squared_as_indicator]
    by_cases hx : x ∈ good
    · simpa [Set.indicator_of_mem hx] using (Matrix.PosSemidef.zero : (0 : N).PosSemidef)
    · simpa [Set.indicator_of_notMem hx] using W_positive x

  -- Finite-dimensional PSD matrices form a closed convex set, so their integral is PSD.
  have PSD_closed : IsClosed {A : N | A.PosSemidef} := by
    have hermitian_closed : IsClosed {A : N | A.IsHermitian} := by
      change IsClosed {A : N | star A = A}
      exact isClosed_eq continuous_star continuous_id
    have quadratic_closed (v : (Fin (q + 1) × Fin (q + 1)) → ℝ) :
        IsClosed {A : N | 0 ≤ dotProduct (star v) (Matrix.mulVec A v)} := by
      apply isClosed_le continuous_const
      change Continuous (fun A : N => ∑ a, star (v a) * ∑ b, A a b * v b)
      fun_prop
    convert hermitian_closed.inter (isClosed_iInter quadratic_closed) using 1
    ext A
    simp [Matrix.posSemidef_iff_dotProduct_mulVec]
  have PSD_convex : Convex ℝ {A : N | A.PosSemidef} := by
    intro A hA B hB a b ha hb hab
    exact (hA.smul ha).add (hB.smul hb)
  have integrated_residual : (∫ x, W x - squared x ∂μ).PosSemidef :=
    PSD_convex.integral_mem PSD_closed (Filter.Eventually.of_forall residual_positive)
      (W_integrable.sub squared_integrable)
  have W_mean : (∫ x, W x ∂μ) = upper := by
    calc
      (∫ x, W x ∂μ) = scaled (∫ x, weighted x ∂μ) :=
        scaled.integral_comp_comm moment.1
      _ = scaled ((r + 2) • (1 : M)) := congrArg scaled moment.2
      _ = upper := by
        change c • Matrix.kronecker ((r + 2) • (1 : M)) feature =
          (((r + 2) * S) / (d : ℝ) ^ 2) • Matrix.kronecker (1 : M) feature
        dsimp only [Matrix.kronecker]
        rw [Matrix.smul_kronecker, smul_smul]
        congr 1
        dsimp [c]
        simp only [div_eq_mul_inv]
        ring
  rw [integral_sub W_integrable squared_integrable, W_mean] at integrated_residual
  change Integrable squared μ ∧ (upper - ∫ x, squared x ∂μ).PosSemidef
  exact ⟨squared_integrable, integrated_residual⟩

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumRadialFourthMoment
