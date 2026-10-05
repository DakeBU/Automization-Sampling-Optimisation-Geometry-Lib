import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.Basic
import Mathlib.Topology.Algebra.Polynomial
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Analysis.Calculus.Deriv.Polynomial
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

noncomputable section
open Polynomial Polynomial.Chebyshev
namespace WeightMoments
private def F (n : ℤ) (x : ℝ) : ℝ :=
  (T ℝ (n+1)).eval x/(2*((n : ℝ)+1)) - (T ℝ (n-1)).eval x/(2*((n : ℝ)-1))

private theorem F_hasDeriv {n : ℤ} (hp : n≠-1) (hm : n≠1) (x : ℝ) :
    HasDerivAt (F n) ((T ℝ n).eval x) x := by
  have hpI : n+1≠0 := by omega
  have hmI : n-1≠0 := by omega
  have hpR : (n : ℝ)+1≠0 := by exact_mod_cast hpI
  have hmR : (n : ℝ)-1≠0 := by exact_mod_cast hmI
  have hU : (U ℝ n).eval x = 2*(T ℝ n).eval x+(U ℝ (n-2)).eval x := by
    have h := congrArg (fun p : ℝ[X] => p.eval x) (U_eq_two_mul_T_add_U ℝ (n-2))
    simpa only [show n-2+2=n by omega, Polynomial.eval_add,Polynomial.eval_mul,Polynomial.eval_ofNat] using h
  have hd := (((T ℝ (n+1)).hasDerivAt x).div_const (2*((n : ℝ)+1))).sub
    (((T ℝ (n-1)).hasDerivAt x).div_const (2*((n : ℝ)-1)))
  have hslope : ((T ℝ (n+1)).derivative.eval x)/(2*((n : ℝ)+1)) -
      ((T ℝ (n-1)).derivative.eval x)/(2*((n : ℝ)-1)) = (T ℝ n).eval x := by
    simp only [T_derivative_eq_U,Polynomial.eval_mul,Polynomial.eval_add,Polynomial.eval_sub,Polynomial.eval_one,Polynomial.eval_intCast,Int.cast_add,Int.cast_sub,Int.cast_one,
      show n+1-1=n by omega,show n-1-1=n-2 by omega]
    have h1 : ((n : ℝ)+1)*(U ℝ n).eval x/(2*((n : ℝ)+1)) = (U ℝ n).eval x/2 := by field_simp
    have h2 : ((n : ℝ)-1)*(U ℝ (n-2)).eval x/(2*((n : ℝ)-1)) = (U ℝ (n-2)).eval x/2 := by field_simp
    rw [h1,h2,hU]
    ring
  simpa only [F,Pi.sub_apply,hslope] using! hd

private theorem integral_T_endpoint {n : ℤ} (hp : n≠-1) (hm : n≠1) :
    (∫ x in (-1 : ℝ)..1, (T ℝ n).eval x) = F n 1-F n (-1) := by
  exact intervalIntegral.integral_eq_sub_of_hasDerivAt (fun x _ => F_hasDeriv hp hm x)
    ((T ℝ n).continuous.intervalIntegrable _ _)

private theorem integral_T_formula {n : ℤ} (hp : n≠-1) (hm : n≠1) :
    (∫ x in (-1 : ℝ)..1, (T ℝ n).eval x) =
      (1+(n.negOnePow : ℝ))/(1-(n : ℝ)^2) := by
  have hpI : n+1≠0 := by omega
  have hmI : n-1≠0 := by omega
  have hpR : (n : ℝ)+1≠0 := by exact_mod_cast hpI
  have hmR : (n : ℝ)-1≠0 := by exact_mod_cast hmI
  have hden : 1-(n : ℝ)^2≠0 := by
    have hf : 1-(n : ℝ)^2 = -((n : ℝ)+1)*((n : ℝ)-1) := by ring
    rw [hf]
    exact mul_ne_zero (neg_ne_zero.mpr hpR) hmR
  have hplus : ((n+1).negOnePow : ℝ) = -(n.negOnePow : ℝ) := by
    simp [Int.negOnePow_add]
  have hminus : ((n-1).negOnePow : ℝ) = -(n.negOnePow : ℝ) := by
    simp [Int.negOnePow_sub]
  rw [integral_T_endpoint hp hm]
  simp only [F,T_eval_one,T_eval_neg_one,hplus,hminus]
  field_simp
  ring

private def I (n : ℕ) : ℝ := ∫ x in (-1 : ℝ)..1, (T ℝ (n : ℤ)).eval x

private theorem I_zero : I 0=2 := by
  norm_num [I]

private theorem I_one : I 1=0 := by
  norm_num [I,integral_id]

private theorem I_odd {n : ℕ} (hn : Odd n) : I n=0 := by
  by_cases he : n=1
  · subst n; exact I_one
  have hp : (n : ℤ)≠-1 := by omega
  have hm : (n : ℤ)≠1 := by exact_mod_cast he
  have ho : Odd (n : ℤ) := by
    rcases hn with ⟨k,hk⟩
    exact ⟨k,by exact_mod_cast hk⟩
  unfold I
  rw [integral_T_formula hp hm,Int.negOnePow_odd _ ho]
  norm_num

private theorem I_even {n : ℕ} (hn : Even n) (hn2 : 2 ≤ n) :
    I n = -(2/((n : ℝ)^2-1)) := by
  have hp : (n : ℤ)≠-1 := by omega
  have hm : (n : ℤ)≠1 := by omega
  have he : Even (n : ℤ) := by
    rcases hn with ⟨k,hk⟩
    exact ⟨k,by exact_mod_cast hk⟩
  unfold I
  rw [integral_T_formula hp hm,Int.negOnePow_even _ he]
  norm_num only [Int.cast_natCast,Units.val_one,Int.cast_one,one_add_one_eq_two]
  have hden : 1-(n : ℝ)^2 = -((n : ℝ)^2-1) := by ring
  rw [hden,div_neg_eq_neg_div]

private theorem abs_I_even {n : ℕ} (hn : Even n) (hn2 : 2 ≤ n) :
    |I n| = 2/((n : ℝ)^2-1) := by
  have hnR : (2 : ℝ) ≤ n := by exact_mod_cast hn2
  have hden : 0<(n : ℝ)^2-1 := by nlinarith
  rw [I_even hn hn2,abs_neg,abs_of_pos (div_pos (by norm_num) hden)]

private def A (n : ℕ) : ℝ := ∑ j ∈ Finset.range n, |I (j+1)|

private theorem A_formula (n : ℕ) :
    A n = if Even n then 1-1/((n : ℝ)+1) else 1-1/(n : ℝ) := by
  induction n using Nat.twoStepInduction with
  | zero => norm_num [A]
  | one => norm_num [A,I_one]
  | more n ih0 ih1 =>
    have hrec : A (n+2)=A n+|I (n+1)|+|I (n+2)| := by
      simp only [A,Finset.sum_range_succ]
    rw [hrec,ih0]
    by_cases hn : Even n
    · have hodd : Odd (n+1) := by exact hn.add_odd (by decide : Odd 1)
      have heven : Even (n+2) := hn.add (by decide : Even 2)
      rw [if_pos hn,if_pos heven,I_odd hodd,abs_zero,add_zero,abs_I_even heven (by omega)]
      have hnR : 0 ≤ (n : ℝ) := Nat.cast_nonneg n
      push_cast
      have hf : ((n : ℝ)+2)^2-1 = ((n : ℝ)+1)*((n : ℝ)+3) := by ring
      have h1 : (n : ℝ)+1≠0 := by positivity
      have h3 : (n : ℝ)+3≠0 := by positivity
      rw [hf]
      field_simp [h1,h3]
      ring
    · have hodd : Odd n := Nat.not_even_iff_odd.mp hn
      have heven : Even (n+1) := hodd.add_odd (by decide : Odd 1)
      have ho : Odd (n+2) := hodd.add_even (by decide : Even 2)
      have hn0 : 0<n := by rcases hodd with ⟨k,hk⟩; omega
      rw [if_neg hn,if_neg (Nat.not_even_iff_odd.mpr ho),abs_I_even heven (by omega),I_odd ho,abs_zero,add_zero]
      have hnR : 0<(n : ℝ) := by exact_mod_cast hn0
      push_cast
      have hf : ((n : ℝ)+1)^2-1 = (n : ℝ)*((n : ℝ)+2) := by ring
      have h0 : (n : ℝ)≠0 := ne_of_gt hnR
      have h2 : (n : ℝ)+2≠0 := by positivity
      rw [hf]
      field_simp [h0,h2]
      ring

private theorem A_lt_one (n : ℕ) : A n<1 := by
  rw [A_formula]
  by_cases hn : Even n
  · rw [if_pos hn]
    have hp : 0<1/((n : ℝ)+1) := by positivity
    linarith
  · rw [if_neg hn]
    have hn0 : 0<n := by
      rcases Nat.not_even_iff_odd.mp hn with ⟨k,hk⟩
      omega
    have hnR : 0<(n : ℝ) := by exact_mod_cast hn0
    have hp : 0<1/(n : ℝ) := by positivity
    linarith

#print axioms A_lt_one
#print axioms integral_T_formula
#print axioms F_hasDeriv
#print axioms integral_T_endpoint
end WeightMoments
