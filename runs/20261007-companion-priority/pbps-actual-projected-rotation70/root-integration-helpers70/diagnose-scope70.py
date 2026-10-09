from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean')
d=r/'compiler-diagnosis70';d.mkdir(exist_ok=False)
b=p.read_bytes();(d/'v1.production.exactraw.snapshot.lean').write_bytes(b)
s=b.decode();body=s.index(' := by\n');head=s[:body]
markers=['  classical\n','  have parentSlice0 := hBase\n','  obtain ⟨e, parentSlice12⟩ := parentSlice11\n',
 '  obtain ⟨Γ, parentSlice25⟩ := parentSlice24\n','  have hGlobal := parentSlice66.2\n',
 '  let D : Hperp','  have hUIntegral','  have hPIntegral','  have hIntegrable',
 '  have hPself','  have hEnergy','  have hGlobal70','    intro f hf\n',
 '    obtain ⟨gP,hgP,hgtail⟩','    have hgPformula','    have hgVformula','    have hgEnergy',
 '  have hFinal','  refine ⟨hμ, ?_⟩','  exact hFinal']
out=s
for i,key in enumerate(markers):
 a=out.index(key,body);indent=key[:len(key)-len(key.lstrip())]
 # Keep markers before the complete tactic/declaration; never split multiline terms.
 out=out[:a]+indent+f'trace "SCOPE70_{i:02d}"\n'+out[a:]
assert out[:out.index(' := by\n')]==head
q=Path('.astis/pbps-actual-rotation70/diagnostic-scope-v1.lean');assert not q.exists()
q.write_text(out,encoding='utf-8',newline='\n')
(d/'scope-error-diagnosis.json').write_text(json.dumps(dict(actual_root_PID=os.getpid(),
 failure='Lean unknown free variable _fvar.8861 at theorem declaration, focused-v1 PID44168 EXIT1.',
 classification='IMPLEMENTATION_FAILED',sealed_statement_unchanged=True,
 recovery_no_axioms_not_accepted=True,production_RAW_sha256=hashlib.sha256(b).hexdigest(),
 diagnostic_only=q.as_posix(),goal='Locate elaboration stage before changing the proof route; no theorem credit.'),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Preserved exact v1 and created trace-only diagnostic; production unchanged, no statement change.')
