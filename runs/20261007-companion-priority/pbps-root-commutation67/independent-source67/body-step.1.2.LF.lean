  have hCommP : Commute ΓP A := by
    change ΓP*A=A*ΓP
    change (e.conjStarAlgEquiv Γ)*A=A*(e.conjStarAlgEquiv Γ)
    rw [hAeqLocal,← map_mul,← map_mul,hCommRoot.eq]
  have hAq : A qP=qP := by
    rw [hAeqLocal]
    change e (T (e.symm (e q)))=e q
    rw [e.symm_apply_apply,hTq]
  have hAPreserves (u : HP0) : A (u : HP) ∈ HP0 := by
    change inner ℝ qP (A (u : HP))=0
    calc
      inner ℝ qP (A (u : HP))=inner ℝ (A qP) (u : HP) :=
        (hAsLocal.isSymmetric qP (u : HP)).symm
      _ = inner ℝ qP (u : HP) := by rw [hAq]
      _ = 0 := u.property
  let A0 : HP0 →L[ℝ] HP0 := (A.comp HP0.subtypeL).codRestrict HP0 hAPreserves
  have hA0 (u : HP0) : (A0 u : HP)=A (u : HP) := rfl
  have hA0self : IsSelfAdjoint A0 := by
    apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
    intro u v
    exact hAsLocal.isSymmetric (u : HP) (v : HP)
