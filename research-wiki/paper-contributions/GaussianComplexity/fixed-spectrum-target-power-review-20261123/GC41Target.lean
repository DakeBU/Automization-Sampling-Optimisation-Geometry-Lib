import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDetector
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetLaw
import Mathlib.Topology.Algebra.Polynomial

/-! The strict Section 4.3 detector and its exact probability under each rotated target. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
set_option autoImplicit false

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation

variable {d : ℕ}

/-- Midpoint Chebyshev grid of Equation (11). -/
def gridAngle (d : ℕ) (i : Fin d) : ℝ :=
  ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)

def diagonalPrecision (d : ℕ) (κ : ℝ) : Matrix (Fin d) (Fin d) ℝ :=
  Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (gridAngle d i))

def hiddenPrecision (κ : ℝ) (O : Matrix.orthogonalGroup (Fin d) ℝ) :
    Matrix (Fin d) (Fin d) ℝ :=
  O.val * diagonalPrecision d κ * O.val.transpose

/-- The intrinsic detector depends on the input precision itself. -/
def detectorStatistic (κ : ℝ) (n : ℕ) (τ : ℝ) (A : Matrix (Fin d) (Fin d) ℝ)
    (x : EuclideanSpace ℝ (Fin d)) : ℝ :=
  let B := (κ - 1)⁻¹ • ((2 : ℝ) • A - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ))
  (-1 : ℝ) ^ n * (WithLp.ofLp x ⬝ᵥ
      ((Polynomial.aeval B (Polynomial.Chebyshev.T ℝ (n : ℤ))) *ᵥ WithLp.ofLp x)) -
    2 * τ * ‖x‖ ^ 2

def detectorEvent (κ : ℝ) (n : ℕ) (τ : ℝ) (A : Matrix (Fin d) (Fin d) ℝ) :
    Set (EuclideanSpace ℝ (Fin d)) :=
  {x | 0 < detectorStatistic κ n τ A x}

theorem continuous_detectorStatistic (κ : ℝ) (n : ℕ) (τ : ℝ) :
    Continuous (fun p : Matrix (Fin d) (Fin d) ℝ × EuclideanSpace ℝ (Fin d) =>
      detectorStatistic κ n τ p.1 p.2) := by
  let T := Polynomial.Chebyshev.T ℝ (n : ℤ)
  have hT : Continuous (fun p : Matrix (Fin d) (Fin d) ℝ × EuclideanSpace ℝ (Fin d) =>
      Polynomial.aeval ((κ - 1)⁻¹ • ((2 : ℝ) • p.1 - (κ + 1) • 1)) T) :=
    T.continuous_aeval.comp (by fun_prop)
  have hx : Continuous (fun p : Matrix (Fin d) (Fin d) ℝ × EuclideanSpace ℝ (Fin d) =>
      WithLp.ofLp p.2) :=
    continuous_pi fun i => (EuclideanSpace.proj i).continuous.comp continuous_snd
  exact (continuous_const.mul (hx.dotProduct (hT.matrix_mulVec hx))).sub
    (continuous_const.mul (continuous_snd.norm.pow 2))

theorem measurableSet_detectorEvent (κ : ℝ) (n : ℕ) (τ : ℝ) (A : Matrix (Fin d) (Fin d) ℝ) :
    MeasurableSet (detectorEvent κ n τ A) :=
  measurableSet_lt measurable_const
    ((continuous_detectorStatistic κ n τ).comp (continuous_const.prodMk continuous_id)).measurable

/-- Diagonalization at the observed point, in coordinates of the hidden eigenbasis. -/
theorem mem_detectorEvent_hiddenPrecision_iff (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) (n : ℕ) (τ : ℝ) (x : EuclideanSpace ℝ (Fin d)) :
    x ∈ detectorEvent κ n τ (hiddenPrecision κ O) ↔
    0 < (-1 : ℝ) ^ n * (∑ i : Fin d, Real.cos ((n : ℝ) * gridAngle d i) *
      ((O.val.transpose *ᵥ WithLp.ofLp x) i) ^ 2) - 2 * τ * ‖x‖ ^ 2 := by
  let D := Matrix.diagonal (fun i : Fin d => Real.cos ((n : ℝ) * gridAngle d i))
  let B := (κ - 1)⁻¹ • ((2 : ℝ) • hiddenPrecision κ O - (κ + 1) • 1)
  have hT : Polynomial.aeval B (Polynomial.Chebyshev.T ℝ (n : ℤ)) =
      O.val * D * O.val.transpose :=
    FixedSpectrumDetector.actual_chebyshev_matrix_cosine hd hκ O n
  have hq : WithLp.ofLp x ⬝ᵥ ((O.val * D * O.val.transpose) *ᵥ WithLp.ofLp x) =
      ∑ i : Fin d, Real.cos ((n : ℝ) * gridAngle d i) *
        ((O.val.transpose *ᵥ WithLp.ofLp x) i) ^ 2 := by
    rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, ← Matrix.dotProduct_transpose_mulVec]
    simp only [D, dotProduct, Matrix.mulVec_diagonal]
    apply Finset.sum_congr rfl
    intro i _
    ring
  change (0 < (-1 : ℝ) ^ n *
    (WithLp.ofLp x ⬝ᵥ (Polynomial.aeval B (Polynomial.Chebyshev.T ℝ (n : ℤ)) *ᵥ WithLp.ofLp x)) -
      2 * τ * ‖x‖ ^ 2) ↔ _
  rw [hT, hq]

/-- The true inverse-precision Gaussian gives the intrinsic event exactly its diagonal mass. -/
theorem rotated_detector_probability_eq (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) (n : ℕ) (τ : ℝ) :
    (multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) (hiddenPrecision κ O)⁻¹).real
      (detectorEvent κ n τ (hiddenPrecision κ O)) =
    (multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) (diagonalPrecision d κ)⁻¹).real
      {z : EuclideanSpace ℝ (Fin d) | 0 < (-1 : ℝ) ^ n * (∑ i : Fin d, Real.cos ((n : ℝ) * gridAngle d i) *
        (WithLp.ofLp z i) ^ 2) - 2 * τ * ‖z‖ ^ 2} := by
  let R := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) O.val
  let μ := multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) (diagonalPrecision d κ)⁻¹
  have hLaw : μ.map R =
      multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) (hiddenPrecision κ O)⁻¹ :=
    FixedSpectrumTargetLaw.actual_rotated_gaussian_target hd hκ O
  have hO : O.val.transpose * O.val = 1 :=
    (Matrix.mem_orthogonalGroup_iff' (n := Fin d) (R := ℝ)).mp O.property
  have hPre : R ⁻¹' detectorEvent κ n τ (hiddenPrecision κ O) =
      {z : EuclideanSpace ℝ (Fin d) | 0 < (-1 : ℝ) ^ n * (∑ i : Fin d, Real.cos ((n : ℝ) * gridAngle d i) *
        (WithLp.ofLp z i) ^ 2) - 2 * τ * ‖z‖ ^ 2} := by
    ext z
    change (R z ∈ detectorEvent κ n τ (hiddenPrecision κ O)) ↔ _
    rw [mem_detectorEvent_hiddenPrecision_iff hd hκ]
    have hundo : O.val.transpose *ᵥ WithLp.ofLp (R z) = WithLp.ofLp z := by
      change O.val.transpose *ᵥ (O.val *ᵥ WithLp.ofLp z) = _
      rw [Matrix.mulVec_mulVec, hO, Matrix.one_mulVec]
    have hnorm : ‖R z‖ = ‖z‖ := ContinuousLinearMap.norm_map_of_mem_unitary
      (Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)) O.property) z
    rw [hundo, hnorm]
    rfl
  rw [← hLaw, measureReal_def, Measure.map_apply R.continuous.measurable
    (measurableSet_detectorEvent κ n τ _), hPre]
  rfl

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
