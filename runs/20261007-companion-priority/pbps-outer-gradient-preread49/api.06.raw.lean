lemma integral_mono_ae {f g : α → E} (hf : Integrable f μ) (hg : Integrable g μ)
    (h : f ≤ᵐ[μ] g) : ∫ x, f x ∂μ ≤ ∫ x, g x ∂μ := by
  rw [← sub_nonneg, ← integral_sub hg hf]
