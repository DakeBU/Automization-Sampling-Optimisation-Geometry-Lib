theorem Integrable.mono_enorm {f : α → ε} {g : α → ε'} (hg : Integrable g μ)
    (hf : AEStronglyMeasurable f μ) (h : ∀ᵐ a ∂μ, ‖f a‖ₑ ≤ ‖g a‖ₑ) : Integrable f μ :=
  ⟨hf, hg.hasFiniteIntegral.mono_enorm h⟩

theorem Integrable.mono {f : α → β} {g : α → γ} (hg : Integrable g μ)
    (hf : AEStronglyMeasurable f μ) (h : ∀ᵐ a ∂μ, ‖f a‖ ≤ ‖g a‖) : Integrable f μ :=
  ⟨hf, hg.hasFiniteIntegral.mono h⟩

theorem Integrable.mono_nonneg [Lattice β] [HasSolidNorm β] [AddLeftMono β] {f g : α → β}
    (hg : Integrable g μ) (hf : AEStronglyMeasurable f μ) (hnonneg : ∀ᵐ a ∂μ, 0 ≤ f a)
    (h : ∀ᵐ a ∂μ, f a ≤ g a) :
    Integrable f μ :=
  ⟨hf, hg.hasFiniteIntegral.mono_nonneg hnonneg h⟩

theorem Integrable.mono'_enorm {f : α → ε} {g : α → ℝ≥0∞} (hg : Integrable g μ)
    (hf : AEStronglyMeasurable f μ) (h : ∀ᵐ a ∂μ, ‖f a‖ₑ ≤ g a) : Integrable f μ :=
  ⟨hf, hg.hasFiniteIntegral.mono_enorm h⟩

theorem Integrable.mono' {f : α → β} {g : α → ℝ} (hg : Integrable g μ)
    (hf : AEStronglyMeasurable f μ) (h : ∀ᵐ a ∂μ, ‖f a‖ ≤ g a) : Integrable f μ :=
  ⟨hf, hg.hasFiniteIntegral.mono' h⟩
