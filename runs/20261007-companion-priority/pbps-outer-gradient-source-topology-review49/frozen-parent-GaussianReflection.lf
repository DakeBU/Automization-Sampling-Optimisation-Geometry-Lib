theorem reflection_preserves_augmentation (μ : Measure E) [IsProbabilityMeasure μ]
    (η : ℝ) (_hη : 0 < η) :
    Function.Involutive (fun p : E × E => (p.1, (2 : ℝ) • p.1 - p.2)) ∧
      Measure.map (fun p : E × E => (p.1, (2 : ℝ) • p.1 - p.2))
        (Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
          (μ.prod (stdGaussian E))) =
        Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
          (μ.prod (stdGaussian E)) 