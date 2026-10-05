import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Tactic

/-!
# The first partial momentum refresh in Smoothed Picard HMC

Algorithm 3.1 of Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, starts each
phase by adjoining a fresh standard Gaussian and setting

`P₀ = exp (-h / 2) P_init + sqrt (1 - exp (-h)) Z`.

The product measure below is the actual independence semantics of that draw.
The theorem proves the exact combined second-moment identity, including the
Gaussian dimension term suppressed in the short proof of Lemma D.4.  Thus an
incoming budget `M` becomes `M + (1 - exp (-h)) d`; it is not silently reused
unchanged.

The repeated Algorithm 3.1 history, its run-wide moment estimate, the second
momentum refresh, the Picard Gaussian array, and the numerical conclusion
(D.7) remain separate.
-/

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped ENNReal RealInnerProductSpace

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PartialMomentumRefresh

open AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The actual independent Gaussian half-refresh has an exact second-moment
identity and supplies the corrected state budget needed by the first Picard
layer. -/
theorem partial_momentum_refresh_second_moment
    (ν : Measure (E × E)) [IsProbabilityMeasure ν]
    (xstar : E) {h M : ℝ} (hh : 0 ≤ h)
    (hstateI : Integrable (fun s : E × E => ‖s.1 - xstar‖ ^ 2 + ‖s.2‖ ^ 2) ν)
    (hstate : (∫ s : E × E, ‖s.1 - xstar‖ ^ 2 + ‖s.2‖ ^ 2 ∂ν) ≤ M) :
    let a := Real.exp (-h / 2)
    let sigma := Real.sqrt (1 - Real.exp (-h))
    let μ := ν.prod (stdGaussian E)
    let X : (E × E) × E → E := fun w => w.1.1
    let P0 : (E × E) × E → E := fun w => a • w.1.2 + sigma • w.2
    Measurable X ∧ Measurable P0 ∧
      Integrable (fun w => ‖X w - xstar‖ ^ 2 + ‖P0 w‖ ^ 2) μ ∧
      (∫ w, ‖X w - xstar‖ ^ 2 + ‖P0 w‖ ^ 2 ∂μ) =
        (∫ s : E × E, ‖s.1 - xstar‖ ^ 2 + Real.exp (-h) * ‖s.2‖ ^ 2 ∂ν) +
          (1 - Real.exp (-h)) * (Module.finrank ℝ E : ℝ) ∧
      (∫ w, ‖X w - xstar‖ ^ 2 + ‖P0 w‖ ^ 2 ∂μ) ≤
        M + (1 - Real.exp (-h)) * (Module.finrank ℝ E : ℝ) := by
  classical
  dsimp only
  have hexp : Real.exp (-h) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
  have hvar : 0 ≤ 1 - Real.exp (-h) := sub_nonneg.mpr hexp
  have ha2 : Real.exp (-h / 2) ^ 2 = Real.exp (-h) := by
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring
  have hs2 : Real.sqrt (1 - Real.exp (-h)) ^ 2 = 1 - Real.exp (-h) :=
    Real.sq_sqrt hvar
  have hposI : Integrable (fun s : E × E => ‖s.1 - xstar‖ ^ 2) ν := by
    apply hstateI.mono' (by fun_prop)
    filter_upwards with s
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    exact le_add_of_nonneg_right (sq_nonneg _)
  have hmomI : Integrable (fun s : E × E => ‖s.2‖ ^ 2) ν := by
    apply hstateI.mono' (by fun_prop)
    filter_upwards with s
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    exact le_add_of_nonneg_left (sq_nonneg _)
  have hmom1 : Integrable (fun s : E × E => s.2) ν :=
    MemLp.integrable (by norm_num : 1 ≤ (2 : ℝ≥0∞))
      ((memLp_two_iff_integrable_sq_norm (by fun_prop)).2 hmomI)
  obtain ⟨hgaussI, hgauss⟩ :=
    integrable_norm_sq_and_integral_stdGaussian (E := E)
  have hz1 : Integrable (fun z : E => z) (stdGaussian E) := IsGaussian.integrable_id
  have hcross : Integrable
      (fun w : (E × E) × E => inner ℝ w.1.2 w.2) (ν.prod (stdGaussian E)) :=
    hmom1.op_fst_snd (by fun_prop)
      ⟨1, by intro x y; simpa using norm_inner_le_norm (𝕜 := ℝ) x y⟩ hz1
  have hcross0 :
      (∫ w : (E × E) × E, inner ℝ w.1.2 w.2 ∂ν.prod (stdGaussian E)) = 0 := by
    rw [integral_prod _ hcross]
    have hz (s : E × E) :
        (∫ z : E, inner ℝ s.2 z ∂stdGaussian E) = 0 :=
      integral_strongDual_stdGaussian (innerSL ℝ s.2)
    simp only [hz, integral_zero]
  have hposP := hposI.comp_fst (stdGaussian E)
  have hmomP := hmomI.comp_fst (stdGaussian E)
  have hgaussP := hgaussI.comp_snd ν
  have hcrossC : Integrable (fun w : (E × E) × E =>
      (2 * Real.exp (-h / 2) * Real.sqrt (1 - Real.exp (-h))) *
        inner ℝ w.1.2 w.2) (ν.prod (stdGaussian E)) := hcross.const_mul _
  have hbase : Integrable (fun w : (E × E) × E =>
      ‖w.1.1 - xstar‖ ^ 2 + Real.exp (-h) * ‖w.1.2‖ ^ 2)
      (ν.prod (stdGaussian E)) := hposP.add (hmomP.const_mul _)
  have hbaseCross : Integrable (fun w : (E × E) × E =>
      ‖w.1.1 - xstar‖ ^ 2 + Real.exp (-h) * ‖w.1.2‖ ^ 2 +
        (2 * Real.exp (-h / 2) * Real.sqrt (1 - Real.exp (-h))) *
          inner ℝ w.1.2 w.2) (ν.prod (stdGaussian E)) := hbase.add hcrossC
  have hnoiseC : Integrable (fun w : (E × E) × E =>
      (1 - Real.exp (-h)) * ‖w.2‖ ^ 2) (ν.prod (stdGaussian E)) :=
    hgaussP.const_mul _
  have hpieces : Integrable (fun w : (E × E) × E =>
      ‖w.1.1 - xstar‖ ^ 2 + Real.exp (-h) * ‖w.1.2‖ ^ 2 +
        (2 * Real.exp (-h / 2) * Real.sqrt (1 - Real.exp (-h))) *
          inner ℝ w.1.2 w.2 +
        (1 - Real.exp (-h)) * ‖w.2‖ ^ 2) (ν.prod (stdGaussian E)) :=
    hbaseCross.add hnoiseC
  have hexpand (w : (E × E) × E) :
      ‖w.1.1 - xstar‖ ^ 2 +
          ‖Real.exp (-h / 2) • w.1.2 +
            Real.sqrt (1 - Real.exp (-h)) • w.2‖ ^ 2 =
        ‖w.1.1 - xstar‖ ^ 2 + Real.exp (-h) * ‖w.1.2‖ ^ 2 +
          (2 * Real.exp (-h / 2) * Real.sqrt (1 - Real.exp (-h))) *
            inner ℝ w.1.2 w.2 +
          (1 - Real.exp (-h)) * ‖w.2‖ ^ 2 := by
    rw [norm_add_sq_real, norm_smul, norm_smul, real_inner_smul_left,
      real_inner_smul_right]
    rw [Real.norm_eq_abs, Real.norm_eq_abs, abs_of_pos (Real.exp_pos _),
      abs_of_nonneg (Real.sqrt_nonneg _)]
    simp only [mul_pow, ha2, hs2]
    ring
  have houtI : Integrable (fun w : (E × E) × E =>
      ‖w.1.1 - xstar‖ ^ 2 +
        ‖Real.exp (-h / 2) • w.1.2 +
          Real.sqrt (1 - Real.exp (-h)) • w.2‖ ^ 2)
      (ν.prod (stdGaussian E)) := by
    simpa only [hexpand] using hpieces
  have heq :
      (∫ w : (E × E) × E,
          ‖w.1.1 - xstar‖ ^ 2 +
            ‖Real.exp (-h / 2) • w.1.2 +
              Real.sqrt (1 - Real.exp (-h)) • w.2‖ ^ 2
          ∂ν.prod (stdGaussian E)) =
        (∫ s : E × E,
          ‖s.1 - xstar‖ ^ 2 + Real.exp (-h) * ‖s.2‖ ^ 2 ∂ν) +
          (1 - Real.exp (-h)) * (Module.finrank ℝ E : ℝ) := by
    simp_rw [hexpand]
    rw [integral_add hbaseCross hnoiseC,
      integral_add hbase hcrossC,
      integral_const_mul, hcross0, mul_zero, add_zero,
      integral_const_mul, integral_prod _ hgaussP]
    simp only [hgauss, integral_const]
    rw [integral_prod _ hbase]
    simp only [integral_const]
    simp
  have hweighted :
      (∫ s : E × E,
          ‖s.1 - xstar‖ ^ 2 + Real.exp (-h) * ‖s.2‖ ^ 2 ∂ν) ≤ M := by
    calc
      _ ≤ ∫ s : E × E, ‖s.1 - xstar‖ ^ 2 + ‖s.2‖ ^ 2 ∂ν := by
        apply integral_mono (hposI.add (hmomI.const_mul _)) hstateI
        intro s
        change ‖s.1 - xstar‖ ^ 2 + Real.exp (-h) * ‖s.2‖ ^ 2 ≤
          ‖s.1 - xstar‖ ^ 2 + ‖s.2‖ ^ 2
        have hp : Real.exp (-h) * ‖s.2‖ ^ 2 ≤ ‖s.2‖ ^ 2 := by
          simpa only [one_mul] using
            mul_le_mul_of_nonneg_right hexp (sq_nonneg ‖s.2‖)
        exact add_le_add_right hp (‖s.1 - xstar‖ ^ 2)
      _ ≤ M := hstate
  refine ⟨by fun_prop, by fun_prop, houtI, heq, ?_⟩
  rw [heq]
  linarith

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PartialMomentumRefresh
