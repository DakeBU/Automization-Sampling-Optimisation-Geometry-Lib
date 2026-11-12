import AutoSamplingTheory.ExampleCases.LowerBounds.GradientSpanDistance

open AutoSamplingTheory.ExampleCases.LowerBounds.GradientSpanDistance

-- Fix the literal witness and the order of assumptions independently of
-- internal helper definitions. This test imports only the production module.
example :
    ∀ (d N : ℕ), 1 ≤ N → 2 * N + 1 ≤ d + 1 → ∀ (β : ℝ), 0 < β →
    ∀ x₀ : EuclideanSpace ℝ (Fin (d + 1)),
    let f : EuclideanSpace ℝ (Fin (d + 1)) → ℝ := fun y =>
      let v := y - x₀
      (β / 4) * (((v 0) ^ 2 + (∑ i : Fin d, (v i.castSucc - v i.succ) ^ 2)
        + (v (Fin.last d)) ^ 2) / 2 - v 0)
    let xstar : EuclideanSpace ℝ (Fin (d + 1)) :=
      x₀ + WithLp.toLp 2 (fun i : Fin (d + 1) =>
        1 - ((i.val : ℝ) + 1) / ((d : ℝ) + 2))
    ConvexOn ℝ Set.univ f ∧ ContDiff ℝ 1 f ∧ IsMinOn f Set.univ xstar ∧
      (∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2) ∧
      ∀ x : ℕ → EuclideanSpace ℝ (Fin (d + 1)), x 0 = x₀ →
        (∀ n, x (n + 1) - x₀ ∈ Submodule.span ℝ
          (Set.range (fun i : Fin (n + 1) => gradient f (x i.val)))) →
        (1 / 8 : ℝ) * ‖x 0 - xstar‖ ^ 2 ≤ ‖x N - xstar‖ ^ 2 :=
  exercise_4_1

#print axioms exercise_4_1
