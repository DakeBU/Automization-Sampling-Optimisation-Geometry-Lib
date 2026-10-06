import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Probability.Moments.CovarianceBilin
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
and PBPS2609.06905v1 Section2.2 augmentation normalization. Actual posterior
score and covariance derivative identities are proved below. Quantitative
covariance inequalities/curvature, higher regularity, invariance, algorithm
error and either main theorem remain separate. The exact density prefactor
includes dimension zero.
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
    let D := fun y : E => ∫ x, gaussianFirst η y x ∂μ
    let H := fun y : E => ∫ x, gaussianSecond η y x ∂μ
    (∀ y, 0 < Z y) ∧ ContDiff ℝ 2 Z ∧
      (∀ C : ℝ, 0 < C → ContDiff ℝ 2 (fun y => -Real.log (C*Z y))) ∧
      (∀ y, HasFDerivAt Z (D y) y) ∧ (∀ y, HasFDerivAt D (H y) y) := by
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
  refine ⟨hZ,hZC,?_,hdZ,hdD⟩
  intro C hC
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
  obtain ⟨hZ,hZC,hV,_hdZ,_hdD⟩ := gaussianNormalizerRegularity μ hη
  exact ⟨gaussianDensity μ hη,fun y => mul_pos hC (hZ y),hZC,hV C hC⟩

private theorem normalizerDerivatives (μ : Measure E) [IsProbabilityMeasure μ]
    {η : ℝ} (hη : 0 < η) :
    let Z := fun y : E => ∫ x, gaussianWeight η y x ∂μ
    let D := fun y : E => ∫ x, gaussianFirst η y x ∂μ
    let H := fun y : E => ∫ x, gaussianSecond η y x ∂μ
    (∀ y, 0 < Z y) ∧ (∀ y, HasFDerivAt Z (D y) y) ∧
      (∀ y, HasFDerivAt D (H y) y) := by
  obtain ⟨hZ,_hZC,_hVC,hdZ,hdD⟩ := gaussianNormalizerRegularity μ hη
  exact ⟨hZ,hdZ,hdD⟩

private theorem rawFirst (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η)
    (y v : E) :
    let Z := fun z : E => ∫ x, gaussianWeight η z x ∂μ
    let D := fun z : E => ∫ x, gaussianFirst η z x ∂μ
    fderiv ℝ (fun z => -Real.log (Z z)) y v = -(D y v)/(Z y) := by
  let Z := fun z : E => ∫ x, gaussianWeight η z x ∂μ
  let D := fun z : E => ∫ x, gaussianFirst η z x ∂μ
  obtain ⟨hZ,hdZ,_hdD⟩ := normalizerDerivatives μ hη
  have hu := ((hdZ y).log (hZ y).ne').neg
  change (fderiv ℝ (-fun z => Real.log (∫ x, gaussianWeight η z x ∂μ)) y) v =
    -(D y v)/(Z y)
  rw [hu.fderiv]
  simp only [neg_apply,smul_apply,smul_eq_mul]
  ring

private theorem rawSecond (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η)
    (y v w : E) :
    let Z := fun z : E => ∫ x, gaussianWeight η z x ∂μ
    let D := fun z : E => ∫ x, gaussianFirst η z x ∂μ
    let H := fun z : E => ∫ x, gaussianSecond η z x ∂μ
    fderiv ℝ (fderiv ℝ (fun z => -Real.log (Z z))) y v w =
      (D y v * D y w)/(Z y)^2 - (H y v w)/(Z y) := by
  let Z := fun z : E => ∫ x, gaussianWeight η z x ∂μ
  let D := fun z : E => ∫ x, gaussianFirst η z x ∂μ
  let H := fun z : E => ∫ x, gaussianSecond η z x ∂μ
  obtain ⟨hZ,hdZ,hdD⟩ := normalizerDerivatives μ hη
  have hEq : fderiv ℝ (fun z => -Real.log (Z z)) = fun z => -((Z z)⁻¹ • D z) := by
    funext z
    exact (((hdZ z).log (hZ z).ne').neg).fderiv
  have hi := (hasDerivAt_inv (hZ y).ne').comp_hasFDerivAt y (hdZ y)
  have hs := (hi.smul (hdD y)).neg
  have hs' : HasFDerivAt (fun z => -((Z z)⁻¹ • D z))
      (-((Z y)⁻¹ • H y + (-(Z y ^ 2)⁻¹ • D y).smulRight (D y))) y := by
    convert hs using 1 <;> rfl
  change (fderiv ℝ (fderiv ℝ (fun z => -Real.log (Z z))) y) v w = _
  rw [hEq]
  rw [hs'.fderiv]
  simp only [neg_apply, add_apply, smul_apply,
    ContinuousLinearMap.smulRight_apply, smul_eq_mul]
  ring

private theorem posteriorIntegral (μ : Measure E) (η : ℝ) (y : E) (g : E → ℝ) :
    (∫ x, g x ∂(μ.tilted (fun x => -‖x-y‖^2/(2*η)))) =
      (∫ x, gaussianWeight η y x*g x ∂μ)/(∫ x, gaussianWeight η y x ∂μ) := by
  rw [integral_tilted]
  have hw (x : E) : Real.exp (-‖x-y‖^2/(2*η)) = gaussianWeight η y x := by
    unfold gaussianWeight
    rw [norm_sub_rev x y]
  simp_rw [hw, smul_eq_mul]
  rw [← integral_div]
  apply integral_congr_ae
  filter_upwards with x
  ring

private theorem normalizedFirst (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) (y v : E) :
    ((∫ x, gaussianFirst η y x ∂μ) v)/(∫ x, gaussianWeight η y x ∂μ) =
      -(∫ x, inner ℝ (y-x) v ∂(μ.tilted (fun x => -‖x-y‖^2/(2*η))))/η := by
  have hi : Integrable (gaussianFirst η y) μ := by
    apply (integrable_const ((1+2*η)/η)).mono' (by
      apply Continuous.aestronglyMeasurable
      unfold gaussianFirst gaussianWeight
      fun_prop)
    filter_upwards with x
    exact first_bound hη y x
  rw [ContinuousLinearMap.integral_apply hi v, posteriorIntegral]
  simp only [gaussianFirst, smul_apply, innerSL_apply_apply, smul_eq_mul]
  have he : (fun x => (-gaussianWeight η y x/η)*inner ℝ (y-x) v) =
      (fun x => (-1/η)*(gaussianWeight η y x*inner ℝ (y-x) v)) := by
    funext x; ring
  rw [he, integral_const_mul]
  ring

private theorem normalizedSecond (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) (y v w : E) :
    (((∫ x, gaussianSecond η y x ∂μ) v) w)/(∫ x, gaussianWeight η y x ∂μ) =
      -inner ℝ v w/η +
        (∫ x, inner ℝ (y-x) v * inner ℝ (y-x) w
          ∂(μ.tilted (fun x => -‖x-y‖^2/(2*η))))/η^2 := by
  have hi : Integrable (gaussianWeight η y) μ := by
    apply (integrable_const (1:ℝ)).mono' (by unfold gaussianWeight; fun_prop)
    filter_upwards with x
    rw [Real.norm_eq_abs, abs_of_pos (weight_bounds hη y x).1]
    exact (weight_bounds hη y x).2.1
  have hiH : Integrable (gaussianSecond η y) μ := by
    apply (integrable_const (3/η)).mono' (by
      apply Continuous.aestronglyMeasurable
      unfold gaussianSecond gaussianFirst gaussianWeight
      fun_prop)
    filter_upwards with x
    exact second_bound hη y x
  let a := fun x : E => (-1/η*inner ℝ v w)*gaussianWeight η y x
  let b := fun x : E => (1/η^2)*(gaussianWeight η y x*
    (inner ℝ (y-x) v*inner ℝ (y-x) w))
  have he : (fun x => gaussianSecond η y x v w) = fun x => a x + b x := by
    funext x
    change (-gaussianWeight η y x/η)*inner ℝ v w +
      ((-1/η)*((-gaussianWeight η y x/η)*inner ℝ (y-x) v))*inner ℝ (y-x) w = _
    dsimp only [a,b]
    ring
  have hiA : Integrable a μ := hi.const_mul _
  have hiB : Integrable b μ := by
    have hs := (hiH.apply_continuousLinearMap v).apply_continuousLinearMap w
    rw [he] at hs
    convert hs.sub hiA using 1
    funext x
    simp only [Pi.sub_apply]
    ring
  rw [ContinuousLinearMap.integral_apply hiH v,
    ContinuousLinearMap.integral_apply (hiH.apply_continuousLinearMap v) w, he,
    integral_add hiA hiB]
  rw [show (∫ x, a x ∂μ) = (-1/η*inner ℝ v w)*(∫ x, gaussianWeight η y x ∂μ) by
    exact integral_const_mul _ _]
  rw [show (∫ x, b x ∂μ) = (1/η^2)*(∫ x, gaussianWeight η y x*
    (inner ℝ (y-x) v*inner ℝ (y-x) w) ∂μ) by exact integral_const_mul _ _]
  rw [posteriorIntegral]
  have hZ := (normalizerDerivatives μ hη).1 y
  field_simp [hZ.ne',hη.ne']

private theorem posteriorMoment (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) (y : E) :
    IsProbabilityMeasure (μ.tilted (fun x => -‖x-y‖^2/(2*η))) ∧
    MemLp (fun x : E => x) 2 (μ.tilted (fun x => -‖x-y‖^2/(2*η))) := by
  let w := fun x : E => Real.exp (-‖x-y‖^2/(2*η))
  have hw (x : E) : 0 < w x ∧ w x ≤ 1 ∧ w x*‖x-y‖^2 ≤ 2*η := by
    have h0 : 0 ≤ ‖x-y‖^2/(2*η) := by positivity
    have hq := Real.mul_exp_neg_le_exp_neg_one (‖x-y‖^2/(2*η))
    have h1 : Real.exp (-1) ≤ 1 := Real.exp_le_one_iff.mpr (by norm_num)
    have ha : ‖x-y‖^2/(2*η)*w x ≤ 1 := by simpa only [w,neg_div] using hq.trans h1
    have hb := (div_le_iff₀ (show (0:ℝ) < 2*η by positivity)).mp
      (show (w x*‖x-y‖^2)/(2*η) ≤ 1 by convert ha using 1 <;> ring)
    refine ⟨Real.exp_pos _,?_,by nlinarith [hb]⟩
    dsimp [w]
    apply Real.exp_le_one_iff.mpr
    exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg _)) (by positivity)
  have hi : Integrable w μ := by
    apply (integrable_const (1:ℝ)).mono' (by dsimp [w]; fun_prop)
    filter_upwards with x
    rw [Real.norm_eq_abs,abs_of_pos (hw x).1]
    exact (hw x).2.1
  have hn (x : E) : ‖x‖^2 ≤ 2*‖y‖^2+2*‖x-y‖^2 := by
    have ht : ‖x‖ ≤ ‖x-y‖+‖y‖ := by simpa only [sub_add_cancel] using norm_add_le (x-y) y
    nlinarith [norm_nonneg x,norm_nonneg y,norm_nonneg (x-y),sq_nonneg (‖y‖-‖x-y‖)]
  have hb (x : E) : w x*‖x‖^2 ≤ 2*‖y‖^2+4*η := by
    have h := mul_le_mul_of_nonneg_left (hn x) (hw x).1.le
    have hy := mul_le_mul_of_nonneg_right (hw x).2.1 (sq_nonneg ‖y‖)
    nlinarith [(hw x).2.2,h,hy]
  have hi2 : Integrable (fun x => w x*‖x‖^2) μ := by
    apply (integrable_const (2*‖y‖^2+4*η)).mono' (by dsimp [w]; fun_prop)
    filter_upwards with x
    rw [Real.norm_eq_abs,abs_of_nonneg (mul_nonneg (hw x).1.le (sq_nonneg _))]
    exact hb x
  refine ⟨isProbabilityMeasure_tilted hi,?_⟩
  apply (memLp_two_iff_integrable_sq_norm (by fun_prop)).mpr
  apply (integrable_tilted_iff hi (fun x => ‖x‖^2)).mpr
  simpa only [smul_eq_mul] using hi2

/-- Actual Gaussian posterior first/second moments and the derivative identities
of its smoothed negative-log density. Input moments, density and covariance
identities are not assumptions. Positive constant prefactors cancel exactly. -/
theorem gaussian_convolution_derivatives (μ : Measure E) [IsProbabilityMeasure μ] {η C : ℝ} (hη : 0 < η)
    (hC : 0 < C) :
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    let U := fun y : E => -Real.log (C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ)
    (∀ y, IsProbabilityMeasure (R y) ∧ MemLp (fun x : E => x) 2 (R y)) ∧
    (∀ y v, fderiv ℝ U y v = inner ℝ (y-∫ x, x ∂(R y)) v/η) ∧
    ∀ y v w, fderiv ℝ (fderiv ℝ U) y v w =
      inner ℝ v w/η - covarianceBilin (R y) v w/η^2 := by
  let Z := fun y : E => ∫ x, gaussianWeight η y x ∂μ
  let D := fun y : E => ∫ x, gaussianFirst η y x ∂μ
  let H := fun y : E => ∫ x, gaussianSecond η y x ∂μ
  let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
  let U0 := fun y : E => -Real.log (Z y)
  have hU : (fun y : E => -Real.log (C*Z y)) = fun y => U0 y-Real.log C := by
    funext y
    have hZ := (normalizerDerivatives μ hη).1 y
    rw [Real.log_mul hC.ne' hZ.ne']
    dsimp only [U0]
    ring
  have hDU : fderiv ℝ (fun y : E => -Real.log (C*Z y)) = fderiv ℝ U0 := by
    rw [hU]
    funext y
    exact fderiv_sub_const _
  refine ⟨fun y => posteriorMoment μ hη y, ?_, ?_⟩
  · intro y v
    change fderiv ℝ (fun y : E => -Real.log (C*Z y)) y v = _
    rw [hDU]
    obtain ⟨hR,hLp⟩ := posteriorMoment μ hη y
    haveI : IsProbabilityMeasure (R y) := hR
    have hi : Integrable (fun x : E => x) (R y) := hLp.integrable (by norm_num)
    have hm : (∫ x, inner ℝ (y-x) v ∂(R y)) = inner ℝ (y-∫ x, x ∂(R y)) v := by
      have he : (fun x : E => inner ℝ (y-x) v) = fun x => inner ℝ v (y-x) := by
        funext x
        exact real_inner_comm _ _
      rw [he]
      have hmean : (∫ x, inner ℝ v (y-x) ∂(R y)) =
          inner ℝ v (∫ x, y-x ∂(R y)) := by
        simpa only [Pi.sub_apply] using
          (integral_inner (𝕜 := ℝ) ((integrable_const y).sub hi) v)
      have hdiff : (∫ x, y-x ∂(R y)) = y-∫ x, x ∂(R y) := by
        simpa only [Pi.sub_apply, integral_const, probReal_univ, one_smul] using
          integral_sub (integrable_const y) hi
      rw [hmean,hdiff]
      exact real_inner_comm _ _
    calc
      _ = -(D y v/Z y) := by simpa only [neg_div] using rawFirst μ hη y v
      _ = (∫ x, inner ℝ (y-x) v ∂(R y))/η := by
        rw [normalizedFirst μ hη y v]; ring
      _ = _ := by rw [hm]
  · intro y v w
    change fderiv ℝ (fderiv ℝ (fun y : E => -Real.log (C*Z y))) y v w = _
    rw [hDU]
    obtain ⟨hR,hLp⟩ := posteriorMoment μ hη y
    haveI : IsProbabilityMeasure (R y) := hR
    have hi : Integrable (fun x : E => x) (R y) := hLp.integrable (by norm_num)
    have hξ : MemLp (fun x : E => y-x) 2 (R y) := (memLp_const y).sub hLp
    have hv := hξ.inner_const (𝕜 := ℝ) v
    have hw := hξ.inner_const (𝕜 := ℝ) w
    have hc : covarianceBilin (R y) v w =
        (∫ x, inner ℝ (y-x) v*inner ℝ (y-x) w ∂(R y)) -
          (∫ x, inner ℝ (y-x) v ∂(R y))*(∫ x, inner ℝ (y-x) w ∂(R y)) := by
      have hcenter : covariance (fun x => inner ℝ (y-x) v)
          (fun x => inner ℝ (y-x) w) (R y) = covarianceBilin (R y) v w := by
        simp_rw [inner_sub_left]
        rw [covariance_const_sub_left (hi.inner_const (𝕜 := ℝ) v),
          covariance_const_sub_right (hi.inner_const (𝕜 := ℝ) w), neg_neg]
        rw [covarianceBilin_apply_eq_cov hLp]
        simp_rw [real_inner_comm v, real_inner_comm w]
        rfl
      exact hcenter.symm.trans (by simpa only [Pi.mul_apply] using covariance_eq_sub hv hw)
    rw [rawSecond μ hη y v w]
    change D y v*D y w/Z y^2 - H y v w/Z y = _
    rw [show D y v*D y w/Z y^2 = (D y v/Z y)*(D y w/Z y) by ring]
    rw [normalizedFirst μ hη y v, normalizedFirst μ hη y w,
      normalizedSecond μ hη y v w, hc]
    ring

end
end AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
