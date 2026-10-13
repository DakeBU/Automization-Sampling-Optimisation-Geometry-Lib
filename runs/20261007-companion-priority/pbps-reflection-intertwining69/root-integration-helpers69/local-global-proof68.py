from pathlib import Path
import hashlib,json,re
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean')
b=p.read_bytes();s=b.decode('utf-8')
d=Path('runs/20261007-companion-priority/pbps-sharp-energy68/compiler-diagnosis68')
snapshot=d/'main.before-local-global-proof.raw.snapshot.lean';assert not snapshot.exists();snapshot.write_bytes(b)
a=s.index('  intro f hf\n');z=s.index('\n\n\nend\nend ',a)
proof=s[a:z]
signature='''  have hFinal : ∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
      ∃ fP : HP0,
        HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
        let fperp : Hperp := R f
        let fV : HP0 := V0.adjoint fperp
        B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) ∧
        HP0.subtypeL (ΓP0 fV)=ΓP (HP0.subtypeL fV) ∧
        ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
        ‖fP‖^2+‖fV‖^2≤‖f‖^2 ∧ |C fP fV|≤‖f‖^2/(2*γ) := by
'''
s=s[:a]+'  exact hFinal'+s[z:]
insert=s.index('  unfold actual_sharp_corrector_bound_statement\n')
local=signature+''.join('  '+line if line.strip() else line for line in proof.splitlines(keepends=True))+'\n'
s=s[:insert]+local+s[insert:]
s=s.replace('stage9-','stage10-').replace('projection9-','projection10-').replace('reassembly9-','reassembly10-').replace('global9-','global10-')
p.write_text(s,encoding='utf-8',newline='\n')
(d/'local-global-proof-route.json').write_text(json.dumps(dict(route='Prove the exact final actual-input conclusion as a local have with compact explicitly named spaces and witnesses before reassembling the large outer literal proposition. Then use the same local proof at the final constructor. This changes elaboration context, not any mathematical ingredient.',before_raw_sha256=hashlib.sha256(b).hexdigest(),after_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),public_statement_unchanged=True,new_Lean_declarations=False,providers_added=False,mathematics_changed=False,compiler_credit=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Exact final actual-input proof localized before full outer reassembly; no new declaration/provider.')
