  letI : NormedSpace ℝ (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) :=
    NormedSpace.restrictScalars ℝ ℂ (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  letI := IsStarNormal.instNonUnitalContinuousFunctionalCalculus
    (A := Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  letI : NonUnitalContinuousFunctionalCalculus ℂ
      (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) IsStarNormal :=
    NonUnitalClosedEmbeddingContinuousFunctionalCalculus.toNonUnitalContinuousFunctionalCalculus
  letI : NonUnitalContinuousFunctionalCalculus ℝ
      (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) IsSelfAdjoint :=
    IsSelfAdjoint.instNonUnitalContinuousFunctionalCalculus
      (A := Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  let ι : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
  let R : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.reCLM.compLpL 2 μ
  let Q : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.imCLM.compLpL 2 μ
  obtain ⟨hNorm,_,Ac,hAc,hAf,hAi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ A hA
  obtain ⟨_,_,Bc,hBc,hBf,hBi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ B hB
  obtain ⟨_,_,Dc,hDc,hDf,hDi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ (B*B-A*A) hSquareOrder
  have hAi' (u : Lp ℝ 2 μ) : Ac (ι u)=ι (A u) := hAi u
  have hBi' (u : Lp ℝ 2 μ) : Bc (ι u)=ι (B u) := hBi u
  have hComplexDiff : Bc*Bc-Ac*Ac=Dc := by
    apply ContinuousLinearMap.ext
    intro g
    change Bc (Bc g) - Ac (Ac g)=Dc g
    rw [hBf g,hAf g,map_add,map_smul,map_add,map_smul,hBi,hBi,hAi,hAi,hDf g]
    simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.mul_apply,map_sub,smul_sub]
    abel
