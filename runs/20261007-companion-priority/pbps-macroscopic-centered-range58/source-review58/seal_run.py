import json,hashlib,os,time,datetime
from pathlib import Path
R=Path('E:/Samplinglib');T=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';B=T/'source-review58'
def h(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def rec(p):
    b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,o):(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=load(B/'input.manifest.json')
for p in [T.parent/'pbps-l2-macroscopic-mean55/math-freeze.json',T.parent/'pbps-l2-macroscopic-mean55/reviewer.source.run.json']:
    if not any(x['path']==rec(p)['path'] for x in m['supplemental_readonly_inputs']):m['supplemental_readonly_inputs'].append(rec(p))
write('input.manifest.json',m)
payload=load(B/'source-review-payload.json');payload['supplemental_input_count']=13;write('source-review-payload.json',payload)
run=dict(schema_version=1,native_schema='independent-primary-first-anti-anchored-three-source-review-run',actor_identity='/root/statement_topology58',status='SEALED_COMPLETE_PENDING_FINAL_LEASE_CLOSURE',source_review_payload=payload,source_review_payload_sha256=h(can(payload)),source_review_payload_artifact=rec(B/'source-review-payload.json'),source_review_payload_digest_rule='SHA256 sorted compact ensure_ascii=false UTF8 JSON of exact named payload; distinct from whole run.',run_sha256_algorithm='SHA256 sorted compact ensure_ascii=false UTF8 JSON of complete run excluding ONLY run_sha256; no narrowed payload substitution.',root_open_lease_snapshot=rec(B/'source.review.lease.OPEN.exactraw.snapshot.json'),input_manifest=rec(B/'input.manifest.json'),root_input_artifact_count=101,supplemental_input_artifact_count=13,result_count=3,semantic_slot_count=21,result_artifact_paths=['source.%d.review.json'%i for i in range(3)],output_manifest_path=str(B/'output.manifest.json'),output_manifest_binding_rule='Final exact raw/LF output manifest and complete/root CLOSED lease bind whole run plus run-bound result artifacts without hash cycle.',foreground_child_processes=[dict(native_chunk='71c116',script='collect_inputs.py',actual_exit_code=0,pid=41400),dict(native_chunk='3b53c3',script='author_payload.py',actual_exit_code=0,pid=35788)],compiler_started=False,compiler_status='NOT_STARTED_CLOSED',whole_math58_verdict_read=False,earlier58_semantic_delta_or_repair_verdict_read=False,canonical_or_Git_or_Lean_mutation=False,publications_corrected_or_accepted=False,mathematical_blocker_count=0,publication_blocker_count=1,resource=dict(pid=os.getpid(),cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system,foreground=True),created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
run['run_sha256']=h(can(run));write('run.json',run)
for i,result in enumerate(payload['results']):
    result=result.copy();result['review_run_sha256']=run['run_sha256'];result['source_review_payload_sha256']=run['source_review_payload_sha256'];write('source.%d.review.json'%i,result)
exclude={'output.manifest.json','validator.json','complete.json','lease.json','validator.foreground.stdout.txt','validator.foreground.stderr.txt'}
out=dict(schema_version=1,actor_identity='/root/statement_topology58',artifacts=[rec(p) for p in sorted(B.rglob('*')) if p.is_file() and p.name not in exclude],excluded_closure_files=sorted(exclude),whole_run_sha256=run['run_sha256'],root_inputs=101,supplemental_inputs=13)
write('output.manifest.json',out)
print(json.dumps(dict(pid=os.getpid(),run_sha256=run['run_sha256'],source_review_payload_sha256=run['source_review_payload_sha256'],output_manifest_count=len(out['artifacts']),run=rec(B/'run.json'))))
