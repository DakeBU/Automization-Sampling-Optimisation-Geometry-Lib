import AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder ENNReal
noncomputable section
universe u
namespace AutoSamplingTheory.Tests.GaussianComplexityLaplaceTail

private lemma hermitian_exp_norm_le
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) {C s : ℝ}
    (hn : ‖A‖ ≤ C) (hs : 0 < s) :
    ‖NormedSpace.exp (s • A)‖ ≤ Real.exp (s * C) := by
  have heq : cfc (fun x : ℝ => Real.exp (s * x)) A = NormedSpace.exp (s • A) := by
    calc
      _ = cfc Real.exp (s • A) :=
        cfc_comp_const_mul s Real.exp A (by fun_prop) hA.isSelfAdjoint
      _ = _ := CFC.real_exp_eq_normedSpace_exp
        ((IsSelfAdjoint.all s).smul hA.isSelfAdjoint)
  rw [← heq]
  apply norm_cfc_le (Real.exp_nonneg _)
  intro x hx
  rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
  exact Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left
    ((Real.le_norm_self x).trans
      ((IsometricContinuousFunctionalCalculus.norm_spectrum_le A hx hA.isSelfAdjoint).trans hn))
    hs.le)

private lemma hermitian_trace_exp_nonneg
    {ι : Type u} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (s : ℝ) :
    0 ≤ Matrix.trace (NormedSpace.exp (s • A)) := by
  have hSA := (IsSelfAdjoint.all s).smul hA.isSelfAdjoint
  have hnonneg : (0 : Matrix ι ι ℝ) ≤ cfc Real.exp (s • A) :=
    cfc_nonneg (fun x _ => Real.exp_nonneg x)
  rw [CFC.real_exp_eq_normedSpace_exp hSA] at hnonneg
  have hPSD : (NormedSpace.exp (s • A)).PosSemidef := by
    simpa only [sub_zero] using Matrix.le_iff.mp hnonneg
  exact hPSD.trace_nonneg

private theorem actual_source_four_sums_laplace_tail :
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
  ∀ s : ℝ, 0 < s → ∀ a : ℝ, ∀ useCos minus : Bool,
    μ {ω | a ≤ sSup (spectrum ℝ (S useCos minus ω))} ≤
      ENNReal.ofReal
        (Real.exp (-(s * a)) *
          ∫ ω, Matrix.trace (NormedSpace.exp (s • S useCos minus ω)) ∂μ)
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
  let ρ : ℝ := 2 * r * (L + 1) / (d : ℝ)
  letI : MeasurableSpace M := borel M
  letI : BorelSpace M := ⟨rfl⟩
  letI : IsProbabilityMeasure μ := by
    dsimp only [μ]
    infer_instance
  change ∀ s : ℝ, 0 < s → ∀ a : ℝ, ∀ useCos minus : Bool,
    μ {ω | a ≤ sSup (spectrum ℝ (S useCos minus ω))} ≤
      ENNReal.ofReal (Real.exp (-(s * a)) *
        ∫ ω, Matrix.trace (NormedSpace.exp (s • S useCos minus ω)) ∂μ)
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
  have hd2 : 2 ≤ d := by omega
  have hd2R : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd2
  have hdpos : (0 : ℝ) < d := by linarith
  have hrpos : 0 < r := by dsimp only [r]; positivity
  have hlog : 0 ≤ Real.log (1000 * (d : ℝ)) := Real.log_nonneg (by nlinarith)
  have hLpos : 0 < L + 1 := by dsimp only [L]; nlinarith
  have hnormZ (j : Fin d) (ω : Ω) : ‖Z j ω‖ ≤ ρ := by
    change ‖Y j ω - mean j‖ ≤ ρ
    calc
      _ ≤ ‖Y j ω‖ + ‖mean j‖ := norm_sub_le _ _
      _ ≤ 2 * r * L / (d : ℝ) + 2 * r / (d : ℝ) :=
        add_le_add (radius.1 j ω) (radius.2 j)
      _ = ρ := by dsimp only [ρ]; ring
  have hw (useCos : Bool) (j : Fin d) : ‖w useCos j‖ ≤ 1 := by
    by_cases h : useCos = true
    · simpa only [w, if_pos h, Real.norm_eq_abs] using Real.abs_cos_le_one
        (((2 * q + 1 : ℕ) : ℝ) * α j)
    · simp only [w, if_neg h, norm_one, le_refl]
  have hnormS (useCos minus : Bool) (ω : Ω) : ‖S useCos minus ω‖ ≤ (d : ℝ) * ρ := by
    have hsign : ‖sign minus‖ = 1 := by cases minus <;> norm_num [sign]
    change ‖sign minus • ∑ j : Fin d, w useCos j • Z j ω‖ ≤ _
    rw [norm_smul, hsign, one_mul]
    calc
      _ ≤ ∑ j : Fin d, ‖w useCos j • Z j ω‖ := norm_sum_le _ _
      _ ≤ ∑ _ : Fin d, ρ := Finset.sum_le_sum fun j _ => by
        rw [norm_smul]
        exact (mul_le_mul (hw useCos j) (hnormZ j ω) (norm_nonneg _) (by norm_num)).trans_eq
          (one_mul _)
      _ = (d : ℝ) * ρ := by simp
  have hmeasS (useCos minus : Bool) : Measurable (S useCos minus) := by
    exact (Finset.measurable_sum _ (fun j _ => (hmeasZ j).const_smul (w useCos j))).const_smul
      (sign minus)
  have hhermS (useCos minus : Bool) (ω : Ω) : (S useCos minus ω).IsHermitian := by
    exact ((IsSelfAdjoint.all (sign minus)).smul
      (isSelfAdjoint_sum _ fun j _ =>
        (IsSelfAdjoint.all (w useCos j)).smul (hhermZ j ω).isSelfAdjoint)).isHermitian
  intro s hs a useCos minus
  have hcontExp : Continuous (NormedSpace.exp : M → M) :=
    continuous_iff_continuousAt.mpr fun A =>
      (NormedSpace.exp_analytic (𝕂 := ℝ) A).continuousAt
  have hintExp : Integrable (fun ω => NormedSpace.exp (s • S useCos minus ω)) μ := by
    apply Integrable.of_bound
      (hcontExp.comp_aestronglyMeasurable
        ((hmeasS useCos minus).aestronglyMeasurable.const_smul s))
      (Real.exp (s * ((d : ℝ) * ρ)))
    exact ae_of_all _ fun ω => hermitian_exp_norm_le _ (hhermS useCos minus ω)
      (hnormS useCos minus ω) hs
  have hintTrace : Integrable
      (fun ω => Matrix.trace (NormedSpace.exp (s • S useCos minus ω))) μ :=
    (Matrix.traceLinearMap _ ℝ ℝ).toContinuousLinearMap.integrable_comp hintExp
  have htraceNonneg : ∀ᵐ ω ∂μ,
      0 ≤ Matrix.trace (NormedSpace.exp (s • S useCos minus ω)) :=
    ae_of_all _ fun ω => hermitian_trace_exp_nonneg _ (hhermS useCos minus ω) s
  have htail :=
    AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail.max_eigenvalue_tail_le_iInf_trace_exp
      μ (S useCos minus) (hmeasS useCos minus).aestronglyMeasurable
      (ae_of_all _ (hhermS useCos minus)) a
  calc
    _ ≤ ENNReal.ofReal (Real.exp (-(s * a))) *
        ∫⁻ ω, ENNReal.ofReal (Matrix.trace (NormedSpace.exp (s • S useCos minus ω))) ∂μ :=
      htail.trans (iInf_le _ (⟨s, hs⟩ : {x : ℝ // 0 < x}))
    _ = _ := by
      rw [← ofReal_integral_eq_lintegral_ofReal hintTrace htraceNonneg,
        ← ENNReal.ofReal_mul (Real.exp_nonneg _)]

end AutoSamplingTheory.Tests.GaussianComplexityLaplaceTail
