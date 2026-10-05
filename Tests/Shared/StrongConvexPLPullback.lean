import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexPLPullback
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Analysis.Calculus.Deriv.Pow

open AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexPLPullback Set

set_option backward.isDefEq.respectTransparency false
set_option backward.isDefEq.respectTransparency.types false

private theorem quadratic_strong :
    StrongConvexOn univ (1 : ℝ) (fun t : ℝ => t ^ 2 / 2) := by
  rw [strongConvexOn_iff_convex]
  have heq : (fun t : ℝ => t ^ 2 / 2 - 1 / 2 * ‖t‖ ^ 2) = fun _ => 0 := by
    funext t
    simp [Real.norm_eq_abs, sq_abs]
    ring
  rw [heq]
  exact convexOn_const _ convex_univ

-- A genuinely nonlinear surjection with a nonconstant Jacobian.
-- All Jacobian/minimum certificates are established here, not test hypotheses.
example : ∃ xstar : ℝ, xstar + xstar ^ 3 = 0 ∧
    IsMinOn (fun x : ℝ => (x + x ^ 3) ^ 2 / 2) univ xstar ∧
    ∀ x : ℝ, (x + x ^ 3) ^ 2 ≤
      ‖gradient (fun t : ℝ => (t + t ^ 3) ^ 2 / 2) x‖ ^ 2 := by
  let g : ℝ → ℝ := fun x => x + x ^ 3
  have hd (x : ℝ) : HasDerivAt g (1 + 3 * x ^ 2) x := by
    convert (hasDerivAt_id x).add ((hasDerivAt_id x).pow 3) using 1 <;>
      first | rfl | (simp only [id_eq]; ring)
  have hc : Continuous g := continuous_id.add (continuous_id.pow 3)
  have hs : Function.Surjective g := by
    intro y
    by_cases hy : 0 ≤ y
    · have hm : y ∈ Icc (g 0) (g y) := by
        dsimp [g]
        constructor <;> nlinarith [pow_nonneg hy 3]
      obtain ⟨x, _, hx⟩ := intermediate_value_Icc hy hc.continuousOn hm
      exact ⟨x, hx⟩
    · have hy' : y ≤ 0 := le_of_not_ge hy
      have hm : y ∈ Icc (g y) (g 0) := by
        have hy3 : y ^ 3 ≤ 0 := by nlinarith [mul_nonpos_of_nonneg_of_nonpos (sq_nonneg y) hy']
        dsimp [g]
        constructor <;> nlinarith
      obtain ⟨x, _, hx⟩ := intermediate_value_Icc hy' hc.continuousOn hm
      exact ⟨x, hx⟩
  have hj (x v : ℝ) : 1 * ‖v‖ ^ 2 ≤
      inner ℝ v ((fderiv ℝ g x) ((fderiv ℝ g x).adjoint v)) := by
    have hA : fderiv ℝ g x = (1 + 3 * x ^ 2) • (1 : ℝ →L[ℝ] ℝ) := by
      rw [(hd x).hasFDerivAt.fderiv]
      ext
      simp [mul_comm]
    rw [hA]
    change 1 * ‖v‖ ^ 2 ≤ inner ℝ v
      (((1 + 3 * x ^ 2) • (ContinuousLinearMap.id ℝ ℝ))
        (((1 + 3 * x ^ 2) • (ContinuousLinearMap.id ℝ ℝ)).adjoint v))
    simp [Real.norm_eq_abs, sq_abs]
    nlinarith [sq_nonneg x, sq_nonneg v, mul_nonneg (sq_nonneg x) (sq_nonneg v),
      sq_nonneg (3 * x ^ 2 * v)]
  have hf : Differentiable ℝ (fun t : ℝ => t ^ 2 / 2) :=
    (differentiable_id.pow 2).div_const 2
  have hz : IsMinOn (fun t : ℝ => t ^ 2 / 2) univ 0 := by
    intro t _
    change (0 : ℝ) ^ 2 / 2 ≤ t ^ 2 / 2
    nlinarith [sq_nonneg t]
  obtain ⟨xstar, hxstar, hmin, hpl⟩ := exists_minimizer_and_pl
    (by norm_num : (0 : ℝ) < 1) (by norm_num : (0 : ℝ) ≤ 1)
    quadratic_strong hf (fun x => (hd x).differentiableAt) hs hz hj
  refine ⟨xstar, hxstar, hmin, ?_⟩
  intro x
  have hp := hpl x
  simp only [Function.comp_def, hxstar, zero_pow (by norm_num : 2 ≠ 0),
    zero_div, sub_zero, mul_one] at hp
  dsimp [g] at hp
  simp only [Real.norm_eq_abs] at ⊢
  nlinarith

#print axioms exists_minimizer_and_pl
