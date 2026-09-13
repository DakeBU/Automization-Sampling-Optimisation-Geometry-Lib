import AutoSamplingTheory.TechnicalLemmas.Analysis.RestartReduction
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Algebra.Order.Floor.Semiring

/-!
# Logarithmic restart complexity

Chewi arXiv2605.07006v1 Section4.1 Lemma4.1, logarithmic rounds and final call.
This closes the horizon premise of the actual finite restart construction.
Natural ceiling includes the coarse-accuracy, zero-round regime. Final cost is
retained; absorbing it requires an explicit comparison of the two budgets.
The small-error bound is conditional, not an unqualified source repair.
As with the parent, a fixed-objective solver contract does not certify oracle
execution or a class-uniform first-order algorithm.
-/
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.RestartLogComplexity
open Set
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- A rounded logarithmic horizon gives actual restart accuracy and explicit
cost, including zero rounds; budget absorption and small-error order are conditional. -/
theorem logarithmic_accuracy_and_cost {f : E → ℝ} {α β R ε : ℝ}
    (hf : ContDiff ℝ 1 f) (hsc : StrongConvexOn univ α f)
    (hα : 0 < α) (hβ : 0 < β) (hR : 0 < R) (hε : 0 < ε)
    {z x₀ : E} (hmin : IsMinOn f univ z) (hx₀ : ‖x₀-z‖ ≤ R)
    (A : E → ℝ → ℝ → E × ℕ) (φ : ℝ → ℕ)
    (hA : ∀ y r δ, 0 < r → 0 < δ → ‖y-z‖ ≤ r →
      f (A y r δ).1 - f z ≤ δ ∧ (A y r δ).2 ≤ φ (β*r^2/δ)) :
    let L := Real.log (α*R^2/ε) / Real.log 4
    let N := ⌈L⌉₊
    let r := fun k : ℕ => R / (2:ℝ)^k
    let run : ℕ → E × ℕ := Nat.rec (x₀, 0) (fun k p =>
      let w := A p.1 (r k) (α*(r k)^2/8)
      (w.1, p.2 + w.2))
    let last := A (run N).1 (Real.sqrt (ε/α)) ε
    let C := (run N).2 + last.2
    (N : ℝ) ≤ max 0 L + 1 ∧ (N = 0 ↔ α*R^2 ≤ ε) ∧
      ‖(run N).1-z‖ ≤ r N ∧ f last.1 - f z ≤ ε ∧
      C ≤ N * φ (8*(β/α)) + φ (β/α) ∧
      (C : ℝ) ≤ (max 0 L + 1) * φ (8*(β/α)) + φ (β/α) ∧
      (φ (β/α) ≤ φ (8*(β/α)) →
        (C : ℝ) ≤ (max 0 L + 2) * φ (8*(β/α)) ∧
        (4 ≤ α*R^2/ε → (C : ℝ) ≤ 3*L*φ (8*(β/α)))) := by
  let L := Real.log (α*R^2/ε) / Real.log 4
  let N := ⌈L⌉₊
  have hlog : 0 < Real.log 4 := Real.log_pos (by norm_num)
  have hq : 0 < α*R^2/ε := by positivity
  have hround : (N : ℝ) ≤ max 0 L + 1 := by
    by_cases hL : 0 ≤ L
    · exact (Nat.ceil_lt_add_one hL).le.trans (by rw [max_eq_right hL])
    · have hz : N = 0 := Nat.ceil_eq_zero.mpr (le_of_not_ge hL)
      rw [hz, Nat.cast_zero, max_eq_left (le_of_not_ge hL)]
      norm_num
  have hzero : N = 0 ↔ α*R^2 ≤ ε := by
    change ⌈Real.log (α*R^2/ε) / Real.log 4⌉₊ = 0 ↔ _
    rw [Nat.ceil_eq_zero, div_le_iff₀ hlog, zero_mul]
    rw [← Real.log_one, Real.log_le_log_iff hq (by norm_num)]
    exact (div_le_iff₀ hε).trans (by simp)
  have hpow : α*R^2/ε ≤ (4:ℝ)^N := by
    apply (Real.log_le_log_iff hq (by positivity)).mp
    rw [Real.log_pow]
    exact (div_le_iff₀ hlog).mp (Nat.le_ceil L)
  have hid : ((2:ℝ)^N)^2 = (4:ℝ)^N := by
    rw [← pow_mul, Nat.mul_comm N 2, pow_mul]
    norm_num
  have hN : α*(R/(2:ℝ)^N)^2 ≤ ε := by
    rw [div_pow, ← mul_div_assoc, hid]
    apply (div_le_iff₀ (by positivity : 0 < (4:ℝ)^N)).mpr
    have h := (div_le_iff₀ hε).mp hpow
    nlinarith
  have hb := RestartReduction.radius_accuracy_and_cost hf hsc hα hβ hR hε
    hmin hx₀ A φ hA N hN
  let r := fun k : ℕ => R / (2:ℝ)^k
  let run : ℕ → E × ℕ := Nat.rec (x₀, 0) (fun k p =>
    let w := A p.1 (r k) (α*(r k)^2/8)
    (w.1, p.2 + w.2))
  let last := A (run N).1 (Real.sqrt (ε/α)) ε
  let C := (run N).2 + last.2
  have hcast : (C : ℝ) ≤ (N : ℝ) * φ (8*(β/α)) + φ (β/α) := by
    have hc : C ≤ N * φ (8*(β/α)) + φ (β/α) := hb.2.2.2
    simpa only [Nat.cast_add, Nat.cast_mul] using ((Nat.cast_le (α := ℝ)).mpr hc)
  have hm : (N : ℝ) * φ (8*(β/α)) ≤
      (max 0 L + 1) * φ (8*(β/α)) :=
    mul_le_mul_of_nonneg_right hround (Nat.cast_nonneg _)
  have hreal : (C : ℝ) ≤ (max 0 L + 1) * φ (8*(β/α)) + φ (β/α) := by
    linarith
  refine ⟨hround, hzero, hb.1, hb.2.2.1, hb.2.2.2, hreal, ?_⟩
  intro hφ
  have hp : (φ (β/α) : ℝ) ≤ φ (8*(β/α)) := by exact_mod_cast hφ
  have ha : (C : ℝ) ≤ (max 0 L + 2) * φ (8*(β/α)) := by nlinarith
  refine ⟨ha, ?_⟩
  intro hsmall
  have hL : 1 ≤ L := by
    apply (le_div_iff₀ hlog).mpr
    simpa using (Real.log_le_log (by norm_num : (0:ℝ)<4) hsmall)
  rw [max_eq_right (by linarith : 0 ≤ L)] at ha
  have hfactor : L+2 ≤ 3*L := by linarith
  exact ha.trans (mul_le_mul_of_nonneg_right hfactor (Nat.cast_nonneg _))

end AutoSamplingTheory.TechnicalLemmas.Analysis.RestartLogComplexity
