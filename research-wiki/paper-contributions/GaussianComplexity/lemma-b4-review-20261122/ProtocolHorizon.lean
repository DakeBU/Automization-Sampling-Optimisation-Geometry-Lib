import B4Protocol

/-!
The cap on actual calls forces an absorbing slot immediately after the
paper's horizon, even when the policy has arbitrary behavior off this path.
-/

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

variable {k n : ℕ}

private theorem extend_or_all_queries (select : Trace k n → Option (Query k n)) (t : ℕ)
    (past : Trace k n) (W : Fin k → O n) :
    rawRun select (t+1) past W = rawRun select t past W ++ [none] ∨
      ∀ r ∈ rawRun select (t+1) past W, r ≠ none := by
  induction t generalizing past with
  | zero =>
    cases hs : select past with
    | none => exact Or.inl (by simp [rawRun, hs])
    | some q => exact Or.inr (by simp [rawRun, hs])
  | succ t ih =>
    cases hs : select past with
    | none =>
      left
      simp only [rawRun, hs]
      exact List.replicate_succ' ..
    | some q =>
      let r : Record k n := some (q, oracleAnswer W q)
      rcases ih (past ++ [r]) with h | h
      · left
        simpa only [rawRun, hs, List.cons_append] using congrArg (List.cons r) h
      · right
        simp only [rawRun, hs, List.mem_cons]
        intro x hx
        rcases hx with rfl | hmem
        · simp
        · exact h x hmem

private theorem sum_blockCount_of_full (xs : Trace k n) (h : ∀ r ∈ xs, r ≠ none) :
    ∑ j, blockCount j xs = xs.length := by
  induction xs with
  | nil => simp [blockCount]
  | cons r xs ih =>
    cases r with
    | none => exact (h none List.mem_cons_self rfl).elim
    | some p =>
      have hi := ih (fun x hx => h x (List.mem_cons_of_mem _ hx))
      simp only [blockCount, List.length_cons, Finset.sum_add_distrib, hi]
      simp [Nat.add_comm]

/-- One more attempted slot after `cap * k` is necessarily padding if the
ordinary transcript respects the per-block cap through that slot. -/
theorem rawRun_after_total_cap (select : Trace k n → Option (Query k n)) (cap : ℕ)
    (past : Trace k n) (W : Fin k → O n)
    (hcap : ∀ j, blockCount j (rawRun select (cap*k+1) past W) ≤ cap) :
    rawRun select (cap*k+1) past W = rawRun select (cap*k) past W ++ [none] := by
  rcases extend_or_all_queries select (cap*k) past W with h | h
  · exact h
  · have hle := Finset.sum_le_sum (fun j (_ : j ∈ Finset.univ) => hcap j)
    rw [sum_blockCount_of_full _ h, length_rawRun] at hle
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul] at hle
    rw [Nat.mul_comm k cap] at hle
    omega

#print axioms rawRun_after_total_cap

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
