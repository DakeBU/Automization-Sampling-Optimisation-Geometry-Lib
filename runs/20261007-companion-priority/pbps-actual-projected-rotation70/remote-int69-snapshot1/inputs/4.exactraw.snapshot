import AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining

/-!
# Actual PBPS projected reflection rotation

Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix B.3, the actual
projected rotation and two-component energy used in (B.21) and Lemma B.4.
The reflected observable and its conditional/polar components are actual
inputs and outputs. Mean preservation is proved internally from the same law.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

theorem actual_projected_rotation
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
              Commute Γ T ∧
              let ΓP : HP →L[ℝ] HP := e.conjStarAlgEquiv Γ
              ΓP.IsPositive ∧ ΓP*ΓP=(1 : HP →L[ℝ] HP)-A*A ∧
              Commute ΓP A ∧
              B.adjoint ∘L B = ΓP*ΓP ∧
              ∃ q : Lp ℝ 2 ν,
                (q : E → ℝ) =ᵐ[ν] (fun _ => (1 : ℝ)) ∧ T q = q ∧
                (∀ u : Lp ℝ 2 ν, inner ℝ q u = ∫ y, u y ∂ν) ∧
                let qP : HP := e q
                let HP0 := (innerSL ℝ qP).ker
                letI : NormedAddCommGroup HP0 := HP0.normedAddCommGroup
                letI : InnerProductSpace ℝ HP0 := HP0.innerProductSpace
                letI : CompleteSpace HP0 := (innerSL ℝ qP).isClosed_ker.completeSpace_coe
                let γ : ℝ := 2*Real.sqrt ((α : ℝ)*η)/(1+(α : ℝ)*η)
                (∀ f : HP, f ∈ HP0 ↔ (∫ y, (e.symm f) y ∂ν) = 0) ∧
                ΓP qP = 0 ∧ 0 < γ ∧
                ∃ ΓP0 : HP0 →L[ℝ] HP0,
                  (∀ f : HP0, (ΓP0 f : HP) = ΓP (f : HP)) ∧
                  ΓP0.IsPositive ∧ (ΓP0-γ • (1 : HP0 →L[ℝ] HP0)).IsPositive ∧
                  IsUnit ΓP0 ∧
                  ∃ Inv : HP0 →L[ℝ] HP0,
                    Inv*ΓP0=(1 : HP0 →L[ℝ] HP0) ∧
                    ΓP0*Inv=(1 : HP0 →L[ℝ] HP0) ∧ ‖Inv‖ ≤ 1/γ ∧
                    IsSelfAdjoint Inv ∧
                    ∃ A0 : HP0 →L[ℝ] HP0,
                      (∀ u : HP0, (A0 u : HP)=A (u : HP)) ∧
                      IsSelfAdjoint A0 ∧ Commute A0 ΓP0 ∧
                      A0*A0+ΓP0*ΓP0=(1 : HP0 →L[ℝ] HP0) ∧
                      Commute A0 Inv ∧
                    let Hperp := P.ker
                    letI : NormedAddCommGroup Hperp := Hperp.normedAddCommGroup
                    letI : InnerProductSpace ℝ Hperp := Hperp.innerProductSpace
                    letI : CompleteSpace Hperp := P.isClosed_ker.completeSpace_coe
                    ∃ B0 : HP0 →L[ℝ] Hperp,
                      (∀ f : HP0, (B0 f : Lp ℝ 2 J) = B (f : HP)) ∧
                      ∃ V0 : HP0 →L[ℝ] Hperp,
                        V0 = B0 ∘L Inv ∧ B0 = V0 ∘L ΓP0 ∧
                        V0.adjoint ∘L V0 = (1 : HP0 →L[ℝ] HP0) ∧
                        (∀ f : HP0, ‖V0 f‖ = ‖f‖) ∧
                        ∃ R : Lp ℝ 2 J →L[ℝ] Hperp,
                          (∀ g : Lp ℝ 2 J, (R g : Lp ℝ 2 J)=g-P g) ∧
                          (∀ g : Lp ℝ 2 J,
                            B.adjoint g=HP0.subtypeL (B0.adjoint (R g))) ∧
                          let D : Hperp →L[ℝ] Hperp :=
                            R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL
                          (∀ h : Hperp, (D h : Lp ℝ 2 J)=
                            U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J))) ∧
                          V0.adjoint ∘L D = -(A0 ∘L V0.adjoint) ∧
                          (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
                            ∃ fP : HP0,
                              HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
                              let fperp : Hperp := R f
                              let fV : HP0 := V0.adjoint fperp
                              B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) ∧
                              HP0.subtypeL (ΓP0 fV)=ΓP (HP0.subtypeL fV) ∧
                              ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
                              let g : Lp ℝ 2 J := U (P f-(f-P f))
                              (∫ z, g z ∂J)=0 ∧
                              ∃ gP : HP0,
                                HP0.subtypeL gP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le g ∧
                                let gperp : Hperp := R g
                                let gV : HP0 := V0.adjoint gperp
                                gP=A0 fP-ΓP0 fV ∧
                                gV=ΓP0 fP+A0 fV ∧
                                ‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2) := by
  classical
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let mY : MeasurableSpace (E × E) := MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)
  letI : MeasurableSpace (E × E) := Prod.instMeasurableSpace
  letI : Fact (mY ≤ (inferInstance : MeasurableSpace (E × E))) := ⟨measurable_snd.comap_le⟩
  let HP := lpMeas ℝ ℝ mY 2 J
  letI : NormedAddCommGroup HP := HP.normedAddCommGroup
  letI : InnerProductSpace ℝ HP := HP.innerProductSpace
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    HP.subtypeL ∘L condExpL2 ℝ ℝ (μ := J) measurable_snd.comap_le
  have hBase := AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining
    (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  have parentSlice0 := hBase
  have hμ := parentSlice0.1
  have parentSlice1 := parentSlice0.2
  have hJ := parentSlice1.1
  have parentSlice2 := parentSlice1.2
  have hν := parentSlice2.1
  have parentSlice3 := parentSlice2.2
  have hRange := parentSlice3.1
  have parentSlice4 := parentSlice3.2
  have hPf := parentSlice4.1
  have parentSlice5 := parentSlice4.2
  obtain ⟨S, parentSlice6⟩ := parentSlice5
  have hS := parentSlice6.1
  have parentSlice7 := parentSlice6.2
  have hSd := parentSlice7.1
  have parentSlice8 := parentSlice7.2
  have hSc := parentSlice8.1
  have parentSlice9 := parentSlice8.2
  have hSf := parentSlice9.1
  have parentSlice10 := parentSlice9.2
  have hSs := parentSlice10.1
  have parentSlice11 := parentSlice10.2
  obtain ⟨e, parentSlice12⟩ := parentSlice11
  have he := parentSlice12.1
  have parentSlice13 := parentSlice12.2
  obtain ⟨U, parentSlice14⟩ := parentSlice13
  have hU := parentSlice14.1
  have parentSlice15 := parentSlice14.2
  have hUi := parentSlice15.1
  have parentSlice16 := parentSlice15.2
  have hUs := parentSlice16.1
  have parentSlice17 := parentSlice16.2
  obtain ⟨T, parentSlice18⟩ := parentSlice17
  have hTs := parentSlice18.1
  have parentSlice19 := parentSlice18.2
  have hAll := parentSlice19.1
  have parentSlice20 := parentSlice19.2
  have hAeq := parentSlice20.1
  have parentSlice21 := parentSlice20.2
  have hAs := parentSlice21.1
  have parentSlice22 := parentSlice21.2
  have hAn := parentSlice22.1
  have parentSlice23 := parentSlice22.2
  have hPB := parentSlice23.1
  have parentSlice24 := parentSlice23.2
  obtain ⟨Γ, parentSlice25⟩ := parentSlice24
  have hΓ := parentSlice25.1
  have parentSlice26 := parentSlice25.2
  have hΓSq := parentSlice26.1
  have parentSlice27 := parentSlice26.2
  have hCommRoot := parentSlice27.1
  have parentSlice28 := parentSlice27.2
  have hΓP := parentSlice28.1
  have parentSlice29 := parentSlice28.2
  have hΓPSq := parentSlice29.1
  have parentSlice30 := parentSlice29.2
  have hCommP := parentSlice30.1
  have parentSlice31 := parentSlice30.2
  have hGram := parentSlice31.1
  have parentSlice32 := parentSlice31.2
  obtain ⟨q, parentSlice33⟩ := parentSlice32
  have hqa := parentSlice33.1
  have parentSlice34 := parentSlice33.2
  have hTq := parentSlice34.1
  have parentSlice35 := parentSlice34.2
  have hq := parentSlice35.1
  have parentSlice36 := parentSlice35.2
  have hCenter := parentSlice36.1
  have parentSlice37 := parentSlice36.2
  have hΓPq := parentSlice37.1
  have parentSlice38 := parentSlice37.2
  have hγ := parentSlice38.1
  have parentSlice39 := parentSlice38.2
  obtain ⟨ΓP0, parentSlice40⟩ := parentSlice39
  have hΓP0 := parentSlice40.1
  have parentSlice41 := parentSlice40.2
  have hPos0 := parentSlice41.1
  have parentSlice42 := parentSlice41.2
  have hOrder0 := parentSlice42.1
  have parentSlice43 := parentSlice42.2
  have hUnit := parentSlice43.1
  have parentSlice44 := parentSlice43.2
  obtain ⟨Inv, parentSlice45⟩ := parentSlice44
  have hLeft := parentSlice45.1
  have parentSlice46 := parentSlice45.2
  have hRight := parentSlice46.1
  have parentSlice47 := parentSlice46.2
  have hNormInv := parentSlice47.1
  have parentSlice48 := parentSlice47.2
  have hInvSelf := parentSlice48.1
  have parentSlice49 := parentSlice48.2
  obtain ⟨A0, parentSlice50⟩ := parentSlice49
  have hA0 := parentSlice50.1
  have parentSlice51 := parentSlice50.2
  have hA0self := parentSlice51.1
  have parentSlice52 := parentSlice51.2
  have hComm0 := parentSlice52.1
  have parentSlice53 := parentSlice52.2
  have hSquare0 := parentSlice53.1
  have parentSlice54 := parentSlice53.2
  have hCommInv := parentSlice54.1
  have parentSlice55 := parentSlice54.2
  obtain ⟨B0, parentSlice56⟩ := parentSlice55
  have hB0 := parentSlice56.1
  have parentSlice57 := parentSlice56.2
  obtain ⟨V0, parentSlice58⟩ := parentSlice57
  have hVdef := parentSlice58.1
  have parentSlice59 := parentSlice58.2
  have hFactor := parentSlice59.1
  have parentSlice60 := parentSlice59.2
  have hVadj := parentSlice60.1
  have parentSlice61 := parentSlice60.2
  have hVnorm := parentSlice61.1
  have parentSlice62 := parentSlice61.2
  obtain ⟨R, parentSlice63⟩ := parentSlice62
  have hR := parentSlice63.1
  have parentSlice64 := parentSlice63.2
  have hAmbient := parentSlice64.1
  have parentSlice65 := parentSlice64.2
  have hDparent := parentSlice65.1
  have parentSlice66 := parentSlice65.2
  have hIntertwineParent := parentSlice66.1
  have hGlobal := parentSlice66.2
  let A : HP →L[ℝ] HP := HP.orthogonalProjectionOnto ∘L U.toContinuousLinearMap ∘L HP.subtypeL
  let B : HP →L[ℝ] Lp ℝ 2 J :=
    (((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P)*U.toContinuousLinearMap*P) ∘L HP.subtypeL
  let ΓP : HP →L[ℝ] HP := e.conjStarAlgEquiv Γ
  let qP : HP := e q
  let HP0 := (innerSL ℝ qP).ker
  letI : NormedAddCommGroup HP0 := HP0.normedAddCommGroup
  letI : InnerProductSpace ℝ HP0 := HP0.innerProductSpace
  letI : CompleteSpace HP0 := (innerSL ℝ qP).isClosed_ker.completeSpace_coe
  let Hperp := P.ker
  letI : NormedAddCommGroup Hperp := Hperp.normedAddCommGroup
  letI : InnerProductSpace ℝ Hperp := Hperp.innerProductSpace
  letI : CompleteSpace Hperp := P.isClosed_ker.completeSpace_coe
  change HP0 →L[ℝ] Hperp at B0 V0
  change HP0 →L[ℝ] HP0 at ΓP0 Inv A0
  change Lp ℝ 2 J →L[ℝ] Hperp at R
  change (∀ g : Lp ℝ 2 J, (R g : Lp ℝ 2 J)=g-P g) at hR
  change (∀ g : Lp ℝ 2 J,
    B.adjoint g=HP0.subtypeL (B0.adjoint (R g))) at hAmbient
  change (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
    ∃ fP : HP0,
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
    (integral_congr_ae (Lp.coeFn_sub u v)).trans (integral_sub (hIntegrable u) (hIntegrable v))
  have hPself : IsSelfAdjoint P := isSelfAdjoint_starProjection HP
  let ι : HP0 →L[ℝ] Lp ℝ 2 J := HP.subtypeL ∘L HP0.subtypeL
  have hPι (u : HP0) : P (ι u)=ι u := hPf (u : HP)
  have hOrth (u : HP0) (h : Hperp) : inner ℝ (ι u) (h : Lp ℝ 2 J)=0 := by
    calc
      inner ℝ (ι u) (h : Lp ℝ 2 J)=inner ℝ (P (ι u)) (h : Lp ℝ 2 J) := by rw [hPι]
      _ = inner ℝ (ι u) (P (h : Lp ℝ 2 J)) := hPself.isSymmetric _ _
      _ = 0 := by rw [show P (h : Lp ℝ 2 J)=0 from h.property,inner_zero_right]
  have hMacro (u : HP0) : P (U (ι u))=ι (A0 u) := by
    change (A (u : HP) : Lp ℝ 2 J)=((A0 u : HP) : Lp ℝ 2 J)
    exact congrArg (fun x : HP => (x : Lp ℝ 2 J)) (hA0 u).symm
  have hMicro (u : HP0) : (B0 u : Lp ℝ 2 J)=U (ι u)-P (U (ι u)) := by
    rw [hB0]
    change U (P (ι u))-P (U (P (ι u)))=U (ι u)-P (U (ι u))
    rw [hPι]
  have hUι (u : HP0) : U (ι u)=ι (A0 u)+(B0 u : Lp ℝ 2 J) := by
    rw [hMicro,←hMacro]
    abel
  have hRmicro (h : Hperp) : R (h : Lp ℝ 2 J)=h := by
    apply Subtype.ext
    rw [hR,show P (h : Lp ℝ 2 J)=0 from h.property,sub_zero]
  have hRUm (u : HP0) : R (U (ι u))=B0 u := by
    apply Subtype.ext
    rw [hR]
    exact (hMicro u).symm
  have hVadjB (u : HP0) : V0.adjoint (B0 u)=ΓP0 u := by
    have hb := DFunLike.congr_fun hFactor u
    change B0 u=V0 (ΓP0 u) at hb
    rw [hb]
    exact DFunLike.congr_fun hVadj (ΓP0 u)
  have hΓself : IsSelfAdjoint ΓP0 := (show ΓP0.IsPositive from hPos0).isSelfAdjoint
  have hEnergy (u : HP0) : ‖A0 u‖^2+‖ΓP0 u‖^2=‖u‖^2 := by
    have h := congrArg (fun L : HP0 →L[ℝ] HP0 => inner ℝ (L u) u) hSquare0
    simp only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
      ContinuousLinearMap.one_apply,inner_add_left] at h
    rw [hA0self.isSymmetric (A0 u) u,hΓself.isSymmetric (ΓP0 u) u] at h
    simpa only [real_inner_self_eq_norm_sq] using h
  have hCross (u v : HP0) : inner ℝ (A0 u) (ΓP0 v)=inner ℝ (ΓP0 u) (A0 v) := by
    calc
      inner ℝ (A0 u) (ΓP0 v)=inner ℝ u (A0 (ΓP0 v)) := hA0self.isSymmetric _ _
      _ = inner ℝ u (ΓP0 (A0 v)) := congrArg (fun z : HP0 => inner ℝ u z) (DFunLike.congr_fun hComm0.eq v)
      _ = inner ℝ (ΓP0 u) (A0 v) := (hΓself.isSymmetric _ _).symm
  have hGlobal70 :
      (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
                            ∃ fP : HP0,
                              HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
                              let fperp : Hperp := R f
                              let fV : HP0 := V0.adjoint fperp
                              B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) ∧
                              HP0.subtypeL (ΓP0 fV)=ΓP (HP0.subtypeL fV) ∧
                              ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
                              let g : Lp ℝ 2 J := U (P f-(f-P f))
                              (∫ z, g z ∂J)=0 ∧
                              ∃ gP : HP0,
                                HP0.subtypeL gP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le g ∧
                                let gperp : Hperp := R g
                                let gV : HP0 := V0.adjoint gperp
                                gP=A0 fP-ΓP0 fV ∧
                                gV=ΓP0 fP+A0 fV ∧
                                ‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2) := by
    intro f hf
    obtain ⟨fP,hfP,hBf,hΓf,hBudget,hVBudget⟩ := hGlobal f hf
    let fperp : Hperp := R f
    let fV : HP0 := V0.adjoint fperp
    change B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) at hBf
    have hPfp : P f=ι fP :=
      (congrArg (fun x : HP => (x : Lp ℝ 2 J)) hfP).symm
    have hB0adjMicro : B0.adjoint fperp=ΓP0 fV := by
      apply Subtype.ext
      have h := (hAmbient (fperp : Lp ℝ 2 J)).symm.trans hBf
      rw [hRmicro] at h
      exact h
    let g : Lp ℝ 2 J := U (P f-(f-P f))
    have hgMean : (∫ z, g z ∂J)=0 := by
      change (∫ z, U (P f-(f-P f)) z ∂J)=0
      rw [hUIntegral]
      simp only [hSubIntegral,hPIntegral,hf,sub_self,sub_zero]
    obtain ⟨gP,hgP,hgtail⟩ := hGlobal g hgMean
    have hPgp : P g=ι gP :=
      (congrArg (fun x : HP => (x : Lp ℝ 2 J)) hgP).symm
    have hInput : P f-(f-P f)=ι fP-(fperp : Lp ℝ 2 J) := by
      change P f-(f-P f)=ι fP-(R f : Lp ℝ 2 J)
      rw [hR f,hPfp]
    have hgPformula : gP=A0 fP-ΓP0 fV := by
      apply ext_inner_left ℝ
      intro u
      calc
        inner ℝ u gP=inner ℝ (ι u) (ι gP) := rfl
        _ = inner ℝ (ι u) (P g) := by rw [hPgp]
        _ = inner ℝ (P (ι u)) g := (hPself.isSymmetric _ _).symm
        _ = inner ℝ (ι u) g := by rw [hPι]
        _ = inner ℝ (U (ι u)) (ι fP-(fperp : Lp ℝ 2 J)) := by
          change inner ℝ (ι u) (U (P f-(f-P f)))=_
          rw [hInput]
          exact (hUs.isSymmetric _ _).symm
        _ = inner ℝ (A0 u) fP-inner ℝ (B0 u) fperp := by
          rw [hUι,inner_add_left,inner_sub_right,inner_sub_right,
            hOrth (A0 u) fperp,
            show inner ℝ (B0 u : Lp ℝ 2 J) (ι fP)=0 from
              (real_inner_comm _ _).trans (hOrth fP (B0 u))]
          change (inner ℝ (A0 u) fP-0)+(0-inner ℝ (B0 u) fperp)=_
          ring
        _ = inner ℝ u (A0 fP)-inner ℝ u (ΓP0 fV) := by
          rw [hA0self.isSymmetric u fP,←B0.adjoint_inner_right,hB0adjMicro]
        _ = inner ℝ u (A0 fP-ΓP0 fV) := (inner_sub_right _ _ _).symm
    have hgVformula : V0.adjoint (R g)=ΓP0 fP+A0 fV := by
      change V0.adjoint (R (U (P f-(f-P f))))=_
      rw [hInput,map_sub,map_sub,hRUm,map_sub,hVadjB]
      have hd := DFunLike.congr_fun hIntertwine fperp
      change V0.adjoint (D fperp)= -(A0 fV) at hd
      change ΓP0 fP-V0.adjoint (D fperp)=_
      rw [hd,sub_neg_eq_add]
    have hgEnergy : ‖gP‖^2+‖V0.adjoint (R g)‖^2=‖fP‖^2+‖fV‖^2 := by
      rw [hgPformula,hgVformula,norm_sub_sq_real,norm_add_sq_real,hCross]
      nlinarith only [hEnergy fP,hEnergy fV]
    exact ⟨fP,hfP,hBf,hΓf,hBudget,hVBudget,hgMean,gP,hgP,hgPformula,hgVformula,hgEnergy⟩
  have hFinal :
      (∀ h : Hperp, (D h : Lp ℝ 2 J)=U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J))) ∧
      V0.adjoint ∘L D= -(A0 ∘L V0.adjoint) ∧
      (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
                            ∃ fP : HP0,
                              HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
                              let fperp : Hperp := R f
                              let fV : HP0 := V0.adjoint fperp
                              B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) ∧
                              HP0.subtypeL (ΓP0 fV)=ΓP (HP0.subtypeL fV) ∧
                              ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
                              let g : Lp ℝ 2 J := U (P f-(f-P f))
                              (∫ z, g z ∂J)=0 ∧
                              ∃ gP : HP0,
                                HP0.subtypeL gP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le g ∧
                                let gperp : Hperp := R g
                                let gV : HP0 := V0.adjoint gperp
                                gP=A0 fP-ΓP0 fV ∧
                                gV=ΓP0 fP+A0 fV ∧
                                ‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2) := ⟨hD,hIntertwine,hGlobal70⟩
  refine ⟨hμ, ?_⟩
  refine ⟨hJ, ?_⟩
  refine ⟨hν, ?_⟩
  refine ⟨hRange, ?_⟩
  refine ⟨hPf, ?_⟩
  refine ⟨S, ?_⟩
  refine ⟨hS, ?_⟩
  refine ⟨hSd, ?_⟩
  refine ⟨hSc, ?_⟩
  refine ⟨hSf, ?_⟩
  refine ⟨hSs, ?_⟩
  refine ⟨e, ?_⟩
  refine ⟨he, ?_⟩
  refine ⟨U, ?_⟩
  refine ⟨hU, ?_⟩
  refine ⟨hUi, ?_⟩
  refine ⟨hUs, ?_⟩
  refine ⟨T, ?_⟩
  refine ⟨hTs, ?_⟩
  refine ⟨hAll, ?_⟩
  refine ⟨hAeq, ?_⟩
  refine ⟨hAs, ?_⟩
  refine ⟨hAn, ?_⟩
  refine ⟨hPB, ?_⟩
  refine ⟨Γ, ?_⟩
  refine ⟨hΓ, ?_⟩
  refine ⟨hΓSq, ?_⟩
  refine ⟨hCommRoot, ?_⟩
  refine ⟨hΓP, ?_⟩
  refine ⟨hΓPSq, ?_⟩
  refine ⟨hCommP, ?_⟩
  refine ⟨hGram, ?_⟩
  refine ⟨q, ?_⟩
  refine ⟨hqa, ?_⟩
  refine ⟨hTq, ?_⟩
  refine ⟨hq, ?_⟩
  refine ⟨hCenter, ?_⟩
  refine ⟨hΓPq, ?_⟩
  refine ⟨hγ, ?_⟩
  refine ⟨ΓP0, ?_⟩
  refine ⟨hΓP0, ?_⟩
  refine ⟨hPos0, ?_⟩
  refine ⟨hOrder0, ?_⟩
  refine ⟨hUnit, ?_⟩
  refine ⟨Inv, ?_⟩
  refine ⟨hLeft, ?_⟩
  refine ⟨hRight, ?_⟩
  refine ⟨hNormInv, ?_⟩
  refine ⟨hInvSelf,A0,hA0,hA0self,hComm0,hSquare0,hCommInv,?_⟩
  refine ⟨B0, ?_⟩
  refine ⟨hB0, ?_⟩
  refine ⟨V0, ?_⟩
  refine ⟨hVdef, ?_⟩
  refine ⟨hFactor, ?_⟩
  refine ⟨hVadj, ?_⟩
  refine ⟨hVnorm, ?_⟩
  refine ⟨R, ?_⟩
  refine ⟨hR, ?_⟩
  refine ⟨hAmbient, ?_⟩
  exact hFinal

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation
