import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationTransfer
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Gradient.Basic

open Set
open AutoSamplingTheory.TechnicalLemmas.Analysis

-- A real gradient step for the regularized quadratic, at its reciprocal
-- smoothness, supplies an actual output without receiving the minimizer witness.
example (ε : ℝ) (hε : 0 < ε) :
    let W := fun x : ℝ => x^2/2 + ε/2*‖x-1‖^2
    let xout := (1:ℝ) - (1/(1+ε)) * gradient W 1
    ∃ w, IsMinOn W univ w ∧ ‖w-1‖ ≤ 1 ∧
      xout = ε/(1+ε) ∧ xout^2/2 ≤ ε := by
  let W := fun x : ℝ => x^2/2 + ε/2*‖x-1‖^2
  have hz : IsMinOn (fun x : ℝ => x^2/2) univ 0 := by
    intro x _; simp; positivity
  obtain ⟨w,hw,hr,ha⟩ := QuadraticRegularizationTransfer.exists_minimizer_radius_and_accuracy
    (f := fun x : ℝ => x^2/2) (by fun_prop) hz (by norm_num : (0:ℝ)<1) hε
    (by norm_num : ‖(0:ℝ)-1‖ ≤ 1)
  have hgrad : gradient W 1 = 1 := by
    have he : W = fun x : ℝ => x^2/2 + ε/2*(x-1)^2 := by
      funext x; simp [W, Real.norm_eq_abs, sq_abs]
    have hd : HasDerivAt W 1 1 := by
      rw [he]
      convert (((hasDerivAt_id (1:ℝ)).pow 2).div_const 2).add
        ((((hasDerivAt_id (1:ℝ)).sub_const 1).pow 2).const_mul (ε/2)) using 1 <;> norm_num <;> rfl
    exact hd.hasGradientAt.gradient
  let xout := (1:ℝ) - (1/(1+ε))*gradient W 1
  have hp : 0 < 1+ε := by linarith
  have hout : xout = ε/(1+ε) := by dsimp [xout]; rw [hgrad]; field_simp; ring
  have hmin : ∀ y, W xout ≤ W y := by
    intro y
    have hs := sq_nonneg (y-ε/(1+ε))
    have hid : W y - W xout = (1+ε)/2*(y-ε/(1+ε))^2 := by
      rw [hout]; dsimp [W]; simp only [sq_abs]
      field_simp
      ring
    have hn : 0 ≤ W y - W xout := by rw [hid]; positivity
    linarith
  have hgap : W xout - W w ≤ ε/2 := by linarith [hmin w]
  have hacc : xout^2/2 ≤ ε := by
    simpa using ha xout (by simpa only [one_pow, div_one] using hgap)
  refine ⟨w, ?_, ?_, hout, hacc⟩
  · simpa only [one_pow, div_one] using hw
  · simpa using hr

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationTransfer.exists_minimizer_radius_and_accuracy
