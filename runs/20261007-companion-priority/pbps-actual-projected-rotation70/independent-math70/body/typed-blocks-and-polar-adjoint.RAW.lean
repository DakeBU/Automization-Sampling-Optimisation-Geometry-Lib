    (integral_congr_ae (Lp.coeFn_sub u v)).trans (integral_sub (hIntegrable u) (hIntegrable v))
  have hPself : IsSelfAdjoint P := isSelfAdjoint_starProjection HP
  let ι : HP0 →L[ℝ] Lp ℝ 2 J := HP.subtypeL ∘L HP0.subtypeL
  have hPι (u : HP0) : P (ι u)=ι u := hPf (u : HP)
  have hOrth (u : HP0) (h : Hperp) : inner ℝ (ι u) (h : Lp ℝ 2 J)=0 := by
    calc
      inner ℝ (ι u) (h : Lp ℝ 2 J)=inner ℝ (P (ι u)) (h : Lp ℝ 2 J) := by rw [hPι]
      _ = inner ℝ (ι u) (P (h : Lp ℝ 2 J)) := hPself.isSymmetric _ _
      _ = 0 := by rw [show P (h : Lp ℝ 2 J)=0 from h.property,inner_zero_right]
  have hMacro (u : HP0) : P (U (ι u))=ι (A0 u) := by
    change (A (u : HP) : Lp ℝ 2 J)=((A0 u : HP) : Lp ℝ 2 J)
    exact congrArg (fun x : HP => (x : Lp ℝ 2 J)) (hA0 u).symm
  have hMicro (u : HP0) : (B0 u : Lp ℝ 2 J)=U (ι u)-P (U (ι u)) := by
    rw [hB0]
    change U (P (ι u))-P (U (P (ι u)))=U (ι u)-P (U (ι u))
    rw [hPι]
  have hUι (u : HP0) : U (ι u)=ι (A0 u)+(B0 u : Lp ℝ 2 J) := by
    rw [hMicro,←hMacro]
    abel
  have hRmicro (h : Hperp) : R (h : Lp ℝ 2 J)=h := by
    apply Subtype.ext
    rw [hR,show P (h : Lp ℝ 2 J)=0 from h.property,sub_zero]
  have hRUm (u : HP0) : R (U (ι u))=B0 u := by
    apply Subtype.ext
    rw [hR]
    exact (hMicro u).symm
  have hVadjB (u : HP0) : V0.adjoint (B0 u)=ΓP0 u := by
    have hb := DFunLike.congr_fun hFactor u
    change B0 u=V0 (ΓP0 u) at hb
