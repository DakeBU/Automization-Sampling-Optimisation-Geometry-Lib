  classical
  dsimp only
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
  have hBase := AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry.actual_centered_polar_isometry
    (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  dsimp only at hBase
  rcases hBase with
    ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,
      T,hTs,hAll,hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,
      q,hqa,hTq,hq,hCenter,hΓPq,hγ,ΓP0,hΓP0,hPos0,hOrder0,hUnit,
      Inv,hLeft,hRight,hNormInv,B0,hB0,V0,hVdef,hFactor,hVadj,hVnorm⟩
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
  change HP0 →L[ℝ] HP0 at ΓP0 Inv
  letI : IsProbabilityMeasure J := hJ
  letI : IsProbabilityMeasure ν := hν
  let C : Lp ℝ 2 J →L[ℝ] HP := condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le
  have hPself (g k : Lp ℝ 2 J) : inner ℝ (P g) k=inner ℝ g (P k) :=
    inner_condExpL2_left_eq_right measurable_snd.comap_le
  have hPid (g : Lp ℝ 2 J) : P (P g)=P g := hPf (C g)
  let R : Lp ℝ 2 J →L[ℝ] Hperp :=
    ((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P).codRestrict Hperp (by
      intro g
      change P (g-P g)=0
      rw [map_sub,hPid,sub_self])
  have hR (g : Lp ℝ 2 J) : (R g : Lp ℝ 2 J)=g-P g := rfl
  have hRself (g : Hperp) : R (g : Lp ℝ 2 J)=g := by
    apply Subtype.ext
    change (g : Lp ℝ 2 J)-P g=g
    rw [show P (g : Lp ℝ 2 J)=0 from g.property,sub_zero]
