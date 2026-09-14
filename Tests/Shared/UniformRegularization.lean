import AutoSamplingTheory.TechnicalLemmas.Analysis.UniformRegularization
import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentValue
import AutoSamplingTheory.TechnicalLemmas.Analysis.SmoothnessEquivalences

open Set InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis
open QuadraticRegularizationOracle
open scoped NNReal

-- A real uniform solver: one query at the center, followed by a half-step.
-- Its premise is proved for EVERY differentiable 1-strongly-convex objective
-- with 2-Lipschitz gradient, not postulated for a single known quadratic.
set_option backward.isDefEq.respectTransparency false in
example :
    let next := fun s : Bool × ℝ => if s.1 then Sum.inl s.2 else Sum.inr (1:ℝ)
    let update := fun _ : Bool × ℝ => fun x : ℝ => fun a : ℝ × ℝ =>
      (true, x-(1/2)*a.2)
    let N := ⌈(2:ℝ)*Real.log 2⌉₊
    ∀ f : ℝ → ℝ, Differentiable ℝ f → ConvexOn ℝ univ f →
      LipschitzWith 1 (gradient f) → ∀ z : ℝ,
      IsMinOn f univ z → ‖z-1‖ ≤ 1 →
      ∃ t x c, run next
        (fun s y (a : ℝ × ℝ) => update s y
          (a.1+(1:ℝ)/2*‖y-1‖^2,a.2+(y-1)))
        (fun y => (f y,gradient f y)) N (false,1) = ((t,some x),c) ∧
        f x-f z ≤ 1 ∧ c ≤ 2 := by
  let next := fun s : Bool × ℝ => if s.1 then Sum.inl s.2 else Sum.inr (1:ℝ)
  let update := fun _ : Bool × ℝ => fun x : ℝ => fun a : ℝ × ℝ =>
    (true, x-(1/2)*a.2)
  let N := ⌈(2:ℝ)*Real.log 2⌉₊
  have hN : 0 < N := Nat.ceil_pos.mpr
    (mul_pos (by norm_num) (Real.log_pos (by norm_num)))
  have hs (g : ℝ → ℝ) (hd : Differentiable ℝ g)
      (hsc : StrongConvexOn univ 1 g) (hL : LipschitzWith 2 (gradient g))
      (w : ℝ) (_hw : IsMinOn g univ w) (hr : ‖w-1‖ ≤ 1) :
      ∃ t x c, run next update (fun y => (g y,gradient g y)) N (false,1) =
        ((t,some x),c) ∧ g x-g w ≤ (1:ℝ)/2 := by
    have hC1 : ContDiff ℝ 1 g := by
      apply contDiff_one_iff_fderiv.mpr
      refine ⟨hd, ?_⟩
      rw [← toDual_comp_gradient]
      exact (toDual ℝ ℝ).continuous.comp hL.continuous
    have hu : ∀ x y, g y ≤ g x+inner ℝ (gradient g x) (y-x)+2/2*‖y-x‖^2 := by
      apply (SmoothnessEquivalences.upper_model_iff_gradient_upper hC1).mpr
      intro x y
      have hLip := hL.dist_le_mul y x
      rw [dist_eq_norm, dist_eq_norm] at hLip
      calc
        inner ℝ (gradient g y-gradient g x) (y-x) ≤
          ‖gradient g y-gradient g x‖*‖y-x‖ := real_inner_le_norm _ _
        _ ≤ (2*‖y-x‖)*‖y-x‖ := mul_le_mul_of_nonneg_right hLip (norm_nonneg _)
        _ = 2*‖y-x‖^2 := by ring
    have he := GradientDescentValue.gradient_step_energy_bound hC1 hsc
      (h := (1:ℝ)/2) (by norm_num) (by norm_num) hu 1 w
    have hr' : ‖(1:ℝ)-w‖ ≤ 1 := by simpa only [norm_sub_rev] using hr
    refine ⟨(true,1-(1/2)*gradient g 1),1-(1/2)*gradient g 1,1,?_,?_⟩
    · obtain ⟨n,hn⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hN)
      rw [hn]
      simp [run, next, update]
    · simp only [smul_eq_mul] at he
      have hsq : ‖(1:ℝ)-w‖^2 ≤ 1 := by nlinarith [norm_nonneg ((1:ℝ)-w)]
      nlinarith [sq_nonneg ‖(1:ℝ)-(1/2)*gradient g 1-w‖]
  have result := UniformRegularization.uniform_accuracy_and_query_bound
    (1:ℝ≥0) (1:ℝ) (R := 1) (ε := 1) (by norm_num) (by norm_num)
    (by norm_num) (fun _ => 2) next update (false,1)
  dsimp only at result ⊢
  norm_num only [NNReal.coe_one, one_pow, div_one, one_mul, NNReal.coe_mk,
    one_div, div_inv_eq_mul, mul_one, one_smul] at result
  intro f hd hc hL z hz hr
  obtain ⟨t,x,c,he,hgap,_,hc⟩ := result hs f hd hc hL z hz hr
  exact ⟨t,x,c,he,hgap,hc⟩

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.UniformRegularization.uniform_accuracy_and_query_bound
