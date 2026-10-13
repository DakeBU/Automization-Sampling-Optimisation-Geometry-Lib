import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation

/-!
# Actual PBPS corrector change under the actual reflection step

Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix B.3, the actual
projected rotation and two-component energy used in (B.21) and Lemma B.4.
The reflected observable and its conditional/polar components are actual
inputs and outputs. Mean preservation is proved internally from the same law.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 4000000

private def actual_corrector_change_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) : Prop :=
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
                                ‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2 ∧
                                let C : HP0 → HP0 → ℝ := fun u v =>
                                  (‖u‖^2-‖v‖^2)/2-inner ℝ (A0 (Inv u)) v
                                C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2)

theorem actual_corrector_change
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) : actual_corrector_change_statement (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη := by
  unfold actual_corrector_change_statement
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
  have hBase := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation
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
                              ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
                              let g : Lp ℝ 2 J := U (P f-(f-P f))
                              (∫ z, g z ∂J)=0 ∧
                              ∃ gP : HP0,
                                HP0.subtypeL gP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le g ∧
                                let gperp : Hperp := R g
                                let gV : HP0 := V0.adjoint gperp
                                gP=A0 fP-ΓP0 fV ∧
                                gV=ΓP0 fP+A0 fV ∧
                                ‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2) at hGlobal
  let D : Hperp →L[ℝ] Hperp := R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL
  have hD (h : Hperp) : (D h : Lp ℝ 2 J)=
      U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J)) := hDparent h
  have hIntertwine : V0.adjoint ∘L D= -(A0 ∘L V0.adjoint) := hIntertwineParent
  have hΓself : IsSelfAdjoint ΓP0 := (show ΓP0.IsPositive from hPos0).isSelfAdjoint
  have hEnergy (u : HP0) : ‖A0 u‖^2+‖ΓP0 u‖^2=‖u‖^2 := by
    have h := congrArg (fun L : HP0 →L[ℝ] HP0 => inner ℝ (L u) u) hSquare0
    simp only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
      ContinuousLinearMap.one_apply,inner_add_left] at h
    have ha : inner ℝ (A0 (A0 u)) u=‖A0 u‖^2 :=
      (hA0self.isSymmetric (A0 u) u).trans (real_inner_self_eq_norm_sq _)
    have hg : inner ℝ (ΓP0 (ΓP0 u)) u=‖ΓP0 u‖^2 :=
      (hΓself.isSymmetric (ΓP0 u) u).trans (real_inner_self_eq_norm_sq _)
    rw [ha,hg,real_inner_self_eq_norm_sq] at h
    exact h
  have hCross (u v : HP0) : inner ℝ (A0 u) (ΓP0 v)=inner ℝ (ΓP0 u) (A0 v) := by
    calc
      inner ℝ (A0 u) (ΓP0 v)=inner ℝ u (A0 (ΓP0 v)) := hA0self.isSymmetric _ _
      _ = inner ℝ u (ΓP0 (A0 v)) := congrArg (fun z : HP0 => inner ℝ u z) (DFunLike.congr_fun hComm0.eq v)
      _ = inner ℝ (ΓP0 u) (A0 v) := (hΓself.isSymmetric _ _).symm
  let K : HP0 →L[ℝ] HP0 := A0 ∘L Inv
  have hInvΓ (u : HP0) : Inv (ΓP0 u)=u := by
    have h := DFunLike.congr_fun hLeft u
    simpa only [ContinuousLinearMap.mul_apply,ContinuousLinearMap.one_apply] using h
  have hΓInv (u : HP0) : ΓP0 (Inv u)=u := by
    have h := DFunLike.congr_fun hRight u
    simpa only [ContinuousLinearMap.mul_apply,ContinuousLinearMap.one_apply] using h
  have hCommEval (u : HP0) : A0 (ΓP0 u)=ΓP0 (A0 u) :=
    DFunLike.congr_fun hComm0.eq u
  have hCommInvEval (u : HP0) : A0 (Inv u)=Inv (A0 u) :=
    DFunLike.congr_fun hCommInv.eq u
  have hKΓ (u : HP0) : K (ΓP0 u)=A0 u := congrArg A0 (hInvΓ u)
  have hΓK (u : HP0) : ΓP0 (K u)=A0 u := by
    change ΓP0 (A0 (Inv u))=A0 u
    calc
      ΓP0 (A0 (Inv u))=A0 (ΓP0 (Inv u)) := (hCommEval (Inv u)).symm
      _ = A0 u := congrArg A0 (hΓInv u)
  have hKA (u : HP0) : K (A0 u)=A0 (K u) := by
    change A0 (Inv (A0 u))=A0 (A0 (Inv u))
    exact congrArg A0 (hCommInvEval u).symm
  have hSquareApply (u : HP0) : A0 (A0 u)+ΓP0 (ΓP0 u)=u := by
    have h := DFunLike.congr_fun hSquare0 u
    simpa only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
      ContinuousLinearMap.one_apply] using h
  have hKMixedVector (u : HP0) : A0 (K (A0 u))+ΓP0 (A0 u)=K u := by
    calc
      A0 (K (A0 u))+ΓP0 (A0 u)=K (A0 (A0 u))+K (ΓP0 (ΓP0 u)) :=
        congrArg₂ (fun x y : HP0 => x+y) (hKA (A0 u)).symm
          ((hCommEval u).symm.trans (hKΓ (ΓP0 u)).symm)
      _ = K (A0 (A0 u)+ΓP0 (ΓP0 u)) := (K.map_add _ _).symm
      _ = K u := congrArg K (hSquareApply u)
  have hMixed (u v : HP0) :
      inner ℝ (K (A0 u)) (A0 v)+inner ℝ (A0 u) (ΓP0 v)=inner ℝ (K u) v := by
    calc
      inner ℝ (K (A0 u)) (A0 v)+inner ℝ (A0 u) (ΓP0 v)=
          inner ℝ (A0 (K (A0 u))) v+inner ℝ (ΓP0 (A0 u)) v :=
        congrArg₂ (fun x y : ℝ => x+y)
          (hA0self.isSymmetric (K (A0 u)) v).symm
          (hΓself.isSymmetric (A0 u) v).symm
      _ = inner ℝ (A0 (K (A0 u))+ΓP0 (A0 u)) v := (inner_add_left _ _ _).symm
      _ = inner ℝ (K u) v := by rw [hKMixedVector]
  have hDiagL (u : HP0) : inner ℝ (K (A0 u)) (ΓP0 u)=‖A0 u‖^2 := by
    calc
      inner ℝ (K (A0 u)) (ΓP0 u)=inner ℝ (ΓP0 (K (A0 u))) u :=
        (hΓself.isSymmetric _ _).symm
      _ = inner ℝ (A0 (A0 u)) u := by rw [hΓK]
      _ = inner ℝ (A0 u) (A0 u) := hA0self.isSymmetric _ _
      _ = ‖A0 u‖^2 := real_inner_self_eq_norm_sq _
  have hDiagR (v : HP0) : inner ℝ (K (ΓP0 v)) (A0 v)=‖A0 v‖^2 := by
    rw [hKΓ,real_inner_self_eq_norm_sq]
  have hSwap (u v : HP0) : inner ℝ (ΓP0 u) (A0 v)=inner ℝ (A0 u) (ΓP0 v) :=
    (hCross u v).symm
  have hSwap2 (u v : HP0) : inner ℝ (A0 v) (ΓP0 u)=inner ℝ (A0 u) (ΓP0 v) :=
    (real_inner_comm _ _).trans (hSwap u v)
  have hCorrector (u v : HP0) :
      ((‖A0 u-ΓP0 v‖^2-‖ΓP0 u+A0 v‖^2)/2-
        inner ℝ (K (A0 u-ΓP0 v)) (ΓP0 u+A0 v))-
      ((‖u‖^2-‖v‖^2)/2-inner ℝ (K u) v)= -‖u‖^2+‖v‖^2 := by
    rw [norm_sub_sq_real,norm_add_sq_real,map_sub,inner_sub_left,
      inner_add_right,inner_add_right,hDiagL,hDiagR,hKΓ,hSwap2,hSwap]
    nlinarith only [hEnergy u,hEnergy v,hMixed u v]
  have hGlobal71 :
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
                                ‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2 ∧
                                let C : HP0 → HP0 → ℝ := fun u v =>
                                  (‖u‖^2-‖v‖^2)/2-inner ℝ (A0 (Inv u)) v
                                C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2) := by
    intro f hf
    obtain ⟨fP,hfP,hBf,hΓf,hBudget,hVBudget,hgMean,gP,hgP,hgPformula,hgVformula,hgEnergy⟩ :=
      hGlobal f hf
    refine ⟨fP,hfP,hBf,hΓf,hBudget,hVBudget,hgMean,gP,hgP,hgPformula,hgVformula,hgEnergy,?_⟩
    change ((‖gP‖^2-‖V0.adjoint (R (U (P f-(f-P f))))‖^2)/2-
        inner ℝ (K gP) (V0.adjoint (R (U (P f-(f-P f))))))-
      ((‖fP‖^2-‖V0.adjoint (R f)‖^2)/2-inner ℝ (K fP) (V0.adjoint (R f)))=
      -‖fP‖^2+‖V0.adjoint (R f)‖^2
    let fV : HP0 := V0.adjoint (R f)
    let gV : HP0 := V0.adjoint (R (U (P f-(f-P f))))
    have hgp : gP=A0 fP-ΓP0 fV := hgPformula
    have hgv : gV=ΓP0 fP+A0 fV := hgVformula
    let C : HP0 → HP0 → ℝ := fun u v => (‖u‖^2-‖v‖^2)/2-inner ℝ (K u) v
    change C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2
    have hPair : C gP gV=C (A0 fP-ΓP0 fV) (ΓP0 fP+A0 fV) :=
      congrArg₂ C hgp hgv
    exact (congrArg (fun a : ℝ => a-C fP fV) hPair).trans (hCorrector fP fV)
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
                                ‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2 ∧
                                let C : HP0 → HP0 → ℝ := fun u v =>
                                  (‖u‖^2-‖v‖^2)/2-inner ℝ (A0 (Inv u)) v
                                C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2) := ⟨hD,hIntertwine,hGlobal71⟩
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
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange.actual_corrector_change
