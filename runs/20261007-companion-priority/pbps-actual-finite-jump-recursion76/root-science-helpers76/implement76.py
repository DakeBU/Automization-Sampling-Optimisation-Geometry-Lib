from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-recursive-preproof76')
seal=json.loads((pre/'root.statement-seal76.json').read_bytes())
h=(pre/'header76.v3.proposed.lean').read_bytes()
assert hashlib.sha256(h).hexdigest()==seal['header']['RAW_sha256']
s=h.decode('utf8').replace('\r\n','\n')
start=s.index('    let c :')
end=s.index('    (∀ y xRef : E, ∀ z₀',start)
defs='\n'.join(x[2:] for x in s[start:end].rstrip().splitlines())+'\n'
target=s[end:s.index('\ntheorem actual_fixed_reference',end)].rstrip()
target='\n'.join(x[2:] for x in target.splitlines())+'\n'
proof=r'''
  have hf := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hb := ActualBounceRate.actual_bounce_rate_energy_laws hα hαβ hV hH hη hβη
  have hk := ActualHazardClock.actual_integrated_hazard_clock_laws hα hαβ hV hH hη hβη
  have hΦmeas : Measurable (fun a : (E × E) × ℝ × (E × E) =>
      Φ a.1.1 a.1.2 a.2.1 a.2.2) := hf.2.1
  have hΦzero (y xRef : E) (z : E × E) : Φ y xRef 0 z = z := hf.2.2.1 y xRef z
  have hΦH (y xRef : E) (t : ℝ) (z : E × E) :
      H y xRef (Φ y xRef t z) = H y xRef z := hf.2.2.2.2.2.2.2.1 y xRef t z
  have hSmeas : Measurable (fun a : E × (E × E) => S a.1 a.2) := hb.1
  have hSH (y xRef : E) (z : E × E) : H y xRef (S xRef z) = H y xRef z :=
    hb.2.2.2.2.2.2.1 y xRef z
  have hrate0 (xRef : E) (z : E × E) : 0 ≤ rate xRef z :=
    (hb.2.2.2.2.2.2.2.1 xRef z).1
  have hratecap (y xRef : E) (z₀ z : E × E) (hz : H y xRef z = H y xRef z₀) :
      rate xRef z ≤ C y xRef z₀ :=
    ((hb.2.2.2.2.2.2.2.2.2 y xRef z₀).2 z hz).2.2
  have hτpositive (y xRef : E) (z : E × E) (e : ℝ≥0) :
      0 < e → (0 : WithTop ℝ≥0) < τ y xRef z e :=
    (hk.2.2.2.2.2.1 y xRef z e).2.2.1
  have hτzero (y xRef : E) (z : E × E) : τ y xRef z 0 = 0 :=
    (hk.2.2.2.2.2.1 y xRef z 0).2.2.2
  have hτmeas : Measurable (fun a : (E × E) × (E × E) × ℝ≥0 =>
      τ a.1.1 a.1.2 a.2.1 a.2.2) := hk.2.2.2.2.2.2.1
  have hC0 (y xRef : E) (z : E × E) : 0 ≤ C y xRef z :=
    (hk.2.2.2.2.2.2.2.2.1 y xRef z).1
  have hwait (y xRef : E) (z : E × E) (e : ℝ≥0) :
      (0 < C y xRef z →
        (Real.toNNReal ((e : ℝ) / C y xRef z) : WithTop ℝ≥0) ≤ τ y xRef z e) ∧
      (C y xRef z = 0 → 0 < e → τ y xRef z e = ⊤) :=
    hk.2.2.2.2.2.2.2.2.2 y xRef z e
  have hrec0 (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0) :
      record y xRef z₀ e 0 = Sum.inl (0, z₀) := rfl
  have hrecstep (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0) (n : ℕ) :
      record y xRef z₀ e (n + 1) = next y xRef (e n) (record y xRef z₀ e n) := rfl
  have hbranches (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0) (n : ℕ)
      (a : ℝ≥0 × (E × E)) (ha : record y xRef z₀ e n = Sum.inl a) :
      (record y xRef z₀ e (n + 1) = Sum.inr () ↔ τ y xRef a.2 (e n) = ⊤) ∧
      (τ y xRef a.2 (e n) ≠ ⊤ → record y xRef z₀ e (n + 1) =
        Sum.inl (a.1 + (τ y xRef a.2 (e n)).untopD 0,
          S xRef (Φ y xRef (((τ y xRef a.2 (e n)).untopD 0 : ℝ≥0) : ℝ) a.2))) := by
    rw [hrecstep, ha]
    dsimp only [next]
    split_ifs with ht <;> simp [ht]
  have hnextmeas : Measurable
      (fun a : (E × E) × ℝ≥0 × ((ℝ≥0 × (E × E)) ⊕ Unit) =>
        next a.1.1 a.1.2 a.2.1 a.2.2) := by
    let g : ((E × E) × ℝ≥0) × (ℝ≥0 × (E × E)) →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun a =>
      if τ a.1.1.1 a.1.1.2 a.2.2 a.1.2 = ⊤ then Sum.inr () else
        Sum.inl (a.2.1 + (τ a.1.1.1 a.1.1.2 a.2.2 a.1.2).untopD 0,
          S a.1.1.2 (Φ a.1.1.1 a.1.1.2
            (((τ a.1.1.1 a.1.1.2 a.2.2 a.1.2).untopD 0 : ℝ≥0) : ℝ) a.2.2))
    have ht : Measurable (fun a : ((E × E) × ℝ≥0) × (ℝ≥0 × (E × E)) =>
        τ a.1.1.1 a.1.1.2 a.2.2 a.1.2) :=
      hτmeas.comp (measurable_fst.fst.prodMk
        (measurable_snd.snd.prodMk measurable_fst.snd))
    have hq := ht.untopD (0 : ℝ≥0)
    have hp := hΦmeas.comp (measurable_fst.fst.prodMk
      ((measurable_coe_nnreal_real.comp hq).prodMk measurable_snd.snd))
    have hs := hSmeas.comp (measurable_fst.fst.snd.prodMk hp)
    have hg : Measurable g := measurable_const.ite
      (measurableSet_eq_fun ht measurable_const)
      (measurable_inl.comp ((measurable_snd.fst.add hq).prodMk hs))
    have hsum := hg.sumElim
      (show Measurable (fun _ : ((E × E) × ℝ≥0) × Unit =>
        (Sum.inr () : (ℝ≥0 × (E × E)) ⊕ Unit)) from measurable_const)
    have hm := hsum.comp ((MeasurableEquiv.prodSumDistrib
      ((E × E) × ℝ≥0) (ℝ≥0 × (E × E)) Unit).measurable.comp
      ((measurable_fst.prodMk measurable_snd.fst).prodMk measurable_snd.snd))
    convert hm using 1
    funext a
    cases a.2.2 <;> rfl
  have hrecordmeas (n : ℕ) : Measurable
      (fun a : (E × E) × (E × E) × (ℕ → ℝ≥0) =>
        record a.1.1 a.1.2 a.2.1 a.2.2 n) := by
    induction n with
    | zero => exact measurable_inl.comp (measurable_const.prodMk measurable_snd.fst)
    | succ n ih =>
      exact hnextmeas.comp (measurable_fst.prodMk
        (((measurable_pi_apply n).comp measurable_snd.snd).prodMk ih))
  have htimemeas (n : ℕ) : Measurable
      (fun a : (E × E) × (E × E) × (ℕ → ℝ≥0) =>
        eventTime a.1.1 a.1.2 a.2.1 a.2.2 n) :=
    ((WithTop.measurable_coe.comp measurable_fst).sumElim measurable_const).comp
      (hrecordmeas n)
  have henergy (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0) (n : ℕ)
      (a : ℝ≥0 × (E × E)) (ha : record y xRef z₀ e n = Sum.inl a) :
      H y xRef a.2 = H y xRef z₀ := by
    induction n generalizing a with
    | zero =>
      have heq : (0, z₀) = a := Sum.inl.inj ha
      subst a
      rfl
    | succ n ih =>
      rw [hrecstep] at ha
      cases hr : record y xRef z₀ e n with
      | inr u => simp [hr, next] at ha
      | inl b =>
        rw [hr] at ha
        dsimp only [next] at ha
        split_ifs at ha with ht
        · cases ha
        · have heq := Sum.inl.inj ha
          rw [← heq]
          exact (hSH y xRef _).trans ((hΦH y xRef _ _).trans (ih b hr))
  have hmono (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0) :
      Monotone (eventTime y xRef z₀ e) := by
    apply monotone_nat_of_le_succ
    intro n
    dsimp only [eventTime]
    rw [hrecstep]
    cases hr : record y xRef z₀ e n with
    | inr u => simp [next]
    | inl a =>
      dsimp only [next]
      split_ifs with ht
      · exact le_top
      · exact WithTop.coe_le_coe.mpr (le_add_of_nonneg_right (zero_le _))
  have hstopped (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0) (n k : ℕ)
      (hn : record y xRef z₀ e n = Sum.inr ()) :
      record y xRef z₀ e (n + k) = Sum.inr () := by
    induction k with
    | zero => simpa using hn
    | succ k ih => simpa only [Nat.add_succ, hrecstep, ih, next]
  have harcs (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0) (n : ℕ)
      (a : ℝ≥0 × (E × E)) (ha : record y xRef z₀ e n = Sum.inl a) :
      H y xRef a.2 = H y xRef z₀ ∧
      ∀ t : ℝ≥0, (t : WithTop ℝ≥0) < τ y xRef a.2 (e n) →
        H y xRef (Φ y xRef (t : ℝ) a.2) = H y xRef z₀ ∧
        0 ≤ rate xRef (Φ y xRef (t : ℝ) a.2) ∧
        rate xRef (Φ y xRef (t : ℝ) a.2) ≤ C y xRef z₀ := by
    have hEa := henergy y xRef z₀ e n a ha
    refine ⟨hEa, fun t _ => ?_⟩
    have hEt := (hΦH y xRef t a.2).trans hEa
    exact ⟨hEt, hrate0 xRef _, hratecap y xRef z₀ _ hEt⟩
  have hcap_eq (y xRef : E) (z₀ z : E × E) (hz : H y xRef z = H y xRef z₀) :
      C y xRef z = C y xRef z₀ := by simp only [C, hz]
  have hincrement (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0)
      (hC : 0 < C y xRef z₀) (n : ℕ) :
      eventTime y xRef z₀ e n +
        (Real.toNNReal ((e n : ℝ) / C y xRef z₀) : WithTop ℝ≥0) ≤
      eventTime y xRef z₀ e (n + 1) := by
    cases hr : record y xRef z₀ e n with
    | inr u => simp [eventTime, hrecstep, hr, next]
    | inl a =>
      have hCa := hcap_eq y xRef z₀ a.2 (henergy y xRef z₀ e n a hr)
      have hw := (hwait y xRef a.2 (e n)).1 (by simpa only [hCa] using hC)
      rw [hCa] at hw
      dsimp only [eventTime]
      rw [hrecstep, hr]
      dsimp only [next]
      split_ifs with ht
      · exact le_top
      · have hq : (((τ y xRef a.2 (e n)).untopD 0 : ℝ≥0) : WithTop ℝ≥0) =
            τ y xRef a.2 (e n) := by
          induction hτ : τ y xRef a.2 (e n) using WithTop.recTopCoe with
          | top => exact False.elim (ht hτ)
          | coe q => simp
        change (a.1 : WithTop ℝ≥0) + _ ≤
          ((a.1 + (τ y xRef a.2 (e n)).untopD 0 : ℝ≥0) : WithTop ℝ≥0)
        rw [WithTop.coe_add, hq]
        exact add_le_add_left hw _
  have hzerocap (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0)
      (hC : C y xRef z₀ = 0) (n : ℕ) (a : ℝ≥0 × (E × E))
      (ha : record y xRef z₀ e n = Sum.inl a) (he : 0 < e n) :
      record y xRef z₀ e (n + 1) = Sum.inr () := by
    apply (hbranches y xRef z₀ e n a ha).1.mpr
    apply (hwait y xRef a.2 (e n)).2 _ he
    exact (hcap_eq y xRef z₀ a.2 (henergy y xRef z₀ e n a ha)).trans hC
  have hzeroevent (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0) (n : ℕ)
      (a : ℝ≥0 × (E × E)) (ha : record y xRef z₀ e n = Sum.inl a)
      (he : e n = 0) :
      record y xRef z₀ e (n + 1) = Sum.inl (a.1, S xRef a.2) := by
    rw [hrecstep, ha]
    simp only [next, he, hτzero, WithTop.zero_ne_top, ↓reduceIte,
      WithTop.untopD_coe, add_zero, NNReal.coe_zero, hΦzero]
  have hstrictevent (y xRef : E) (z₀ : E × E) (e : ℕ → ℝ≥0) (n : ℕ)
      (a : ℝ≥0 × (E × E)) (ha : record y xRef z₀ e n = Sum.inl a)
      (b : ℝ≥0 × (E × E)) (he : 0 < e n)
      (hb : record y xRef z₀ e (n + 1) = Sum.inl b) : a.1 < b.1 := by
    have ht : τ y xRef a.2 (e n) ≠ ⊤ := by
      intro ht
      have hs := (hbranches y xRef z₀ e n a ha).1.mpr ht
      rw [hb] at hs
      cases hs
    have hq : 0 < (τ y xRef a.2 (e n)).untopD 0 := by
      have hp := hτpositive y xRef a.2 (e n) he
      induction hτ : τ y xRef a.2 (e n) using WithTop.recTopCoe with
      | top => exact False.elim (ht hτ)
      | coe q => simpa only [hτ, WithTop.untopD_coe, ← WithTop.coe_zero,
          WithTop.coe_lt_coe] using hp
    have hupdate := (hbranches y xRef z₀ e n a ha).2 ht
    rw [hb] at hupdate
    have heq := Sum.inl.inj hupdate
    have hbtime := congrArg Prod.fst heq
    rw [hbtime]
    exact lt_add_of_pos_right _ hq
  exact ⟨hrec0, fun y xRef z₀ e n =>
    ⟨hrecstep y xRef z₀ e n, hbranches y xRef z₀ e n⟩,
    hnextmeas, hrecordmeas, htimemeas,
    fun y xRef z₀ e => ⟨rfl, hmono y xRef z₀ e⟩, hstopped, harcs,
    fun y xRef z₀ e => ⟨hC0 y xRef z₀, hincrement y xRef z₀ e,
      hzerocap y xRef z₀ e⟩,
    fun y xRef z₀ e n a ha => ⟨hzeroevent y xRef z₀ e n a ha,
      hstrictevent y xRef z₀ e n a ha⟩⟩
'''
s=s.replace('import Mathlib.MeasureTheory.Constructions.BorelSpace.WithTop\n','import Mathlib.MeasureTheory.Constructions.BorelSpace.WithTop\nimport Mathlib.MeasureTheory.MeasurableSpace.Embedding\n')
s=s.replace('theorem actual_fixed_reference_finite_jump_recursion\n','set_option maxHeartbeats 1600000 in\ntheorem actual_fixed_reference_finite_jump_recursion\n')
out=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean')
assert not out.exists()
out.write_text(s+defs+'  change\n'+target+proof+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion\n',encoding='utf8',newline='\n')
print('PASS76 first complete literal implementation written; focused compilation remains pending, no theorem credit.')
