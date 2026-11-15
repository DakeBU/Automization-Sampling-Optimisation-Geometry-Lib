import AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-!
# Actual Gaussian scalar trace-exponential domains

The original unconditional Gaussian experiment, inclusive own-row cutoff and
true full-law means are retained. Both centered sums and both global signs
have strictly positive scalar trace exponentials for every real parameter,
with the exact r²-scaled pointwise envelope and finite positive ordinary
expectation. This private consumer emits no full matrix-valued MGF theorem.
-/

open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder ENNReal
noncomputable section
namespace AutoSamplingTheory.Tests.GaussianComplexityTraceMgfDomain

private theorem actual_source_four_trace_mgfs_integrable_positive_and_bounded :
∀ {d q : ℕ} (hq : 2 * q + 1 < d),
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let M := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let α : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let tvec : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * α i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω → M := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (tvec i) (tvec i))
    else 0
  let mean : Fin d → M := fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → M := fun i ω => Y i ω - mean i
  let w : Bool → Fin d → ℝ := fun useCos i =>
    if useCos = true then Real.cos (((2 * q + 1 : ℕ) : ℝ) * α i) else 1
  let sign : Bool → ℝ := fun minus => if minus = true then -1 else 1
  let S : Bool → Bool → Ω → M := fun useCos minus ω =>
    sign minus • ∑ i : Fin d, w useCos i • Z i ω
  let Rstar : ℝ := 2 * r * (L + 1) / (d : ℝ)
  ∀ s : ℝ, ∀ useCos minus : Bool,
    let f : Ω → ℝ := fun ω => Matrix.trace (NormedSpace.exp (s • S useCos minus ω))
    let B : ℝ := r ^ 2 * Real.exp (|s| * ((d : ℝ) * Rstar))
    Integrable f μ ∧ (∀ ω, 0 < f ω ∧ f ω ≤ B) ∧
      0 < ∫ ω, f ω ∂μ ∧ (∫ ω, f ω ∂μ) ≤ B
 := by
  classical
  intro d q hq
  dsimp only
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let M := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let α : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let tvec : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * α i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω → M := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (tvec i) (tvec i))
    else 0
  let mean : Fin d → M := fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → M := fun i ω => Y i ω - mean i
  let w : Bool → Fin d → ℝ := fun useCos i =>
    if useCos = true then Real.cos (((2 * q + 1 : ℕ) : ℝ) * α i) else 1
  let sign : Bool → ℝ := fun minus => if minus = true then -1 else 1
  let S : Bool → Bool → Ω → M := fun useCos minus ω =>
    sign minus • ∑ i : Fin d, w useCos i • Z i ω
  let Rstar : ℝ := 2 * r * (L + 1) / (d : ℝ)
  let : MeasurableSpace M := borel M
  let : BorelSpace M := ⟨rfl⟩
  let : IsProbabilityMeasure μ := by
    dsimp only [μ]
    infer_instance
  change ∀ s : ℝ, ∀ useCos minus : Bool,
    let f : Ω → ℝ := fun ω => Matrix.trace (NormedSpace.exp (s • S useCos minus ω))
    let B : ℝ := r ^ 2 * Real.exp (|s| * ((d : ℝ) * Rstar))
    Integrable f μ ∧ (∀ ω, 0 < f ω ∧ f ω ≤ B) ∧
      0 < ∫ ω, f ω ∂μ ∧ (∫ ω, f ω ∂μ) ≤ B
  have hstructure :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure
      (d := d) (q := q) hq
  change (∀ j : Fin d, Measurable (Z j)) ∧ iIndepFun Z μ ∧
    (∀ j : Fin d, Integrable (Z j) μ) ∧
    (∀ j : Fin d, (∫ ω, Z j ω ∂μ) = 0) ∧
    (∀ j : Fin d, ∀ ω : Ω, (Z j ω).IsHermitian) at hstructure
  rcases hstructure with ⟨hmeasZ, _, _, _, hhermZ⟩
  have radius :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds
      (d := d) (q := q) hq
  change (∀ j : Fin d, ∀ ω : Ω, ‖Y j ω‖ ≤ 2 * r * L / (d : ℝ)) ∧
    (∀ j : Fin d, ‖mean j‖ ≤ 2 * r / (d : ℝ)) at radius
  have hnormZ (j : Fin d) (ω : Ω) : ‖Z j ω‖ ≤ Rstar := by
    change ‖Y j ω - mean j‖ ≤ Rstar
    calc
      _ ≤ ‖Y j ω‖ + ‖mean j‖ := norm_sub_le _ _
      _ ≤ 2 * r * L / (d : ℝ) + 2 * r / (d : ℝ) :=
        add_le_add (radius.1 j ω) (radius.2 j)
      _ = Rstar := by dsimp only [Rstar]; ring
  have hw (useCos : Bool) (j : Fin d) : ‖w useCos j‖ ≤ 1 := by
    by_cases h : useCos = true
    · simpa only [w, if_pos h, Real.norm_eq_abs] using Real.abs_cos_le_one
        (((2 * q + 1 : ℕ) : ℝ) * α j)
    · simp only [w, if_neg h, norm_one, le_refl]
  have hnormS (useCos minus : Bool) (ω : Ω) : ‖S useCos minus ω‖ ≤ (d : ℝ) * Rstar := by
    have hsign : ‖sign minus‖ = 1 := by cases minus <;> norm_num [sign]
    change ‖sign minus • ∑ j : Fin d, w useCos j • Z j ω‖ ≤ _
    rw [norm_smul, hsign, one_mul]
    calc
      _ ≤ ∑ j : Fin d, ‖w useCos j • Z j ω‖ := norm_sum_le _ _
      _ ≤ ∑ _ : Fin d, Rstar := Finset.sum_le_sum fun j _ => by
        rw [norm_smul]
        exact (mul_le_mul (hw useCos j) (hnormZ j ω) (norm_nonneg _) (by norm_num)).trans_eq
          (one_mul _)
      _ = (d : ℝ) * Rstar := by simp
  have hmeasS (useCos minus : Bool) : Measurable (S useCos minus) := by
    exact (Finset.measurable_sum _ (fun j _ => (hmeasZ j).const_smul (w useCos j))).const_smul
      (sign minus)
  have hhermS (useCos minus : Bool) (ω : Ω) : (S useCos minus ω).IsHermitian := by
    exact ((IsSelfAdjoint.all (sign minus)).smul
      (isSelfAdjoint_sum _ fun j _ =>
        (IsSelfAdjoint.all (w useCos j)).smul (hhermZ j ω).isSelfAdjoint)).isHermitian
  intro s useCos minus
  let f : Ω → ℝ := fun ω => Matrix.trace (NormedSpace.exp (s • S useCos minus ω))
  let B : ℝ := r ^ 2 * Real.exp (|s| * ((d : ℝ) * Rstar))
  change Integrable f μ ∧ (∀ ω, 0 < f ω ∧ f ω ≤ B) ∧
    0 < ∫ ω, f ω ∂μ ∧ (∫ ω, f ω ∂μ) ≤ B
  have hcard : (Fintype.card (Fin (q + 1) × Fin (q + 1)) : ℝ) = r ^ 2 := by
    simp [r, Fintype.card_prod, pow_two]
  have hpoint (ω : Ω) : 0 < f ω ∧ f ω ≤ B := by
    have hp :=
      AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds.trace_exp_pos_and_le_card_mul_exp_abs_mul_norm
        (S useCos minus ω) (hhermS useCos minus ω) s
    refine ⟨hp.1, ?_⟩
    calc
      f ω ≤ (Fintype.card (Fin (q + 1) × Fin (q + 1)) : ℝ) *
          Real.exp (|s| * ‖S useCos minus ω‖) := hp.2
      _ ≤ (Fintype.card (Fin (q + 1) × Fin (q + 1)) : ℝ) *
          Real.exp (|s| * ((d : ℝ) * Rstar)) :=
        mul_le_mul_of_nonneg_left
          (Real.exp_le_exp.mpr
            (mul_le_mul_of_nonneg_left (hnormS useCos minus ω) (abs_nonneg s)))
          (by positivity)
      _ = B := by rw [hcard]
  have hcontExp : Continuous (NormedSpace.exp : M → M) :=
    continuous_iff_continuousAt.mpr fun A =>
      (NormedSpace.exp_analytic (𝕂 := ℝ) A).continuousAt
  have hmeasf : Measurable f :=
    (Matrix.traceLinearMap _ ℝ ℝ).toContinuousLinearMap.continuous.measurable.comp
      (hcontExp.measurable.comp ((hmeasS useCos minus).const_smul s))
  have hint : Integrable f μ := by
    apply Integrable.of_bound hmeasf.aestronglyMeasurable B
    exact ae_of_all _ fun ω => by
      rw [Real.norm_eq_abs, abs_of_pos (hpoint ω).1]
      exact (hpoint ω).2
  have hsupport : Function.support f = Set.univ := by
    ext ω
    simp only [Function.mem_support, Set.mem_univ, iff_true]
    exact ne_of_gt (hpoint ω).1
  have hintpos : 0 < ∫ ω, f ω ∂μ := by
    apply (integral_pos_iff_support_of_nonneg (fun ω => (hpoint ω).1.le) hint).mpr
    rw [hsupport]
    simp
  have hintle : (∫ ω, f ω ∂μ) ≤ B := by
    simpa using integral_mono_ae hint (integrable_const B)
      (ae_of_all μ fun ω => (hpoint ω).2)
  exact ⟨hint, hpoint, hintpos, hintle⟩

end AutoSamplingTheory.Tests.GaussianComplexityTraceMgfDomain
