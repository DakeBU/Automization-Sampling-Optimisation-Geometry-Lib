from pathlib import Path
import hashlib,json
p=Path('runs/20261007-companion-priority/pbps-macro-root63/macro-root-draft.lean');b=p.read_bytes()
q=p.with_name('macro-root-draft.v3.failed.exactraw.snapshot.lean');assert not q.exists();q.write_bytes(b)
s=b.decode('utf-8').replace('set_option maxHeartbeats 1600000','set_option maxHeartbeats 3200000\nset_option diagnostics true')
s=s.replace('      ext u\n      simp only','      apply ContinuousLinearMap.ext\n      intro u\n      simp only')
s=s.replace('        ext f\n        simp only','        apply ContinuousLinearMap.ext\n        intro f\n        simp only')
p.write_text(s,encoding='utf-8',newline='\n')
record={'v3_raw_sha256':hashlib.sha256(b).hexdigest(),'v3_exit':1,'failure':'Only deterministic whnf timeout1600000; earlier CLM/subtype and star-adjoint errors absent. No theorem credit from failed #print output.','route_change':'Restrict both remaining conjugation extensionality proofs to CLM equality; enable diagnostic unfolding counts, bounded3200000. Exact sealed theorem header unchanged.','proof_not_complete':True}
p.with_name('v3.compiler-diagnosis.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(record))
