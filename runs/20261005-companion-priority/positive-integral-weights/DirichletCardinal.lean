import Mathlib.Analysis.SpecialFunctions.Trigonometric.Complex
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.Extremal
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Push
import Mathlib.Tactic.Tauto

noncomputable section
open Finset Polynomial
namespace WeightProof
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

private theorem cardinalPoly_eq_basis {n : ℕ} (hn : 0<n) (i : Fin (n+1)) :
    cardinalPoly n i = Lagrange.basis univ (fun j : Fin (n+1) => Real.cos ((j : ℝ)*Real.pi/n)) i := by
  classical
  let v := fun j : Fin (n+1) => Real.cos ((j : ℝ)*Real.pi/n)
  have hvi : Function.Injective v := by
    intro j k hjk
    have hv : ∀ j : Fin (n+1), v j = Polynomial.Chebyshev.node n j := by intro j; rfl
    have h := Polynomial.Chebyshev.strictAntiOn_node n
    exact Fin.ext (h.injOn (by simpa using j.isLt) (by simpa using k.isLt) (by simpa only [hv] using hjk))
  apply Polynomial.eq_of_degrees_lt_of_eval_index_eq univ hvi.injOn
  · apply (Polynomial.degree_le_natDegree).trans_lt
    simp only [Finset.card_univ,Fintype.card_fin]
    exact_mod_cast lt_of_le_of_lt (cardinalPoly_natDegree n i) (Nat.lt_succ_self n)
  · rw [Lagrange.degree_basis hvi.injOn (mem_univ i)]
    simp only [Finset.card_univ,Fintype.card_fin,Nat.add_sub_cancel]
    exact_mod_cast Nat.lt_succ_self n
  · intro j _
    have hi : (i : ℕ) ≤ n := by omega
    have hj : (j : ℕ) ≤ n := by omega
    rw [cardinalPoly_eval hn hi hj]
    by_cases he : i=j
    · subst j
      simp only [ite_true]
      exact (Lagrange.eval_basis_self hvi.injOn (mem_univ i)).symm
    · rw [if_neg (by exact fun h => he (Fin.ext h))]
      exact (Lagrange.eval_basis_of_ne he (mem_univ j)).symm

#print axioms cardinalPoly_eq_basis
#print axioms D_cardinal
#print axioms sine_C
#print axioms C_index
end WeightProof
