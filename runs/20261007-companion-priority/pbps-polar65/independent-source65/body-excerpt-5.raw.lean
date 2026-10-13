  have hNormV : ‖V0‖ ≤ (1 : ℝ) :=
    ContinuousLinearMap.opNorm_le_bound _ zero_le_one (by intro f; rw [hVnorm f,one_mul])
  have hNormAdj : ‖V0.adjoint‖ ≤ (1 : ℝ) :=
    (ContinuousLinearMap.adjoint.norm_map V0).trans_le hNormV
  refine ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,hAll,
    hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,q,hqa,hTq,hq,hCenter,hΓPq,hγ,
    ΓP0,hΓP0,hPos0,hOrder0,hUnit,Inv,hLeft,hRight,hNormInv,B0,hB0,V0,hVdef,
    hFactor,hVadj,hVnorm,?_,?_,?_⟩
  · intro g
    exact congrArg (fun C : Hperp →L[ℝ] HP0 => C g) hBAdj
  · intro g
    calc
      ‖V0.adjoint g‖ ≤ ‖V0.adjoint‖*‖g‖ := V0.adjoint.le_opNorm g
      _ ≤ 1*‖g‖ := mul_le_mul_of_nonneg_right hNormAdj (norm_nonneg _)
      _ = ‖g‖ := one_mul _
  · intro g
    have hf : V0.adjoint (V0 (V0.adjoint g))=V0.adjoint g :=
      congrArg (fun C : HP0 →L[ℝ] HP0 => C (V0.adjoint g)) hVadj
    exact (map_sub V0.adjoint g (V0 (V0.adjoint g))).trans (sub_eq_zero.mpr hf.symm)
