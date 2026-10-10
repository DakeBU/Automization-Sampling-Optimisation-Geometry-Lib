from pathlib import Path
import json,hashlib
R=Path('E:/Samplinglib');O=Path(__file__).parent
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(n,x):
 p=O/n
 with p.open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
 return pin(p)
p=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitDensity.json'
old=pin(p);assert old['raw_sha256']=='02059257abea104e6d64e2d3ec52a377076492956730a6ff601ba5dfd55e386d'
q=O/'.private.coordinator-audit89.after-exposition.exactraw.json';assert not q.exists();q.write_bytes(p.read_bytes())
index=put('hash-only-coordinator-input89.snapshot-index.json',{'status':'HASH_ONLY_SNAPSHOT_NO_VERDICT_CONTENT_READ','historical_location':old,'immutable_snapshot':pin(q),'reason':'Successor publication freeze descriptor was RAW-checked without reading canonical audit content. Coordinator may later legitimately evolve metadata after independent mathematics closure; historical RAW must resolve through this snapshot rather than future canonical bytes.','not_mathematical_or_source_verdict_evidence':True})
m=json.loads((O/'closed-RAW-manifest89.json').read_text('utf8'))
for d in m['frozen_current_inputs']:
 if d['path']==old['path']:
  d.update(pin(q));d['historical_location']=old['path'];d['read_mode']='RAW hash-only; content never parsed or used as verdict'
m['coordinator_hash_only_historical_resolution']=index
m['owned_artifacts']=[pin(x) for x in sorted(O.rglob('*')) if x.is_file() and x.name!='closed-RAW-manifest89.authoritative.json']
m['supersedes_closure_manifest_only']=pin(O/'closed-RAW-manifest89.json')
m['noncircular']='This authoritative manifest excludes itself; original closure and all original artifacts remain immutable. Only hash-only coordinator input resolution is made future-stable through an exact snapshot.'
result=put('closed-RAW-manifest89.authoritative.json',m)
print(json.dumps({'authoritative_closed_manifest':result,'snapshot_index':index},indent=2))
