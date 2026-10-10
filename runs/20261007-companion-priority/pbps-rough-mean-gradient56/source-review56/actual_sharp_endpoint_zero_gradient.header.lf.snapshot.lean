theorem actual_sharp_endpoint_zero_gradient
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) (hαη : (α : ℝ)*η = 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
      G.IsClosable ∧ G.closure.IsClosed ∧
      ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
        ∃ K : Lp ℝ 2 ν →L[ℝ] Lp E 2 ν,
          K = 0 ∧ ∀ u : Lp ℝ 2 ν,
            (T u,0) ∈ G.closure.graph ∧
            (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂
              ((volume : Measure E).tilted
                (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η)))) 