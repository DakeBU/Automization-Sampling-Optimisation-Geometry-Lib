import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticGradientDescent
import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep
import Mathlib.Analysis.Calculus.Deriv.Pow

/-!
# Sharp constant-step distance bounds witnessed by genuine quadratics

Chewi arXiv:2605.07006v1 Exercise3.3, testing the bound of Exercise3.2.
For each fixed step choose a scalar endpoint curvature. The parameters are
bounds defining the function class, not both tight constants of the witness.
The witness works for every iteration count. No adaptive-step or general
first-order oracle lower bound, or full Section3 sharpness claim, is made.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentSharpness

open Set InnerProductSpace
open QuadraticGradientDescent GradientDescentOptimalStep

/-- Every fixed step has a positive scalar quadratic attaining the endpoint
max-envelope at every iteration count; the balanced step attains its minimax
factor on the same witness. The curvature parameters are class bounds. -/
theorem exists_quadratic_worst_case {α β : ℝ} (hα : 0 < α) (hαβ : α ≤ β) (h : ℝ) :
    ∃ μ : ℝ, (μ = α ∨ μ = β) ∧ 0 < μ ∧
      let f : ℝ → ℝ := fun x => μ * x ^ 2 / 2
      ContDiff ℝ 2 f ∧ StrongConvexOn univ α f ∧
      (∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2) ∧
      IsMinOn f univ 0 ∧
      ∀ N : ℕ,
        ‖(fun x => x - h * gradient f x)^[N] 1‖ = (max |1 - h * α| |1 - h * β|) ^ N ∧
        ((β - α) / (α + β)) ^ N ≤ ‖(fun x => x - h * gradient f x)^[N] 1‖ ∧
        ‖(fun x => x - (2 / (α + β)) * gradient f x)^[N] 1‖ =
          ((β - α) / (α + β)) ^ N := by
  obtain ⟨μ, hm, he⟩ : ∃ μ : ℝ, (μ = α ∨ μ = β) ∧
      |1 - h * μ| = max |1 - h * α| |1 - h * β| := by
    by_cases hc : |1 - h * α| ≤ |1 - h * β|
    · exact ⟨β, Or.inr rfl, (max_eq_right hc).symm⟩
    · exact ⟨α, Or.inl rfl, (max_eq_left (le_of_not_ge hc)).symm⟩
  have ham : α ≤ μ := by rcases hm with rfl | rfl <;> order
  have hmb : μ ≤ β := by rcases hm with rfl | rfl <;> order
  have hmpos : 0 < μ := hα.trans_le ham
  let f : ℝ → ℝ := fun x => μ * x ^ 2 / 2
  have hf : ContDiff ℝ 2 f := (contDiff_const.mul (contDiff_id.pow 2)).div_const 2
  have hg (x : ℝ) : gradient f x = μ * x := by
    have hd : HasDerivAt f (μ * x) x := by
      convert (((hasDerivAt_id x).pow 2).const_mul μ).div_const (2 : ℝ) using 1 <;> first | rfl | (simp only [id_eq]; ring)
    exact hd.hasGradientAt.gradient
  have hc : StrongConvexOn univ α f := by
    apply StrongConvexOn.mono ham
    rw [strongConvexOn_iff_convex]
    have hz : (fun x : ℝ => f x - μ / 2 * ‖x‖ ^ 2) = fun _ => 0 := by
      funext x; simp [f, Real.norm_eq_abs, sq_abs]; ring
    rw [hz]; exact convexOn_const _ convex_univ
  have hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2 := by
    intro x y
    rw [hg]; simp only [f, Real.inner_apply, Real.norm_eq_abs, sq_abs]
    nlinarith [mul_nonneg (sub_nonneg.mpr hmb) (sq_nonneg (y-x))]
  have hmin : IsMinOn f univ 0 := by
    intro x _
    change μ * (0 : ℝ) ^ 2 / 2 ≤ μ * x ^ 2 / 2
    simpa using div_nonneg (mul_nonneg hmpos.le (sq_nonneg x)) (by norm_num : (0 : ℝ) ≤ 2)
  have hn (t : ℝ) (N : ℕ) :
      ‖(fun x => x - t * gradient f x)^[N] 1‖ = |1 - t * μ| ^ N := by
    have hs : (μ • (1 : ℝ →L[ℝ] ℝ)).IsSymmetric := by
      intro x y; simp [mul_comm, mul_left_comm]
    have heig : (μ • (1 : ℝ →L[ℝ] ℝ)) 1 = μ • (1 : ℝ) := by simp
    have hr := (quadratic_eigenmode (μ • (1 : ℝ →L[ℝ] ℝ)) hs heig t N).2.1
    have heq : (fun z : ℝ => inner ℝ z ((μ • (1 : ℝ →L[ℝ] ℝ)) z) / 2) = f := by
      funext z; simp [f]; ring
    simpa only [heq, smul_eq_mul, norm_one, mul_one] using hr
  have hβ : 0 < β := hα.trans_le hαβ
  have hD : 0 < α + β := add_pos hα hβ
  have hq : 0 ≤ (β - α) / (α + β) := div_nonneg (sub_nonneg.mpr hαβ) hD.le
  have hlow := (optimal_gradient_step hf hc hα.le hβ hαβ hu 0 1).2 h
  have hbal : |1 - 2 / (α + β) * μ| = (β - α) / (α + β) := by
    rcases hm with hma | hmb
    · rw [hma]
      have ha : 1 - 2 / (α + β) * α = (β - α) / (α + β) := by field_simp; ring
      rw [ha, abs_of_nonneg hq]
    · rw [hmb]
      have hb : 1 - 2 / (α + β) * β = -((β - α) / (α + β)) := by field_simp; ring
      rw [hb, abs_neg, abs_of_nonneg hq]
  refine ⟨μ, hm, hmpos, hf, hc, hu, hmin, ?_⟩
  intro N
  rw [hn h N, hn (2 / (α + β)) N, he, hbal]
  exact ⟨rfl, pow_le_pow_left₀ hq hlow N, rfl⟩

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentSharpness
