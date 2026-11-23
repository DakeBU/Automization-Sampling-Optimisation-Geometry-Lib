import B4HistorySpace
import AutoSamplingTheory.TechnicalLemmas.Analysis.BatchedOracleSimulation

/-!
# Running a stateful primitive policy from its transcript

Replay chronological query/answer records to recover the state and its final
readout. The proof keeps the label costs used by the Gaussian batch expansion.
-/

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarBatchProtocol

open AutoSamplingTheory.TechnicalLemmas.Analysis

variable {k n : ℕ} {S X : Type*} [MeasurableSpace S] [MeasurableSpace X]

def ask {P : Type*} : X ⊕ P → Option P := Sum.elim (fun _ => none) some

def halt {P : Type*} : X ⊕ P → Option X := Sum.elim some (fun _ => none)

theorem measurable_ask {P : Type*} [MeasurableSpace P] :
    Measurable (ask : X ⊕ P → Option P) := measurable_const.sumElim measurable_some

theorem measurable_halt {P : Type*} [MeasurableSpace P] :
    Measurable (halt : X ⊕ P → Option X) := measurable_some.sumElim measurable_const

/-- Apply every non-padding record in order. -/
def replay (step : S → Query k n → Vec n → S) (s : S) (h : Trace k n) : S :=
  h.foldl (fun a r => match r with | none => a | some p => step a p.1 p.2) s

theorem measurable_replay (step : S → Query k n → Vec n → S)
    (hs : Measurable (fun p : S × Query k n × Vec n => step p.1 p.2.1 p.2.2)) :
    Measurable (Function.uncurry (replay step)) := by
  let advance := fun a (r : Record k n) => match r with
    | none => a | some p => step a p.1 p.2
  have hm : Measurable (Function.uncurry advance) := by
    convert measurable_option_cases (fun p : S × Record k n => p.2) measurable_snd
      Prod.fst measurable_fst (fun p qy => step p.1 qy.1 qy.2)
      (hs.comp ((measurable_fst.comp measurable_fst).prodMk measurable_snd)) using 1
    funext ⟨s,r⟩
    cases r <;> rfl
  have fold (m : ℕ) : Measurable (fun p : S × (Fin m → Record k n) =>
      (List.ofFn p.2).foldl advance p.1) := by
    induction m with
    | zero => simpa only [List.ofFn_zero, List.foldl_nil] using
        (measurable_fst : Measurable (Prod.fst : S × (Fin 0 → Record k n) → S))
    | succ m ih =>
      simp only [List.ofFn_succ, List.foldl_cons]
      exact ih.comp ((hm.comp (measurable_fst.prodMk ((measurable_pi_apply 0).comp measurable_snd))).prodMk
        (measurable_pi_lambda _ fun j => (measurable_pi_apply j.succ).comp measurable_snd))
  let eval := fun p : ℕ × (S × Trace k n) =>
    (List.ofFn (tupleAt none p.1 p.2.2)).foldl advance p.2.1
  have he : Measurable eval := measurable_from_prod_countable_right fun m =>
    (fold m).comp (measurable_fst.prodMk ((measurable_tupleAt none m).comp measurable_snd))
  have h := he.comp ((measurable_trace_length.comp measurable_snd).prodMk measurable_id)
  change Measurable (fun p : S × Trace k n =>
    (List.ofFn (tupleAt none p.2.length p.2)).foldl advance p.1) at h
  simp only [tupleAt_length] at h
  change Measurable (fun p : S × Trace k n => p.2.foldl advance p.1)
  exact h

omit [MeasurableSpace S] in
private theorem replay_pad (step : S → Query k n → Vec n → S) (past : Trace k n)
    (t : ℕ) (s : S) : replay step s (past ++ List.replicate t none) = replay step s past := by
  simp only [replay, List.foldl_append]
  induction t with
  | zero => rfl
  | succ t ih => simpa only [List.replicate_succ, List.foldl_cons] using ih

private theorem blockCount_pad (j : Fin k) (t : ℕ) :
    blockCount j (List.replicate t (none : Record k n)) = 0 := by
  induction t with
  | zero => rfl
  | succ t ih => simp [List.replicate_succ, blockCount, ih]

omit [MeasurableSpace S] [MeasurableSpace X] in
/-- Start from any already-read history and replay its raw continuation. This
recovers the canonical state and tagged output, and every well-tracked block
counter increases by its actual number of records. -/
theorem replay_raw_correct (next : S → X ⊕ Query k n) (step : S → Query k n → Vec n → S)
    (counter : S → Fin k → ℕ) (hc : ∀ s p, next s = .inr p → ∀ y j,
      counter (step s p y) j = counter s j + (if p.1 = j then 1 else 0))
    (W : Fin k → O n) (s : S) (past : Trace k n) (t : ℕ) :
    let select := fun h => ask (next (replay step s h))
    let suf := rawRun select t past W
    let start := replay step s past
    let final := replay step s (past ++ suf)
    let direct := QuadraticRegularizationOracle.run next step (oracleAnswer W) t start
    (final, halt (next final)) = direct.1 ∧
      ∀ j, counter final j = counter start j + blockCount j suf := by
  let select := fun h => ask (next (replay step s h))
  change (let suf := rawRun select t past W; let final := replay step s (past ++ suf)
          (final, halt (next final)) = (QuadraticRegularizationOracle.run next step (oracleAnswer W) t (replay step s past)).1 ∧
          ∀ j, counter final j = counter (replay step s past) j + blockCount j suf)
  induction t generalizing past with
  | zero =>
    cases hn : next (replay step s past) <;> simp [rawRun, QuadraticRegularizationOracle.run, hn, halt, blockCount]
  | succ t ih =>
    cases hn : next (replay step s past) with
    | inl x =>
      have hs : select past = none := by simp [select, hn, ask]
      simp [rawRun, hs, replay_pad, QuadraticRegularizationOracle.run, hn, halt, blockCount_pad]
    | inr q =>
      let r : Record k n := some (q, oracleAnswer W q)
      have hstart : replay step s (past ++ [r]) = step (replay step s past) q (oracleAnswer W q) := by
        simp [replay, List.foldl_append, r]
      have hs : select past = some q := by simp [select, hn, ask]
      obtain ⟨hfinal, hcount⟩ := ih (past ++ [r])
      rw [QuadraticRegularizationOracle.run, hn]
      simp only [rawRun, hs, blockCount]
      simp only [List.append_assoc, List.singleton_append] at hfinal hcount
      rw [hstart] at hfinal hcount
      constructor
      · exact hfinal
      · intro j
        have he := hcount j
        rw [hc _ _ hn] at he
        exact he.trans (Nat.add_assoc _ _ _)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarBatchProtocol
