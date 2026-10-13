import json,hashlib,os,datetime
from pathlib import Path
B=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macroscopic-centered-range58/source0-verdict-addendum58')
def h(b):return hashlib.sha256(b).hexdigest()
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def write(n,o):(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
payload=load(B/'source-review-payload.json')
run=dict(schema_version=1,native_schema='independent-source0-schema-verdict-addendum-run',actor_identity='/root/statement_topology58',status='SEALED_COMPLETE_PENDING_FINAL_LEASE_CLOSURE',source_review_payload=payload,source_review_payload_sha256=h(can(payload)),source_review_payload_artifact=rec(B/'source-review-payload.json'),source_review_payload_digest_rule='SHA256 sorted compact ensure_ascii=false UTF8 JSON of exact named payload; distinct from whole native run.',run_sha256_algorithm='SHA256 sorted compact ensure_ascii=false UTF8 JSON of full run excluding ONLY run_sha256.',input_manifest=rec(B/'input.manifest.json'),input_count=21,result_count=1,semantic_slot_count=7,result_artifact_paths=['source.0.verdict-addendum.review.json'],output_manifest_path=str(B/'output.manifest.json'),output_manifest_binding_rule='Final output manifest and CLOSED lease bind run/results without a hash cycle.',foreground_processes=[dict(script='review.py',native_chunk='f98998',actual_exit_code=0,pid=40604)],compiler_started=False,compiler_status='NOT_STARTED_CLOSED',canonical_or_Git_or_Lean_mutation=False,original_seven_slots_unchanged=True,theorem_or_source_or_signature_changed=False,source2_current_acceptance_changed=False,mathematical_blocker_count=0,publication_blocker_count=0,resource=dict(pid=os.getpid(),cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system,foreground=True),created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
run['run_sha256']=h(can(run));write('run.json',run)
result=payload['results'][0].copy();result['review_run_sha256']=run['run_sha256'];result['source_review_payload_sha256']=run['source_review_payload_sha256'];write('source.0.verdict-addendum.review.json',result)
exclude={'output.manifest.json','validator.json','complete.json','lease.json','validator.foreground.stdout.txt','validator.foreground.stderr.txt'}
out=dict(schema_version=1,artifacts=[rec(p) for p in sorted(B.rglob('*')) if p.is_file() and p.name not in exclude],excluded_closure_files=sorted(exclude),whole_run_sha256=run['run_sha256']);write('output.manifest.json',out)
print(json.dumps(dict(pid=os.getpid(),run_sha256=run['run_sha256'],source_review_payload_sha256=run['source_review_payload_sha256'],output_manifest_count=len(out['artifacts']),run=rec(B/'run.json'))))
