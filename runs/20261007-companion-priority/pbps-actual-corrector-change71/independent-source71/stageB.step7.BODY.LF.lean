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
