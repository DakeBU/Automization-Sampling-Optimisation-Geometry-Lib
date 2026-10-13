open scoped Classical in
/-- Hitting time: given a stochastic process `u` and a set `s`, `hittingAfter u s n` is
the first time `u` is in `s` after time `n` (if `u` does not hit `s` after time `n` then the
hitting time is `⊤`). -/
noncomputable def hittingAfter (u : ι → Ω → β) (s : Set β) (n : ι) :
    Ω → WithTop ι :=
  fun x ↦ if ∃ j, n ≤ j ∧ u j x ∈ s then (sInf {i : ι | n ≤ i ∧ u i x ∈ s} : ι) else ⊤

open scoped Classical in
theorem hittingBtwn_def (u : ι → Ω → β) (s : Set β) (n m : ι) :
    hittingBtwn u s n m =
    fun x => if ∃ j ∈ Set.Icc n m, u j x ∈ s then sInf (Set.Icc n m ∩ {i : ι | u i x ∈ s}) else m :=
  rfl

open scoped Classical in
lemma hittingAfter_def (u : ι → Ω → β) (s : Set β) (n : ι) :
    hittingAfter u s n =
    fun x => if ∃ j, n ≤ j ∧ u j x ∈ s
      then ((sInf {i : ι | n ≤ i ∧ u i x ∈ s} : ι) : WithTop ι) else ⊤ := rfl
