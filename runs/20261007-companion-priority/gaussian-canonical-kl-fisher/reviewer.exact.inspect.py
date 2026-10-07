from pathlib import Path
import json,hashlib,subprocess,datetime
root=Path(r'E:/Samplinglib'); run=root/'runs/20261007-companion-priority/gaussian-canonical-kl-fisher'
commit='19b569ae0fe37c97da0f98b4d1f4933ebabc7052'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads((root/p).read_text(encoding='utf-8-sig'))
def summarize(p):
 j=read(p); print('\nFILE',p,'KEYS',list(j) if isinstance(j,dict) else type(j).__name__)
 if isinstance(j,dict):
  for k,v in j.items():
   if k in ['inputs','input_pins','source_inputs','reachable_sources','path_pins','checks','commands','focused_checks']:
    print(k, ('count '+str(len(v))) if isinstance(v,(dict,list)) else v)
   elif len(str(v))<3000: print(k, json.dumps(v,ensure_ascii=False))
(run/'reviewer.exact.lease.open.raw.snapshot.json').write_bytes((run/'reviewer.exact.lease.json').read_bytes())
for p in ['runs/20261007-companion-priority/gaussian-canonical-kl-fisher/whole-proof-review43/reviewer.math.review.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher/whole-proof-review43/reviewer.math.run.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher/whole-proof-review43/reviewer.math.checks.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher/whole-proof-review43/reviewer.math.inputs.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher/source.1.review.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher/source.review.repair1.lease.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher/source.review.repair1.overlay-review.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher/anonymous.0.decoder.json','runs/20261007-companion-priority/gaussian-noncompact-lsi/verified.json']: summarize(p)
