  have hCoerc (f : HP0) : γ*‖f‖^2 ≤ inner ℝ (ΓP0 f) f := by
    have h := hOrder0.inner_nonneg_left f
    simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.smul_apply,
      ContinuousLinearMap.one_apply,inner_sub_left,inner_smul_left,real_inner_self_eq_norm_sq,
      starRingEnd_apply,star_trivial] at h
    linarith
  have hUnit : IsUnit ΓP0 := by
    apply ContinuousLinearMap.isUnit_of_forall_le_norm_inner_map ΓP0 (c:=⟨γ,hγ.le⟩) hγ
    intro f
    have hnn : 0 ≤ inner ℝ (ΓP0 f) f := hPos0.inner_nonneg_left f
    rw [Real.norm_eq_abs,abs_of_nonneg hnn,mul_comm]
    exact hCoerc f
