  refine ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,hAll,
    hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,q,hqa,hTq,hq,hCenter,hΓPq,hγ,
    ΓP0,hΓP0,hPos0,hOrder0,hUnit,Inv,hLeft,hRight,hNormInv,B0,hB0,V0,hVdef,
    hFactor,hVadj,hVnorm,R,hR,hAmbient,?_⟩
  intro f hf
  have hCf : C f ∈ HP0 := by
    change inner ℝ qP (C f)=0
    change inner ℝ (qP : Lp ℝ 2 J) (P f)=0
    rw [← hPself,hPq,hqIntegral,hf]
  let fP : HP0 := ⟨C f,hCf⟩
  refine ⟨fP,rfl,?_,?_,?_,hVcontract (R f)⟩
  · calc
      B.adjoint (R f : Lp ℝ 2 J)=HP0.subtypeL (B0.adjoint (R (R f))) := hAmbient _
      _ = HP0.subtypeL (B0.adjoint (R f)) := congrArg
        (fun z : Hperp => HP0.subtypeL (B0.adjoint z)) (hRself (R f))
      _ = HP0.subtypeL (ΓP0 (V0.adjoint (R f))) :=
        congrArg (fun z : HP0 => HP0.subtypeL z)
          (congrArg (fun D : Hperp →L[ℝ] HP0 => D (R f)) hBAdj)
  · exact hΓP0 _
  · have hn := HP.norm_sq_eq_add_norm_sq_starProjection f
    have hProj : HP.starProjection=P := rfl
    rw [hProj,HP.starProjection_orthogonal_val] at hn
    change ‖f‖^2=‖(C f : Lp ℝ 2 J)‖^2+‖f-P f‖^2 at hn
    exact hn
