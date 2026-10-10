from pathlib import Path
import json,hashlib
R=Path('E:/Samplinglib');r=Path(__file__).parent
header=(r/'header87.proposed.lean').read_text(encoding='utf-8')
seal=json.loads((r/'root.statement-seal87.json').read_bytes())
assert hashlib.sha256((r/'header87.proposed.lean').read_bytes()).hexdigest()==seal['header']['raw_sha256']
base=header.split('\n#check',1)[0]
spec=header.split('private def actual_finite_history_tail_law_statement',1)[1].split('\n#check',1)[0]
binders,body=spec.split(' : Prop :=\n',1)
lets,conclusion=body.split('    ∀ y xRef',1)
local='\n'.join(s[2:] if s.startswith('  ') else s for s in lets.rstrip().splitlines())
conclusion='  ∀ y xRef'+conclusion
proof='''  classical
'''+local+'''
  change
'''+conclusion+'''
  have hrec := ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
    hα hαβ hV hH hη hβη
  have hR (j : ℕ) : Measurable (fun a : (E × E) × (E × E) × (ℕ → ℝ≥0) =>
      record a.1.1 a.1.2 a.2.1 a.2.2 j) := hrec.2.2.2.1 j
  have hinput := AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.
    unit_exponential_product_laws
  letI : IsProbabilityMeasure P := hinput.1
  letI : IsProbabilityMeasure (expMeasure (1 : ℝ)) :=
    isProbabilityMeasure_expMeasure zero_lt_one
  have hclock : iIndepFun (fun k (w : ℕ → ℝ) => w k) P := hinput.2.2.1
  intro y xRef z₀ n
  -- Deterministic causality: the mth record consumes exactly coordinates below m.
  have hcausal (e e' : ℕ → ℝ≥0) (m : ℕ)
      (he : ∀ k < m, e k = e' k) :
      record y xRef z₀ e m = record y xRef z₀ e' m := by
    induction m with
    | zero => rfl
    | succ m ih =>
      change next y xRef (e m) (record y xRef z₀ e m) =
        next y xRef (e' m) (record y xRef z₀ e' m)
      rw [he m (Nat.lt_succ_self m), ih (fun k hk => he k (Nat.lt_succ_of_lt hk))]
  have hprefix (w w' : ℕ → ℝ) (hw : ∀ k < n, w k = w' k) :
      history y xRef z₀ n w = history y xRef z₀ n w' := by
    funext j
    exact hcausal (ε w) (ε w') j.val (fun k hk =>
      congrArg Real.toNNReal (hw k (lt_of_lt_of_le hk (Nat.le_of_lt_succ j.isLt))))
  have hε : Measurable ε := measurable_pi_lambda _ (fun k =>
    measurable_real_toNNReal.comp (measurable_pi_apply k))
  have hHmeas : Measurable (history y xRef z₀ n) :=
    measurable_pi_lambda _ (fun j => (hR j.val).comp
      (measurable_const.prodMk (measurable_const.prodMk hε)))
  have hTmeas : Measurable (tail n) :=
    measurable_pi_lambda _ (fun k => measurable_pi_apply (n + k))
  -- Truncation is a proof factorization, never a replacement algorithm/input law.
  let truncated : (ℕ → ℝ) → ℕ → ℝ≥0 :=
    fun w k => if k < n then ε w k else 0
  have htruncated : Measurable[past n] truncated := by
    apply measurable_pi_lambda
    intro k
    by_cases hk : k < n
    · have hx : Measurable[past n] (fun w : ℕ → ℝ => w k) := by
        apply measurable_iff_comap_le.mpr
        exact le_iSup_of_le k (le_iSup_of_le hk le_rfl)
      simpa only [truncated, hk, if_true, ε] using measurable_real_toNNReal.comp hx
    · simpa only [truncated, hk, if_false] using
        (measurable_const : Measurable[past n] (fun _ : ℕ → ℝ => (0 : ℝ≥0)))
  have hHp : Measurable[past n] (history y xRef z₀ n) := by
    apply measurable_pi_lambda
    intro j
    have hm := (hR j.val).comp
      (measurable_const.prodMk (measurable_const.prodMk htruncated))
    have heq : (fun w => record y xRef z₀ (truncated w) j.val) =
        (fun w => history y xRef z₀ n w j) := by
      funext w
      exact hcausal (truncated w) (ε w) j.val (fun k hk =>
        if_pos (lt_of_lt_of_le hk (Nat.le_of_lt_succ j.isLt)))
    rw [← heq]
    exact hm
  let future : MeasurableSpace (ℕ → ℝ) :=
    ⨆ k ∈ Set.Ici n, MeasurableSpace.comap (fun w : ℕ → ℝ => w k) inferInstance
  have hTf : Measurable[future] (tail n) := by
    apply measurable_pi_lambda
    intro k
    apply measurable_iff_comap_le.mpr
    exact le_iSup_of_le (n + k) (le_iSup_of_le (Nat.le_add_right n k) le_rfl)
  have hdis : Disjoint (Set.Iio n) (Set.Ici n) := by
    exact Set.disjoint_left.mpr (fun k hk hn => (not_lt_of_ge hn) hk)
  have hblocks : Indep (past n) future P :=
    indep_iSup_of_disjoint (fun k => (measurable_pi_apply k).comap_le)
      (iIndepFun_iff_iIndep.mp hclock) hdis
  have hindep : IndepFun (history y xRef z₀ n) (tail n) P :=
    indep_of_indep_of_le hblocks hHp.comap_le hTf.comap_le
  have htailLaw : Measure.map (tail n) P = P := by
    exact Measure.map_infinitePi_infinitePi_of_inj
      (P := fun _ : ℕ => expMeasure (1 : ℝ)) (f := fun k => n + k)
      (fun _ _ h => Nat.add_left_cancel h)
  have hjoint : Measure.map (fun w => (history y xRef z₀ n w, tail n w)) P =
      (Measure.map (history y xRef z₀ n) P).prod P := by
    rw [hindep.map_prod_eq_prod_map_map hHmeas.aemeasurable hTmeas.aemeasurable,
      htailLaw]
  refine ⟨hHmeas, hTmeas, hprefix, hHp, htailLaw, hindep, hjoint, ?_⟩
  intro A hA
  apply Measure.ext
  intro B hB
  rw [Measure.map_apply hTmeas hB, Measure.restrict_apply (hB.preimage hTmeas),
    Measure.smul_apply, Set.inter_comm,
    hindep.measure_inter_preimage_eq_mul A B hA hB]
  have hBtail : P (tail n ⁻¹' B) = P B := by
    rw [← Measure.map_apply hTmeas hB, htailLaw]
  rw [hBtail]
  rfl
'''
module=base+'\n\nset_option maxHeartbeats 1600000 in\ntheorem actual_finite_history_tail_law'+binders+' :\n    actual_finite_history_tail_law_statement hα hαβ hV hH hη hβη := by\n'+proof+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw\n'
p=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean';assert not p.exists();p.write_text(module,encoding='utf-8',newline='\n')
print('Sole writer proof created after exact statement seal; no local compilation credit yet.')
