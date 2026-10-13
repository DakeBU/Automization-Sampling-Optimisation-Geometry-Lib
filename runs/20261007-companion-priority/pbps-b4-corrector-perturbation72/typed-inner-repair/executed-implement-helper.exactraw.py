from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-b4-perturbation-preproof72')
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72')
claim=json.loads((r/'claim.json').read_bytes());assert claim['state']=='PROPOSED'
p=pre/'header72.generic.proposed.lean';raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='d1435ac883ab1ba0d2b763a8094664d3eba18970a0fa8ff9cd051dc2966fdd8a'
header=raw.decode().replace('import Mathlib.Analysis.InnerProductSpace.Adjoint\n','import Mathlib.Analysis.InnerProductSpace.Adjoint\nimport Mathlib.Tactic.Linarith\n',1)
body=''' := by
  dsimp only
  have hIG (x : H) : Inv (G x)=x := by
    have h := congrArg (fun L : H →L[ℝ] H => L x) hInvG
    simpa only [ContinuousLinearMap.mul_apply,ContinuousLinearMap.one_apply] using h
  have hSq (x : H) : A (A x)+G (G x)=x := by
    have h := congrArg (fun L : H →L[ℝ] H => L x) hSquares
    simpa only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
      ContinuousLinearMap.one_apply] using h
  have hEnergy (x : H) : ‖A x‖^2+‖G x‖^2=‖x‖^2 := by
    have h := congrArg (fun z : H => inner ℝ z x) (hSq x)
    rw [inner_add_left,hA.isSymmetric (A x) x,hG.isSymmetric (G x) x] at h
    simpa only [real_inner_self_eq_norm_sq] using h
  have hLinear (x : H) : Inv (A (A x))+G x=Inv x := by
    calc
      Inv (A (A x))+G x=Inv (A (A x))+Inv (G (G x)) := by rw [hIG]
      _ = Inv (A (A x)+G (G x)) := by rw [map_add]
      _ = Inv x := congrArg Inv (hSq x)
  have hMixed : inner ℝ (A (Inv u)) (A r)+inner ℝ u (G r)=inner ℝ u (Inv r) := by
    rw [hA.isSymmetric (Inv u) (A r),hInv.isSymmetric u (A (A r)),
      ← inner_add_right,hLinear r]
  rw [norm_add_sq_real,norm_sub_sq_real]
  simp only [map_add,hIG,inner_add_left,inner_sub_right,real_inner_self_eq_norm_sq]
  rw [real_inner_comm v (A r)]
  nlinarith only [hEnergy r,hMixed]

end
end AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.quadratic_corrector_perturbation
'''
dest=Path(claim['proposed_files'][0]);assert not dest.exists()
dest.write_text(header+body,encoding='utf8',newline='\n')
assert dest.read_text(encoding='utf8').split(' := by\n',1)[0].replace('import Mathlib.Tactic.Linarith\n','')==raw.decode().rstrip('\n')+'\n'
print('WROTE exact sealed generic72 signature, proof-only tactic import; PID',os.getpid())
