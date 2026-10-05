import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentSharpness
import Mathlib.Algebra.Order.Ring.Pow

/-!
# Convex gradient-descent function-value order witnessed by quadratics

Chewi arXiv:2605.07006v1 Exercise3.3, testing Theorem3.4 at step `1 / β`.
The positive curvature is chosen after the horizon. This proves a class-level
order obstruction, not an exact optimal constant or a single fixed objective
with a reciprocal asymptotic tail. No general oracle lower bound is asserted.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexGradientGapSharpness

open Set InnerProductSpace GradientDescentSharpness

set_option backward.isDefEq.respectTransparency false in
/-- A horizon-dependent positive quadratic has an actual gradient-descent gap
of order `β / (N + 1)`. The smoothness bound `β` need not be tight. -/
theorem quadratic_gap_lower_bound {β : ℝ} (hβ : 0 < β) (N : ℕ) :
    let μ := β / (2 * ((N : ℝ) + 1))
    let f : ℝ → ℝ := fun x => μ * x ^ 2 / 2
    0 < μ ∧ ContDiff ℝ 2 f ∧ StrongConvexOn univ μ f ∧
      (∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2) ∧
      IsMinOn f univ 0 ∧
      let z := (fun x => x - (1 / β) * gradient f x)^[N] 1
      f z - f 0 = β / (4 * ((N : ℝ) + 1)) *
        (1 - 1 / (2 * ((N : ℝ) + 1))) ^ (2 * N) ∧
      β / (16 * ((N : ℝ) + 1)) ≤ f z - f 0 := by
  let D : ℝ := (N : ℝ) + 1
  have hD : 0 < D := by dsimp [D]; positivity
  have hD1 : 1 ≤ D := by dsimp [D]; exact le_add_of_nonneg_left (Nat.cast_nonneg N)
  let μ := β / (2 * D)
  have hμ : 0 < μ := div_pos hβ (by positivity)
  have hμβ : μ ≤ β := by
    apply (div_le_iff₀ (by positivity : 0 < 2 * D)).mpr
    nlinarith
  obtain ⟨ν, hν, _, hf, hc, hu, hm, hn⟩ :=
    exists_quadratic_worst_case hμ (le_refl μ) (1 / β)
  have hv : ν = μ := hν.elim id id
  subst ν
  let f : ℝ → ℝ := fun x => μ * x ^ 2 / 2
  let q : ℝ := 1 - 1 / (2 * D)
  have hq : 0 ≤ q := by
    have : 1 / (2 * D) ≤ 1 := (div_le_one (by positivity)).mpr (by linarith)
    dsimp [q]; linarith
  have he : 1 - 1 / β * μ = q := by
    dsimp [μ, q]; field_simp
  have hn' : ‖(fun x => x - (1 / β) * gradient f x)^[N] 1‖ = q ^ N := by
    simpa only [max_self, he, abs_of_nonneg hq] using (hn N).1
  have hpow : 1 / 2 ≤ q ^ N := by
    have hb := one_add_mul_sub_le_pow (by linarith : -1 ≤ q) N
    have heq : 1 + (N : ℝ) * (q - 1) = (D + 1) / (2 * D) := by
      dsimp [q, D]; field_simp; ring
    rw [heq] at hb
    have : (1 : ℝ) / 2 ≤ (D + 1) / (2 * D) := by
      apply (le_div_iff₀ (by positivity)).mpr
      linarith
    exact this.trans hb
  have huβ : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2 := by
    intro x y
    have hh : f y ≤ f x + inner ℝ (gradient f x) (y - x) + μ / 2 * ‖y - x‖ ^ 2 := hu x y
    nlinarith [mul_nonneg (sub_nonneg.mpr hμβ) (sq_nonneg ‖y - x‖)]
  change 0 < μ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _
  refine ⟨hμ, hf, hc, huβ, hm, ?_⟩
  dsimp only
  have hvalue : f ((fun x => x - (1 / β) * gradient f x)^[N] 1) - f 0 =
      β / (4 * D) * (q ^ N) ^ 2 := by
    have hs : ((fun x => x - (1 / β) * gradient f x)^[N] 1) ^ 2 = (q ^ N) ^ 2 := by
      simpa only [Real.norm_eq_abs, abs_mul_abs_self, sq] using congrArg (fun r : ℝ => r * r) hn'
    change μ * _ ^ 2 / 2 - μ * 0 ^ 2 / 2 = _
    rw [hs]
    dsimp [μ]; field_simp; ring
  rw [hvalue]
  change β / (4 * D) * (q ^ N) ^ 2 = β / (4 * D) * q ^ (2 * N) ∧
    β / (16 * D) ≤ β / (4 * D) * (q ^ N) ^ 2
  constructor
  · rw [Nat.mul_comm 2 N, pow_mul]
  · have hs : (1 : ℝ) / 4 ≤ (q ^ N) ^ 2 := by nlinarith
    have := mul_le_mul_of_nonneg_left hs (by positivity : 0 ≤ β / (4 * D))
    convert this using 1 <;> first | rfl | (field_simp; ring)

end AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexGradientGapSharpness
