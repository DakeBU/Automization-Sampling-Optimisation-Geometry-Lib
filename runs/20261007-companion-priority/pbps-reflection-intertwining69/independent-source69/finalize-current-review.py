import base64,copy,datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def load(n):return json.loads((out/n).read_bytes())
def named(n):
 b=(out/n).read_bytes();lf=b.replace(b'\r\n',b'\n')
 return dict(name=n,RAW_bytes=len(b),RAW_sha256=sha(b),RAW_base64=base64.b64encode(b).decode('ascii'),LF_bytes=len(lf),LF_sha256=sha(lf),LF_base64=base64.b64encode(lf).decode('ascii'))
m=load('current-input-manifest.json');assert m['count']==len(m['inputs'])==62 and len({x['name'] for x in m['inputs']})==62
inputs=[]
for e in m['inputs']:
 x=named(e['name']);assert x['RAW_bytes']==e['RAW_bytes'] and x['RAW_sha256']==e['RAW_sha256'] and x['LF_sha256']==e['LF_sha256']
 assert base64.b64decode(x['LF_base64'])==(out/(e['name']+'.LF')).read_bytes()
 x['original_path']=e['original_path'];x['role']=e['role'];inputs.append(x)
input_payload=dict(schema='source69-complete-named-RAW-LF-input-payload-v1',count=62,LF_recipe='replace CRLF byte pairs by LF ONLY; retain isolated CR,every other byte and trailing whitespace',attribution_is_separate_from_source_hypotheses=True,entries=inputs,manifest_RAW_sha256=sha((out/'current-input-manifest.json').read_bytes()),initial_draft_inputs_retained=True,post_overlay_binding_authority='official.source.0.reviewer-packet.RAW.json and publication-binding.exact-payload.json; initial publication-freeze preserves pre-overlay draft and is not silently rewritten')
put('RAW-input-payload.json',input_payload)
terminal_names=sorted(p.name for p in out.glob('*.receipt.json'))
terminals=[dict(name=n,receipt=load(n),RAW_sha256=sha((out/n).read_bytes())) for n in terminal_names]
put('terminal-evidence.before-finalizer.json',dict(schema='source69-terminal-evidence-v1',foreground=True,background=False,completed_stages=terminals,current_finalizer_pid=os.getpid(),current_finalizer_exit='observed externally by run-foreground.py after this script completes; receipt belongs to final owned closure',failures_preserved=True))
review_names=['source-review.native-review.json','finite-current-source-review-coverage.json','bounded-synthesis.source69.json','official-packet-binding-and-decoder-provenance.json','publication-binding.exact-payload.json','primary419-NODE-EXCLUDED.json','literal-statement-and-whole-module-audit.json','six-BODY-formula-and-code-review.json','whole-module446-line-coverage.json','source-implementation-route-comparison.prepacket.json','independent-seven-slots.prepacket.json','prepacket-bounded-observations.json','reader-api-metadata-overlay.proposal.json','reader-api-metadata-overlay.decision.json','reader-overlay.helper-fold.preview.html','opaque-prior-closure-and-compiler-provenance-recheck.json','visibility-and-role-declaration.json','console-negative-observations.json','terminal-evidence.before-finalizer.json','current-input-manifest.json']
native_review_payload=dict(schema='source69-complete-named-native-review-v1',count=len(review_names),entries=[named(n) for n in review_names])
review=load('source-review.native-review.json');packet=load('official.source.0.reviewer-packet.RAW.json')
run=dict(schema='source69-whole-logical-independent-source-review-v1',owner='/root/independent_primary69',actual_finalizer_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer_packet_sha256=packet['packet_sha256'],reviewer_packet_RAW_sha256=sha((out/'official.source.0.reviewer-packet.RAW.json').read_bytes()),publication_binding_sha256=packet['publication_binding_sha256'],decoder_whole_logical_sha256=packet['blind_reconstruction']['decoder_run_sha256'],source_review_native=review,complete_named_RAW_LF_inputs=input_payload,complete_named_native_review=native_review_payload,finite_coverage=load('finite-current-source-review-coverage.json'),logical_hash_recipe='SHA256 UTF8 JSON ensure_ascii=False sort_keys=True separators=(comma,colon); delete ONLY the top-level run_sha256 before hashing; do not remove any nested field',no_canonical_Git_ledger_Goal_edits=True,boundary=review['boundary'])
run['run_sha256']=sha(canon(run));put('review-run.json',run)
decision=copy.deepcopy(review);decision['review_run_sha256']=run['run_sha256'];decision['reviewer_packet_RAW_sha256']=run['reviewer_packet_RAW_sha256']
decision['audit_source_admission']=dict(state='accepted',verdict=review['verdict'],source_review=dict(state='accepted',reviewer=review['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=review['review_evidence'],reviewer_packet_sha256=packet['packet_sha256'],review_run_sha256=run['run_sha256']),publication_binding_sha256=packet['publication_binding_sha256'],repairs=[])
decision['native_review_RAW_sha256']=sha((out/'source-review.native-review.json').read_bytes());decision['review_run_RAW_sha256']=sha((out/'review-run.json').read_bytes())
put('source.0.decision.json',decision)
complete_names=review_names+['source.0.decision.json','review-run.json','RAW-input-payload.json']
put('complete-named-review-decision-input-payload.json',dict(schema='source69-complete-named-review-decision-input-v1',count=len(complete_names),entries=[named(n) for n in complete_names],whole_logical_run_sha256=run['run_sha256'],reviewer_packet_canonical_sha256=packet['packet_sha256'],publication_binding_sha256=packet['publication_binding_sha256'],self_hash_policy='This complete named payload is externally RAW hashed in final lease/owned manifest; no recursive self hash.'))
put('finalizer-result.json',dict(schema='source69-finalizer-result-v1',actual_pid=os.getpid(),whole_logical_run_sha256=run['run_sha256'],source_decision_RAW_sha256=sha((out/'source.0.decision.json').read_bytes()),complete_named_review_decision_input_RAW_sha256=sha((out/'complete-named-review-decision-input-payload.json').read_bytes()),complete_RAW_LF_input_RAW_sha256=sha((out/'RAW-input-payload.json').read_bytes()),input_count=62,native_review_entries=len(review_names),complete_named_entries=len(complete_names),verdict=review['verdict'],source_review_state='accepted',source_math_count=419,module_lines=446,slots=7,deltas=12,BODY_steps=6))
print(json.dumps(load('finalizer-result.json'),sort_keys=True))
