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
