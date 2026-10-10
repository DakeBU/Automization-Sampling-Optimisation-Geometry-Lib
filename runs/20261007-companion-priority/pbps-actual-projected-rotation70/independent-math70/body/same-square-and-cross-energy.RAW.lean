    rw [hb]
    exact DFunLike.congr_fun hVadj (ΓP0 u)
  have hΓself : IsSelfAdjoint ΓP0 := (show ΓP0.IsPositive from hPos0).isSelfAdjoint
  have hEnergy (u : HP0) : ‖A0 u‖^2+‖ΓP0 u‖^2=‖u‖^2 := by
    have h := congrArg (fun L : HP0 →L[ℝ] HP0 => inner ℝ (L u) u) hSquare0
    simp only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
      ContinuousLinearMap.one_apply,inner_add_left] at h
    have ha : inner ℝ (A0 (A0 u)) u=‖A0 u‖^2 :=
      (hA0self.isSymmetric (A0 u) u).trans (real_inner_self_eq_norm_sq _)
    have hg : inner ℝ (ΓP0 (ΓP0 u)) u=‖ΓP0 u‖^2 :=
      (hΓself.isSymmetric (ΓP0 u) u).trans (real_inner_self_eq_norm_sq _)
    rw [ha,hg,real_inner_self_eq_norm_sq] at h
    exact h
  have hCross (u v : HP0) : inner ℝ (A0 u) (ΓP0 v)=inner ℝ (ΓP0 u) (A0 v) := by
    calc
      inner ℝ (A0 u) (ΓP0 v)=inner ℝ u (A0 (ΓP0 v)) := hA0self.isSymmetric _ _
      _ = inner ℝ u (ΓP0 (A0 v)) := congrArg (fun z : HP0 => inner ℝ u z) (DFunLike.congr_fun hComm0.eq v)
      _ = inner ℝ (ΓP0 u) (A0 v) := (hΓself.isSymmetric _ _).symm
  have hGlobal70 :
      (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
