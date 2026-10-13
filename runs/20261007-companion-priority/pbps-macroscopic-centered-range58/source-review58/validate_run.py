import json,hashlib,os,time
from pathlib import Path
R=Path('E:/Samplinglib');T=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';B=T/'source-review58'
def h(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def rec(p):
    b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
readbacks=[]
def check(r):
    got=rec(r['path']);assert all(got[k]==r[k] for k in ['raw_bytes','raw_sha256','lf_bytes','lf_sha256']),r['path'];readbacks.append(got)
start=time.monotonic();m=load(B/'input.manifest.json')
for e in m['inputs']:
    for k in ['actual_input','exactraw_snapshot','crlf_to_lf_snapshot']:check(e[k])
for r in m['supplemental_readonly_inputs']:check(r)
for r in load(B/'output.manifest.json')['artifacts']:check(r)
run=load(B/'run.json');x=run.copy();runsha=x.pop('run_sha256');assert h(can(x))==runsha
payload=load(B/'source-review-payload.json');assert payload==run['source_review_payload'] and h(can(payload))==run['source_review_payload_sha256']
for i,r in enumerate(payload['results']):
    actual=load(B/('source.%d.review.json'%i));assert actual.pop('review_run_sha256')==runsha;assert actual.pop('source_review_payload_sha256')==run['source_review_payload_sha256'];assert actual==r
    assert len(r['semantic_slots'])==7 and all(s['relation']!='not-audited' and s['evidence'] for s in r['semantic_slots'].values())
    p=load(T/('source.%d.reviewer-packet.json'%i));assert p['packet_sha256']==r['reviewer_packet_sha256']
assert payload['results'][2]['publication_blockers'] and not payload['results'][2]['mathematical_blockers']
assert not run['compiler_started'] and not run['canonical_or_Git_or_Lean_mutation']
out=dict(schema_version=1,status='PASS_EXACT_ORIGINAL_SOURCE_REVIEW_NATIVE',actor_identity='/root/statement_topology58',root_input_artifacts=101,supplemental_input_artifacts=13,actual_raw_lf_readback_count=len(readbacks),raw_lf_readbacks=readbacks,run_sha256=runsha,source_review_payload_sha256=run['source_review_payload_sha256'],resource=dict(pid=os.getpid(),wall_seconds=time.monotonic()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system),publication_blocker_preserved=True)
(B/'validator.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='raw_lf_readbacks'}))
