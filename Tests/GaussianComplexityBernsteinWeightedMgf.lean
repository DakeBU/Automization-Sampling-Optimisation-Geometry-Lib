import AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinMgf
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure

open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder
noncomputable section
universe u
namespace AutoSamplingTheory.Tests.GaussianComplexityBernsteinWeightedMgf

private lemma one_sub_posSemidef_of_norm_le_one
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (hn : ‖A‖ ≤ 1) :
    (1 - A).PosSemidef := by
  have hspec : ∀ x ∈ spectrum ℝ A, x ≤ 1 := by
    intro x hx
    exact (Real.le_norm_self x).trans
      ((IsometricContinuousFunctionalCalculus.norm_spectrum_le A hx hA.isSelfAdjoint).trans hn)
  exact Matrix.le_iff.mp ((CFC.le_one_iff (R := ℝ) A hA.isSelfAdjoint).mpr hspec)

private theorem actual_source_weighted_normalized_single_summand_mgf
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
  let ρ : ℝ := 2 * r * (L + 1) / (d : ℝ)
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let X : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => ρ⁻¹ • (w i • Z i ω)
  ∀ s : ℝ, 0 < s → ∀ i : Fin d,
    (NormedSpace.exp
        ((Real.exp s - s - 1) • (∫ ω, X i ω * X i ω ∂μ)) -
      ∫ ω, NormedSpace.exp (s • X i ω) ∂μ).PosSemidef
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
  let ρ : ℝ := 2 * r * (L + 1) / (d : ℝ)
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let X : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => ρ⁻¹ • (w i • Z i ω)
  let M := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  letI : MeasurableSpace M := borel M
  letI : BorelSpace M := ⟨rfl⟩
  letI : IsProbabilityMeasure μ := by
    dsimp only [μ]
    infer_instance
  change ∀ s : ℝ, 0 < s → ∀ i : Fin d,
    (NormedSpace.exp ((Real.exp s - s - 1) • (∫ ω, X i ω * X i ω ∂μ)) -
      ∫ ω, NormedSpace.exp (s • X i ω) ∂μ).PosSemidef
  have radius :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds
      (d := d) (q := q) hq
  change (∀ j : Fin d, ∀ ω : Ω, ‖Y j ω‖ ≤ 2 * r * L / (d : ℝ)) ∧
    (∀ j : Fin d, ‖mean j‖ ≤ 2 * r / (d : ℝ)) at radius
  have hstructure :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure
      (d := d) (q := q) hq
  change (∀ j : Fin d, Measurable (Z j)) ∧ iIndepFun Z μ ∧
    (∀ j : Fin d, Integrable (Z j) μ) ∧
    (∀ j : Fin d, (∫ ω, Z j ω ∂μ) = 0) ∧
    (∀ j : Fin d, ∀ ω : Ω, (Z j ω).IsHermitian) at hstructure
  rcases hstructure with ⟨hmeasZ, _, hintZ, hzeroZ, hhermZ⟩
  have hd2 : 2 ≤ d := by omega
  have hd2R : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd2
  have hdpos : (0 : ℝ) < d := by linarith
  have hrpos : 0 < r := by dsimp only [r]; positivity
  have hlog : 0 ≤ Real.log (1000 * (d : ℝ)) := Real.log_nonneg (by nlinarith)
  have hLpos : 0 < L + 1 := by dsimp only [L]; nlinarith
  have hρpos : 0 < ρ := by dsimp only [ρ]; positivity
  have hnormZ (j : Fin d) (ω : Ω) : ‖Z j ω‖ ≤ ρ := by
    change ‖Y j ω - mean j‖ ≤ ρ
    calc
      _ ≤ ‖Y j ω‖ + ‖mean j‖ := norm_sub_le _ _
      _ ≤ 2 * r * L / (d : ℝ) + 2 * r / (d : ℝ) :=
        add_le_add (radius.1 j ω) (radius.2 j)
      _ = ρ := by dsimp only [ρ]; ring
  have hnormW (j : Fin d) (ω : Ω) : ‖w j • Z j ω‖ ≤ ρ := by
    rw [norm_smul, Real.norm_eq_abs]
    have hw : |w j| ≤ 1 := Real.abs_cos_le_one _
    calc
      |w j| * ‖Z j ω‖ ≤ 1 * ρ :=
        mul_le_mul hw (hnormZ j ω) (norm_nonneg _) (by positivity)
      _ = ρ := one_mul _
  have hnormX (j : Fin d) (ω : Ω) : ‖X j ω‖ ≤ 1 := by
    change ‖ρ⁻¹ • (w j • Z j ω)‖ ≤ 1
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hρpos)]
    calc
      _ ≤ ρ⁻¹ * ρ := mul_le_mul_of_nonneg_left (hnormW j ω) (inv_nonneg.mpr hρpos.le)
      _ = 1 := inv_mul_cancel₀ (ne_of_gt hρpos)
  have hhermX (j : Fin d) (ω : Ω) : (X j ω).IsHermitian := by
    change (ρ⁻¹ • (w j • Z j ω)).IsHermitian
    exact ((IsSelfAdjoint.all (ρ⁻¹ : ℝ)).smul
      ((IsSelfAdjoint.all (w j)).smul (hhermZ j ω).isSelfAdjoint)).isHermitian
  have hcapX (j : Fin d) (ω : Ω) : (1 - X j ω).PosSemidef :=
    one_sub_posSemidef_of_norm_le_one _ (hhermX j ω) (hnormX j ω)
  intro s hs i
  have hmeasX : Measurable (X i) := by
    change Measurable (fun ω : Ω => ρ⁻¹ • (w i • Z i ω))
    exact ((hmeasZ i).const_smul (w i)).const_smul (ρ⁻¹ : ℝ)
  have hintX : Integrable (X i) μ := by
    change Integrable (fun ω : Ω => ρ⁻¹ • (w i • Z i ω)) μ
    exact ((hintZ i).smul (w i)).smul (ρ⁻¹ : ℝ)
  have hzeroW : (∫ ω, w i • Z i ω ∂μ) = 0 := by
    rw [integral_smul (w i) (Z i), hzeroZ i, smul_zero]
  have hzeroX : (∫ ω, X i ω ∂μ) = 0 := by
    change (∫ ω, ρ⁻¹ • (w i • Z i ω) ∂μ) = 0
    rw [integral_smul (ρ⁻¹) (fun ω : Ω => w i • Z i ω), hzeroW, smul_zero]
  have hintSq : Integrable (fun ω : Ω => X i ω * X i ω) μ := by
    apply Integrable.of_bound (hmeasX.mul hmeasX).aestronglyMeasurable 1
    exact ae_of_all _ fun ω => (norm_mul_le _ _).trans
      (by nlinarith [hnormX i ω, norm_nonneg (X i ω)])
  exact AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinMgf.centered_bounded_matrix_mgf
    μ (X i) hmeasX.aestronglyMeasurable hintX hintSq
    (ae_of_all _ (hhermX i)) (ae_of_all _ (hcapX i)) hzeroX hs

end AutoSamplingTheory.Tests.GaussianComplexityBernsteinWeightedMgf
