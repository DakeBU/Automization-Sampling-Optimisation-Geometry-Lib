import json,hashlib,os,time
from pathlib import Path
B=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macroscopic-centered-range58/reader-controls58/independent-review')
def h(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(n):return json.loads((B/n).read_text(encoding='utf-8'))
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
reads=[]
def check(r):
 assert rec(r['path'])==r,r['path'];reads.append(r)
start=time.monotonic();m=load('input.manifest.json');assert m['input_count']==len(m['inputs'])==54 and not m['basename_aliases_used'] and len({r['qualified_identity'] for r in m['inputs']})==54
for e in m['inputs']:
 for k in ['actual_input','exactraw_snapshot','crlf_to_lf_snapshot']:check(e[k])
for r in load('output.manifest.json')['artifacts']:check(r)
run=load('run.json');x=dict(run);sha=x.pop('run_sha256');assert h(can(x))==sha;p=load('repair-payload.json');assert p==run['reader_controls_repair_payload'] and h(can(p))==run['reader_controls_repair_payload_sha256'] and sha!=h(can(p))
result=load('reader-controls.review.json');assert result.pop('review_run_sha256')==sha and result.pop('reader_controls_repair_payload_sha256')==h(can(p)) and result==p
assert p['status']=='ACCEPT_SCOPED_READER_CONTROLS_REPAIR' and len(p['controls'])==len(p['clipboard_readbacks'])==9 and len(p['downloads'])==p['completed_native_download_event_count']==3 and len(p['actual_visuals'])==2 and all(v['actually_viewed_with_view_image'] for v in p['actual_visuals'])
assert len(p['rows'])==3 and sum(r['proof_steps'] for r in p['rows'])==11 and len(p['unchanged_canonical_code_publication_lesson_audit_receipts'])==12 and not p['blocking_repair_deltas'] and len(p['retained_failures'])==4
assert not any(p[k] for k in ['full_reader_accepted','Chapter1_3_full_reader_acceptance','full_Exposition_Seal','PURIFIED','live_verified','math_source_acceptance_changed','canonical_Git_Lean_renderer_state_edits','compiler_started'])
assert p['own_browser_closure']['status']=='CLOSED' and p['own_browser_closure']['actualBrowserExit']['code']==0 and p['root_actual_checks']['browser']['actual_exit_code']==0
check(run['input_manifest']);check(run['payload_artifact'])
o=dict(schema_version=1,status='PASS_INDEPENDENT_SCOPED_READER_CONTROLS_REPAIR',run_sha256=sha,reader_controls_repair_payload_sha256=h(can(p)),actual_raw_lf_readback_count=len(reads),raw_lf_readbacks=reads,input_count=54,resource=dict(pid=os.getpid(),wall_seconds=time.monotonic()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system))
(B/'validator.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in o.items() if k!='raw_lf_readbacks'}))
