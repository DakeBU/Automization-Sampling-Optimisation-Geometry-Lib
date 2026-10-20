import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticFeatureRisk

open MeasureTheory
open scoped ENNReal InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticFeatureRisk

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.JointEmpiricalSegmentRisk

theorem joint_empirical_probability_segment_derivative
    {W X : Type*} [MeasurableSpace W] [MeasurableSingletonClass W] [MeasurableSpace X]
    (P : Measure (X × ℝ)) [IsProbabilityMeasure P]
    (K : W → X → ℝ)
    (hlabel : MemLp (fun z : X × ℝ => z.2) 2 P)
    {N : ℕ} (hN : 0 < N) (w0 w1 : Fin N → W)
    (hfeature0 : ∀ j, MemLp (K (w0 j)) 2 (P.map Prod.fst))
    (hfeature1 : ∀ j, MemLp (K (w1 j)) 2 (P.map Prod.fst)) :
    let rho0 : Measure W := (N : ℝ≥0∞)⁻¹ • ∑ j, Measure.dirac (w0 j)
    let rho1 : Measure W := (N : ℝ≥0∞)⁻¹ • ∑ j, Measure.dirac (w1 j)
    let curve : ℝ → Measure W := fun t =>
      ENNReal.ofReal (1 - t) • rho0 + ENNReal.ofReal t • rho1
    let predictor : Measure W → X → ℝ := fun law x => ∫ q, K q x ∂law
    let risk : Measure W → ℝ := fun law => ∫ z, (predictor law z.1 - z.2) ^ 2 ∂P
    let potential : W → ℝ := fun q =>
      2 * ∫ z, (predictor rho0 z.1 - z.2) * K q z.1 ∂P
    (∀ t ∈ Set.Icc (0 : ℝ) 1,
      IsProbabilityMeasure (curve t) ∧
      Integrable (fun z : X × ℝ => (predictor (curve t) z.1 - z.2) ^ 2) P) ∧
    Integrable potential rho0 ∧ Integrable potential rho1 ∧
    HasDerivWithinAt (fun t => risk (curve t))
      ((∫ q, potential q ∂rho1) - (∫ q, potential q ∂rho0))
      (Set.Icc (0 : ℝ) 1) 0 := by
  classical
  dsimp only
  let rhoOf : (Fin N → W) → Measure W :=
    fun cfg => (N : ℝ≥0∞)⁻¹ • ∑ j, Measure.dirac (cfg j)
  let curve : ℝ → Measure W := fun t =>
    ENNReal.ofReal (1 - t) • rhoOf w0 + ENNReal.ofReal t • rhoOf w1
  let predictor : Measure W → X → ℝ := fun law x => ∫ q, K q x ∂law
  let risk : Measure W → ℝ := fun law => ∫ z, (predictor law z.1 - z.2) ^ 2 ∂P
  let potential : W → ℝ := fun q =>
    2 * ∫ z, (predictor (rhoOf w0) z.1 - z.2) * K q z.1 ∂P
  change (∀ t ∈ Set.Icc (0 : ℝ) 1,
      IsProbabilityMeasure (curve t) ∧
      Integrable (fun z : X × ℝ => (predictor (curve t) z.1 - z.2) ^ 2) P) ∧
    Integrable potential (rhoOf w0) ∧ Integrable potential (rhoOf w1) ∧
    HasDerivWithinAt (fun t => risk (curve t))
      ((∫ q, potential q ∂rhoOf w1) - (∫ q, potential q ∂rhoOf w0))
      (Set.Icc (0 : ℝ) 1) 0
  have hinv : (N : ℝ≥0∞)⁻¹ ≠ ∞ := by
    apply ENNReal.inv_ne_top.mpr
    exact_mod_cast hN.ne'
  have hInt (cfg : Fin N → W) (g : W → ℝ) : Integrable g (rhoOf cfg) := by
    apply Integrable.smul_measure (c := (N : ℝ≥0∞)⁻¹) _ hinv
    exact integrable_finsetSum_measure.mpr (fun j _ => integrable_dirac (by simp))
  have hEval (cfg : Fin N → W) (g : W → ℝ) :
      (∫ q, g q ∂rhoOf cfg) = (N : ℝ)⁻¹ * ∑ j, g (cfg j) := by
    dsimp only [rhoOf]
    rw [integral_smul_measure,
      integral_finsetSum_measure (fun j _ => integrable_dirac (by simp))]
    simp [smul_eq_mul]
  have hPred (cfg : Fin N → W) (x : X) :
      predictor (rhoOf cfg) x = (N : ℝ)⁻¹ * ∑ j, K (cfg j) x :=
    hEval cfg (fun q => K q x)
  have hmarg : MeasurePreserving (Prod.fst : X × ℝ → X) P (P.map Prod.fst) :=
    measurable_fst.measurePreserving P
  have hf0 (j : Fin N) : MemLp (fun z : X × ℝ => K (w0 j) z.1) 2 P :=
    (hfeature0 j).comp_measurePreserving hmarg
  have hf1 (j : Fin N) : MemLp (fun z : X × ℝ => K (w1 j) z.1) 2 P :=
    (hfeature1 j).comp_measurePreserving hmarg
  let mean (cfg : Fin N → W) (hf : ∀ j, MemLp (fun z : X × ℝ => K (cfg j) z.1) 2 P) :
      Lp ℝ 2 P := (N : ℝ)⁻¹ • ∑ j, (hf j).toLp (fun z => K (cfg j) z.1)
  let m0 : Lp ℝ 2 P := mean w0 hf0
  let m1 : Lp ℝ 2 P := mean w1 hf1
  let label : Lp ℝ 2 P := hlabel.toLp (fun z : X × ℝ => z.2)
  have hBase (cfg : Fin N → W) (hf : ∀ j, MemLp (fun z : X × ℝ => K (cfg j) z.1) 2 P) :=
    empirical_law_squared_risk_eq_L2_norm P hN cfg
      (fun q z => K q z.1) (fun z => z.2) hf hlabel
  have hMean (cfg : Fin N → W) (hf : ∀ j, MemLp (fun z : X × ℝ => K (cfg j) z.1) 2 P) :
      (fun z => mean cfg hf z) =ᵐ[P]
        (fun z : X × ℝ => predictor (rhoOf cfg) z.1) := by
    filter_upwards [Lp.coeFn_smul (N : ℝ)⁻¹ (∑ j, (hf j).toLp (fun z => K (cfg j) z.1)),
      Lp.coeFn_fun_finsetSum Finset.univ (fun j => (hf j).toLp (fun z => K (cfg j) z.1)),
      ae_all_iff.2 (fun j => (hf j).coeFn_toLp)] with z hsmul hsum hj
    change (((N : ℝ)⁻¹ • ∑ j, (hf j).toLp (fun z => K (cfg j) z.1)) z) = _
    simp only [Pi.smul_apply, smul_eq_mul] at hsmul
    rw [hsmul, hsum, hPred]
    congr 1
    exact Finset.sum_congr rfl (fun j _ => hj j)
  have hResidual : (fun z => (m0 - label) z) =ᵐ[P]
      (fun z : X × ℝ => predictor (rhoOf w0) z.1 - z.2) := by
    filter_upwards [Lp.coeFn_sub m0 label, hMean w0 hf0, hlabel.coeFn_toLp]
      with z hsub hm hy
    simp only [Pi.sub_apply] at hsub
    rw [hsub, hm, hy]
  have hPotMean (cfg : Fin N → W)
      (hf : ∀ j, MemLp (fun z : X × ℝ => K (cfg j) z.1) 2 P) :
      (∫ q, potential q ∂rhoOf cfg) = 2 * ⟪m0 - label, mean cfg hf⟫_ℝ := by
    have hpot (j : Fin N) : potential (cfg j) =
        2 * ⟪m0 - label, (hf j).toLp (fun z => K (cfg j) z.1)⟫_ℝ := by
      dsimp only [potential]
      rw [L2.inner_def]
      congr 1
      apply integral_congr_ae
      filter_upwards [hResidual, (hf j).coeFn_toLp] with z hr hj
      simp only [Real.inner_apply, hr, hj]
    rw [hEval]
    simp_rw [hpot]
    dsimp only [mean]
    rw [real_inner_smul_right, inner_sum, ← Finset.mul_sum]
    ring
  have hPair : ((∫ q, potential q ∂rhoOf w1) - (∫ q, potential q ∂rhoOf w0)) =
      2 * ⟪m0 - label, m1 - m0⟫_ℝ := by
    rw [hPotMean w1 hf1, hPotMean w0 hf0, inner_sub_right]
    dsimp only [m0, m1]
    ring
  have hCurvePred (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) 1) (x : X) :
      predictor (curve t) x =
        (1 - t) * predictor (rhoOf w0) x + t * predictor (rhoOf w1) x := by
    dsimp only [predictor, curve]
    rw [integral_add_measure
      ((hInt w0 (fun q => K q x)).smul_measure ENNReal.ofReal_ne_top)
      ((hInt w1 (fun q => K q x)).smul_measure ENNReal.ofReal_ne_top)]
    simp only [integral_smul_measure, ENNReal.toReal_ofReal (sub_nonneg.mpr ht.2),
      ENNReal.toReal_ofReal ht.1, smul_eq_mul]
  have hPredLp (cfg : Fin N → W)
      (hf : ∀ j, MemLp (fun z : X × ℝ => K (cfg j) z.1) 2 P) :
      MemLp (fun z : X × ℝ => predictor (rhoOf cfg) z.1) 2 P := by
    have hs := (memLp_finsetSum Finset.univ (fun j _ => hf j)).const_smul (N : ℝ)⁻¹
    exact hs.ae_eq (Filter.Eventually.of_forall (fun z => (hPred cfg z.1).symm))
  have hMixLp (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) 1) :
      MemLp (fun z : X × ℝ => predictor (curve t) z.1 - z.2) 2 P := by
    have hs := (((hPredLp w0 hf0).const_smul (1 - t)).add
      ((hPredLp w1 hf1).const_smul t)).sub hlabel
    exact hs.ae_eq (Filter.Eventually.of_forall (fun z => by
      change (1 - t) * predictor (rhoOf w0) z.1 +
        t * predictor (rhoOf w1) z.1 - z.2 = predictor (curve t) z.1 - z.2
      rw [hCurvePred t ht]))
  have hMixAE (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) 1) :
      (fun z => ((1 - t) • m0 + t • m1 - label) z) =ᵐ[P]
        (fun z : X × ℝ => predictor (curve t) z.1 - z.2) := by
    filter_upwards [Lp.coeFn_sub ((1 - t) • m0 + t • m1) label,
      Lp.coeFn_add ((1 - t) • m0) (t • m1),
      Lp.coeFn_smul (1 - t) m0, Lp.coeFn_smul t m1,
      hMean w0 hf0, hMean w1 hf1, hlabel.coeFn_toLp]
      with z hsub hadd hsm0 hsm1 hm0 hm1 hy
    simp only [Pi.sub_apply, Pi.add_apply, Pi.smul_apply, smul_eq_mul] at hsub hadd hsm0 hsm1
    rw [hsub, hadd, hsm0, hsm1, hm0, hm1, hy, hCurvePred t ht]
  have hRiskCurve (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) 1) :
      risk (curve t) = ‖(1 - t) • m0 + t • m1 - label‖ ^ 2 := by
    dsimp only [risk]
    rw [← real_inner_self_eq_norm_sq, L2.inner_def]
    symm
    apply integral_congr_ae
    filter_upwards [hMixAE t ht] with z hz
    simp only [Real.inner_apply, hz, pow_two]
  have hProps (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) 1) :
      IsProbabilityMeasure (curve t) ∧
      Integrable (fun z : X × ℝ => (predictor (curve t) z.1 - z.2) ^ 2) P := by
    refine ⟨?_, (hMixLp t ht).integrable_sq⟩
    letI : IsProbabilityMeasure (rhoOf w0) := (hBase w0 hf0).1
    letI : IsProbabilityMeasure (rhoOf w1) := (hBase w1 hf1).1
    apply isProbabilityMeasure_iff.mpr
    simp only [curve, Measure.add_apply, Measure.smul_apply, measure_univ, smul_eq_mul, mul_one]
    rw [← ENNReal.ofReal_add (sub_nonneg.mpr ht.2) ht.1]
    norm_num
  refine ⟨hProps, hInt w0 potential, hInt w1 potential, ?_⟩
  rw [hPair]
  have hlin : HasDerivAt (fun t : ℝ => m0 + t • (m1 - m0) - label) (m1 - m0) 0 := by
    have hs : HasDerivAt (fun t : ℝ => t • (m1 - m0)) (m1 - m0) 0 := by
      simpa only [one_smul, id_eq] using (hasDerivAt_id (0 : ℝ)).smul_const (m1 - m0)
    exact (hs.const_add m0).sub_const label
  have hd : HasDerivAt (fun t : ℝ => ‖m0 + t • (m1 - m0) - label‖ ^ 2)
      (2 * ⟪m0 - label, m1 - m0⟫_ℝ) 0 := by
    simpa only [zero_smul, add_zero] using hlin.norm_sq
  apply hd.hasDerivWithinAt.congr_of_mem
  · intro t ht
    rw [hRiskCurve t ht]
    congr 2
    rw [sub_smul, one_smul, smul_sub]
    abel
  · exact ⟨le_rfl, zero_le_one⟩


end AutoSamplingTheory.TechnicalLemmas.Analysis.JointEmpiricalSegmentRisk
