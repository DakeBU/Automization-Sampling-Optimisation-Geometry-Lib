section Integral

lemma _root_.MeasureTheory.AEStronglyMeasurable.ae_of_compProd [SFinite μ] [IsSFiniteKernel κ]
    {E : Type*} [NormedAddCommGroup E] {f : α → β → E}
    (hf : AEStronglyMeasurable f.uncurry (μ ⊗ₘ κ)) :
    ∀ᵐ x ∂μ, AEStronglyMeasurable (f x) (κ x) := by
  simpa using hf.compProd_mk_left

lemma integrable_compProd_iff [SFinite μ] [IsSFiniteKernel κ] {E : Type*} [NormedAddCommGroup E]
    {f : α × β → E} (hf : AEStronglyMeasurable f (μ ⊗ₘ κ)) :
    Integrable f (μ ⊗ₘ κ) ↔
      (∀ᵐ x ∂μ, Integrable (fun y => f (x, y)) (κ x)) ∧
        Integrable (fun x => ∫ y, ‖f (x, y)‖ ∂(κ x)) μ := by
  simp_rw [Measure.compProd, ProbabilityTheory.integrable_compProd_iff hf, Kernel.prodMkLeft_apply,
    Kernel.const_apply]

lemma integral_compProd [SFinite μ] [IsSFiniteKernel κ] {E : Type*}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : α × β → E} (hf : Integrable f (μ ⊗ₘ κ)) :
    ∫ x, f x ∂(μ ⊗ₘ κ) = ∫ a, ∫ b, f (a, b) ∂(κ a) ∂μ := by
  rw [Measure.compProd, ProbabilityTheory.integral_compProd hf]
