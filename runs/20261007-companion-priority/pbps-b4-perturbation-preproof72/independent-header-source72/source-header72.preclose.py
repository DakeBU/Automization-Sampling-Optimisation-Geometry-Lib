import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;R=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
for q in json.loads((O/'stageA.owned-finite-manifest72.json').read_bytes())['files']:
 p=B/q['path'];b=p.read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
run=json.loads((O/'source-header72.run.json').read_bytes());assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
for q in run['records']:
 b=(B/q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
decision=json.loads((O/'source-header72.decision.json').read_bytes());assert decision['review_run_sha256']==run['run_sha256']
assert {k:v for k,v in decision.items() if k!='review_run_sha256'}==run['decision_complete']
payloadpath=O/'complete-named-review-decision-input-payload72.json';payload=json.loads(payloadpath.read_bytes())
if payload['complete_native_run']!=run:
 delta=payload['complete_native_run']['decision_complete'].copy();assert delta.pop('review_run_sha256')==run['run_sha256'] and delta==run['decision_complete']
 probe=payload['complete_native_run'].copy();probe['decision_complete']=run['decision_complete'];assert probe==run
 (O/'complete-named-payload72.before-native-run-alias-correction.exactraw.snapshot.json').write_bytes(payloadpath.read_bytes())
 payload['complete_native_run']=run;write(payloadpath.name,payload)
 write('source-header72.payload-serialization-correction.json',{'schema':'source72-native-payload-serialization-observer-correction-v1','actual_pid':os.getpid(),'before':pin(O/'complete-named-payload72.before-native-run-alias-correction.exactraw.snapshot.json'),'after':pin(payloadpath),'only_JSON_change':'Remove unintended complete_native_run.decision_complete.review_run_sha256 key from in-memory aliased copy,so payload complete_native_run is exactly native run on disk. Native run/wholelogical/decision/review/source/header bytes unchanged.','mathematical_repair':False,'historical_before_exact_bytes_retained':True})
 p=O/'stageB-review-headers72.py';s=p.read_text(encoding='utf-8');assert "'complete_native_run':run" in s;s=s.replace("'complete_native_run':run","'complete_native_run':json.loads((O/'source-header72.run.json').read_bytes())");p.write_text(s,encoding='utf-8',newline='\n')
payload=json.loads(payloadpath.read_bytes());assert payload['complete_native_run']==run and payload['complete_decision']==decision and payload['complete_RAW_review_utf8']==(O/'source-header72.review.RAW.md').read_text(encoding='utf-8')
manifest=json.loads((O/'stageB.exact-header-input-manifest72.json').read_bytes())
for q in manifest['inputs']:assert sha((B/q['path']).read_bytes())==q['RAW_sha256']
for q in json.loads((O/'stageA.prior71-readonly-pins72.json').read_bytes())['inputs']:assert sha((B/q['path']).read_bytes())==q['RAW_sha256']
cov=json.loads((O/'stageA.finite-source255-plus-supplemental-coverage72.frozen.json').read_bytes());primary=json.loads((O/'stageA.primary-input-manifest72.json').read_bytes());raw=(B/primary['primary']['path']).read_bytes();assert sha(raw)==primary['primary']['RAW_sha256']
for q in cov['primary_entries']+cov['supplemental_entries']:assert sha(raw[q['RAW_start']:q['RAW_end_exclusive']])==q['RAW_sha256']
ob=json.loads((O/'stageB.all27-source-header-decisions72.json').read_bytes());assert ob['count']==len(ob['entries'])==27 and ob['blocking_count']==0 and not ob['required_repairs']
terminals=[]
for p in sorted(O.glob('*.terminal-receipt.json')):
 q=json.loads(p.read_bytes())
 for k in ['stdout','stderr']:
  x=q[k];b=(O/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256']
 terminals.append({'actual_pid':q['actual_pid'],'exit_code':q['exit_code'],'receipt':pin(p),'foreground':q['foreground']})
write('source-header72.actual-terminal-catalog.json',{'schema':'source72-actual-terminal-catalog-v1','entries':terminals,'negative_inline_and_PowerShell_parse_observers':'Separate exactnegative records; no childPID invented.','final_preclose_and_close_receipts_join_finalmanifest':True})
inputmanifest={'schema':'source72-small-complete-input-layers-v1','primary_input_manifest':pin(O/'stageA.primary-input-manifest72.json'),'primary_inventory255':pin(O/'stageA.primary255.independent-inventory72.json'),'B1_supplement74':pin(O/'stageA.supplement-B1-framework.inventory72.json'),'B2_domain27':pin(O/'stageA.supplement-B2-domain.inventory72.json'),'B2_root5_in_discovery':pin(O/'stageA.supplementary-discovery72.json'),'complete_unique_source_classification361':pin(O/'stageA.finite-source255-plus-supplemental-coverage72.frozen.json'),'prior_immutable_native_pins':pin(O/'stageA.prior71-readonly-pins72.json'),'exact_two_candidate_and_parent_manifest':pin(O/'stageB.exact-header-input-manifest72.json'),'all_source_math_elements_RAW_offsets_and_hashes_verified':361,'candidate_and_parent_input_paths':3,'LF_recipe':'ONLY byteCRLF toLF; no othernormalization','no_recursive_historical_payload':True};write('source-header72.complete-input-layer-manifest.json',inputmanifest)
payload['complete_input_layer_manifest']=inputmanifest;payload['complete_input_layer_manifest_RAW_LF']=pin(O/'source-header72.complete-input-layer-manifest.json');payload['actual_terminal_catalog_RAW_LF']=pin(O/'source-header72.actual-terminal-catalog.json');write(payloadpath.name,payload)
report={'schema':'source72-preclose-verification-v1','actual_pid':os.getpid(),'status':'PASS_PRE_CLOSE','StageA207manifest_files_unchanged':207,'source_items_verified':361,'all27obligations_compared':True,'both_exact_headers_and_current_parent_pins_unchanged':True,'same6callers12witnesses_completeparent':True,'whole_logical_run_sha256':run['run_sha256'],'decision':pin(O/'source-header72.decision.json'),'full_RAW_review':pin(O/'source-header72.review.RAW.md'),'named_payload':pin(payloadpath),'input_layers':pin(O/'source-header72.complete-input-layer-manifest.json'),'no_mathrepair_noBODYcompile_sourceimplementationorVERIFIED_credit':True};write('source-header72.preclose-verification.json',report);print(json.dumps(report,indent=2))
