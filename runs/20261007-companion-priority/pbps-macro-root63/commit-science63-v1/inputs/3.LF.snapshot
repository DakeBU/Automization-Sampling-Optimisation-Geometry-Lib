theorem actual_unique_positive_macroscopic_defect_root
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
    let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
    let F := fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2)
    let mY := MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)
    letI : MeasurableSpace (E × E) := Prod.instMeasurableSpace
    letI : Fact (mY ≤ (inferInstance : MeasurableSpace (E × E))) :=
      ⟨measurable_snd.comap_le⟩
    let HP := lpMeas ℝ ℝ mY 2 J
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      HP.subtypeL ∘L condExpL2 ℝ ℝ (μ := J) measurable_snd.comap_le
    let hp : MeasurePreserving (Prod.snd : E × E → E) J ν := ⟨measurable_snd,rfl⟩
    let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    HP = P.toLinearMap.range ∧
    (∀ f : HP, P (f : Lp ℝ 2 J) = f) ∧
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν ∧
      ∃ e : Lp ℝ 2 ν ≃ₗᵢ[ℝ] HP,
        (∀ u : Lp ℝ 2 ν, (e u : Lp ℝ 2 J) = M u) ∧
        ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
          (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F) ∧
          Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap ∧
          ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
            IsSelfAdjoint T ∧
            (∀ u : Lp ℝ 2 ν,
              ‖T u‖ ≤ ‖u‖ ∧
              (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
              (∫ y, T u y ∂ν) = ∫ y, u y ∂ν) ∧
            let A : HP →L[ℝ] HP :=
              HP.orthogonalProjectionOnto ∘L U.toContinuousLinearMap ∘L HP.subtypeL
            let B : HP →L[ℝ] Lp ℝ 2 J :=
              (((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P)*U.toContinuousLinearMap*P) ∘L HP.subtypeL
            A = e.conjStarAlgEquiv T ∧ IsSelfAdjoint A ∧
            (∀ f : HP, ‖A f‖ ≤ ‖f‖) ∧
            (∀ f : HP, P (B f) = 0) ∧
            ∃ Γ : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
              Γ.IsPositive ∧ Γ*Γ=(1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T ∧
              let ΓP : HP →L[ℝ] HP := e.conjStarAlgEquiv Γ
              ΓP.IsPositive ∧ ΓP*ΓP=(1 : HP →L[ℝ] HP)-A*A ∧
              B.adjoint ∘L B = ΓP*ΓP ∧
              (∀ f : HP, ‖B f‖ = ‖ΓP f‖ ∧
                ‖ΓP f‖^2 = ‖f‖^2-‖A f‖^2) ∧
              (∀ G : HP →L[ℝ] HP,
                G.IsPositive → G*G=(1 : HP →L[ℝ] HP)-A*A → G=ΓP)
