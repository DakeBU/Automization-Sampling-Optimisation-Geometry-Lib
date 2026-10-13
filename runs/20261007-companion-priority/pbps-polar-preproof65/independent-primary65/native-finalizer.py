import os,sys,json,hashlib,datetime,re,html
from pathlib import Path
O=Path(__file__).resolve().parent
P=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(n):return json.loads((O/n).read_text(encoding='utf-8-sig'))
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def logicalhash(v):
 x=dict(v);del x['run_sha256'];return sha(canonical(x))
def checks():
 i=load('source-inputs.json');c=load('source-coverage-inventory.json');g=load('source-proof-graph.json');h=load('residual-next-header.json');p=load('primary-only-review.json');n=load('negative-boundaries.json');raw=P.read_bytes()
 assert sha(raw)==i['primary_raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 assert c['math_count']==280 and len(c['math_items'])==280
 assert c['missing_alttext_count']==c['missing_annotation_count']==c['annotation_mismatch_count']==0
 for r in i['regions']:
  a,b=r['source_raw_byte_range'];blob=raw[a:b];assert blob==(O/(r['name']+'.raw.html')).read_bytes();assert sha(blob)==r['raw_sha256'];lf=blob.replace(b'\r\n',b'\n').replace(b'\r',b'\n');assert lf==(O/(r['name']+'.lf.html')).read_bytes();assert sha(lf)==r['lf_sha256']
 for m in c['math_items']:
  blob=raw[m['raw_byte_start']:m['raw_byte_end_exclusive']];assert sha(blob)==m['raw_math_sha256'];assert html.unescape(re.search(rb'\balttext="([^"]*)"',blob).group(1).decode())==m['alttext'];assert m['annotation_exactly_matches_alttext'] is True;assert m['classification']
 payload=(O/i['named_raw_input_payload']['filename']).read_bytes();assert sha(payload)==i['named_raw_input_payload']['sha256']
 for s in i['named_raw_input_payload']['segment_map']:
  a,b=s['source_byte_range'];assert payload[s['body_byte_start']:s['body_byte_end_exclusive']]==raw[a:b]
 assert g==p['source_graph'] and h==p['residual_next_header']
 assert not g['future65_candidate_or_header_or_Lean_seen'] and not g['mathematical_progress_claim']
 assert h['public_extra_premises']==[] and h['no_new_H1_B13_B14_floor_premise']
 assert p['negative_boundaries']==n and n['candidate_verdict'] is None
 for k in ['candidate_inputs_seen','new_Lean_or_proof','mathematical_progress','SAU_claim','Goal_changed','canonical_Git_ledger_writes','closed64_reopened_or_written','full_Exposition','PURIFIED','whole_paper','surjective_polar_claim','full_root_inverse_claim']:assert n[k] is False,k
 return {'primary_raw_sha256':sha(raw),'region_count':len(i['regions']),'math_count':280,'missing_alttext':0,'annotation_mismatch':0,'all_named_input_segments_exact':True,'source_only_no_candidate':True}
mode=sys.argv[1]
assert not (O/'lease.final.json').exists(),'No writes or finalization after CLOSED_LAST'
result=checks()
if mode=='finalize':
 names=['source-inputs.json','source-coverage-inventory.json','printed-formula-index.json','source-proof-graph.json','residual-next-header.json','primary-only-review.json','negative-boundaries.json','tool-negatives.json','finite-inventory-refinement.json']
 contents={n:load(n) for n in names}
 ordinary={x.name:{'raw_sha256':sha(x.read_bytes()),'raw_bytes':x.stat().st_size,'lf_sha256':sha(x.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n'))} for x in sorted(O.iterdir()) if x.is_file() and x.name not in ['review-run.json','raw-review-binding.json'] and not x.name.startswith('foreground-')}
 run={'schema':'primary65-complete-logical-run-v1','run_sha256':None,'logical_run_hash_rule':'Delete ONLY top-level run_sha256, then UTF8 JSON ensure_ascii=false sort_keys=true separators=(comma,colon), SHA256. No other deletion or selected subset.','full_source_planning_contents':contents,'primary_only_status':'PRIMARY_TOPOLOGY_READY; source/header planning only','actual_foreground_finalizer_pid':os.getpid(),'actual_foreground_runner_pid':os.getppid(),'finalized_utc':now(),'artifacts_at_logical_finalization':ordinary,'complete_named_RAW_REVIEW_payload':{'filename':'review-run.json','scope':'Exact complete raw bytes of this entire review-run.json, no deletion. Full source graph, full280-item coverage, full residual header and negatives are embedded. Distinct from named source INPUT payload.','pin_file':'raw-review-binding.json'},'closure_contract':{'foreground_receipts':['foreground-finalizer.receipt.json','foreground-readback.receipt.json'],'owned_manifest':'owned-manifest.json','last_owned_write':'lease.final.json','final_lease_status':'CLOSED_LAST','postclose_policy':'read-only; terminal stdout capsule externally pins exact manifest and final lease bytes.'}}
 run['run_sha256']=logicalhash(run);write('review-run.json',run);b=(O/'review-run.json').read_bytes();write('raw-review-binding.json',{'schema':'primary65-complete-raw-review-binding-v1','filename':'review-run.json','role':'COMPLETE_NAMED_RAW_REVIEW_PAYLOAD','raw_sha256':sha(b),'raw_bytes':len(b),'deletions':[],'complete_logical_run_sha256':run['run_sha256'],'distinct_named_raw_INPUT_payload':load('source-inputs.json')['named_raw_input_payload']});assert sha(b)!=load('source-inputs.json')['named_raw_input_payload']['sha256'];result.update({'logical_run_sha256':run['run_sha256'],'complete_RAW_REVIEW_sha256':sha(b),'complete_RAW_REVIEW_bytes':len(b)})
elif mode=='readback':
 run=load('review-run.json');assert logicalhash(run)==run['run_sha256'];rb=load('raw-review-binding.json');b=(O/'review-run.json').read_bytes();assert rb['raw_sha256']==sha(b) and rb['raw_bytes']==len(b);assert run['full_source_planning_contents']=={n:load(n) for n in run['full_source_planning_contents']}
 for name,rec in run['artifacts_at_logical_finalization'].items():assert sha((O/name).read_bytes())==rec['raw_sha256'],name
 result.update({'logical_run_sha256':run['run_sha256'],'complete_RAW_REVIEW_sha256':sha(b),'full_logical_run_deleting_only_run_sha256':True,'complete_review_no_deletion':True})
else:raise ValueError(mode)
result.update({'schema':'primary65-foreground-check-v1','mode':mode,'pid':os.getpid(),'ppid':os.getppid(),'completed_utc':now(),'exit_code':0});print(json.dumps(result,ensure_ascii=False,sort_keys=True))
