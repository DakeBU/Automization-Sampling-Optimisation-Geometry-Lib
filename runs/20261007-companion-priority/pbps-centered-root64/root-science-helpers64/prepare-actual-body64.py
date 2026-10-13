from pathlib import Path
r=Path('runs/20261007-companion-priority/pbps-centered-root64')
body='''  classical
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let mY : MeasurableSpace (E × E) := MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)
  letI : MeasurableSpace (E × E) := Prod.instMeasurableSpace
  letI : Fact (mY ≤ (inferInstance : MeasurableSpace (E × E))) := ⟨measurable_snd.comap_le⟩
  let HP := lpMeas ℝ ℝ mY 2 J
  letI : NormedAddCommGroup HP := HP.normedAddCommGroup
  letI : InnerProductSpace ℝ HP := HP.innerProductSpace
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    HP.subtypeL ∘L condExpL2 ℝ ℝ (μ := J) measurable_snd.comap_le
  rcases MacroscopicDefectRoot.actual_unique_positive_macroscopic_defect_root
      hα hαβ hV hH hη hβη with
    ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,
      T,hTs,hAll,hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,hEnergy,hUnique⟩
  letI : IsProbabilityMeasure μ := hμ
  letI : IsProbabilityMeasure J := hJ
  letI : IsProbabilityMeasure ν := hν
  let A : HP →L[ℝ] HP := HP.orthogonalProjectionOnto ∘L U.toContinuousLinearMap ∘L HP.subtypeL
  let B : HP →L[ℝ] Lp ℝ 2 J :=
    (((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P)*U.toContinuousLinearMap*P) ∘L HP.subtypeL
  let ΓP : HP →L[ℝ] HP := e.conjStarAlgEquiv Γ
  let q : Lp ℝ 2 ν := AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.one ν
  have hq (u : Lp ℝ 2 ν) : inner ℝ q u=∫ y,u y ∂ν :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.inner_one_eq_integral ν u
  have hqa : (q : E → ℝ)=ᵐ[ν] (fun _ => (1 : ℝ)) :=
    Lp.coeFn_const (α:=E) (μ:=ν) (p:=(2 : ℝ≥0∞)) (c:=(1 : ℝ))
  have hTq : T q=q := by
    apply ext_inner_right ℝ
    intro u
    rw [hTs.isSymmetric,hq,hq,(hAll u).2.2]
  have hqq : inner ℝ q q=1 := by
    rw [hq,integral_congr_ae hqa]
    simp
  have hΓEnergy (u : Lp ℝ 2 ν) : ‖Γ u‖^2=‖u‖^2-‖T u‖^2 := by
    have h := Γ.apply_norm_sq_eq_inner_adjoint_right u
    rw [hΓ.isSelfAdjoint.adjoint_eq,hΓSq] at h
    simpa only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.one_apply,
      ContinuousLinearMap.mul_apply,inner_sub_left,hTs.isSymmetric,
      real_inner_self_eq_norm_sq] using h
  have hΓq : Γ q=0 := by
    have h : ‖Γ q‖^2=0 := by rw [hΓEnergy,hTq,sub_self]
    exact norm_eq_zero.mp (by nlinarith [norm_nonneg (Γ q)])
  obtain ⟨_,G,_,hClose,hClosed,hGraph,hPI⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare
      hα hαβ hV hH hη hβη
  obtain ⟨_,G',_,_,_,hGraph',Tr,K,hRough⟩ :=
    RoughMeanGradient.actual_rough_mean_gradient hα hαβ hV hH hη hβη
  have hSameG : G'=G := LinearPMap.eq_of_eq_graph (by
    ext p
    rcases p with ⟨u,v⟩
    exact (hGraph' u v).trans (hGraph u v).symm)
  subst G'
  have hSameT : Tr=T := by
    apply ContinuousLinearMap.ext
    intro u
    apply Lp.ext
    filter_upwards [(hRough u).2.2.1,(hAll u).2.1] with y hr ht
    exact hr.trans ((congrArg (fun m : Measure E => ∫ x,u x ∂m) (hSd y)).symm.trans ht.symm)
  subst Tr
  have ha0 : 0 < (α : ℝ)*η := mul_pos hα hη
  have ha1 : (α : ℝ)*η ≤ 1 :=
    (mul_le_mul_of_nonneg_right (by exact_mod_cast hαβ) hη.le).trans hβη
  have hd : 0 < 1+(α : ℝ)*η := by positivity
  let ρ : ℝ := (1-(α : ℝ)*η)/(1+(α : ℝ)*η)
  let γ : ℝ := 2*Real.sqrt ((α : ℝ)*η)/(1+(α : ℝ)*η)
  have hρ : 0 ≤ ρ := div_nonneg (sub_nonneg.mpr ha1) hd.le
  have hγ : 0 < γ := by dsimp [γ]; positivity
  have hγSq : γ^2=1-ρ^2 := by
    dsimp [γ,ρ]
    rw [div_pow,mul_pow,Real.sq_sqrt ha0.le]
    field_simp [ne_of_gt hd]
    ring
  have hCon (u : Lp ℝ 2 ν) (hu : (∫ y,u y ∂ν)=0) : ‖T u‖ ≤ ρ*‖u‖ := by
    obtain ⟨hPair,_,_,_,hSharp,_⟩ := hRough u
    let z : G.closure.domain := ⟨T u,G.closure.mem_domain_of_mem_graph hPair⟩
    have hz : (∫ x,(z : Lp ℝ 2 ν) x ∂ν)=0 := (hAll u).2.2.trans hu
    have hK : G.closure z=K u := G.closure.mem_graph_snd_inj (G.closure.mem_graph z) hPair rfl
    have hC3 := hPI z hz
    change ((α : ℝ)/(1+(α : ℝ)*η))*‖T u‖^2 ≤ ‖G.closure z‖^2 at hC3
    rw [hK] at hC3
    have hP : (α : ℝ)*‖T u‖^2 ≤ (1+(α : ℝ)*η)*‖K u‖^2 := by
      calc
        _ ≤ ‖K u‖^2*(1+(α : ℝ)*η) :=
          (div_le_iff₀ hd).mp (by simpa only [div_mul_eq_mul_div] using hC3)
        _ = _ := mul_comm _ _
    have hs : η*‖K u‖^2 ≤
        ((1-(α : ℝ)*η)^2*(‖u‖^2-‖T u‖^2))/(4*(1+(α : ℝ)*η)) := by
      simpa only [div_mul_eq_mul_div] using hSharp
    have hs' := (le_div_iff₀ (show 0<4*(1+(α : ℝ)*η) from by positivity)).mp hs
    have hSharp' : 4*(1+(α : ℝ)*η)*η*‖K u‖^2 ≤
        (1-(α : ℝ)*η)^2*(‖u‖^2-‖T u‖^2) := by nlinarith [hs']
    have hSq : (1+(α : ℝ)*η)^2*‖T u‖^2 ≤ (1-(α : ℝ)*η)^2*‖u‖^2 := by
      nlinarith [mul_le_mul_of_nonneg_left hP (show 0≤4*η from by positivity)]
    have hSq' : ‖T u‖^2 ≤ (ρ*‖u‖)^2 := by
      dsimp [ρ]
      rw [mul_pow,div_pow,div_mul_eq_mul_div]
      apply (le_div_iff₀ (sq_pos_of_pos hd)).2
      nlinarith [hSq]
    exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hρ (norm_nonneg _))).mp hSq'
  let Q : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν := 1-(innerSL ℝ q).smulRight q
  have hQ (u : Lp ℝ 2 ν) : Q u=u-inner ℝ q u • q := rfl
  have hQmean (u : Lp ℝ 2 ν) : inner ℝ q (Q u)=0 := by
    rw [hQ,inner_sub_right,inner_smul_right,hqq]
    simp
  have hDecomp (u : Lp ℝ 2 ν) : u=Q u+inner ℝ q u • q := by rw [hQ];abel
  have hQself : IsSelfAdjoint Q := by
    apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
    intro u v
    simp only [hQ,inner_sub_left,inner_sub_right,inner_smul_left,inner_smul_right]
    rw [real_inner_comm v q]
    ring
  have hQinner (u : Lp ℝ 2 ν) : inner ℝ (Q u) u=‖Q u‖^2 := by
    nth_rw 2 [hDecomp u]
    rw [inner_add_right,inner_smul_right,real_inner_comm (Q u) q,hQmean]
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
      rw [hΓ.inner_left_eq_inner_right,real_inner_self_eq_norm_sq]
    have hm : (γ • Q)*(γ • Q)=(γ*γ) • Q := by
      rw [smul_mul_smul_comm,hQsq]
    rw [ContinuousLinearMap.sub_apply,inner_sub_left,he,hm,
      ContinuousLinearMap.smul_apply,inner_smul_left,hQinner]
    rw [← hΓQ u,hΓEnergy,hγSq,← pow_two]
    nlinarith [hcSq]
  have hOrder : (Γ-γ • Q).IsPositive :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order
      ν (γ • Q) Γ (hQpos.smul_of_nonneg hγ.le) hΓ hSquare
  let qP : HP := e q
  let HP0 := (innerSL ℝ qP).ker
  letI : NormedAddCommGroup HP0 := HP0.normedAddCommGroup
  letI : InnerProductSpace ℝ HP0 := HP0.innerProductSpace
  have hCenter (f : HP) : f ∈ HP0 ↔ (∫ y,(e.symm f) y ∂ν)=0 := by
    change inner ℝ (e q) f=0 ↔ _
    rw [← e.apply_symm_apply f, e.inner_map_map,hq]
  have hΓPq : ΓP qP=0 := by
    change e (Γ (e.symm (e q)))=0
    rw [e.symm_apply_apply,hΓq,map_zero]
  have hInv (f : HP0) : ΓP (f : HP) ∈ HP0 := by
    change inner ℝ qP (ΓP (f : HP))=0
    rw [← hΓP.inner_left_eq_inner_right,hΓPq,inner_zero_left]
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
  have hCoerc (f : HP0) : γ*‖f‖^2 ≤ inner ℝ (ΓP0 f) f := by
    have h := hOrder0.inner_nonneg_left f
    simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.smul_apply,
      ContinuousLinearMap.one_apply,inner_sub_left,inner_smul_left,real_inner_self_eq_norm_sq] at h
    linarith
  have hUnit : IsUnit ΓP0 := by
    apply ContinuousLinearMap.isUnit_of_forall_le_norm_inner_map ΓP0 (c:=⟨γ,hγ.le⟩) hγ
    intro f
    have hnn : 0 ≤ inner ℝ (ΓP0 f) f := hPos0.inner_nonneg_left f
    rw [Real.norm_eq_abs,abs_of_nonneg hnn,mul_comm]
    exact hCoerc f
  let Inv : HP0 →L[ℝ] HP0 := ↑(hUnit.unit⁻¹)
  have hLeft : Inv*ΓP0=1 := by
    change ↑(hUnit.unit⁻¹)*ΓP0=1
    rw [← hUnit.unit_spec]
    exact Units.inv_mul hUnit.unit
  have hRight : ΓP0*Inv=1 := by
    change ΓP0*↑(hUnit.unit⁻¹)=1
    rw [← hUnit.unit_spec]
    exact Units.mul_inv hUnit.unit
  have hNormCoerc (f : HP0) : γ*‖f‖ ≤ ‖ΓP0 f‖ := by
    by_cases hf : f=0
    · simp [hf]
    · have hn : 0 < ‖f‖ := norm_pos_iff.mpr hf
      have h := (hCoerc f).trans (by
        calc inner ℝ (ΓP0 f) f ≤ ‖inner ℝ (ΓP0 f) f‖ := le_abs_self _
             _ ≤ ‖ΓP0 f‖*‖f‖ := norm_inner_le_norm _ _)
      nlinarith [h]
  have hNormInv : ‖Inv‖ ≤ 1/γ := by
    apply ContinuousLinearMap.opNorm_le_bound (by positivity)
    intro f
    have h := hNormCoerc (Inv f)
    have hc : ΓP0 (Inv f)=f := congrArg (fun C : HP0 →L[ℝ] HP0 => C f) hRight
    rw [hc] at h
    have hh : ‖Inv f‖ ≤ ‖f‖/γ := (le_div_iff₀ hγ).mpr (by simpa only [mul_comm] using h)
    simpa only [one_div,div_eq_mul_inv,mul_comm] using hh
  exact ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,hAll,
    hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,q,hqa,hTq,hq,hCenter,hΓPq,hγ,
    ΓP0,hΓP0,hPos0,hOrder0,hUnit,Inv,hLeft,hRight,hNormInv⟩
'''
p=r/'actual-body-v1.txt';assert not p.exists();p.write_text(body,encoding='utf-8',newline='\n')
print('Authored complete actual64 proof-body candidate: internal C4 actual-gradient/Poincare join; constant projection; same-root B15; centered inverse. Uncompiled, no public premise change or production Test import.')
