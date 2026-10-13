from pathlib import Path
pre=Path('runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67');old=Path('Tests/ProximalBPSAmbientAdjointCorrector.lean').read_text();mainold=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean').read_text();prefix=old[old.index('  classical\n'):old.index('  have hRself')]
# Canonical original-input setup and exact same parent witnesses, not new assumptions.
prefix=prefix.replace('  dsimp only\n','  unfold actual_same_root_inverse_commutation_statement\n  dsimp only\n',1)
math='''  have hDpos : ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)+T).IsPositive := by
    refine ⟨((isSelfAdjoint_one : IsSelfAdjoint (1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)).add hTs).isSymmetric,?_⟩
    intro u
    simp only [ContinuousLinearMap.add_apply,ContinuousLinearMap.one_apply,
      inner_add_left,real_inner_self_eq_norm_sq,RCLike.re_to_real]
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
  have hCommP : Commute ΓP A := by
    change ΓP*A=A*ΓP
    change (e.conjStarAlgEquiv Γ)*A=A*(e.conjStarAlgEquiv Γ)
    rw [hAeq,← map_mul,← map_mul,hCommRoot.eq]
  have hAq : A qP=qP := by
    rw [hAeq]
    change e (T (e.symm (e q)))=e q
    rw [e.symm_apply_apply,hTq]
  have hAPreserves (u : HP0) : A (u : HP) ∈ HP0 := by
    change inner ℝ qP (A (u : HP))=0
    rw [← hAs.isSymmetric,hAq]
    exact u.property
  let A0 : HP0 →L[ℝ] HP0 := (A.comp HP0.subtypeL).codRestrict HP0 hAPreserves
  have hA0 (u : HP0) : (A0 u : HP)=A (u : HP) := rfl
  have hA0self : IsSelfAdjoint A0 := by
    apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
    intro u v
    exact hAs.isSymmetric (u : HP) (v : HP)
  have hComm0 : Commute A0 ΓP0 := by
    apply ContinuousLinearMap.ext
    intro u
    apply Subtype.ext
    change (A0 (ΓP0 u) : HP)=(ΓP0 (A0 u) : HP)
    rw [hA0,hΓP0,hΓP0,hA0]
    exact congrArg (fun D : HP →L[ℝ] HP => D (u : HP)) hCommP.eq.symm
  have hSquare0 : A0*A0+ΓP0*ΓP0=(1 : HP0 →L[ℝ] HP0) := by
    apply ContinuousLinearMap.ext
    intro u
    apply Subtype.ext
    change (A0 (A0 u) : HP)+(ΓP0 (ΓP0 u) : HP)=(u : HP)
    rw [hA0,hA0,hΓP0,hΓP0]
    have h : ΓP (ΓP (u : HP))=(u : HP)-A (A (u : HP)) :=
      congrArg (fun D : HP →L[ℝ] HP => D (u : HP)) hΓPSq
    rw [h]
    abel
  have hStarInv : ΓP0*star Inv=(1 : HP0 →L[ℝ] HP0) := by
    have h := congrArg star hLeft
    simpa only [star_mul,hPos0.isSelfAdjoint.star_eq,star_one] using h
  have hInvSelf : IsSelfAdjoint Inv := by
    change star Inv=Inv
    calc
      star Inv=(Inv*ΓP0)*star Inv := by rw [hLeft,one_mul]
      _ = Inv*(ΓP0*star Inv) := mul_assoc _ _ _
      _ = Inv := by rw [hStarInv,mul_one]
  have hCommInv : Commute A0 Inv := by
    change A0*Inv=Inv*A0
    calc
      A0*Inv=(Inv*ΓP0)*(A0*Inv) := by rw [hLeft,one_mul]
      _ = Inv*((ΓP0*A0)*Inv) := by noncomm_ring
      _ = Inv*((A0*ΓP0)*Inv) := by rw [hComm0.eq.symm]
      _ = Inv*A0 := by simp only [mul_assoc,hRight,mul_one]
'''
tail=old[old.index('  refine ⟨hμ, ?_⟩'):old.index('\nend\nend Tests.')].replace('  exact hConsumer','  exact hGlobal')
tail=tail.replace('  refine ⟨hΓSq, ?_⟩','  refine ⟨hΓSq, ?_⟩\n  refine ⟨hCommRoot, ?_⟩').replace('  refine ⟨hΓPSq, ?_⟩','  refine ⟨hΓPSq, ?_⟩\n  refine ⟨hCommP, ?_⟩').replace('  refine ⟨hNormInv, ?_⟩','  refine ⟨hNormInv, ?_⟩\n  refine ⟨hInvSelf,A0,hA0,hA0self,hComm0,hSquare0,hCommInv,?_⟩')
caller=mainold[mainold.index('theorem actual_ambient_adjoint_centered_decomposition\n'):mainold.index(' := by\n',mainold.index('theorem actual_ambient_adjoint_centered_decomposition\n'))].replace('actual_ambient_adjoint_centered_decomposition','actual_same_root_inverse_commutation')
s='''import AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector
import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute

open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

'''+(pre/'statement1.definition.lean').read_text()+'\n\n'+caller+' := by\n'+prefix+math+tail+'''\nend
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation
'''
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean');assert not p.exists();p.write_text(s,encoding='utf-8',newline='\n')
