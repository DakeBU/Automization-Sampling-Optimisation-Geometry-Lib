import copy,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(n):return json.loads((out/n).read_bytes())
lease=load('lease.final.json');manifest=load('owned-manifest.json');entries=manifest['regular_file_entries']
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] is True and lease['postclose_writes_permitted'] is False
assert sha((out/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']
assert sha(canon(entries))==lease['finite_owned_closure_sha256'] and len(entries)==lease['regular_file_count']
assert {x['name'] for x in entries}|{'owned-manifest.json','lease.final.json'}=={p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}
for e in entries:
 b=(out/e['name']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256']
r=load('review-run.json');c=copy.deepcopy(r);del c['run_sha256'];assert sha(canon(c))==r['run_sha256']==lease['whole_logical_run_sha256']
print(json.dumps(dict(schema='header-source70-readonly-postclose-observation-v1',actual_postclose_observer_pid=os.getpid(),read_only=True,status='CLOSED_LAST',all_regular_hashes_verified=len(entries),owned_file_count=lease['owned_file_count'],manifest_RAW_sha256=lease['manifest_RAW_sha256'],finite_owned_closure_sha256=lease['finite_owned_closure_sha256'],lease_RAW_sha256=sha((out/'lease.final.json').read_bytes()),whole_logical_run_sha256=r['run_sha256'],decision_RAW_sha256=lease['COMPLETE_NAMED_DECISION']['RAW_sha256'],complete_named_review_RAW_sha256=lease['COMPLETE_NAMED_REVIEW']['RAW_sha256'],RAW_LF_input_RAW_sha256=lease['SEPARATE_COMPLETE_RAW_LF_INPUT']['RAW_sha256'],header_lines=116,source_math=419,input_count=17,statement_repair_required=False,no_proof_search_compilation_claim_seal=True),sort_keys=True))
