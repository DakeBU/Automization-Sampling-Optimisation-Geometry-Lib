import Mathlib.MeasureTheory.MeasurableSpace.Constructions

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative

open Set

variable {E : Type*} {K : Set E}

/-- Keep each point of the set and send points outside it to a fixed member. -/
noncomputable def restrictState (fallback : K) (x : E) : K := by
  classical
  exact
  if hx : x ∈ K then ⟨x, hx⟩ else fallback

theorem coe_restrictState_of_mem (fallback : K) {x : E} (hx : x ∈ K) :
    (restrictState fallback x : E) = x := by
  classical
  simp [restrictState, hx]

theorem measurable_restrictState [MeasurableSpace E]
    (hK : MeasurableSet K) (fallback : K) : Measurable (restrictState fallback) := by
  classical
  apply Measurable.subtype_mk
  have heq : (fun x => (restrictState fallback x : E)) =
      K.piecewise id (fun _ => fallback.val) := by
    funext x
    by_cases hx : x ∈ K <;> simp [restrictState, Set.piecewise, hx]
  change Measurable (fun x => (restrictState fallback x : E))
  rw [heq]
  exact measurable_id.piecewise hK measurable_const
end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative
