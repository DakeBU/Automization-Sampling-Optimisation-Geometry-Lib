import AutoSamplingTheory.TechnicalLemmas.Probability.KernelTotalVariation

/-!
# Mean conditional-kernel errors and finite hybrid telescopes

This module isolates the reusable probability-kernel core of Chen--Chewi--Lu--
Zhang, arXiv:2609.38710v1, Lemma 6.3.  If two conditional Markov kernels differ
eventwise by an integrable history-dependent bound, their output laws differ by
at most the mean of that bound.  A common downstream Markov kernel preserves
the same estimate, so later adaptive computation is absorbed by data
processing.  A finite real-valued telescope then adds the adjacent hybrid
errors.

The declarations do not construct the paper's dummy-filled history kernels,
identify its `δ_t` with a measurable total-variation function, or compare the
capped ideal algorithm with its uncapped version.  Those adapters remain
separate source obligations.
-/

open MeasureTheory ProbabilityTheory Set Finset
open scoped ProbabilityTheory BigOperators

namespace AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope

/-- An integrable pointwise event bound between two Markov kernels controls the
corresponding event discrepancy after averaging over the input law.  This is
the mean-replacement step in the adaptive hybrid argument. -/
theorem abs_real_comp_sub_le_integral_eventBound
    {A B : Type*} [MeasurableSpace A] [MeasurableSpace B]
    (μ : Measure A) [IsProbabilityMeasure μ]
    (K L : Kernel A B) [IsMarkovKernel K] [IsMarkovKernel L]
    (ε : A → ℝ) (hε : Integrable ε μ)
    (hbound : ∀ᵐ x ∂μ, ∀ s, MeasurableSet s →
      |(K x).real s - (L x).real s| ≤ ε x) :
    ∀ t, MeasurableSet t →
      |(K ∘ₘ μ).real t - (L ∘ₘ μ).real t| ≤ ∫ x, ε x ∂μ := by
  intro t ht
  have hint (M : Kernel A B) [IsMarkovKernel M] :
      Integrable (fun x => (M x).real t) μ := by
    apply (integrable_const (1 : ℝ)).mono'
      (M.measurable_coe ht).ennreal_toReal.aestronglyMeasurable
    exact Filter.Eventually.of_forall fun x => by
      rw [Real.norm_eq_abs, abs_of_nonneg ENNReal.toReal_nonneg]
      exact (measureReal_le_one : (M x).real t ≤ 1)
  have happly (M : Kernel A B) [IsMarkovKernel M] :
      (M ∘ₘ μ).real t = ∫ x, (M x).real t ∂μ := by
    change (Measure.bind μ M t).toReal = ∫ x, (M x t).toReal ∂μ
    rw [Measure.bind_apply ht M.aemeasurable]
    exact (integral_toReal (M.measurable_coe ht).aemeasurable
      (Filter.Eventually.of_forall fun x => measure_lt_top (M x) t)).symm
  rw [happly K, happly L, ← integral_sub (hint K) (hint L)]
  exact abs_integral_le_integral_abs.trans <|
    integral_mono_ae ((hint K).sub (hint L)).abs hε <|
      hbound.mono fun x hx => hx t ht

/-- The same mean replacement bound survives a common downstream Markov
kernel.  In an adjacent adaptive hybrid, the downstream kernel represents all
later calls after the one conditional rule being replaced. -/
theorem abs_real_comp_commonSuffix_sub_le_integral_eventBound
    {A B C : Type*} [MeasurableSpace A] [MeasurableSpace B] [MeasurableSpace C]
    (μ : Measure A) [IsProbabilityMeasure μ]
    (K L : Kernel A B) [IsMarkovKernel K] [IsMarkovKernel L]
    (S : Kernel B C) [IsMarkovKernel S]
    (ε : A → ℝ) (hε : Integrable ε μ)
    (hbound : ∀ᵐ x ∂μ, ∀ s, MeasurableSet s →
      |(K x).real s - (L x).real s| ≤ ε x) :
    ∀ t, MeasurableSet t →
      |((S ∘ₖ K) ∘ₘ μ).real t - ((S ∘ₖ L) ∘ₘ μ).real t| ≤
        ∫ x, ε x ∂μ := by
  have hKL := abs_real_comp_sub_le_integral_eventBound μ K L ε hε hbound
  have hS := KernelTotalVariation.abs_real_comp_sub_le
    (K ∘ₘ μ) (L ∘ₘ μ) S hKL
  simpa only [← Measure.comp_assoc] using hS

/-- Finite adjacent-hybrid errors telescope.  Applying this to the output laws
of hybrids `0, ..., n` turns the one-slot bounds into their accumulated error.
The result is deliberately stated for real sequences so it does not invent a
second total-variation definition. -/
theorem abs_sub_zero_le_sum_range_of_adjacent
    (a δ : ℕ → ℝ) (n : ℕ)
    (hstep : ∀ i < n, |a (i + 1) - a i| ≤ δ i) :
    |a n - a 0| ≤ ∑ i ∈ range n, δ i := by
  induction n with
  | zero => simp
  | succ n ih =>
      calc
        |a (n + 1) - a 0| ≤ |a (n + 1) - a n| + |a n - a 0| := by
          exact abs_sub_le _ _ _
        _ ≤ δ n + ∑ i ∈ range n, δ i :=
          add_le_add (hstep n (Nat.lt_succ_self n))
            (ih fun i hi => hstep i (hi.trans (Nat.lt_succ_self n)))
        _ = ∑ i ∈ range (n + 1), δ i := by
          rw [sum_range_succ, add_comm]

end AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope
