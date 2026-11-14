import AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential
import AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral

/-! The real normalized single-matrix expectation MGF step of Tropp Lemma 6.7.
Regularity expands his section 2.2 standing convention. This is not a sum tail.
-/
open MeasureTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder
noncomputable section
universe u v
namespace AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinMgf

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

/-- Real normalized bounded Bernstein MGF, with almost-sure one-sided cap. -/
theorem centered_bounded_matrix_mgf
    {Ω : Type v} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (X : Ω → Matrix ι ι ℝ)
    (hX : AEStronglyMeasurable X μ)
    (hintX : Integrable X μ)
    (hintSq : Integrable (fun ω => X ω * X ω) μ)
    (hherm : ∀ᵐ ω ∂μ, (X ω).IsHermitian)
    (hcap : ∀ᵐ ω ∂μ, (1 - X ω).PosSemidef)
    (hzero : (∫ ω, X ω ∂μ) = 0)
    {s : ℝ} (hs : 0 < s) :
    (NormedSpace.exp ((Real.exp s - s - 1) • (∫ ω, X ω * X ω ∂μ)) -
      ∫ ω, NormedSpace.exp (s • X ω) ∂μ).PosSemidef
 := by
  classical
  let M := Matrix ι ι ℝ
  let g : ℝ := Real.exp s - s - 1
  let C : M := g • (∫ ω, X ω * X ω ∂μ)
  have hcontExp : Continuous (NormedSpace.exp : M → M) :=
    continuous_iff_continuousAt.mpr fun A =>
      (NormedSpace.exp_analytic (𝕂 := ℝ) A).continuousAt
  have hmeasExp : AEStronglyMeasurable (fun ω => NormedSpace.exp (s • X ω)) μ :=
    hcontExp.comp_aestronglyMeasurable (hX.const_smul s)
  have hintExp : Integrable (fun ω => NormedSpace.exp (s • X ω)) μ := by
    apply Integrable.of_bound hmeasExp (Real.exp s)
    filter_upwards [hherm, hcap] with ω hh hc
    exact capped_matrix_exp_norm_le _ hh hc hs
  have hsqPSD : ∀ᵐ ω ∂μ, (X ω * X ω).PosSemidef := by
    filter_upwards [hherm] with ω hh
    have heq : Matrix.conjTranspose (X ω) = X ω := hh
    simpa only [heq] using Matrix.posSemidef_conjTranspose_mul_self (X ω)
  have hcovPSD :=
    AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef
      (fun ω => X ω * X ω) hintSq hsqPSD
  have hg : 0 ≤ g := by dsimp only [g]; linarith [Real.add_one_le_exp s]
  have hCPSD : C.PosSemidef := hcovPSD.smul hg
  let Q : Ω → M := fun ω => (1 : M) + s • X ω + g • (X ω * X ω)
  let F : Ω → M := fun ω => Q ω - NormedSpace.exp (s • X ω)
  have hintOne : Integrable (fun _ : Ω => (1 : M)) μ := integrable_const _
  have honeMean : (∫ _ : Ω, (1 : M) ∂μ) = 1 := by simp
  have hintQ : Integrable Q μ := (hintOne.add (hintX.smul s)).add (hintSq.smul g)
  have hintF : Integrable F μ := hintQ.sub hintExp
  have hQmean : (∫ ω, Q ω ∂μ) = (1 : M) + C := by
    dsimp only [Q, C]
    have hsum :
        (∫ ω, (1 : M) + s • X ω + g • (X ω * X ω) ∂μ) =
          (∫ ω, (1 : M) + s • X ω ∂μ) + (∫ ω, g • (X ω * X ω) ∂μ) := by
      simpa only [Pi.add_apply, Pi.smul_apply] using
        integral_add (hintOne.add (hintX.smul s)) (hintSq.smul g)
    have hsumOne :
        (∫ ω, (1 : M) + s • X ω ∂μ) =
          (∫ _ : Ω, (1 : M) ∂μ) + (∫ ω, s • X ω ∂μ) := by
      simpa only [Pi.add_apply, Pi.smul_apply] using integral_add hintOne (hintX.smul s)
    rw [hsum, hsumOne, integral_smul s X,
      integral_smul g (fun ω => X ω * X ω), honeMean, hzero]
    simp only [smul_zero, add_zero]
  have hFmean : (∫ ω, F ω ∂μ) = (1 : M) + C - ∫ ω, NormedSpace.exp (s • X ω) ∂μ := by
    change (∫ ω, Q ω - NormedSpace.exp (s • X ω) ∂μ) = _
    rw [integral_sub hintQ hintExp, hQmean]
  have hFPSD : ∀ᵐ ω ∂μ, (F ω).PosSemidef := by
    filter_upwards [hherm, hcap] with ω hh hc
    exact AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential.bernstein_exponential_quadratic_bound
      (X ω) hh hc hs
  have hupperPSD :=
    AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef
      F hintF hFPSD
  rw [hFmean] at hupperPSD
  have hlowerPSD := exp_sub_one_add_posSemidef C hCPSD.isHermitian
  change (NormedSpace.exp C - ∫ ω, NormedSpace.exp (s • X ω) ∂μ).PosSemidef
  have halg : NormedSpace.exp C - (∫ ω, NormedSpace.exp (s • X ω) ∂μ) =
      (NormedSpace.exp C - (1 + C)) +
        ((1 + C) - ∫ ω, NormedSpace.exp (s • X ω) ∂μ) := by abel
  rw [halg]
  exact hlowerPSD.add hupperPSD

end AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinMgf
