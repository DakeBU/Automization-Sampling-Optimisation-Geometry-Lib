  let V0 : HP0 →L[ℝ] Hperp := B0 ∘L Inv
  have hGramLocal : B.adjoint ∘L B=ΓP*ΓP := hGram
  have hPosLocal : ΓP.IsPositive := hΓP
  have hVnorm (f : HP0) : ‖V0 f‖=‖f‖ := by
    let g : HP0 := Inv f
    have hg : ΓP0 g=f := congrArg (fun C : HP0 →L[ℝ] HP0 => C f) hRight
    have hb := B.apply_norm_sq_eq_inner_adjoint_right (g : HP)
    have hr := ΓP.apply_norm_sq_eq_inner_adjoint_right (g : HP)
    rw [hGramLocal] at hb
    rw [hPosLocal.isSelfAdjoint.adjoint_eq] at hr
    have hNorm : ‖B (g : HP)‖=‖ΓP (g : HP)‖ :=
      (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp (hb.trans hr.symm)
    calc
      ‖V0 f‖=‖B (g : HP)‖ := rfl
      _ = ‖ΓP (g : HP)‖ := hNorm
      _ = ‖ΓP0 g‖ := congrArg (fun z : HP => ‖z‖) (hΓP0 g).symm
      _ = ‖f‖ := congrArg (fun z : HP0 => ‖z‖) hg
