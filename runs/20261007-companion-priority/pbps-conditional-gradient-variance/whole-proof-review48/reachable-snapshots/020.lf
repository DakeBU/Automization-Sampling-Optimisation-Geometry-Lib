import AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity
import AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs
import Mathlib.Analysis.SpecialFunctions.ImproperIntegrals
import Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform

/-!
# Integrability leaves

Reusable integrability bridges for Chewi-style log-concave sampling.

The Gibbs target-measure API lives in `Measure.Gibbs`; this file supplies the
analytic tail estimates that make those normalization contracts usable on
Lebesgue space.  The first concrete tail is a finite-dimensional quadratic
lower-bound envelope, built from Mathlib's Gaussian Fourier/integral API.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Analysis
namespace Integrability

open scoped ENNReal NNReal RealInnerProductSpace

open MeasureTheory
open Complex hiding exp continuous_exp
open Set

variable {α : Type*} [MeasurableSpace α] {μ : Measure α}

/-- A nonnegative integrable real function has finite `ℝ≥0∞` lintegral after
`ENNReal.ofReal`. -/
theorem lintegral_ofReal_ne_top_of_integrable_nonneg {f : α → ℝ}
    (hf : Integrable f μ) (hf_nonneg : 0 ≤ᵐ[μ] f) :
    ∫⁻ x, ENNReal.ofReal (f x) ∂μ ≠ ∞ :=
  (lintegral_ofReal_ne_top_iff_integrable hf.aestronglyMeasurable hf_nonneg).2 hf

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- Finite-dimensional Gaussian quadratic tails are Lebesgue-integrable. -/
theorem integrable_exp_neg_mul_norm_sq {a : ℝ} (ha : 0 < a) :
    Integrable (fun x : E => Real.exp (-a * ‖x‖ ^ 2)) volume := by
  have hcx : Integrable
      (fun x : E =>
        cexp (-(a : ℂ) * (‖x‖ : ℂ) ^ 2 + 0 * (⟪(0 : E), x⟫ : ℂ))) volume := by
    simpa using GaussianFourier.integrable_cexp_neg_mul_sq_norm_add (V := E)
      (b := (a : ℂ)) (w := (0 : E)) (c := 0) (by simpa using ha)
  have hre : Integrable
      (fun x : E => (cexp (-(a : ℂ) * (‖x‖ : ℂ) ^ 2)).re) volume := by
    have hre' := hcx.re
    rw [RCLike.re_eq_complex_re] at hre'
    simpa only [zero_mul, add_zero] using hre'
  refine hre.congr ?_
  filter_upwards with x
  have harg :
      (-(a : ℂ) * (‖x‖ : ℂ) ^ 2) = ((-(a * ‖x‖ ^ 2) : ℝ) : ℂ) := by
    norm_num [Complex.ofReal_mul, Complex.ofReal_pow]
  rw [harg, Complex.exp_ofReal_re]
  ring_nf

/-- A shifted finite-dimensional Gaussian quadratic tail is
Lebesgue-integrable. -/
theorem integrable_exp_neg_add_mul_norm_sq {a b : ℝ} (ha : 0 < a) :
    Integrable (fun x : E => Real.exp (-(a * ‖x‖ ^ 2 + b))) volume := by
  have h := (integrable_exp_neg_mul_norm_sq (E := E) ha).const_mul (Real.exp (-b))
  refine h.congr ?_
  filter_upwards with x
  rw [show -(a * ‖x‖ ^ 2 + b) = -b + (-a * ‖x‖ ^ 2) by ring]
  rw [Real.exp_add]

/-- The `ℝ≥0∞` integral of a shifted finite-dimensional Gaussian quadratic
tail is finite. -/
theorem lintegral_exp_neg_add_mul_norm_sq_ne_top {a b : ℝ} (ha : 0 < a) :
    ∫⁻ x : E, ENNReal.ofReal (Real.exp (-(a * ‖x‖ ^ 2 + b))) ∂volume ≠ ∞ :=
  lintegral_ofReal_ne_top_of_integrable_nonneg
    (integrable_exp_neg_add_mul_norm_sq (E := E) (b := b) ha)
    (ae_of_all _ fun _ => Real.exp_nonneg _)

/-- A centered finite-dimensional Gaussian quadratic tail is
Lebesgue-integrable. -/
theorem integrable_exp_neg_add_mul_norm_sub_sq {a b : ℝ} (m : E) (ha : 0 < a) :
    Integrable (fun x : E => Real.exp (-(a * ‖x - m‖ ^ 2 + b))) volume := by
  simpa only using
    (integrable_exp_neg_add_mul_norm_sq (E := E) (a := a) (b := b) ha).comp_sub_right m

/-- The `ℝ≥0∞` integral of a centered finite-dimensional Gaussian quadratic
tail is finite. -/
theorem lintegral_exp_neg_add_mul_norm_sub_sq_ne_top {a b : ℝ} (m : E) (ha : 0 < a) :
    ∫⁻ x : E, ENNReal.ofReal (Real.exp (-(a * ‖x - m‖ ^ 2 + b))) ∂volume ≠ ∞ :=
  lintegral_ofReal_ne_top_of_integrable_nonneg
    (integrable_exp_neg_add_mul_norm_sub_sq (E := E) (a := a) (b := b) m ha)
    (ae_of_all _ fun _ => Real.exp_nonneg _)

section RealLine

/-- One-dimensional Laplace tails are Lebesgue-integrable. -/
theorem integrable_exp_neg_add_mul_abs {a b : ℝ} (ha : 0 < a) :
    Integrable (fun x : ℝ => Real.exp (-(a * |x| + b))) volume := by
  have hright0 : IntegrableOn (fun x : ℝ => Real.exp ((-a) * x)) (Ioi 0) := by
    exact integrableOn_exp_mul_Ioi (a := -a) (by linarith) 0
  have hright_base :
      IntegrableOn (fun x : ℝ => Real.exp (-b) * Real.exp ((-a) * x)) (Ioi 0) :=
    hright0.const_mul (Real.exp (-b))
  have hright : IntegrableOn (fun x : ℝ => Real.exp (-(a * |x| + b))) (Ioi 0) := by
    refine (integrableOn_congr_fun ?_ measurableSet_Ioi).mp hright_base
    intro x hx
    have hxnonneg : 0 ≤ x := le_of_lt hx
    change Real.exp (-b) * Real.exp (-a * x) = Real.exp (-(a * |x| + b))
    rw [abs_of_nonneg hxnonneg]
    rw [show -(a * x + b) = -b + (-a) * x by ring]
    rw [Real.exp_add]
  have hleft0 : IntegrableOn (fun x : ℝ => Real.exp (a * x)) (Iic 0) := by
    exact integrableOn_exp_mul_Iic (a := a) ha 0
  have hleft_base :
      IntegrableOn (fun x : ℝ => Real.exp (-b) * Real.exp (a * x)) (Iic 0) :=
    hleft0.const_mul (Real.exp (-b))
  have hleft : IntegrableOn (fun x : ℝ => Real.exp (-(a * |x| + b))) (Iic 0) := by
    refine (integrableOn_congr_fun ?_ measurableSet_Iic).mp hleft_base
    intro x hx
    have hxnonpos : x ≤ 0 := hx
    change Real.exp (-b) * Real.exp (a * x) = Real.exp (-(a * |x| + b))
    rw [abs_of_nonpos hxnonpos]
    rw [show -(a * -x + b) = -b + a * x by ring]
    rw [Real.exp_add]
  rw [← integrableOn_univ]
  rw [← Iic_union_Ioi (a := (0 : ℝ)), integrableOn_union]
  exact ⟨hleft, hright⟩

/-- The `ℝ≥0∞` integral of a one-dimensional Laplace tail is finite. -/
theorem lintegral_exp_neg_add_mul_abs_ne_top {a b : ℝ} (ha : 0 < a) :
    ∫⁻ x : ℝ, ENNReal.ofReal (Real.exp (-(a * |x| + b))) ∂volume ≠ ∞ :=
  lintegral_ofReal_ne_top_of_integrable_nonneg
    (integrable_exp_neg_add_mul_abs (a := a) (b := b) ha)
    (ae_of_all _ fun _ => Real.exp_nonneg _)

/-- Exact normalizer for one-dimensional absolute-linear Laplace tails. -/
theorem integral_exp_neg_add_mul_abs_eq {a b : ℝ} (ha : 0 < a) :
    ∫ x : ℝ, Real.exp (-(a * |x| + b)) ∂volume =
      2 * Real.exp (-b) / a := by
  let f : ℝ → ℝ := fun x => Real.exp (-(a * |x| + b))
  have hf : Integrable f volume :=
    integrable_exp_neg_add_mul_abs (a := a) (b := b) ha
  have hsplit :
      (∫ x, f x ∂volume) =
        ∫ x in Iic (0 : ℝ), f x ∂volume +
          ∫ x in Ioi (0 : ℝ), f x ∂volume := by
    rw [← setIntegral_univ, ← Iic_union_Ioi (a := (0 : ℝ))]
    exact setIntegral_union (Iic_disjoint_Ioi le_rfl) measurableSet_Ioi
      hf.integrableOn hf.integrableOn
  have hleft :
      ∫ x in Iic (0 : ℝ), f x ∂volume = Real.exp (-b) / a := by
    have hbase :
        ∫ x in Iic (0 : ℝ), Real.exp (-b) * Real.exp (a * x) ∂volume =
          Real.exp (-b) / a := by
      rw [integral_const_mul]
      rw [integral_exp_mul_Iic (a := a) ha (c := 0)]
      simp
      ring
    rw [← hbase]
    apply setIntegral_congr_fun measurableSet_Iic
    intro x hx
    have hxnonpos : x ≤ 0 := hx
    calc
      f x = Real.exp (-b + a * x) := by
        simp [f, abs_of_nonpos hxnonpos]
      _ = Real.exp (-b) * Real.exp (a * x) := by
        rw [Real.exp_add]
  have hright :
      ∫ x in Ioi (0 : ℝ), f x ∂volume = Real.exp (-b) / a := by
    have hbase :
        ∫ x in Ioi (0 : ℝ), Real.exp (-b) * Real.exp ((-a) * x) ∂volume =
          Real.exp (-b) / a := by
      rw [integral_const_mul]
      rw [integral_exp_mul_Ioi (a := -a) (by linarith) (c := 0)]
      simp
      ring
    rw [← hbase]
    apply setIntegral_congr_fun measurableSet_Ioi
    intro x hx
    have hxnonneg : 0 ≤ x := le_of_lt hx
    calc
      f x = Real.exp (-b + (-a) * x) := by
        simp [f, abs_of_nonneg hxnonneg]
      _ = Real.exp (-b) * Real.exp ((-a) * x) := by
        rw [Real.exp_add]
  rw [show (∫ x : ℝ, Real.exp (-(a * |x| + b)) ∂volume) =
      ∫ x : ℝ, f x ∂volume by rfl]
  rw [hsplit, hleft, hright]
  field_simp [ha.ne']
  ring

/-- Exact `ℝ≥0∞` normalizer for one-dimensional absolute-linear Laplace
tails. -/
theorem lintegral_exp_neg_add_mul_abs_eq {a b : ℝ} (ha : 0 < a) :
    ∫⁻ x : ℝ, ENNReal.ofReal (Real.exp (-(a * |x| + b))) ∂volume =
      ENNReal.ofReal (2 * Real.exp (-b) / a) := by
  rw [← ofReal_integral_eq_lintegral_ofReal
    (integrable_exp_neg_add_mul_abs (a := a) (b := b) ha)
    (ae_of_all _ fun _ => Real.exp_nonneg _)]
  rw [integral_exp_neg_add_mul_abs_eq (a := a) (b := b) ha]

end RealLine

/-- Exact `ℝ≥0∞` normalizer for the finite-dimensional quadratic Gaussian
tail. -/
theorem lintegral_exp_neg_mul_norm_sq_eq {a : ℝ} (ha : 0 < a) :
    ∫⁻ x : E, ENNReal.ofReal (Real.exp (-a * ‖x‖ ^ 2)) ∂volume =
      ENNReal.ofReal ((Real.pi / a) ^ ((Module.finrank ℝ E : ℝ) / 2)) := by
  rw [← ofReal_integral_eq_lintegral_ofReal
    (integrable_exp_neg_mul_norm_sq (E := E) ha)
    (ae_of_all _ fun _ => Real.exp_nonneg _)]
  rw [GaussianFourier.integral_rexp_neg_mul_sq_norm (V := E) ha]

/-- Exact `ℝ≥0∞` normalizer for a shifted finite-dimensional quadratic
Gaussian tail. -/
theorem lintegral_exp_neg_add_mul_norm_sq_eq {a b : ℝ} (ha : 0 < a) :
    ∫⁻ x : E, ENNReal.ofReal (Real.exp (-(a * ‖x‖ ^ 2 + b))) ∂volume =
      ENNReal.ofReal (Real.exp (-b) * (Real.pi / a) ^
        ((Module.finrank ℝ E : ℝ) / 2)) := by
  rw [← ofReal_integral_eq_lintegral_ofReal
    (integrable_exp_neg_add_mul_norm_sq (E := E) (b := b) ha)
    (ae_of_all _ fun _ => Real.exp_nonneg _)]
  have hInt :
      ∫ x : E, Real.exp (-(a * ‖x‖ ^ 2 + b)) ∂volume =
        Real.exp (-b) * ∫ x : E, Real.exp (-a * ‖x‖ ^ 2) ∂volume := by
    rw [← integral_const_mul]
    congr with x
    rw [show -(a * ‖x‖ ^ 2 + b) = -b + (-a * ‖x‖ ^ 2) by ring]
    rw [Real.exp_add]
  rw [hInt, GaussianFourier.integral_rexp_neg_mul_sq_norm (V := E) ha]

/-- Exact `ℝ≥0∞` normalizer for a centered finite-dimensional quadratic
Gaussian tail. -/
theorem lintegral_exp_neg_add_mul_norm_sub_sq_eq {a b : ℝ} (m : E) (ha : 0 < a) :
    ∫⁻ x : E, ENNReal.ofReal (Real.exp (-(a * ‖x - m‖ ^ 2 + b))) ∂volume =
      ENNReal.ofReal (Real.exp (-b) * (Real.pi / a) ^
        ((Module.finrank ℝ E : ℝ) / 2)) := by
  calc
    ∫⁻ x : E, ENNReal.ofReal (Real.exp (-(a * ‖x - m‖ ^ 2 + b))) ∂volume
        = ∫⁻ x : E, ENNReal.ofReal (Real.exp (-(a * ‖x‖ ^ 2 + b))) ∂volume := by
          simpa only using
            (lintegral_sub_right_eq_self
              (μ := (volume : Measure E))
              (f := fun x : E => ENNReal.ofReal (Real.exp (-(a * ‖x‖ ^ 2 + b))))
              m)
    _ = ENNReal.ofReal (Real.exp (-b) * (Real.pi / a) ^
        ((Module.finrank ℝ E : ℝ) / 2)) :=
          lintegral_exp_neg_add_mul_norm_sq_eq (E := E) (a := a) (b := b) ha

/-- The explicitly normalized finite-dimensional quadratic Gibbs density is a
probability measure on Lebesgue space. -/
theorem isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sq
    {a b : ℝ} (ha : 0 < a) :
    IsProbabilityMeasure
      ((volume : Measure E).withDensity fun x =>
        (ENNReal.ofReal
          (Real.exp (-b) * (Real.pi / a) ^
            ((Module.finrank ℝ E : ℝ) / 2)))⁻¹ *
          ENNReal.ofReal (Real.exp (-(a * ‖x‖ ^ 2 + b)))) := by
  let f : E → ℝ≥0∞ := fun x => ENNReal.ofReal (Real.exp (-(a * ‖x‖ ^ 2 + b)))
  let Z : ℝ≥0∞ := ENNReal.ofReal
    (Real.exp (-b) * (Real.pi / a) ^ ((Module.finrank ℝ E : ℝ) / 2))
  have hZeq : (∫⁻ x, f x ∂(volume : Measure E)) = Z := by
    simpa [f, Z] using
      lintegral_exp_neg_add_mul_norm_sq_eq (E := E) (a := a) (b := b) ha
  have hZpos : 0 < Z := by
    dsimp [Z]
    rw [ENNReal.ofReal_pos]
    exact mul_pos (Real.exp_pos _) (Real.rpow_pos_of_pos (div_pos Real.pi_pos ha) _)
  have h0 : ∫⁻ x, f x ∂(volume : Measure E) ≠ 0 := by
    rw [hZeq]
    exact ne_of_gt hZpos
  have hfin : ∫⁻ x, f x ∂(volume : Measure E) ≠ ∞ := by
    rw [hZeq]
    exact ENNReal.ofReal_ne_top
  have h0G :
      ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal
        (fun x : E => a * ‖x‖ ^ 2 + b) x ∂(volume : Measure E) ≠ 0 := by
    simpa [f, Measure.Gibbs.gibbsDensityENNReal] using h0
  have hfinG :
      ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal
        (fun x : E => a * ‖x‖ ^ 2 + b) x ∂(volume : Measure E) ≠ ∞ := by
    simpa [f, Measure.Gibbs.gibbsDensityENNReal] using hfin
  have hprobG :=
    Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs
      (volume : Measure E) (fun x : E => a * ‖x‖ ^ 2 + b) h0G hfinG
  have hprob :
      IsProbabilityMeasure
        ((volume : Measure E).withDensity fun x =>
          (∫⁻ y, f y ∂(volume : Measure E))⁻¹ * f x) := by
    simpa [f, Measure.Gibbs.gibbsDensityENNReal] using hprobG
  change IsProbabilityMeasure ((volume : Measure E).withDensity fun x => Z⁻¹ * f x)
  rw [← hZeq]
  exact hprob

/-- The explicitly normalized centered finite-dimensional quadratic Gibbs
density is a probability measure on Lebesgue space. -/
theorem isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sub_sq
    {a b : ℝ} (m : E) (ha : 0 < a) :
    IsProbabilityMeasure
      ((volume : Measure E).withDensity fun x =>
        (ENNReal.ofReal
          (Real.exp (-b) * (Real.pi / a) ^
            ((Module.finrank ℝ E : ℝ) / 2)))⁻¹ *
          ENNReal.ofReal (Real.exp (-(a * ‖x - m‖ ^ 2 + b)))) := by
  let f : E → ℝ≥0∞ := fun x => ENNReal.ofReal (Real.exp (-(a * ‖x - m‖ ^ 2 + b)))
  let Z : ℝ≥0∞ := ENNReal.ofReal
    (Real.exp (-b) * (Real.pi / a) ^ ((Module.finrank ℝ E : ℝ) / 2))
  have hZeq : (∫⁻ x, f x ∂(volume : Measure E)) = Z := by
    simpa [f, Z] using
      lintegral_exp_neg_add_mul_norm_sub_sq_eq (E := E) (a := a) (b := b) m ha
  have hZpos : 0 < Z := by
    dsimp [Z]
    rw [ENNReal.ofReal_pos]
    exact mul_pos (Real.exp_pos _) (Real.rpow_pos_of_pos (div_pos Real.pi_pos ha) _)
  have h0 : ∫⁻ x, f x ∂(volume : Measure E) ≠ 0 := by
    rw [hZeq]
    exact ne_of_gt hZpos
  have hfin : ∫⁻ x, f x ∂(volume : Measure E) ≠ ∞ := by
    rw [hZeq]
    exact ENNReal.ofReal_ne_top
  have h0G :
      ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal
        (fun x : E => a * ‖x - m‖ ^ 2 + b) x ∂(volume : Measure E) ≠ 0 := by
    simpa [f, Measure.Gibbs.gibbsDensityENNReal] using h0
  have hfinG :
      ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal
        (fun x : E => a * ‖x - m‖ ^ 2 + b) x ∂(volume : Measure E) ≠ ∞ := by
    simpa [f, Measure.Gibbs.gibbsDensityENNReal] using hfin
  have hprobG :=
    Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs
      (volume : Measure E) (fun x : E => a * ‖x - m‖ ^ 2 + b) h0G hfinG
  have hprob :
      IsProbabilityMeasure
        ((volume : Measure E).withDensity fun x =>
          (∫⁻ y, f y ∂(volume : Measure E))⁻¹ * f x) := by
    simpa [f, Measure.Gibbs.gibbsDensityENNReal] using hprobG
  change IsProbabilityMeasure ((volume : Measure E).withDensity fun x => Z⁻¹ * f x)
  rw [← hZeq]
  exact hprob

/-- The explicitly normalized one-dimensional absolute-linear Laplace Gibbs
density is a probability measure on Lebesgue space. -/
theorem isProbabilityMeasure_withDensity_exp_neg_add_mul_abs
    {a b : ℝ} (ha : 0 < a) :
    IsProbabilityMeasure
      ((volume : Measure ℝ).withDensity fun x =>
        (ENNReal.ofReal (2 * Real.exp (-b) / a))⁻¹ *
          ENNReal.ofReal (Real.exp (-(a * |x| + b)))) := by
  let f : ℝ → ℝ≥0∞ := fun x =>
    ENNReal.ofReal (Real.exp (-(a * |x| + b)))
  let Z : ℝ≥0∞ := ENNReal.ofReal (2 * Real.exp (-b) / a)
  have hZeq : (∫⁻ x, f x ∂(volume : Measure ℝ)) = Z := by
    simpa [f, Z] using
      lintegral_exp_neg_add_mul_abs_eq (a := a) (b := b) ha
  have hZpos : 0 < Z := by
    dsimp [Z]
    rw [ENNReal.ofReal_pos]
    positivity
  have h0 : ∫⁻ x, f x ∂(volume : Measure ℝ) ≠ 0 := by
    rw [hZeq]
    exact ne_of_gt hZpos
  have hfin : ∫⁻ x, f x ∂(volume : Measure ℝ) ≠ ∞ := by
    rw [hZeq]
    exact ENNReal.ofReal_ne_top
  have h0G :
      ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal
        (fun x : ℝ => a * |x| + b) x ∂(volume : Measure ℝ) ≠ 0 := by
    simpa [f, Measure.Gibbs.gibbsDensityENNReal] using h0
  have hfinG :
      ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal
        (fun x : ℝ => a * |x| + b) x ∂(volume : Measure ℝ) ≠ ∞ := by
    simpa [f, Measure.Gibbs.gibbsDensityENNReal] using hfin
  have hprobG :=
    Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs
      (volume : Measure ℝ) (fun x : ℝ => a * |x| + b) h0G hfinG
  have hprob :
      IsProbabilityMeasure
        ((volume : Measure ℝ).withDensity fun x =>
          (∫⁻ y, f y ∂(volume : Measure ℝ))⁻¹ * f x) := by
    simpa [f, Measure.Gibbs.gibbsDensityENNReal] using hprobG
  change IsProbabilityMeasure ((volume : Measure ℝ).withDensity fun x => Z⁻¹ * f x)
  rw [← hZeq]
  exact hprob

/-- A quadratic lower bound on a potential gives a finite Gibbs normalization
constant on finite-dimensional Lebesgue space. -/
theorem lintegral_gibbsDensityENNReal_ne_top_of_ae_quadratic_lower_bound
    {V : E → ℝ} {a b : ℝ} (ha : 0 < a)
    (hquad : ∀ᵐ x ∂(volume : Measure E), a * ‖x‖ ^ 2 + b ≤ V x) :
    ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal V x ∂(volume : Measure E) ≠ ∞ := by
  refine Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge
    (volume : Measure E) hquad ?_
  simpa [Measure.Gibbs.gibbsDensityENNReal] using
    lintegral_exp_neg_add_mul_norm_sq_ne_top (E := E) (a := a) (b := b) ha

/-- A centered quadratic lower bound on a potential gives a finite Gibbs
normalization constant on finite-dimensional Lebesgue space. -/
theorem lintegral_gibbsDensityENNReal_ne_top_of_ae_centered_quadratic_lower_bound
    {V : E → ℝ} {a b : ℝ} (m : E) (ha : 0 < a)
    (hquad : ∀ᵐ x ∂(volume : Measure E), a * ‖x - m‖ ^ 2 + b ≤ V x) :
    ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal V x ∂(volume : Measure E) ≠ ∞ := by
  refine Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge
    (volume : Measure E) hquad ?_
  simpa [Measure.Gibbs.gibbsDensityENNReal] using
    lintegral_exp_neg_add_mul_norm_sub_sq_ne_top (E := E) (a := a) (b := b) m ha

/-- A one-dimensional absolute-linear lower bound on a potential gives a finite
Gibbs normalization constant on Lebesgue space. -/
theorem lintegral_gibbsDensityENNReal_ne_top_of_ae_abs_linear_lower_bound
    {V : ℝ → ℝ} {a b : ℝ} (ha : 0 < a)
    (hlin : ∀ᵐ x ∂(volume : Measure ℝ), a * |x| + b ≤ V x) :
    ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal V x ∂(volume : Measure ℝ) ≠ ∞ := by
  refine Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge
    (volume : Measure ℝ) hlin ?_
  simpa [Measure.Gibbs.gibbsDensityENNReal] using
    lintegral_exp_neg_add_mul_abs_ne_top (a := a) (b := b) ha

/-- A strongly convex potential with an exposed global minimizer has a finite
Gibbs normalization constant on finite-dimensional Lebesgue space. -/
theorem lintegral_gibbsDensityENNReal_ne_top_of_strongConvexOn_minimizer
    {V : E → ℝ} {k : ℝ} (hk : 0 < k) (x₀ : E)
    (hstrong : StrongConvexOn (Set.univ : Set E) k V)
    (hx₀ : IsMinOn V (Set.univ : Set E) x₀) :
    ∫⁻ x, Measure.Gibbs.gibbsDensityENNReal V x ∂(volume : Measure E) ≠ ∞ := by
  have ha : 0 < k / 4 := by positivity
  have hquad : ∀ᵐ x ∂(volume : Measure E), (k / 4) * ‖x - x₀‖ ^ 2 + V x₀ ≤ V x := by
    filter_upwards with x
    have hbound :=
      AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity.centered_quadratic_lower_bound_of_strongConvexOn_minimizer
        hstrong x₀ hx₀ x
    simpa [add_comm] using hbound
  exact lintegral_gibbsDensityENNReal_ne_top_of_ae_centered_quadratic_lower_bound
    (E := E) (V := V) (a := k / 4) (b := V x₀) x₀ ha hquad

/-- A measurable potential with a quadratic lower bound defines a normalized
Gibbs probability measure on finite-dimensional Lebesgue space. -/
theorem isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_quadratic_lower_bound
    {V : E → ℝ} {a b : ℝ} (hV : AEMeasurable V (volume : Measure E))
    (ha : 0 < a)
    (hquad : ∀ᵐ x ∂(volume : Measure E), a * ‖x‖ ^ 2 + b ≤ V x) :
    IsProbabilityMeasure
      ((volume : Measure E).withDensity fun x =>
        (∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂(volume : Measure E))⁻¹ *
          Measure.Gibbs.gibbsDensityENNReal V x) :=
  Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs
    (volume : Measure E) V
    (Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_zero (volume : Measure E) hV)
    (lintegral_gibbsDensityENNReal_ne_top_of_ae_quadratic_lower_bound
      (E := E) ha hquad)

/-- A measurable potential with a centered quadratic lower bound defines a
normalized Gibbs probability measure on finite-dimensional Lebesgue space. -/
theorem isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_centered_quadratic_lower_bound
    {V : E → ℝ} {a b : ℝ} (m : E) (hV : AEMeasurable V (volume : Measure E))
    (ha : 0 < a)
    (hquad : ∀ᵐ x ∂(volume : Measure E), a * ‖x - m‖ ^ 2 + b ≤ V x) :
    IsProbabilityMeasure
      ((volume : Measure E).withDensity fun x =>
        (∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂(volume : Measure E))⁻¹ *
          Measure.Gibbs.gibbsDensityENNReal V x) :=
  Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs
    (volume : Measure E) V
    (Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_zero (volume : Measure E) hV)
    (lintegral_gibbsDensityENNReal_ne_top_of_ae_centered_quadratic_lower_bound
      (E := E) m ha hquad)

/-- A measurable one-dimensional potential with an absolute-linear lower bound
defines a normalized Gibbs probability measure on Lebesgue space. -/
theorem isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_abs_linear_lower_bound
    {V : ℝ → ℝ} {a b : ℝ} (hV : AEMeasurable V (volume : Measure ℝ))
    (ha : 0 < a)
    (hlin : ∀ᵐ x ∂(volume : Measure ℝ), a * |x| + b ≤ V x) :
    IsProbabilityMeasure
      ((volume : Measure ℝ).withDensity fun x =>
        (∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂(volume : Measure ℝ))⁻¹ *
          Measure.Gibbs.gibbsDensityENNReal V x) :=
  Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs
    (volume : Measure ℝ) V
    (Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_zero (volume : Measure ℝ) hV)
    (lintegral_gibbsDensityENNReal_ne_top_of_ae_abs_linear_lower_bound
      (V := V) ha hlin)

/-- A measurable strongly convex potential with an exposed global minimizer
defines a normalized Gibbs probability measure on finite-dimensional Lebesgue
space. -/
theorem isProbabilityMeasure_withDensity_normalized_gibbs_of_strongConvexOn_minimizer
    {V : E → ℝ} {k : ℝ} (hV : AEMeasurable V (volume : Measure E))
    (hk : 0 < k) (x₀ : E)
    (hstrong : StrongConvexOn (Set.univ : Set E) k V)
    (hx₀ : IsMinOn V (Set.univ : Set E) x₀) :
    IsProbabilityMeasure
      ((volume : Measure E).withDensity fun x =>
        (∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂(volume : Measure E))⁻¹ *
          Measure.Gibbs.gibbsDensityENNReal V x) :=
  Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs
    (volume : Measure E) V
    (Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_zero (volume : Measure E) hV)
    (lintegral_gibbsDensityENNReal_ne_top_of_strongConvexOn_minimizer
      (E := E) hk x₀ hstrong hx₀)

end Integrability
end Analysis
end TechnicalLemmas
end AutoSamplingTheory
