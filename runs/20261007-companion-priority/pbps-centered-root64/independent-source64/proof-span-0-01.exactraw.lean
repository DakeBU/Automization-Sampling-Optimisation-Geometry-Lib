  have hAcNonneg : 0 ≤ Ac := (ContinuousLinearMap.nonneg_iff_isPositive Ac).mpr hAc
  have hBcNonneg : 0 ≤ Bc := (ContinuousLinearMap.nonneg_iff_isPositive Bc).mpr hBc
  have hSqLe : Ac*Ac ≤ Bc*Bc := by
    apply (ContinuousLinearMap.le_def _ _).mpr
    rw [hComplexDiff]
    exact hDc
  have hLe : Ac ≤ Bc := by
    have h := CFC.sqrt_le_sqrt (Ac*Ac) (Bc*Bc) hSqLe
    have ha : CFC.sqrt (Ac*Ac)=Ac := CFC.sqrt_unique rfl hAcNonneg
    have hb : CFC.sqrt (Bc*Bc)=Bc := CFC.sqrt_unique rfl hBcNonneg
    exact ha.symm.le.trans (h.trans hb.le)
  have hDiff : (Bc-Ac).IsPositive := (ContinuousLinearMap.le_def _ _).mp hLe
