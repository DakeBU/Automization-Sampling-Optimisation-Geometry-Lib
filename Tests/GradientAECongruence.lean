import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientAECongruence

open AutoSamplingTheory.TechnicalLemmas.Analysis

#check GradientAECongruence.not_gradient_ae_congr_for_arbitrary_measure
#print axioms GradientAECongruence.not_gradient_ae_congr_for_arbitrary_measure

example :
    ¬ ∀ (μ : MeasureTheory.Measure ℝ) (f g : ℝ → ℝ),
      f =ᵐ[μ] g → ∀ᵐ x ∂μ, gradient f x = gradient g x :=
  GradientAECongruence.not_gradient_ae_congr_for_arbitrary_measure
