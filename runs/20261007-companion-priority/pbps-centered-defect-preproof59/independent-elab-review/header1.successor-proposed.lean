theorem actual_centered_defect_coercive_and_unit
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
      IsSelfAdjoint T ∧
      (∀ u : Lp ℝ 2 ν, (T u : E → ℝ) =ᵐ[ν]
        (fun y => ∫ x, u x ∂((volume : Measure E).tilted
          (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))))) ∧
      ∃ q : Lp ℝ 2 ν,
        (q : E → ℝ) =ᵐ[ν] (fun _ => (1 : ℝ)) ∧
        (∀ u : Lp ℝ 2 ν, inner ℝ q u = ∫ y, u y ∂ν) ∧
        let H0 : Submodule ℝ (Lp ℝ 2 ν) := (innerSL ℝ q).ker
        ∃ T0 : H0 →L[ℝ] H0,
          (∀ u : H0, (T0 u : Lp ℝ 2 ν) = T u) ∧
          IsSelfAdjoint T0 ∧ ((1 : H0 →L[ℝ] H0)-T0*T0).IsPositive ∧
          (∀ u : H0,
            ‖T0 u‖ ≤ ((1-(α : ℝ)*η)/(1+(α : ℝ)*η))*‖u‖ ∧
            inner ℝ (((1 : H0 →L[ℝ] H0)-T0*T0) u) u = ‖u‖^2-‖T0 u‖^2 ∧
            (4*(α : ℝ)*η/(1+(α : ℝ)*η)^2)*‖u‖^2 ≤
              inner ℝ (((1 : H0 →L[ℝ] H0)-T0*T0) u) u) ∧
          IsUnit ((1 : H0 →L[ℝ] H0)-T0*T0)
