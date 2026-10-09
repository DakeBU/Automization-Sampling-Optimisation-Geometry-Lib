  have hGramLocal : B.adjoint ∘L B=ΓP*ΓP := hGram
  have hRootq : ΓP qP=0 := hΓPq
  have hBq : B qP=0 := by
    have hn := B.apply_norm_sq_eq_inner_adjoint_right qP
    rw [hGramLocal] at hn
    have hz : (ΓP*ΓP) qP=0 := by
      change ΓP (ΓP qP)=0
      rw [hRootq,map_zero]
    rw [hz,inner_zero_right] at hn
    exact norm_eq_zero.mp (sq_eq_zero_iff.mp hn)
  have hBCenter (g : Lp ℝ 2 J) : B.adjoint g ∈ HP0 := by
    change inner ℝ qP (B.adjoint g)=0
    rw [B.adjoint_inner_right,hBq,inner_zero_left]
  have hAmbient (g : Lp ℝ 2 J) :
      B.adjoint g=HP0.subtypeL (B0.adjoint (R g)) := by
    let b : HP0 := ⟨B.adjoint g,hBCenter g⟩
    have heq : b=B0.adjoint (R g) := by
      apply ext_inner_left ℝ
      intro u
      change inner ℝ (u : HP) (B.adjoint g)=inner ℝ u (B0.adjoint (R g))
      rw [B.adjoint_inner_right,B0.adjoint_inner_right]
      change inner ℝ (B (u : HP)) g=inner ℝ (B0 u : Lp ℝ 2 J) (R g : Lp ℝ 2 J)
      rw [hB0,hR,inner_sub_right]
      have ho : inner ℝ (B (u : HP)) (P g)=0 := by
        rw [← hPself,hPB,inner_zero_left]
      rw [ho,sub_zero]
    exact congrArg (fun z : HP0 => HP0.subtypeL z) heq
