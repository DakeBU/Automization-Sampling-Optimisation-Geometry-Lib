  let Q : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν := 1-(innerSL ℝ q).smulRight q
  have hQ (u : Lp ℝ 2 ν) : Q u=u-inner ℝ q u • q := rfl
  have hQmean (u : Lp ℝ 2 ν) : inner ℝ q (Q u)=0 := by
    rw [hQ,inner_sub_right,inner_smul_right,hqq]
    simp
  have hDecomp (u : Lp ℝ 2 ν) : u=Q u+inner ℝ q u • q := by rw [hQ];abel
  have hQself : IsSelfAdjoint Q := by
    apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
    intro u v
    change inner ℝ (Q u) v=inner ℝ u (Q v)
    simp only [hQ,inner_sub_left,inner_sub_right,inner_smul_left,inner_smul_right,
      starRingEnd_apply,star_trivial]
    rw [real_inner_comm q u]
    ring
  have hQinner (u : Lp ℝ 2 ν) : inner ℝ (Q u) u=‖Q u‖^2 := by
    nth_rw 2 [hDecomp u]
    rw [inner_add_right,inner_smul_right,real_inner_comm q (Q u),hQmean]
    simp [real_inner_self_eq_norm_sq]
  have hQpos : Q.IsPositive := (ContinuousLinearMap.isPositive_iff' Q).mpr
    ⟨hQself,fun u => by rw [hQinner];positivity⟩
  have hQsq : Q*Q=Q := by
    apply ContinuousLinearMap.ext
    intro u
    change Q (Q u)=Q u
    rw [hQ (Q u),hQmean,zero_smul,sub_zero]
  have hΓQ (u : Lp ℝ 2 ν) : Γ (Q u)=Γ u := by rw [hQ,map_sub,map_smul,hΓq,smul_zero,sub_zero]
  have hSquare : (Γ*Γ-(γ • Q)*(γ • Q)).IsPositive := by
    apply (ContinuousLinearMap.isPositive_iff' _).mpr
    refine ⟨(by simpa only [pow_two] using (hΓ.isSelfAdjoint.pow 2).sub ((hQpos.smul_of_nonneg hγ.le).isSelfAdjoint.pow 2)),?_⟩
    intro u
    have hc := hCon (Q u) (by rw [← hq,hQmean])
    have hcSq : ‖T (Q u)‖^2 ≤ (ρ*‖Q u‖)^2 :=
      (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hρ (norm_nonneg _))).mpr hc
    have he : inner ℝ ((Γ*Γ) u) u=‖Γ u‖^2 := by
      change inner ℝ (Γ (Γ u)) u=_
      have hs : inner ℝ (Γ (Γ u)) u=inner ℝ (Γ u) (Γ u) := hΓ.inner_left_eq_inner_right (Γ u) u
      rw [hs,real_inner_self_eq_norm_sq]
    have hm : (γ • Q)*(γ • Q)=(γ*γ) • Q := by
      rw [smul_mul_smul_comm,hQsq]
    rw [ContinuousLinearMap.sub_apply,inner_sub_left,he,hm,
      ContinuousLinearMap.smul_apply,inner_smul_left,hQinner]
    rw [← hΓQ u,hΓEnergy,← pow_two γ,hγSq]
    simp only [starRingEnd_apply,star_trivial]
    nlinarith only [hcSq]
