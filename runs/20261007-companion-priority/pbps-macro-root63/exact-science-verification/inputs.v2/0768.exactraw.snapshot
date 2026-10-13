import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator
import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRange
import AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionL2
import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRoot
import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
set_option autoImplicit false
set_option maxHeartbeats 3200000
set_option diagnostics false

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot
noncomputable section

theorem actual_unique_positive_macroscopic_defect_root
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
    let F := fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2)
    let mY := MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)
    letI : MeasurableSpace (E × E) := Prod.instMeasurableSpace
    letI : Fact (mY ≤ (inferInstance : MeasurableSpace (E × E))) :=
      ⟨measurable_snd.comap_le⟩
    let HP := lpMeas ℝ ℝ mY 2 J
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      HP.subtypeL ∘L condExpL2 ℝ ℝ (μ := J) measurable_snd.comap_le
    let hp : MeasurePreserving (Prod.snd : E × E → E) J ν := ⟨measurable_snd,rfl⟩
    let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    HP = P.toLinearMap.range ∧
    (∀ f : HP, P (f : Lp ℝ 2 J) = f) ∧
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν ∧
      ∃ e : Lp ℝ 2 ν ≃ₗᵢ[ℝ] HP,
        (∀ u : Lp ℝ 2 ν, (e u : Lp ℝ 2 J) = M u) ∧
        ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
          (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F) ∧
          Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap ∧
          ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
            IsSelfAdjoint T ∧
            (∀ u : Lp ℝ 2 ν,
              ‖T u‖ ≤ ‖u‖ ∧
              (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
              (∫ y, T u y ∂ν) = ∫ y, u y ∂ν) ∧
            let A : HP →L[ℝ] HP :=
              HP.orthogonalProjectionOnto ∘L U.toContinuousLinearMap ∘L HP.subtypeL
            let B : HP →L[ℝ] Lp ℝ 2 J :=
              (((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P)*U.toContinuousLinearMap*P) ∘L HP.subtypeL
            A = e.conjStarAlgEquiv T ∧ IsSelfAdjoint A ∧
            (∀ f : HP, ‖A f‖ ≤ ‖f‖) ∧
            (∀ f : HP, P (B f) = 0) ∧
            ∃ Γ : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
              Γ.IsPositive ∧ Γ*Γ=(1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T ∧
              let ΓP : HP →L[ℝ] HP := e.conjStarAlgEquiv Γ
              ΓP.IsPositive ∧ ΓP*ΓP=(1 : HP →L[ℝ] HP)-A*A ∧
              B.adjoint ∘L B = ΓP*ΓP ∧
              (∀ f : HP, ‖B f‖ = ‖ΓP f‖ ∧
                ‖ΓP f‖^2 = ‖f‖^2-‖A f‖^2) ∧
              (∀ G : HP →L[ℝ] HP,
                G.IsPositive → G*G=(1 : HP →L[ℝ] HP)-A*A → G=ΓP)
:= by
  classical
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let mY : MeasurableSpace (E × E) := MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)
  letI : MeasurableSpace (E × E) := Prod.instMeasurableSpace
  letI : Fact (mY ≤ (inferInstance : MeasurableSpace (E × E))) :=
    ⟨measurable_snd.comap_le⟩
  let HP := lpMeas ℝ ℝ mY 2 J
  letI : NormedAddCommGroup HP := HP.normedAddCommGroup
  letI : InnerProductSpace ℝ HP := HP.innerProductSpace
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    HP.subtypeL ∘L condExpL2 ℝ ℝ (μ := J) measurable_snd.comap_le
  let hp : MeasurePreserving (Prod.snd : E × E → E) J ν := ⟨measurable_snd,rfl⟩
  let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
  rcases CenteredDefectOperator.actual_centered_selfadjoint_defect hα hαβ hV hH hη hβη with
    ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M0,hM0,T,hTs,hAll,
      q,hqa,hTq,hqi,hzero,hD,hDq,hDef,hRest⟩
  letI : IsProbabilityMeasure μ := hμ
  letI : IsProbabilityMeasure J := hJ
  letI : IsProbabilityMeasure ν := hν
  have hM0eq : M0 = M := by
    apply LinearIsometry.ext
    intro u
    apply Lp.ext
    exact (hM0 u).trans (Lp.coeFn_compMeasurePreserving u hp).symm
  subst M0
  have hPdef : P = HP.starProjection := rfl
  have hPrange : P.toLinearMap.range = HP := by
    change P.range = HP
    rw [hPdef]
    exact HP.range_starProjection
  have hMR : M.toLinearMap.range = P.toLinearMap.range :=
    (MacroscopicRange.actual_macroscopic_centered_range hα hαβ hV hH hη hβη).2.2.1
  let e : Lp ℝ 2 ν ≃ₗᵢ[ℝ] HP :=
    M.equivRange.trans (LinearIsometryEquiv.ofEq _ _ (hMR.trans hPrange))
  have he (u : Lp ℝ 2 ν) : (e u : Lp ℝ 2 J) = M u := rfl
  have hPf (f : HP) : P (f : Lp ℝ 2 J) = f := by
    rw [hPdef]
    exact HP.starProjection_mem_subspace_eq_self f
  have hPP : P*P=P := by rw [hPdef];exact HP.isIdempotentElem_starProjection
  have hPid (f : Lp ℝ 2 J) : P (P f)=P f := by
    change (P*P) f=P f
    rw [hPP]
  let A : HP →L[ℝ] HP :=
    HP.orthogonalProjectionOnto ∘L U.toContinuousLinearMap ∘L HP.subtypeL
  let B0 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    ((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P)*U.toContinuousLinearMap*P
  let AJ := P*U.toContinuousLinearMap*P
  let B : HP →L[ℝ] Lp ℝ 2 J := B0 ∘L HP.subtypeL
  have hAincl (f : HP) : (A f : Lp ℝ 2 J) = AJ f := by
    change P (U f) = P (U (P f))
    rw [hPf]
  have hAeq : A=e.conjStarAlgEquiv T := by
    apply ContinuousLinearMap.ext
    intro f
    apply Subtype.ext
    change (A f : Lp ℝ 2 J) = (e (T (e.symm f)) : Lp ℝ 2 J)
    rw [hAincl,he]
    have hf : M (e.symm f) = (f : Lp ℝ 2 J) := by
      rw [← he,e.apply_symm_apply]
    rw [← hf]
    exact ((hAll (e.symm f)).2.1).symm
  have hAapply (f : HP) : A f=e (T (e.symm f)) := by rw [hAeq];rfl
  have hAs : IsSelfAdjoint A := by
    rw [hAeq]
    simpa only [LinearIsometryEquiv.conjStarAlgEquiv_apply,e.adjoint_eq_symm] using
      hTs.conj_adjoint (e : Lp ℝ 2 ν →L[ℝ] HP)
  have hAn (f : HP) : ‖A f‖ ≤ ‖f‖ := by
    rw [hAapply,e.norm_map]
    exact ((hAll (e.symm f)).2.2.1).trans_eq (e.symm.norm_map f)
  have hPB (f : HP) : P (B f)=0 := by
    change P (U (P f)-P (U (P f)))=0
    rw [map_sub,hPid,sub_self]
  obtain ⟨R,hR,hRf,U2,hU2,hU2i,hU2s,hRp,hBB,hBD,hBE⟩ :=
    ReflectionL2.actual_reflection_block_identities μ hη
  have hU2eq : U2=U := by
    apply LinearIsometry.ext
    intro f
    apply Lp.ext
    exact (hU2 f).trans (hU f).symm
  subst U2
  have hB0Gram : B0.adjoint ∘L B0=P-AJ*AJ := by
    have hBBtyped : B0.adjoint ∘L B0 = P-AJ^2 := hBB
    simpa only [pow_two] using hBBtyped
  obtain ⟨Γ,hΓ,hΓSq,hEnergy⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRoot.exists_positive_real_square_root
      ν ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) hD
  let ΓP : HP →L[ℝ] HP := e.conjStarAlgEquiv Γ
  have hΓP : ΓP.IsPositive := by
    simpa only [ΓP,LinearIsometryEquiv.conjStarAlgEquiv_apply,e.adjoint_eq_symm] using
      hΓ.conj_adjoint (e : Lp ℝ 2 ν →L[ℝ] HP)
  have hΓPSq : ΓP*ΓP=(1 : HP →L[ℝ] HP)-A*A := by
    change e.conjStarAlgEquiv Γ*e.conjStarAlgEquiv Γ=_
    rw [← map_mul,hΓSq,map_sub,map_one,map_mul,← hAeq]
  have hGram : B.adjoint ∘L B=ΓP*ΓP := by
    calc
      B.adjoint ∘L B = HP.subtypeL.adjoint ∘L (B0.adjoint ∘L B0) ∘L HP.subtypeL := by
        simp only [B,ContinuousLinearMap.adjoint_comp,ContinuousLinearMap.comp_assoc]
      _ = HP.subtypeL.adjoint ∘L (P-AJ*AJ) ∘L HP.subtypeL := by rw [hB0Gram]
      _ = (1 : HP →L[ℝ] HP)-A*A := by
        apply ContinuousLinearMap.ext
        intro f
        rw [HP.adjoint_subtypeL]
        change HP.orthogonalProjectionOnto (P f-AJ (AJ f))=f-A (A f)
        rw [hPf,← hAincl f,← hAincl (A f),map_sub]
        simp only [Submodule.orthogonalProjectionOnto_mem_subspace_eq_self]
      _ = ΓP*ΓP := hΓPSq.symm
  have hMacroEnergy (f : HP) : ‖ΓP f‖^2=‖f‖^2-‖A f‖^2 := by
    have hs : ‖Γ (e.symm f)‖^2=‖e.symm f‖^2-‖T (e.symm f)‖^2 :=
      (hEnergy (e.symm f)).trans (hDef (e.symm f))
    simpa only [ΓP,LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,hAapply,
      e.norm_map,e.symm.norm_map] using hs
  have hNorm (f : HP) : ‖B f‖=‖ΓP f‖ := by
    have hb := B.apply_norm_sq_eq_inner_adjoint_right f
    have hg := ΓP.apply_norm_sq_eq_inner_adjoint_right f
    rw [hGram] at hb
    rw [hΓP.isSelfAdjoint.adjoint_eq] at hg
    exact (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp (hb.trans hg.symm)
  have hUnique (G : HP →L[ℝ] HP) (hG : G.IsPositive)
      (hGSq : G*G=(1 : HP →L[ℝ] HP)-A*A) : G=ΓP := by
    let G0 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν := e.symm.conjStarAlgEquiv G
    have hG0 : G0.IsPositive := by
      simpa only [G0,LinearIsometryEquiv.conjStarAlgEquiv_apply,e.symm.adjoint_eq_symm] using
        hG.conj_adjoint (e.symm : HP →L[ℝ] Lp ℝ 2 ν)
    have hPullA : e.symm.conjStarAlgEquiv A=T := by
      rw [hAeq]
      apply ContinuousLinearMap.ext
      intro u
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
        LinearIsometryEquiv.symm_symm,e.symm_apply_apply,e.apply_symm_apply]
    have hG0Sq : G0*G0=(1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T := by
      change e.symm.conjStarAlgEquiv G*e.symm.conjStarAlgEquiv G=_
      rw [← map_mul,hGSq,map_sub,map_one,map_mul,hPullA]
    have hEq : G0=Γ :=
      AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique.positive_square_roots_unique
        ν G0 Γ hG0 hΓ (hG0Sq.trans hΓSq.symm)
    calc
      G=e.conjStarAlgEquiv G0 := by
        apply ContinuousLinearMap.ext
        intro f
        simp only [G0,LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
          LinearIsometryEquiv.symm_symm,e.symm_apply_apply,e.apply_symm_apply]
      _ = e.conjStarAlgEquiv Γ := congrArg e.conjStarAlgEquiv hEq
      _ = ΓP := rfl
  refine ⟨hμ,hJ,hν,hPrange.symm,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,
    T,hTs,?_,hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,?_,hUnique⟩
  · intro u
    exact (hAll u).2.2
  · intro f
    exact ⟨hNorm f,hMacroEnergy f⟩

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot.actual_unique_positive_macroscopic_defect_root

namespace Tests.ProximalBPSMacroscopicDefectRoot

theorem genuine_actual_macroscopic_root_consumer
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
    let F := fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2)
    let mY := MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)
    letI : MeasurableSpace (E × E) := Prod.instMeasurableSpace
    letI : Fact (mY ≤ (inferInstance : MeasurableSpace (E × E))) :=
      ⟨measurable_snd.comap_le⟩
    let HP := lpMeas ℝ ℝ mY 2 J
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      HP.subtypeL ∘L condExpL2 ℝ ℝ (μ := J) measurable_snd.comap_le
    let hp : MeasurePreserving (Prod.snd : E × E → E) J ν := ⟨measurable_snd,rfl⟩
    let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    HP = P.toLinearMap.range ∧
    (∀ f : HP, P (f : Lp ℝ 2 J) = f) ∧
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν ∧
      ∃ e : Lp ℝ 2 ν ≃ₗᵢ[ℝ] HP,
        (∀ u : Lp ℝ 2 ν, (e u : Lp ℝ 2 J) = M u) ∧
        ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
          (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F) ∧
          Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap ∧
          ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
            IsSelfAdjoint T ∧
            (∀ u : Lp ℝ 2 ν,
              ‖T u‖ ≤ ‖u‖ ∧
              (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
              (∫ y, T u y ∂ν) = ∫ y, u y ∂ν) ∧
            let A : HP →L[ℝ] HP :=
              HP.orthogonalProjectionOnto ∘L U.toContinuousLinearMap ∘L HP.subtypeL
            let B : HP →L[ℝ] Lp ℝ 2 J :=
              (((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P)*U.toContinuousLinearMap*P) ∘L HP.subtypeL
            A = e.conjStarAlgEquiv T ∧ IsSelfAdjoint A ∧
            (∀ f : HP, ‖A f‖ ≤ ‖f‖) ∧
            (∀ f : HP, P (B f) = 0) ∧
            ∃ Γ : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
              Γ.IsPositive ∧ Γ*Γ=(1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T ∧
              let ΓP : HP →L[ℝ] HP := e.conjStarAlgEquiv Γ
              ΓP.IsPositive ∧ ΓP*ΓP=(1 : HP →L[ℝ] HP)-A*A ∧
              B.adjoint ∘L B = ΓP*ΓP ∧
              (∀ f : HP, ‖B f‖ = ‖ΓP f‖ ∧
                ‖ΓP f‖^2 = ‖f‖^2-‖A f‖^2 ∧ ‖ΓP f‖ ≤ ‖f‖) ∧
              (∀ G : HP →L[ℝ] HP,
                G.IsPositive → G*G=(1 : HP →L[ℝ] HP)-A*A → G=ΓP) := by
  classical
  dsimp only
  obtain ⟨hμ,hJ,hν,hHP,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,
    hT,hA,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,hEnergy,hUnique⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot.actual_unique_positive_macroscopic_defect_root
      hα hαβ hV hH hη hβη
  refine ⟨hμ,hJ,hν,hHP,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,
    hT,hA,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,?_,hUnique⟩
  intro f
  have hf := hEnergy f
  refine ⟨hf.1,hf.2,?_⟩
  have hnonneg : 0 ≤ ‖f‖^2 - ‖(e.conjStarAlgEquiv Γ) f‖^2 := by
    rw [hf.2]
    simp only [sub_sub_cancel]
    positivity
  nlinarith [norm_nonneg ((e.conjStarAlgEquiv Γ) f),norm_nonneg f]

end Tests.ProximalBPSMacroscopicDefectRoot

#print axioms Tests.ProximalBPSMacroscopicDefectRoot.genuine_actual_macroscopic_root_consumer
