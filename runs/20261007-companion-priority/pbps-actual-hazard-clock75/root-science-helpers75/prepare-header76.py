from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-recursive-preproof76');pre.mkdir(exist_ok=True)
old=Path('runs/20261007-companion-priority/pbps-clock-preproof75/header75.v2.proposed.lean').read_text(encoding='utf8')
start=old.index('    {E : Type*}');end=old.index(' : Prop :=',start);binders=old[start:end]
defs=old[old.index('    let c :'):old.index('    let W :')]
anchor='    let rate :'
sdef='''    let S : E → (E × E) → (E × E) := fun xRef z =>
      (z.1, z.2 - (2 * inner ℝ z.2 (gradient V z.1 - gradient V xRef) /
        ‖gradient V z.1 - gradient V xRef‖ ^ 2) • (gradient V z.1 - gradient V xRef))
'''
defs=defs.replace(anchor,sdef+anchor,1)
extra='''    let next : E → E → ℝ≥0 → ((ℝ≥0 × (E × E)) ⊕ Unit) →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef e r =>
      match r with
      | Sum.inr _ => Sum.inr ()
      | Sum.inl a =>
        if τ y xRef a.2 e = ⊤ then Sum.inr () else
          Sum.inl (a.1 + (τ y xRef a.2 e).untopD 0,
            S xRef (Φ y xRef ((τ y xRef a.2 e).untopD 0 : ℝ) a.2))
    let record : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef z₀ e n =>
      Nat.rec (Sum.inl (0, z₀)) (fun k r => next y xRef (e k) r) n
    let eventTime : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ e n => (record y xRef z₀ e n).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0,
      record y xRef z₀ e 0 = Sum.inl (0, z₀)) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0, ∀ n : ℕ,
      record y xRef z₀ e (n + 1) = next y xRef (e n) (record y xRef z₀ e n) ∧
      (∀ a : ℝ≥0 × (E × E), record y xRef z₀ e n = Sum.inl a →
        (record y xRef z₀ e (n + 1) = Sum.inr () ↔ τ y xRef a.2 (e n) = ⊤) ∧
        (τ y xRef a.2 (e n) ≠ ⊤ → record y xRef z₀ e (n + 1) =
          Sum.inl (a.1 + (τ y xRef a.2 (e n)).untopD 0,
            S xRef (Φ y xRef ((τ y xRef a.2 (e n)).untopD 0 : ℝ) a.2))))) ∧
    Measurable (fun a : (E × E) × ℝ≥0 × ((ℝ≥0 × (E × E)) ⊕ Unit) =>
      next a.1.1 a.1.2 a.2.1 a.2.2) ∧
    (∀ n : ℕ, Measurable (fun a : (E × E) × (E × E) × (ℕ → ℝ≥0) =>
      record a.1.1 a.1.2 a.2.1 a.2.2 n)) ∧
    (∀ n : ℕ, Measurable (fun a : (E × E) × (E × E) × (ℕ → ℝ≥0) =>
      eventTime a.1.1 a.1.2 a.2.1 a.2.2 n)) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0,
      eventTime y xRef z₀ e 0 = 0 ∧ Monotone (eventTime y xRef z₀ e)) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0, ∀ n k : ℕ,
      record y xRef z₀ e n = Sum.inr () →
        record y xRef z₀ e (n + k) = Sum.inr ()) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0, ∀ n : ℕ,
      ∀ a : ℝ≥0 × (E × E), record y xRef z₀ e n = Sum.inl a →
        H y xRef a.2 = H y xRef z₀ ∧
        ∀ t : ℝ≥0, (t : WithTop ℝ≥0) < τ y xRef a.2 (e n) →
          H y xRef (Φ y xRef (t : ℝ) a.2) = H y xRef z₀ ∧
          0 ≤ rate xRef (Φ y xRef (t : ℝ) a.2) ∧
          rate xRef (Φ y xRef (t : ℝ) a.2) ≤ C y xRef z₀) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0,
      0 ≤ C y xRef z₀ ∧
      (0 < C y xRef z₀ → ∀ n : ℕ,
        eventTime y xRef z₀ e n +
          (Real.toNNReal ((e n : ℝ) / C y xRef z₀) : WithTop ℝ≥0) ≤
        eventTime y xRef z₀ e (n + 1)) ∧
      (C y xRef z₀ = 0 → ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E),
        record y xRef z₀ e n = Sum.inl a → 0 < e n →
          record y xRef z₀ e (n + 1) = Sum.inr ())) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0, ∀ n : ℕ,
      ∀ a : ℝ≥0 × (E × E), record y xRef z₀ e n = Sum.inl a →
        (e n = 0 → record y xRef z₀ e (n + 1) = Sum.inl (a.1, S xRef a.2)) ∧
        (∀ b : ℝ≥0 × (E × E), 0 < e n →
          record y xRef z₀ e (n + 1) = Sum.inl b → a.1 < b.1))
'''
prefix='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock
import Mathlib.MeasureTheory.Constructions.BorelSpace.WithTop

/-! Prospective header76 only: actual finite stopped postjump recursion.
Active records are Sum.inl (finite time, phase); Sum.inr () means stopped,
has event time infinity and carries no phase at infinity. Threshold e n is
source E_(n+1). Zero thresholds are a deterministic extension; no global
physical-time phase or iid/nonexplosion/Markov/invariance is asserted. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion
open InnerProductSpace MeasureTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

'''
text=prefix+'private def actual_fixed_reference_finite_jump_recursion_statement\n'+binders+' : Prop :=\n'+defs+extra+'\ntheorem actual_fixed_reference_finite_jump_recursion\n'+binders+' :\n    actual_fixed_reference_finite_jump_recursion_statement hα hαβ hV hH hη hβη := by\n'
p=pre/'header76.proposed.lean';assert not p.exists();p.write_text(text,encoding='utf8',newline='\n')
manifest=dict(status='PROSPECTIVE_HEADER_ONLY_NOT_SEALED_NOT_IMPLEMENTED',actual_root_PID=os.getpid(),header=dict(path=p.as_posix(),RAW_bytes=p.stat().st_size,RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest()),definitions=11,original_analytic_callers=6,conclusion_groups=10,representation='(NNReal × phase) ⊕ Unit: active left, stopped right. Native sum measurable structure; no phase at infinity.',threshold_index='e n = source E_(n+1)',true_parent75='Focused compiled and independently mathematically checked; fresh source admission pending. No implementation/claim before admission.',new_mathematics='Produced actual stopped recursion, joint Borel, original-energy invariant, monotone event times and uniform actual waiting increment; no assumed state/cap/provider.',source_plan='runs/20261007-companion-priority/pbps-recursive-path-preread76/selected.contract.json',proof_search=False,SAU=False,PROVED_LOCAL=False,VERIFIED=False)
q=pre/'header76.proposal.json';assert not q.exists();q.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('PASS76 prospective eleven-definition ten-clause header authored only; mathematical/source header review and seal pending.')
