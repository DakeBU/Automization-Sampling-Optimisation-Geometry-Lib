import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius

/-!
# Actual centered and cosine-weighted summand radius

This private mathematical consumer uses both actual norm estimates, the literal
Bochner mean, and the original product experiment. It is not a public API or a
matrix Bernstein/concentration theorem.
-/
noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius

private theorem actual_source_centered_summand_radius
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
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let Rstar : ℝ := 2 * r * (L + 1) / (d : ℝ)
  (∀ i : Fin d, ∀ ω : Ω, ‖Z i ω‖ ≤ Rstar) ∧
    (∀ i : Fin d, ∀ ω : Ω, ‖w i • Z i ω‖ ≤ Rstar)
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
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let Rstar : ℝ := 2 * r * (L + 1) / (d : ℝ)
  change (∀ i : Fin d, ∀ ω : Ω, ‖Z i ω‖ ≤ Rstar) ∧
    (∀ i : Fin d, ∀ ω : Ω, ‖w i • Z i ω‖ ≤ Rstar)
  have bounds := FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds
    (d := d) (q := q) hq
  change (∀ i : Fin d, ∀ ω : Ω, ‖Y i ω‖ ≤ 2 * r * L / (d : ℝ)) ∧
    (∀ i : Fin d, ‖∫ ω, Y i ω ∂μ‖ ≤ 2 * r / (d : ℝ)) at bounds
  have hz (i : Fin d) (ω : Ω) : ‖Z i ω‖ ≤ Rstar := by
    dsimp only [Z, mean]
    calc
      ‖Y i ω - ∫ ω, Y i ω ∂μ‖ ≤ ‖Y i ω‖ + ‖∫ ω, Y i ω ∂μ‖ := norm_sub_le _ _
      _ ≤ 2 * r * L / (d : ℝ) + 2 * r / (d : ℝ) :=
        add_le_add (bounds.1 i ω) (bounds.2 i)
      _ = Rstar := by dsimp only [Rstar]; ring
  constructor
  · exact hz
  · intro i ω
    rw [norm_smul, Real.norm_eq_abs]
    calc
      |w i| * ‖Z i ω‖ ≤ 1 * ‖Z i ω‖ :=
        mul_le_mul_of_nonneg_right (Real.abs_cos_le_one _) (norm_nonneg _)
      _ = ‖Z i ω‖ := one_mul _
      _ ≤ Rstar := hz i ω

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius
