import AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential
import AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure

open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder

noncomputable section

universe u

namespace AutoSamplingTheory.Tests.GaussianComplexityBernsteinMgf

private lemma one_sub_posSemidef_of_norm_le_one
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (hn : ‖A‖ ≤ 1) :
    (1 - A).PosSemidef := by
  have hspec : ∀ x ∈ spectrum ℝ A, x ≤ 1 := by
    intro x hx
    exact (Real.le_norm_self x).trans
      ((IsometricContinuousFunctionalCalculus.norm_spectrum_le A hx hA.isSelfAdjoint).trans hn)
  exact Matrix.le_iff.mp ((CFC.le_one_iff (R := ℝ) A hA.isSelfAdjoint).mpr hspec)

private lemma capped_matrix_exp_norm_le
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (hcap : (1 - A).PosSemidef)
    {s : ℝ} (hs : 0 < s) : ‖NormedSpace.exp (s • A)‖ ≤ Real.exp s := by
  have hSA : IsSelfAdjoint A := hA.isSelfAdjoint
  have hspec : ∀ x ∈ spectrum ℝ A, x ≤ 1 :=
    (CFC.le_one_iff (R := ℝ) A hSA).mp (Matrix.le_iff.mpr hcap)
  have heq : cfc (fun x : ℝ => Real.exp (s * x)) A = NormedSpace.exp (s • A) := by
    calc
      _ = cfc Real.exp (s • A) := cfc_comp_const_mul s Real.exp A (by fun_prop) hSA
      _ = _ := CFC.real_exp_eq_normedSpace_exp ((IsSelfAdjoint.all s).smul hSA)
  rw [← heq]
  apply norm_cfc_le (Real.exp_nonneg s)
  intro x hx
  rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
  apply Real.exp_le_exp.mpr
  simpa only [mul_one] using mul_le_mul_of_nonneg_left (hspec x hx) hs.le

private lemma exp_sub_one_add_posSemidef
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) :
    (NormedSpace.exp A - (1 + A)).PosSemidef := by
  have hSA : IsSelfAdjoint A := hA.isSelfAdjoint
  have hfc : cfc (fun x : ℝ => 1 + x) A ≤ cfc Real.exp A :=
    cfc_mono (a := A) (fun x _ => by linarith [Real.add_one_le_exp x])
      (by fun_prop) (by fun_prop)
  have hlin : cfc (fun x : ℝ => 1 + x) A = (1 : Matrix ι ι ℝ) + A := by
    rw [cfc_add (a := A) (fun _ : ℝ => 1) (fun x : ℝ => x) (by fun_prop) (by fun_prop),
      cfc_const (R := ℝ) 1 A hSA, cfc_id' ℝ A hSA, map_one]
  exact Matrix.le_iff.mp
    (by simpa only [hlin, CFC.real_exp_eq_normedSpace_exp hSA] using hfc)

private theorem actual_source_normalized_single_summand_mgf
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
  let X : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => ρ⁻¹ • Z i ω
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
  let X : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => ρ⁻¹ • Z i ω
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
  have hnormX (j : Fin d) (ω : Ω) : ‖X j ω‖ ≤ 1 := by
    change ‖ρ⁻¹ • Z j ω‖ ≤ 1
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hρpos)]
    calc
      _ ≤ ρ⁻¹ * ρ := mul_le_mul_of_nonneg_left (hnormZ j ω) (inv_nonneg.mpr hρpos.le)
      _ = 1 := inv_mul_cancel₀ (ne_of_gt hρpos)
  have hhermX (j : Fin d) (ω : Ω) : (X j ω).IsHermitian := by
    change (ρ⁻¹ • Z j ω).IsHermitian
    exact ((IsSelfAdjoint.all (ρ⁻¹ : ℝ)).smul (hhermZ j ω).isSelfAdjoint).isHermitian
  have hcapX (j : Fin d) (ω : Ω) : (1 - X j ω).PosSemidef :=
    one_sub_posSemidef_of_norm_le_one _ (hhermX j ω) (hnormX j ω)
  intro s hs i
  let g : ℝ := Real.exp s - s - 1
  let C : M := g • (∫ ω, X i ω * X i ω ∂μ)
  have hmeasX : Measurable (X i) := by
    change Measurable (fun ω : Ω => ρ⁻¹ • Z i ω)
    exact (hmeasZ i).const_smul (ρ⁻¹ : ℝ)
  have hintX : Integrable (X i) μ := by
    change Integrable (fun ω : Ω => ρ⁻¹ • Z i ω) μ
    exact (hintZ i).smul (ρ⁻¹ : ℝ)
  have hzeroX : (∫ ω, X i ω ∂μ) = 0 := by
    change (∫ ω, ρ⁻¹ • Z i ω ∂μ) = 0
    rw [integral_smul, hzeroZ i, smul_zero]
  have hintSq : Integrable (fun ω : Ω => X i ω * X i ω) μ := by
    apply Integrable.of_bound (hmeasX.mul hmeasX).aestronglyMeasurable 1
    exact ae_of_all _ fun ω => (norm_mul_le _ _).trans (by nlinarith [hnormX i ω, norm_nonneg (X i ω)])
  have hcontExp : Continuous (NormedSpace.exp : M → M) :=
    continuous_iff_continuousAt.mpr fun A =>
      (NormedSpace.exp_analytic (𝕂 := ℝ) A).continuousAt
  have hmeasExp : Measurable (fun ω : Ω => NormedSpace.exp (s • X i ω)) :=
    hcontExp.measurable.comp (hmeasX.const_smul s)
  have hintExp : Integrable (fun ω : Ω => NormedSpace.exp (s • X i ω)) μ := by
    apply Integrable.of_bound hmeasExp.aestronglyMeasurable (Real.exp s)
    exact ae_of_all _ fun ω => capped_matrix_exp_norm_le _ (hhermX i ω) (hcapX i ω) hs
  have hsqPSD : ∀ᵐ ω ∂μ, (X i ω * X i ω).PosSemidef := by
    apply ae_of_all
    intro ω
    have hh : Matrix.conjTranspose (X i ω) = X i ω := hhermX i ω
    simpa only [hh] using Matrix.posSemidef_conjTranspose_mul_self (X i ω)
  have hcovPSD :=
    AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef
      (fun ω : Ω => X i ω * X i ω) hintSq hsqPSD
  have hg : 0 ≤ g := by dsimp only [g]; linarith [Real.add_one_le_exp s]
  have hCPSD : C.PosSemidef := hcovPSD.smul hg
  let Q : Ω → M := fun ω => (1 : M) + s • X i ω + g • (X i ω * X i ω)
  let F : Ω → M := fun ω => Q ω - NormedSpace.exp (s • X i ω)
  have hintOne : Integrable (fun _ : Ω => (1 : M)) μ := integrable_const _
  have honeMean : (∫ _ : Ω, (1 : M) ∂μ) = 1 := by simp
  have hintQ : Integrable Q μ := (hintOne.add (hintX.smul s)).add (hintSq.smul g)
  have hintF : Integrable F μ := hintQ.sub hintExp
  have hQmean : (∫ ω, Q ω ∂μ) = (1 : M) + C := by
    dsimp only [Q, C]
    rw [integral_add (hintOne.add (hintX.smul s)) (hintSq.smul g),
      integral_add hintOne (hintX.smul s), integral_smul, integral_smul, honeMean, hzeroX]
    simp only [smul_zero, add_zero]
  have hFmean : (∫ ω, F ω ∂μ) = (1 : M) + C - ∫ ω, NormedSpace.exp (s • X i ω) ∂μ := by
    change (∫ ω, Q ω - NormedSpace.exp (s • X i ω) ∂μ) = _
    rw [integral_sub hintQ hintExp, hQmean]
  have hFPSD : ∀ᵐ ω ∂μ, (F ω).PosSemidef := by
    apply ae_of_all
    intro ω
    change ((1 : M) + s • X i ω + g • (X i ω * X i ω) -
      NormedSpace.exp (s • X i ω)).PosSemidef
    exact AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential.bernstein_exponential_quadratic_bound
      _ (hhermX i ω) (hcapX i ω) hs
  have hupperPSD :=
    AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef
      F hintF hFPSD
  rw [hFmean] at hupperPSD
  have hlowerPSD := exp_sub_one_add_posSemidef C hCPSD.isHermitian
  change (NormedSpace.exp C - ∫ ω, NormedSpace.exp (s • X i ω) ∂μ).PosSemidef
  have halg : NormedSpace.exp C - (∫ ω, NormedSpace.exp (s • X i ω) ∂μ) =
      (NormedSpace.exp C - (1 + C)) +
        ((1 + C) - ∫ ω, NormedSpace.exp (s • X i ω) ∂μ) := by abel
  rw [halg]
  exact hlowerPSD.add hupperPSD

end AutoSamplingTheory.Tests.GaussianComplexityBernsteinMgf
