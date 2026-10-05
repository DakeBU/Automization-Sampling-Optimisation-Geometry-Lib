import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic
import AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation

open MeasureTheory ProbabilityTheory Filter Set
open scoped Topology InnerProductSpace
/-!
# Actual Gaussian convolution potential regularity

The actual independent Gaussian add-noise marginal has a positive density
C_eta Z_eta. Derive global C2 regularity of its negative logarithm, with no
input density or moment assumption, from explicit Gaussian first/second
derivative domination against the probability input law.

This is the analytic producer behind SPHMC2609.06906v1 Section4.1 smoothing
and PBPS2609.06905v1 Section2.2 augmentation normalization. Covariance/curvature,
higher regularity, invariance, algorithm error and either main theorem remain
separate. The exact density prefactor includes dimension zero.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity

noncomputable section
set_option backward.isDefEq.respectTransparency false
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
private local instance : NormedSpace ℝ ℝ := NormedField.toNormedSpace
private local instance : NormedAddCommGroup (E →L[ℝ] ℝ) := ContinuousLinearMap.toNormedAddCommGroup
private local instance : NormedSpace ℝ (E →L[ℝ] ℝ) := ContinuousLinearMap.toNormedSpace

private def gaussianWeight (η : ℝ) (y x : E) : ℝ := Real.exp (-‖y-x‖^2/(2*η))
private def gaussianFirst (η : ℝ) (y x : E) : E →L[ℝ] ℝ :=
  (-gaussianWeight η y x/η) • innerSL ℝ (y-x)

private theorem gaussianDeriv (η : ℝ) (y x : E) :
    HasFDerivAt (fun z => gaussianWeight η z x) (gaussianFirst η y x) y := by
  have hd := (((hasFDerivAt_id y).sub_const x).norm_sq.const_mul (-1/(2*η))).exp
  convert hd using 1
  · funext z
    dsimp only [gaussianWeight, id]
    congr 1
    ring
  · ext v
    dsimp only [id]
    have he : -‖y-x‖^2/(2*η) = (-1/(2*η))*‖y-x‖^2 := by ring
    simp only [gaussianFirst,gaussianWeight,he,smul_apply,
      ContinuousLinearMap.comp_apply,ContinuousLinearMap.id_apply,smul_eq_mul,
      innerSL_apply_apply]
    ring

private theorem gaussianSmooth (η : ℝ) (x : E) : ContDiff ℝ 2 (fun y => gaussianWeight η y x) := by
  have hn : ContDiff ℝ 2 (fun y : E => ‖y-x‖^2) :=
    (contDiff_id.sub contDiff_const).norm_sq (𝕜 := ℝ)
  have hm : ContDiff ℝ 2 (fun y : E => (-1/(2*η))*‖y-x‖^2) := contDiff_const.mul hn
  convert hm.exp using 1 <;> try rfl
  funext y
  dsimp only [gaussianWeight, id]
  congr 1
  ring

private theorem weight_bounds {η : ℝ} (hη : 0 < η) (y x : E) :
    0 < gaussianWeight η y x ∧ gaussianWeight η y x ≤ 1 ∧
      gaussianWeight η y x * ‖y-x‖^2 ≤ 2*η := by
  have hw := Real.exp_pos (-‖y-x‖^2/(2*η))
  have h1 : gaussianWeight η y x ≤ 1 := Real.exp_le_one_iff.mpr
    (div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg _)) (by positivity))
  have hb := Real.mul_exp_neg_le_exp_neg_one (‖y-x‖^2/(2*η))
  have he : Real.exp (-1) ≤ 1 := Real.exp_le_one_iff.mpr (by norm_num)
  have hb' : gaussianWeight η y x * (‖y-x‖^2/(2*η)) ≤ 1 := by
    dsimp [gaussianWeight]; simpa [mul_comm, neg_div] using hb.trans he
  have heq : gaussianWeight η y x * (‖y-x‖^2/(2*η)) =
      (gaussianWeight η y x * ‖y-x‖^2)/(2*η) := by ring
  rw [heq, div_le_iff₀ (by positivity)] at hb'
  exact ⟨hw,h1,by simpa using hb'⟩

private theorem first_bound {η : ℝ} (hη : 0 < η) (y x : E) :
    ‖gaussianFirst η y x‖ ≤ (1+2*η)/η := by
  obtain ⟨hw,h1,h2⟩ := weight_bounds hη y x
  have hr : ‖y-x‖ ≤ 1+‖y-x‖^2 := by nlinarith [sq_nonneg (‖y-x‖-1)]
  have hb : gaussianWeight η y x * ‖y-x‖ ≤ 1+2*η := by
    calc
      _ ≤ gaussianWeight η y x * (1+‖y-x‖^2) := mul_le_mul_of_nonneg_left hr hw.le
      _ ≤ 1+2*η := by nlinarith
  rw [gaussianFirst, norm_smul, Real.norm_eq_abs, abs_div,
    abs_neg, abs_of_pos hw, abs_of_pos hη, innerSL_apply_norm]
  rw [div_mul_eq_mul_div, div_le_div_iff_of_pos_right hη]
  exact hb

private def realDual : E →L[ℝ] (E →L[ℝ] ℝ) := innerSL ℝ

private def gaussianSecond (η : ℝ) (y x : E) : E →L[ℝ] (E →L[ℝ] ℝ) :=
  (-gaussianWeight η y x/η) • realDual +
    ((-1/η) • gaussianFirst η y x).smulRight (innerSL ℝ (y-x))

private theorem gaussianFirstDeriv (η : ℝ) (y x : E) :
    HasFDerivAt (fun z => gaussianFirst η z x) (gaussianSecond η y x) y := by
  have hc := (gaussianDeriv η y x).const_mul (-1/η)
  have hl := (realDual (E := E)).hasFDerivAt.comp y ((hasFDerivAt_id y).sub_const x)
  convert hc.smul hl using 1 <;> try rfl
  · funext z; dsimp [gaussianFirst]; congr 1; ring
  · ext v w
    change ((gaussianSecond η y x) v) w = _
    simp [gaussianSecond, realDual, gaussianFirst,
      innerSL_apply_apply]
    dsimp [innerSL]
    ring

private theorem second_bound {η : ℝ} (hη : 0 < η) (y x : E) :
    ‖gaussianSecond η y x‖ ≤ 3/η := by
  obtain ⟨hw,h1,h2⟩ := weight_bounds hη y x
  have ha : ‖(-gaussianWeight η y x/η) •
      (realDual (E := E))‖ ≤ 1/η := by
    rw [norm_smul, Real.norm_eq_abs, abs_div, abs_neg, abs_of_pos hw, abs_of_pos hη]
    calc
      _ ≤ (gaussianWeight η y x/η)*1 :=
        mul_le_mul_of_nonneg_left (show ‖(realDual (E := E))‖ ≤ 1 from
          norm_innerSL_le (𝕜 := ℝ)) (by positivity)
      _ ≤ 1/η := by simpa using (div_le_div_iff_of_pos_right hη).mpr h1
  have hb : ‖((-1/η) • gaussianFirst η y x).smulRight (innerSL ℝ (y-x))‖ ≤ 2/η := by
    rw [ContinuousLinearMap.norm_smulRight_apply, norm_smul, Real.norm_eq_abs,
      abs_div, abs_neg, abs_one, abs_of_pos hη, gaussianFirst, norm_smul,
      Real.norm_eq_abs, abs_div, abs_neg, abs_of_pos hw, abs_of_pos hη,
      innerSL_apply_norm]
    have heq : (1/η*(gaussianWeight η y x/η*‖y-x‖))*‖y-x‖ =
        (gaussianWeight η y x*‖y-x‖^2)/η^2 := by ring
    rw [heq, div_le_iff₀ (sq_pos_of_pos hη)]
    calc
      _ ≤ 2*η := h2
      _ = 2/η*η^2 := by field_simp
  dsimp only [gaussianSecond]
  calc
    _ ≤ ‖(-gaussianWeight η y x/η) • (realDual (E := E))‖ +
      ‖((-1/η) • gaussianFirst η y x).smulRight (innerSL ℝ (y-x))‖ := norm_add_le _ _
    _ ≤ 1/η+2/η := add_le_add ha hb
    _ = 3/η := by ring

variable [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]

private theorem gaussianNormalizerRegularity (μ : Measure E) [IsProbabilityMeasure μ]
    {η : ℝ} (hη : 0 < η) :
    let Z := fun y : E => ∫ x, gaussianWeight η y x ∂μ
    (∀ y, 0 < Z y) ∧ ContDiff ℝ 2 Z ∧
      ∀ C : ℝ, 0 < C → ContDiff ℝ 2 (fun y => -Real.log (C*Z y)) := by
  let Z := fun y : E => ∫ x, gaussianWeight η y x ∂μ
  let D := fun y : E => ∫ x, gaussianFirst η y x ∂μ
  let H := fun y : E => ∫ x, gaussianSecond η y x ∂μ
  have hI (y : E) : Integrable (gaussianWeight η y) μ := by
    apply (integrable_const (1 : ℝ)).mono' (by unfold gaussianWeight; fun_prop)
    filter_upwards with x
    rw [Real.norm_eq_abs, abs_of_pos (weight_bounds hη y x).1]
    exact (weight_bounds hη y x).2.1
  have hZ (y : E) : 0 < Z y := integral_exp_pos (hI y)
  have hDmeas (y : E) : AEStronglyMeasurable (gaussianFirst η y) μ := by
    apply Continuous.aestronglyMeasurable
    unfold gaussianFirst gaussianWeight
    fun_prop
  have hHmeas (y : E) : AEStronglyMeasurable (gaussianSecond η y) μ := by
    apply Continuous.aestronglyMeasurable
    unfold gaussianSecond gaussianFirst gaussianWeight
    fun_prop
  have hDI (y : E) : Integrable (gaussianFirst η y) μ := by
    apply (integrable_const ((1+2*η)/η)).mono' (hDmeas y)
    filter_upwards with x
    exact first_bound hη y x
  have hdZ (y : E) : HasFDerivAt Z (D y) y := by
    apply hasFDerivAt_integral_of_dominated_of_fderiv_le (s := Set.univ)
      (bound := fun _ => (1+2*η)/η) (Filter.univ_mem)
    · exact Filter.Eventually.of_forall (fun z => (hI z).aestronglyMeasurable)
    · exact hI y
    · exact hDmeas y
    · exact Filter.Eventually.of_forall (fun x z _ => first_bound hη z x)
    · exact integrable_const _
    · exact Filter.Eventually.of_forall (fun x z _ => gaussianDeriv η z x)
  have hdD (y : E) : HasFDerivAt D (H y) y := by
    apply hasFDerivAt_integral_of_dominated_of_fderiv_le (s := Set.univ)
      (bound := fun _ => 3/η) (Filter.univ_mem)
    · exact Filter.Eventually.of_forall hDmeas
    · exact hDI y
    · exact hHmeas y
    · exact Filter.Eventually.of_forall (fun x z _ => second_bound hη z x)
    · exact integrable_const _
    · exact Filter.Eventually.of_forall (fun x z _ => gaussianFirstDeriv η z x)
  have hHC : Continuous H := by
    apply continuous_of_dominated hHmeas
      (bound := fun _ => 3/η) (fun y => Filter.Eventually.of_forall (fun x => second_bound hη y x))
      (integrable_const _)
    filter_upwards with x
    unfold gaussianSecond gaussianFirst gaussianWeight
    fun_prop
  have hDC : ContDiff ℝ 1 D := contDiff_one_iff_fderiv.mpr
    ⟨fun y => (hdD y).differentiableAt, by
      have he : fderiv ℝ D = H := funext (fun y => (hdD y).fderiv)
      rw [he]; exact hHC⟩
  have hZC : ContDiff ℝ 2 Z := by
    rw [show (2 : WithTop ℕ∞) = 1+1 by norm_num, contDiff_succ_iff_fderiv]
    refine ⟨fun y => (hdZ y).differentiableAt, by simp, ?_⟩
    have he : fderiv ℝ Z = D := funext (fun y => (hdZ y).fderiv)
    rw [he]; exact hDC
  refine ⟨hZ,hZC,fun C hC => ?_⟩
  exact ((contDiff_const.mul hZC).log (fun y => (mul_pos hC (hZ y)).ne')).neg

private theorem gaussianDensity (μ : Measure E) [IsProbabilityMeasure μ]
    {η : ℝ} (hη : 0 < η) :
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
    let Z := fun y : E => ∫ x, gaussianWeight η y x ∂μ
    (μ.prod (stdGaussian E)).map (fun p => p.1+Real.sqrt η • p.2) =
      (volume : Measure E).withDensity (fun y => ENNReal.ofReal (C*Z y)) := by
  let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
  let Z := fun y : E => ∫ x, gaussianWeight η y x ∂μ
  have hC : 0 ≤ C := by dsimp [C]; positivity
  have hZC : ContDiff ℝ 2 Z := (gaussianNormalizerRegularity μ hη).2.1
  have hden : Measurable (fun y => ENNReal.ofReal (C*Z y)) :=
    (measurable_const.mul hZC.continuous.measurable).ennreal_ofReal
  have hI (y : E) : Integrable (gaussianWeight η y) μ := by
    apply (integrable_const (1 : ℝ)).mono' (by unfold gaussianWeight; fun_prop)
    filter_upwards with x
    rw [Real.norm_eq_abs, abs_of_pos (weight_bounds hη y x).1]
    exact (weight_bounds hη y x).2.1
  have hJ := AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation.augmentation_eq_withDensity μ η hη
  have hmap : (μ.prod (stdGaussian E)).map (fun p => p.1+Real.sqrt η • p.2) =
      ((μ.prod (stdGaussian E)).map (fun p => (p.1,p.1+Real.sqrt η • p.2))).map Prod.snd := by
    rw [Measure.map_map (by fun_prop) (by fun_prop)]
    rfl
  rw [hmap,hJ]
  apply Measure.ext_of_lintegral
  intro f hf
  rw [lintegral_map hf (by fun_prop)]
  rw [lintegral_withDensity_eq_lintegral_mul (μ.prod (volume : Measure E))
      (by fun_prop) (g := fun p : E × E => f p.2) (hf.comp measurable_snd)]
  rw [lintegral_prod_symm _ (by fun_prop),
    lintegral_withDensity_eq_lintegral_mul (volume : Measure E) hden (g := f) hf]
  refine lintegral_congr (fun y => ?_)
  change (∫⁻ x, ENNReal.ofReal (C*gaussianWeight η y x)*f y ∂μ) =
    ENNReal.ofReal (C*Z y)*f y
  rw [lintegral_mul_const _ (by unfold gaussianWeight; fun_prop)]
  congr 1
  simpa only [Z, integral_const_mul] using
    (ofReal_integral_eq_lintegral_ofReal ((hI y).const_mul C)
      (Filter.Eventually.of_forall (fun x => mul_nonneg hC (weight_bounds hη y x).1.le))).symm

/-- The actual Gaussian-smoothed probability law has the displayed everywhere
positive density; its normalizer and exact negative-log density are globally C2.
No finite moments, input Lebesgue density or supplied regularity are required. -/
theorem gaussian_convolution_potential_c2 (μ : Measure E) [IsProbabilityMeasure μ]
    {η : ℝ} (hη : 0 < η) :
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
    let Z := fun y : E => ∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ
    (μ.prod (stdGaussian E)).map (fun p => p.1+Real.sqrt η • p.2) =
      (volume : Measure E).withDensity (fun y => ENNReal.ofReal (C*Z y)) ∧
    (∀ y, 0 < C*Z y) ∧ ContDiff ℝ 2 Z ∧
      ContDiff ℝ 2 (fun y => -Real.log (C*Z y)) := by
  let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
  have hC : 0 < C := by dsimp [C]; positivity
  obtain ⟨hZ,hZC,hV⟩ := gaussianNormalizerRegularity μ hη
  exact ⟨gaussianDensity μ hη,fun y => mul_pos hC (hZ y),hZC,hV C hC⟩

end
end AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
