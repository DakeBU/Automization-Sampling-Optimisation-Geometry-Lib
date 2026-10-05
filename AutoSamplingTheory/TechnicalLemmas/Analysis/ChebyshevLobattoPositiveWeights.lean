import AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Complex
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.Extremal
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Push
import Mathlib.Tactic.Tauto
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.Basic
import Mathlib.Topology.Algebra.Polynomial
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.Calculus.Deriv.Polynomial
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-! Actual Chebyshev-Lobatto momentum integral positivity.

SPHMC arXiv:2609.06906v1 Appendix B.1, Proposition B.1(B2), uses
nonnegative Clenshaw-Curtis weights in Lemma 4.6. We derive the actual
ordinary-Lebesgue integral weights from finite cosine interpolation,
Chebyshev antiderivatives, and exact affine scaling. All J>=2 and h>0
are covered, including both endpoint factors and both degree parities.
No positive-weight or closed-form certificate is supplied as a premise.
The logarithmic Lebesgue bound, Banach interpolation error, averaged
Hessian construction and discrete kinetic contraction remain separate.
-/

noncomputable section
open Finset Polynomial
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoPositiveWeights
private def C (n : ℕ) (a : ℝ) : ℝ :=
  2 * (∑ j ∈ range (n+1), Real.cos ((j : ℝ)*a)) - 1 - Real.cos ((n : ℝ)*a)

private theorem sine_C (n : ℕ) (a : ℝ) :
    Real.sin (a/2) * C n a = Real.cos (a/2) * Real.sin ((n : ℝ)*a) := by
  have hterm (j : ℕ) :
      2 * Real.sin (a/2) * Real.cos ((j : ℝ)*a) =
        Real.sin (((j+1 : ℕ) : ℝ)*a-a/2) - Real.sin ((j : ℝ)*a-a/2) := by
    rw [Real.sin_sub_sin]
    push_cast
    ring_nf
  have hsum : 2 * Real.sin (a/2) * (∑ j ∈ range (n+1), Real.cos ((j : ℝ)*a)) =
      Real.sin (((n+1 : ℕ) : ℝ)*a-a/2) + Real.sin (a/2) := by
    rw [mul_sum]
    simp_rw [hterm]
    rw [sum_range_sub (fun j : ℕ => Real.sin ((j : ℝ)*a-a/2))]
    simp only [Nat.cast_zero, zero_mul, zero_sub, Real.sin_neg, sub_neg_eq_add]
  have harg : ((n+1 : ℕ) : ℝ)*a-a/2 = (n : ℝ)*a+a/2 := by push_cast; ring
  rw [harg,Real.sin_add] at hsum
  dsimp [C]
  nlinarith [hsum]

private theorem C_even (n : ℕ) (a : ℝ) : C n (-a) = C n a := by
  simp [C, mul_neg,Real.cos_neg]

private theorem C_zero (n : ℕ) : C n 0 = 2*(n : ℝ) := by
  simp [C]
  ring

private theorem C_two_pi (n : ℕ) : C n (2*Real.pi) = 2*(n : ℝ) := by
  simp [C, Real.cos_nat_mul_two_pi]
  ring

private theorem C_index {n : ℕ} (hn : 0<n) {k : ℕ} (hk : k ≤ 2*n) :
    C n ((k : ℝ)*Real.pi/n) = if k=0 ∨ k=2*n then 2*(n : ℝ) else 0 := by
  have hnR : 0<(n : ℝ) := by exact_mod_cast hn
  have hn0 : (n : ℝ)≠0 := ne_of_gt hnR
  by_cases h0 : k=0
  · subst k
    simpa using C_zero n
  by_cases he : k=2*n
  · subst k
    have ha : ((2*n : ℕ) : ℝ)*Real.pi/n = 2*Real.pi := by push_cast; field_simp
    rw [ha,C_two_pi]
    simp
  rw [if_neg (by tauto)]
  have hkR : (k : ℝ)<2*n := by exact_mod_cast (lt_of_le_of_ne hk he)
  have hk0 : 0<(k : ℝ) := by exact_mod_cast (Nat.pos_of_ne_zero h0)
  have ha0 : 0<((k : ℝ)*Real.pi/n)/2 := by positivity
  have ha1 : ((k : ℝ)*Real.pi/n)/2<Real.pi := by
    apply (div_lt_iff₀ (by norm_num : (0 : ℝ)<2)).mpr
    apply (div_lt_iff₀ hnR).mpr
    nlinarith [Real.pi_pos]
  have hs := ne_of_gt (Real.sin_pos_of_pos_of_lt_pi ha0 ha1)
  have h := sine_C n ((k : ℝ)*Real.pi/n)
  have ha : (n : ℝ)*((k : ℝ)*Real.pi/n) = (k : ℝ)*Real.pi := by field_simp
  rw [ha,Real.sin_nat_mul_pi,mul_zero] at h
  exact (mul_eq_zero.mp h).resolve_left hs

private theorem C_difference {n : ℕ} (hn : 0<n) {i j : ℕ} (hi : i ≤ n) (hj : j ≤ n) :
    C n ((i : ℝ)*Real.pi/n-(j : ℝ)*Real.pi/n) = if i=j then 2*(n : ℝ) else 0 := by
  by_cases he : i=j
  · subst j
    simp [C_zero]
  rw [if_neg he]
  by_cases hji : j ≤ i
  · have hm : i-j ≤ 2*n := by omega
    have ha : (i : ℝ)*Real.pi/n-(j : ℝ)*Real.pi/n = ((i-j : ℕ) : ℝ)*Real.pi/n := by
      rw [Nat.cast_sub hji]
      ring
    rw [ha,C_index hn hm,if_neg (by omega)]
  · have hij : i ≤ j := by omega
    have hm : j-i ≤ 2*n := by omega
    have ha : (i : ℝ)*Real.pi/n-(j : ℝ)*Real.pi/n = -(((j-i : ℕ) : ℝ)*Real.pi/n) := by
      rw [Nat.cast_sub hij]
      ring
    rw [ha,C_even,C_index hn hm,if_neg (by omega)]

private theorem C_sum {n : ℕ} (hn : 0<n) {i j : ℕ} (hi : i ≤ n) (hj : j ≤ n) :
    C n ((i : ℝ)*Real.pi/n+(j : ℝ)*Real.pi/n) =
      if i=j ∧ (i=0 ∨ i=n) then 2*(n : ℝ) else 0 := by
  have ha : (i : ℝ)*Real.pi/n+(j : ℝ)*Real.pi/n = ((i+j : ℕ) : ℝ)*Real.pi/n := by
    push_cast
    ring
  rw [ha,C_index hn (by omega : i+j ≤ 2*n)]
  have he : i+j=0 ∨ i+j=2*n ↔ i=j ∧ (i=0 ∨ i=n) := by omega
  simp only [he]

private def D (n : ℕ) (a b : ℝ) : ℝ :=
  2*(∑ j ∈ range (n+1), Real.cos ((j : ℝ)*a)*Real.cos ((j : ℝ)*b)) - 1 -
    Real.cos ((n : ℝ)*a)*Real.cos ((n : ℝ)*b)

private theorem D_formula (n : ℕ) (a b : ℝ) :
    2*D n a b = C n (a-b)+C n (a+b) := by
  have ht (j : ℕ) : Real.cos ((j : ℝ)*(a-b))+Real.cos ((j : ℝ)*(a+b)) =
      2*Real.cos ((j : ℝ)*a)*Real.cos ((j : ℝ)*b) := by
    rw [mul_sub,mul_add,Real.cos_sub,Real.cos_add]
    ring
  have hsum : (∑ j ∈ range (n+1),Real.cos ((j : ℝ)*(a-b))) +
      (∑ j ∈ range (n+1),Real.cos ((j : ℝ)*(a+b))) =
      2*(∑ j ∈ range (n+1),Real.cos ((j : ℝ)*a)*Real.cos ((j : ℝ)*b)) := by
    rw [←sum_add_distrib]
    simp_rw [ht]
    rw [mul_sum]
    apply sum_congr rfl
    intro j _
    ring
  dsimp [C,D]
  nlinarith [ht n,hsum]

private theorem D_cardinal {n : ℕ} (hn : 0<n) {i j : ℕ} (hi : i ≤ n) (hj : j ≤ n) :
    (if i=0 ∨ i=n then (1 : ℝ) else 2)/(2*(n : ℝ)) *
      D n ((i : ℝ)*Real.pi/n) ((j : ℝ)*Real.pi/n) = if i=j then 1 else 0 := by
  have h := D_formula n ((i : ℝ)*Real.pi/n) ((j : ℝ)*Real.pi/n)
  rw [C_difference hn hi hj,C_sum hn hi hj] at h
  have hnR : (n : ℝ)≠0 := by exact_mod_cast (Nat.ne_of_gt hn)
  by_cases he : i=j
  · rw [if_pos he] at h ⊢
    by_cases hend : i=0 ∨ i=n
    · rw [if_pos hend]
      rw [if_pos ⟨he,hend⟩] at h
      have hd : D n ((i : ℝ)*Real.pi/n) ((j : ℝ)*Real.pi/n) = 2*(n : ℝ) := by linarith
      rw [hd]
      field_simp
    · rw [if_neg hend]
      rw [if_neg (by tauto : ¬(i=j ∧ (i=0 ∨ i=n)))] at h
      have hd : D n ((i : ℝ)*Real.pi/n) ((j : ℝ)*Real.pi/n) = (n : ℝ) := by linarith
      rw [hd]
      field_simp
  · rw [if_neg he,if_neg (by tauto : ¬(i=j ∧ (i=0 ∨ i=n)))] at h
    have hd : D n ((i : ℝ)*Real.pi/n) ((j : ℝ)*Real.pi/n) = 0 := by linarith
    rw [hd,if_neg he,mul_zero]

private def cardinalPoly (n i : ℕ) : ℝ[X] :=
  Polynomial.C ((if i=0 ∨ i=n then (1 : ℝ) else 2)/(2*(n : ℝ))) *
    (Polynomial.C 2 * (∑ j ∈ range (n+1),
      Polynomial.C (Real.cos ((j : ℝ)*((i : ℝ)*Real.pi/n))) * Polynomial.Chebyshev.T ℝ (j : ℤ)) -
      1 - Polynomial.C (Real.cos ((n : ℝ)*((i : ℝ)*Real.pi/n))) * Polynomial.Chebyshev.T ℝ (n : ℤ))

private theorem cardinalPoly_eval {n : ℕ} (hn : 0<n) {i j : ℕ} (hi : i ≤ n) (hj : j ≤ n) :
    (cardinalPoly n i).eval (Real.cos ((j : ℝ)*Real.pi/n)) = if i=j then 1 else 0 := by
  simpa only [cardinalPoly,D,Polynomial.eval_mul,Polynomial.eval_sub,Polynomial.eval_C,
    Polynomial.eval_finsetSum,Polynomial.eval_one,Polynomial.Chebyshev.T_real_cos,Int.cast_natCast]
    using D_cardinal hn hi hj

private theorem cardinalPoly_natDegree (n i : ℕ) : (cardinalPoly n i).natDegree ≤ n := by
  have hsum : (∑ j ∈ range (n+1),
      Polynomial.C (Real.cos ((j : ℝ)*((i : ℝ)*Real.pi/n))) * Polynomial.Chebyshev.T ℝ (j : ℤ)).natDegree ≤ n := by
    apply Polynomial.natDegree_sum_le_of_forall_le
    intro j hj
    apply (Polynomial.natDegree_C_mul_le _ _).trans
    simpa only [Polynomial.Chebyshev.natDegree_T,Int.natAbs_natCast] using (Nat.le_of_lt_succ (mem_range.mp hj))
  have hlast : (Polynomial.C (Real.cos ((n : ℝ)*((i : ℝ)*Real.pi/n))) * Polynomial.Chebyshev.T ℝ (n : ℤ)).natDegree ≤ n := by
    apply (Polynomial.natDegree_C_mul_le _ _).trans
    simp only [Polynomial.Chebyshev.natDegree_T,Int.natAbs_natCast,le_rfl]
  unfold cardinalPoly
  apply (Polynomial.natDegree_C_mul_le _ _).trans
  apply (Polynomial.natDegree_sub_le _ _).trans
  apply max_le
  · apply (Polynomial.natDegree_sub_le _ _).trans
    apply max_le
    · exact (Polynomial.natDegree_C_mul_le _ _).trans hsum
    · simp
  · exact hlast

end AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoPositiveWeights

noncomputable section
open Polynomial Polynomial.Chebyshev
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoPositiveWeights.Moments
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

end AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoPositiveWeights.Moments
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoPositiveWeights
open Moments MeasureTheory

private theorem cardinal_integral_formula (n i : ℕ) :
    (∫ x in (-1 : ℝ)..1, (cardinalPoly n i).eval x) =
      ((if i=0 ∨ i=n then (1 : ℝ) else 2)/(2*(n : ℝ))) *
        (2*(∑ j ∈ range (n+1), Real.cos ((j : ℝ)*((i : ℝ)*Real.pi/n))*I j) -
          2 - Real.cos ((n : ℝ)*((i : ℝ)*Real.pi/n))*I n) := by
  let c := fun j : ℕ => Real.cos ((j : ℝ)*((i : ℝ)*Real.pi/n))
  let Q := ∑ j ∈ range (n+1), Polynomial.C (c j)*Polynomial.Chebyshev.T ℝ (j : ℤ)
  have hintQ : IntervalIntegrable (fun x : ℝ => Q.eval x) volume (-1) 1 :=
    Q.continuous.intervalIntegrable _ _
  have hintOne : IntervalIntegrable (fun _ : ℝ => (1 : ℝ)) volume (-1) 1 :=
    continuous_const.intervalIntegrable _ _
  have hintT : IntervalIntegrable (fun x : ℝ => (Polynomial.Chebyshev.T ℝ (n : ℤ)).eval x) volume (-1) 1 :=
    (Polynomial.Chebyshev.T ℝ (n : ℤ)).continuous.intervalIntegrable _ _
  have hQ : (∫ x in (-1 : ℝ)..1, Q.eval x) = ∑ j ∈ range (n+1), c j*I j := by
    simp_rw [Q,Polynomial.eval_finsetSum]
    rw [intervalIntegral.integral_finsetSum]
    · simp_rw [Polynomial.eval_mul,Polynomial.eval_C,intervalIntegral.integral_const_mul,I]
    · intro j _
      exact (Polynomial.C (c j)*Polynomial.Chebyshev.T ℝ (j : ℤ)).continuous.intervalIntegrable _ _
  change (∫ x in (-1 : ℝ)..1,
    (Polynomial.C ((if i=0 ∨ i=n then (1 : ℝ) else 2)/(2*(n : ℝ))) *
      (Polynomial.C 2*Q-1-Polynomial.C (c n)*Polynomial.Chebyshev.T ℝ (n : ℤ))).eval x) = _
  simp only [Polynomial.eval_sub,Polynomial.eval_mul,Polynomial.eval_C,Polynomial.eval_one]
  rw [intervalIntegral.integral_const_mul,
    intervalIntegral.integral_sub ((hintQ.const_mul 2).sub hintOne) (hintT.const_mul (c n)),
    intervalIntegral.integral_sub (hintQ.const_mul 2) hintOne,
    intervalIntegral.integral_const_mul,intervalIntegral.integral_const_mul,hQ]
  norm_num only [intervalIntegral.integral_const,smul_eq_mul,mul_one]
  rfl

private theorem cos_mul_moment_ge (k : ℕ) (a : ℝ) :
    -|I k| ≤ Real.cos a*I k := by
  have hc : |Real.cos a| ≤ 1 := abs_le.mpr ⟨Real.neg_one_le_cos a,Real.cos_le_one a⟩
  have hab : |Real.cos a*I k| ≤ |I k| := by
    rw [abs_mul]
    simpa only [one_mul] using mul_le_mul_of_nonneg_right hc (abs_nonneg (I k))
  exact (neg_le_neg hab).trans (neg_abs_le (Real.cos a*I k))

private theorem cardinal_integral_positive_succ (k i : ℕ) :
    0<(∫ x in (-1 : ℝ)..1, (cardinalPoly (k+1) i).eval x) := by
  let n := k+1
  let a := (i : ℝ)*Real.pi/n
  let S := ∑ j ∈ range k, Real.cos (((j+1 : ℕ) : ℝ)*a)*I (j+1)
  have hS : -A k ≤ S := by
    have h := sum_le_sum (fun j (_ : j∈range k) => cos_mul_moment_ge (j+1) (((j+1 : ℕ) : ℝ)*a))
    simpa only [sum_neg_distrib,A,S] using h
  have hEnd := cos_mul_moment_ge n ((n : ℝ)*a)
  have hA : A n=A k+|I n| := by simp only [n,A,sum_range_succ]
  have hsmall := A_lt_one n
  have habs := abs_nonneg (I n)
  have hbr : 0<2+2*S+Real.cos ((n : ℝ)*a)*I n := by
    nlinarith
  have hs : (∑ j ∈ range (n+1),Real.cos ((j : ℝ)*a)*I j) =
      2+S+Real.cos ((n : ℝ)*a)*I n := by
    rw [show n+1=(k+1)+1 from rfl,sum_range_succ,sum_range_succ']
    simp only [Nat.cast_zero,zero_mul,Real.cos_zero,one_mul,I_zero]
    dsimp only [S,n]
    ring
  have hnR : 0<(n : ℝ) := by dsimp [n]; positivity
  have hp : 0<(if i=0 ∨ i=n then (1 : ℝ) else 2)/(2*(n : ℝ)) := by
    split_ifs <;> positivity
  rw [cardinal_integral_formula]
  change 0<((if i=0 ∨ i=n then (1 : ℝ) else 2)/(2*(n : ℝ))) *
    (2*(∑ j ∈ range (n+1),Real.cos ((j : ℝ)*a)*I j)-2-Real.cos ((n : ℝ)*a)*I n)
  rw [hs]
  apply mul_pos hp
  nlinarith [hbr]

private def scaledPoly (n i : ℕ) (h : ℝ) : ℝ[X] :=
  (cardinalPoly n i).comp (1-Polynomial.C (2/h)*Polynomial.X)

private theorem scaledPoly_eq_source {J : ℕ} (hJ : 2 ≤ J) {h : ℝ} (hh : 0<h)
    (i : Fin J) :
    scaledPoly (J-1) i h = Lagrange.basis univ
      (fun j : Fin J => h/2*(1-Real.cos ((j : ℝ)/(J-1 : ℝ)*Real.pi))) i := by
  classical
  let t := fun j : Fin J => h/2*(1-Real.cos ((j : ℝ)/(J-1 : ℝ)*Real.pi))
  have hinj : Function.Injective t :=
    (AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature.chebyshev_lobatto_coefficients hJ hh).2.1
  have hh0 : h ≠ 0 := ne_of_gt hh
  have hn : 0<J-1 := by omega
  have hnR : ((J-1 : ℕ) : ℝ) = (J : ℝ)-1 := by
    rw [Nat.cast_sub (by omega : 1 ≤ J),Nat.cast_one]
  have ha : (1-Polynomial.C (2/h)*Polynomial.X : ℝ[X]).natDegree ≤ 1 := by
    apply (Polynomial.natDegree_sub_le _ _).trans
    apply max_le
    · simp
    · simpa using Polynomial.natDegree_C_mul_le (2/h) (Polynomial.X : ℝ[X])
  have hdeg : (scaledPoly (J-1) i h).natDegree ≤ J-1 := by
    apply Polynomial.natDegree_comp_le.trans
    calc
      _ ≤ (J-1)*1 := Nat.mul_le_mul (cardinalPoly_natDegree (J-1) i) ha
      _ = J-1 := Nat.mul_one _
  apply Polynomial.eq_of_degrees_lt_of_eval_index_eq univ hinj.injOn
  · apply Polynomial.degree_le_natDegree.trans_lt
    simp only [Finset.card_univ,Fintype.card_fin]
    exact_mod_cast lt_of_le_of_lt hdeg (by omega : J-1<J)
  · rw [Lagrange.degree_basis hinj.injOn (mem_univ i)]
    simp only [Finset.card_univ,Fintype.card_fin]
    exact_mod_cast (by omega : J-1<J)
  · intro j _
    have hi : (i : ℕ) ≤ J-1 := by omega
    have hj : (j : ℕ) ≤ J-1 := by omega
    have heval : 1-(2/h)*t j = Real.cos ((j : ℝ)*Real.pi/((J-1 : ℕ) : ℝ)) := by
      dsimp only [t]
      rw [hnR]
      have hangle : (j : ℝ)/((J : ℝ)-1)*Real.pi = (j : ℝ)*Real.pi/((J : ℝ)-1) := by ring
      rw [hangle]
      field_simp
      ring
    change (scaledPoly (J-1) i h).eval (t j) = _
    simp only [scaledPoly,Polynomial.eval_comp,Polynomial.eval_sub,Polynomial.eval_one,
      Polynomial.eval_mul,Polynomial.eval_C,Polynomial.eval_X]
    rw [heval,cardinalPoly_eval hn hi hj]
    by_cases he : i=j
    · subst j
      simp only [ite_true]
      exact (Lagrange.eval_basis_self hinj.injOn (mem_univ i)).symm
    · rw [if_neg (by exact fun h => he (Fin.ext h))]
      exact (Lagrange.eval_basis_of_ne he (mem_univ j)).symm

private theorem scaledPoly_integral {h : ℝ} (hh : 0<h) (n i : ℕ) :
    (∫ s in (0 : ℝ)..h, (scaledPoly n i h).eval s) =
      (h/2)*(∫ x in (-1 : ℝ)..1, (cardinalPoly n i).eval x) := by
  have hh0 : h ≠ 0 := ne_of_gt hh
  simp only [scaledPoly,Polynomial.eval_comp,Polynomial.eval_sub,Polynomial.eval_one,
    Polynomial.eval_mul,Polynomial.eval_C,Polynomial.eval_X]
  rw [intervalIntegral.integral_comp_sub_mul (fun x : ℝ => (cardinalPoly n i).eval x)
    (by positivity : (2 : ℝ)/h ≠ 0) 1]
  have hend : 1-(2/h)*h = (-1 : ℝ) := by field_simp; ring
  rw [hend]
  simp only [mul_zero,sub_zero,smul_eq_mul]
  congr 1
  field_simp

/-- Actual source Chebyshev-Lobatto cardinal momentum integrals are nonnegative
for every number of nodes J>=2 and every positive duration h. -/
theorem nonnegative_momentum_weights {J : ℕ} (hJ : 2 ≤ J) {h : ℝ} (hh : 0<h) :
    let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
    let ell := fun j : Fin J => Lagrange.basis univ t j
    ∀ j, 0 ≤ ∫ s in (0 : ℝ)..h, (ell j).eval s := by
  dsimp only
  intro j
  rw [← scaledPoly_eq_source hJ hh j,scaledPoly_integral hh]
  obtain ⟨k,hk⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : J-1 ≠ 0)
  rw [hk]
  exact (mul_pos (by positivity : 0<h/2) (cardinal_integral_positive_succ k j)).le



end AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoPositiveWeights
