  let qP : HP := e q
  let HP0 := (innerSL ℝ qP).ker
  letI : NormedAddCommGroup HP0 := HP0.normedAddCommGroup
  letI : InnerProductSpace ℝ HP0 := HP0.innerProductSpace
  have hCenter (f : HP) : f ∈ HP0 ↔ (∫ y,(e.symm f) y ∂ν)=0 := by
    change inner ℝ (e q) f=0 ↔ _
    rw [← e.apply_symm_apply f, e.inner_map_map,hq,e.symm_apply_apply]
  have hΓPq : ΓP qP=0 := by
    change e (Γ (e.symm (e q)))=0
    rw [e.symm_apply_apply,hΓq,map_zero]
  have hInv (f : HP0) : ΓP (f : HP) ∈ HP0 := by
    change inner ℝ qP (ΓP (f : HP))=0
    have hs : inner ℝ qP (ΓP (f : HP))=inner ℝ (ΓP qP) (f : HP) :=
      (hΓP.inner_left_eq_inner_right qP (f : HP)).symm
    rw [hs,hΓPq,inner_zero_left]
  let ΓP0 : HP0 →L[ℝ] HP0 := (ΓP.comp HP0.subtypeL).codRestrict HP0 hInv
  have hΓP0 (f : HP0) : (ΓP0 f : HP)=ΓP (f : HP) := rfl
  have hPos0 : ΓP0.IsPositive := by
    refine ⟨?_,?_⟩
    · intro f g
      exact hΓP.isSymmetric (f : HP) (g : HP)
    · intro f
      exact hΓP.re_inner_nonneg_left (f : HP)
  have hOrder0 : (ΓP0-γ • (1 : HP0 →L[ℝ] HP0)).IsPositive := by
    apply (ContinuousLinearMap.isPositive_iff' _).mpr
    refine ⟨hPos0.isSelfAdjoint.sub ((ContinuousLinearMap.isPositive_one).smul_of_nonneg hγ.le).isSelfAdjoint,?_⟩
    intro f
    let u : Lp ℝ 2 ν := e.symm (f : HP)
    have hu : inner ℝ q u=0 := by rw [hq];exact (hCenter _).mp f.property
    have hQu : Q u=u := by rw [hQ,hu,zero_smul,sub_zero]
    have h := hOrder.inner_nonneg_left u
    simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.smul_apply,
      ContinuousLinearMap.one_apply,inner_sub_left,inner_smul_left,hQu] at h ⊢
    have hInner : inner ℝ (ΓP0 f) f=inner ℝ (Γ u) u := by
      change inner ℝ (ΓP (f : HP)) (f : HP)=_
      change inner ℝ (e (Γ u)) (f : HP)=_
      rw [← e.apply_symm_apply (f : HP),e.inner_map_map]
    rw [hInner]
    have hNorm : inner ℝ f f=inner ℝ u u := by
      change inner ℝ (f : HP) (f : HP)=_
      rw [← e.apply_symm_apply (f : HP),e.inner_map_map]
    rw [hNorm]
    exact h
