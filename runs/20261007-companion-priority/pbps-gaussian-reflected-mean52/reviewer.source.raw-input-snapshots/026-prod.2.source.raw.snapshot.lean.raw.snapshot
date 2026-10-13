import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity

/-!
# Literal Gaussian posterior reflection: compact-observer regularity

Authored background for PBPS arXiv:2609.06905v1 Appendix C.1 normalized
conditional-density differentiation. The probability input, compact C1 observer
and finite Hilbert/rank-zero scope explicitly generalize the paper's Gibbs input
and smooth compact tests. The result concerns the specified posterior at every
parameter, not an arbitrary almost-everywhere conditional representative.

The source-density pointwise adapter, actual Tf closed-gradient membership,
rough B.13, hypocoercivity, algorithm errors and main/query-cost results remain
separate. Domination and derivative continuity are proved internally.
-/

open MeasureTheory Filter Set
open scoped Topology InnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean

noncomputable section
set_option maxHeartbeats 800000
set_option backward.isDefEq.respectTransparency false

/-- Compact C1 observables have C1 means under the literal reflected Gaussian
posterior. No input moment, density or analytic certificate is assumed. -/
theorem gaussian_reflected_mean_c1
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η)
    {f : E → ℝ} (hf : ContDiff ℝ 1 f) (hc : HasCompactSupport f) :
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    let S := fun y : E => (R y).map (fun x : E => (2:ℝ) • x-y)
    ContDiff ℝ 1 (fun y : E => ∫ u, f u ∂S y)
 := by
  let K := fun y x : E => Real.exp (-‖y-x‖^2/(2*η))
  let K' := fun y x : E => (-K y x/η) • innerSL ℝ (y-x)
  let F := fun y x : E => K y x * f ((2:ℝ) • x-y)
  let G := fun y x : E => K y x • (-fderiv ℝ f ((2:ℝ) • x-y)) +
    f ((2:ℝ) • x-y) • K' y x
  let N := fun y : E => ∫ x, F y x ∂μ
  let D := fun y : E => ∫ x, G y x ∂μ
  let Z := fun y : E => ∫ x, K y x ∂μ
  have hdfC : Continuous (fderiv ℝ f) := hf.continuous_fderiv one_ne_zero
  obtain ⟨Mf, hMf⟩ := hc.exists_bound_of_continuous hf.continuous
  obtain ⟨Md, hMd⟩ := (hc.fderiv ℝ).exists_bound_of_continuous hdfC
  have hMf0 : 0 ≤ Mf := (norm_nonneg (f 0)).trans (hMf 0)
  have hK (y x : E) : 0 < K y x ∧ K y x ≤ 1 ∧ K y x * ‖y-x‖^2 ≤ 2*η := by
    have hp : 0 < K y x := Real.exp_pos _
    have h1 : K y x ≤ 1 := Real.exp_le_one_iff.mpr
      (div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg _)) (by positivity))
    have hb := Real.mul_exp_neg_le_exp_neg_one (‖y-x‖^2/(2*η))
    have he : Real.exp (-1) ≤ 1 := Real.exp_le_one_iff.mpr (by norm_num)
    have hb' : K y x * (‖y-x‖^2/(2*η)) ≤ 1 := by
      simpa [K, mul_comm, neg_div] using hb.trans he
    have heq : K y x * (‖y-x‖^2/(2*η)) = (K y x * ‖y-x‖^2)/(2*η) := by ring
    rw [heq, div_le_iff₀ (by positivity)] at hb'
    exact ⟨hp,h1,by simpa using hb'⟩
  have hKderiv (y x : E) : HasFDerivAt (fun z => K z x) (K' y x) y := by
    have hd := (((hasFDerivAt_id y).sub_const x).norm_sq.const_mul (-1/(2*η))).exp
    convert hd using 1
    · funext z; dsimp only [K,id]; congr 1; ring
    · ext v
      have he : -‖y-x‖^2/(2*η) = (-1/(2*η))*‖y-x‖^2 := by ring
      simp only [K',K,he,smul_apply,ContinuousLinearMap.comp_apply,
        ContinuousLinearMap.id_apply,smul_eq_mul,innerSL_apply_apply,id]
      ring
  have hKbound (y x : E) : ‖K' y x‖ ≤ (1+2*η)/η := by
    obtain ⟨hp,h1,h2⟩ := hK y x
    have hr : ‖y-x‖ ≤ 1+‖y-x‖^2 := by nlinarith [sq_nonneg (‖y-x‖-1)]
    have hb : K y x * ‖y-x‖ ≤ 1+2*η := by
      calc
        _ ≤ K y x * (1+‖y-x‖^2) := mul_le_mul_of_nonneg_left hr hp.le
        _ ≤ 1+2*η := by nlinarith
    dsimp only [K']
    rw [norm_smul,Real.norm_eq_abs,abs_div,abs_neg,abs_of_pos hp,
      abs_of_pos hη,innerSL_apply_norm,div_mul_eq_mul_div,div_le_div_iff_of_pos_right hη]
    exact hb
  have hGbound (y x : E) : ‖G y x‖ ≤ Md + Mf*((1+2*η)/η) := by
    have hk := hK y x
    calc
      _ ≤ ‖K y x • (-fderiv ℝ f ((2:ℝ) • x-y))‖ +
          ‖f ((2:ℝ) • x-y) • K' y x‖ := norm_add_le _ _
      _ = K y x * ‖fderiv ℝ f ((2:ℝ) • x-y)‖ +
          ‖f ((2:ℝ) • x-y)‖ * ‖K' y x‖ := by
            rw [norm_smul,norm_smul,norm_neg,Real.norm_eq_abs,abs_of_pos hk.1]
      _ ≤ 1*Md + Mf*((1+2*η)/η) := add_le_add
        (mul_le_mul hk.2.1 (hMd _) (norm_nonneg _) (by norm_num))
        (mul_le_mul (hMf _) (hKbound y x) (norm_nonneg _) hMf0)
      _ = _ := by ring
  have hFmeas (y : E) : AEStronglyMeasurable (F y) μ := by
    apply Continuous.aestronglyMeasurable
    have hk : Continuous (K y) := by unfold K; fun_prop
    exact hk.mul (hf.continuous.comp (by fun_prop))
  have hGmeas (y : E) : AEStronglyMeasurable (G y) μ := by
    apply Continuous.aestronglyMeasurable
    dsimp only [G,K',K]
    have hd : Continuous (fun x : E => fderiv ℝ f ((2:ℝ) • x-y)) :=
      hdfC.comp (by fun_prop)
    have ho : Continuous (fun x : E => f ((2:ℝ) • x-y)) := hf.continuous.comp (by fun_prop)
    fun_prop
  have hFI (y : E) : Integrable (F y) μ := by
    apply (integrable_const Mf).mono' (hFmeas y)
    filter_upwards with x
    dsimp only [F]
    rw [norm_mul,Real.norm_eq_abs,abs_of_pos (hK y x).1]
    calc
      _ ≤ 1*Mf := mul_le_mul (hK y x).2.1 (hMf _) (norm_nonneg _) (by norm_num)
      _ = _ := one_mul _
  have hFderiv (y x : E) : HasFDerivAt (fun z => F z x) (G y x) y := by
    have ha := (hasFDerivAt_id (𝕜 := ℝ) y).const_sub ((2:ℝ) • x)
    have ho := (hf.differentiable_one ((2:ℝ) • x-y)).hasFDerivAt.comp y ha
    have ho' : HasFDerivAt (fun z : E => f ((2:ℝ) • x-z))
        (-fderiv ℝ f ((2:ℝ) • x-y)) y := by
      convert ho using 1
      ext v
      simp
    exact (hKderiv y x).mul ho'
  have hdN (y : E) : HasFDerivAt N (D y) y := by
    apply hasFDerivAt_integral_of_dominated_of_fderiv_le (s := Set.univ)
      (bound := fun _ => Md+Mf*((1+2*η)/η)) Filter.univ_mem
    · exact Filter.Eventually.of_forall hFmeas
    · exact hFI y
    · exact hGmeas y
    · exact Filter.Eventually.of_forall (fun x z _ => hGbound z x)
    · exact integrable_const _
    · exact Filter.Eventually.of_forall (fun x z _ => hFderiv z x)
  have hDC : Continuous D := by
    apply continuous_of_dominated hGmeas
      (bound := fun _ => Md+Mf*((1+2*η)/η))
      (fun y => Filter.Eventually.of_forall (fun x => hGbound y x)) (integrable_const _)
    filter_upwards with x
    dsimp only [G,K',K]
    have hd : Continuous (fun y : E => fderiv ℝ f ((2:ℝ) • x-y)) := hdfC.comp (by fun_prop)
    have ho : Continuous (fun y : E => f ((2:ℝ) • x-y)) := hf.continuous.comp (by fun_prop)
    fun_prop
  have hNC : ContDiff ℝ 1 N := contDiff_one_iff_hasFDerivAt.mpr ⟨D,hDC,hdN⟩
  have hparent := GaussianConvolutionRegularity.gaussian_convolution_potential_c2 μ hη
  have hZC : ContDiff ℝ 2 Z := hparent.2.2.1
  have hZ (y : E) : Z y ≠ 0 := by
    have hp := hparent.2.1 y
    intro hz
    change 0 < ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E * Z y at hp
    rw [hz,mul_zero] at hp
    exact lt_irrefl _ hp
  have hKI (y : E) : Integrable (K y) μ := by
    apply (integrable_const (1:ℝ)).mono' (by unfold K; fun_prop)
    filter_upwards with x
    rw [Real.norm_eq_abs,abs_of_pos (hK y x).1]
    exact (hK y x).2.1
  have hmean (y : E) :
      (∫ u, f u ∂((μ.tilted (fun x => -‖x-y‖^2/(2*η))).map
        (fun x : E => (2:ℝ) • x-y))) = N y / Z y := by
    have hlike : Integrable (fun x : E => Real.exp (-‖x-y‖^2/(2*η))) μ := by
      simpa only [K,norm_sub_rev] using hKI y
    have : IsProbabilityMeasure (μ.tilted (fun x => -‖x-y‖^2/(2*η))) :=
      isProbabilityMeasure_tilted hlike
    have hobs : Integrable (fun x : E => f ((2:ℝ) • x-y))
        (μ.tilted (fun x => -‖x-y‖^2/(2*η))) := by
      apply (integrable_const Mf).mono' (hf.continuous.comp (by fun_prop)).aestronglyMeasurable
      exact Filter.Eventually.of_forall (fun x => hMf _)
    have hmapI : Integrable f ((μ.tilted (fun x => -‖x-y‖^2/(2*η))).map
        (fun x : E => (2:ℝ) • x-y)) :=
      (integrable_map_measure hf.continuous.aestronglyMeasurable (by fun_prop)).mpr hobs
    rw [integral_map (by fun_prop) hmapI.aestronglyMeasurable,integral_tilted]
    have hw (x : E) : Real.exp (-‖x-y‖^2/(2*η)) = K y x := by
      dsimp [K]; rw [norm_sub_rev x y]
    simp_rw [hw,smul_eq_mul]
    rw [← integral_div]
    apply integral_congr_ae
    filter_upwards with x
    dsimp [N,Z,F]
    ring
  change ContDiff ℝ 1 (fun y : E => ∫ u, f u ∂((μ.tilted
    (fun x => -‖x-y‖^2/(2*η))).map (fun x : E => (2:ℝ) • x-y)))
  simp_rw [hmean]
  exact hNC.div (hZC.of_le (by norm_num)) hZ

end
end AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean
