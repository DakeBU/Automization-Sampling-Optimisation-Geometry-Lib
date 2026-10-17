import AutoSamplingTheory.TechnicalLemmas.Probability.KernelRetainedReversibility

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.KernelRetainedReversibility

-- Exercise the full a.e./s-finite interface, without a hidden Markov instance.
example {A B : Type*} [MeasurableSpace A] [MeasurableSpace B]
    (μ : Measure A) [SFinite μ]
    (R : Kernel A B) [IsSFiniteKernel R]
    (F : Kernel (A × B) B) [IsSFiniteKernel F]
    (hF : ∀ᵐ a ∂μ, (F.comap (fun b => (a, b))
      (measurable_const.prodMk measurable_id)).IsReversible (R a)) :
    ((Kernel.deterministic Prod.fst measurable_fst) ×ₖ F).IsReversible (μ ⊗ₘ R) :=
  retained_coordinate_isReversible μ R F hF

-- A zero update is deliberately not a probability kernel on a nonzero state.
example {A B : Type*} [MeasurableSpace A] [MeasurableSpace B]
    (μ : Measure A) [SFinite μ] (R : Kernel A B) [IsSFiniteKernel R] :
    ((Kernel.deterministic Prod.fst measurable_fst) ×ₖ
      (0 : Kernel (A × B) B)).IsReversible (μ ⊗ₘ R) := by
  apply retained_coordinate_isReversible μ R 0
  filter_upwards [] with a
  intro S T hS hT
  simp

-- Null retained coordinates impose no pointwise condition on F.
example {A B : Type*} [MeasurableSpace A] [MeasurableSpace B]
    (R : Kernel A B) [IsSFiniteKernel R]
    (F : Kernel (A × B) B) [IsSFiniteKernel F] :
    ((Kernel.deterministic Prod.fst measurable_fst) ×ₖ F).IsReversible
      ((0 : Measure A) ⊗ₘ R) := by
  apply retained_coordinate_isReversible (0 : Measure A) R F
  simp

#print axioms retained_coordinate_isReversible
