theorem actual_reflection_block_identities
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) :
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    let F := fun p : E × E => (p.1,(2:ℝ) • p.1-p.2)
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2 J).subtypeL
        ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    ∃ R : Kernel E E, IsMarkovKernel R ∧
      (∀ y, R y = μ.tilted (fun x => -‖x-y‖^2/(2*η))) ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ f, U f =ᵐ[J] f ∘ F) ∧ Function.Involutive U ∧
        IsSelfAdjoint U.toContinuousLinearMap ∧
        (∀ f : Lp ℝ 2 J, (P f : E × E → ℝ) =ᵐ[J]
          fun p => ∫ x, f (x,p.2) ∂R p.2) ∧
        let A := P * U.toContinuousLinearMap * P
        let B := (1-P) * U.toContinuousLinearMap * P
        let D := (1-P) * U.toContinuousLinearMap * (1-P)
        star B*B=P-A^2 ∧ star B*D= -(A*star B) ∧
          (∀ f, P f=f → ‖B f‖^2 = ‖f‖^2-‖A f‖^2) 