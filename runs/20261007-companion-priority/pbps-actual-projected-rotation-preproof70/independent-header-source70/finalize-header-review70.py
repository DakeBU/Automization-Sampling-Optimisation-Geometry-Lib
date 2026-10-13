import base64,copy,datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def load(n):return json.loads((out/n).read_bytes())
def named(n):
 b=(out/n).read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(name=n,RAW_bytes=len(b),RAW_sha256=sha(b),RAW_base64=base64.b64encode(b).decode('ascii'),LF_bytes=len(lf),LF_sha256=sha(lf),LF_base64=base64.b64encode(lf).decode('ascii'))
m=load('input-manifest.json');assert m['count']==len(m['inputs'])==17
inputs=[]
for x in m['inputs']:
 e=named(x['name']);assert e['RAW_sha256']==x['RAW_sha256'] and e['LF_sha256']==x['LF_sha256']
 assert base64.b64decode(e['LF_base64'])==(out/(x['name']+'.LF')).read_bytes()
 for k in ['original_path','role','source_RAW_range_end_exclusive']:
  if k in x:e[k]=x[k]
 inputs.append(e)
inp=dict(schema='header-source70-complete-exact-RAW-LF-input-v1',count=17,LF_recipe='CRLF byte pairs to LF ONLY; preserve every other byte',entries=inputs,attribution_and_provenance_are_not_source_hypotheses=True)
put('RAW-input-payload.json',inp)
names=['source-expectations70.before-header.json','mean-g-source-and-internal-completion70.json','source-before-header-order.json','parent69.literal-Prop.fragment-map.json','parent69-retention-and-binder-audit.json','primary419-NODE-EXCLUDED70.json','header-line-coverage70.json','independent-header-source70.decision.json','bounded-synthesis70.json','opaque-prior-closures70.json','input-manifest.json','source.actual-reflection-invariance.context.exactraw.html.text.txt','source.actual-projected-rotation.context.exactraw.html.text.txt']
review=dict(schema='header-source70-complete-named-review-v1',count=len(names),entries=[named(n) for n in names])
put('complete-named-review70.json',review)
decision=load('independent-header-source70.decision.json')
terminals=[dict(name=p.name,receipt=json.loads(p.read_bytes())) for p in sorted(out.glob('*.receipt.json'))]
run=dict(schema='header-source70-whole-logical-native-review-v1',owner='/root/independent_primary69',actual_finalizer_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),decision=decision,complete_named_review=review,complete_exact_RAW_LF_inputs=inp,terminal_receipts_before_finalizer=terminals,logical_hash_recipe='SHA256 UTF8 canonical JSON ensure_ascii=False sort_keys=True separators=(comma,colon), deleting ONLY top-level run_sha256; retain every nested field',scope='Header/source/binder/definition-only; no proof search,compilation,claim,seal,SAUverification or whole-paper completion.',no_canonical_Git_ledger_Goal_edits=True)
run['run_sha256']=sha(canon(run));put('review-run.json',run)
put('finite-coverage-manifest70.json',dict(schema='header-source70-finite-coverage-manifest-v1',input_count=17,input_names=[x['name'] for x in m['inputs']],source_math=419,source_NODE=173,source_EXCLUDED=246,source_unclassified=0,source_regions=7,source_graph_nodes=22,source_graph_edges=49,source_entries_canonical_sha256=load('primary419-NODE-EXCLUDED70.json')['entries_canonical_sha256'],header_lines=116,header_unclassified=0,header_entries_canonical_sha256=load('header-line-coverage70.json')['entries_canonical_sha256'],public_analytic_conditions=6,common_witnesses=12,per_f_witnesses=['fP','gP'],individual_review_checks=9,statement_repairs=0,proof_search_or_compilation=False,source_frozen_before_candidate=True,whole_logical_run_sha256=run['run_sha256']))
result=dict(schema='header-source70-finalizer-result-v1',actual_pid=os.getpid(),whole_logical_run_sha256=run['run_sha256'],complete_named_review_RAW_sha256=sha((out/'complete-named-review70.json').read_bytes()),RAW_LF_input_RAW_sha256=sha((out/'RAW-input-payload.json').read_bytes()),decision_RAW_sha256=sha((out/'independent-header-source70.decision.json').read_bytes()),finite_coverage_RAW_sha256=sha((out/'finite-coverage-manifest70.json').read_bytes()),input_count=17,verdict=decision['verdict'],statement_repair_required=False)
put('finalizer-result70.json',result);print(json.dumps(result,sort_keys=True))
