import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PhaseStateMoment
import Mathlib.Tactic

/-!
# The twisted phase metric used by Smoothed Picard HMC

Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, display preceding Theorem 4.5,
use the block matrix

`M_kappa = [[1/(2*kappa)+1/2, 1/2], [1/2, 1]] tensor I`.

This file records its quadratic form and explicit comparison with the ordinary
position--momentum energy.  The constants are dimension-free.  No contraction,
kernel error, or paper estimate (D.3) is asserted here.
-/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PhaseMetric

open MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Measure
open scoped ENNReal

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The real quadratic form induced by the paper's `M_kappa` block matrix. -/
private def phaseQuadraticForm (kappa : ℝ) (z : E × E) : ℝ :=
  (1 / (2 * kappa) + 1 / 2) * ‖z.1‖ ^ 2 + inner ℝ z.1 z.2 + ‖z.2‖ ^ 2

/-- The `M_kappa` transport cost on two phase-space points. -/
def phaseCost (kappa : ℝ) : (E × E) × (E × E) → ℝ≥0∞ :=
  fun z => ENNReal.ofReal (phaseQuadraticForm kappa (z.1 - z.2))

/-- The squared paper-specific Wasserstein quantity, defined directly as its
Kantorovich value. -/
def phaseWassersteinSq [MeasurableSpace E] (kappa : ℝ)
    (mu nu : Measure (E × E)) : ℝ≥0∞ :=
  Transport.transportCost (phaseCost (E := E) kappa) mu nu

/-- For `kappa >= 1`, the twisted quadratic form controls the ordinary sum of
the squared position and momentum norms. -/
private theorem ordinary_energy_le_phaseQuadraticForm {kappa : ℝ} (hkappa : 1 ≤ kappa)
    (z : E × E) :
    ‖z.1‖ ^ 2 + ‖z.2‖ ^ 2 ≤ 6 * phaseQuadraticForm kappa z := by
  have hkappa0 : 0 < kappa := lt_of_lt_of_le zero_lt_one hkappa
  have hinner : -(‖z.1‖ * ‖z.2‖) ≤ inner ℝ z.1 z.2 :=
    (abs_le.mp (abs_real_inner_le_norm z.1 z.2)).1
  have hcoef0 : 0 ≤ 1 / (2 * kappa) := by positivity
  rw [phaseQuadraticForm]
  nlinarith [mul_nonneg hcoef0 (sq_nonneg ‖z.1‖),
    sq_nonneg (2 * ‖z.1‖ - 3 * ‖z.2‖)]

/-- The twisted quadratic form is bounded above by `3/2` times the ordinary
sum of squares, uniformly over `kappa >= 1`. -/
private theorem phaseQuadraticForm_le_ordinary_energy {kappa : ℝ} (hkappa : 1 ≤ kappa)
    (z : E × E) :
    phaseQuadraticForm kappa z ≤ (3 / 2 : ℝ) * (‖z.1‖ ^ 2 + ‖z.2‖ ^ 2) := by
  have hkappa0 : 0 < kappa := lt_of_lt_of_le zero_lt_one hkappa
  have hinv : 1 / kappa ≤ 1 := (div_le_one hkappa0).2 hkappa
  have hhalf : (1 / kappa) * (1 / 2 : ℝ) ≤ 1 / 2 := by
    simpa using mul_le_mul_of_nonneg_right hinv (by norm_num : (0 : ℝ) ≤ 1 / 2)
  have hcoef : 1 / (2 * kappa) + 1 / 2 ≤ (1 : ℝ) := by
    rw [one_div, mul_inv_rev, show (2 : ℝ)⁻¹ = 1 / 2 by norm_num]
    convert add_le_add_right hhalf (1 / 2) using 1 <;> norm_num <;> ring
  have hinner : inner ℝ z.1 z.2 ≤ ‖z.1‖ * ‖z.2‖ :=
    real_inner_le_norm z.1 z.2
  have hsquare : 2 * (‖z.1‖ * ‖z.2‖) ≤ ‖z.1‖ ^ 2 + ‖z.2‖ ^ 2 := by
    nlinarith [sq_nonneg (‖z.1‖ - ‖z.2‖)]
  rw [phaseQuadraticForm]
  nlinarith [mul_nonneg (sub_nonneg.mpr hcoef) (sq_nonneg ‖z.1‖),
    sq_nonneg ‖z.1‖, sq_nonneg ‖z.2‖]

/-- Positivity of the paper quadratic form is a consequence of the explicit
lower comparison, rather than an untracked matrix-positivity assertion. -/
private theorem phaseQuadraticForm_nonneg {kappa : ℝ} (hkappa : 1 ≤ kappa)
    (z : E × E) : 0 ≤ phaseQuadraticForm kappa z := by
  have hkappa0 : 0 < kappa := lt_of_lt_of_le zero_lt_one hkappa
  have h := ordinary_energy_le_phaseQuadraticForm hkappa z
  have henergy : 0 ≤ ‖z.1‖ ^ 2 + ‖z.2‖ ^ 2 := by positivity
  nlinarith

/-- Pointwise comparison between ordinary squared product distance and the
paper's twisted transport cost. -/
private theorem quadraticCost_le_phaseCost {kappa : ℝ} (hkappa : 1 ≤ kappa)
    (z : (E × E) × (E × E)) :
    WassersteinSpace.quadraticCost (E := E × E) z ≤
      ENNReal.ofReal 6 * phaseCost (E := E) kappa z := by
  let d : E × E := z.1 - z.2
  have hnorm : ‖d‖ ^ 2 ≤ ‖d.1‖ ^ 2 + ‖d.2‖ ^ 2 := by
    rw [Prod.norm_def]
    rcases le_total ‖d.1‖ ‖d.2‖ with h | h <;>
      simp [max_eq_right h, max_eq_left h]
  have hreal : ‖d‖ ^ 2 ≤ 6 * phaseQuadraticForm kappa d :=
    hnorm.trans (ordinary_energy_le_phaseQuadraticForm hkappa d)
  change ENNReal.ofReal (‖d‖ ^ 2) ≤
    ENNReal.ofReal 6 * ENNReal.ofReal (phaseQuadraticForm kappa d)
  rw [← ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 6)]
  exact ENNReal.ofReal_le_ofReal hreal

/-- A twisted quadratic transport bound controls the ordinary product
Wasserstein distance.  The infimum comparison uses near-optimal couplings and
does not assume that either transport problem has an optimizer. -/
theorem wassersteinDistance_sq_le_phaseWassersteinSq
    [MeasurableSpace E] [BorelSpace E] [SecondCountableTopology E]
    {kappa : ℝ} (hkappa : 1 ≤ kappa) (mu nu : Measure (E × E)) :
    WassersteinSpace.wassersteinDistance mu nu ^ 2 ≤
      ENNReal.ofReal 6 * phaseWassersteinSq kappa mu nu := by
  rw [WassersteinSpace.wassersteinDistance_sq]
  apply ENNReal.le_of_forall_pos_le_add
  intro epsilon hepsilon hfinite
  let A : ℝ≥0∞ := ENNReal.ofReal 6
  let C : ℝ≥0∞ := phaseWassersteinSq kappa mu nu
  have hA0 : A ≠ 0 := by
    simp [A]
  have hAtop : A ≠ ⊤ := ENNReal.ofReal_ne_top
  have hCtop : C < ⊤ := by
    rcases ENNReal.mul_lt_top_iff.mp hfinite with h | h | h
    · exact h.2
    · exact (hA0 h).elim
    · simpa [C, h]
  let delta : ℝ≥0∞ := (epsilon : ℝ≥0∞) / A
  have hdelta0 : delta ≠ 0 := by
    have hepsilon0 : (epsilon : ℝ≥0∞) ≠ 0 := by exact_mod_cast hepsilon.ne'
    exact (ENNReal.div_pos hepsilon0 hAtop).ne'
  have hstrict : C < C + delta :=
    ENNReal.lt_add_right hCtop.ne hdelta0
  obtain ⟨gamma, hgamma, hgammaCost⟩ :=
    Transport.exists_isCoupling_lintegral_lt_of_transportCost_lt
      (phaseCost (E := E) kappa) mu nu hstrict
  have hphaseMeas : Measurable (phaseCost (E := E) kappa) := by
    unfold phaseCost phaseQuadraticForm
    fun_prop
  calc
    Transport.transportCost (WassersteinSpace.quadraticCost (E := E × E)) mu nu ≤
        ∫⁻ z, WassersteinSpace.quadraticCost (E := E × E) z ∂gamma :=
      Transport.transportCost_le_lintegral_of_isCoupling _ mu nu gamma hgamma
    _ ≤ ∫⁻ z, A * phaseCost (E := E) kappa z ∂gamma := by
      apply lintegral_mono
      intro z
      exact quadraticCost_le_phaseCost hkappa z
    _ = A * ∫⁻ z, phaseCost (E := E) kappa z ∂gamma := by
      exact lintegral_const_mul _ hphaseMeas
    _ ≤ A * (C + delta) := by
      gcongr
    _ = A * C + (epsilon : ℝ≥0∞) := by
      rw [mul_add, show A * delta = (epsilon : ℝ≥0∞) by
        exact ENNReal.mul_div_cancel hA0 hAtop]
    _ = ENNReal.ofReal 6 * phaseWassersteinSq kappa mu nu +
        (epsilon : ℝ≥0∞) := rfl

/-- Source-specific adapter from the paper's twisted `M_kappa` Wasserstein
quantity to the ordinary phase-state second moment.  This is the metric step in
the proof of Lemma D.4; the run-wide estimate (D.3) remains an input. -/
theorem phase_state_second_moment_of_phaseWasserstein
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (nu reference : Measure (E × E)) (xstar : E) {kappa r Mx Mp : ℝ}
    (hkappa : 1 ≤ kappa)
    (hX : Integrable (fun z : E × E => ‖z.1 - xstar‖ ^ 2) reference)
    (hP : Integrable (fun z : E × E => ‖z.2‖ ^ 2) reference)
    (hXbound : (∫ z : E × E, ‖z.1 - xstar‖ ^ 2 ∂reference) ≤ Mx)
    (hPbound : (∫ z : E × E, ‖z.2‖ ^ 2 ∂reference) ≤ Mp)
    (hW : phaseWassersteinSq kappa nu reference ≤ ENNReal.ofReal (r ^ 2)) :
    Integrable (fun z : E × E => ‖z.1 - xstar‖ ^ 2 + ‖z.2‖ ^ 2) nu ∧
      (∫ z : E × E, ‖z.1 - xstar‖ ^ 2 + ‖z.2‖ ^ 2 ∂nu) ≤
        2 * (Mx + Mp) + 24 * r ^ 2 := by
  have hsqrt : Real.sqrt 6 ^ 2 = 6 := Real.sq_sqrt (by norm_num)
  have hordinary : WassersteinSpace.wassersteinDistance nu reference ^ 2 ≤
      ENNReal.ofReal ((Real.sqrt 6 * r) ^ 2) := by
    refine (wassersteinDistance_sq_le_phaseWassersteinSq hkappa nu reference).trans ?_
    calc
      ENNReal.ofReal 6 * phaseWassersteinSq kappa nu reference ≤
          ENNReal.ofReal 6 * ENNReal.ofReal (r ^ 2) := by gcongr
      _ = ENNReal.ofReal ((Real.sqrt 6 * r) ^ 2) := by
        rw [← ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 6)]
        congr 1
        rw [mul_pow, hsqrt]
  have h := PhaseStateMoment.phase_state_second_moment_of_wasserstein
    nu reference xstar hX hP hXbound hPbound hordinary
  refine ⟨h.1, h.2.trans_eq ?_⟩
  rw [mul_pow, hsqrt]
  ring

end

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PhaseMetric
