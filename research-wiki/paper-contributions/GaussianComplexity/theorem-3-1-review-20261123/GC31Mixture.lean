import GC33Target

/-!
# Uniform accuracy under a hard input prior

For each measurable event, integrate its fixed-input output and target probabilities.
Uniform accuracy on the support bounds the difference of these integrals. Under a
common averaged output, the two target mixtures then differ by at most twice the
accuracy. These statements use the measurable-event definition of total variation.
-/

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open scoped ENNReal

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

variable {X P : Type*} [MeasurableSpace X] [MeasurableSpace P]

theorem event_gap_le_tv (μ ν : Measure X) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    {B : Set X} (hB : MeasurableSet B) : |μ.real B - ν.real B| ≤ eventTV μ ν := by
  unfold eventTV
  refine le_csSup ?_ (show |μ.real B - ν.real B| ∈
    {z : ℝ | ∃ S : Set X, MeasurableSet S ∧ z = |μ.real S - ν.real S|} from ⟨B, hB, rfl⟩)
  refine ⟨1, ?_⟩
  rintro _ ⟨S, _, rfl⟩
  have hp₀ : 0 ≤ μ.real S := measureReal_nonneg
  have hp₁ : μ.real S ≤ 1 := measureReal_le_one
  have hq₀ : 0 ≤ ν.real S := measureReal_nonneg
  have hq₁ : ν.real S ≤ 1 := measureReal_le_one
  exact abs_le.mpr ⟨by linarith, by linarith⟩

private theorem real_bind_event (D : Measure P) {K : P → Measure X} (hK : AEMeasurable K D)
    [∀ a, IsProbabilityMeasure (K a)] {B : Set X} (hB : MeasurableSet B) :
    (D.bind K).real B = ∫ a, (K a).real B ∂D := by
  rw [measureReal_def, Measure.bind_apply hB hK]
  exact (integral_toReal ((Measure.measurable_coe hB).comp_aemeasurable hK)
    (ae_of_all _ fun a => measure_lt_top (K a) B)).symm

private theorem integrable_event (D : Measure P) [IsProbabilityMeasure D]
    {K : P → Measure X} (hK : AEMeasurable K D) [∀ a, IsProbabilityMeasure (K a)]
    {B : Set X} (hB : MeasurableSet B) : Integrable (fun a => (K a).real B) D := by
  have hm := ENNReal.measurable_toReal.comp_aemeasurable
    ((Measure.measurable_coe hB).comp_aemeasurable hK)
  apply (integrable_const (1 : ℝ)).mono' hm.aestronglyMeasurable
  exact ae_of_all _ fun a => by
    change ‖(K a).real B‖ ≤ 1
    rw [Real.norm_eq_abs, abs_of_nonneg measureReal_nonneg]
    exact measureReal_le_one

theorem event_gap_under_mixing (D : Measure P) [IsProbabilityMeasure D]
    {K L : P → Measure X} (hK : AEMeasurable K D) (hL : AEMeasurable L D)
    [∀ a, IsProbabilityMeasure (K a)] [∀ a, IsProbabilityMeasure (L a)]
    {ε : ℝ} (hacc : ∀ᵐ a ∂D, eventTV (K a) (L a) ≤ ε) {B : Set X} (hB : MeasurableSet B) :
    |(D.bind K).real B - (D.bind L).real B| ≤ ε := by
  have hi := integrable_event D hK hB
  have hj := integrable_event D hL hB
  have hpt := hacc.mono fun a ha => (event_gap_le_tv (K a) (L a) hB).trans ha
  rw [real_bind_event D hK hB, real_bind_event D hL hB, ← integral_sub hi hj]
  calc
    _ ≤ ∫ a, |(K a).real B - (L a).real B| ∂D := by
      simpa only [Real.norm_eq_abs] using
        (norm_integral_le_integral_norm (μ := D) (fun a => (K a).real B - (L a).real B))
    _ ≤ ∫ _ : P, ε ∂D := integral_mono_ae (hi.sub hj).abs (integrable_const _) hpt
    _ = ε := by simp

variable {d n T : ℕ} {κ ε : ℝ} {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]

/-- Source comparison before equation (9) for any block size with 2T < n. -/
theorem target_separation_le_twice_accuracy (hn : 3 ≤ n) (hnd : n ≤ d) (hκ : 4 ≤ κ)
    (hT : 2*T < n) (ρ : Measure Seed) [IsProbabilityMeasure ρ] (alg : Algorithm d Seed State)
    (hacc : ∀ A, Admissible κ A → eventTV (alg.outputLaw ρ T A) (targetLaw A) ≤ ε) :
    eventTV (averagedTarget d n κ 1) (averagedTarget d n κ (-1)) ≤ 2 * ε := by
  let K := alg.outputLaw ρ T
  have hK : Measurable K := measurable_seed_output_law ρ _ (alg.measurable_sample T)
  let (A : Precision d) : IsProbabilityMeasure (K A) :=
    Measure.isProbabilityMeasure_map (((alg.measurable_sample T).comp
      (measurable_prodMk_right (y := A))).aemeasurable)
  have closeness (b : ℝ) (hb : b = 1 ∨ b = -1) {B : Set (E d)} (hB : MeasurableSet B) :
      |((hardPrior d n κ b).bind K).real B - (averagedTarget d n κ b).real B| ≤ ε := by
    let D := hardPrior d n κ b
    let : IsProbabilityMeasure D := hardPrior_probability hn hnd hκ hb
    apply event_gap_under_mixing D hK.aemeasurable
      (targetLaw_aeMeasurable D (hardPrior_posDef hn hnd hκ hb)) _ hB
    exact (hardPrior_admissible hn hnd hκ b).mono (fun A hA => hacc A hA)
  have hcommon := averaged_first_order_indistinguishability hn hnd hκ hT ρ alg
  change (hardPrior d n κ 1).bind K = (hardPrior d n κ (-1)).bind K at hcommon
  unfold eventTV
  apply csSup_le
  · exact ⟨0, ∅, MeasurableSet.empty, by simp⟩
  rintro _ ⟨B, hB, rfl⟩
  have hp := closeness 1 (Or.inl rfl) hB
  have hm := closeness (-1) (Or.inr rfl) hB
  rw [hcommon] at hp
  exact abs_le.mpr ⟨by linarith [(abs_le.mp hp).2, (abs_le.mp hm).1],
    by linarith [(abs_le.mp hp).1, (abs_le.mp hm).2]⟩

#print axioms target_separation_le_twice_accuracy
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
