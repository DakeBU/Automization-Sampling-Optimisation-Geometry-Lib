import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean

/-! Actual original-experiment centered matrix structure. All measurability,
integrability, independence, zero-mean and Hermitian obligations are discharged
internally under the sole original source condition. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure

theorem actual_source_centered_matrix_structure
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
  (∀ i : Fin d, Measurable (Z i)) ∧
    iIndepFun Z μ ∧
    (∀ i : Fin d, Integrable (Z i) μ) ∧
    (∀ i : Fin d, (∫ ω, Z i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (Z i ω).IsHermitian)
 := by
  classical
  dsimp only
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
  letI : BorelSpace (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ) := ⟨rfl⟩

  letI : IsProbabilityMeasure μ := by dsimp only [μ]; infer_instance
  change (∀ i : Fin d, Measurable (Z i)) ∧ iIndepFun Z μ ∧
    (∀ i : Fin d, Integrable (Z i) μ) ∧
    (∀ i : Fin d, (∫ ω, Z i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (Z i ω).IsHermitian)
  let F : Fin d → E → Matrix (Fin (q + 1) × Fin (q + 1))
      (Fin (q + 1) × Fin (q + 1)) ℝ := fun i x =>
    if ‖x‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec x.ofLp x.ofLp) (Matrix.vecMulVec (t i) (t i))
    else 0
  have row_law (i : Fin d) : MeasurePreserving (row i) μ (stdGaussian E) :=
    FixedSpectrumSourceRowLaw.actual_source_row_marginal_law hq i
  have row_independent : iIndepFun row μ :=
    FixedSpectrumSourceRowIndependence.actual_source_rows_independent hq
  have cutoff : MeasurableSet {x : E | ‖x‖ ^ 2 ≤ L} :=
    measurableSet_le (by fun_prop) measurable_const
  have F_measurable (i : Fin d) : Measurable (F i) := by
    apply Measurable.ite cutoff
    · apply Continuous.measurable
      apply continuous_pi
      intro u
      apply continuous_pi
      intro v
      change Continuous (fun x : E =>
        (d : ℝ)⁻¹ * ((x u.1 * x v.1) * (t i u.2 * t i v.2)))
      fun_prop
    · exact measurable_const
  have translated_measurable (i : Fin d) :
      Measurable (fun x : E => F i x - mean i) :=
    (F_measurable i).sub measurable_const
  have Z_measurable (i : Fin d) : Measurable (Z i) :=
    (translated_measurable i).comp (row_law i).measurable
  have Z_independent : iIndepFun Z μ :=
    row_independent.comp (fun i x => F i x - mean i) translated_measurable
  let a : ℝ := (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L}
    (fun y : E => ‖y‖ ^ 2) x ∂stdGaussian E) / r
  have hm := FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means
    (d := d) (q := q) hq
  change (∀ i : Fin d, Integrable (Y i) μ) ∧
    (∀ i : Fin d, mean i = (a / (d : ℝ)) • Matrix.kronecker
      (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ)
      (Matrix.vecMulVec (t i) (t i))) at hm
  have Y_hermitian (i : Fin d) (ω : Ω) : (Y i ω).IsHermitian := by
    change (Y i ω).conjTranspose = Y i ω
    by_cases hx : ‖row i ω‖ ^ 2 ≤ L
    · ext u v
      simp only [Y, if_pos hx, Matrix.conjTranspose_apply, Matrix.smul_apply,
        Matrix.kronecker, Matrix.kroneckerMap_apply, Matrix.vecMulVec_apply,
        smul_eq_mul, star_trivial]
      ring
    · simp [Y, hx]
  have mean_hermitian (i : Fin d) : (mean i).IsHermitian := by
    rw [hm.2 i]
    change ((a / (d : ℝ)) • Matrix.kronecker
      (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ)
      (Matrix.vecMulVec (t i) (t i))).conjTranspose = _
    ext u v
    simp [Matrix.conjTranspose_apply, Matrix.kronecker, Matrix.kroneckerMap,
      Matrix.vecMulVec, eq_comm, mul_comm]
  have Z_integrable (i : Fin d) : Integrable (Z i) μ :=
    (hm.1 i).sub (integrable_const _)
  have Z_mean_zero (i : Fin d) : (∫ ω, Z i ω ∂μ) = 0 := by
    change (∫ ω, Y i ω - mean i ∂μ) = 0
    rw [integral_sub (hm.1 i) (integrable_const _)]
    simp [mean]
  exact ⟨Z_measurable, Z_independent, Z_integrable, Z_mean_zero,
    fun i ω => (Y_hermitian i ω).sub (mean_hermitian i)⟩

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure
