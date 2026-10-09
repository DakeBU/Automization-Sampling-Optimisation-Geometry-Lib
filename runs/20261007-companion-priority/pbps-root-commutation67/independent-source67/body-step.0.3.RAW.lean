  let e : Lp ℝ 2 μ →ₗᵢ[ℝ] Lp ℂ 2 μ :=
    { toLinearMap := ι.toLinearMap, norm_map' := hNorm }
  apply ContinuousLinearMap.ext
  intro u
  apply e.injective
  change ι (G (D u))=ι (D (G u))
  rw [← hGi (D u), ← hDi u, ← hDi (G u), ← hGi u]
  exact congrArg (fun A : Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ => A (ι u)) hLift.eq
