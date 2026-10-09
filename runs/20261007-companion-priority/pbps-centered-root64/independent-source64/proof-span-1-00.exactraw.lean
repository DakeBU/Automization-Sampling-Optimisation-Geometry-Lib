  have hBase := MacroscopicDefectRoot.actual_unique_positive_macroscopic_defect_root
      (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  dsimp only at hBase
  rcases hBase with
    ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,
      T,hTs,hAll,hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,hEnergy,hUnique⟩
  letI : IsProbabilityMeasure μ := hμ
  letI : IsProbabilityMeasure J := hJ
  letI : IsProbabilityMeasure ν := hν
  let A : HP →L[ℝ] HP := HP.orthogonalProjectionOnto ∘L U.toContinuousLinearMap ∘L HP.subtypeL
  let B : HP →L[ℝ] Lp ℝ 2 J :=
    (((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P)*U.toContinuousLinearMap*P) ∘L HP.subtypeL
  let ΓP : HP →L[ℝ] HP := e.conjStarAlgEquiv Γ
  have hAeqLocal : A=e.conjStarAlgEquiv T := hAeq
  let q : Lp ℝ 2 ν := AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.one ν
  have hq (u : Lp ℝ 2 ν) : inner ℝ q u=∫ y,u y ∂ν :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.inner_one_eq_integral ν u
  have hqa : (q : E → ℝ)=ᵐ[ν] (fun _ => (1 : ℝ)) :=
    Lp.coeFn_const (α:=E) (μ:=ν) (p:=(2 : ℝ≥0∞)) (c:=(1 : ℝ))
  have hTq : T q=q := by
    apply ext_inner_right ℝ
    intro u
    calc
      inner ℝ (T q) u=inner ℝ q (T u) := hTs.isSymmetric q u
      _ = ∫ y,T u y ∂ν := hq _
      _ = ∫ y,u y ∂ν := (hAll u).2.2
      _ = inner ℝ q u := (hq _).symm
  have hqq : inner ℝ q q=1 := by
    rw [hq,integral_congr_ae hqa]
    simp
  have hΓEnergy (u : Lp ℝ 2 ν) : ‖Γ u‖^2=‖u‖^2-‖T u‖^2 := by
    have hs := (hEnergy (e u)).2
    have hAction : A (e u)=e (T u) := by
      have hh : A (e u)=(e.conjStarAlgEquiv T) (e u) :=
        congrArg (fun C : HP →L[ℝ] HP => C (e u)) hAeqLocal
      exact hh.trans (by simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,e.symm_apply_apply])
    change ‖(e.conjStarAlgEquiv Γ) (e u)‖^2=‖e u‖^2-‖A (e u)‖^2 at hs
    simpa only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,e.symm_apply_apply,
      hAction,e.norm_map] using hs
  have hΓq : Γ q=0 := by
    have h : ‖Γ q‖^2=0 := by rw [hΓEnergy,hTq,sub_self]
    exact norm_eq_zero.mp (by nlinarith [norm_nonneg (Γ q)])
