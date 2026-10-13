from pathlib import Path
import hashlib, json
r=Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78')
s=json.loads((r/'root.statement-seal78.json').read_bytes()); h=Path(s['header']['path']).read_bytes()
assert hashlib.sha256(h).hexdigest()==s['header']['RAW_sha256']
h=h.decode('utf8').replace('\r\n','\n'); prefix=h.split('\nend\n',1)[0]
sig=h.split('private def actual_fixed_reference_event_time_nonaccumulation_statement',1)[1].split(' : Prop :=',1)[0]
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean').read_text(encoding='utf8')
defs=p.split(' := by\n',1)[1].split('  change\n',1)[0]
body='''  classical
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun sample k => Real.toNNReal (sample k)
'''+defs+'''  change ∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ sample ∂P,
    (∀ t : ℝ≥0, ∀ᶠ n : ℕ in atTop,
      (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) n) ∧
    (∀ t : ℝ≥0, {n : ℕ | eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0)}.Finite)
  -- Reuse the actual deterministic recurrence; no cap or recurrence is supplied.
  rcases ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
      hα hαβ hV hH hη hβη with
    ⟨hinit, _, _, _, _, htime, hstop, _, hcap, _⟩
  -- The good event supplies all positive thresholds and divergent actual sums.
  rcases AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws with
    ⟨_, _, _, hgood, hdiv⟩
  intro y xRef z₀
  filter_upwards [hgood, hdiv] with sample hpos hsum
  have hepos (k : ℕ) : 0 < ε sample k :=
    Real.toNNReal_pos.mpr (hpos k).1
  obtain ⟨hC, hinc, hzero⟩ := hcap y xRef z₀ (ε sample)
  have hescape : ∀ t : ℝ≥0, ∀ᶠ n : ℕ in atTop,
      (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) n := by
    -- Zero cap forces the first positive-threshold update to stop; it absorbs.
    by_cases hC0 : C y xRef z₀ = 0
    · have hfirst : record y xRef z₀ (ε sample) 1 = Sum.inr () :=
        hzero hC0 0 (0, z₀) (hinit y xRef z₀ (ε sample)) (hepos 0)
      intro t
      filter_upwards [eventually_ge_atTop (1 : ℕ)] with n hn
      obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hn
      have hs : record y xRef z₀ (ε sample) (1 + k) = Sum.inr () :=
        hstop y xRef z₀ (ε sample) 1 k hfirst
      change (t : WithTop ℝ≥0) < (record y xRef z₀ (ε sample) (1 + k)).elim _ _
      rw [hs]
      exact WithTop.coe_lt_top t
    -- Positive cap: inductively compare every actual clock with partial sums/C.
    · have hCp : 0 < C y xRef z₀ := lt_of_le_of_ne hC (Ne.symm hC0)
      let cap : ℝ≥0 := Real.toNNReal (C y xRef z₀)
      have hcapcoe : (cap : ℝ) = C y xRef z₀ := Real.coe_toNNReal _ hC
      have hcapPos : 0 < cap := Real.toNNReal_pos.mpr hCp
      have hbound (n : ℕ) :
          (((∑ k ∈ Finset.range n, ε sample k) / cap : ℝ≥0) : WithTop ℝ≥0) ≤
            eventTime y xRef z₀ (ε sample) n := by
        induction n with
        | zero => simpa using (htime y xRef z₀ (ε sample)).1.ge
        | succ n ih =>
          have hi := hinc hCp n
          have hterm : Real.toNNReal ((ε sample n : ℝ) / C y xRef z₀) =
              ε sample n / cap := by
            rw [Real.toNNReal_div (ε sample n).coe_nonneg, Real.toNNReal_coe]
          rw [hterm] at hi
          calc
            (((∑ k ∈ Finset.range (n + 1), ε sample k) / cap : ℝ≥0) : WithTop ℝ≥0)
                = (((∑ k ∈ Finset.range n, ε sample k) / cap : ℝ≥0) : WithTop ℝ≥0) +
                    ((ε sample n / cap : ℝ≥0) : WithTop ℝ≥0) := by
                      rw [Finset.sum_range_succ, add_div, WithTop.coe_add]
            _ ≤ eventTime y xRef z₀ (ε sample) n +
                    ((ε sample n / cap : ℝ≥0) : WithTop ℝ≥0) := add_le_add_right ih _
            _ ≤ eventTime y xRef z₀ (ε sample) (n + 1) := hi
      intro t
      have hs : ∀ᶠ n : ℕ in atTop,
          (t : ℝ) * C y xRef z₀ < ∑ k ∈ Finset.range n, (ε sample k : ℝ) :=
        hsum.eventually (eventually_gt_atTop ((t : ℝ) * C y xRef z₀))
      filter_upwards [hs] with n hn
      have ht : t < (∑ k ∈ Finset.range n, ε sample k) / cap := by
        apply (NNReal.coe_lt_coe).mp
        push_cast
        rw [hcapcoe]
        exact (lt_div_iff₀ hCp).mpr hn
      exact lt_of_lt_of_le (WithTop.coe_lt_coe.mpr ht) (hbound n)
  refine ⟨hescape, ?_⟩
  -- The bounded-horizon index set is contained in a finite initial interval.
  intro t
  obtain ⟨N, hN⟩ := eventually_atTop.mp (hescape t)
  apply (Set.finite_Iio N).subset
  intro n hn
  exact lt_of_not_ge (fun hge => (not_lt_of_ge hn) (hN n hge))
'''
theorem='\n\nset_option maxHeartbeats 800000 in\ntheorem actual_fixed_reference_event_time_nonaccumulation'+sig+' :\n    actual_fixed_reference_event_time_nonaccumulation_statement hα hαβ hV hH hη hβη := by\n'
f=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean'); assert not f.exists()
f.write_text(prefix+theorem+body+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation\n',encoding='utf8',newline='\n')
print('Wrote first proof candidate after statement seal; no proof credit until compiler closes.')
