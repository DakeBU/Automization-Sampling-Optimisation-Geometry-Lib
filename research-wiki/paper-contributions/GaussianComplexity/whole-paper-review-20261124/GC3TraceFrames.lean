import GC3PublicFrames

/-! Frames computed from the actual chronological query/answer records. -/
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling (frameComplement)
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior.PublicFrame

variable {k N : ℕ} {H : Type*} [MeasurableSpace H]

def initialFrames (k N : ℕ) : Fin k → PublicFrame N :=
  fun _ => ⟨N, BlockFrame.initial N⟩

def updateRecord (f : Fin k → PublicFrame N) (r : Record k N) : Fin k → PublicFrame N :=
  match r with
  | none => f
  | some a => Function.update f a.1.1 (recordStep (f a.1.1) a.1.2.2 a.1.2.1 a.2)

@[simp] theorem updateRecord_none (f : Fin k → PublicFrame N) : updateRecord f none = f := rfl

theorem measurable_updateRecord {f : H → Fin k → PublicFrame N} {r : H → Record k N}
    (hf : Measurable f) (hr : Measurable r) : Measurable (fun h => updateRecord (f h) (r h)) := by
  let add (h : H) (a : Query k N × Vec N) :=
    Function.update (f h) a.1.1 (recordStep (f h a.1.1) a.1.2.2 a.1.2.1 a.2)
  suffices hAdd : Measurable (Function.uncurry add) by
    convert measurable_option_cases r hr f hf add hAdd using 1
    funext h
    cases hR : r h <;> rfl
  let X := H × (Query k N × Vec N)
  let index (h : X) := h.2.1.1
  have hi : Measurable index := measurable_fst.comp (measurable_fst.comp measurable_snd)
  have hx : Measurable (fun h : X => f h.1 (index h)) :=
    (measurable_from_prod_countable_right (f := fun p : Fin k × H => f p.2 p.1)
      (fun j => (measurable_pi_apply j).comp hf)).comp (hi.prodMk measurable_fst)
  have hback : Measurable (fun h : X => h.2.1.2.2) :=
    measurable_snd.comp (measurable_snd.comp (measurable_fst.comp measurable_snd))
  have hv : Measurable (fun h : X => h.2.1.2.1) :=
    measurable_fst.comp (measurable_snd.comp (measurable_fst.comp measurable_snd))
  have hy : Measurable (fun h : X => h.2.2) := measurable_snd.comp measurable_snd
  apply measurable_pi_lambda
  intro j
  have hif : Measurable (fun h : X => if index h = j then
      recordStep (f h.1 (index h)) h.2.1.2.2 h.2.1.2.1 h.2.2 else f h.1 j) :=
    Measurable.ite (p := fun h : X => index h = j)
    (hi (measurableSet_singleton j)) (measurable_recordStep hx hback hv hy)
    ((measurable_pi_apply j).comp (hf.comp measurable_fst))
  convert hif using 1
  funext p
  rcases p with ⟨h,⟨q,y⟩⟩
  by_cases hj : q.1=j
  · subst j; simp [add, index, Function.uncurry]
  · simp [add, index, Function.uncurry,hj,Ne.symm hj]

def foldFrames (l : Trace k N) : Fin k → PublicFrame N :=
  l.foldl updateRecord (initialFrames k N)

@[simp] theorem foldFrames_nil : foldFrames ([] : Trace k N) = initialFrames k N := rfl

theorem foldFrames_append (l : Trace k N) (r : Record k N) :
    foldFrames (l ++ [r]) = updateRecord (foldFrames l) r := by simp [foldFrames]

private theorem measurable_fold_ofFn (n : ℕ)
    (f : H → Fin k → PublicFrame N) (hf : Measurable f)
    (v : H → Fin n → Record k N) (hv : Measurable v) :
    Measurable (fun h => (List.ofFn (v h)).foldl updateRecord (f h)) := by
  induction n generalizing f with
  | zero => simpa using hf
  | succ n ih =>
    simp only [List.ofFn_succ,List.foldl_cons]
    exact ih _ (measurable_updateRecord hf ((measurable_pi_apply 0).comp hv)) _
      (measurable_pi_lambda _ fun i => (measurable_pi_apply i.succ).comp hv)

theorem measurable_foldFrames : Measurable (@foldFrames k N) := by
  apply (measurable_history_iff_ofFn none _).2
  intro n
  exact measurable_fold_ofFn n _ measurable_const _ measurable_id

theorem update_oriented (f : Fin k → PublicFrame N) (h : ∀ j, Oriented (f j))
    (r : Record k N) (j : Fin k) : Oriented (updateRecord f r j) := by
  rcases r with _ | ⟨q,y⟩
  · exact h j
  · by_cases hj : j=q.1
    · subst j
      simpa only [updateRecord, Function.update_self] using step_oriented (f q.1) q.2.2 q.2.1 y (h q.1)
    · simpa only [updateRecord,Function.update_of_ne hj] using h j

private theorem fold_oriented (l : Trace k N) (f : Fin k → PublicFrame N) (ho : ∀ j, Oriented (f j)) :
    ∀ j, Oriented (l.foldl updateRecord f j) := by
  induction l generalizing f with
  | nil => exact ho
  | cons r l ih => exact ih _ (update_oriented f ho r)

theorem foldFrames_oriented (l : Trace k N) (j : Fin k) : Oriented (foldFrames l j) := by
  exact fold_oriented l (initialFrames k N) (fun _ => by simp [initialFrames,Oriented,BlockFrame.initial]) j

private theorem fold_rank_le (l : Trace k N) (f : Fin k → PublicFrame N) (j : Fin k) :
    (l.foldl updateRecord f j).2.rank ≤ (f j).2.rank + blockCount j l := by
  induction l generalizing f with
  | nil => simp [blockCount]
  | cons r l ih =>
    change (l.foldl updateRecord (updateRecord f r) j).2.rank ≤ _
    apply (ih _).trans
    rcases r with _ | ⟨⟨i,v,b⟩,y⟩
    · rfl
    · by_cases hj : j=i
      · subst j
        have h := step_rank_le (f i) b v y
        change (Function.update f i (recordStep (f i) b v y) i).2.rank + _ ≤
          (f i).2.rank + ((if i = i then 1 else 0) + _)
        rw [Function.update_self,if_pos rfl]
        omega
      · change (Function.update f i (recordStep (f i) b v y) j).2.rank + _ ≤
          (f j).2.rank + ((if i = j then 1 else 0) + _)
        rw [Function.update_of_ne hj,if_neg (Ne.symm hj),zero_add]

theorem foldFrames_rank_le (l : Trace k N) (j : Fin k) :
    (foldFrames l j).2.rank ≤ blockCount j l := by
  simpa [foldFrames,initialFrames,BlockFrame.initial] using fold_rank_le l (initialFrames k N) j

theorem remaining_after_count (l : Trace k N) (j : Fin k) (h : blockCount j l + 1 < N) :
    2 ≤ (foldFrames l j).1 := by
  have h1 := foldFrames_rank_le l j
  have h2 := (foldFrames l j).2.fits
  omega

theorem recordStep_pos (F : PublicFrame N) (hF : 0 < F.1) (back : Bool) (v y : Vec N) :
    0 < (recordStep F back v y).1 := by
  obtain ⟨m,F⟩ := F
  cases m with
  | zero => exact False.elim (Nat.not_lt_zero _ hF)
  | succ m =>
    cases m with
    | zero => exact Nat.zero_lt_succ _
    | succ n =>
      by_cases hc : frameComplement F back v = 0
      · rw [recordStep_zero _ _ _ _ hc]; exact Nat.zero_lt_succ _
      · rw [recordStep_informative _ _ _ _ hc]; exact Nat.zero_lt_succ _

private theorem fold_pos (l : Trace k N) (f : Fin k → PublicFrame N) (hp : ∀ j, 0 < (f j).1) :
    ∀ j, 0 < (l.foldl updateRecord f j).1 := by
  induction l generalizing f with
  | nil => exact hp
  | cons r l ih =>
    apply ih
    intro j
    rcases r with _ | ⟨⟨i,v,b⟩,y⟩
    · exact hp j
    · change 0 < (Function.update f i (recordStep (f i) b v y) j).1
      by_cases hj : j = i
      · subst j; rw [Function.update_self]; exact recordStep_pos _ (hp i) _ _ _
      · rw [Function.update_of_ne hj]; exact hp j

theorem foldFrames_pos (hN : 0 < N) (l : Trace k N) (j : Fin k) : 0 < (foldFrames l j).1 :=
  fold_pos l (initialFrames k N) (fun _ => hN) j

#print axioms measurable_foldFrames
#print axioms foldFrames_rank_le
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior.PublicFrame
