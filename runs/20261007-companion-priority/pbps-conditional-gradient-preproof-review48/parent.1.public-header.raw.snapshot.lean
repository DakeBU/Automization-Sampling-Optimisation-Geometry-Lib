theorem conditional_centered_domain_and_score_variance
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : NNReal} {η : ℝ}
    (hα : 0 < (α:ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x a : E, (α:ℝ)*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ V) x a a ∧
      fderiv ℝ (fderiv ℝ V) x a a ≤ (β:ℝ)*‖a‖^2)
    (hη : 0 < η) (hβη : (β:ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    let W := fun y u : E => V ((1/2:ℝ) • (y+u))+‖u-y‖^2/(8*η)
    let s := fun y u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
      (1/(4*η)) • innerSL ℝ (y-u)
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y=(R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y=(volume : Measure E).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ Integrable (fun u => Real.exp (-W y u)) ∧
        0 < ∫ u, Real.exp (-W y u) ∧
        ∃ D : Lp ℝ 2 (S y) →ₗ.[ℝ] Lp E 2 (S y),
          Dense (D.domain : Set (Lp ℝ 2 (S y))) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
          (∀ (a : Lp ℝ 2 (S y)) (G : Lp E 2 (S y)), (a,G) ∈ D.graph ↔
            ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
              a =ᵐ[S y] φ ∧ G =ᵐ[S y] gradient φ) ∧
          (∀ z : D.closure.domain, (∫ x, (z : Lp ℝ 2 (S y)) x ∂S y)=0 →
            (((α:ℝ)+1/η)/4)*‖(z : Lp ℝ 2 (S y))‖^2 ≤ ‖D.closure z‖^2) ∧
          ∀ a : E,
            AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Admissible
              (S y) (fun u => s y u a) ∧
            AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
              (S y) (fun u => s y u a) ≤
                (1/η-(α:ℝ))^2/(4*((α:ℝ)+1/η))*‖a‖^2 