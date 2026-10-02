import AutoSamplingTheory.TechnicalLemmas.InformationTheory.QuadraticTiltFisher

#check AutoSamplingTheory.TechnicalLemmas.InformationTheory.QuadraticTiltFisher.information_quadratic_representative

#print axioms AutoSamplingTheory.TechnicalLemmas.InformationTheory.QuadraticTiltFisher.information_quadratic_representative

example {ι : Type*} [Fintype ι]
    (nu mu : MeasureTheory.Measure (EuclideanSpace ℝ ι))
    [MeasureTheory.IsProbabilityMeasure mu]
    {eta : ℝ} (heta : 0 < eta) (y y' : EuclideanSpace ℝ ι) :
    AutoSamplingTheory.TechnicalLemmas.InformationTheory.RelativeFisher.information
        mu (fun _ => 1)
        (fun t =>
          -(‖t - y‖ ^ 2 / (2 * eta)) -
            Real.log (∫ z, Real.exp (-(‖z - y‖ ^ 2 / (2 * eta))) ∂nu) -
          (-(‖t - y'‖ ^ 2 / (2 * eta))) +
            Real.log (∫ z, Real.exp (-(‖z - y'‖ ^ 2 / (2 * eta))) ∂nu)) =
      eta⁻¹ ^ 2 * ‖y - y'‖ ^ 2 := by
  exact AutoSamplingTheory.TechnicalLemmas.InformationTheory.QuadraticTiltFisher.information_quadratic_representative
    nu mu heta.ne' y y'
