import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation
import AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound

/-!
# The actual PBPS sharp first-corrector estimate

Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix B.3, (B.20)--(B.24).
The private literal statement expands every original input and every witness;
it introduces no mathematical provider. Production uses production parents.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

private def actual_sharp_corrector_bound_statement
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
                      IsSelfAdjoint (A0*Inv) ∧
                      (1 : HP0 →L[ℝ] HP0)+(A0*Inv)*(A0*Inv)=Inv*Inv ∧
                    let C : HP0 → HP0 → ℝ := fun u v =>
                      (1/2 : ℝ)*(‖u‖^2-‖v‖^2)-inner ℝ ((A0*Inv) u) v
                    (∀ u v : HP0, |C u v| ≤ (‖u‖^2+‖v‖^2)/(2*γ)) ∧
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
                          (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
                            ∃ fP : HP0,
                              HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
                              let fperp : Hperp := R f
                              let fV : HP0 := V0.adjoint fperp
                              B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) ∧
                              HP0.subtypeL (ΓP0 fV)=ΓP (HP0.subtypeL fV) ∧
                              ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
                              ‖fP‖^2+‖fV‖^2≤‖f‖^2 ∧
                              |C fP fV|≤‖f‖^2/(2*γ))


theorem actual_sharp_corrector_bound
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) : actual_sharp_corrector_bound_statement (E := E) (V := V) (α := α) (β := β) (η := η) hα hαβ hV hH hη hβη := by
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
  have hBase := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation
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
  have hGlobal := parentSlice65
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
  have hKself : IsSelfAdjoint (A0*Inv) := (hA0self.commute_iff hInvSelf).mp hCommInv
  have hCoefficient : (1 : HP0 →L[ℝ] HP0)+(A0*Inv)*(A0*Inv)=Inv*Inv := by
    have hFirst : (ΓP0*ΓP0)*(Inv*Inv)=(1 : HP0 →L[ℝ] HP0) := by
      calc
        (ΓP0*ΓP0)*(Inv*Inv)=ΓP0*((ΓP0*Inv)*Inv) := by noncomm_ring
        _ = (1 : HP0 →L[ℝ] HP0) := by rw [hRight,one_mul,hRight]
    have hSecond : (A0*Inv)*(A0*Inv)=(A0*A0)*(Inv*Inv) := by
      calc
        (A0*Inv)*(A0*Inv)=A0*((Inv*A0)*Inv) := by noncomm_ring
        _ = A0*((A0*Inv)*Inv) := by rw [hCommInv.eq.symm]
        _ = (A0*A0)*(Inv*Inv) := by noncomm_ring
    calc
      (1 : HP0 →L[ℝ] HP0)+(A0*Inv)*(A0*Inv)=
          (ΓP0*ΓP0)*(Inv*Inv)+(A0*A0)*(Inv*Inv) := by rw [hFirst,hSecond]
      _ = (ΓP0*ΓP0+A0*A0)*(Inv*Inv) := by rw [add_mul]
      _ = Inv*Inv := by rw [add_comm,hSquare0,one_mul]
  let γ : ℝ := 2*Real.sqrt ((α : ℝ)*η)/(1+(α : ℝ)*η)
  change 0 < γ at hγ
  change ‖Inv‖ ≤ 1/γ at hNormInv
  let C : HP0 → HP0 → ℝ := fun u v =>
    (1/2 : ℝ)*(‖u‖^2-‖v‖^2)-inner ℝ ((A0*Inv) u) v
  have hPair (u v : HP0) : |C u v| ≤ (‖u‖^2+‖v‖^2)/(2*γ) := by
    have h := AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.quadratic_corrector_bound_of_square_identity
      (A0*Inv) Inv hKself hInvSelf hCoefficient (1/γ) (by positivity) hNormInv u v
    change |C u v| ≤ ((1/γ)/2)*(‖u‖^2+‖v‖^2) at h
    calc
      |C u v| ≤ ((1/γ)/2)*(‖u‖^2+‖v‖^2) := h
      _ = (‖u‖^2+‖v‖^2)/(2*γ) := by
        field_simp
  have hFinal : ∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
      ∃ fP : HP0,
        HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
        let fperp : Hperp := R f
        let fV : HP0 := V0.adjoint fperp
        B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) ∧
        HP0.subtypeL (ΓP0 fV)=ΓP (HP0.subtypeL fV) ∧
        ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
        ‖fP‖^2+‖fV‖^2≤‖f‖^2 ∧ |C fP fV|≤‖f‖^2/(2*γ) := by
    intro f hf
    obtain ⟨fP,hGlobalFields⟩ := hGlobal f hf
    have hfP := hGlobalFields.1
    have hBf := hGlobalFields.2.1
    have hΓf := hGlobalFields.2.2.1
    have hPyth := hGlobalFields.2.2.2.1
    have hNormV := hGlobalFields.2.2.2.2
    let fperp : Hperp := R f
    let fV : HP0 := V0.adjoint fperp
    have hBudget : ‖fP‖^2+‖fV‖^2 ≤ ‖f‖^2 := by
      have hs := (sq_le_sq₀ (norm_nonneg fV) (norm_nonneg fperp)).2 hNormV
      nlinarith only [hPyth, hs]
    refine ⟨fP,hfP,hBf,hΓf,hPyth,hNormV,hBudget,?_⟩
    exact (hPair fP fV).trans (div_le_div_of_nonneg_right hBudget (by positivity))
  unfold actual_sharp_corrector_bound_statement
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
  refine ⟨hInvSelf,A0,hA0,hA0self,hComm0,hSquare0,hCommInv,hKself,hCoefficient,hPair,?_⟩
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
end AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound
