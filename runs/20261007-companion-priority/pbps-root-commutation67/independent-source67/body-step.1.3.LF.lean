  have hComm0 : Commute A0 ΓP0 := by
    apply ContinuousLinearMap.ext
    intro u
    apply Subtype.ext
    change (A0 (ΓP0 u) : HP)=(ΓP0 (A0 u) : HP)
    rw [hA0,hΓP0,hΓP0,hA0]
    exact congrArg (fun D : HP →L[ℝ] HP => D (u : HP)) hCommP.eq.symm
  have hSquare0 : A0*A0+ΓP0*ΓP0=(1 : HP0 →L[ℝ] HP0) := by
    apply ContinuousLinearMap.ext
    intro u
    apply Subtype.ext
    change (A0 (A0 u) : HP)+(ΓP0 (ΓP0 u) : HP)=(u : HP)
    rw [hA0,hA0,hΓP0,hΓP0]
    have h : ΓP (ΓP (u : HP))=(u : HP)-A (A (u : HP)) :=
      congrArg (fun D : HP →L[ℝ] HP => D (u : HP)) hΓPSq
    rw [h]
    abel
