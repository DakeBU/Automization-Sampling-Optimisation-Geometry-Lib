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
      simp only [hSubIntegral,hPIntegral,hf,sub_self]
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
