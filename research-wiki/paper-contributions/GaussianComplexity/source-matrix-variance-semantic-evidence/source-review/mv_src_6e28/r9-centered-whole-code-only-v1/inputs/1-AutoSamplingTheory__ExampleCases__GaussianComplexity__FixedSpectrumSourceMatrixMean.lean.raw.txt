import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.Analysis.CStarAlgebra.Matrix

/-! Exact first moments of the original-experiment closed-cutoff matrices.
The existing canonical row law and truncated radial moment remain shared nodes.
No row-law, integrability or mean certificate is a public premise. -/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean

theorem actual_source_truncated_matrix_means
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let a : ℝ :=
    (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L} (fun y : E => ‖y‖ ^ 2) x
      ∂stdGaussian E) / r
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
  (∀ i : Fin d, Integrable (Y i) μ) ∧
    ∀ i : Fin d, (∫ ω, Y i ω ∂μ) =
      (a / (d : ℝ)) • Matrix.kronecker
        (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) (Matrix.vecMulVec (t i) (t i))
:= by
  classical
  dsimp only
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let a : ℝ :=
    (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L} (fun y : E => ‖y‖ ^ 2) x
      ∂stdGaussian E) / r
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
  let ν : Measure E := stdGaussian E
  let M := Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let good : Set E := {x | ‖x‖ ^ 2 ≤ L}
  let G : E → M := fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let kept : E → M := good.indicator G
  have moment := FixedSpectrumTruncatedRowMoment.actual_truncated_row_second_moment
    (d := d) (q := q) hq
  change Integrable kept ν ∧ (∫ x, kept x ∂ν) = a • (1 : M) at moment
  have row_law (i : Fin d) : MeasurePreserving (row i) μ ν :=
    FixedSpectrumSourceRowLaw.actual_source_row_marginal_law hq i
  have actual_kept_integrable (i : Fin d) :
      Integrable (fun ω => kept (row i ω)) μ :=
    (row_law i).integrable_comp_of_integrable moment.1
  have actual_kept_mean (i : Fin d) :
      (∫ ω, kept (row i ω) ∂μ) = a • (1 : M) := by
    have measurable_on_map : AEStronglyMeasurable kept (Measure.map (row i) μ) := by
      rw [(row_law i).map_eq]
      exact moment.1.aestronglyMeasurable
    have transport := integral_map (row_law i).measurable.aemeasurable measurable_on_map
    rw [(row_law i).map_eq] at transport
    exact transport.symm.trans moment.2
  let feature : Fin d → M := fun i => Matrix.vecMulVec (t i) (t i)
  let tensor : Fin d → M →ₗ[ℝ] N := fun i =>
    (Matrix.kroneckerBilinear : M →ₗ[ℝ] M →ₗ[ℝ] N).flip (feature i)
  let scaled : Fin d → M →L[ℝ] N := fun i => (d : ℝ)⁻¹ • (tensor i).toContinuousLinearMap
  have actual_image (i : Fin d) : Y i = fun ω => scaled i (kept (row i ω)) := by
    funext ω
    change (if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker (G (row i ω)) (feature i) else 0) =
        (d : ℝ)⁻¹ • Matrix.kronecker (kept (row i ω)) (feature i)
    by_cases hω : ‖row i ω‖ ^ 2 ≤ L
    · simp [hω, kept, good]
    · simp [hω, kept, good]
  change (∀ i : Fin d, Integrable (Y i) μ) ∧
    ∀ i : Fin d, (∫ ω, Y i ω ∂μ) =
      (a / (d : ℝ)) • Matrix.kronecker (1 : M) (feature i)
  refine ⟨?_, ?_⟩
  · intro i
    rw [actual_image]
    exact (scaled i).integrable_comp (actual_kept_integrable i)
  · intro i
    calc
      (∫ ω, Y i ω ∂μ) = scaled i (∫ ω, kept (row i ω) ∂μ) := by
        rw [actual_image]
        exact (scaled i).integral_comp_comm (actual_kept_integrable i)
      _ = scaled i (a • (1 : M)) := congrArg (scaled i) (actual_kept_mean i)
      _ = a • scaled i (1 : M) := (scaled i).map_smul a (1 : M)
      _ = (a / (d : ℝ)) • Matrix.kronecker (1 : M) (feature i) := by
        change a • ((d : ℝ)⁻¹ • Matrix.kronecker (1 : M) (feature i)) = _
        simp only [smul_smul, div_eq_mul_inv]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
