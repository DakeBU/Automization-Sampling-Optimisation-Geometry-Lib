import os,sys,json,hashlib,datetime,re
from pathlib import Path
O=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(n):return json.loads((O/n).read_text(encoding='utf-8-sig'))
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def logicalhash(v):
 x=dict(v);del x['run_sha256'];return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def checks():
 s=load('source-first-seal.json');ci=load('candidate-inputs.json');mi=load('inputs.manifest.json');ei=load('finite-evidence-inputs.json');assert not s['candidate_read_before_this_seal'];assert s['source_read_end_utc']<ci['first_candidate_read_start_utc'];assert ci['source_first_seal_raw_sha256']==sha((O/'source-first-seal.json').read_bytes())
 for x in s['source_snapshot_bindings']:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'] and sha((O/x['snapshot']).read_bytes())==x['raw_sha256']
 for x in ci['inputs']:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'] and sha((O/x['raw_snapshot']).read_bytes())==x['raw_sha256']
 p=(O/'complete-inputs.named.raw.payload').read_bytes();assert sha(p)==mi['complete_named_RAW_INPUT_payload']['raw_sha256'];assert len(p)==mi['complete_named_RAW_INPUT_payload']['raw_bytes'];assert mi['total_named_inputs']==len(mi['inputs'])==32
 for x in mi['inputs']:
  b=(O/x['raw_snapshot']).read_bytes();assert sha(b)==x['raw_sha256'];assert sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==x['lf_sha256'];assert p[x['payload_body_byte_start']:x['payload_body_byte_end_exclusive']]==b
 for x in ei['inputs']:assert sha(Path(x['source_path']).read_bytes())==x['source_full_raw_sha256']
 a=load('binder-definition-audit.json');assert len(a['public_binders'])==15 and len(a['internal_lets'])==25 and len(a['produced_existential_witnesses'])==10;assert a['unmatched_public_binders']==[]
 c=load('source-first.source-coverage-inventory.json');assert c['math_count']==len(c['math_items'])==280 and c['missing_alttext_count']==c['annotation_mismatch_count']==0
 r=load('header-review.json');assert r['status']=='TWO_HEADERS_ACCEPTED_ONLY_UNPROVED'
 slots={'objects','domains','quantifiers','assumptions','conclusion','scopes_senses','constant_dependencies'}
 for k in [0,1]:
  d=load('decision.'+str(k)+'.json');assert r['native_decisions'][k]==d;assert set(d['semantic_slots'])==slots and d['repairs']==d['deltas']==[] and d['header_admission']=='ACCEPT_HEADER_ONLY';assert not d['truth_boundary']['theorem_compiled'] and not d['truth_boundary']['compiler_PASS'] and not d['truth_boundary']['proof_search'];assert d['compiler_evidence']['actual_Lean_exit_code']==1 and d['compiler_evidence']['all_errors_at_or_after_BODY']
 assert ei['baseline64_input_binders_byte_identical'] and ei['inherited_prefix_through_Inv_byte_identical_after_removing_ONLY_internal_HP0_CompleteSpace_let'] and ei['candidate_header_exactly_matches_full_file_before_BODY']
 return {'source_first_sequence_verified':True,'all32_input_RAW_LF_maps_verified':True,'source_inventory_math_items':280,'two_complete_seven_slot_header_decisions':True,'no_proof_or_compiler_PASS':True}
mode=sys.argv[1];assert not (O/'lease.final.json').exists();out=checks()
if mode=='finalize':
 names=['source-first-seal.json','source-first.source-proof-graph.json','source-first.source-coverage-inventory.json','source-first.residual-next-header.json','source-first.negative-boundaries.json','candidate-inputs.json','finite-evidence-inputs.json','inputs.manifest.json','binder-definition-audit.json','source-ingredient-DAG-audit.json','consumer-audit.json','header-review.json','decision.0.json','decision.1.json','negative-boundaries.json']
 run={'schema':'header65-complete-logical-review-run-v1','run_sha256':None,'run_hash_rule':'Delete ONLY top-level run_sha256; UTF8 JSON ensure_ascii=false sort_keys=true separators=(comma,colon); SHA256; no other deletion.','full_logical_contents':{n:load(n) for n in names},'native_decisions':[load('decision.'+str(k)+'.json') for k in [0,1]],'actual_foreground_finalizer_pid':os.getpid(),'actual_runner_pid':os.getppid(),'finalized_utc':now(),'status':'HEADER_ONLY_ACCEPTED_BODIES_UNPROVED','complete_named_RAW_REVIEW_payload':{'filename':'review-run.json','designation':'Exact complete raw bytes, no deletion; all full seven-slot decisions, binder/definition audit, source graph/inventory, finite evidence and negative boundaries included.','pin_file':'raw-review-binding.json'},'closure_files':['foreground-finalizer.receipt.json','foreground-readback.receipt.json','owned-manifest.json','lease.final.json'],'final_lease_contract':'CLOSED_LAST then read-only'}
 run['run_sha256']=logicalhash(run);write('review-run.json',run);b=(O/'review-run.json').read_bytes();raw={'schema':'header65-complete-named-raw-review-binding-v1','filename':'review-run.json','role':'COMPLETE_NAMED_RAW_REVIEW_PAYLOAD','raw_sha256':sha(b),'raw_bytes':len(b),'deletions':[],'logical_run_sha256':run['run_sha256'],'separate_complete_named_RAW_INPUT_payload':load('inputs.manifest.json')['complete_named_RAW_INPUT_payload']};assert raw['raw_sha256']!=raw['separate_complete_named_RAW_INPUT_payload']['raw_sha256'];write('raw-review-binding.json',raw);out.update({'run_sha256':run['run_sha256'],'complete_RAW_REVIEW_sha256':sha(b),'complete_RAW_REVIEW_bytes':len(b)})
elif mode=='readback':
 r=load('review-run.json');rb=load('raw-review-binding.json');b=(O/'review-run.json').read_bytes();assert logicalhash(r)==r['run_sha256'] and sha(b)==rb['raw_sha256'] and len(b)==rb['raw_bytes'];assert r['full_logical_contents']=={n:load(n) for n in r['full_logical_contents']};assert r['native_decisions']==[load('decision.'+str(k)+'.json') for k in [0,1]];out.update({'run_sha256':r['run_sha256'],'complete_RAW_REVIEW_sha256':sha(b),'hash_rule_deletes_only_top_level_run_sha256':True,'RAW_REVIEW_no_deletion':True})
else:raise ValueError(mode)
out.update({'schema':'header65-foreground-check-v1','role':mode,'actual_pid':os.getpid(),'actual_parent_pid':os.getppid(),'exit_code':0,'completed_utc':now()});print(json.dumps(out,ensure_ascii=False,sort_keys=True))
