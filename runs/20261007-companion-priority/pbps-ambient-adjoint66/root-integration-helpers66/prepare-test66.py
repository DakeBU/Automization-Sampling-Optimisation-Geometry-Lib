from pathlib import Path
import json,hashlib
pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66')
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
gate=json.loads((r/'focused-main-private-v6/receipt.json').read_bytes())
assert gate['exit_code']==0 and gate['terminal_closed']
parent=Path('Tests/ProximalBPSPolarIsometry.lean').read_text(encoding='utf-8')
begin=parent.index('  classical\n',parent.index(':= by'))
end=parent.index('  have hPosLocal',begin)
setup=parent[begin:end].replace('AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry.actual_centered_polar_isometry','AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition')
setup=setup.replace('hVadj,hVnorm⟩','hVadj,hVnorm,R,hR,hAmbient,hGlobal⟩')
setup=setup.replace('  dsimp only at hBase\n','')
body=setup+'''  change Lp ℝ 2 J →L[ℝ] Hperp at R
  have hRself (g : Hperp) : R (g : Lp ℝ 2 J)=g := by
    apply Subtype.ext
    rw [hR]
    rw [show P (g : Lp ℝ 2 J)=0 from g.property,sub_zero]
  refine ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,hAll,
    hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,q,hqa,hTq,hq,hCenter,hΓPq,hγ,
    ΓP0,hΓP0,hPos0,hOrder0,hUnit,Inv,hLeft,hRight,hNormInv,B0,hB0,V0,hVdef,
    hFactor,hVadj,hVnorm,R,hR,hAmbient,?_⟩
  intro f hf
  obtain ⟨fP,hfP,hCorrector,hRoot,hNorm,hVNorm⟩ := hGlobal f hf
  let fperp : Hperp := R f
  let fV : HP0 := V0.adjoint fperp
  have hSame : B.adjoint f=B.adjoint (fperp : Lp ℝ 2 J) := by
    calc
      B.adjoint f=HP0.subtypeL (B0.adjoint (R f)) := hAmbient f
      _ = HP0.subtypeL (B0.adjoint (R (fperp : Lp ℝ 2 J))) :=
        congrArg (fun z : Hperp => HP0.subtypeL (B0.adjoint z))
          (hRself fperp).symm
      _ = B.adjoint (fperp : Lp ℝ 2 J) := (hAmbient _).symm
  refine ⟨fP,fperp,fV,?_,hR f,rfl,hSame.trans (hCorrector.trans hRoot),?_⟩
  · rw [hfP,hR]
    change f=P f+(f-P f)
    abel
  · have hv : ‖fV‖≤‖fperp‖ := hVNorm
    have hn : ‖f‖^2=‖fP‖^2+‖fperp‖^2 := hNorm
    nlinarith [norm_nonneg fV,norm_nonneg fperp]
'''
raw=(pre/'independent-type-diagnosis66/proposed-named-adapter1.lean').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='0400010f8113409e1683ec89bc0ec8ad75e32b7c27077da72d7ceafc0c062966'
candidate=raw.decode().replace('\r\n','\n').replace('import AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry','import AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector',1)
candidate=candidate.replace('namespace IndependentTypeDiagnosis66','namespace Tests.ProximalBPSAmbientAdjointCorrector',1).replace('end IndependentTypeDiagnosis66','end Tests.ProximalBPSAmbientAdjointCorrector',1)
name='genuine_actual_global_corrector_consumer_statement'
candidate=candidate.replace('def '+name,'private def '+name,1).replace('#check '+name+'\n','')
assert candidate.count('  fail "INTENTIONAL_NAMED_PROP_BODY_REACHED66"')==1
p=Path('Tests/ProximalBPSAmbientAdjointCorrector.lean');assert not p.exists()
p.write_text(candidate.replace('  fail "INTENTIONAL_NAMED_PROP_BODY_REACHED66"','  unfold '+name+'\n'+body.rstrip())+'\n#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition\n#print axioms Tests.ProximalBPSAmbientAdjointCorrector.genuine_actual_global_corrector_consumer\n',encoding='utf-8',newline='\n')
print('Uncompiled genuine global corrector Test prepared from exact sealed header.')
