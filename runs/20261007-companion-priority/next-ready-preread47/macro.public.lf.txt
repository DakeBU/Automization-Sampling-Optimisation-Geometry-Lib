theorem macroscopic_reflection_smooth_representative {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : NNReal} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2) (hη : 0 < η) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    let Λ := J.map (fun p : E × E => (p.2,(2:ℝ) • p.1-p.2))
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2 J).subtypeL
        ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    let s := fun y u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
      (1/(4*η)) • innerSL ℝ (y-u)
    ∃ S : Kernel E E, IsMarkovKernel S ∧ Λ.IsCondKernel S ∧ Λ.fst = J.snd ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J]
          (fun p => g (p.1,(2:ℝ) • p.1-p.2))) ∧
        Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap ∧
        ∀ (f : E → ℝ), ContDiff ℝ ∞ f → HasCompactSupport f →
          ∃ g : Lp ℝ 2 J,
            (g : E × E → ℝ) =ᵐ[J] (fun p => f p.2) ∧ P g = g ∧
            ((P * U.toContinuousLinearMap * P) g : E × E → ℝ) =ᵐ[J]
              (fun p => ∫ u, f u ∂S p.2) ∧
            MemLp (fun y => ∫ u, f u ∂S y) 2 J.snd ∧
            ∀ y, Integrable (s y) (S y) ∧ Integrable (fun u => f u • s y u) (S y) ∧
              HasFDerivAt (fun z => ∫ u, f u ∂S z)
              ((∫ u, f u • s y u ∂S y) -
                (∫ u, f u ∂S y) • (∫ u, s y u ∂S y)) y 