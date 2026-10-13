  letI : InnerProductSpace ℝ (Lp ℂ 2 μ) := InnerProductSpace.rclikeToReal ℂ (Lp ℂ 2 μ)
  let e : Lp ℝ 2 μ →ₗᵢ[ℝ] Lp ℂ 2 μ :=
    { toLinearMap := ι.toLinearMap, norm_map' := hNorm }
  have hInner (v w : Lp ℝ 2 μ) : RCLike.re (inner ℂ (ι v) (ι w))=inner ℝ v w := by
    rw [← real_inner_eq_re_inner]
    exact e.inner_map_map v w
  refine ⟨hB.isSymmetric.sub hA.isSymmetric,?_⟩
  intro u
  have h := hDiff.re_inner_nonneg_left (ι u)
  have hAction : (Bc-Ac) (ι u)=ι ((B-A) u) := by
    simp only [ContinuousLinearMap.sub_apply,hBi',hAi',map_sub]
  rw [hAction,hInner] at h
  exact h
