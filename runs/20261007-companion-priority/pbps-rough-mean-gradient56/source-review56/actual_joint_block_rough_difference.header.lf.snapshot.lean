theorem actual_joint_block_rough_difference
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
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
      (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J]
        g ∘ (fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2))) ∧
      ∃ M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ u : Lp ℝ 2 ν, (M u : E × E → ℝ) =ᵐ[J] u ∘ Prod.snd) ∧
        ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
          ∃ K : Lp ℝ 2 ν →L[ℝ] Lp E 2 ν,
            let A := P * U.toContinuousLinearMap * P
            let B := (1-P) * U.toContinuousLinearMap * P
            ∀ u v : Lp ℝ 2 ν,
              P (M (u-v)) = M (u-v) ∧
              M (T u-T v) = A (M (u-v)) ∧
              η*‖K u-K v‖^2 ≤
                (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η))*‖B (M (u-v))‖^2 ∧
              4*η*‖K u-K v‖^2 ≤ ‖B (M (u-v))‖^2 