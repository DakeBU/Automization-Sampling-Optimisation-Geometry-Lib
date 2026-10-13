import base64, datetime, hashlib, json, os, pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def item(name,b,role,path):
 lf=b.replace(b'\r\n',b'\n')
 return dict(name=name,source_path=path,semantic_role=role,RAW_bytes=len(b),RAW_sha256=sha(b),
  LF_bytes=len(lf),LF_sha256=sha(lf),LF_transform='replace CRLF byte pair with LF only; preserve every other byte',
  complete_RAW_bytes_base64=base64.b64encode(b).decode('ascii'),complete_LF_bytes_base64=base64.b64encode(lf).decode('ascii'))
source=[]
whole=pathlib.Path(r'E:\Samplinglib\runs\20261007-companion-priority\phase-pbps-gamma-preread57\primary-pbps.exactraw.snapshot.html')
b=whole.read_bytes();assert len(b)==1482128 and sha(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
source.append(item('whole-primary.exact-RAW.html',b,'fixed-primary-root; no whole-paper math inventory claim',str(whole)))
for p in sorted(out.glob('source.*.RAW.html')):
 source.append(item(p.name,p.read_bytes(),'finite-selected-primary-RAW-region',str(p)))
for p in sorted(out.glob('upstream-primary67.*.json')):
 source.append(item(p.name,p.read_bytes(),'opaque-predecessor-provenance-container; non-HTML payload entries and verdicts not decoded or used mathematically',str(p)))
assert len(source)==13
payload=dict(schema='primary69-complete-named-RAW-LF-input-payload-v1',complete_named_inputs=True,
 source_before_candidate69=True,source_semantic_inputs='seven exact primary RAW HTML regions; whole fixed primary bound in full',
 provenance_containers_not_source_hypotheses=True,non_HTML_Lean_entries_in_predecessor_payload_not_decoded=True,
 total_named_input_count=len(source),inputs=source)
put('RAW-input-payload.json',payload)
input_manifest=[{k:v for k,v in x.items() if not k.startswith('complete_')} for x in source]
put('named-input-manifest.json',dict(schema='primary69-named-input-manifest-v1',count=len(input_manifest),
 inputs=input_manifest,inputs_canonical_sha256=sha(canon(input_manifest))))
names=['bounded-synthesis.json','source-proof-graph.json','source-expectations.json','source-directed-algebra-expansion.json',
 'finite-coverage-manifest.json','source-coverage-inventory.json','literal-formulas-and-conditions.json',
 'source-input-regions.json','source-expectations-frozen.json','visibility-and-negative-observations.json',
 'prior-CLOSED59-source-provenance-verification.json','source-read-process.json','B4-consumer-read-process.json']
complete=[]
for name in names:
 b=(out/name).read_bytes(); complete.append(item(name,b,'complete-primary-source-expectation-output',str(out/name)))
named=dict(schema='primary69-complete-named-source-expectation-payload-v1',count=len(complete),complete_outputs=complete,
 candidate69_seen=False,proof_or_completion_claim=False)
put('primary-source-expectation-payload.json',named)
prior_receipts=[]
for p in sorted(out.glob('foreground-*.receipt.json')):
 r=json.loads(p.read_bytes());assert r['actual_exit']==0 and r['completed'] and r['foreground'];prior_receipts.append(r)
run=dict(schema='primary69-whole-logical-source-only-run-v1',owner='/root/independent_primary69',
 mathematical_or_formal_completion_claim=False,candidate69_seen=False,header69_seen=False,
 source_only_before_candidate69=True,actual_finalizer_pid=os.getpid(),finalizer_exit_observed_externally=True,
 named_complete_RAW_LF_input_payload=payload,named_complete_source_expectation_payload=named,
 synthesis=json.loads((out/'bounded-synthesis.json').read_bytes()),
 freeze=json.loads((out/'source-expectations-frozen.json').read_bytes()),
 prior_foreground_actual_terminal_receipts=prior_receipts,
 whole_logical_hash_rule='SHA256(UTF8 json.dumps(copy of this object deleting ONLY its top-level run_sha256, ensure_ascii=False,sort_keys=True,separators=(comma,colon)))')
run['run_sha256']=sha(canon(run));put('review-run.json',run)
put('finalizer-process.json',dict(actual_pid=os.getpid(),actual_exit_observed_in='foreground-finalize.receipt.json',
 whole_logical_run_sha256=run['run_sha256'],RAW_input_sha256=sha((out/'RAW-input-payload.json').read_bytes()),
 complete_named_expectation_payload_sha256=sha((out/'primary-source-expectation-payload.json').read_bytes()),
 finalization_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
put('lease.open.json',dict(schema='primary69-source-only-open-lease-v1',owner='/root/independent_primary69',
 owned_path=str(out),status='OPEN',scope='source expectations only; no Goal/SAU claim or candidate review',
 candidate69_seen=False,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
print(json.dumps(dict(actual_pid=os.getpid(),whole_logical_run_sha256=run['run_sha256'],
 named_input_count=len(source),named_output_count=len(complete),source_math_count=419),sort_keys=True))
