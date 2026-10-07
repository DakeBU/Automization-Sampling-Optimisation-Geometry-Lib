lemma ae_nonneg_slice_of_ae_nonneg (i : Fin n) (f : (Fin n → Ω) → ℝ)
    (hf_nn : 0 ≤ᵐ[μˢ] f) :
    ∀ᵐ x ∂μˢ, ∀ᵐ y ∂(μs i), 0 ≤ f (Function.update x i y) := by
