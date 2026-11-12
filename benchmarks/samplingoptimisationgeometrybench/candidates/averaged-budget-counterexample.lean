import Mathlib.Probability.ProbabilityMassFunction.Integrals
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Averaged likelihood budgets do not control terminal work

A trusted, non-admitted Lean candidate for the finite counterexample in
`sogb-035` (public adaptive-hybrid-cost-boundary family). These are genuine
probability mass functions and Bochner integrals on `Bool × Bool`. After two
active bits, the prose extends the process by a common deterministic suffix;
the candidate concerns the two-bit marginal only. The terminal charge is not
the number of calls.

For `m ≥ 2`, put `p = 1/m²` and `q = 1/m`. On first bit true, the second-bit
true probabilities are `p` under `P` and `1` under `Q`; on first bit false they
are both zero. On the atom (true,true), the nonnegative work is `m²`. The
averaged budget is below two and the ideal second moment is one, while the
implemented expected charge is `m`. The local zero-mass support conditions
justify the totalized divisions in the chi-square expression.

This does not prove the positive pathwise budget theorem, an infinite-path
density or almost-sure termination result. It supplies no new question, Lean
track, model score, Registry leaf or claim about either actual sampler.
-/

namespace SamplingOptimisationGeometryBench.AveragedBudget

open MeasureTheory
open scoped BigOperators

noncomputable section

def bitMass (p : ℝ) (b : Bool) : ℝ := if b then p else 1 - p

def pathMass (p r : ℝ) (x : Bool × Bool) : ℝ :=
  bitMass p x.1 * bitMass (if x.1 then r else 0) x.2

private theorem bitMass_nonneg {p : ℝ} (h0 : 0 ≤ p) (h1 : p ≤ 1) (b : Bool) :
    0 ≤ bitMass p b := by
  cases b <;> simp [bitMass, h0, sub_nonneg.mpr h1]

private theorem pathMass_nonneg {p r : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1)
    (hr0 : 0 ≤ r) (hr1 : r ≤ 1) (x : Bool × Bool) :
    0 ≤ pathMass p r x := by
  rcases x with ⟨a,b⟩
  cases a <;> exact mul_nonneg (bitMass_nonneg hp0 hp1 _)
    (by apply bitMass_nonneg <;> simp [hr0, hr1])

noncomputable def twoStepLaw (p r : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1)
    (hr0 : 0 ≤ r) (hr1 : r ≤ 1) : PMF (Bool × Bool) :=
  PMF.ofFintype (fun x => ENNReal.ofReal (pathMass p r x)) (by
    rw [← ENNReal.ofReal_sum_of_nonneg (fun x _ => pathMass_nonneg hp0 hp1 hr0 hr1 x)]
    rw [show (∑ x : Bool × Bool, pathMass p r x) = 1 by
      simp [Fintype.sum_prod_type, pathMass, bitMass]; ring]
    simp)

private theorem twoStepLaw_real (p r : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1)
    (hr0 : 0 ≤ r) (hr1 : r ≤ 1) (x : Bool × Bool) :
    ((twoStepLaw p r hp0 hp1 hr0 hr1) x).toReal = pathMass p r x := by
  simp [twoStepLaw, ENNReal.toReal_ofReal, pathMass_nonneg hp0 hp1 hr0 hr1 x]

-- A zero ideal mass contributes zero only when the matching support
-- condition is verified; it is verified for both tables below.
def chiTwo (p q : ℝ) : ℝ :=
  (q - p)^2 / p + ((1 - q) - (1 - p))^2 / (1 - p)

theorem two_step_actual_averaged_budget_counterexample (m : ℝ) (hm : 2 ≤ m) :
    let p := (m ^ 2)⁻¹
    let q := m⁻¹
    let W := fun x : Bool × Bool => if x = (true, true) then m ^ 2 else 0
    ∃ P Q : PMF (Bool × Bool),
      (∀ x, (P x).toReal = pathMass p p x ∧ (Q x).toReal = pathMass q 1 x) ∧
      (∀ b, bitMass p b = 0 → bitMass q b = 0) ∧
      (∀ (a b : Bool), bitMass (if a then p else 0) b = 0 →
        bitMass (if a then 1 else 0) b = 0) ∧
      chiTwo p q + (∫ x, chiTwo (if x.1 then p else 0) (if x.1 then 1 else 0)
        ∂(P.toMeasure)) < 2 ∧
      (∀ x, 0 ≤ W x) ∧
      Integrable W P.toMeasure ∧ Integrable W Q.toMeasure ∧
      Integrable (fun x => (W x)^2) P.toMeasure ∧
      (∫ x, W x ∂(P.toMeasure)) = p ∧
      (∫ x, (W x)^2 ∂(P.toMeasure)) = 1 ∧
      (∫ x, W x ∂(Q.toMeasure)) = m := by
  intro p q W
  have hm0 : 0 < m := by linarith
  have hm1 : 1 < m := by linarith
  have hq : 0 < q := inv_pos.mpr hm0
  have hq1 : q < 1 := inv_lt_one_of_one_lt₀ hm1
  have hqp : q^2 = p := by simp [p, q, inv_pow]
  have hp : 0 < p := hqp ▸ sq_pos_of_pos hq
  have hpq : p < q := by rw [← hqp]; nlinarith [mul_pos hq (sub_pos.mpr hq1)]
  have hp1 : p < 1 := hpq.trans hq1
  have hpbar : 0 < 1-p := sub_pos.mpr hp1
  let P := twoStepLaw p p hp.le hp1.le hp.le hp1.le
  let Q := twoStepLaw q 1 hq.le hq1.le zero_le_one le_rfl
  have hP (x : Bool × Bool) : (P x).toReal = pathMass p p x :=
    twoStepLaw_real p p hp.le hp1.le hp.le hp1.le x
  have hQ (x : Bool × Bool) : (Q x).toReal = pathMass q 1 x :=
    twoStepLaw_real q 1 hq.le hq1.le zero_le_one le_rfl x
  have hs (b : Bool) : 0 < bitMass p b := by
    cases b
    · simpa [bitMass] using hpbar
    · simpa [bitMass] using hp
  have hfirst : chiTwo p q < 1 := by
    have he : chiTwo p q = (q-p)^2 / (p*(1-p)) := by
      unfold chiTwo
      field_simp [hp.ne', hpbar.ne']
      ; ring
    rw [he, div_lt_one (mul_pos hp hpbar)]
    nlinarith [mul_pos hp (sub_pos.mpr hpq)]
  have hsecond : p * chiTwo p 1 = 1-p := by
    unfold chiTwo
    field_simp [hp.ne', hpbar.ne']
    ; ring
  have hzero : chiTwo 0 0 = 0 := by norm_num [chiTwo]
  refine ⟨P, Q, fun x => ⟨hP x, hQ x⟩, fun b h => (ne_of_gt (hs b) h).elim,
    ?_, ?_, ?_, Integrable.of_finite, Integrable.of_finite, Integrable.of_finite,
    ?_, ?_, ?_⟩
  · intro a b
    cases a
    · simp
    · intro h
      exact (ne_of_gt (hs b) (by simpa using h)).elim
  · have he : (∫ x, chiTwo (if x.1 then p else 0) (if x.1 then 1 else 0)
        ∂(P.toMeasure)) = p * chiTwo p 1 := by
      rw [PMF.integral_eq_sum]
      simp [hP, smul_eq_mul, Fintype.sum_prod_type, pathMass, bitMass, hzero]
      ; ring
    rw [he, hsecond]
    linarith
  · intro x
    unfold W
    split <;> positivity
  · rw [PMF.integral_eq_sum]
    simp [hP, smul_eq_mul, pathMass, bitMass, W, p]
    field_simp [hm0.ne']
  · rw [PMF.integral_eq_sum]
    simp [hP, smul_eq_mul, pathMass, bitMass, W, p]
    ; field_simp [hm0.ne']
  · rw [PMF.integral_eq_sum]
    simp [hQ, smul_eq_mul, pathMass, bitMass, W, q]
    ; field_simp [hm0.ne']

/--
info: 'SamplingOptimisationGeometryBench.AveragedBudget.two_step_actual_averaged_budget_counterexample' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms two_step_actual_averaged_budget_counterexample

end
end SamplingOptimisationGeometryBench.AveragedBudget
