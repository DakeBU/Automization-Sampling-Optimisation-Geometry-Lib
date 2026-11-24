import GC3TraceFrames
import GC3JointIteration

/-! Padded Borel evolution and equality to the genuinely unrestricted oracle
on every realization satisfying the source per-block cap. -/
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior.PublicFrame

variable {k N : ℕ}

abbrev Live (k N : ℕ) := Trace k N × Bool

def pickQuery (select : Trace k N → Option (Query k N)) (p : Live k N) : Option (Query k N) :=
  if p.2 then none else
    match select p.1 with
    | none => none
    | some q => if 2 ≤ (foldFrames p.1 q.1).1 then some q else none

def pushState (p : Live k N) (r : Record k N) : Live k N := (p.1++[r], r.isNone)

def nextState (select : Trace k N → Option (Query k N))
    (pW : Live k N × (Fin k → O N)) : Live k N :=
  match pickQuery select pW.1 with
  | none => pushState pW.1 none
  | some q => pushState pW.1 (some (q,oracleAnswer pW.2 q))

theorem pickQuery_ready {select : Trace k N → Option (Query k N)} {p : Live k N} {q : Query k N}
    (h : pickQuery select p = some q) : 2 ≤ (foldFrames p.1 q.1).1 := by
  unfold pickQuery at h
  split at h
  · contradiction
  · cases he : select p.1 with
    | none => simp [he] at h
    | some a =>
      simp only [he] at h
      split at h
      · exact Option.some.inj h ▸ by assumption
      · contradiction

theorem measurable_pickQuery {select : Trace k N → Option (Query k N)} (hs : Measurable select) :
    Measurable (pickQuery select) := by
  apply Measurable.ite (measurable_snd (measurableSet_singleton true)) measurable_const
  let ok (p : Live k N) (q : Query k N) := if 2 ≤ (foldFrames p.1 q.1).1 then some q else none
  suffices hOk : Measurable (Function.uncurry ok) by
    convert measurable_option_cases (fun p : Live k N => select p.1) (hs.comp measurable_fst)
      (fun _ => none) measurable_const ok hOk using 1
    funext p
    cases select p.1 <;> rfl
  let X := Live k N × Query k N
  let idx (h : X) := h.2.1
  have hi : Measurable idx := measurable_fst.comp measurable_snd
  have hf : Measurable fun h : X => foldFrames h.1.1 (idx h) :=
    (measurable_from_prod_countable_right (f := fun t : Fin k × Trace k N => foldFrames t.2 t.1)
      (fun j => (measurable_pi_apply j).comp measurable_foldFrames)).comp
      (hi.prodMk (measurable_fst.comp measurable_fst))
  exact Measurable.ite (measurableSet_le measurable_const (measurable_profile.comp hf))
    (measurable_some.comp measurable_snd) measurable_const

theorem measurable_pushState : Measurable (Function.uncurry (@pushState k N)) := by
  have hn : Measurable (fun r : Record k N => r.isNone) := by
    convert measurable_option_cases (fun r : Record k N => r) measurable_id
      (fun _ => true) measurable_const (fun _ _ => false) measurable_const using 1
    funext r
    cases r <;> rfl
  exact (measurable_append_singleton (measurable_fst.comp measurable_fst) measurable_snd).prodMk
    (hn.comp measurable_snd)

theorem measurable_nextState {select : Trace k N → Option (Query k N)} (hs : Measurable select) :
    Measurable (nextState select) := by
  let X := Live k N × (Fin k → O N)
  let flag := pickQuery select ∘ (Prod.fst : X → Live k N)
  let add (p : X) (q : Query k N) := pushState p.1 (some (q,oracleAnswer p.2 q))
  have hAdd : Measurable (Function.uncurry add) :=
    measurable_pushState.comp ((measurable_fst.comp measurable_fst).prodMk
      (measurable_some.comp (measurable_snd.prodMk (measurable_oracleAnswer.comp
        ((measurable_snd.comp measurable_fst).prodMk measurable_snd)))))
  convert measurable_option_cases flag ((measurable_pickQuery hs).comp measurable_fst)
    (fun p => pushState p.1 none) (measurable_pushState.comp (measurable_fst.prodMk measurable_const))
    add hAdd using 1
  funext p
  cases hp : pickQuery select p.1 <;> simp [nextState,flag,Function.comp_apply,hp,add]

theorem blockCount_append_records (j : Fin k) (h l : Trace k N) :
    blockCount j (h++l) = blockCount j h + blockCount j l := by
  induction h with
  | nil => simp [blockCount]
  | cons r h ih =>
    rcases r with _ | ⟨q,y⟩
    · exact ih
    · simp [blockCount, ih, Nat.add_assoc]

private theorem repeat_front {H X : Type*} (step : H × X → H) (h : H) (n : ℕ) (w : X) :
    repeatState step h (n+1) w = repeatState step (step (h,w)) n w := by
  induction n with
  | zero => rfl
  | succ n ih => exact congrArg (fun a => step (a,w)) ih

private theorem stopped (select : Trace k N → Option (Query k N)) (n : ℕ) (past : Trace k N)
    (W : Fin k → O N) : repeatState (nextState select) (past,true) n W =
      (past ++ List.replicate n none,true) := by
  induction n generalizing past with
  | zero => simp [repeatState]
  | succ n ih =>
    rw [repeat_front]
    change repeatState (nextState select) (past++[none],true) n W = _
    rw [ih]
    simp [List.replicate_succ]

theorem guarded_eq_raw_from (select : Trace k N → Option (Query k N)) {T : ℕ} (hN : 2*T < N)
    (n : ℕ) (past : Trace k N) (W : Fin k → O N)
    (cap : ∀ j, blockCount j past + blockCount j (rawRun select n past W) ≤ 2*T) :
    (repeatState (nextState select) (past,false) n W).1 = past ++ rawRun select n past W := by
  induction n generalizing past with
  | zero => simp [repeatState,rawRun]
  | succ n ih =>
    rw [repeat_front]
    cases hq : select past with
    | none =>
      have hn : nextState select ((past,false),W) = (past++[none],true) := by
        simp [nextState,pickQuery,hq,pushState]
      rw [hn,stopped]
      simp [rawRun,hq,List.replicate_succ]
    | some q =>
      let record : Record k N := some (q,oracleAnswer W q)
      have hr : rawRun select (n+1) past W = record :: rawRun select n (past++[record]) W := by
        simp [rawRun,hq,record]
      have hb := cap q.1
      rw [hr] at hb
      have hstep : blockCount q.1 past + 1 < N := by
        change blockCount q.1 past + ((if q.1=q.1 then 1 else 0) + _) ≤ _ at hb
        rw [if_pos rfl] at hb
        omega
      have hready := remaining_after_count past q.1 hstep
      have hn : nextState select ((past,false),W) = (past++[record],false) := by
        simp [nextState,pickQuery,pushState,hq,hready,record]
      rw [hn,ih,hr]
      · simp
      · intro j
        rw [blockCount_append_records]
        have hb := cap j
        rw [hr] at hb
        change (blockCount j past + ((if q.1=j then 1 else 0)+0)) + _ ≤ _
        change blockCount j past + ((if q.1=j then 1 else 0)+_) ≤ _ at hb
        omega

theorem guarded_eq_rawRun (select : Trace k N → Option (Query k N)) {T : ℕ} (hN : 2*T < N)
    (n : ℕ) (W : Fin k → O N) (cap : ∀ j, blockCount j (rawRun select n [] W) ≤ 2*T) :
    (repeatState (nextState select) ([],false) n W).1 = rawRun select n [] W := by
  simpa using guarded_eq_raw_from select hN n [] W (fun j => by simpa [blockCount] using cap j)

#print axioms measurable_nextState
#print axioms guarded_eq_rawRun
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior.PublicFrame
