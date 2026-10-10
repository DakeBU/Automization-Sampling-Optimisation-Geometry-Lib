theorem augmentation_eq_withDensity (μ : Measure E) [IsProbabilityMeasure μ]
    (η : ℝ) (hη : 0 < η) :
    Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
        (μ.prod (stdGaussian E)) =
      (μ.prod (volume : Measure E)).withDensity (fun p =>
        ENNReal.ofReal
          (((Real.sqrt (2 * Real.pi * η))⁻¹) ^ Module.finrank ℝ E *
            Real.exp (-‖p.2 - p.1‖ ^ 2 / (2 * η)))) 