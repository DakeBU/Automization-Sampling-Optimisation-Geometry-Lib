import AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveDefIntegral
import AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-! True matrix-exponential expectations of the literal original Gaussian
experiment. Every real parameter and both signs of both source sums are
covered. Integrability, positive definiteness of the actual full-law mean,
trace commutation and its explicit finite envelope are proved internally.
This does not prove a matrix-log identity, Lieb, or a Bernstein tail. -/

open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder ENNReal
noncomputable section
namespace AutoSamplingTheory.Tests.GaussianComplexityMatrixMgfDomain

private theorem actual_source_four_matrix_mgfs_integrable_posDef_and_trace_bounded :
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
    let G : Ω → M := fun ω => NormedSpace.exp (s • S useCos minus ω)
    let MX : M := ∫ ω, G ω ∂μ
    let B : ℝ := r ^ 2 * Real.exp (|s| * ((d : ℝ) * Rstar))
    Integrable G μ ∧ MX.PosDef ∧
      Matrix.trace MX = (∫ ω, Matrix.trace (G ω) ∂μ) ∧
      0 < Matrix.trace MX ∧ Matrix.trace MX ≤ B
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
    let G : Ω → M := fun ω => NormedSpace.exp (s • S useCos minus ω)
    let MX : M := ∫ ω, G ω ∂μ
    let B : ℝ := r ^ 2 * Real.exp (|s| * ((d : ℝ) * Rstar))
    Integrable G μ ∧ MX.PosDef ∧
      Matrix.trace MX = (∫ ω, Matrix.trace (G ω) ∂μ) ∧
      0 < Matrix.trace MX ∧ Matrix.trace MX ≤ B
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
  let G : Ω → M := fun ω => NormedSpace.exp (s • S useCos minus ω)
  let MX : M := ∫ ω, G ω ∂μ
  let B : ℝ := r ^ 2 * Real.exp (|s| * ((d : ℝ) * Rstar))
  change Integrable G μ ∧ MX.PosDef ∧
    Matrix.trace MX = (∫ ω, Matrix.trace (G ω) ∂μ) ∧
    0 < Matrix.trace MX ∧ Matrix.trace MX ≤ B
  have heq (ω : Ω) : cfc (fun x : ℝ => Real.exp (s * x)) (S useCos minus ω) = G ω := by
    calc
      _ = cfc Real.exp (s • S useCos minus ω) :=
        cfc_comp_const_mul s Real.exp _ (by fun_prop) (hhermS useCos minus ω).isSelfAdjoint
      _ = _ := CFC.real_exp_eq_normedSpace_exp
        ((IsSelfAdjoint.all s).smul (hhermS useCos minus ω).isSelfAdjoint)
  have hPD (ω : Ω) : (G ω).PosDef := by
    have hstrict : IsStrictlyPositive
        (cfc (fun x : ℝ => Real.exp (s * x)) (S useCos minus ω)) :=
      (cfc_isStrictlyPositive_iff (fun x : ℝ => Real.exp (s * x)) _
        (by fun_prop) (hhermS useCos minus ω).isSelfAdjoint).mpr
          (fun x _ => Real.exp_pos (s * x))
    rw [heq ω] at hstrict
    exact Matrix.isStrictlyPositive_iff_posDef.mp hstrict
  have hnormG (ω : Ω) : ‖G ω‖ ≤ Real.exp (|s| * ((d : ℝ) * Rstar)) := by
    rw [← heq ω]
    apply norm_cfc_le (Real.exp_nonneg _)
    intro x hx
    rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
    apply Real.exp_le_exp.mpr
    have hnormx : |x| ≤ ‖S useCos minus ω‖ := by
      simpa only [Real.norm_eq_abs] using
        IsometricContinuousFunctionalCalculus.norm_spectrum_le _ hx
          (hhermS useCos minus ω).isSelfAdjoint
    calc
      s * x ≤ |s * x| := le_abs_self _
      _ = |s| * |x| := abs_mul _ _
      _ ≤ |s| * ‖S useCos minus ω‖ :=
        mul_le_mul_of_nonneg_left hnormx (abs_nonneg s)
      _ ≤ |s| * ((d : ℝ) * Rstar) :=
        mul_le_mul_of_nonneg_left (hnormS useCos minus ω) (abs_nonneg s)
  have hcontExp : Continuous (NormedSpace.exp : M → M) :=
    continuous_iff_continuousAt.mpr fun A =>
      (NormedSpace.exp_analytic (𝕂 := ℝ) A).continuousAt
  have hmeasG : Measurable G :=
    hcontExp.measurable.comp ((hmeasS useCos minus).const_smul s)
  have hintG : Integrable G μ :=
    Integrable.of_bound hmeasG.aestronglyMeasurable
      (Real.exp (|s| * ((d : ℝ) * Rstar))) (ae_of_all μ hnormG)
  have hMX : MX.PosDef :=
    AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveDefIntegral.integral_posDef
      G hintG (ae_of_all μ hPD)
  let tr : M →L[ℝ] ℝ := (Matrix.traceLinearMap _ ℝ ℝ).toContinuousLinearMap
  have htrace : Matrix.trace MX = (∫ ω, Matrix.trace (G ω) ∂μ) :=
    (tr.integral_comp_comm hintG).symm
  have hintTr : Integrable (fun ω => Matrix.trace (G ω)) μ := tr.integrable_comp hintG
  have hcard : (Fintype.card (Fin (q + 1) × Fin (q + 1)) : ℝ) = r ^ 2 := by
    simp [r, Fintype.card_prod, pow_two]
  have hpointle (ω : Ω) : Matrix.trace (G ω) ≤ B := by
    have hp :=
      AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds.trace_exp_pos_and_le_card_mul_exp_abs_mul_norm
        (S useCos minus ω) (hhermS useCos minus ω) s
    calc
      Matrix.trace (G ω) ≤ (Fintype.card (Fin (q + 1) × Fin (q + 1)) : ℝ) *
          Real.exp (|s| * ‖S useCos minus ω‖) := hp.2
      _ ≤ (Fintype.card (Fin (q + 1) × Fin (q + 1)) : ℝ) *
          Real.exp (|s| * ((d : ℝ) * Rstar)) :=
        mul_le_mul_of_nonneg_left
          (Real.exp_le_exp.mpr
            (mul_le_mul_of_nonneg_left (hnormS useCos minus ω) (abs_nonneg s)))
          (by positivity)
      _ = B := by rw [hcard]
  have hbound : Matrix.trace MX ≤ B := by
    rw [htrace]
    simpa using integral_mono_ae hintTr (integrable_const B) (ae_of_all μ hpointle)
  exact ⟨hintG, hMX, htrace, hMX.trace_pos, hbound⟩

end AutoSamplingTheory.Tests.GaussianComplexityMatrixMgfDomain
