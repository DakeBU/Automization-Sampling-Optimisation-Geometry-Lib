import AutoSamplingTheory.TechnicalLemmas.Analysis.RestartLogComplexity
import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentRates
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Algebra.Order.Floor.Semiring

open Set
open AutoSamplingTheory.TechnicalLemmas.Analysis
open scoped RealInnerProductSpace

-- Actual counted quadratic GD, with arbitrary positive accuracy rather than
-- a supplied adequate horizon. Coarse accuracy forces N0 but keeps the final call.
example (ε : ℝ) (hε : 0 < ε) :
    let L := Real.log (1/ε) / Real.log 4
    let N := ⌈L⌉₊
    let r := fun k : ℕ => 1 / (2:ℝ)^k
    let A : ℝ → ℝ → ℝ → ℝ × ℕ := fun y r δ =>
      ((fun x : ℝ => x - (1/2:ℝ)*x)^[⌈r^2/δ⌉₊+1] y, ⌈r^2/δ⌉₊+1)
    let run : ℕ → ℝ × ℕ := Nat.rec (1,0) (fun k p =>
      let w := A p.1 (r k) ((r k)^2/8)
      (w.1,p.2+w.2))
    let last := A (run N).1 (Real.sqrt ε) ε
    let C := (run N).2+last.2
    (N=0 ↔ 1≤ε) ∧ last.1^2/2 ≤ ε ∧ C ≤ 9*N+2 ∧
      (C:ℝ) ≤ 9*(max 0 L+1)+2 ∧ (ε≤1/4 → (C:ℝ) ≤ 27*L) := by
  let f : ℝ → ℝ := fun x => x^2/2
  let A : ℝ → ℝ → ℝ → ℝ × ℕ := fun y r δ =>
    ((fun x : ℝ => x - (1/2:ℝ)*x)^[⌈r^2/δ⌉₊+1] y, ⌈r^2/δ⌉₊+1)
  let φ : ℝ → ℕ := fun t => ⌈t/2⌉₊+1
  have hf : ContDiff ℝ 1 f := (contDiff_id.pow 2).div_const 2
  have hg (x : ℝ) : gradient f x = x := by
    have hd : HasDerivAt f x x := by
      simpa [f] using ((hasDerivAt_id x).pow 2).div_const (2:ℝ)
    exact hd.hasGradientAt.gradient
  have hc : StrongConvexOn univ 1 f := by
    rw [strongConvexOn_iff_convex]
    have he : (fun t : ℝ => f t - (1:ℝ)/2*‖t‖^2) = fun _ => 0 := by
      funext t; simp [f, Real.norm_eq_abs, sq_abs]; ring
    rw [he]; exact convexOn_const _ convex_univ
  have hu : ∀ a b, f b ≤ f a + inner ℝ (gradient f a) (b-a) + 2/2*‖b-a‖^2 := by
    intro a b; rw [hg]; simp only [f, Real.inner_apply, Real.norm_eq_abs, sq_abs]
    nlinarith [sq_nonneg (b-a)]
  have hm : IsMinOn f univ 0 := by intro t _; simp [f]; positivity
  have hA : ∀ y r δ, 0 < r → 0 < δ → ‖y-(0:ℝ)‖ ≤ r →
      f (A y r δ).1 - f 0 ≤ δ ∧ (A y r δ).2 ≤ φ (2*r^2/δ) := by
    intro y r δ hr hd hy
    let n := ⌈r^2/δ⌉₊+1
    have hn : 0 < n := Nat.succ_pos _
    have hnr : 0 < (n:ℝ) := Nat.cast_pos.mpr hn
    have ht : r^2/δ ≤ (n:ℝ) := (Nat.le_ceil (r^2/δ)).trans (by dsimp [n]; push_cast; linarith)
    have hrn : r^2 ≤ δ*n := by nlinarith [(div_le_iff₀ hd).mp ht]
    have hyr : ‖y‖^2 ≤ r^2 := by
      have hab : ‖y‖ ≤ r := by simpa using hy
      nlinarith [norm_nonneg y]
    have hv := GradientDescentRates.convex_value_le hf (strongConvexOn_zero.mp (StrongConvexOn.mono (by norm_num : (0:ℝ)≤1) hc))
      (by norm_num : (0:ℝ)<1/2) (by norm_num : (2:ℝ)*(1/2)≤1) hu y 0 hn
    constructor
    · have hz : ‖y‖^2 / (n:ℝ) ≤ δ := (div_le_iff₀ hnr).mpr (by nlinarith)
      have hv' : f (A y r δ).1 - f 0 ≤ ‖y‖^2/(n:ℝ) := by
        simpa [A, n, hg] using hv
      exact hv'.trans hz
    · have he : (2*r^2/δ)/2 = r^2/δ := by ring
      simp [A, φ, he]
  have hb := RestartLogComplexity.logarithmic_accuracy_and_cost hf hc
    (by norm_num : (0:ℝ)<1) (by norm_num : (0:ℝ)<2)
    (by norm_num : (0:ℝ)<1) hε hm (by norm_num : ‖(1:ℝ)-0‖ ≤ 1) A φ hA
  have hφ8 : φ (8*(2:ℝ)) = 9 := by norm_num [φ]
  have hφ1 : φ (2:ℝ) = 2 := by norm_num [φ]
  simp only [hφ8, hφ1, one_mul, one_pow, div_one, sub_zero, f,
    zero_pow (by decide : 2≠0), zero_div, Nat.cast_ofNat] at hb
  refine ⟨hb.2.1, hb.2.2.2.1, ?_, ?_, ?_⟩
  · simpa only [Nat.mul_comm] using hb.2.2.2.2.1
  · simpa only [A, mul_comm] using hb.2.2.2.2.2.1
  · intro he
    have hq : (4:ℝ) ≤ 1/ε := (le_div_iff₀ hε).mpr (by linarith)
    have ht := (hb.2.2.2.2.2.2 (by norm_num)).2 hq
    convert ht using 1
    ring

-- Positive and negative logarithmic regimes and the exact boundary.
example : ⌈Real.log ((4:ℝ)^3) / Real.log 4⌉₊ = 3 := by
  rw [Real.log_pow, mul_div_cancel_right₀ _ (ne_of_gt (Real.log_pos (by norm_num : (1:ℝ)<4)))]
  norm_num
example : ⌈Real.log (1/4:ℝ) / Real.log 4⌉₊ = 0 := by
  apply Nat.ceil_eq_zero.mpr
  exact div_nonpos_of_nonpos_of_nonneg (Real.log_nonpos (by norm_num) (by norm_num))
    (Real.log_nonneg (by norm_num))
example : ⌈Real.log (1:ℝ) / Real.log 4⌉₊ = 0 := by simp

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.RestartLogComplexity.logarithmic_accuracy_and_cost
