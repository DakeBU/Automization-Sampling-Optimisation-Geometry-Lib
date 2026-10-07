theorem bounded_product_entropy_subadditivity
    {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y]
    (μ : Measure X) (ν : Measure Y) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    (F : X × Y → ℝ) (hF : Measurable F)
    (hF0 : ∀ z, 0 ≤ F z) (hFb : ∃ C : ℝ, ∀ z, F z ≤ C) :
    let Φ : ℝ → ℝ := fun t => t * Real.log t
    let A : X → ℝ := fun x => ∫ y, F (x, y) ∂ν
    let B : Y → ℝ := fun y => ∫ x, F (x, y) ∂μ
    let m : ℝ := ∫ z, F z ∂μ.prod ν
    Integrable F (μ.prod ν) ∧
    Integrable (fun z => Φ (F z)) (μ.prod ν) ∧
    (∀ x, Integrable (fun y => F (x, y)) ν ∧
      Integrable (fun y => Φ (F (x, y))) ν) ∧
    (∀ y, Integrable (fun x => F (x, y)) μ ∧
      Integrable (fun x => Φ (F (x, y))) μ) ∧
    Integrable A μ ∧ Integrable B ν ∧
    Integrable (fun x => Φ (A x)) μ ∧ Integrable (fun y => Φ (B y)) ν ∧
    (∫ x, Φ (A x) ∂μ) + (∫ y, Φ (B y) ∂ν) ≤
      (∫ z, Φ (F z) ∂μ.prod ν) + Φ m := by
  obtain ⟨C, hC⟩ := hFb
  rcases product_domains μ ν F hF hF0 C hC with
    ⟨iF, iPhi, sx, sy, iA, iB, iPhiA, iPhiB, _⟩
  exact ⟨iF, iPhi, sx, sy, iA, iB, iPhiA, iPhiB,
    bounded_product_inequality μ ν F hF hF0 C hC⟩

end AutoSamplingTheory.TechnicalLemmas.InformationTheory.ProductEntropy