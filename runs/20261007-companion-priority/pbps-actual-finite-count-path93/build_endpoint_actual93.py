from pathlib import Path
import re
run=Path(__file__).resolve().parent
pre=run.parent/'pbps-finite-count-path-preread93'
header=(pre/'Header93.lean').read_text(encoding='utf8')
sig=header.split('def candidate_finite_count_path_statement',1)[1].split(' : Prop := by',1)[0]
lets=header.split('  exact\n',1)[1].split('    let I :',1)[0]
conclusion='''    ∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,
      ∀ᵐ w ∂P, ∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)'''
body='''
  intro y xRef z₀ T
  have h76 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
    hα hαβ hV hH hη hβη
  have hmono (w : ℕ → ℝ) : Monotone (eventTime y xRef z₀ w) :=
    (h76.2.2.2.2.2.1 y xRef z₀ (ε w)).2
  have hgood := AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.2.2.2.1
  have hguard : ∀ᵐ w ∂P, ∀ n : ℕ,
      eventTime y xRef z₀ w n < ((T+1 : ℝ≥0) : WithTop ℝ≥0) →
        history y xRef z₀ n w ∈ A n (T+1) := by
    filter_upwards [hgood] with w hw
    intro n hn
    have hstrict (k : ℕ) (a b : ℝ≥0 × (E × E))
        (ha : record y xRef z₀ (ε w) k = Sum.inl a)
        (hb : record y xRef z₀ (ε w) (k+1) = Sum.inl b) : a.1 < b.1 :=
      (h76.2.2.2.2.2.2.2.2.2 y xRef z₀ (ε w) k a ha).2 b
        (Real.toNNReal_pos.mpr (hw k).1) hb
    have hh := live_prefix_strict_guard (record y xRef z₀ (ε w)) (hmono w) hstrict n (T+1) hn
    have heq (r : Rec) : readTime r = r.elim (fun a => (a.1 : ℝ)) (fun _ => 0) := by
      cases r <;> rfl
    exact ⟨hh.1, by simpa only [history, heq] using hh.2.1,
      by simpa only [history, heq] using hh.2.2⟩
  have hzero (n : ℕ) : P ({w | eventTime y xRef z₀ w (n+1) = (T : WithTop ℝ≥0)} ∩
      {w | history y xRef z₀ (n+1) w ∈ A (n+1) (T+1)}) = 0 := by
    have h92 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law
      hα hαβ hV hH hη hβη (n+1) (T+1)
    have hh := h92.2.2.2.2 y xRef z₀
    let obs : Hist (n+1) → ℝ := fun h => readTime (h (Fin.last (n+1)))
    have hread : Measurable readTime := by
      apply Measurable.sumElim
      · exact measurable_coe_nnreal_real.comp measurable_fst
      · exact measurable_const
    have hobs : Measurable obs := hread.comp (measurable_pi_apply (Fin.last (n+1)))
    have hK : Measurable (K y xRef z₀ (n+1) (T+1)) :=
      h92.2.2.1.comp (measurable_const (a := ((y,xRef),z₀)) |>.prodMk measurable_id)
    have hcoord (t : Prefix (n+1) (T+1)) :
        obs (K y xRef z₀ (n+1) (T+1) t) = t.val (Fin.last n) := by
      have hpos : 0 < t.val (Fin.last n) := by
        have ht := t.property.1 (show (0 : Fin (n+2)) < (Fin.last n).succ by
          change 0 < n+1; omega)
        simpa only [Fin.cons_zero, Fin.cons_succ] using ht
      change (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin (n+1) → ℝ) : Fin (n+2) → ℝ) (Fin.last (n+1))) : ℝ) = _
      change (Real.toNNReal (t.val (Fin.last n)) : ℝ) = _
      exact Real.coe_toNNReal _ hpos.le
    have hz := weighted_map_coordinate_null P
      (history y xRef z₀ (n+1) ⁻¹' A (n+1) (T+1)) (history y xRef z₀ (n+1))
      (n+1) (Δ (n+1) (T+1)) (K y xRef z₀ (n+1) (T+1))
      (q y xRef z₀ (n+1) (T+1)) obs (Fin.last n) (T : ℝ)
      hh.1 hK hobs hcoord hh.2.2.2.2.2.1
    apply measure_mono_null _ hz
    intro w hw
    refine ⟨?_, hw.2⟩
    obtain ⟨a, ha⟩ := hw.2.1 (Fin.last (n+1))
    change record y xRef z₀ (ε w) (n+1) = Sum.inl a at ha
    have he : a.1 = T := by
      have ht := hw.1
      change (record y xRef z₀ (ε w) (n+1)).elim _ _ = _ at ht
      rw [ha] at ht
      exact WithTop.coe_inj.mp ht
    change readTime (record y xRef z₀ (ε w) (n+1)) = (T : ℝ)
    rw [ha]
    exact congrArg (fun x : ℝ≥0 => (x : ℝ)) he
  have havoid (n : ℕ) : ∀ᵐ w ∂P, ¬ (eventTime y xRef z₀ w (n+1) = (T : WithTop ℝ≥0) ∧
      history y xRef z₀ (n+1) w ∈ A (n+1) (T+1)) := by
    rw [ae_iff]
    simpa only [not_not, Set.ofPred_and] using hzero n
  filter_upwards [hguard, ae_all_iff.mpr havoid] with w hg hn
  intro j hj heq
  obtain ⟨n, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hj)
  apply hn n
  refine ⟨heq, hg (n+1) ?_⟩
  rw [heq]
  exact WithTop.coe_lt_coe.mpr (lt_add_one T)
'''
base=(run/'EndpointInterfaces93.lean').read_text(encoding='utf8').rsplit('end EndpointInterfaces93',1)[0]
out=base+'\nopen scoped ContDiff Topology Interval BigOperators\nnoncomputable section\n'
out+='set_option maxHeartbeats 1000000 in\nprivate theorem actual_fixed_horizon_endpoint_nullity'+sig+' :\n'+lets+conclusion+' := by\n  classical\n'
out+='\n'.join(line[2:] if line.startswith('  ') else line for line in lets.rstrip().splitlines())+'\n'
out+='  change\n'+conclusion+body+'\n#print axioms actual_fixed_horizon_endpoint_nullity\nend\nend EndpointInterfaces93\n'
(run/'ActualEndpointNullity93.lean').write_text(out,encoding='utf8',newline='\n')
