import json,hashlib,os,time
from pathlib import Path
B=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macroscopic-centered-range58/source0-verdict-addendum58')
def h(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
reads=[]
def check(r):
 a=rec(r['path']);assert all(a[k]==r[k] for k in ['raw_bytes','raw_sha256','lf_bytes','lf_sha256']),r['path'];reads.append(a)
start=time.monotonic();m=load(B/'input.manifest.json');assert len(m['inputs'])==21
for e in m['inputs']:
 for k in ['actual_input','exactraw_snapshot','crlf_to_lf_snapshot']:check(e[k])
for r in load(B/'output.manifest.json')['artifacts']:check(r)
run=load(B/'run.json');x=run.copy();sha=x.pop('run_sha256');assert h(can(x))==sha
payload=load(B/'source-review-payload.json');assert payload==run['source_review_payload'] and h(can(payload))==run['source_review_payload_sha256']
r=payload['results'][0];result=load(B/'source.0.verdict-addendum.review.json');assert result.pop('review_run_sha256')==sha;assert result.pop('source_review_payload_sha256')==run['source_review_payload_sha256'];assert result==r
original=load(r['classification_addendum']['original_result']['path']);assert r['semantic_slots']==original['semantic_slots'] and len(r['semantic_slots'])==7
assert r['verdict']==r['mathematical_fidelity_verdict']=='equivalent-after-elaboration';assert all(x['relation'] in {'same','equivalent','explicit-elaboration'} for x in r['semantic_slots'].values());assert r['semantic_slots']['scopes']['relation']=='explicit-elaboration';assert not r['mathematical_blockers'] and not r['publication_blockers'] and not r['repairs'];assert all(not d['blocking'] for d in r['deltas'])
check(run['input_manifest']);check(run['source_review_payload_artifact']);check(payload['original_result']);check(payload['current_packet'])
out=dict(schema_version=1,status='PASS_SOURCE0_VERDICT_ADDENDUM_NATIVE',actual_raw_lf_readback_count=len(reads),raw_lf_readbacks=reads,run_sha256=sha,source_review_payload_sha256=run['source_review_payload_sha256'],input_count=21,seven_slots_unchanged=True,classification_consistent_with_schema=True,resource=dict(pid=os.getpid(),wall_seconds=time.monotonic()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system))
(B/'validator.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='raw_lf_readbacks'}))
