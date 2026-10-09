from pathlib import Path
import json,hashlib
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean');b=p.read_bytes();s=b.decode('utf-8')
d=Path('runs/20261007-companion-priority/pbps-sharp-energy68/compiler-diagnosis68')
snapshot=d/'main.v10-before-redundant-ring-repair.raw.snapshot.lean';assert not snapshot.exists();snapshot.write_bytes(b)
old='        field_simp\n        ring\n';assert s.count(old)==1
s=s.replace(old,'        field_simp\n').replace('stage10-','stage11-').replace('projection10-','projection11-').replace('reassembly10-','reassembly11-').replace('global10-','global11-')
p.write_text(s,encoding='utf-8',newline='\n')
(d/'redundant-ring-repair.json').write_text(json.dumps(dict(typed_class='IMPLEMENTATION_FAILED',compiler_receipt='runs/20261007-companion-priority/pbps-sharp-energy68/focused-actual68-v10-local-global/receipt.json',exact_error='No goals to be solved at redundant ring after field_simp already closed rational identity.',repair='Remove only the redundant ring tactic; all sealed statements and mathematical ingredients unchanged.',before_raw_sha256=hashlib.sha256(b).hexdigest(),after_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),previous_exit_code=1,previous_run_not_formal_success=True),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Removed one redundant ring after field_simp; clean diagnostic compile still required.')
