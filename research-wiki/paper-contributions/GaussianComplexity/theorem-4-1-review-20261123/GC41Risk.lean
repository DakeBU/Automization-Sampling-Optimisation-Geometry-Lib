import GC44GramUse
import GC41KnownSpectrum
import GC31SourceChecks
import AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar

/-! The Haar input distribution with the independent algorithm seed.
Uniform accuracy is on the actual fixed-input output. Integrating the
matrix-dependent strict event gives the detector probability in the joint
experiment with the orientation retained. -/

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
set_option maxHeartbeats 900000
set_option backward.isDefEq.respectTransparency false
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis

variable {d q : ℕ} {κ ε : ℝ} {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]

def experimentPair (κ : ℝ) (q : ℕ) (alg : Algorithm d Seed State)
    (p : Seed × Matrix.orthogonalGroup (Fin d) ℝ) : Matrix.orthogonalGroup (Fin d) ℝ × Space d :=
  (p.2, alg.sample q (hiddenPrecision κ p.2) p.1)

theorem measurable_experimentPair (κ : ℝ) (q : ℕ) (alg : Algorithm d Seed State) :
    Measurable (experimentPair κ q alg) := by
  have hp : Continuous (hiddenPrecision (d := d) κ) := by
    unfold hiddenPrecision
    exact (continuous_subtype_val.matrix_mul continuous_const).matrix_mul continuous_subtype_val.matrix_transpose
  let P := Matrix.orthogonalGroup (Fin d) ℝ
  have hf : Measurable (fun p : Seed × P => (p.1, hiddenPrecision κ p.2)) :=
    measurable_id.prodMap hp.measurable
  have hx := (alg.measurable_sample q).comp hf
  exact (measurable_snd : Measurable (Prod.snd : Seed × P → P)).prodMk hx

def experimentLaw (κ : ℝ) (q : ℕ) (ρ : Measure Seed) (alg : Algorithm d Seed State) :
    Measure (Matrix.orthogonalGroup (Fin d) ℝ × Space d) :=
  (ρ.prod (orthogonalHaar d)).map (experimentPair κ q alg)

theorem admissible_hiddenPrecision {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) : Admissible κ (hiddenPrecision κ O) := by
  have h := FixedSpectrumAdmissibility.actual_precision_admissible hd hκ O
  exact (admissible_iff_posSemidef_bounds κ _).mpr ⟨h.1.1,h.2⟩

private theorem measurable_fixed_sample (alg : Algorithm d Seed State) (q : ℕ) (A : Precision d) :
    Measurable (alg.sample q A) := by
  have h₁ : Measurable (fun s : Seed => (s,A)) := measurable_prodMk_right
  have h₂ := (alg.measurable_sample q).comp h₁
  exact h₂

/-- If all the targets pass the detector with probability at least 9/10, an
accurate algorithm on the same fixed inputs has average pass rate ≥ 9/10−ε. -/
theorem experiment_detector_lower {τ : ℝ} (ρ : Measure Seed) [IsProbabilityMeasure ρ]
    (alg : Algorithm d Seed State)
    (hacc : ∀ O : Matrix.orthogonalGroup (Fin d) ℝ, eventTV (alg.outputLaw ρ q (hiddenPrecision κ O)) (targetLaw (hiddenPrecision κ O)) ≤ ε)
    (hpow : ∀ O : Matrix.orthogonalGroup (Fin d) ℝ, (9/10 : ℝ) ≤ (targetLaw (hiddenPrecision κ O)).real
      (detectorEvent κ (2*q+1) τ (hiddenPrecision κ O))) :
    9/10 - ε ≤ (experimentLaw κ q ρ alg).real (jointDetectorEvent d q κ τ) := by
  let μ := orthogonalHaar d
  let : IsProbabilityMeasure μ := (orthogonalHaar_spec d).1
  let H := jointDetectorEvent d q κ τ
  let F := experimentPair κ q alg
  have hH : MeasurableSet H := measurableSet_jointDetectorEvent d q κ τ
  have hF : Measurable F := measurable_experimentPair κ q alg
  let : IsProbabilityMeasure (experimentLaw κ q ρ alg) :=
    Measure.isProbabilityMeasure_map (μ := ρ.prod μ) hF.aemeasurable
  apply (ENNReal.ofReal_le_iff_le_toReal (measure_ne_top (experimentLaw κ q ρ alg) H)).mp
  change _ ≤ ((ρ.prod μ).map F) H
  rw [Measure.map_apply hF hH, Measure.prod_apply_symm (hF hH)]
  calc
    _ = ∫⁻ _ : Matrix.orthogonalGroup (Fin d) ℝ, ENNReal.ofReal (9/10-ε) ∂μ := by simp
    _ ≤ _ := by
      apply lintegral_mono
      intro O
      let A := hiddenPrecision κ O
      let B := detectorEvent κ (2*q+1) τ A
      have hs := measurable_fixed_sample alg q A
      let : IsProbabilityMeasure (alg.outputLaw ρ q A) := Measure.isProbabilityMeasure_map hs.aemeasurable
      have hB : MeasurableSet B := measurableSet_detectorEvent κ (2*q+1) τ A
      have gap := (event_gap_le_tv (alg.outputLaw ρ q A) (targetLaw A) hB).trans (hacc O)
      have lower : 9/10 - ε ≤ (alg.outputLaw ρ q A).real B := by
        have := (abs_le.mp gap).1
        have t : (9/10 : ℝ) ≤ (targetLaw A).real B := hpow O
        linarith
      have hmass := (ENNReal.ofReal_le_iff_le_toReal (measure_ne_top (alg.outputLaw ρ q A) B)).mpr lower
      change _ ≤ ρ ((alg.sample q A) ⁻¹' B)
      rw [← Measure.map_apply hs hB]
      exact hmass

#print axioms experiment_detector_lower
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
