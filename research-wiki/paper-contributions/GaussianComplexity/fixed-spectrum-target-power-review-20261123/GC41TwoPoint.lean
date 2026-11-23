import GC31Mixture

/-!
# Two disjoint high-probability events

Both total variation inequalities use the first event as a single measurable
witness. Its probability is large for the first target and small for the
second. A sampler that receives the same information on both inputs has
one common output law to compare with the two targets.
-/

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation

variable {X : Type*} [MeasurableSpace X]

/-- If two targets give their own disjoint events mass at least 9/10, the
targets are 4/5 apart and each common output law has worst-case error at least 2/5. -/
theorem two_point_event_separation (P Q : Measure X) [IsProbabilityMeasure P] [IsProbabilityMeasure Q]
    {U V : Set X} (hU : MeasurableSet U) (hV : MeasurableSet V) (hd : Disjoint U V)
    (hp : 9/10 ≤ P.real U) (hq : 9/10 ≤ Q.real V) :
    4/5 ≤ eventTV P Q ∧ ∀ (μ : Measure X) [IsProbabilityMeasure μ],
      2/5 ≤ max (eventTV μ P) (eventTV μ Q) := by
  have hsum : Q.real U + Q.real V ≤ 1 := by
    rw [← measureReal_union hd hV]
    exact measureReal_le_one
  have hgap : 4/5 ≤ P.real U - Q.real U := by linarith
  constructor
  · exact hgap.trans ((le_abs_self _).trans (event_gap_le_tv P Q hU))
  · intro μ _
    have h₁ := (neg_le_abs (μ.real U - P.real U)).trans (event_gap_le_tv μ P hU)
    have h₂ := (le_abs_self (μ.real U - Q.real U)).trans (event_gap_le_tv μ Q hU)
    linarith [le_max_left (eventTV μ P) (eventTV μ Q), le_max_right (eventTV μ P) (eventTV μ Q)]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
