import AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio

#check AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio.llr_tilted_tilted_ae
#check AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio.gradient_quadratic_representative

#print axioms AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio.llr_tilted_tilted_ae
#print axioms AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio.gradient_quadratic_representative

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (mu : MeasureTheory.Measure E) [MeasureTheory.SigmaFinite mu]
    {eta : ℝ} (heta : 0 < eta) (y y' x : E)
    (hy : MeasureTheory.Integrable
      (fun z => Real.exp (-(‖z - y‖ ^ 2 / (2 * eta)))) mu)
    (hy' : MeasureTheory.Integrable
      (fun z => Real.exp (-(‖z - y'‖ ^ 2 / (2 * eta)))) mu) :
    MeasureTheory.llr
        (mu.tilted
          (fun z => -(‖z - y‖ ^ 2 / (2 * eta))))
        (mu.tilted
          (fun z => -(‖z - y'‖ ^ 2 / (2 * eta)))) =ᵐ[mu.tilted
          (fun z => -(‖z - y‖ ^ 2 / (2 * eta)))]
      (fun z =>
        -(‖z - y‖ ^ 2 / (2 * eta)) -
          Real.log (∫ w, Real.exp (-(‖w - y‖ ^ 2 / (2 * eta))) ∂mu) -
        (-(‖z - y'‖ ^ 2 / (2 * eta))) +
          Real.log (∫ w, Real.exp (-(‖w - y'‖ ^ 2 / (2 * eta))) ∂mu)) ∧
      gradient
          (fun z =>
            -(‖z - y‖ ^ 2 / (2 * eta)) -
              Real.log (∫ w, Real.exp (-(‖w - y‖ ^ 2 / (2 * eta))) ∂mu) -
            (-(‖z - y'‖ ^ 2 / (2 * eta))) +
              Real.log (∫ w, Real.exp (-(‖w - y'‖ ^ 2 / (2 * eta))) ∂mu)) x =
        eta⁻¹ • (y - y') := by
  constructor
  · exact AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio.llr_tilted_tilted_ae
      mu _ _ (by fun_prop) hy hy'
  · exact AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio.gradient_quadratic_representative
      mu heta.ne' y y' x
