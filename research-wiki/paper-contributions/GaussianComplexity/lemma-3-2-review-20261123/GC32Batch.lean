import GC32Replay

/-!
# Compiling a fixed batch into the padded primitive transcript

For Zhou–Suzuki, Lemma 3.2, the primitive queries in one batch are fixed by
the selected first-order query; only the next first-order query may depend on
their answers. Reuse the exact finite-batch simulation with its per-label
counts, making its selector and readout functions of the recorded transcript.
-/

open MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Analysis
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarBatchProtocol

variable {k n : ℕ} {S X Q B : Type*}
variable [MeasurableSpace S] [MeasurableSpace X] [MeasurableSpace Q] [MeasurableSpace B]

private abbrev Micro (S : Type*) (k n m : ℕ) :=
  S × (Fin m → Vec n) × Fin m × List (Query k n × Vec n)

private def nextMicro {m : ℕ} (next : S → X ⊕ Q) (plan : Q → Fin m → Query k n) :
    Micro S k n m → X ⊕ Query k n := fun z =>
  match next z.1 with
  | .inl x => .inl x
  | .inr q => .inr (plan q z.2.2.1)

private def updateMicro (m : ℕ) (hm : 0 < m) (next : S → X ⊕ Q)
    (update : S → Q → B → S) (decode : Q → (Fin m → Vec n) → B) :
    Micro S k n m → Query k n → Vec n → Micro S k n m := fun z p a =>
  match next z.1 with
  | .inl _ => z
  | .inr q =>
    let answers := Function.update z.2.1 z.2.2.1 a
    let history := (p, a) :: z.2.2.2
    if h : z.2.2.1.val + 1 < m then
      (z.1, answers, ⟨z.2.2.1.val + 1,h⟩, history)
    else (update z.1 q (decode q answers), (fun _ => 0), ⟨0, hm⟩, history)

private theorem measurable_sum_cases {D L R C : Type*} [MeasurableSpace D]
    [MeasurableSpace L] [MeasurableSpace R] [MeasurableSpace C]
    (f : D → L ⊕ R) (hf : Measurable f) (left : D → L → C) (right : D → R → C)
    (hl : Measurable (Function.uncurry left)) (hr : Measurable (Function.uncurry right)) :
    Measurable (fun d => (f d).elim (left d) (right d)) := by
  have hd := (MeasurableEquiv.prodSumDistrib D L R).measurable.comp (measurable_id.prodMk hf)
  convert (hl.sumElim hr).comp hd using 1
  funext d
  cases hd' : f d <;> simp only [Function.comp_apply, hd'] <;> rfl

private theorem measurable_nextMicro {m : ℕ} (next : S → X ⊕ Q)
    (plan : Q → Fin m → Query k n) (hn : Measurable next) (hp : ∀ i, Measurable (fun q => plan q i)) :
    Measurable (nextMicro next plan) := by
  let D := Micro S k n m
  have hi : Measurable (fun p : D × Q => p.1.2.2.1) :=
    measurable_fst.comp (measurable_snd.comp (measurable_snd.comp measurable_fst))
  have hp' : Measurable (Function.uncurry plan) := measurable_from_prod_countable_left hp
  have h := measurable_sum_cases (fun z : D => next z.1) (hn.comp measurable_fst)
    (fun _ x => Sum.inl x) (fun z q => Sum.inr (plan q z.2.2.1))
    (measurable_inl.comp measurable_snd) (measurable_inr.comp (hp'.comp (measurable_snd.prodMk hi)))
  convert h using 1
  funext z
  cases e : next z.1 <;> simp [nextMicro, e]

private theorem measurable_updateMicro (m : ℕ) (hm : 0 < m) (next : S → X ⊕ Q)
    (update : S → Q → B → S) (decode : Q → (Fin m → Vec n) → B) (hn : Measurable next)
    (hu : Measurable (fun p : S × Q × B => update p.1 p.2.1 p.2.2))
    (hd : Measurable (Function.uncurry decode)) :
    Measurable (fun p : Micro S k n m × Query k n × Vec n => updateMicro m hm next update decode p.1 p.2.1 p.2.2) := by
  let D := Micro S k n m × Query k n × Vec n
  let more (i : Fin m) (v : D × Q) : Micro S k n m :=
    let z := v.1.1
    let a := Function.update z.2.1 i v.1.2.2
    let l := v.1.2 :: z.2.2.2
    if h : i.val + 1 < m then (z.1, a, ⟨i.val+1,h⟩, l)
    else (update z.1 v.2 (decode v.2 a), fun _ => 0, ⟨0,hm⟩, l)
  have hs : Measurable (fun v : D × Q => v.1.1.1) :=
    measurable_fst.comp (measurable_fst.comp measurable_fst)
  have hdata : Measurable (fun v : D × Q => v.1.1.2) :=
    measurable_snd.comp (measurable_fst.comp measurable_fst)
  have hr : Measurable (fun v : D × Q => v.1.2) := measurable_snd.comp measurable_fst
  have hl := measurable_list_cons hr (measurable_snd.comp (measurable_snd.comp hdata))
  have hmore (i : Fin m) : Measurable (more i) := by
    have ha : Measurable (fun v : D × Q => Function.update v.1.1.2.1 i v.1.2.2) := by
      apply measurable_pi_lambda
      intro j
      by_cases hj : j = i
      · subst j; simpa only [Function.update_self] using hr.snd
      · simp only [Function.update_of_ne hj]
        exact (measurable_pi_apply j).comp hdata.fst
    by_cases hi : i.val+1 < m
    · simp only [more, dif_pos hi]
      exact hs.prodMk (ha.prodMk ((measurable_const (a := (⟨i.val+1,hi⟩ : Fin m))).prodMk hl))
    · have hstate := hu.comp (hs.prodMk (measurable_snd.prodMk (hd.comp (measurable_snd.prodMk ha))))
      simp only [more, dif_neg hi]
      exact hstate.prodMk
        ((measurable_const (a := (fun _ : Fin m => (0 : Vec n)))).prodMk
          ((measurable_const (a := (⟨0,hm⟩ : Fin m))).prodMk hl))
  have hh : Measurable (Function.uncurry more) :=
    measurable_from_prod_countable_right fun i => hmore i
  have hcursor := (measurable_fst.comp (measurable_snd.comp hdata))
  have h := measurable_sum_cases (fun p : D => next p.1.1)
    (hn.comp (measurable_fst.comp measurable_fst))
    (fun p _ => p.1) (fun p q => more p.1.2.2.1 (p,q))
    (measurable_fst.comp measurable_fst) (hh.comp (hcursor.prodMk measurable_id))
  convert h using 1
  funext p
  cases e : next p.1.1 <;> simp [updateMicro, more, e]

/-- Compile any adaptive first-order state machine using a fixed positive
number of primitive slots per request. The complete primitive transcript
locally determines the source state and output. Each block's cost is exactly
its multiplicity in one batch times the number of actual first-order requests. -/
theorem compile_batch (m : ℕ) (hm : 0 < m) (next : S → X ⊕ Q)
    (update : S → Q → B → S) (plan : Q → Fin m → Query k n)
    (decode : Q → (Fin m → Vec n) → B) (hnext : Measurable next)
    (hupdate : Measurable (fun p : S × Q × B => update p.1 p.2.1 p.2.2))
    (hplan : ∀ i, Measurable (fun q => plan q i)) (hdecode : Measurable (Function.uncurry decode))
    (slot : Fin m → Fin k) (hlabel : ∀ q i, (plan q i).1 = slot i) :
    ∃ select : S → Trace k n → Option (Query k n), ∃ output : S → Trace k n → S × Option X,
      Measurable (Function.uncurry select) ∧ Measurable (Function.uncurry output) ∧
      ∀ (s : S) (W : Fin k → O n) (T : ℕ),
        let h := rawRun (select s) (m*T) [] W
        let direct := QuadraticRegularizationOracle.run next update
          (fun q => decode q (fun i => oracleAnswer W (plan q i))) T s
        output s h = direct.1 ∧ direct.2 ≤ T ∧
          ∀ j, blockCount j h = (List.ofFn slot).countP (fun v => decide (v = j)) * direct.2 := by
  let nx := nextMicro next plan
  let upd := updateMicro (k := k) m hm next update decode
  let init := fun s : S =>
    (s, fun _ : Fin m => (0 : Vec n), (⟨0,hm⟩ : Fin m), ([] : List (Query k n × Vec n)))
  let state := fun s h => replay upd (init s) h
  let select := fun s h => ask (nx (state s h))
  let output := fun s h => ((state s h).1, halt (nx (state s h)))
  have hx : Measurable nx := measurable_nextMicro next plan hnext hplan
  have hu := measurable_updateMicro (k := k) m hm next update decode hnext hupdate hdecode
  have hi : Measurable init := measurable_id.prodMk measurable_const
  have hr : Measurable (Function.uncurry state) := (measurable_replay upd hu).comp
    ((hi.comp measurable_fst).prodMk measurable_snd)
  refine ⟨select, output, measurable_ask.comp (hx.comp hr),
    hr.fst.prodMk (measurable_halt.comp (hx.comp hr)), ?_⟩
  intro s W T
  let h := rawRun (select s) (m*T) [] W
  let direct := QuadraticRegularizationOracle.run next update
    (fun q => decode q (fun i => oracleAnswer W (plan q i))) T s
  let primitive := QuadraticRegularizationOracle.run nx upd (oracleAnswer W) (m*T) (init s)
  let count := fun (z : Micro S k n m) (j : Fin k) =>
    z.2.2.2.countP (fun pa => decide (pa.1.1 = j))
  have hcost (z : Micro S k n m) (p : Query k n) (hp : nx z = .inr p) (y : Vec n) (j : Fin k) :
      count (upd z p y) j = count z j + (if p.1 = j then 1 else 0) := by
    cases hn : next z.1 with
    | inl x => simp [nx, nextMicro, hn] at hp
    | inr q =>
      simp only [upd, updateMicro, hn]
      split <;> simp [count, List.countP_cons, Nat.add_comm]
  obtain ⟨hraw, hcounts⟩ := replay_raw_correct nx upd count hcost W (init s) [] (m*T)
  change (state s h, halt (nx (state s h))) = primitive.1 at hraw
  have hcounts' (j : Fin k) : count (state s h) j = blockCount j h := by
    exact (hcounts j).trans (Nat.zero_add _)
  have heq := BatchedOracleSimulation.batch_simulation_with_trace_and_label_costs
    m hm (0 : Vec n) next update (oracleAnswer W)
    (fun q => decode q (fun i => oracleAnswer W (plan q i))) plan decode
    Prod.fst slot (fun _ => rfl) hlabel T s
  extract_lets M oldNext oldUpdate oldBatch at heq
  have eNext : oldNext = nx := by
    funext z
    cases eq : next z.1 <;> simp [oldNext, nx, nextMicro, eq]
  have eUpdate : oldUpdate = upd := by
    funext z p a
    cases eq : next z.1 <;> simp [oldUpdate, upd, updateMicro, eq]
  have eBatch : oldBatch = primitive := by
    dsimp only [oldBatch, primitive]
    rw [eNext, eUpdate]
  rw [eBatch] at heq
  change ((primitive.1.1.1, primitive.1.2), primitive.2 / m) = direct ∧
    primitive.2 = m * direct.2 ∧ direct.2 ≤ T ∧
    (∀ j, count primitive.1.1 j = (List.ofFn slot).countP (fun v => decide (v = j)) * direct.2) at heq
  constructor
  · exact (congrArg (fun p : Micro S k n m × Option X => (p.1.1, p.2)) hraw).trans
      (congrArg Prod.fst heq.1)
  · refine ⟨heq.2.2.1, ?_⟩
    intro j
    exact (hcounts' j).symm.trans
      ((congrArg (fun p : Micro S k n m × Option X => count p.1 j) hraw).trans (heq.2.2.2 j))

#print axioms compile_batch

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarBatchProtocol
