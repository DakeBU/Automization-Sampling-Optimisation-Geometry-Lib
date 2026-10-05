import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentSharpness

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentSharpness
open Set

-- Negative fixed step is included in the obstruction: the upper endpoint grows
-- by4 each step, while the balanced step decays by1/2 on the very same witness.
example : ∃ μ : ℝ, (μ = 1 ∨ μ = 3) ∧
    let f : ℝ → ℝ := fun x => μ * x^2 / 2
    IsMinOn f univ 0 ∧ ∀ N : ℕ,
      ‖(fun x => x + gradient f x)^[N] 1‖ = (4 : ℝ)^N ∧
      ‖(fun x => x - (1/2 : ℝ) * gradient f x)^[N] 1‖ = (1/2 : ℝ)^N := by
  obtain ⟨μ, hm, _, _, _, _, hmin, hN⟩ :=
    exists_quadratic_worst_case (α := 1) (β := 3) (by norm_num) (by norm_num) (-1)
  refine ⟨μ, hm, hmin, fun N => ?_⟩
  have hr := hN N
  norm_num at hr
  exact ⟨hr.1, hr.2.2⟩

-- Equal bounds determine the actual scalar objective. The balanced step reaches
-- its minimum after one step, but N=0 still preserves the nonzero initial point.
example : let f : ℝ → ℝ := fun x => 2 * x^2 / 2
    (‖(fun x => x - (1/2 : ℝ) * gradient f x)^[0] 1‖ = 1) ∧
    ∀ N : ℕ, ‖(fun x => x - (1/2 : ℝ) * gradient f x)^[N+1] 1‖ = 0 := by
  obtain ⟨μ, hm, _, _, _, _, _, hN⟩ :=
    exists_quadratic_worst_case (α := 2) (β := 2) (by norm_num) (by norm_num) (1/2)
  have he : μ = 2 := hm.elim id id
  subst μ
  constructor
  · norm_num
  · intro N; have hr := (hN (N+1)).2.2; norm_num at hr ⊢; exact hr

-- Zero step retains distance1 at every N; the theorem does not silently assume
-- positive steps or infer convergence from the positive-definite objective.
example : ∃ μ : ℝ, (μ = 1 ∨ μ = 3) ∧ ∀ N : ℕ,
    ‖(fun x => x - (0 : ℝ) * gradient (fun z : ℝ => μ * z^2 / 2) x)^[N] 1‖ = 1 := by
  obtain ⟨μ, hm, _, _, _, _, _, hN⟩ :=
    exists_quadratic_worst_case (α := 1) (β := 3) (by norm_num) (by norm_num) 0
  refine ⟨μ, hm, fun N => ?_⟩
  have hr := (hN N).1
  norm_num at hr ⊢
  exact hr

#print axioms exists_quadratic_worst_case
