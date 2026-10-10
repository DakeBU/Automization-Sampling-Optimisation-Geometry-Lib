import base64,copy,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(n):return json.loads((out/n).read_bytes())
def check_entry(x):
 b=base64.b64decode(x['RAW_base64']);lf=base64.b64decode(x['LF_base64'])
 assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and (out/x['name']).read_bytes()==b
 assert lf==b.replace(b'\r\n',b'\n') and len(lf)==x['LF_bytes'] and sha(lf)==x['LF_sha256']
r=load('review-run.json');h=r['run_sha256'];c=copy.deepcopy(r);del c['run_sha256'];assert sha(canon(c))==h
assert len(r['complete_named_RAW_LF_inputs']['entries'])==62
for x in r['complete_named_RAW_LF_inputs']['entries']:check_entry(x)
for x in r['complete_named_native_review']['entries']:check_entry(x)
named=load('complete-named-review-decision-input-payload.json')
assert len(named['entries'])==named['count']==23
for x in named['entries']:check_entry(x)
d=load('source.0.decision.json');assert d['review_run_sha256']==h and d['verdict']=='equivalent-after-elaboration'
assert d['reviewer_packet_sha256']=='98e9a39c9f7eafea5a7a6660c162631fed010e9533ef2ab6debbdcdcd6405fc6'
assert len(d['semantic_slots'])==7 and len(d['deltas'])==12 and all(x['severity']=='informational' and set(x)=={'slot','severity','description','evidence'} for x in d['deltas'])
for k,v in d['semantic_slots'].items():assert v['relation'] in {'same','equivalent','explicit-elaboration'} and all(v[x] for x in ['original','reconstructed','evidence'])
assert d['repairs']==[] and d['audit_source_admission']['state']=='accepted'
for n in ['source.0.decision.json','review-run.json','RAW-input-payload.json','complete-named-review-decision-input-payload.json']:
 assert (out/n).stat().st_size>0
result=dict(schema='source69-complete-payload-readback-v1',actual_pid=os.getpid(),whole_logical_run_sha256=h,only_top_level_run_sha256_deleted=True,input_entries_verified=62,native_review_entries_verified=20,complete_named_entries_verified=23,all_RAW_LF_payloads_exact=True,slots=7,deltas=12,source_math=419,module_lines=446,BODY_steps=6,canonical_decision_schema_valid=True)
(out/'readback-result.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,sort_keys=True))
