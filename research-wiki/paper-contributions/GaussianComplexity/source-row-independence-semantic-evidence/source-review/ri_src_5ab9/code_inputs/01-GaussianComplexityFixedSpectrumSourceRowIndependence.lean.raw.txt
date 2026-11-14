import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence

noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence
set_option autoImplicit false

namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceRowIndependence

private theorem actual_truncated_matrices_measurable_and_independent
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun a : Fin (q + 1) => ω a i)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i =>
    (((i.val : ℝ) + 1 - (1 / 2 : ℝ)) * Real.pi) / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let Y : Fin d → Ω →
      ((Fin (q + 1) × Fin (q + 1)) → (Fin (q + 1) × Fin (q + 1)) → ℝ) := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (fun a => row i ω a) (fun a => row i ω a))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  (∀ i : Fin d, Measurable (Y i)) ∧ iIndepFun Y μ := by
  classical
  dsimp only
  let Q := Fin (q + 1)
  let I := Fin d
  let D := EuclideanSpace ℝ I
  let E := EuclideanSpace ℝ Q
  let Ω := Q → D
  let μ : Measure Ω := Measure.pi (fun _ : Q => stdGaussian D)
  let row : I → Ω → E := fun i ω => WithLp.toLp 2 (fun a : Q => ω a i)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : I → ℝ := fun i =>
    (((i.val : ℝ) + 1 - (1 / 2 : ℝ)) * Real.pi) / (d : ℝ)
  let t : I → Q → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let F : I → E → ((Q × Q) → (Q × Q) → ℝ) := fun i x =>
    if ‖x‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (fun a => x a) (fun a => x a))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let Y : I → Ω → ((Q × Q) → (Q × Q) → ℝ) := fun i ω => F i (row i ω)
  change (∀ i : I, Measurable (Y i)) ∧ iIndepFun Y μ
  have row_law := actual_source_row_marginal_law (d := d) (q := q) hq
  change ∀ i : I, MeasurePreserving (row i) μ (stdGaussian E) at row_law
  have row_independent := actual_source_rows_independent (d := d) (q := q) hq
  change iIndepFun row μ at row_independent

  have coordinate (a : Q) : Measurable (fun x : E => x a) := by
    dsimp [E]
    fun_prop
  have cutoff : MeasurableSet {x : E | ‖x‖ ^ 2 ≤ L} :=
    measurableSet_le (by fun_prop) measurable_const
  have F_measurable (i : I) : Measurable (F i) := by
    apply Measurable.ite cutoff
    · apply measurable_pi_lambda
      intro u
      apply measurable_pi_lambda
      intro v
      change Measurable (fun x : E =>
        (d : ℝ)⁻¹ * ((x u.1 * x v.1) * (t i u.2 * t i v.2)))
      exact measurable_const.mul (((coordinate u.1).mul (coordinate v.1)).mul measurable_const)
    · exact measurable_const
  constructor
  · intro i
    exact (F_measurable i).comp (row_law i).measurable
  · exact row_independent.comp F F_measurable

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceRowIndependence
