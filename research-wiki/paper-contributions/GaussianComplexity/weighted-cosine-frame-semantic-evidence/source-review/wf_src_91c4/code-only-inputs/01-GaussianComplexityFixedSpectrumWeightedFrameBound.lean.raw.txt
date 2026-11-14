import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment
import Mathlib.Analysis.Convex.Integral

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped Matrix.Norms.L2Operator
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment
set_option autoImplicit false

namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumWeightedFrameBound

private theorem actual_uncentered_second_moment_sum_bound
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let Y : Fin d → E → N := fun i =>
    Set.indicator {x : E | R x ≤ L}
      (fun x => (d : ℝ)⁻¹ • Matrix.kronecker (G x) (Matrix.vecMulVec (t i) (t i)))
  let secondSum : N := ∑ i : Fin d, (∫ x, Y i x * Y i x ∂μ)
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  (∀ i : Fin d, Integrable (fun x => Y i x * Y i x) μ) ∧
    Matrix.PosSemidef (C • (1 : N) - secondSum) := by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let M := Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let G : E → M := fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let weighted : E → M := fun x => R x • G x
  let feature : Fin d → M := fun i => Matrix.vecMulVec (t i) (t i)
  let S : Fin d → ℝ := fun i => ∑ k : Fin (q + 1), (t i k) ^ 2
  let K : Fin d → N := fun i => Matrix.kronecker (1 : M) (feature i)
  let α : ℝ := (r + 2) / (d : ℝ) ^ 2
  let B : N := α • (∑ i : Fin d, S i • K i)
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  let good : Set E := {x | R x ≤ L}
  let Y : Fin d → E → N := fun i =>
    good.indicator (fun x => (d : ℝ)⁻¹ • Matrix.kronecker (G x) (feature i))
  let squared : Fin d → E → N := fun i x => Y i x * Y i x
  let c : Fin d → ℝ := fun i => S i / (d : ℝ) ^ 2
  let tensor : Fin d → M →ₗ[ℝ] N := fun i =>
    (Matrix.kroneckerBilinear : M →ₗ[ℝ] M →ₗ[ℝ] N).flip (feature i)
  let scaled : Fin d → M →L[ℝ] N := fun i => c i • (tensor i).toContinuousLinearMap
  let W : Fin d → E → N := fun i x => scaled i (weighted x)
  have moment := actual_radial_fourth_moment_matrix (d := d) (q := q) hq
  change Integrable weighted μ ∧ (∫ x, weighted x ∂μ) = (r + 2) • (1 : M) at moment
  have W_integrable (i : Fin d) : Integrable (W i) μ :=
    (scaled i).integrable_comp moment.1
  have good_measurable : MeasurableSet good := by
    dsimp [good, R]
    exact measurableSet_le (by fun_prop) measurable_const

  -- Exact rank-one and tensor squares retain one cutoff indicator.
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
  have feature_square (i : Fin d) : feature i * feature i = S i • feature i :=
    rank_square (t i)
  have squared_as_indicator (i : Fin d) : squared i = good.indicator (W i) := by
    funext x
    by_cases hx : x ∈ good
    · simp only [squared, Y, Set.indicator_of_mem hx]
      change ((d : ℝ)⁻¹ • Matrix.kronecker (G x) (feature i)) *
        ((d : ℝ)⁻¹ • Matrix.kronecker (G x) (feature i)) =
          c i • Matrix.kronecker (R x • G x) (feature i)
      dsimp only [Matrix.kronecker]
      rw [smul_mul_assoc, mul_smul_comm, ← Matrix.mul_kronecker_mul,
        gram_square x, feature_square i]
      ext a b
      change (d : ℝ)⁻¹ * ((d : ℝ)⁻¹ *
        ((R x * G x a.1 b.1) * (S i * feature i a.2 b.2))) =
          c i * ((R x * G x a.1 b.1) * feature i a.2 b.2)
      dsimp [c]
      simp only [div_eq_mul_inv]
      ring
    · simp [squared, Y, Set.indicator_of_notMem hx]
  have squared_integrable (i : Fin d) : Integrable (squared i) μ := by
    rw [squared_as_indicator i]
    exact (W_integrable i).indicator good_measurable
  have W_positive (i : Fin d) (x : E) : (W i x).PosSemidef := by
    let v : Fin (q + 1) × Fin (q + 1) → ℝ := fun a => x a.1 * t i a.2
    have rank_positive : (Matrix.vecMulVec v v).PosSemidef := by
      simpa only [star_trivial] using Matrix.posSemidef_vecMulVec_self_star v
    have W_rank : W i x = (c i * R x) • Matrix.vecMulVec v v := by
      ext a b
      change c i * (R x * (x a.1 * x b.1) * (t i a.2 * t i b.2)) =
        (c i * R x) * ((x a.1 * t i a.2) * (x b.1 * t i b.2))
      ring
    rw [W_rank]
    exact rank_positive.smul (mul_nonneg
      (div_nonneg (Finset.sum_nonneg (fun _ _ => sq_nonneg _)) (sq_nonneg _))
      (sq_nonneg ‖x‖))

  -- Integrate the whole PSD residual sum, with integrability for every square.
  have residual_positive (x : E) :
      ((∑ i : Fin d, W i x) - ∑ i : Fin d, squared i x).PosSemidef := by
    rw [← Finset.sum_sub_distrib]
    apply Matrix.posSemidef_sum Finset.univ
    intro i _
    rw [squared_as_indicator i]
    by_cases hx : x ∈ good
    · simpa [Set.indicator_of_mem hx] using (Matrix.PosSemidef.zero : (0 : N).PosSemidef)
    · simpa [Set.indicator_of_notMem hx] using W_positive i x
  have W_sum_integrable : Integrable (fun x => ∑ i : Fin d, W i x) μ :=
    integrable_finsetSum Finset.univ (fun i _ => W_integrable i)
  have squared_sum_integrable : Integrable (fun x => ∑ i : Fin d, squared i x) μ :=
    integrable_finsetSum Finset.univ (fun i _ => squared_integrable i)
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
  have integrated_residual :
      (∫ x, (∑ i : Fin d, W i x) - ∑ i : Fin d, squared i x ∂μ).PosSemidef :=
    PSD_convex.integral_mem PSD_closed (Filter.Eventually.of_forall residual_positive)
      (W_sum_integrable.sub squared_sum_integrable)
  have W_mean (i : Fin d) : (∫ x, W i x ∂μ) = α • (S i • K i) := by
    calc
      (∫ x, W i x ∂μ) = scaled i (∫ x, weighted x ∂μ) :=
        (scaled i).integral_comp_comm moment.1
      _ = scaled i ((r + 2) • (1 : M)) := congrArg (scaled i) moment.2
      _ = α • (S i • K i) := by
        change c i • Matrix.kronecker ((r + 2) • (1 : M)) (feature i) =
          α • (S i • Matrix.kronecker (1 : M) (feature i))
        dsimp only [Matrix.kronecker]
        rw [Matrix.smul_kronecker, smul_smul, smul_smul]
        congr 1
        dsimp [c, α]
        simp only [div_eq_mul_inv]
        ring
  have W_sum_mean : (∫ x, ∑ i : Fin d, W i x ∂μ) = B := by
    rw [integral_finsetSum Finset.univ (fun i _ => W_integrable i)]
    simp_rw [W_mean]
    exact Finset.smul_sum.symm
  rw [integral_sub W_sum_integrable squared_sum_integrable, W_sum_mean,
    integral_finsetSum Finset.univ (fun i _ => squared_integrable i)] at integrated_residual
  have deterministic := actual_weighted_cosine_coefficient_bound (d := d) (q := q) hq
  change (C • (1 : N) - B).PosSemidef at deterministic
  change (∀ i : Fin d, Integrable (squared i) μ) ∧
    (C • (1 : N) - ∑ i : Fin d, ∫ x, squared i x ∂μ).PosSemidef
  refine ⟨squared_integrable, ?_⟩
  convert deterministic.add integrated_residual using 1
  abel

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumWeightedFrameBound
