import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDetector
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.Adjoint

open Matrix InnerProductSpace MeasureTheory ProbabilityTheory
set_option autoImplicit false

/-!
Actual private source detector consumer. Both conjuncts are proved internally:
the intrinsic polynomial event is Borel, and its mass under the actual
rotated pushforward diagonal Gaussian equals the strict diagonal event mass.
This does not identify that pushforward with multivariateGaussian0 A inverse
or prove a high-probability/algorithm/query lower bound.
-/
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumDetector

private theorem actual_rotated_gaussian_detector_event {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) (n : ℕ) (τ : ℝ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let R : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun z => WithLp.toLp 2 ((O : Matrix (Fin d) (Fin d) ℝ) *ᵥ WithLp.ofLp z)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Λ *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let B : Matrix (Fin d) (Fin d) ℝ :=
    (κ - 1)⁻¹ • ((2 : ℝ) • A - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ))
  let S : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (-1 : ℝ) ^ n *
      ((WithLp.ofLp x) ⬝ᵥ ((Polynomial.aeval B (Polynomial.Chebyshev.T ℝ (n : ℤ))) *ᵥ WithLp.ofLp x)) -
      2 * τ * ‖x‖ ^ 2
  MeasurableSet {x | 0 < S x} ∧
    (μ.map R) {x | 0 < S x} =
      μ {z | 0 < (-1 : ℝ) ^ n *
        (∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp z i) ^ 2) -
        2 * τ * ‖z‖ ^ 2} := by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin d)
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let μ : Measure E := multivariateGaussian (0 : E) Λ⁻¹
  let R : E → E := fun z =>
    WithLp.toLp 2 ((O : Matrix (Fin d) (Fin d) ℝ) *ᵥ WithLp.ofLp z)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Λ *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let B : Matrix (Fin d) (Fin d) ℝ :=
    (κ - 1)⁻¹ • ((2 : ℝ) • A - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ))
  let T : Matrix (Fin d) (Fin d) ℝ :=
    Polynomial.aeval B (Polynomial.Chebyshev.T ℝ (n : ℤ))
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos ((n : ℝ) * θ i))
  let S : E → ℝ := fun x =>
    (-1 : ℝ) ^ n * ((WithLp.ofLp x) ⬝ᵥ (T *ᵥ WithLp.ofLp x)) -
      2 * τ * ‖x‖ ^ 2
  have hT : T = (O : Matrix (Fin d) (Fin d) ℝ) * D *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDetector.actual_chebyshev_matrix_cosine hd hκ O n
  have hR : Measurable R :=
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) (O : Matrix (Fin d) (Fin d) ℝ)).continuous.measurable
  have hSc : Continuous S := by
    have hq : Continuous (fun x : E =>
        (WithLp.ofLp x) ⬝ᵥ (T *ᵥ WithLp.ofLp x)) := by
      have hi : Continuous (fun x : E =>
          inner ℝ x (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) T x)) :=
        continuous_id.inner (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) T).continuous
      have heq : (fun x : E =>
          inner ℝ x (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) T x)) =
          (fun x : E => (WithLp.ofLp x) ⬝ᵥ (T *ᵥ WithLp.ofLp x)) := by
        funext x
        exact Matrix.inner_toEuclideanCLM T x x
      rw [← heq]
      exact hi
    exact (continuous_const.mul hq).sub (continuous_const.mul (continuous_norm.pow 2))
  have hEvent : MeasurableSet {x : E | 0 < S x} :=
    measurableSet_lt measurable_const hSc.measurable
  have hO : (O : Matrix (Fin d) (Fin d) ℝ).transpose *
      (O : Matrix (Fin d) (Fin d) ℝ) = 1 :=
    (Matrix.mem_orthogonalGroup_iff' (n := Fin d) (R := ℝ)).mp O.property
  have hundo (v : Fin d → ℝ) :
      (O : Matrix (Fin d) (Fin d) ℝ).transpose *ᵥ
        ((O : Matrix (Fin d) (Fin d) ℝ) *ᵥ v) = v := by
    rw [Matrix.mulVec_mulVec, hO, Matrix.one_mulVec]
  have hnorm (z : E) : ‖R z‖ = ‖z‖ := by
    exact ContinuousLinearMap.norm_map_of_mem_unitary
      (Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)) O.property) z
  have hquad (z : E) :
      (WithLp.ofLp (R z)) ⬝ᵥ (T *ᵥ WithLp.ofLp (R z)) =
        ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp z i) ^ 2 := by
    rw [hT]
    change ((O : Matrix (Fin d) (Fin d) ℝ) *ᵥ WithLp.ofLp z) ⬝ᵥ
      (((O : Matrix (Fin d) (Fin d) ℝ) * D *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose) *ᵥ
          ((O : Matrix (Fin d) (Fin d) ℝ) *ᵥ WithLp.ofLp z)) = _
    rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, hundo]
    rw [← Matrix.dotProduct_transpose_mulVec, hundo]
    simp only [D, dotProduct, Matrix.mulVec_diagonal]
    apply Finset.sum_congr rfl
    intro i _
    ring
  have hstat (z : E) : S (R z) =
      (-1 : ℝ) ^ n * (∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp z i) ^ 2) -
        2 * τ * ‖z‖ ^ 2 := by
    dsimp only [S]
    rw [hquad, hnorm]
  change MeasurableSet {x : E | 0 < S x} ∧
    (μ.map R) {x : E | 0 < S x} = _
  refine ⟨hEvent, ?_⟩
  rw [Measure.map_apply hR hEvent]
  apply congrArg μ
  ext z
  change (0 < S (R z)) ↔ _
  rw [hstat]
  rfl

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumDetector
