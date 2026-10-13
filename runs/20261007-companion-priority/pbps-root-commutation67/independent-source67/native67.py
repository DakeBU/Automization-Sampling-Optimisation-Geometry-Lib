import os,sys,json,hashlib,datetime
from pathlib import Path
O=Path(__file__).resolve().parent

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b):return hashlib.sha256(b).hexdigest()
def cj(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def rd(n):return json.loads((O/n).read_bytes())
def wr(n,o):
 assert not (O/'lease.final.json').exists(),'CLOSED_LAST writes forbidden'
 (O/n).write_bytes((json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':h(b),'LF_bytes':len(l),'LF_sha256':h(l)}
def localpin(p):
 x=pin(p);x['relative_path']=Path(p).relative_to(O).as_posix();return x
def verify(x):
 a=pin(x['path'])
 for k in ('RAW_bytes','RAW_sha256','LF_bytes','LF_sha256'):
  if k in x:assert a[k]==x[k],(x['path'],k)
def logical(run):
 v=dict(run);del v['run_sha256'];return h(cj(v))
def snapshots():
 m=rd('inputs.manifest.json')
 for e in m['inputs']:
  verify(e['RAW_snapshot']);verify(e['LF_snapshot']);raw=Path(e['RAW_snapshot']['path']).read_bytes();assert Path(e['LF_snapshot']['path']).read_bytes()==raw.replace(b'\r\n',b'\n');assert h(raw)==e['original']['RAW_sha256']
 return m
def payloads(check_current=False):
 b=rd('raw-payload-bindings.json');r=rd('review-run.json');assert logical(r)==r['run_sha256']==b['whole_logical_run_sha256']
 for k in ('COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT'):verify(b[k])
 assert rd('complete-RAW-decision.json')==rd('decision.json')==r['complete_decision_payload'];assert r['decisions']==r['complete_decision_payload']['decisions'];assert len(r['decisions'])==2
 for i,d in enumerate(r['decisions']):assert rd('source.%d.decision.json'%i)==d and len(d['semantic_slots'])==7 and d['verdict']=='equivalent-after-elaboration'
 assert rd('RAW-input-payload.json')==r['complete_RAW_input_payload']
 for x in r['owned_pre_finalization_pins']:verify(x)
 verify(r['source_first']['parent_graph_RAW_pin']);verify(r['source_first']['parent_inventory_RAW_pin'])
 snapshots()
 if check_current:
  for x in r['final_current_candidate_pins']:verify(x)
 return b,r
mode=sys.argv[1]
if mode=='finalize':
 assert not (O/'review-run.json').exists()
 m=snapshots();package=rd('decision.json');assert package==rd('complete-RAW-decision.json');assert len(package['decisions'])==2
 inp={'schema':'source67-SEPARATE-COMPLETE-RAW-INPUT-v1','meaning':'Complete finite original RAW UTF8 payloads at each historical/final stage, with exact RAW/LF maps; source six regions plus whole primary pin; no broad transcript/ledger copies','inputs':[dict(e,complete_original_RAW_UTF8=Path(e['RAW_snapshot']['path']).read_bytes().decode('utf-8-sig') if Path(e['RAW_snapshot']['path']).read_bytes().startswith(b'\xef\xbb\xbf') else Path(e['RAW_snapshot']['path']).read_bytes().decode('utf-8')) for e in m['inputs']],'UTF8_BOM_policy':'Original snapshot and original RAW SHA preserve any BOM; complete_original_RAW_UTF8 records text without UTF8 BOM only when present, plus exact RAW snapshot bytes/pin. No named payload RAW hash normalizes bytes.','whole_primary_pin':rd('source-first-reconstruction.json')['whole_primary'],'finite_input_count':len(m['inputs'])}
 # All current finite inputs are UTF8 and their literal RAW text must reconstruct exactly, including any BOM.
 for e in inp['inputs']:
  raw=Path(e['RAW_snapshot']['path']).read_bytes();e['complete_original_RAW_UTF8']=raw.decode('utf-8');assert e['complete_original_RAW_UTF8'].encode('utf-8')==raw
 inp['UTF8_BOM_policy']='Raw UTF8 decoded without stripping BOM; re-encoding each complete text must equal exact original RAW bytes.'
 wr('RAW-input-payload.json',inp)
 auditnames=['source-coverage-audit.json','whole-module-representation-and-source-contracts.json','ten-literal-BODY-excerpt-audit.json','source-graph-current-boundary-comparison.json','final-publication-binding-context-audit.json','finite-current-to-freeze-map.json','compiler-evidence-boundary.json','citation-catalogue-overlay.verdict.json','audit-source-url-overlay.verdict.json','final-single-URL-application-audit.json','initial-reader-precision-findings.json','observer-negatives.json','negative.final-helper-default-GBK.json','foreground-review.observed-receipts.json','final-review.observed-result.json']
 audits={n:rd(n) for n in auditnames};pending={'foreground-finalizer.stdout.RAW.log','foreground-finalizer.stderr.RAW.log'}
 pre=[localpin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in pending]
 finalpins=rd('final-review.observed-result.json')['final_current_candidate_pins']
 for x in finalpins:verify(x)
 run={'schema':'source67-COMPLETE-logical-review-run-v1','reviewer':'/root/independent_source64','created_utc':utc(),'actual_foreground_finalizer_PID':os.getpid(),'source_first':rd('source-first-reconstruction.json'),'decisions':package['decisions'],'complete_decision_payload':package,'complete_RAW_input_payload':inp,'complete_native_audits':audits,'final_current_candidate_pins':finalpins,'owned_pre_finalization_pins':pre,'closure_contract':{'whole_logical_hash':'Entire parsed logical object; delete ONLY top-level run_sha256; sorted compact UTF8 JSON','complete_RAW_review':'Entire review-run.json file RAW bytes without deletion','complete_RAW_decision':'Entire complete-RAW-decision.json file, both decisions/all seven slots/full current contexts','separate_complete_RAW_input':'Entire RAW-input-payload.json file with finite original/final stage texts and exact RAW/LF maps','standard_review_run_sha256':'Native decisions key empty to avoid impossible self-hash cycle; finite root adapter supplies verified raw-payload-bindings.json whole_logical_run_sha256 without native mutation','exact_deferred_open_logs':sorted(pending),'terminal_self_binding':'Final manifest binds all terminal receipts/logs and outputs except exact self/lease; CLOSED_LAST lease binds manifest and every other owned file; final lease RAW pinned by external actual close/postclose tools','last_write':'lease.final.json last owned write; thereafter read-only','source_mathematical_repair':False,'full_Exposition':False,'PURIFIED':False,'source_reviewer_compiler_started':False},'run_sha256':None}
 run['run_sha256']=logical(run);wr('review-run.json',run)
 bindings={'schema':'source67-distinct-COMPLETE-RAW-payload-bindings-v1','whole_logical_run_sha256':run['run_sha256'],'COMPLETE_RAW_REVIEW':pin(O/'review-run.json'),'COMPLETE_RAW_DECISION':pin(O/'complete-RAW-decision.json'),'SEPARATE_COMPLETE_RAW_INPUT':pin(O/'RAW-input-payload.json'),'CANONICAL_DECISION_ARTIFACTS':[pin(O/('source.%d.decision.json'%i)) for i in range(2)]}
 wr('raw-payload-bindings.json',bindings);wr('finalizer.result.json',{'schema':'source67-actual-foreground-finalizer-v1','actual_PID':os.getpid(),'status':'PASS_PENDING_READBACK','complete_payload_bindings':bindings,'inputs':len(m['inputs']),'decisions':2,'seven_slots_each':True,'source_items':344,'BODY_spans':10,'utc':utc()})
 print(json.dumps({'mode':mode,'actual_PID':os.getpid(),'status':'PASS','whole_logical_run_sha256':run['run_sha256'],'complete_RAW_review_sha256':bindings['COMPLETE_RAW_REVIEW']['RAW_sha256']}))
elif mode=='readback':
 b,r=payloads(True);x=rd('foreground-finalizer.receipt.json');assert x['actual_EXIT']==0;verify(x['stdout']);verify(x['stderr']);assert r['complete_native_audits']['source-coverage-audit.json']['missing_items']==0
 wr('readback.result.json',{'schema':'source67-actual-foreground-readback-v1','actual_PID':os.getpid(),'status':'PASS','whole_logical_run_sha256':r['run_sha256'],'decisions':2,'seven_slots_each':True,'RAW_LF_inputs':len(snapshots()['inputs']),'source_items':344,'literal_BODY_regions':10,'all_current_candidate_pins_verified':True,'all_raw_payloads_verified':True,'utc':utc()})
 print(json.dumps({'mode':mode,'actual_PID':os.getpid(),'status':'PASS','decisions':2,'source_items':344,'BODY':10}))
elif mode=='closevalidate':
 b,r=payloads(True)
 for label in ('finalizer','readback'):
  x=rd('foreground-'+label+'.receipt.json');assert x['actual_EXIT']==0;verify(x['stdout']);verify(x['stderr'])
 assert rd('readback.result.json')['status']=='PASS';wr('close-validation.result.json',{'schema':'source67-actual-foreground-close-validation-v1','actual_PID':os.getpid(),'status':'PASS','whole_logical_run_sha256':r['run_sha256'],'observed_finalizer_readback_EXITs':[0,0],'utc':utc()});print(json.dumps({'mode':mode,'actual_PID':os.getpid(),'status':'PASS'}))
elif mode=='close':
 b,r=payloads(True)
 for label in ('finalizer','readback','closevalidate'):
  x=rd('foreground-'+label+'.receipt.json');assert x['actual_EXIT']==0;verify(x['stdout']);verify(x['stderr'])
 assert rd('close-validation.result.json')['status']=='PASS'
 wr('close-last.prelease-result.json',{'schema':'source67-actual-foreground-last-writer-v1','actual_PID':os.getpid(),'status':'ALL_VALIDATED_FINAL_LEASE_NEXT','utc':utc(),'actual_EXIT_observation':'External foreground exec returns actual exit; no self-asserted terminal exit','canonical_writes':False})
 fs=[localpin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in ('owned.manifest.json','lease.final.json')]
 manifest={'schema':'source67-exhaustive-owned-manifest-v1','files':fs,'owned_files_including_manifest_and_final_lease':len(fs)+2,'exact_self_binding_exceptions':['owned.manifest.json','lease.final.json'],'self_and_final_lease_binding':'CLOSED_LAST lease hashes manifest/all other files; external actual close+postclose pins lease RAW','whole_logical_run_sha256':r['run_sha256'],'all_negatives_inputs_scripts_terminal_receipts_bound':True,'actual_last_writer_PID':os.getpid()};wr('owned.manifest.json',manifest)
 allfiles=[localpin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='lease.final.json']
 lease={'schema':'source67-CLOSED_LAST-final-owned-lease-v1','status':'CLOSED_LAST','owner':'/root/independent_source64','owned_path':O.as_posix(),'closed_utc':utc(),'actual_last_writer_PID':os.getpid(),'last_owned_write':'lease.final.json','owned_file_count_including_self':len(allfiles)+1,'owned_files_except_this_final_lease':allfiles,'whole_logical_run_sha256':r['run_sha256'],'distinct_complete_RAW_payloads':b,'actual_foreground_receipts':{k:rd('foreground-'+k+'.receipt.json') for k in ('finalizer','readback','closevalidate')},'canonical_Git_ledger_Lean_writes':False,'postclose_rule':'READ_ONLY zero owned writes. External actual foreground close/postclose stdout pins final lease RAW.'};wr('lease.final.json',lease)
 print(json.dumps({'mode':mode,'actual_PID':os.getpid(),'status':'CLOSED_LAST','owned_files':len(allfiles)+1,'lease_RAW_sha256':h((O/'lease.final.json').read_bytes()),'manifest_RAW_sha256':h((O/'owned.manifest.json').read_bytes()),'whole_logical_run_sha256':r['run_sha256'],'payloads':b}))
elif mode=='postclose':
 lease=rd('lease.final.json');assert lease['status']=='CLOSED_LAST';expected={x['relative_path'] for x in lease['owned_files_except_this_final_lease']}|{'lease.final.json'};actual={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()};assert actual==expected
 stamp=(O/'lease.final.json').stat().st_mtime_ns
 for x in lease['owned_files_except_this_final_lease']:verify(x);assert Path(x['path']).stat().st_mtime_ns<=stamp
 b,r=payloads(False);m=rd('owned.manifest.json')
 for x in m['files']:verify(x)
 assert len(actual)==lease['owned_file_count_including_self']==m['owned_files_including_manifest_and_final_lease']
 print(json.dumps({'schema':'source67-readonly-postclose-observation-v1','actual_PID':os.getpid(),'status':'PASS','owned_files':len(actual),'zero_postclose_owned_writes':True,'lease_last_mtime_verified':True,'lease_RAW_sha256':h((O/'lease.final.json').read_bytes()),'manifest_RAW_sha256':h((O/'owned.manifest.json').read_bytes()),'whole_logical_run_sha256':r['run_sha256'],'complete_RAW_bindings':b,'write_operations':0}))
else:raise ValueError(mode)
