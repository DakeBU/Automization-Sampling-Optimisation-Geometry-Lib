  have hPosLocal : ΓP0.IsPositive := hPos0
  have hBAdj : B0.adjoint=ΓP0 ∘L V0.adjoint := by
    calc
      B0.adjoint = (V0 ∘L ΓP0).adjoint :=
        congrArg (fun D : HP0 →L[ℝ] Hperp => D.adjoint) hFactor
      _ = ΓP0.adjoint ∘L V0.adjoint := ContinuousLinearMap.adjoint_comp V0 ΓP0
      _ = ΓP0 ∘L V0.adjoint :=
        congrArg (fun D : HP0 →L[ℝ] HP0 => D ∘L V0.adjoint)
          hPosLocal.isSelfAdjoint.adjoint_eq
  have hNormV : ‖V0‖ ≤ (1 : ℝ) :=
    ContinuousLinearMap.opNorm_le_bound _ zero_le_one (by intro u; rw [hVnorm u,one_mul])
  have hNormAdj : ‖V0.adjoint‖ ≤ (1 : ℝ) :=
    (ContinuousLinearMap.adjoint.norm_map V0).trans_le hNormV
  have hVcontract (g : Hperp) : ‖V0.adjoint g‖≤‖g‖ := by
    calc
      ‖V0.adjoint g‖ ≤ ‖V0.adjoint‖*‖g‖ := V0.adjoint.le_opNorm g
      _ ≤ 1*‖g‖ := mul_le_mul_of_nonneg_right hNormAdj (norm_nonneg _)
      _ = ‖g‖ := one_mul _
