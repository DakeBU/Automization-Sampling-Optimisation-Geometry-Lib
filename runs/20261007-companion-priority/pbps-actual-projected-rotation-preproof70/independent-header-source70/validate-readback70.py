import base64,copy,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(n):return json.loads((out/n).read_bytes())
def check(e):
 b=base64.b64decode(e['RAW_base64']);lf=base64.b64decode(e['LF_base64'])
 assert b==(out/e['name']).read_bytes() and len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256']
 assert lf==b.replace(b'\r\n',b'\n') and len(lf)==e['LF_bytes'] and sha(lf)==e['LF_sha256']
r=load('review-run.json');c=copy.deepcopy(r);del c['run_sha256'];assert sha(canon(c))==r['run_sha256']
for e in r['complete_exact_RAW_LF_inputs']['entries']:check(e)
for e in r['complete_named_review']['entries']:check(e)
assert len(r['complete_exact_RAW_LF_inputs']['entries'])==17 and len(r['complete_named_review']['entries'])==13
assert r['decision']==load('independent-header-source70.decision.json')
s=load('primary419-NODE-EXCLUDED70.json');h=load('header-line-coverage70.json')
assert s['count']==len(s['entries'])==419 and s['counts']=={'EXCLUDED':246,'NODE':173} and s['unclassified']==0
assert h['line_count']==len(h['entries'])==116 and h['unclassified']==0
assert sha(canon(s['entries']))==s['entries_canonical_sha256'] and sha(canon(h['entries']))==h['entries_canonical_sha256']
assert r['decision']['mathematical_statement_repair_required'] is False and len(r['decision']['checks'])==9
assert load('parent69-retention-and-binder-audit.json')['complete_parent69_Prop_retained'] is True
assert load('source-before-header-order.json')['source_freeze_completed_before_candidate_snapshot'] is True
for n in ['freeze-source','candidate-snapshot','header-review','opaque-priors','finalizer']:
 assert load(n+'.receipt.json')['actual_exit']==0
assert not (out/'lease.final.json').exists()
result=dict(schema='header-source70-readback-and-close-validator-v1',actual_pid=os.getpid(),whole_logical_run_sha256=r['run_sha256'],only_top_level_run_sha256_deleted=True,complete_input_payload_verified=17,complete_named_review_entries_verified=13,all_RAW_LF_exact=True,source_math=419,source_NODE=173,source_EXCLUDED=246,header_lines=116,review_checks=9,complete_parent69_retained=True,source_frozen_before_header=True,statement_repair_required=False,foreground_stages_all_EXIT0=True,no_proof_search_compilation_claim_seal=True)
(out/'readback-validation70.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,sort_keys=True))
