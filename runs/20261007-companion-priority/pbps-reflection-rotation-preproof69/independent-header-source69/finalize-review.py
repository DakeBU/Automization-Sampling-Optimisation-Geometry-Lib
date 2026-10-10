import base64,datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def item(name,b,role):
 lf=b.replace(b'\r\n',b'\n')
 return dict(name=name,role=role,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf),
  complete_RAW_bytes_base64=base64.b64encode(b).decode('ascii'),complete_LF_bytes_base64=base64.b64encode(lf).decode('ascii'))
manifest=json.loads((out/'current-input-manifest.json').read_bytes())
inputs=[]
for x in manifest['inputs']:
 b=(out/x['name']).read_bytes();assert sha(b)==x['RAW_sha256']
 inputs.append(dict(item(x['name'],b,x['role']),original_path=x['original_path']))
assert len(inputs)==22
payload=dict(schema='header-source69-complete-named-RAW-LF-input-payload-v1',count=22,inputs=inputs,
 complete_named_inputs=True,LF_transform='CRLF to LF only',candidate_inputs_header_only=True,
 source_expectations_precede_candidate=True,parent_full_body_excluded=True,prior_CLOSED82_never_written=True)
put('RAW-input-payload.json',payload)
names=['header-source-decision.json','binder-and-definition-audit.json','exact-parent-continuity.json',
 'finite-coverage-manifest.json','bounded-synthesis.json','new-D-semantics-and-intertwining.exact-RAW.fragment.lean',
 'current-input-manifest.json','input-read-process.json']
outputs=[item(n,(out/n).read_bytes(),'complete-independent-header-source-review-output') for n in names]
review=dict(schema='header-source69-complete-named-RAW-review-payload-v1',count=len(outputs),outputs=outputs,
 header_only=True,proof_or_compilation_claim=False)
put('RAW-review-payload.json',review)
receipts=[]
for p in sorted(out.glob('foreground-*.receipt.json')):
 r=json.loads(p.read_bytes());assert r['actual_exit']==0 and r['completed'] and r['foreground'];receipts.append(r)
run=dict(schema='header-source69-complete-logical-review-run-v1',owner='/root/independent_primary69',
 actual_finalizer_pid=os.getpid(),complete_named_RAW_LF_input_payload=payload,complete_named_RAW_review_payload=review,
 verdict=json.loads((out/'header-source-decision.json').read_bytes())['verdict'],
 source_first=True,candidate_header_only=True,prior_CLOSED82_written=False,no_68_reviews_or_decoders_or_bodies=True,
 proof_or_compilation_claim=False,Statement_Seal=False,SAU_claim=False,whole_result_claim=False,
 actual_prior_foreground_terminals=receipts,
 whole_logical_hash_rule='SHA256 canonical UTF8 JSON deleting ONLY top-level run_sha256; sort_keys=True,ensure_ascii=False,separators=(comma,colon)')
run['run_sha256']=sha(canon(run));put('review-run.json',run)
put('finalizer-process.json',dict(actual_pid=os.getpid(),whole_logical_run_sha256=run['run_sha256'],
 finalization_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_observed_in='foreground-finalize.receipt.json'))
print(json.dumps(dict(actual_pid=os.getpid(),whole_logical_run_sha256=run['run_sha256'],named_inputs=22,named_outputs=len(outputs)),sort_keys=True))
