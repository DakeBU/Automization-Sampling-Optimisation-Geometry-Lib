from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
SP=Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-statement-seal.json')
assert hashlib.sha256(SP.read_bytes()).hexdigest()=='c3103a9e8d08fea6c83f35201fce953af4dd93e88a1a3d7d647fc4deaaddeb7a'
sig=json.loads(SP.read_bytes())['actual_private_consumer']['signature']
context=sig.split(' :\n',1)[1].split('  ∀ s : ℝ,',1)[0]
proof=r'''  classical
  dsimp only
'''+context+r'''  let M := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
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
  have structure :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure
      (d := d) (q := q) hq
  change (∀ j : Fin d, Measurable (Z j)) ∧ iIndepFun Z μ ∧
    (∀ j : Fin d, Integrable (Z j) μ) ∧
    (∀ j : Fin d, (∫ ω, Z j ω ∂μ) = 0) ∧
    (∀ j : Fin d, ∀ ω : Ω, (Z j ω).IsHermitian) at structure
  rcases structure with ⟨hmeasZ, _, hintZ, hzeroZ, hhermZ⟩
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
    exact (hmeasZ i).const_smul _
  have hintX : Integrable (X i) μ := by
    change Integrable (fun ω : Ω => ρ⁻¹ • Z i ω) μ
    exact (hintZ i).smul _
  have hzeroX : (∫ ω, X i ω ∂μ) = 0 := by
    change (∫ ω, ρ⁻¹ • Z i ω ∂μ) = 0
    rw [integral_smul, hzeroZ i, smul_zero]
  have hintSq : Integrable (fun ω : Ω => X i ω * X i ω) μ := by
    apply Integrable.of_bound (hmeasX.mul hmeasX).aestronglyMeasurable 1
    exact ae_of_all _ fun ω => (norm_mul_le _ _).trans (by nlinarith [hnormX i ω, norm_nonneg (X i ω)])
  have hmeasExp : Measurable (fun ω : Ω => NormedSpace.exp (s • X i ω)) :=
    NormedSpace.exp_continuous.measurable.comp (hmeasX.const_smul s)
  have hintExp : Integrable (fun ω : Ω => NormedSpace.exp (s • X i ω)) μ := by
    apply Integrable.of_bound hmeasExp.aestronglyMeasurable (Real.exp s)
    exact ae_of_all _ fun ω => capped_matrix_exp_norm_le _ (hhermX i ω) (hcapX i ω) hs
  have hsqPSD : ∀ᵐ ω ∂μ, (X i ω * X i ω).PosSemidef := by
    apply ae_of_all
    intro ω
    have hh : (X i ω)ᴴ = X i ω := hhermX i ω
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
'''
p=Path('Tests/GaussianComplexityBernsteinMgf.lean')
end='end AutoSamplingTheory.Tests.GaussianComplexityBernsteinMgf\n'
s=p.read_text();assert s.endswith(end)
assert 'private theorem actual_source_normalized_single_summand_mgf' not in s
declaration='private theorem actual_source_normalized_single_summand_mgf\n    '+sig+' := by\n'+proof+'\n'
p.write_text(s[:-len(end)]+declaration+end)
print(json.dumps({'actual_consumer_written':str(p),'literal_signature_sha256':hashlib.sha256(sig.encode()).hexdigest(),
 'source_lines':len(p.read_bytes().splitlines()),'new_source_hypotheses':0,'proof_is_unchecked_attempt':True}))
