"""Create the sole owned proof module after its exact Statement Seal."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
PRE = RUN.parent / "pbps-next-history-extension-preread90"
header = (PRE / "header90.v2.proposed.lean").read_text(encoding="utf-8")
seal = json.loads((RUN / "root.statement-seal90.json").read_bytes())
assert hashlib.sha256((PRE / "header90.v2.proposed.lean").read_bytes()).hexdigest() == seal["header"]["raw_sha256"]
prefix, statement = header.split("private def ", 1)
statement = statement.split("\nend", 1)[0].rstrip()
binders = statement[statement.index("\n    {E :"):statement.index(" : Prop :=")]
definitions = statement[statement.index("    let c :"):statement.index("    ∀ y xRef :")]
conclusion = statement[statement.index("    ∀ y xRef :"):]
local_defs = "\n".join(line[2:] if line.startswith("  ") else line for line in definitions.splitlines())
body = r"""
  have hdensity := ActualConditionalNextWaitDensity.actual_conditional_next_wait_density
    hα hαβ hV hH hη hβη
  have hhistory := ActualFiniteHistoryTailLaw.actual_finite_history_tail_law
    hα hαβ hV hH hη hβη
  have hflow := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hbounce := ActualBounceRate.actual_bounce_rate_energy_laws hα hαβ hV hH hη hβη
  intro y xRef z₀ n
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist := Fin (n + 1) → Rec
  let HistNext := Fin (n + 2) → Rec
  let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
  let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
  let Hnext : (ℕ → ℝ) → HistNext := history y xRef z₀ (n + 1)
  let append : Hist × ℝ → HistNext := fun p =>
    Fin.snoc p.1 (match p.1 last with
      | Sum.inl a => Sum.inl (a.1 + Real.toNNReal p.2,
          S xRef (Φ y xRef p.2 a.2))
      | Sum.inr _ => Sum.inr ())
  let lift : Hist × ℝ → HistNext × ℝ := fun p => (append p, p.2)
  change Measurable Hnext ∧ Measurable append ∧ Measurable lift ∧
    (∀ p : Hist × ℝ, ∀ j : Fin (n + 1), append p j.castSucc = p.1 j) ∧ _
  -- Borel actual histories and the source's zero-safe flow/reflection constructor.
  have hH : Measurable H := (hhistory y xRef z₀ n).1
  have hHnext : Measurable Hnext := (hhistory y xRef z₀ (n + 1)).1
  let update : Rec × ℝ → Rec := fun q => match q.1 with
    | Sum.inl a => Sum.inl (a.1 + Real.toNNReal q.2, S xRef (Φ y xRef q.2 a.2))
    | Sum.inr _ => Sum.inr ()
  have hupdate : Measurable update := by
    let e := MeasurableEquiv.sumProdDistrib (ℝ≥0 × (E × E)) Unit ℝ
    have hφ : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ => Φ y xRef q.2 q.1.2) :=
      hflow.1.measurable.comp (f := fun q : (ℝ≥0 × (E × E)) × ℝ =>
        ((y, xRef), q.2, q.1.2))
        (measurable_const.prodMk (measurable_snd.prodMk measurable_fst.snd))
    have hS : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ =>
        S xRef (Φ y xRef q.2 q.1.2)) :=
      hbounce.1.comp ((measurable_const : Measurable
        (fun _ : (ℝ≥0 × (E × E)) × ℝ => xRef)).prodMk hφ)
    have hl : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ =>
        (Sum.inl (q.1.1 + Real.toNNReal q.2, S xRef (Φ y xRef q.2 q.1.2)) : Rec)) :=
      measurable_inl.comp ((measurable_fst.fst.add
        (measurable_real_toNNReal.comp measurable_snd)).prodMk hS)
    have heq : update = (Sum.elim
        (fun q : (ℝ≥0 × (E × E)) × ℝ =>
          (Sum.inl (q.1.1 + Real.toNNReal q.2, S xRef (Φ y xRef q.2 q.1.2)) : Rec))
        (fun _ : Unit × ℝ => (Sum.inr () : Rec))) ∘ e := by
      funext q
      rcases q with ⟨a | a, s⟩ <;> rfl
    rw [heq]
    exact (hl.sumElim (measurable_const : Measurable
      (fun _ : Unit × ℝ => (Sum.inr () : Rec)))).comp e.measurable
  have hnew : Measurable (fun p : Hist × ℝ => update (p.1 last, p.2)) :=
    hupdate.comp (((measurable_pi_apply last).comp measurable_fst).prodMk measurable_snd)
  have happend : Measurable append := by
    apply measurable_pi_lambda
    intro j
    refine Fin.lastCases ?_ (fun i => ?_) j
    · simpa only [append, Fin.snoc_last] using hnew
    · simpa only [append, Fin.snoc_castSucc] using
        ((measurable_pi_apply i).comp (measurable_fst : Measurable (fun p : Hist × ℝ => p.1)))
  have hlift : Measurable lift := happend.prodMk measurable_snd
  have hprefix (p : Hist × ℝ) (j : Fin (n + 1)) : append p j.castSucc = p.1 j := by
    exact Fin.snoc_castSucc
  refine ⟨hHnext, happend, hlift, hprefix, ?_⟩
  intro d hd
  let μ : Measure Hist := Measure.map H P
  let D : Hist → ℝ → ℝ≥0∞ := fun h s =>
    if 0 < s ∧ s < (d h : ℝ) then density y xRef (h last, s) else 0
  let B : Set (ℕ → ℝ) := {w |
    (0 : WithTop ℝ≥0) < waitObs y xRef (record y xRef z₀ (ε w) n, w n) ∧
    waitObs y xRef (record y xRef z₀ (ε w) n, w n) <
      ((d (H w) : ℝ≥0) : WithTop ℝ≥0)}
  let X : (ℕ → ℝ) → Hist × ℝ := fun w =>
    (H w, timeObs y xRef (record y xRef z₀ (ε w) n, w n))
  let Y : (ℕ → ℝ) → HistNext × ℝ := fun w =>
    (Hnext w, timeObs y xRef (record y xRef z₀ (ε w) n, w n))
  let ν : Measure (Hist × ℝ) := (μ.prod (volume : Measure ℝ)).withDensity
    (fun p => D p.1 p.2)
  change MeasurableSet B ∧ Measurable Y ∧
    (∀ w ∈ B, Hnext w = append (X w)) ∧
    Measure.map Y (P.restrict B) = Measure.map lift ν ∧
    Measure.map Hnext (P.restrict B) = Measure.map append ν ∧
    (Measure.map lift ν) Set.univ ≤ 1 ∧
    (∀ F : HistNext × ℝ → ℝ≥0∞, Measurable F →
      Measurable (fun h => ∫⁻ s : ℝ, F (lift (h, s)) * D h s) ∧
      (∀ A : Set Hist, MeasurableSet A →
        (∫⁻ w in B ∩ H ⁻¹' A, F (Y w) ∂P) =
          ∫⁻ h in A, (∫⁻ s : ℝ, F (lift (h, s)) * D h s) ∂μ))
  have h89 := (hdensity y xRef z₀ n).2.2.2 d hd
  have hB : MeasurableSet B := h89.2.2.2.2.1
  have hX : Measurable X := h89.2.2.2.2.2.1
  have hXlaw : Measure.map X (P.restrict B) = ν := h89.2.2.2.2.2.2.1
  have hνmass : ν Set.univ ≤ 1 := h89.2.2.2.2.2.2.2.1
  have htests := h89.2.2.2.2.2.2.2.2
  have hY : Measurable Y := hHnext.prodMk hX.snd
  -- The positive finite guard identifies the source recursion pointwise.
  have hactual (w : ℕ → ℝ) (hw : w ∈ B) : Hnext w = append (X w) := by
    rcases hrec : record y xRef z₀ (ε w) n with a | a
    · have hfinite : τ y xRef a.2 (Real.toNNReal (w n)) ≠ ⊤ := by
        intro ht
        have hupper := hw.2
        simp only [waitObs, hrec, ht] at hupper
        exact (not_lt_of_ge le_top) hupper
      funext j
      refine Fin.lastCases ?_ (fun i => ?_) j
      · simp only [append, Fin.snoc_last]
        change next y xRef (ε w n) (record y xRef z₀ (ε w) n) = _
        simp [next, hrec, hfinite, H, history, last, X, timeObs, waitObs, ε]
      · simp only [append, Fin.snoc_castSucc]
        rfl
    · have hpositive := hw.1
      simp only [waitObs, hrec, lt_self_iff_false] at hpositive
  have hYactual (w : ℕ → ℝ) (hw : w ∈ B) : Y w = lift (X w) :=
    Prod.ext (hactual w hw) rfl
  -- Compose the exact89 joint measure law; the event is never normalized.
  have hjoint : Measure.map Y (P.restrict B) = Measure.map lift ν := by
    rw [← hXlaw, Measure.map_map hlift hX]
    exact Measure.map_congr (ae_restrict_of_forall_mem hB hYactual)
  have hmarginal : Measure.map Hnext (P.restrict B) = Measure.map append ν := by
    rw [← hXlaw, Measure.map_map happend hX]
    exact Measure.map_congr (ae_restrict_of_forall_mem hB hactual)
  have hmass : (Measure.map lift ν) Set.univ ≤ 1 := by
    rw [Measure.map_apply hlift MeasurableSet.univ, Set.preimage_univ]
    exact hνmass
  refine ⟨hB, hY, hactual, hjoint, hmarginal, hmass, ?_⟩
  -- All joint ENNReal tests, including infinity and null old-history events.
  intro F hF
  have htest := htests (F ∘ lift) (hF.comp hlift)
  refine ⟨htest.1, ?_⟩
  intro A hA
  calc
    (∫⁻ w in B ∩ H ⁻¹' A, F (Y w) ∂P) =
        ∫⁻ w in B ∩ H ⁻¹' A, (F ∘ lift) (X w) ∂P := by
      apply setLIntegral_congr_fun (hB.inter (hA.preimage hH))
      intro w hw
      exact congrArg F (hYactual w hw.1)
    _ = ∫⁻ h in A, (∫⁻ s : ℝ, F (lift (h, s)) * D h s) ∂μ := htest.2 A hA
"""
result = prefix.replace("Prospective statement only:", "Actual source-implicit completion:") + "private def " + statement + "\n\n"
result += "set_option maxHeartbeats 1600000 in\ntheorem actual_finite_history_extension" + binders
result += " :\n    actual_finite_history_extension_statement hα hαβ hV hH hη hβη := by\n  classical\n"
result += local_defs + "\n  change\n" + conclusion + body
result += "\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension\n"
target = ROOT / "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean"
assert not target.exists()
target.write_text(result, encoding="utf-8", newline="\n")
print("Created sealed sole-owner actual90 proof module; no compilation/review credit.")
