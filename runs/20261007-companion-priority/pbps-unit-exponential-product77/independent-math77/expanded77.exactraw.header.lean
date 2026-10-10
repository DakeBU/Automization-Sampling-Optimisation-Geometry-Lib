theorem unit_exponential_product_laws :
let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let X : ℕ → (ℕ → ℝ) → ℝ := fun k ω => ω k
  let ε : ℕ → (ℕ → ℝ) → ℝ≥0 := fun k ω => Real.toNNReal (X k ω)
  IsProbabilityMeasure P ∧
  (∀ k : ℕ, Measurable (X k) ∧ Measurable (ε k) ∧
    Measure.map (X k) P = expMeasure (1 : ℝ)) ∧
  iIndepFun X P ∧
  (∀ᵐ ω ∂P, ∀ k : ℕ, 0 < X k ω ∧ (ε k ω : ℝ) = X k ω) ∧
  (∀ᵐ ω ∂P, Tendsto (fun n : ℕ => ∑ k ∈ Finset.range n, (ε k ω : ℝ))
    atTop atTop)
