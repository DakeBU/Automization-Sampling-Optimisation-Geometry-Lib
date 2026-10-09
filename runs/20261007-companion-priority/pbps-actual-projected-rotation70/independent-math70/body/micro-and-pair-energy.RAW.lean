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
