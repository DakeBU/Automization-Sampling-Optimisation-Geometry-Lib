import json,hashlib,os,time
from pathlib import Path
B=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macroscopic-centered-range58/exposition-seal58')
def h(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
reads=[]
def check(r):
 a=rec(r['path']);assert all(a[k]==r[k] for k in ['raw_bytes','raw_sha256','lf_bytes','lf_sha256']),r['path'];reads.append(a)
start=time.monotonic();m=load(B/'input.manifest.json');assert len(m['inputs'])==87 and not m['basename_aliases_used'];assert len(set(e['qualified_identity'] for e in m['inputs']))==87
for e in m['inputs']:
 for k in ['actual_input','exactraw_snapshot','crlf_to_lf_snapshot']:check(e[k])
for r in load(B/'output.manifest.json')['artifacts']:check(r)
run=load(B/'run.json');x=run.copy();sha=x.pop('run_sha256');assert h(can(x))==sha
payload=load(B/'exposition-seal-payload.json');assert payload==run['exposition_seal_payload'] and h(can(payload))==run['exposition_seal_payload_sha256']
result=load(B/'exposition.seal.json');assert result.pop('review_run_sha256')==sha;assert result.pop('exposition_seal_payload_sha256')==run['exposition_seal_payload_sha256'];assert result==payload
assert payload['result_count']==len(payload['rows'])==3 and sum(r['proof_step_count'] for r in payload['rows'])==11
assert sum(len(r['inline_exact_Lean']) for r in payload['rows'])==6 and all(x['initially_folded'] and x['exact_current_source_substring'] for r in payload['rows'] for x in r['inline_exact_Lean'])
assert len(payload['actual_visuals'])==4 and all(v['actually_viewed_with_view_image'] for v in payload['actual_visuals'])
assert not payload['blocking_reader_fidelity_deltas'] and len(payload['reader_delivery_blockers'])==1;assert payload['reader_delivery_blockers'][0]['classification']=='reader-delivery-missing-clipboard-and-direct-source-download';assert not payload['full_Exposition_Seal'] and not payload['PURIFIED'] and not payload['Chapter1_3_full_reader_acceptance'] and not payload['live_or_physical_device_verified']
assert len(payload['integration_gates'])==14 and all(g['actual_recorded_exit_code']==0 for g in payload['integration_gates']);assert not payload['renderer_or_canonical_or_state_or_Git_edits'] and not payload['source_acceptance_changed']
check(run['input_manifest']);check(run['exposition_seal_payload_artifact']);check(run['retained_tooling_failure'])
out=dict(schema_version=1,status='PASS_SCOPED_EXPOSITION_NATIVE_WITH_READER_DELIVERY_BLOCKER',actual_raw_lf_readback_count=len(reads),raw_lf_readbacks=reads,run_sha256=sha,exposition_seal_payload_sha256=run['exposition_seal_payload_sha256'],input_count=87,source_fidelity_blockers=0,reader_delivery_blockers=1,resource=dict(pid=os.getpid(),wall_seconds=time.monotonic()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system))
(B/'validator.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='raw_lf_readbacks'}))
