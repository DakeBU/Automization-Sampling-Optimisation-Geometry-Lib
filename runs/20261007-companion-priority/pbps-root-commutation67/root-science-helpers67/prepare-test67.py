from pathlib import Path
pre=Path('runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67');main=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean').read_text();old=Path('Tests/ProximalBPSAmbientAdjointCorrector.lean').read_text();prefix=old[old.index('  classical\n'):old.index('  have hRself')]
prefix=prefix.replace('  dsimp only\n','  unfold genuine_actual_corrector_coefficient_consumer_statement\n  dsimp only\n',1).replace('AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation')
prefix=prefix.replace('hΓ,hΓSq,hΓP,hΓPSq,hGram','hΓ,hΓSq,hCommRoot,hΓP,hΓPSq,hCommP,hGram').replace('Inv,hLeft,hRight,hNormInv,B0','Inv,hLeft,hRight,hNormInv,hInvSelf,A0,hA0,hA0self,hComm0,hSquare0,hCommInv,B0')
prefix=prefix.replace('  change HP0 →L[ℝ] HP0 at ΓP0 Inv','  change HP0 →L[ℝ] HP0 at ΓP0 Inv A0')
math='''  have hKself : IsSelfAdjoint (A0*Inv) := (hA0self.commute_iff hInvSelf).mp hCommInv
  have hCoefficient : (1 : HP0 →L[ℝ] HP0)+(A0*Inv)*(A0*Inv)=Inv*Inv := by
    have hFirst : (ΓP0*ΓP0)*(Inv*Inv)=(1 : HP0 →L[ℝ] HP0) := by
      calc
        (ΓP0*ΓP0)*(Inv*Inv)=ΓP0*((ΓP0*Inv)*Inv) := by noncomm_ring
        _ = (1 : HP0 →L[ℝ] HP0) := by rw [hRight,one_mul,hRight]
    have hSecond : (A0*Inv)*(A0*Inv)=(A0*A0)*(Inv*Inv) := by
      calc
        (A0*Inv)*(A0*Inv)=A0*((Inv*A0)*Inv) := by noncomm_ring
        _ = A0*((A0*Inv)*Inv) := by rw [hCommInv.eq.symm]
        _ = (A0*A0)*(Inv*Inv) := by noncomm_ring
    calc
      (1 : HP0 →L[ℝ] HP0)+(A0*Inv)*(A0*Inv)=
          (ΓP0*ΓP0)*(Inv*Inv)+(A0*A0)*(Inv*Inv) := by rw [hFirst,hSecond]
      _ = (ΓP0*ΓP0+A0*A0)*(Inv*Inv) := by rw [add_mul]
      _ = Inv*Inv := by rw [add_comm,hSquare0,one_mul]
'''
tail=main[main.index('  refine ⟨hμ, ?_⟩'):main.index('\nend\nend AutoSamplingTheory.')].replace('hSquare0,hCommInv,?_','hSquare0,hCommInv,hKself,hCoefficient,?_')
caller=main[main.index('theorem actual_same_root_inverse_commutation\n'):main.index(' := by\n',main.index('theorem actual_same_root_inverse_commutation\n'))].replace('actual_same_root_inverse_commutation','genuine_actual_corrector_coefficient_consumer')
s='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation

open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
namespace Tests.ProximalBPSActualRootCommutation
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

'''+(pre/'statement2.definition.lean').read_text()+'\n\n'+caller+' := by\n'+prefix+math+tail+'''\nend
end Tests.ProximalBPSActualRootCommutation

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation
#print axioms Tests.ProximalBPSActualRootCommutation.genuine_actual_corrector_coefficient_consumer
'''
p=Path('Tests/ProximalBPSActualRootCommutation.lean');assert not p.exists();p.write_text(s,encoding='utf-8',newline='\n')
