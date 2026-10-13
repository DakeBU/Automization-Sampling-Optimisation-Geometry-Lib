import os,sys,json,hashlib,datetime
from pathlib import Path
O=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((O/n).read_text(encoding='utf-8-sig'))
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def logicalhash(v):
 x=dict(v);del x['run_sha256'];return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def diff(x,y,p=''):
 if type(x)!=type(y):return [p]
 if isinstance(x,dict):
  out=[]
  for k in sorted(set(x)|set(y)):
   if k not in x or k not in y:out.append(p+'.'+k)
   else:out+=diff(x[k],y[k],p+'.'+k)
  return out
 return [] if x==y else [p]
def checks():
 m=load('inputs.manifest.json');p=(O/'complete-inputs.named.raw.payload').read_bytes();assert len(m['inputs'])==m['finite_named_input_count']==14;assert sha(p)==m['complete_named_RAW_INPUT_payload']['raw_sha256']
 for x in m['inputs']:
  b=(O/x['raw_snapshot']).read_bytes();assert b==Path(x['source_path']).read_bytes() and sha(b)==x['raw_sha256'] and len(b)==x['raw_bytes'];lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');assert lf==(O/x['LF_snapshot']).read_bytes() and sha(lf)==x['LF_sha256'];assert p[x['payload_body_byte_start']:x['payload_body_byte_end_exclusive']]==b
 before=load('before.raw.json');after=load('proposed-after.raw.json');assert diff(before,after)==['.evidence.truth_boundary','.source_anchor'];assert (O/'before.raw.json').read_bytes()==(O/'canonical-cell.raw.json').read_bytes();d=load('decision.json');assert d['overlay_decision']=='ACCEPT_EXACT_TWO_FIELD_METADATA_OVERLAY' and d['repairs']==[] and not d['source_mathematical_repair'] and not d['canonical_apply_performed'];assert set(d['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes_senses','constant_dependencies'};f=load('finite-diff-checks.json');assert d['deltas']==f['full_recursive_diff'];assert d['reviewed_proposed_after_RAW_sha256']==sha((O/'proposed-after.raw.json').read_bytes());assert d['required_before_RAW_sha256']==sha((O/'before.raw.json').read_bytes())
 audit=load('canonical-audit.raw.json');pub=load('canonical-publication.raw.json')['items'][0];lesson=load('canonical-lesson.raw.json')['units'][0];bp=dict(audit['publication_context']);bp.pop('candidate_assumptions');bp['binding']={k:v for k,v in pub['bindings'][0].items() if k not in {'audit_id','legacy_audit_debt'}};bp['lesson']=lesson;assert sha(json.dumps(bp,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==audit['publication_binding_sha256']==d['publication_binding_sha256']
 for x in f['science_file_hash_checks']:assert sha(Path(x['path']).read_bytes())==x['raw_sha256']
 n=load('negative-boundaries.json');assert d['truth_boundary']==n and all(n[k] is False for k in ['compiler_run','source_mathematical_repair','canonical_applied_by_reviewer','Git_ledger_SAU_Goal_change','closed_scopes_mutated_or_reactivated','full_Exposition','PURIFIED','main_or_merged_or_live','whole_paper_or_composition'])
 return {'exact_two_field_recursive_diff':True,'finite14_input_RAW_LF_maps_verified':True,'seven_complete_semantic_slots':True,'canonical_publication_binding_verified':True,'no_compiler_or_math_change':True,'canonical_before_still_unchanged':True}
mode=sys.argv[1];assert not (O/'lease.final.json').exists();out=checks()
if mode=='finalize':
 mi=load('inputs.manifest.json');names=['decision.json','finite-diff-checks.json','negative-boundaries.json','inputs.manifest.json'];logicalinputs={x['name']:load(x['raw_snapshot']) for x in mi['inputs'] if x['name']!='publication-binding-implementation'}
 r={'schema':'stale-cell-overlay64-complete-logical-run-v1','run_sha256':None,'whole_logical_hash_rule':'Delete ONLY top-level run_sha256; UTF8 JSON ensure_ascii=false sort_keys=true separators=(comma,colon); SHA256; no subset or other deletion.','full_logical_contents':{n:load(n) for n in names},'full_finite_JSON_inputs':logicalinputs,'native_decision':load('decision.json'),'actual_foreground_finalizer_pid':os.getpid(),'actual_runner_pid':os.getppid(),'finalized_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'complete_named_RAW_DECISION_payload':{'filename':'decision.json','scope':'Exact complete RAW bytes including all seven semantic slots, deltas, verdict, repairs, status and exclusions; no deletion.'},'complete_named_RAW_REVIEW_payload':{'filename':'review-run.json','scope':'Exact complete RAW bytes of this logical run; no deletion.'},'terminal_closure_files':['foreground-finalizer.receipt.json','foreground-readback.receipt.json','owned-manifest.json','lease.final.json'],'postclose':'CLOSED_LAST then immutable read-only'};r['run_sha256']=logicalhash(r);write('review-run.json',r);db=(O/'decision.json').read_bytes();rb=(O/'review-run.json').read_bytes();v={'schema':'stale-cell-overlay64-complete-RAW-payload-bindings-v1','logical_run_sha256':r['run_sha256'],'complete_named_RAW_DECISION':{'filename':'decision.json','raw_bytes':len(db),'raw_sha256':sha(db),'deletions':[]},'complete_named_RAW_REVIEW':{'filename':'review-run.json','raw_bytes':len(rb),'raw_sha256':sha(rb),'deletions':[]},'separate_complete_named_RAW_INPUT':mi['complete_named_RAW_INPUT_payload']};assert len({sha(db),sha(rb),mi['complete_named_RAW_INPUT_payload']['raw_sha256']})==3;write('raw-payload-bindings.json',v);out.update({'logical_run_sha256':r['run_sha256'],'complete_RAW_DECISION_sha256':sha(db),'complete_RAW_REVIEW_sha256':sha(rb),'RAW_REVIEW_bytes':len(rb)})
elif mode=='readback':
 r=load('review-run.json');v=load('raw-payload-bindings.json');assert logicalhash(r)==r['run_sha256'];assert r['native_decision']==load('decision.json');assert r['full_logical_contents']=={n:load(n) for n in r['full_logical_contents']}
 for k in ['complete_named_RAW_DECISION','complete_named_RAW_REVIEW']:
  z=v[k];b=(O/z['filename']).read_bytes();assert sha(b)==z['raw_sha256'] and len(b)==z['raw_bytes'] and z['deletions']==[]
 out.update({'logical_run_sha256':r['run_sha256'],'RAW_payloads_no_deletion':True,'whole_logical_run_deletes_ONLY_top_level_run_sha256':True})
else:raise ValueError(mode)
out.update({'schema':'stale-cell-overlay64-foreground-check-v1','role':mode,'actual_pid':os.getpid(),'actual_parent_pid':os.getppid(),'exit_code':0,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});print(json.dumps(out,ensure_ascii=False,sort_keys=True))
