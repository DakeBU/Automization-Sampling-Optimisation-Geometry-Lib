import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# Continuity of an integral with a moving probability law

Joint continuity on a compact state space controls variation of the
observable uniformly. Weak continuity of the law controls the remaining
integral of a fixed observable.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Measure.WeakProbabilityIntegral

open Filter MeasureTheory Set
open scoped Topology

variable {T X : Type*} [TopologicalSpace T] [TopologicalSpace X] [CompactSpace X]
  [MeasurableSpace X] [OpensMeasurableSpace X]

/-- The integral of a jointly continuous observable on a compact state space
is continuous along a weakly continuous probability-law curve. -/
theorem continuous_integral_of_compact
    {F : T → X → ℝ} (hF : Continuous (fun p : T × X => F p.1 p.2))
    {μ : T → ProbabilityMeasure X} (hμ : Continuous μ) :
    Continuous (fun t => ∫ x, F t x ∂(μ t : Measure X)) := by
  have hFc (t : T) : Continuous (F t) := by
    have hpair : Continuous (fun x : X => (t, x)) := continuous_const.prodMk continuous_id
    exact hF.comp hpair
  rw [continuous_iff_continuousAt]
  intro t
  let fixed : C(X, ℝ) := ⟨F t, hFc t⟩
  have hweak :
      Tendsto (fun u => ∫ x, F t x ∂(μ u : Measure X)) (𝓝 t)
        (𝓝 (∫ x, F t x ∂(μ t : Measure X))) :=
    ((ProbabilityMeasure.continuous_integral_continuousMap fixed).comp hμ).continuousAt
  let error := fun u => ∫ x, F u x - F t x ∂(μ u : Measure X)
  have herr : Tendsto error (𝓝 t) (𝓝 0) := by
    apply Metric.tendsto_nhds.mpr
    intro ε hε
    have hnear : ∀ᶠ u in 𝓝 t, ∀ x ∈ (univ : Set X), ‖F u x - F t x‖ < ε / 2 :=
      isCompact_univ.eventually_forall_of_forall_eventually (fun x _ => by
        have hfixed : Continuous (fun p : T × X => F t p.2) := (hFc t).comp continuous_snd
        have hdiff := (hF.sub hfixed).continuousAt (x := (t, x))
        have h := Metric.tendsto_nhds.mp hdiff.tendsto (ε / 2) (half_pos hε)
        simpa only [Pi.sub_apply, sub_self, dist_zero_right] using h)
    filter_upwards [hnear] with u hu
    have hbound := norm_integral_le_of_norm_le_const (μ := (μ u : Measure X))
      (ae_of_all _ (fun x => (hu x (mem_univ x)).le))
    have hle : ‖error u‖ ≤ ε / 2 := by simpa [error] using hbound
    simpa only [dist_zero_right] using hle.trans_lt (half_lt_self hε)
  have hsum := hweak.add herr
  simp only [add_zero] at hsum
  apply hsum.congr'
  filter_upwards with u
  have hI (v : T) : Integrable (F v) (μ u : Measure X) :=
    (BoundedContinuousFunction.mkOfCompact ⟨F v, hFc v⟩).integrable _
  dsimp only [error, Pi.add_apply]
  rw [integral_sub (hI u) (hI t)]
  ring

end AutoSamplingTheory.TechnicalLemmas.Measure.WeakProbabilityIntegral
