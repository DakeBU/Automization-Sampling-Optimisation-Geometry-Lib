import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure

/-! Private genuine consumer: the literal deterministic cosine-weighted family
retains all five actual centered structural properties. No combined-family
independence, nonzero/sign weight assumption or concentration is claimed. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure

private theorem actual_source_weighted_centered_matrix_structure
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  letI : MeasurableSpace
      (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ) :=
    borel (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)
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
  let X : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => w i • Z i ω
  (∀ i : Fin d, Measurable (X i)) ∧
    iIndepFun X μ ∧
    (∀ i : Fin d, Integrable (X i) μ) ∧
    (∀ i : Fin d, (∫ ω, X i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (X i ω).IsHermitian)
 := by
  classical
  dsimp only
  let : MeasurableSpace
      (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ) :=
    borel (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)
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
  let X : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => w i • Z i ω
  let : BorelSpace (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ) := ⟨rfl⟩

  change (∀ i : Fin d, Measurable (X i)) ∧ iIndepFun X μ ∧
    (∀ i : Fin d, Integrable (X i) μ) ∧
    (∀ i : Fin d, (∫ ω, X i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (X i ω).IsHermitian)
  have hp := FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure
    (d := d) (q := q) hq
  change (∀ i : Fin d, Measurable (Z i)) ∧ iIndepFun Z μ ∧
    (∀ i : Fin d, Integrable (Z i) μ) ∧
    (∀ i : Fin d, (∫ ω, Z i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (Z i ω).IsHermitian) at hp
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro i
    exact measurable_const.smul (hp.1 i)
  · exact hp.2.1.comp (fun i A => w i • A)
      (fun _ => measurable_const.smul measurable_id)
  · intro i
    exact (hp.2.2.1 i).const_smul (w i)
  · intro i
    dsimp only [X]
    rw [integral_smul, hp.2.2.2.1 i, smul_zero]
  · intro i ω
    exact (hp.2.2.2.2 i ω).smul (isSelfAdjoint_iff.mpr rfl)

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure
