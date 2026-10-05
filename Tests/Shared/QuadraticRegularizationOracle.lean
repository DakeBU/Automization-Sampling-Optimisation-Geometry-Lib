import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul

open Set
open AutoSamplingTheory.TechnicalLemmas.Analysis
open QuadraticRegularizationOracle
open scoped NNReal

-- Control inspection is free, including at zero query fuel.
example (n : ℕ) : run (fun s : ℕ => (Sum.inl s : Sum ℕ ℕ))
    (fun _ _ (a : ℕ) => a) id n 7 = ((7, some 7), 0) := by
  cases n <;> rfl
example : run (fun s : ℕ => (Sum.inr s : Sum ℕ ℕ))
    (fun _ _ (a : ℕ) => a) id 0 7 = ((7, none), 0) := rfl

-- A two-query adaptive method: second point depends on the first gradient;
-- termination after the second reply depends on that reply's gradient.
set_option backward.isDefEq.respectTransparency false in
example :
    let f := fun x : ℝ => x^2/2
    let W := fun x : ℝ => f x + (1:ℝ)/2*‖x-1‖^2
    let next := fun s : ℕ × ℝ × ℝ =>
      if s.1 = 0 then Sum.inr (1:ℝ)
      else if s.1 = 1 then Sum.inr (s.2.1-s.2.2/2)
      else if s.2.2 = 0 then Sum.inl s.2.1 else Sum.inr s.2.1
    let update := fun s : ℕ × ℝ × ℝ => fun x : ℝ => fun a : ℝ × ℝ =>
      (s.1+1, x, a.2)
    let corrected := fun s x (a : ℝ × ℝ) =>
      update s x (a.1+(1:ℝ)/2*‖x-1‖^2,a.2+(x-1))
    let oracle := fun x => (f x, gradient f x)
    run next corrected oracle 1 (0,0,0) = (((1,1,1),none),1) ∧
    run next corrected oracle 2 (0,0,0) = (((2,1/2,0),some (1/2)),2) ∧
    run next update (fun x => (W x,gradient W x)) 4 (0,0,0) =
      (((2,1/2,0),some (1/2)),2) := by
  dsimp only
  let f := fun x : ℝ => x^2/2
  have hd : Differentiable ℝ f := by fun_prop
  have hg (x : ℝ) : gradient f x = x := by
    have h : HasDerivAt f x x := by
      simpa [f] using ((hasDerivAt_id x).pow 2).div_const (2:ℝ)
    exact h.hasGradientAt.gradient
  have hc : ConvexOn ℝ univ f := by
    refine ⟨convex_univ, ?_⟩
    intro x _ y _ a b ha hb hab
    simp only [f, smul_eq_mul]
    have hnon : 0 ≤ a*b*(x-y)^2 := mul_nonneg (mul_nonneg ha hb) (sq_nonneg _)
    have he : a*x^2/2+b*y^2/2-(a*x+b*y)^2/2 = a*b*(x-y)^2/2 := by
      have hb' : b = 1-a := by linarith
      rw [hb']; ring
    nlinarith
  have hL : LipschitzWith 1 (gradient f) := by
    rw [show gradient f = id from funext hg]; exact LipschitzWith.id
  let next := fun s : ℕ × ℝ × ℝ =>
    if s.1 = 0 then Sum.inr (1:ℝ)
    else if s.1 = 1 then Sum.inr (s.2.1-s.2.2/2)
    else if s.2.2 = 0 then Sum.inl s.2.1 else Sum.inr s.2.1
  let update := fun s : ℕ × ℝ × ℝ => fun x : ℝ => fun a : ℝ × ℝ =>
    (s.1+1, x, a.2)
  have sim := (simulate_regularized next update hd hc hL (δ := 1) 1 4 (0,0,0)).1
  dsimp only at sim
  norm_num only [NNReal.coe_one, one_smul] at sim
  refine ⟨?_,?_,?_⟩
  · norm_num [run, show (fun x : ℝ => x^2/2) = f from rfl, hg]
  · norm_num [run, show (fun x : ℝ => x^2/2) = f from rfl, hg]
  · rw [← sim]
    norm_num [run, next, update, hg]

-- Zero precision is the identity reply conversion, also for arbitrary programs.
example {S X : Type*} (next : S → Sum X ℝ)
    (update : S → ℝ → (ℝ × ℝ) → S) (n : ℕ) (s : S) :
    run next (fun s x (a : ℝ × ℝ) => update s x (a.1+0/2*‖x-1‖^2,a.2+0*(x-1)))
      (fun x => (x^2/2,x)) n s = run next update (fun x => (x^2/2,x)) n s := by
  simp

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle.simulate_regularized
