  let Inv : HP0 →L[ℝ] HP0 := ↑(hUnit.unit⁻¹)
  have hLeft : Inv*ΓP0=1 := by
    exact (congrArg (fun C : HP0 →L[ℝ] HP0 => Inv*C) hUnit.unit_spec).symm.trans
      (Units.inv_mul hUnit.unit)
  have hRight : ΓP0*Inv=1 := by
    exact (congrArg (fun C : HP0 →L[ℝ] HP0 => C*Inv) hUnit.unit_spec).symm.trans
      (Units.mul_inv hUnit.unit)
  have hNormCoerc (f : HP0) : γ*‖f‖ ≤ ‖ΓP0 f‖ := by
    by_cases hf : f=0
    · simp [hf]
    · have hn : 0 < ‖f‖ := norm_pos_iff.mpr hf
      have h := (hCoerc f).trans (by
        calc inner ℝ (ΓP0 f) f ≤ ‖inner ℝ (ΓP0 f) f‖ := le_abs_self _
             _ ≤ ‖ΓP0 f‖*‖f‖ := norm_inner_le_norm _ _)
      nlinarith [h]
  have hNormInv : ‖Inv‖ ≤ 1/γ := by
    apply Inv.opNorm_le_bound (show 0≤1/γ from by positivity)
    intro f
    have h := hNormCoerc (Inv f)
    have hc : ΓP0 (Inv f)=f := congrArg (fun C : HP0 →L[ℝ] HP0 => C f) hRight
    rw [hc] at h
    have hh : ‖Inv f‖ ≤ ‖f‖/γ := (le_div_iff₀ hγ).mpr (by simpa only [mul_comm] using h)
    simpa only [one_div,div_eq_mul_inv,mul_comm,one_mul] using hh
