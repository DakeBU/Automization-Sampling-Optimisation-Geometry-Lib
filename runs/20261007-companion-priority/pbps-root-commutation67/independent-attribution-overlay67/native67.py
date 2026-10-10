import os,sys,json,hashlib,datetime
from pathlib import Path
O=Path(__file__).resolve().parent

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b): return hashlib.sha256(b).hexdigest()
def cj(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def rd(n): return json.loads((O/n).read_bytes())
def wr(n,o):
 assert not (O/'lease.final.json').exists(), 'CLOSED_LAST: writes forbidden'
 (O/n).write_bytes((json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8'))
def pin(p):
 p=Path(p); b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
 return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':h(b),'LF_bytes':len(l),'LF_sha256':h(l)}
def localpin(p):
 d=pin(p);d['relative_path']=Path(p).relative_to(O).as_posix(); return d
def verify(x):
 a=pin(x['path'])
 for k in ('RAW_bytes','RAW_sha256','LF_bytes','LF_sha256'):
  if k in x: assert a[k]==x[k],(x['path'],k)
def logical(run):
 v=dict(run);del v['run_sha256'];return h(cj(v))
def snapshots():
 m=rd('inputs.manifest.json')
 for e in m['inputs']:
  verify(e['RAW_snapshot']);verify(e['LF_snapshot'])
  raw=Path(e['RAW_snapshot']['path']).read_bytes()
  assert Path(e['LF_snapshot']['path']).read_bytes()==raw.replace(b'\r\n',b'\n')
  assert h(raw)==e['original']['RAW_sha256']
 return m

def verify_payloads():
 b=rd('raw-payload-bindings.json');r=rd('review-run.json')
 assert logical(r)==r['run_sha256']==b['whole_logical_run_sha256']
 for k in ('COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT'):verify(b[k])
 assert rd('complete-RAW-decision.json')==r['decisions'][0]==rd('decision.json')
 assert rd('RAW-input-payload.json')==r['complete_RAW_input_payload']
 for x in r['owned_pre_finalization_pins']:verify(x)
 for x in rd('source-first-adoption.json')['primary_frozen_pins']:verify(x)
 snapshots()
 return b,r

mode=sys.argv[1]
if mode=='finalize':
 assert not (O/'review-run.json').exists(), 'No overwrite of previous finalizer'
 m=snapshots();d=rd('decision.json');a=rd('finite-diff-binding-and-consumer-audit.json');s=rd('source-first-adoption.json')
 entries=[]
 for e in m['inputs']:
  b=Path(e['RAW_snapshot']['path']).read_bytes()
  entries.append({'original':e['original'],'RAW_snapshot':e['RAW_snapshot'],'LF_snapshot':e['LF_snapshot'],'complete_original_RAW_UTF8':b.decode('utf-8')})
 inp={'schema':'overlay67-COMPLETE-RAW-INPUT-payload-v1','meaning':'Complete finite exact original RAW input texts with distinct RAW/LF snapshots; not a semantic decision payload','inputs':entries,'source_first_reuse':s,'finite_input_count':len(entries)}
 wr('RAW-input-payload.json',inp)
 # The only currently-open log files are explicit terminal-layer dependencies.
 excluded={'foreground-finalizer.stdout.RAW.log','foreground-finalizer.stderr.RAW.log'}
 pre=[localpin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in excluded]
 run={'schema':'overlay67-COMPLETE-logical-review-run-v1','reviewer':'/root/independent_source64','created_utc':utc(),'actual_foreground_finalizer_PID':os.getpid(),'kind':'independent finite presentation attribution overlay only','decisions':[d],'complete_finite_diff_binding_and_consumer_audit':a,'complete_RAW_input_payload':inp,'negative_boundaries':rd('negative-boundaries.json'),'source_first_before_proposal':s,'actual_foreground_review_observation':rd('foreground-review.observed-receipt.json'),'owned_pre_finalization_pins':pre,'closure_contract':{'whole_logical_hash':'Delete ONLY top-level run_sha256; canonical sorted UTF8 compact JSON of entire remaining object','complete_RAW_review':'Entire named review-run.json file bytes, no deletion','complete_RAW_decision':'Entire named complete-RAW-decision.json file bytes, all seven semantic slots','separate_complete_RAW_input':'Entire named RAW-input-payload.json bytes, no deletion','terminal_layers':'Foreground finalizer/readback/close-validation receipts and logs bound by final owned manifest and CLOSED_LAST lease; current open finalizer logs deferred exactly by name','manifest_self_binding':'owned.manifest.json hashes every owned file except itself and lease.final.json; lease.final.json binds manifest plus all other owned files; postclose console/tool output pins final lease RAW','last_write':'lease.final.json is last owned write; actual close process EXIT observed externally, then postclose is read-only','compiler_run':False},'run_sha256':None}
 run['run_sha256']=logical(run);wr('review-run.json',run)
 bindings={'schema':'overlay67-distinct-COMPLETE-RAW-payload-bindings-v1','whole_logical_run_sha256':run['run_sha256'],'COMPLETE_RAW_REVIEW':pin(O/'review-run.json'),'COMPLETE_RAW_DECISION':pin(O/'complete-RAW-decision.json'),'SEPARATE_COMPLETE_RAW_INPUT':pin(O/'RAW-input-payload.json')}
 wr('raw-payload-bindings.json',bindings)
 wr('finalizer.result.json',{'schema':'overlay67-foreground-finalizer-result-v1','actual_PID':os.getpid(),'status':'FINALIZED_PENDING_READBACK','complete_payload_bindings':bindings,'all_seven_slots_present':len(d['seven_semantic_slots'])==7,'canonical_writes':False,'source_mathematical_repair':False,'utc':utc()})
 print(json.dumps({'mode':mode,'actual_PID':os.getpid(),'status':'PASS','whole_logical_run_sha256':run['run_sha256'],'complete_RAW_review_sha256':bindings['COMPLETE_RAW_REVIEW']['RAW_sha256']}))
elif mode=='readback':
 b,r=verify_payloads();f=rd('foreground-finalizer.receipt.json');assert f['actual_EXIT']==0;verify(f['stdout']);verify(f['stderr'])
 wr('readback.result.json',{'schema':'overlay67-actual-foreground-readback-v1','actual_PID':os.getpid(),'status':'PASS','whole_logical_run_sha256':r['run_sha256'],'complete_RAW_payloads_verified':3,'all_seven_slots_verified':len(r['decisions'][0]['seven_semantic_slots'])==7,'finite_RAW_LF_inputs_verified':len(snapshots()['inputs']),'pre_finalization_owned_pins_verified':len(r['owned_pre_finalization_pins']),'parent_primary_header_pins_verified':True,'canonical_writes':False,'utc':utc()})
 print(json.dumps({'mode':mode,'actual_PID':os.getpid(),'status':'PASS','finite_RAW_LF_inputs':19,'slots':7}))
elif mode=='closevalidate':
 b,r=verify_payloads()
 for label in ('finalizer','readback'):
  x=rd('foreground-'+label+'.receipt.json');assert x['actual_EXIT']==0;verify(x['stdout']);verify(x['stderr'])
 assert rd('readback.result.json')['status']=='PASS'
 wr('close-validation.result.json',{'schema':'overlay67-actual-foreground-close-validation-v1','actual_PID':os.getpid(),'status':'PASS','utc':utc(),'whole_logical_run_sha256':r['run_sha256'],'observed_foreground_finalizer_and_readback_EXITs':[0,0],'lease_last_write_pending':True})
 print(json.dumps({'mode':mode,'actual_PID':os.getpid(),'status':'PASS'}))
elif mode=='close':
 b,r=verify_payloads()
 for label in ('finalizer','readback','closevalidate'):
  x=rd('foreground-'+label+'.receipt.json');assert x['actual_EXIT']==0;verify(x['stdout']);verify(x['stderr'])
 assert rd('close-validation.result.json')['status']=='PASS'
 wr('close-last.prelease-result.json',{'schema':'overlay67-actual-foreground-last-writer-v1','actual_PID':os.getpid(),'utc':utc(),'status':'ALL_CHECKS_PASS_LAST_WRITE_NEXT','observed_EXIT_contract':'Close writer actual process exit observed by external foreground exec; no self-asserted completion exit','canonical_writes':False})
 fs=[localpin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in ('owned.manifest.json','lease.final.json')]
 manifest={'schema':'overlay67-exhaustive-owned-manifest-v1','files':fs,'owned_files_including_manifest_and_final_lease':len(fs)+2,'exact_self_binding_exceptions':['owned.manifest.json','lease.final.json'],'self_and_final_lease_binding':'CLOSED_LAST lease hashes manifest and all other files; final lease RAW independently pinned by postclose stdout/tool result','whole_logical_run_sha256':r['run_sha256'],'negative_files_bound':True,'actual_last_writer_PID':os.getpid()}
 wr('owned.manifest.json',manifest)
 allfiles=[localpin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='lease.final.json']
 lease={'schema':'overlay67-CLOSED_LAST-final-owned-lease-v1','status':'CLOSED_LAST','owner':'/root/independent_source64','owned_path':O.as_posix(),'closed_utc':utc(),'actual_last_writer_PID':os.getpid(),'last_owned_write':'lease.final.json','owned_file_count_including_self':len(allfiles)+1,'owned_files_except_this_final_lease':allfiles,'whole_logical_run_sha256':r['run_sha256'],'distinct_complete_RAW_payloads':b,'actual_foreground_receipts':{k:rd('foreground-'+k+'.receipt.json') for k in ('finalizer','readback','closevalidate')},'canonical_Git_ledger_Lean_writes':False,'postclose_rule':'READ_ONLY; zero writes. External actual foreground close EXIT and readonly postclose console bind this final lease RAW.'}
 wr('lease.final.json',lease)
 print(json.dumps({'mode':mode,'actual_PID':os.getpid(),'status':'CLOSED_LAST','owned_files':len(allfiles)+1,'lease_RAW_sha256':h((O/'lease.final.json').read_bytes()),'manifest_RAW_sha256':h((O/'owned.manifest.json').read_bytes()),'whole_logical_run_sha256':r['run_sha256'],'payloads':b}))
elif mode=='postclose':
 lease=rd('lease.final.json');assert lease['status']=='CLOSED_LAST'
 expected={x['relative_path'] for x in lease['owned_files_except_this_final_lease']}|{'lease.final.json'}
 actual={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()};assert actual==expected,(actual-expected,expected-actual)
 stamp=(O/'lease.final.json').stat().st_mtime_ns
 for x in lease['owned_files_except_this_final_lease']:
  verify(x);assert Path(x['path']).stat().st_mtime_ns<=stamp,x['path']
 b,r=verify_payloads();m=rd('owned.manifest.json')
 for x in m['files']:verify(x)
 assert len(actual)==lease['owned_file_count_including_self']==m['owned_files_including_manifest_and_final_lease']
 print(json.dumps({'schema':'overlay67-readonly-postclose-observation-v1','actual_PID':os.getpid(),'status':'PASS','owned_files':len(actual),'zero_postclose_owned_writes':True,'lease_last_mtime_verified':True,'lease_RAW_sha256':h((O/'lease.final.json').read_bytes()),'manifest_RAW_sha256':h((O/'owned.manifest.json').read_bytes()),'whole_logical_run_sha256':r['run_sha256'],'complete_RAW_bindings':b,'write_operations':0}))
else:raise ValueError(mode)
