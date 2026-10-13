import copy,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(n):return json.loads((out/n).read_bytes())
lease=load('lease.final.json');manifest=load('owned-manifest.json');entries=manifest['regular_file_entries']
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] is True and lease['postclose_writes_permitted'] is False
assert len(entries)==lease['regular_file_count']==manifest['regular_file_count']
assert sha(canon(entries))==lease['finite_owned_closure_sha256']==manifest['closure_entries_canonical_sha256']
assert sha((out/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']
expected={e['name'] for e in entries}|{'owned-manifest.json','lease.final.json'}
assert expected=={p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()} and len(expected)==lease['owned_file_count']
for e in entries:
 b=(out/e['name']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256']
r=load('review-run.json');c=copy.deepcopy(r);del c['run_sha256'];assert sha(canon(c))==r['run_sha256']==lease['whole_logical_run_sha256']
d=load('source.0.decision.json');assert d['review_run_sha256']==r['run_sha256'] and d['reviewer_packet_sha256']==lease['reviewer_packet_canonical_sha256']
print(json.dumps(dict(schema='source69-read-only-postclose-observation-v1',actual_postclose_observer_pid=os.getpid(),read_only=True,status='CLOSED_LAST',all_owned_hashes_verified=len(entries),owned_file_count=len(expected),manifest_RAW_sha256=lease['manifest_RAW_sha256'],lease_RAW_sha256=sha((out/'lease.final.json').read_bytes()),finite_owned_closure_sha256=lease['finite_owned_closure_sha256'],whole_logical_run_sha256=r['run_sha256'],source_decision_RAW_sha256=sha((out/'source.0.decision.json').read_bytes()),complete_named_review_decision_input_RAW_sha256=sha((out/'complete-named-review-decision-input-payload.json').read_bytes()),RAW_LF_input_RAW_sha256=sha((out/'RAW-input-payload.json').read_bytes()),verdict=d['verdict'],source_review_state='accepted',source_math=419,module_lines=446,BODY_steps=6,semantic_slots=7,semantic_deltas=12,complete_named_inputs=62),sort_keys=True))
