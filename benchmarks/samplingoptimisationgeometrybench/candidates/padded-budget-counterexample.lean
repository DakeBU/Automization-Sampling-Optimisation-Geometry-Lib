import «averaged-budget-counterexample»
import «conditional-budget-transfer»

/-!
# Two-call averaged-budget counterexample on actual paths

Push forward the proved finite laws through the measurable deterministic
padding map. Check the actual cylinder probabilities at depth zero, one,
two, and all later depths, plus local support and normalization of both
tables. Transfer the finite moments, the stop at two, and the common zero
tail. The whole expected-work family is unbounded although every prefix
has average budget less than two and ideal squared work one.

This is a trusted proof candidate for public sogb-035, not a new evaluation
task, independent semantic verdict or native execution result.
-/

namespace SamplingOptimisationGeometryBench.PaddedCounterexample
open MeasureTheory Set
open scoped BigOperators ENNReal
open BinaryPrefixLikelihood AveragedBudget

noncomputable section

def pad (u : Bool × Bool) (i : ℕ) : Bool :=
  if i = 0 then u.1 else if i = 1 then u.2 else false

theorem measurable_pad : Measurable pad := measurable_of_finite _

def paddedLaw (M : PMF (Bool × Bool)) : Measure Path := M.toMeasure.map pad

instance (M : PMF (Bool × Bool)) : IsProbabilityMeasure (paddedLaw M) :=
  Measure.isProbabilityMeasure_map measurable_pad.aemeasurable

def paddedTable (p r : ℝ) : Table
  | 0, _, b => bitMass p b
  | 1, h, b => bitMass (if h 0 then r else 0) b
  | _ + 2, _, b => bitMass 0 b

private theorem measurable_cylinder (n : ℕ) (h : History n) : MeasurableSet (cylinder n h) :=
  measurable_readPrefix n (MeasurableSet.singleton _)

private theorem cylinder_snoc (n : ℕ) (h : History n) (b : Bool) :
    cylinder (n+1) (Fin.snoc h b) = cylinder n h ∩ {x | x n = b} := by
  ext x
  change readPrefix (n+1) x = Fin.snoc h b ↔ readPrefix n x = h ∧ x n = b
  constructor
  · intro he
    refine ⟨?_, ?_⟩
    · have hi := congrArg Fin.init he
      rw [Fin.init_snoc] at hi
      exact hi
    · have hi := congrFun he (Fin.last n)
      rw [Fin.snoc_last] at hi
      exact hi
  · rintro ⟨hh, hb⟩
    have hi : readPrefix (n+1) x = Fin.snoc (readPrefix n x) (x n) :=
      (Fin.snoc_init_self (readPrefix (n+1) x)).symm
    rwa [hh, hb] at hi

private theorem mass_padded (M : PMF (Bool × Bool)) (n : ℕ) (h : History n) :
    mass (paddedLaw M) n h = M.toMeasure.real (pad ⁻¹' cylinder n h) := by
  simp [paddedLaw, mass, measureReal_def, Measure.map_apply measurable_pad (measurable_cylinder n h)]

private theorem mass_one (M : PMF (Bool × Bool)) (p r : ℝ)
    (hM : ∀ x, (M x).toReal = pathMass p r x) (h : History 1) :
    mass (paddedLaw M) 1 h = bitMass p (h 0) := by
  have he : pad ⁻¹' cylinder 1 h = {(h 0,false)} ∪ {(h 0,true)} := by
    ext x
    rcases x with ⟨a,b⟩
    cases b <;> simp [BinaryPrefixLikelihood.cylinder, readPrefix, pad, funext_iff,
      Fin.forall_fin_one]
  rw [mass_padded, he, measureReal_union (by simp) (MeasurableSet.singleton _)]
  simp only [measureReal_def, PMF.toMeasure_apply_singleton _ _ (MeasurableSet.singleton _), hM]
  cases h 0
  · simp [pathMass, bitMass]
  · simp [pathMass, bitMass]
    ring

private theorem mass_two (M : PMF (Bool × Bool)) (p r : ℝ)
    (hM : ∀ x, (M x).toReal = pathMass p r x) (h : History 2) :
    mass (paddedLaw M) 2 h = pathMass p r (h 0, h 1) := by
  have he : pad ⁻¹' cylinder 2 h = {(h 0,h 1)} := by
    ext x
    rcases x with ⟨a,b⟩
    simp [BinaryPrefixLikelihood.cylinder, readPrefix, pad, funext_iff, Fin.forall_fin_succ]
  rw [mass_padded, he, measureReal_def,
    PMF.toMeasure_apply_singleton _ _ (MeasurableSet.singleton _), hM]

private theorem mass_tail (M : PMF (Bool × Bool)) {n : ℕ} (hn : 2 ≤ n)
    (h : History n) (b : Bool) :
    mass (paddedLaw M) (n+1) (Fin.snoc h b) = mass (paddedLaw M) n h * bitMass 0 b := by
  have hn0 : n ≠ 0 := by omega
  have hn1 : n ≠ 1 := by omega
  rw [mass_padded, mass_padded, cylinder_snoc]
  cases b <;> simp [Set.preimage_inter, pad, hn0, hn1, bitMass]

theorem paddedLaw_realizes (M : PMF (Bool × Bool)) (p r : ℝ)
    (hM : ∀ x, (M x).toReal = pathMass p r x) :
    Realizes (paddedLaw M) (paddedTable p r) := by
  intro n h b
  cases n with
  | zero =>
    rw [mass_one M p r hM, mass_zero_length]
    change bitMass p (Fin.snoc (α := fun _ => Bool) h b (Fin.last 0)) = 1 * bitMass p b
    rw [Fin.snoc_last, one_mul]
  | succ n =>
    cases n with
    | zero =>
      rw [mass_two M p r hM, mass_one M p r hM]
      change pathMass p r (Fin.snoc (α := fun _ => Bool) h b 0,
        Fin.snoc (α := fun _ => Bool) h b (Fin.last 1)) =
        bitMass p (h 0) * bitMass (if h 0 then r else 0) b
      rw [Fin.snoc_apply_zero, Fin.snoc_last]
      rfl
    | succ n => exact mass_tail M (by omega) h b

/--
info: 'SamplingOptimisationGeometryBench.PaddedCounterexample.paddedLaw_realizes' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms paddedLaw_realizes

private theorem chiSquare_bitMass (p q : ℝ) :
    chiSquare (bitMass p) (bitMass q) = chiTwo p q := by
  simp [chiSquare, chiTwo, bitMass]

private theorem bitMass_pos {p : ℝ} (hp : 0 < p) (hp1 : p < 1) (b : Bool) :
    0 < bitMass p b := by
  cases b
  · simpa [bitMass] using sub_pos.mpr hp1
  · simpa [bitMass] using hp

theorem paddedBudget_zero (M : PMF (Bool × Bool)) (p q r s : ℝ) (x : Path) :
    budgetProcess (paddedLaw M) (paddedTable p r) (paddedTable q s) 0 x = chiTwo p q := by
  unfold budgetProcess conditionalBudget
  rw [mass_zero_length, if_neg one_ne_zero]
  exact chiSquare_bitMass _ _

theorem paddedBudget_one (M : PMF (Bool × Bool)) {p q r s : ℝ}
    (hM : ∀ x, (M x).toReal = pathMass p r x) (hp : 0 < p) (hp1 : p < 1) (x : Path) :
    budgetProcess (paddedLaw M) (paddedTable p r) (paddedTable q s) 1 x =
      chiTwo (if x 0 then r else 0) (if x 0 then s else 0) := by
  unfold budgetProcess conditionalBudget
  rw [mass_one M p r hM, if_neg (bitMass_pos hp hp1 _).ne']
  exact chiSquare_bitMass _ _

theorem paddedBudget_tail (M : PMF (Bool × Bool)) (p q r s : ℝ) {n : ℕ} (hn : 2 ≤ n)
    (x : Path) : budgetProcess (paddedLaw M) (paddedTable p r) (paddedTable q s) n x = 0 := by
  rcases n with _ | _ | n
  · omega
  · omega
  · simp [budgetProcess, conditionalBudget, paddedTable, chiSquare, bitMass]

theorem padded_supports (M : PMF (Bool × Bool)) {p q : ℝ}
    (hp : 0 < p) (hp1 : p < 1) :
    Supports (paddedLaw M) (paddedTable p p) (paddedTable q 1) := by
  intro n h b _ hb
  rcases n with _ | _ | n
  · exact ((bitMass_pos hp hp1 b).ne' hb).elim
  · by_cases hh : h 0 = true
    · exact ((bitMass_pos hp hp1 b).ne' (by simpa [paddedTable, hh] using hb)).elim
    · simpa [paddedTable, hh] using hb
  · exact hb

theorem padded_normalized {p r : ℝ} (hp : 0 ≤ p) (hp1 : p ≤ 1) (hr : 0 ≤ r) (hr1 : r ≤ 1) :
    ∀ n h, (∀ b, 0 ≤ paddedTable p r n h b) ∧ ∑ b, paddedTable p r n h b = 1 := by
  have hbit (z : ℝ) (hz : 0 ≤ z) (hz1 : z ≤ 1) :
      (∀ b, 0 ≤ bitMass z b) ∧ ∑ b, bitMass z b = 1 := by
    refine ⟨?_, ?_⟩
    · intro b
      cases b <;> simp [bitMass, hz, sub_nonneg.mpr hz1]
    · simp [bitMass]
  intro n h
  rcases n with _ | _ | n
  · exact hbit p hp hp1
  · by_cases hh : h 0 = true
    · simpa [paddedTable, hh] using hbit r hr hr1
    · simpa [paddedTable, hh] using hbit 0 le_rfl zero_le_one
  · exact hbit 0 le_rfl zero_le_one

/--
info: 'SamplingOptimisationGeometryBench.PaddedCounterexample.padded_supports' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms padded_supports

def terminalCharge (m : ℝ) (x : Path) : ℝ≥0∞ :=
  ENNReal.ofReal (if (x 0, x 1) = (true, true) then m^2 else 0)

private theorem measurable_terminalCharge (m : ℝ) : Measurable (terminalCharge m) := by
  exact (measurable_of_finite (fun b : Bool × Bool =>
    ENNReal.ofReal (if b = (true,true) then m^2 else 0))).comp
      ((measurable_pi_apply 0).prodMk (measurable_pi_apply 1))

private theorem ae_pad_tail (M : PMF (Bool × Bool)) :
    ∀ᵐ x ∂paddedLaw M, ∀ k ≥ 2, x k = false := by
  have hm : MeasurableSet {x : Path | ∀ k ≥ 2, x k = false} := by
    have he : {x : Path | ∀ k ≥ 2, x k = false} = ⋂ k : ℕ, ⋂ _ : 2 ≤ k,
        (fun x : Path => x k) ⁻¹' {false} := by
      ext x
      simp
    rw [he]
    exact MeasurableSet.iInter fun k => MeasurableSet.iInter fun _ =>
      measurable_pi_apply k (MeasurableSet.singleton _)
  apply (ae_map_iff measurable_pad.aemeasurable hm).2
  exact Filter.Eventually.of_forall fun u k hk => by
    have h0 : k ≠ 0 := by omega
    have h1 : k ≠ 1 := by omega
    simp [pad, h0, h1]

/-- The finite counterexample on the actual infinite product path space.
The ideal averaged budget stays below two for every prefix, even though the
implemented expected terminal charge equals the unbounded parameter m. -/
theorem binary_padded_averaged_budget_counterexample (m : ℝ) (hm : 2 ≤ m) :
    let p := (m^2)⁻¹
    let q := m⁻¹
    let pt := paddedTable p p
    let qt := paddedTable q 1
    ∃ P Q : Measure Path,
      IsProbabilityMeasure P ∧ IsProbabilityMeasure Q ∧
      Realizes P pt ∧ Realizes Q qt ∧ Supports P pt qt ∧
      (∀ n h, (∀ b, 0 ≤ pt n h b) ∧ ∑ b, pt n h b = 1) ∧
      (∀ n h, (∀ b, 0 ≤ qt n h b) ∧ ∑ b, qt n h b = 1) ∧
      IsStoppingTime historyFiltration (fun _ => (2 : WithTop ℕ)) ∧
      (∀ᵐ x ∂P, ∀ k ≥ 2, x k = false) ∧ (∀ᵐ x ∂Q, ∀ k ≥ 2, x k = false) ∧
      (∀ n, ∑ k ∈ Finset.range n, (∫ x, budgetProcess P pt qt k x ∂P) < 2) ∧
      Measurable (terminalCharge m) ∧
      (∫⁻ x, (terminalCharge m x)^2 ∂P) = 1 ∧
      (∫⁻ x, terminalCharge m x ∂Q) = ENNReal.ofReal m := by
  intro p q pt qt
  let V : Bool × Bool → ℝ := fun x => if x = (true,true) then m^2 else 0
  have hfin := two_step_actual_averaged_budget_counterexample m hm
  change ∃ M N : PMF (Bool × Bool),
    (∀ x, (M x).toReal = pathMass p p x ∧ (N x).toReal = pathMass q 1 x) ∧ _ at hfin
  obtain ⟨M, N, hMN, _, _, hb, hV0, hVM, hVN, hV2M, _, hM2, hNm⟩ := hfin
  have hm0 : 0 < m := by linarith
  have hm1 : 1 < m := by linarith
  have hp : 0 < p := inv_pos.mpr (sq_pos_of_pos hm0)
  have hp1 : p < 1 := inv_lt_one_of_one_lt₀ (by nlinarith)
  have hq : 0 < q := inv_pos.mpr hm0
  have hq1 : q < 1 := inv_lt_one_of_one_lt₀ hm1
  let P := paddedLaw M
  let Q := paddedLaw N
  have hpM (x : Bool × Bool) : (M x).toReal = pathMass p p x := (hMN x).1
  have hqN (x : Bool × Bool) : (N x).toReal = pathMass q 1 x := (hMN x).2
  have hpt := padded_normalized hp.le hp1.le hp.le hp1.le
  have hqt := padded_normalized hq.le hq1.le zero_le_one le_rfl
  let E : ℕ → ℝ := fun n => ∫ x, budgetProcess P pt qt n x ∂P
  let e1 : ℝ := ∫ u, chiTwo (if u.1 then p else 0) (if u.1 then 1 else 0) ∂M.toMeasure
  have he0 : E 0 = chiTwo p q := by
    change (∫ x, budgetProcess P pt qt 0 x ∂P) = _
    simp [P, pt, qt, paddedBudget_zero]
  have he1 : E 1 = e1 := by
    change (∫ x, budgetProcess P pt qt 1 x ∂P) = _
    have hmE := (stronglyAdapted_budgetProcess P pt qt 1).mono (historyFiltration.le 1)
    calc
      _ = ∫ u, budgetProcess P pt qt 1 (pad u) ∂M.toMeasure :=
        integral_map measurable_pad.aemeasurable hmE.aestronglyMeasurable
      _ = e1 := integral_congr_ae <| Filter.Eventually.of_forall fun u => by
        simp [P, pt, qt, paddedBudget_one M hpM hp hp1, pad]
  have he_tail (n : ℕ) (hn : 2 ≤ n) : E n = 0 := by
    change (∫ x, budgetProcess P pt qt n x ∂P) = _
    simp [P, pt, qt, paddedBudget_tail M p q p 1 hn]
  have he1nn : 0 ≤ e1 := by
    rw [← he1]
    exact integral_nonneg (budgetProcess_nonneg (p := pt) (q := qt) P
      (fun n h => (hpt n h).1) 1)
  have hsum (n : ℕ) : ∑ k ∈ Finset.range (n + 2), E k = chiTwo p q + e1 := by
    induction n with
    | zero => simp [Finset.sum_range_succ, he0, he1]
    | succ n ih =>
      rw [show n + 1 + 2 = n + 2 + 1 by omega, Finset.sum_range_succ,
        ih, he_tail (n+2) (by omega), add_zero]
  have hbud (n : ℕ) : ∑ k ∈ Finset.range n, E k < 2 := by
    rcases n with _ | _ | n
    · norm_num
    · simpa [Finset.sum_range_succ, he0] using (le_add_of_nonneg_right he1nn).trans_lt hb
    · exact (hsum n).trans_lt hb
  have hmW := measurable_terminalCharge m
  have hpadW (u : Bool × Bool) : terminalCharge m (pad u) = ENNReal.ofReal (V u) := by
    cases u
    simp [terminalCharge, pad, V]
  refine ⟨P, Q, inferInstance, inferInstance, paddedLaw_realizes M p p hpM,
    paddedLaw_realizes N q 1 hqN, padded_supports M hp hp1, hpt, hqt,
    isStoppingTime_const historyFiltration 2, ae_pad_tail M, ae_pad_tail N, hbud, hmW, ?_, ?_⟩
  · change (∫⁻ x, (terminalCharge m x)^2 ∂(M.toMeasure.map pad)) = 1
    rw [lintegral_map (hmW.pow_const _) measurable_pad]
    calc
      _ = ∫⁻ u, ENNReal.ofReal ((V u)^2) ∂M.toMeasure := by
        apply lintegral_congr
        intro u
        rw [hpadW, ENNReal.ofReal_pow (hV0 u)]
      _ = 1 := by
        rw [← ofReal_integral_eq_lintegral_ofReal hV2M
          (Filter.Eventually.of_forall fun _ => sq_nonneg _), hM2]
        simp
  · change (∫⁻ x, terminalCharge m x ∂(N.toMeasure.map pad)) = ENNReal.ofReal m
    rw [lintegral_map hmW measurable_pad]
    simp_rw [hpadW]
    rw [← ofReal_integral_eq_lintegral_ofReal hVN (Filter.Eventually.of_forall hV0), hNm]

/--
info: 'SamplingOptimisationGeometryBench.PaddedCounterexample.binary_padded_averaged_budget_counterexample' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms binary_padded_averaged_budget_counterexample
end
end SamplingOptimisationGeometryBench.PaddedCounterexample
