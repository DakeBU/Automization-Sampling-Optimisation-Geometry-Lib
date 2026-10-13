      HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
      let fperp : Hperp := R f
      let fV : HP0 := V0.adjoint fperp
      B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) ∧
      HP0.subtypeL (ΓP0 fV)=ΓP (HP0.subtypeL fV) ∧
      ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖) at hGlobal
  let D : Hperp →L[ℝ] Hperp := R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL
  have hD (h : Hperp) : (D h : Lp ℝ 2 J)=
      U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J)) := hDparent h
  have hIntertwine : V0.adjoint ∘L D= -(A0 ∘L V0.adjoint) := hIntertwineParent
  letI : IsProbabilityMeasure μ := hμ
  letI : IsProbabilityMeasure J := hJ
  let F : E × E → E × E := fun z => (z.1,(2 : ℝ) • z.1-z.2)
  have hFmeas : Measurable F := by fun_prop
  have hFJ : Measure.map F J=J :=
    (AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection.reflection_preserves_augmentation μ η hη).2
  have hUIntegral (u : Lp ℝ 2 J) : (∫ z, U u z ∂J)=∫ z, u z ∂J := by
    calc
      (∫ z, U u z ∂J)=(∫ z, u (F z) ∂J) := integral_congr_ae (hU u)
      _ = (∫ z, u z ∂Measure.map F J) :=
        (integral_map hFmeas.aemeasurable (by rw [hFJ]; exact (Lp.memLp u).aestronglyMeasurable)).symm
      _ = (∫ z, u z ∂J) := by rw [hFJ]
  have hPIntegral (u : Lp ℝ 2 J) : (∫ z, P u z ∂J)=∫ z, u z ∂J := by
    change (∫ z, (condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le u : E × E → ℝ) z ∂J)=_
    simpa only [Measure.restrict_univ] using
      (integral_condExpL2_eq (𝕜:=ℝ) (s:=Set.univ) measurable_snd.comap_le u
        MeasurableSet.univ (measure_ne_top J Set.univ))
  have hIntegrable (u : Lp ℝ 2 J) : Integrable u J :=
    MemLp.integrable (by norm_num : (1 : ℝ≥0∞) ≤ 2) (Lp.memLp u)
  have hSubIntegral (u v : Lp ℝ 2 J) :
      (∫ z, (u-v) z ∂J)=(∫ z, u z ∂J)-(∫ z, v z ∂J) :=
