  have hAeqLocal : A=e.conjStarAlgEquiv T := hAeq
  have hAsLocal : IsSelfAdjoint A := hAs
  have hLeftLocal : Inv*ΓP0=(1 : HP0 →L[ℝ] HP0) := hLeft
  have hPosLocal : ΓP0.IsPositive := hPos0
  have hDpos : ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)+T).IsPositive := by
    refine ⟨((IsSelfAdjoint.one (Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)).add hTs).isSymmetric,?_⟩
    intro u
    change 0 ≤ inner ℝ (u+T u) u
    rw [inner_add_left,real_inner_self_eq_norm_sq]
    have hn : ‖T u‖≤‖u‖ := (hAll u).1
    have hi := (abs_le.mp (abs_real_inner_le_norm (T u) u)).1
    nlinarith only [hn,hi,norm_nonneg u]
  have hCommSquare : Commute (Γ*Γ) ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)+T) := by
    rw [hΓSq]
    show (1-T*T)*(1+T)=(1+T)*(1-T*T)
    noncomm_ring
  have hCommRootPlus := AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute.positive_square_commutation
    ν Γ (1+T) hΓ hDpos hCommSquare
  have hCommRoot : Commute Γ T := by
    have h := hCommRootPlus.eq
    simp only [mul_add,add_mul,mul_one,one_mul] at h
    exact add_left_cancel h
