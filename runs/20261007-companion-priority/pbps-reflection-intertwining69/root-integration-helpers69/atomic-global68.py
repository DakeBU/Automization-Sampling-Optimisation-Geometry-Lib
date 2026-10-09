from pathlib import Path
import hashlib,json,re
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68/compiler-diagnosis68')
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean')
b=p.read_bytes();s=b.decode('utf-8')
snapshot=r/'main.before-atomic-global.raw.snapshot.lean';assert not snapshot.exists();snapshot.write_bytes(b)
old='  obtain ⟨fP,hfP,hBf,hΓf,hPyth,hNormV⟩ := hGlobal f hf'
assert s.count(old)==1
new='''  obtain ⟨fP,hGlobalFields⟩ := hGlobal f hf
  have hfP := hGlobalFields.1
  have hBf := hGlobalFields.2.1
  have hΓf := hGlobalFields.2.2.1
  have hPyth := hGlobalFields.2.2.2.1
  have hNormV := hGlobalFields.2.2.2.2'''
s=s.replace(old,new).replace('stage8-','stage9-').replace('projection8-','projection9-').replace('reassembly8-','reassembly9-')
needle='  intro f hf\n'+new
assert s.count(needle)==1
s=s.replace(needle,'  intro f hf\n  run_tac do\n    let _ ← IO.FS.writeFile ".astis/pbps-sharp-energy68/global9-intro.log" "after global input introduction\\n"\n    pure ()\n'+new)
needle='  obtain ⟨fP,hGlobalFields⟩ := hGlobal f hf\n'
s=s.replace(needle,needle+'  run_tac do\n    let _ ← IO.FS.writeFile ".astis/pbps-sharp-energy68/global9-witness.log" "after global witness elimination\\n"\n    pure ()\n')
p.write_text(s,encoding='utf-8',newline='\n')
(r/'atomic-global-route.json').write_text(json.dumps(dict(route='The same atomically eliminated existential and bounded proof projections now apply to the final actual-input decomposition; retain exact fP and all five original clauses.',before_raw_sha256=hashlib.sha256(b).hexdigest(),after_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),statement_or_mathematics_change=False,previous_v8_math_phases_reached='parent extraction, coefficient identity, pair bound, all59 witness constructors',previous_v8_not_formal_success=True),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Final actual-input existential now atomic;5 proof fields projected; same statement and mathematics.')
