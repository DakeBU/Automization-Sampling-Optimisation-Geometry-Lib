  have hKself : IsSelfAdjoint (A0*Inv) := (hA0self.commute_iff hInvSelf).mp hCommInv
  have hCoefficient : (1 : HP0 →L[ℝ] HP0)+(A0*Inv)*(A0*Inv)=Inv*Inv := by
    have hFirst : (ΓP0*ΓP0)*(Inv*Inv)=(1 : HP0 →L[ℝ] HP0) := by
      calc
        (ΓP0*ΓP0)*(Inv*Inv)=ΓP0*((ΓP0*Inv)*Inv) := by noncomm_ring
        _ = (1 : HP0 →L[ℝ] HP0) := by rw [hRight,one_mul,hRight]
    have hSecond : (A0*Inv)*(A0*Inv)=(A0*A0)*(Inv*Inv) := by
      calc
        (A0*Inv)*(A0*Inv)=A0*((Inv*A0)*Inv) := by noncomm_ring
        _ = A0*((A0*Inv)*Inv) := by rw [hCommInv.eq.symm]
        _ = (A0*A0)*(Inv*Inv) := by noncomm_ring
    calc
      (1 : HP0 →L[ℝ] HP0)+(A0*Inv)*(A0*Inv)=
          (ΓP0*ΓP0)*(Inv*Inv)+(A0*A0)*(Inv*Inv) := by rw [hFirst,hSecond]
      _ = (ΓP0*ΓP0+A0*A0)*(Inv*Inv) := by rw [add_mul]
      _ = Inv*Inv := by rw [add_comm,hSquare0,one_mul]
