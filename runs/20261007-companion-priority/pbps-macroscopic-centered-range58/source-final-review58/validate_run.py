import json,hashlib,os,time
from pathlib import Path
R=Path('E:/Samplinglib');T=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';B=T/'source-final-review58'
def h(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
readbacks=[]
def check(r):
 got=rec(r['path']);assert all(got[k]==r[k] for k in ['raw_bytes','raw_sha256','lf_bytes','lf_sha256']),r['path'];readbacks.append(got)
start=time.monotonic();m=load(B/'input.manifest.json');assert len(m['inputs'])==43 and len(m['supplemental_readonly_inputs'])==14
for e in m['inputs']:
 for k in ['actual_input','exactraw_snapshot','crlf_to_lf_snapshot']:check(e[k])
for r in m['supplemental_readonly_inputs']:check(r)
for r in load(B/'output.manifest.json')['artifacts']:check(r)
run=load(B/'run.json');x=run.copy();runsha=x.pop('run_sha256');assert h(can(x))==runsha
payload=load(B/'source-review-payload.json');assert payload==run['source_review_payload'] and h(can(payload))==run['source_review_payload_sha256']
r=payload['results'][0];actual=load(B/'source.2.final.review.json');assert actual.pop('review_run_sha256')==runsha;assert actual.pop('source_review_payload_sha256')==run['source_review_payload_sha256'];assert actual==r
assert len(r['semantic_slots'])==7 and all(s['relation']!='not-audited' and s['evidence'] for s in r['semantic_slots'].values())
p=load(T/'source.2.final.reviewer-packet.json');q=p.copy();packetsha=q.pop('packet_sha256');assert h(can(q))==packetsha==r['reviewer_packet_sha256'];assert p['publication_binding_sha256']==r['publication_binding_sha256'];assert not any(p['anti_anchoring'].values())
assert r['mathematical_fidelity_verdict']=='equivalent-after-elaboration' and not r['mathematical_blockers'];assert len(r['publication_blockers'])==1 and r['publication_review_status']=='BLOCKED_CURRENT_BINDING_DIMENSION_WORDING';assert r['dimension_wording_main_status']=='ACCEPTED_CURRENT_MAIN_STATEMENT' and r['Mathlib_reference_status']=='ACCEPTED_CURRENT_LINEARISOMETRY_NORM_MAP'
check(r['original_negative_preserved']);check(r['successor_negative_preserved']);check(payload['route_diagnosis_artifact'])
for receipt in payload['unchanged_current_code_decoder_packets01_checks']:check(receipt)
check(run['input_manifest']);check(run['root_open_lease_snapshot']);check(run['source_review_payload_artifact']);assert not run['compiler_started'] and not run['canonical_or_Git_or_Lean_mutation']
out=dict(schema_version=1,status='PASS_EXACT_FINAL_SOURCE_REVIEW_WITH_BINDING_WORDING_BLOCKER',actor_identity='/root/statement_topology58',root_input_artifacts=43,supplemental_input_artifacts=14,actual_raw_lf_readback_count=len(readbacks),raw_lf_readbacks=readbacks,run_sha256=runsha,source_review_payload_sha256=run['source_review_payload_sha256'],resource=dict(pid=os.getpid(),wall_seconds=time.monotonic()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system),original_negative_preserved=True,mathematical_blockers=0,publication_blockers=1)
(B/'validator.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='raw_lf_readbacks'}))
