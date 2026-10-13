from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-macro-root63');pre=Path('runs/20261007-companion-priority/pbps-macro-root-preproof63');p=r/'macro-root-draft.lean';b=p.read_bytes();receipt=json.loads((r/'focused-macro-draft-v5/receipt.json').read_bytes());assert receipt['exit_code']==0 and receipt['terminal_closed'];assert receipt['inputs'][0]['raw_sha256']==hashlib.sha256(b).hexdigest()
q=r/'macro-root-draft.v5.PASS.exactraw.snapshot.lean';assert not q.exists();q.write_bytes(b)
header=(pre/'header1.lean').read_text(encoding='utf-8').rstrip()
body=''' := by
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
  nlinarith [norm_nonneg ((e.conjStarAlgEquiv Γ) f),norm_nonneg f,
    sq_nonneg ‖(HP.orthogonalProjectionOnto ∘L U.toContinuousLinearMap ∘L HP.subtypeL) f‖]
'''
# HP is a let in the sealed conclusion, hence the nlinarith auxiliary uses its
# concrete source expression. No additional mathematical premise is supplied.
body=body.replace('HP.orthogonalProjectionOnto','(lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2\n      (((volume : Measure E).tilted (fun x => -V x)).prod (stdGaussian E)).map\n        (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))).orthogonalProjectionOnto').replace('HP.subtypeL','(lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2\n      (((volume : Measure E).tilted (fun x => -V x)).prod (stdGaussian E)).map\n        (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))).subtypeL')
# Simpler: hf.2 itself determines the nonnegative subtracted term; use its
# known macro contraction hAn instead of repeating expanded source lets.
a=body.index('  nlinarith [')
body=body[:a]+'''  have hnonneg : 0 ≤ ‖f‖^2 - ‖(e.conjStarAlgEquiv Γ) f‖^2 := by
    rw [hf.2]
    simp only [sub_sub_cancel]
    positivity
  nlinarith [norm_nonneg ((e.conjStarAlgEquiv Γ) f),norm_nonneg f]
'''
test='namespace Tests.ProximalBPSMacroscopicDefectRoot\n\n'+header+body+'\nend Tests.ProximalBPSMacroscopicDefectRoot\n\n#print axioms Tests.ProximalBPSMacroscopicDefectRoot.genuine_actual_macroscopic_root_consumer\n'
(r/'consumer63.body-and-header.lean').write_text(test,encoding='utf-8',newline='\n');p.write_bytes(b+b'\n'+test.encode('utf-8'))
print('Preserved exact successful v5 proof; appended sealed original-input consumer deriving macro-root contraction, no production writes.')
