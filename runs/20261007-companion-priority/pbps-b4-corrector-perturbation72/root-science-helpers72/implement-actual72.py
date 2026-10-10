from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-b4-perturbation-preproof72')
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72')
assert json.loads((r/'focused-generic-typed-inner/receipt.json').read_bytes())['exit_code']==0
p=pre/'header72.actual.named-literal.proposed.lean';raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='bb6eaa684a81dbf74d7778e8fa6e98f15c1b443fa3c1e0ec4d2b36560b1ab88d'
old=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean').read_text(encoding='utf8')
assert hashlib.sha256(Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean').read_bytes()).hexdigest()=='f321d13c612a3702e3d42043a49fff8feb3b76bb302638a60f9dad4cb166ad1a'
a=old.index('  unfold actual_corrector_change_statement\n');b=old.index('  change (∀ f : Lp ℝ 2 J,',a)
prefix=old[a:b].replace('unfold actual_corrector_change_statement','unfold actual_corrector_perturbation_statement',1)
prefix=prefix.replace('AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange.actual_corrector_change',1)
a=old.index('  have hFinal :');b=old.index('  refine ⟨hμ, ?_⟩',a)
final=old[a:b]
oldtail='C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2)'
newtail='''C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2 ∧
                                (∀ u v r : HP0,
                                  C (u+ΓP0 r) (v-A0 r)-C u v=
                                    inner ℝ u (Inv r)+‖r‖^2/2))'''
assert final.count(oldtail)==1
final=final.replace(oldtail,newtail).replace('⟨hD,hIntertwine,hGlobal71⟩','⟨hD,hIntertwine,hGlobal72⟩')
globaltype=final[final.index('      (∀ f : Lp ℝ 2 J,'):final.index(' := ⟨hD,')]
middle='''  let D : Hperp →L[ℝ] Hperp := R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL
  have hD (h : Hperp) : (D h : Lp ℝ 2 J)=
      U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J)) := hDparent h
  have hIntertwine : V0.adjoint ∘L D= -(A0 ∘L V0.adjoint) := hIntertwineParent
  have hΓself : IsSelfAdjoint ΓP0 := (show ΓP0.IsPositive from hPos0).isSelfAdjoint
  have hPerturb (u v r : HP0) :
      let C : HP0 → HP0 → ℝ := fun u v =>
        (‖u‖^2-‖v‖^2)/2-inner ℝ (A0 (Inv u)) v
      C (u+ΓP0 r) (v-A0 r)-C u v=inner ℝ u (Inv r)+‖r‖^2/2 := by
    exact AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.quadratic_corrector_perturbation
      A0 ΓP0 Inv hA0self hΓself hInvSelf hCommInv hLeft hRight hSquare0 u v r
  have hGlobal72 :
'''+globaltype+''' := by
    intro f hf
    obtain ⟨fP,hpf,hB,hEmbed,hEnergy,hVbound,hgMean,gP,hgpf,hgp,hgv,hPair,hCorrector⟩ :=
      hGlobal f hf
    refine ⟨fP,hpf,hB,hEmbed,hEnergy,hVbound,hgMean,gP,hgpf,hgp,hgv,hPair,hCorrector,?_⟩
    exact hPerturb
'''
tail=old[b:old.index('\n\nend\n',b)]
ending='''

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.actual_corrector_perturbation
'''
dest=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorPerturbation.lean');assert not dest.exists()
dest.write_text(raw.decode()+prefix+middle+final+tail+ending,encoding='utf8',newline='\n')
assert dest.read_bytes().startswith(raw)
print('WROTE exact sealed actual72 prefix and same-witness genuine generic consumer; PID',os.getpid())
