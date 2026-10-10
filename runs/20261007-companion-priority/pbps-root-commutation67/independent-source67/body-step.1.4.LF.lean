  have hStarInv : ΓP0*star Inv=(1 : HP0 →L[ℝ] HP0) := by
    have h := congrArg (fun D : HP0 →L[ℝ] HP0 => star D) hLeftLocal
    simpa only [star_mul,hPosLocal.isSelfAdjoint.star_eq,star_one] using h
  have hInvSelf : IsSelfAdjoint Inv := by
    change star Inv=Inv
    calc
      star Inv=(Inv*ΓP0)*star Inv := by rw [hLeft,one_mul]
      _ = Inv*(ΓP0*star Inv) := mul_assoc _ _ _
      _ = Inv := by rw [hStarInv,mul_one]
  have hCommInv : Commute A0 Inv := by
    change A0*Inv=Inv*A0
    calc
      A0*Inv=(Inv*ΓP0)*(A0*Inv) := by rw [hLeft,one_mul]
      _ = Inv*((ΓP0*A0)*Inv) := by noncomm_ring
      _ = Inv*((A0*ΓP0)*Inv) := by rw [hComm0.eq.symm]
      _ = Inv*A0 := by simp only [mul_assoc,hRight,mul_one]
