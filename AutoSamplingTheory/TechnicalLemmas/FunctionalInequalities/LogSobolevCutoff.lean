/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Samplinglib contributors
-/
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Analysis.SpecialFunctions.Log.NegMulLog
import Mathlib.Topology.Order.OrderClosed

/-!
# Radial cutoff limits and the smooth log-Sobolev test domain

The measure-generic C2 cutoff proof is canonically extracted from
`GaussianLogSobolev`, preserving its complete-Hilbert scope. The new domain
extension applies a compact-C-infinity function LSI to actual compact smooth
approximants, then passes mass, entropy and genuine gradient energy to the limit.

This expands an omitted analytic step in Chewi, *Log-Concave Sampling*
(August20 2026), Section2.1.1, printed48-49/PDF60-61. It is not canonical
probability KL/Fisher, Poincare, a form-domain theorem or full Exercise1.7.
-/

set_option autoImplicit false
noncomputable section
open MeasureTheory Filter
open scoped Topology RealInnerProductSpace ContDiff

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff
open Analysis.Calculus.Cutoff

private theorem entropy_dilation_bound {a q : ℝ}
    (ha : a ∈ Set.Icc (0 : ℝ) 1) (hq : 0 ≤ q) :
    |(a*q) * Real.log (a*q)| ≤ |q * Real.log q| + q := by
  have hmul : (a*q) * Real.log (a*q) =
      a * (q * Real.log q) + q * (a * Real.log a) := by
    have h := Real.negMulLog_mul a q
    simp only [Real.negMulLog_eq_neg] at h
    linarith
  have hab : |a * Real.log a| ≤ 1 := by
    apply abs_le.mpr
    constructor
    · have h := Real.self_sub_one_le_mul_log ha.1
      linarith [ha.1]
    · exact (Real.mul_log_nonpos ha.1 ha.2).trans zero_le_one
  rw [hmul]
  calc
    |a * (q * Real.log q) + q * (a * Real.log a)|
        ≤ |a| * |q * Real.log q| + |q| * |a * Real.log a| := by
          simpa only [abs_mul] using abs_add_le (a * (q * Real.log q)) (q * (a * Real.log a))
    _ ≤ 1 * |q * Real.log q| + q * 1 := by
      rw [abs_of_nonneg ha.1, abs_of_nonneg hq]
      exact add_le_add (mul_le_mul_of_nonneg_right ha.2 (abs_nonneg _))
        (mul_le_mul_of_nonneg_left hab hq)
    _ = |q * Real.log q| + q := by ring

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [MeasurableSpace E] [BorelSpace E]

omit [MeasurableSpace E] [BorelSpace E] in
private theorem gradient_mul (c f : E → ℝ) (x : E)
    (hc : DifferentiableAt ℝ c x) (hf : DifferentiableAt ℝ f x) :
    gradient (fun y => c y * f y) x =
      c x • gradient f x + f x • gradient c x := by
  simp only [gradient, fderiv_fun_mul hc hf, map_add, map_smul]

omit [MeasurableSpace E] [BorelSpace E] in
private theorem cutoff_energy_bound (f : E → ℝ) (hf : ContDiff ℝ 2 f)
    {R C : ℝ} (hR : 1 ≤ R) (hC : 0 ≤ C)
    (hb : ∀ x : E, ‖fderiv ℝ (radialSmoothCutoff R : E → ℝ) x‖ ≤ C / R)
    (x : E) :
    ‖gradient (fun y => radialSmoothCutoff R y * f y) x‖^2 ≤
      2 * ‖gradient f x‖^2 + 2 * C^2 * (f x)^2 := by
  have hRp : 0 < R := lt_of_lt_of_le zero_lt_one hR
  have hc := (radialSmoothCutoff_contDiff (E := E) hRp).differentiable
    (WithTop.coe_ne_zero.mpr WithTop.top_ne_zero)
  rw [gradient_mul _ _ x (hc x) (hf.differentiable (by norm_num) x)]
  have hcg : ‖gradient (radialSmoothCutoff R : E → ℝ) x‖ ≤ C := by
    change ‖(InnerProductSpace.toDual ℝ E).symm
      (fderiv ℝ (radialSmoothCutoff R : E → ℝ) x)‖ ≤ C
    rw [(InnerProductSpace.toDual ℝ E).symm.norm_map]
    exact (hb x).trans (div_le_self hC hR)
  have hcc := radialSmoothCutoff_mem_Icc R x
  have hn : ‖radialSmoothCutoff R x • gradient f x +
      f x • gradient (radialSmoothCutoff R : E → ℝ) x‖ ≤
        ‖gradient f x‖ + C * |f x| := by
    calc
      _ ≤ ‖radialSmoothCutoff R x • gradient f x‖ +
          ‖f x • gradient (radialSmoothCutoff R : E → ℝ) x‖ := norm_add_le _ _
      _ ≤ ‖gradient f x‖ + C * |f x| := by
        simp only [norm_smul, Real.norm_eq_abs, abs_of_nonneg hcc.1]
        have h1 := mul_le_mul_of_nonneg_right hcc.2 (norm_nonneg (gradient f x))
        have h2 := mul_le_mul_of_nonneg_left hcg (abs_nonneg (f x))
        nlinarith
  have hs := (sq_le_sq₀ (norm_nonneg _) (by positivity :
    0 ≤ ‖gradient f x‖ + C * |f x|)).mpr hn
  nlinarith [sq_nonneg (‖gradient f x‖ - C * |f x|), sq_abs (f x)]

omit [MeasurableSpace E] [BorelSpace E] in
private theorem cutoff_gradient_eventually_eq (f : E → ℝ) (x : E) :
    ∀ᶠ n : ℕ in atTop,
      gradient (fun y => radialSmoothCutoff ((n:ℝ)+1) y * f y) x = gradient f x := by
  have hR : Tendsto (fun n : ℕ => (n:ℝ)+1) atTop atTop :=
    tendsto_atTop_add_const_right atTop (1:ℝ) tendsto_natCast_atTop_atTop
  filter_upwards [hR.eventually (eventually_gt_atTop (‖x‖ + 1))] with n hn
  apply Filter.EventuallyEq.gradient_eq
  refine Metric.eventually_nhds_iff.mpr ⟨1, zero_lt_one, ?_⟩
  intro y hy
  have hb : ‖y‖ ≤ ‖x‖ + ‖y-x‖ := by
    calc
      ‖y‖ = ‖x + (y-x)‖ := by congr 1; abel
      _ ≤ ‖x‖ + ‖y-x‖ := norm_add_le _ _
  rw [dist_eq_norm] at hy
  have he : radialSmoothCutoff ((n:ℝ)+1) y = 1 :=
    radialSmoothCutoff_eq_one_of_norm_le (by positivity) (by linarith)
  simp only [he, one_mul]

/-- Actual radial cutoff limits of square mass, square-log-square and true-gradient
energy on the C2 analytic domain of an arbitrary measure. This is the canonical
extraction of the existing Gaussian implementation, not a new Gaussian fact. -/
theorem cutoff_integral_limits (μ : Measure E) (f : E → ℝ)
    (hf : ContDiff ℝ 2 f) (hf2 : MemLp f 2 μ)
    (hgrad2 : MemLp (gradient f) 2 μ)
    (hp : Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) μ) :
    let fn := fun n : ℕ => fun x : E => radialSmoothCutoff ((n:ℝ)+1) x * f x
    Tendsto (fun n => ∫ x, (fn n x)^2 ∂μ) atTop (𝓝 (∫ x, (f x)^2 ∂μ)) ∧
    Tendsto (fun n => ∫ x, (fn n x)^2 * Real.log ((fn n x)^2) ∂μ)
      atTop (𝓝 (∫ x, (f x)^2 * Real.log ((f x)^2) ∂μ)) ∧
    Tendsto (fun n => ∫ x, ‖gradient (fn n) x‖^2 ∂μ)
      atTop (𝓝 (∫ x, ‖gradient f x‖^2 ∂μ)) := by
  dsimp only
  let χ := fun n : ℕ => (radialSmoothCutoff ((n:ℝ)+1) : E → ℝ)
  let fn := fun n : ℕ => fun x : E => χ n x * f x
  have hfn (n : ℕ) : ContDiff ℝ 2 (fn n) :=
    ((radialSmoothCutoff_contDiff (E := E) (by positivity : (0:ℝ)<(n:ℝ)+1)).of_le
      (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))).mul hf
  have hχb (n : ℕ) (x : E) := radialSmoothCutoff_mem_Icc ((n:ℝ)+1) x
  have hft (x : E) : Tendsto (fun n => fn n x) atTop (𝓝 (f x)) := by
    have hR : Tendsto (fun n : ℕ => (n:ℝ)+1) atTop atTop :=
      tendsto_atTop_add_const_right atTop (1:ℝ) tendsto_natCast_atTop_atTop
    have h := ((radialSmoothCutoff_tendsto_one x).comp hR).mul_const (f x)
    simpa only [Function.comp_def, one_mul] using h
  have im : Integrable (fun x => (f x)^2) μ := hf2.integrable_sq
  have ie : Integrable (fun x => ‖gradient f x‖^2) μ :=
    (memLp_two_iff_integrable_sq_norm hgrad2.aestronglyMeasurable).mp hgrad2
  have hm : Tendsto (fun n => ∫ x, (fn n x)^2 ∂μ)
      atTop (𝓝 (∫ x, (f x)^2 ∂μ)) := by
    apply tendsto_integral_of_dominated_convergence (fun x => (f x)^2)
      (fun n => ((hfn n).continuous.pow 2).aestronglyMeasurable) im
    · intro n
      filter_upwards with x
      rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
      have hb := hχb n x
      have hs : (χ n x)^2 ≤ 1 := by dsimp [χ]; nlinarith [hb.1, hb.2]
      change (χ n x * f x)^2 ≤ (f x)^2
      nlinarith [mul_le_mul_of_nonneg_right hs (sq_nonneg (f x))]
    · exact Eventually.of_forall (fun x => (hft x).pow 2)
  have hphi : Tendsto (fun n => ∫ x, (fn n x)^2 * Real.log ((fn n x)^2) ∂μ)
      atTop (𝓝 (∫ x, (f x)^2 * Real.log ((f x)^2) ∂μ)) := by
    apply tendsto_integral_of_dominated_convergence
      (fun x => |(f x)^2 * Real.log ((f x)^2)| + (f x)^2)
      (fun n => (Real.Continuous.mul_log ((hfn n).continuous.pow 2)).aestronglyMeasurable)
      (hp.abs.add im)
    · intro n
      filter_upwards with x
      rw [Real.norm_eq_abs]
      have hb := hχb n x
      have ha : (χ n x)^2 ∈ Set.Icc (0:ℝ) 1 :=
        ⟨sq_nonneg _, by dsimp [χ]; nlinarith [hb.1, hb.2]⟩
      change |(χ n x * f x)^2 * Real.log ((χ n x * f x)^2)| ≤ _
      simpa only [mul_pow] using entropy_dilation_bound ha (sq_nonneg (f x))
    · exact Eventually.of_forall (fun x =>
        Real.continuous_mul_log.continuousAt.tendsto.comp ((hft x).pow 2))
  obtain ⟨C,hC,hCb⟩ := radialSmoothCutoff_fderiv_bound (E := E)
  have henergy : Tendsto (fun n => ∫ x, ‖gradient (fn n) x‖^2 ∂μ)
      atTop (𝓝 (∫ x, ‖gradient f x‖^2 ∂μ)) := by
    apply tendsto_integral_of_dominated_convergence
      (fun x => 2 * ‖gradient f x‖^2 + 2 * C^2 * (f x)^2)
      (fun n => ((Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one
        ((hfn n).of_le (by norm_num))).norm.pow 2).aestronglyMeasurable)
      ((ie.const_mul 2).add (im.const_mul (2*C^2)))
    · intro n
      filter_upwards with x
      rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
      exact cutoff_energy_bound f hf (by have h := Nat.cast_nonneg (α := ℝ) n; linarith) hC.le
        (hCb _ (by positivity)) x
    · apply Eventually.of_forall
      intro x
      apply tendsto_const_nhds.congr'
      filter_upwards [cutoff_gradient_eventually_eq f x] with n hn
      change ‖gradient f x‖^2 =
        ‖gradient (fun y => radialSmoothCutoff ((n:ℝ)+1) y * f y) x‖^2
      rw [hn]
  exact ⟨hm,hphi,henergy⟩

variable [FiniteDimensional ℝ E]

/-- A compact-C-infinity function log-Sobolev inequality extends to the genuine
smooth L2/gradient-L2/entropy-integrable domain. The homogeneous entropy is the
literal real integral formula, including zero mass. No sign of C, probability
normalization or chosen RN score is needed for this conditional extension.
A source consumer must produce these analytic inputs, not assume them anew. -/
theorem logSobolev_of_compact_test (μ : Measure E) (C : ℝ)
    (hcompact : ∀ (v : E → ℝ), ContDiff ℝ ∞ v → HasCompactSupport v →
      (∫ x, (v x)^2 * Real.log ((v x)^2) ∂μ) -
        (∫ x, (v x)^2 ∂μ) * Real.log (∫ x, (v x)^2 ∂μ) ≤
      2 * C * ∫ x, ‖gradient v x‖^2 ∂μ)
    (f : E → ℝ) (hf : ContDiff ℝ ∞ f) (hf2 : MemLp f 2 μ)
    (hgrad2 : MemLp (gradient f) 2 μ)
    (hentropy : Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) μ) :
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂μ) -
      (∫ x, (f x)^2 ∂μ) * Real.log (∫ x, (f x)^2 ∂μ) ≤
    2 * C * ∫ x, ‖gradient f x‖^2 ∂μ := by
  let fn := fun n : ℕ => fun x : E => radialSmoothCutoff ((n:ℝ)+1) x * f x
  have hfC2 : ContDiff ℝ 2 f :=
    hf.of_le (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))
  obtain ⟨hm, hp, he⟩ := cutoff_integral_limits μ f hfC2 hf2 hgrad2 hentropy
  have hle (n : ℕ) :
      (∫ x, (fn n x)^2 * Real.log ((fn n x)^2) ∂μ) -
        (∫ x, (fn n x)^2 ∂μ) * Real.log (∫ x, (fn n x)^2 ∂μ) ≤
      2 * C * ∫ x, ‖gradient (fn n) x‖^2 ∂μ := by
    apply hcompact (fn n)
    · exact (radialSmoothCutoff_contDiff (by positivity)).mul hf
    · exact (radialSmoothCutoff_hasCompactSupport (by positivity)).mul_right
  exact le_of_tendsto_of_tendsto
    (hp.sub (Real.continuous_mul_log.continuousAt.tendsto.comp hm))
    (he.const_mul (2*C)) (Eventually.of_forall hle)

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff
