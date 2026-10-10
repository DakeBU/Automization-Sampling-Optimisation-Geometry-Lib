  have hFactor : B0=V0 ∘L ΓP0 := by
    apply ContinuousLinearMap.ext
    intro f
    change B0 f=B0 (Inv (ΓP0 f))
    have hf : Inv (ΓP0 f)=f := congrArg (fun C : HP0 →L[ℝ] HP0 => C f) hLeft
    rw [hf]
  have hVadj : V0.adjoint ∘L V0=(1 : HP0 →L[ℝ] HP0) :=
    (ContinuousLinearMap.norm_map_iff_adjoint_comp_self V0).mp hVnorm
