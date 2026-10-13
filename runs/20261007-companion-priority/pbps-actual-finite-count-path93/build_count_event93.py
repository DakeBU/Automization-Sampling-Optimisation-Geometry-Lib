from pathlib import Path
run=Path(__file__).resolve().parent
header=(run.parent/'pbps-finite-count-path-preread93/Header93.lean').read_text(encoding='utf8')
sig=header.split('def candidate_finite_count_path_statement',1)[1].split(' : Prop := by',1)[0]
lets=header.split('  exact\n',1)[1].split('    let Path :',1)[0]
base=(run/'ActualEndpointNullity93.lean').read_text(encoding='utf8').rsplit('\nend\nend EndpointInterfaces93',1)[0]
count=(run/'CountInterfaces93.lean').read_text(encoding='utf8')
helpers=count[count.index('private theorem find_decidable_eq'):count.index('set_option maxHeartbeats')]
path=(run/'ActualPathIdentification93.lean').read_text(encoding='utf8')
term=path[path.index('private theorem terminal_event_after'):path.index('set_option maxHeartbeats',path.index('private theorem terminal_event_after'))]
conclusion='''    ∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,
      (∀ n : ℕ, ∀ w ∈ C y xRef z₀ n T, w ∈ I y xRef z₀ T n) ∧
      (∀ᵐ w ∂P, (∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)) ∧
        (∀ k : ℕ, N y xRef z₀ T w = k ↔ w ∈ C y xRef z₀ k T) ∧
        {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.Finite ∧
        {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.Finite ∧
        N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.ncard ∧
        N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.ncard) ∧
      (Pairwise fun i j : ℕ => Disjoint (C y xRef z₀ i T) (C y xRef z₀ j T)) ∧
      P (⋃ k : ℕ, C y xRef z₀ k T) = 1'''
body='''
  intro y xRef z₀ T
  have h76 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
    hα hαβ hV hH hη hβη
  have hmono (w : ℕ → ℝ) : Monotone (eventTime y xRef z₀ w) :=
    (h76.2.2.2.2.2.1 y xRef z₀ (ε w)).2
  have hraw : ∀ n : ℕ, ∀ w ∈ C y xRef z₀ n T, w ∈ I y xRef z₀ T n := by
    intro n w hw
    obtain ⟨a, ha⟩ := hw.1.1 (Fin.last n)
    change record y xRef z₀ (ε w) n = Sum.inl a at ha
    have htime : a.1 ≤ T := by
      cases n with
      | zero =>
        have hz : (0 : ℝ≥0) = a.1 := congrArg Prod.fst (Sum.inl.inj ha)
        rw [← hz]; exact zero_le
      | succ n =>
        have ht := hw.1.2.2 (Fin.last n)
        change readTime (record y xRef z₀ (ε w) (n+1)) < (T : ℝ) at ht
        rw [ha] at ht
        exact (NNReal.coe_lt_coe.mp ht).le
    have hsurv : ((T - a.1 : ℝ≥0) : WithTop ℝ≥0) < τ y xRef a.2 (ε w n) := by
      have hh := hw.2
      change survival y xRef (record y xRef z₀ (ε w) n)
        (T - liveTime (record y xRef z₀ (ε w) n)) (w n) at hh
      rw [ha] at hh
      exact hh
    constructor
    · change (record y xRef z₀ (ε w) n).elim _ _ ≤ _
      rw [ha]; exact WithTop.coe_le_coe.mpr htime
    · have hnext : eventTime y xRef z₀ w (n+1) =
          (if τ y xRef a.2 (ε w n) = ⊤ then ⊤ else
            ((a.1 + (τ y xRef a.2 (ε w n)).untopD 0 : ℝ≥0) : WithTop ℝ≥0)) := by
        change (next y xRef (ε w n) (record y xRef z₀ (ε w) n)).elim _ _ = _
        rw [ha]; dsimp only [next]; split_ifs <;> rfl
      rw [hnext]
      exact terminal_event_after T a.1 (τ y xRef a.2 (ε w n)) hsurv
  have hgood := AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.2.2.2.1
  have hcover := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover
    hα hαβ hV hH hη hβη y xRef z₀
  have hno := actual_fixed_horizon_endpoint_nullity hα hαβ hV hH hη hβη y xRef z₀ T
  have hAE : ∀ᵐ w ∂P,
      (∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)) ∧
      (∃ k, w ∈ I y xRef z₀ T k) ∧
      (∀ k, w ∈ I y xRef z₀ T k ↔ w ∈ C y xRef z₀ k T) := by
    filter_upwards [hgood, hcover, hno] with w hw hc hn
    refine ⟨hn, (hc.1 T).exists, ?_⟩
    intro k
    refine ⟨?_, hraw k w⟩
    intro hi
    have hstrict (l : ℕ) (a b : ℝ≥0 × (E × E))
        (ha : record y xRef z₀ (ε w) l = Sum.inl a)
        (hb : record y xRef z₀ (ε w) (l+1) = Sum.inl b) : a.1 < b.1 :=
      (h76.2.2.2.2.2.2.2.2.2 y xRef z₀ (ε w) l a ha).2 b
        (Real.toNNReal_pos.mpr (hw l).1) hb
    have hg := live_prefix_strict_guard (record y xRef z₀ (ε w)) (hmono w) hstrict k (T+1)
      (lt_of_le_of_lt hi.1 (WithTop.coe_lt_coe.mpr (lt_add_one T)))
    have heq (r : Rec) : readTime r = r.elim (fun a => (a.1 : ℝ)) (fun _ => 0) := by
      cases r <;> rfl
    refine ⟨⟨hg.1, ?_, ?_⟩, ?_⟩
    · simpa only [history, heq] using hg.2.1
    · intro j
      have hjle : eventTime y xRef z₀ w j.succ.val ≤ (T : WithTop ℝ≥0) :=
        le_trans (hmono w (Nat.le_of_lt_succ j.succ.isLt)) hi.1
      have hjlt := lt_of_le_of_ne hjle (hn j.succ.val (Nat.succ_pos _))
      obtain ⟨a, ha⟩ := hg.1 j.succ
      change (record y xRef z₀ (ε w) j.succ.val).elim _ _ < _ at hjlt
      change readTime (record y xRef z₀ (ε w) j.succ.val) < (T : ℝ)
      rw [ha] at hjlt ⊢
      exact NNReal.coe_lt_coe.mpr (WithTop.coe_lt_coe.mp hjlt)
    · obtain ⟨a, ⟨ha, hat, haw⟩, _⟩ := hc.2 T k hi.1 hi.2
      change record y xRef z₀ (ε w) k = Sum.inl a at ha
      change survival y xRef (record y xRef z₀ (ε w) k)
        (T - liveTime (record y xRef z₀ (ε w) k)) (w k)
      rw [ha]
      exact haw
  have hcount : ∀ᵐ w ∂P,
      (∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)) ∧
      (∀ k : ℕ, N y xRef z₀ T w = k ↔ w ∈ C y xRef z₀ k T) ∧
      {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.Finite ∧
      {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.Finite ∧
      N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.ncard ∧
      N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.ncard := by
    filter_upwards [hAE] with w hw
    have hN : w ∈ I y xRef z₀ T (N y xRef z₀ T w) := by
      dsimp only [N]
      split_ifs with hex
      · exact Nat.find_spec hex
      · exact False.elim (hex hw.2.1)
    refine ⟨hw.1, ?_, interval_count_cardinality (eventTime y xRef z₀ w) (hmono w)
      T (N y xRef z₀ T w) hN hw.1⟩
    intro k
    rw [← hw.2.2 k]
    constructor
    · intro hk; rw [← hk]; exact hN
    · intro hk
      exact monotone_intervals_unique (eventTime y xRef z₀ w) (hmono w) T _ _ hN hk
  refine ⟨hraw, hcount, ?_, ?_⟩
  · intro i j hij
    apply Set.disjoint_left.mpr
    intro w hi hj
    exact hij (monotone_intervals_unique (eventTime y xRef z₀ w) (hmono w) T i j
      (hraw i w hi) (hraw j w hj))
  · letI : IsProbabilityMeasure P :=
      AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
    have hfull : ∀ᵐ w ∂P, w ∈ ⋃ k : ℕ, C y xRef z₀ k T := by
      filter_upwards [hAE] with w hw
      obtain ⟨k, hk⟩ := hw.2.1
      exact Set.mem_iUnion.mpr ⟨k, (hw.2.2 k).mp hk⟩
    exact (measure_congr (ae_eq_univ.mpr hfull)).trans (measure_univ : P Set.univ = 1)
'''
out='import Mathlib.Data.Set.Card\nimport Mathlib.Order.Interval.Set.Nat\n'+base+'\nattribute [local instance] Classical.propDecidable\n'+helpers+'\n'+term
out+='\nattribute [local instance] Classical.propDecidable\nset_option maxHeartbeats 1800000 in\nprivate theorem actual_count_event_identification'+sig+' :\n'+lets+conclusion+' := by\n  classical\n'
out+='\n'.join(line[2:] if line.startswith('  ') else line for line in lets.rstrip().splitlines())+'\n'
out+='  change\n'+conclusion+body+'\n#print axioms actual_count_event_identification\nend\nend EndpointInterfaces93\n'
(run/'ActualCountEvent93.lean').write_text(out,encoding='utf8',newline='\n')
