omit [IsProbabilityMeasure μ] in
/-- **Strong law of large numbers**, almost sure version: if `X n` is a sequence of independent
identically distributed integrable random variables taking values in a Banach space,
then `n⁻¹ • ∑ i ∈ range n, X i` converges almost surely to `𝔼[X 0]`. We give here the strong
version, due to Etemadi, that only requires pairwise independence. -/
theorem strong_law_ae (X : ℕ → Ω → E) (hint : Integrable (X 0) μ)
    (hindep : Pairwise ((· ⟂ᵢ[μ] ·) on X))
    (hident : ∀ i, IdentDistrib (X i) (X 0) μ μ) :
    ∀ᵐ ω ∂μ, Tendsto (fun n : ℕ ↦ (n : ℝ)⁻¹ • (∑ i ∈ range n, X i ω)) atTop (𝓝 μ[X 0]) := by
