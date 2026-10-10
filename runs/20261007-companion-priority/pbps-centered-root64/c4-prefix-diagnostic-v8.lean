import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot
import AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare
import Mathlib.Analysis.Normed.Operator.Banach

import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Order

open MeasureTheory
open scoped ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

theorem positive_square_order
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (A B : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ)
    (hA : A.IsPositive) (hB : B.IsPositive)
    (hSquareOrder : (B*B-A*A).IsPositive) :
    (B-A).IsPositive := by
  letI : NormedSpace ℝ (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) :=
    NormedSpace.restrictScalars ℝ ℂ (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  letI := IsStarNormal.instNonUnitalContinuousFunctionalCalculus
    (A := Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  letI : NonUnitalContinuousFunctionalCalculus ℂ
      (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) IsStarNormal :=
    NonUnitalClosedEmbeddingContinuousFunctionalCalculus.toNonUnitalContinuousFunctionalCalculus
  letI : NonUnitalContinuousFunctionalCalculus ℝ
      (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) IsSelfAdjoint :=
    IsSelfAdjoint.instNonUnitalContinuousFunctionalCalculus
      (A := Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  let ι : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
  let R : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.reCLM.compLpL 2 μ
  let Q : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.imCLM.compLpL 2 μ
  obtain ⟨hNorm,_,Ac,hAc,hAf,hAi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ A hA
  obtain ⟨_,_,Bc,hBc,hBf,hBi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ B hB
  obtain ⟨_,_,Dc,hDc,hDf,hDi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ (B*B-A*A) hSquareOrder
  have hAi' (u : Lp ℝ 2 μ) : Ac (ι u)=ι (A u) := hAi u
  have hBi' (u : Lp ℝ 2 μ) : Bc (ι u)=ι (B u) := hBi u
  have hComplexDiff : Bc*Bc-Ac*Ac=Dc := by
    apply ContinuousLinearMap.ext
    intro g
    change Bc (Bc g) - Ac (Ac g)=Dc g
    rw [hBf g,hAf g,map_add,map_smul,map_add,map_smul,hBi,hBi,hAi,hAi,hDf g]
    simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.mul_apply,map_sub,smul_sub]
    abel
  have hAcNonneg : 0 ≤ Ac := (ContinuousLinearMap.nonneg_iff_isPositive Ac).mpr hAc
  have hBcNonneg : 0 ≤ Bc := (ContinuousLinearMap.nonneg_iff_isPositive Bc).mpr hBc
  have hSqLe : Ac*Ac ≤ Bc*Bc := by
    apply (ContinuousLinearMap.le_def _ _).mpr
    rw [hComplexDiff]
    exact hDc
  have hLe : Ac ≤ Bc := by
    have h := CFC.sqrt_le_sqrt (Ac*Ac) (Bc*Bc) hSqLe
    have ha : CFC.sqrt (Ac*Ac)=Ac := CFC.sqrt_unique rfl hAcNonneg
    have hb : CFC.sqrt (Bc*Bc)=Bc := CFC.sqrt_unique rfl hBcNonneg
    exact ha.symm.le.trans (h.trans hb.le)
  have hDiff : (Bc-Ac).IsPositive := (ContinuousLinearMap.le_def _ _).mp hLe
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

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order

open ProbabilityTheory InnerProductSpace
open scoped ContDiff NNReal Topology
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse
open AutoSamplingTheory.ExampleCases.ProximalBPS
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

theorem actual_centered_root_order_inverse
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
              ∃ q : Lp ℝ 2 ν,
                (q : E → ℝ) =ᵐ[ν] (fun _ => (1 : ℝ)) ∧ T q = q ∧
                (∀ u : Lp ℝ 2 ν, inner ℝ q u = ∫ y, u y ∂ν) ∧
                let qP : HP := e q
                let HP0 := (innerSL ℝ qP).ker
                letI : NormedAddCommGroup HP0 := HP0.normedAddCommGroup
                letI : InnerProductSpace ℝ HP0 := HP0.innerProductSpace
                let γ : ℝ := 2*Real.sqrt ((α : ℝ)*η)/(1+(α : ℝ)*η)
                (∀ f : HP, f ∈ HP0 ↔ (∫ y, (e.symm f) y ∂ν) = 0) ∧
                ΓP qP = 0 ∧ 0 < γ ∧
                ∃ ΓP0 : HP0 →L[ℝ] HP0,
                  (∀ f : HP0, (ΓP0 f : HP) = ΓP (f : HP)) ∧
                  ΓP0.IsPositive ∧ (ΓP0-γ • (1 : HP0 →L[ℝ] HP0)).IsPositive ∧
                  IsUnit ΓP0 ∧
                  ∃ Inv : HP0 →L[ℝ] HP0,
                    Inv*ΓP0=(1 : HP0 →L[ℝ] HP0) ∧
                    ΓP0*Inv=(1 : HP0 →L[ℝ] HP0) ∧ ‖Inv‖ ≤ 1/γ := by
  classical
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
  run_tac Lean.logInfo "64_DIAGNOSTIC_BEFORE_GAUSSIAN_PRODUCER"
  have hPIBase :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare
      (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  dsimp only at hPIBase
  rcases hPIBase with ⟨_,G,_,hClose,hClosed,hGraph,hPI⟩
  run_tac Lean.logInfo "64_DIAGNOSTIC_AFTER_GAUSSIAN_BEFORE_ROUGH_PRODUCER"
  have hRoughBase := RoughMeanGradient.actual_rough_mean_gradient
    (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  dsimp only at hRoughBase
  rcases hRoughBase with ⟨_,G',_,_,_,hGraph',Tr,K,hRough⟩
  run_tac Lean.logInfo "64_DIAGNOSTIC_AFTER_ROUGH_BEFORE_GRAPH_IDENTIFICATION"
  have hSameG : G'=G := LinearPMap.eq_of_eq_graph (by
    ext p
    rcases p with ⟨u,v⟩
    exact (hGraph' u v).trans (hGraph u v).symm)
  subst G'
  run_tac Lean.logInfo "64_DIAGNOSTIC_AFTER_GRAPH_BEFORE_MEAN_IDENTIFICATION"
  have hSameT : Tr=T := by
    apply ContinuousLinearMap.ext
    intro u
    apply Lp.ext
    filter_upwards [(hRough u).2.2.1,(hAll u).2.1] with y hr ht
    exact hr.trans ((congrArg (fun m : Measure E => ∫ x,u x ∂m) (hSd y)).symm.trans ht.symm)
  subst Tr
  exact noProof64_C4_V8_DIAGNOSTIC_INTENTIONALLY_UNDEFINED

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse
