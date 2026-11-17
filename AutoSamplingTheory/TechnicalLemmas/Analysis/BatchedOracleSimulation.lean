import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle

/-!
# Exact finite-batch refinement of the canonical oracle interpreter

Author-derived library infrastructure for the operational expansion in
arXiv:2610.20492v1, Appendix B.1. The public statement is sealed separately.
One primitive query is an actual interaction of the unchanged canonical `run`.
The trace is reverse chronological; scratch answers are never output samples.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.BatchedOracleSimulation

open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle

universe uS uQ uA uB uX uP uJ

private abbrev Micro (S : Type uS) (P : Type uP) (A : Type uA) (m : ℕ) :=
  S × (Fin m → A) × Fin m × List (P × A)

private def nextB {S : Type uS} {Q : Type uQ} {A : Type uA}
    {X : Type uX} {P : Type uP} {m : ℕ}
    (next : S → Sum X Q) (plan : Q → Fin m → P) :
    Micro S P A m → Sum X P := fun z =>
  match next z.1 with
  | .inl x => .inl x
  | .inr q => .inr (plan q z.2.2.1)

private def updateB {S : Type uS} {Q : Type uQ} {A : Type uA}
    {B : Type uB} {X : Type uX} {P : Type uP}
    (m : ℕ) (hm : 0 < m) (blank : A)
    (next : S → Sum X Q) (update : S → Q → B → S)
    (decode : Q → (Fin m → A) → B) : Micro S P A m → P → A → Micro S P A m :=
  fun z p a =>
    match next z.1 with
    | .inl _ => z
    | .inr q =>
      let answers := Function.update z.2.1 z.2.2.1 a
      let history := (p, a) :: z.2.2.2
      if h : z.2.2.1.val + 1 < m then
        (z.1, answers, ⟨z.2.2.1.val + 1, h⟩, history)
      else
        (update z.1 q (decode q answers), (fun _ => blank), ⟨0, hm⟩, history)

private def batchSuffix {Q : Type uQ} {P : Type uP} {A : Type uA} {m : ℕ}
    (plan : Q → Fin m → P) (primitive : P → A) (q : Q) (i : ℕ) : List (P × A) :=
  ((List.ofFn (fun j : Fin m => (plan q j, primitive (plan q j)))).drop i).reverse

private theorem batchSuffix_step {Q : Type uQ} {P : Type uP} {A : Type uA} {m : ℕ}
    (plan : Q → Fin m → P) (primitive : P → A) (q : Q) (i : ℕ) (hi : i < m) :
    batchSuffix plan primitive q i = batchSuffix plan primitive q (i + 1) ++
      [(plan q ⟨i, hi⟩, primitive (plan q ⟨i, hi⟩))] := by
  unfold batchSuffix
  have hi' : i < (List.ofFn (fun j : Fin m => (plan q j, primitive (plan q j)))).length :=
    by simpa using hi
  rw [List.drop_eq_getElem_cons hi', List.reverse_cons]
  simp

private theorem fill_prefix {A : Type uA} {m : ℕ}
    (answers actual : Fin m → A) (i : Fin m)
    (hprefix : ∀ j : Fin m, j.val < i.val → answers j = actual j) :
    ∀ j : Fin m, j.val < i.val + 1 →
      Function.update answers i (actual i) j = actual j := by
  intro j hj
  by_cases hji : j = i
  · subst j
    simp
  · have hv : j.val ≠ i.val := fun h => hji (Fin.ext h)
    have hlt : j.val < i.val := by omega
    rw [Function.update_of_ne hji]
    exact hprefix j hlt

private theorem run_batch_suffix {S : Type uS} {Q : Type uQ} {A : Type uA}
    {B : Type uB} {X : Type uX} {P : Type uP}
    (m : ℕ) (hm : 0 < m) (blank : A)
    (next : S → Sum X Q) (update : S → Q → B → S)
    (primitive : P → A) (plan : Q → Fin m → P)
    (decode : Q → (Fin m → A) → B)
    (s : S) (q : Q) (hs : next s = .inr q)
    (i : Fin m) (answers : Fin m → A)
    (hprefix : ∀ j : Fin m, j.val < i.val → answers j = primitive (plan q j))
    (history : List (P × A)) (fuel : ℕ) :
    run (nextB next plan) (updateB m hm blank next update decode) primitive
        (m - i.val + fuel) (s, answers, i, history) =
      let tail := run (nextB next plan) (updateB m hm blank next update decode)
        primitive fuel
        (update s q (decode q (fun j => primitive (plan q j))), (fun _ => blank),
          ⟨0, hm⟩, batchSuffix plan primitive q i.val ++ history)
      (tail.1, tail.2 + (m - i.val)) := by
  let actual : Fin m → A := fun j => primitive (plan q j)
  let filled := Function.update answers i (actual i)
  let history' := (plan q i, primitive (plan q i)) :: history
  have hfill : ∀ j : Fin m, j.val < i.val + 1 → filled j = actual j :=
    fill_prefix answers actual i hprefix
  have hpos : 0 < m - i.val := Nat.sub_pos_of_lt i.isLt
  have hf : m - i.val + fuel = (m - i.val - 1 + fuel) + 1 := by omega
  have step :
      run (nextB next plan) (updateB m hm blank next update decode) primitive
          (m - i.val + fuel) (s, answers, i, history) =
        let tail := run (nextB next plan) (updateB m hm blank next update decode)
          primitive (m - i.val - 1 + fuel)
          (if h : i.val + 1 < m then (s, filled, ⟨i.val + 1, h⟩, history')
           else (update s q (decode q filled), (fun _ => blank), ⟨0, hm⟩, history'))
        (tail.1, tail.2 + 1) := by
    conv_lhs => rw [hf, run]
    rw [show nextB next plan (s, answers, i, history) = .inr (plan q i) by
      simp [nextB, hs]]
    simp only [updateB, hs, actual, filled, history']
  rw [step]
  by_cases hi : i.val + 1 < m
  · rw [dif_pos hi]
    have hr := run_batch_suffix m hm blank next update primitive plan decode s q hs
      ⟨i.val + 1, hi⟩ filled hfill history' fuel
    have hf' : m - i.val - 1 + fuel = m - (i.val + 1) + fuel := by omega
    have hc : m - (i.val + 1) + 1 = m - i.val := by omega
    rw [hf', hr]
    rw [batchSuffix_step plan primitive q i.val i.isLt]
    simp only [history', List.append_assoc, List.singleton_append, Nat.add_assoc, hc]
  · rw [dif_neg hi]
    have hi' : i.val + 1 = m := by omega
    have hfilled : filled = actual := by
      funext j
      exact hfill j (by omega)
    have hm' : m - i.val = 1 := by omega
    have htrace : batchSuffix plan primitive q i.val =
        [(plan q i, primitive (plan q i))] := by
      rw [batchSuffix_step plan primitive q i.val i.isLt]
      simp [batchSuffix, hi']
    rw [hfilled, htrace]
    simp only [hm', Nat.sub_self, Nat.zero_add, List.singleton_append]
    rfl
termination_by m - i.val
decreasing_by
  omega

private theorem batchSuffix_count {Q : Type uQ} {P : Type uP} {A : Type uA}
    {J : Type uJ} [DecidableEq J] {m : ℕ}
    (plan : Q → Fin m → P) (primitive : P → A) (label : P → J) (slot : Fin m → J)
    (hlabel : ∀ q i, label (plan q i) = slot i) (q : Q) (j : J) :
    (batchSuffix plan primitive q 0).countP (fun pa => decide (label pa.1 = j)) =
      (List.ofFn slot).countP (fun v => decide (v = j)) := by
  simp only [batchSuffix, List.drop_zero, List.countP_reverse]
  have hmap : (List.ofFn (fun i : Fin m => (plan q i, primitive (plan q i)))).map
      (fun pa => label pa.1) = List.ofFn slot := by
    rw [List.map_ofFn]
    congr 1
    funext i
    exact hlabel q i
  simpa only [List.countP_map, Function.comp_def] using
    congrArg (List.countP (fun v => decide (v = j))) hmap

private theorem simulate {S : Type uS} {Q : Type uQ} {A : Type uA}
    {B : Type uB} {X : Type uX} {P : Type uP} {J : Type uJ} [DecidableEq J]
    (m : ℕ) (hm : 0 < m) (blank : A)
    (next : S → Sum X Q) (update : S → Q → B → S)
    (primitive : P → A) (target : Q → B)
    (plan : Q → Fin m → P) (decode : Q → (Fin m → A) → B)
    (label : P → J) (slot : Fin m → J)
    (hdecode : ∀ q, decode q (fun i => primitive (plan q i)) = target q)
    (hlabel : ∀ q i, label (plan q i) = slot i)
    (fuel : ℕ) (s : S) (history : List (P × A)) :
    let batch := run (nextB next plan) (updateB m hm blank next update decode) primitive
      (m * fuel) (s, (fun _ => blank), ⟨0, hm⟩, history)
    let direct := run next update target fuel s
    (batch.1.1.1, batch.1.2) = direct.1 ∧
      batch.2 = m * direct.2 ∧ direct.2 ≤ fuel ∧
      ∀ j : J, batch.1.1.2.2.2.countP (fun pa => decide (label pa.1 = j)) =
        history.countP (fun pa => decide (label pa.1 = j)) +
          (List.ofFn slot).countP (fun v => decide (v = j)) * direct.2 := by
  induction fuel generalizing s history with
  | zero =>
      cases hn : next s <;> simp [run, nextB, hn]
  | succ n ih =>
      cases hn : next s with
      | inl x => simp [run, nextB, hn]
      | inr q =>
          have hd : run next update target (n + 1) s =
              let tail := run next update target n (update s q (target q))
              (tail.1, tail.2 + 1) := by rw [run, hn]
          have hb :
              run (nextB next plan) (updateB m hm blank next update decode) primitive
                  (m * (n + 1)) (s, (fun _ => blank), ⟨0, hm⟩, history) =
                let tail := run (nextB next plan) (updateB m hm blank next update decode)
                  primitive (m * n)
                  (update s q (target q), (fun _ => blank), ⟨0, hm⟩,
                    batchSuffix plan primitive q 0 ++ history)
                (tail.1, tail.2 + m) := by
            have hprefix0 : ∀ j : Fin m, j.val < (0 : ℕ) →
                (fun _ : Fin m => blank) j = primitive (plan q j) := by
              intro j hj
              omega
            have h := run_batch_suffix m hm blank next update primitive plan decode s q hn
              ⟨0, hm⟩ (fun _ => blank) hprefix0 history (m * n)
            simpa only [Fin.val_mk, Nat.sub_zero, hdecode, Nat.mul_add, Nat.mul_one,
              Nat.add_comm] using h
          have h := ih (update s q (target q)) (batchSuffix plan primitive q 0 ++ history)
          simp only [hb, hd]
          refine ⟨h.1, ?_, Nat.succ_le_succ h.2.2.1, ?_⟩
          · rw [h.2.1, Nat.mul_succ]
          · intro j
            rw [h.2.2.2 j, List.countP_append,
              batchSuffix_count plan primitive label slot hlabel q j, Nat.mul_succ]
            omega

/-- Actual fixed-size batches preserve source state and tagged output, with
exact primitive and per-label interaction counts. Decoder and slot-label
contracts are obligations to discharge inside concrete source consumers. -/
theorem batch_simulation_with_trace_and_label_costs :
∀ {S : Type uS} {Q : Type uQ} {A : Type uA} {B : Type uB}
    {X : Type uX} {P : Type uP} {J : Type uJ} [DecidableEq J]
    (m : ℕ) (hm : 0 < m) (blank : A)
    (next : S → Sum X Q) (update : S → Q → B → S)
    (primitive : P → A) (target : Q → B)
    (plan : Q → Fin m → P) (decode : Q → (Fin m → A) → B)
    (label : P → J) (slot : Fin m → J),
    (∀ q, decode q (fun i => primitive (plan q i)) = target q) →
    (∀ q i, label (plan q i) = slot i) →
    ∀ (fuel : ℕ) (s : S),
      let Micro := S × (Fin m → A) × Fin m × List (P × A)
      let nextB : Micro → Sum X P := fun z =>
        match next z.1 with
        | .inl x => .inl x
        | .inr q => .inr (plan q z.2.2.1)
      let updateB : Micro → P → A → Micro := fun z p a =>
        match next z.1 with
        | .inl _ => z
        | .inr q =>
          let answers := Function.update z.2.1 z.2.2.1 a
          let history := (p, a) :: z.2.2.2
          if h : z.2.2.1.val + 1 < m then
            (z.1, answers, ⟨z.2.2.1.val + 1, h⟩, history)
          else
            (update z.1 q (decode q answers), (fun _ => blank), ⟨0, hm⟩, history)
      let batch := run nextB updateB primitive (m * fuel)
        (s, (fun _ => blank), ⟨0, hm⟩, [])
      let direct := run next update target fuel s
      (((batch.1.1.1, batch.1.2), batch.2 / m) = direct) ∧
      batch.2 = m * direct.2 ∧
      direct.2 ≤ fuel ∧
      (∀ j : J,
        batch.1.1.2.2.2.countP (fun pa => decide (label pa.1 = j)) =
          (List.ofFn slot).countP (fun v => decide (v = j)) * direct.2)
 := by
  intro S Q A B X P J inst m hm blank next update primitive target plan decode label slot
    hdecode hlabel fuel s
  change
    let batch := run (nextB next plan) (updateB m hm blank next update decode) primitive
      (m * fuel) (s, (fun _ => blank), ⟨0, hm⟩, [])
    let direct := run next update target fuel s
    (((batch.1.1.1, batch.1.2), batch.2 / m) = direct) ∧
      batch.2 = m * direct.2 ∧ direct.2 ≤ fuel ∧
      (∀ j : J,
        batch.1.1.2.2.2.countP (fun pa => decide (label pa.1 = j)) =
          (List.ofFn slot).countP (fun v => decide (v = j)) * direct.2)
  have h := simulate m hm blank next update primitive target plan decode label slot
    hdecode hlabel fuel s []
  refine ⟨Prod.ext h.1 ?_, h.2.1, h.2.2.1, ?_⟩
  · rw [h.2.1]
    exact Nat.mul_div_cancel_left _ hm
  · intro j
    simpa only [List.countP_nil, Nat.zero_add] using h.2.2.2 j

end AutoSamplingTheory.TechnicalLemmas.Analysis.BatchedOracleSimulation
