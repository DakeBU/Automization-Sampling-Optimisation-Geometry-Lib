import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment

/-!
# The actual expected truncated Gaussian matrix summand

This source application uses the one-row second moment and the deterministic
midpoint cosine feature. All matrix integrals use the Euclidean operator norm.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped Matrix.Norms.L2Operator
set_option autoImplicit false

namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumTruncatedRowMoment

open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment

private theorem actual_truncated_matrix_summand_mean
    {d q : ℕ} (hq : 2 * q + 1 < d) (i : Fin d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let a : ℝ := (∫ x, Set.indicator {y : E | R y ≤ L} R x ∂μ) / r
  let θ : Fin d → ℝ := fun j => ((j.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun j k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ j)
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let Y : E → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    Set.indicator {y : E | R y ≤ L}
      (fun x => (d : ℝ)⁻¹ • Matrix.kronecker (G x) (Matrix.vecMulVec (t i) (t i)))
  Integrable Y μ ∧
    (∫ x, Y x ∂μ) =
      (a / (d : ℝ)) • Matrix.kronecker
        (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) (Matrix.vecMulVec (t i) (t i)) := by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let a : ℝ := (∫ x, Set.indicator {y : E | R y ≤ L} R x ∂μ) / r
  let θ : Fin d → ℝ := fun j => ((j.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun j k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ j)
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let good : Set E := {y : E | R y ≤ L}
  let kept : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ := good.indicator G
  let Y : E → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    good.indicator
      (fun x => (d : ℝ)⁻¹ • Matrix.kronecker (G x) (Matrix.vecMulVec (t i) (t i)))
  let M := Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let feature : M := Matrix.vecMulVec (t i) (t i)
  let tensor : M →ₗ[ℝ] N :=
    (Matrix.kroneckerBilinear : M →ₗ[ℝ] M →ₗ[ℝ] N).flip feature
  let scaled : M →L[ℝ] N := (d : ℝ)⁻¹ • tensor.toContinuousLinearMap
  have moment := actual_truncated_row_second_moment (d := d) (q := q) hq
  change Integrable kept μ ∧ (∫ x, kept x ∂μ) = a • (1 : M) at moment
  have summand_as_linear_image : Y = fun x => scaled (kept x) := by
    funext x
    change good.indicator (fun x => (d : ℝ)⁻¹ • Matrix.kronecker (G x) feature) x =
      (d : ℝ)⁻¹ • Matrix.kronecker (good.indicator G x) feature
    by_cases hx : x ∈ good
    · simp [Set.indicator_of_mem hx]
    · simp [Set.indicator_of_notMem hx]
  change Integrable Y μ ∧
    (∫ x, Y x ∂μ) = (a / (d : ℝ)) • Matrix.kronecker (1 : M) feature
  refine ⟨?_, ?_⟩
  · rw [summand_as_linear_image]
    exact scaled.integrable_comp moment.1
  · calc
      (∫ x, Y x ∂μ) = scaled (∫ x, kept x ∂μ) := by
        rw [summand_as_linear_image]
        exact scaled.integral_comp_comm moment.1
      _ = scaled (a • (1 : M)) := congrArg scaled moment.2
      _ = a • scaled (1 : M) := scaled.map_smul a (1 : M)
      _ = (a / (d : ℝ)) • Matrix.kronecker (1 : M) feature := by
        change a • ((d : ℝ)⁻¹ • Matrix.kronecker (1 : M) feature) = _
        simp only [smul_smul, div_eq_mul_inv]

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumTruncatedRowMoment
