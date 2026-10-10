from pathlib import Path
import json,hashlib,os,datetime
O=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def cj(j):return json.dumps(j,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def ld(n):return json.loads((O/n).read_bytes())
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'name':p.relative_to(O).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l)}
def wr(n,j):
 assert not (O/'lease.final.json').exists();(O/n).write_bytes((json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
d=ld('decision.json');assert (O/'decision.json').read_bytes()==(O/'complete-RAW-decision.json').read_bytes();assert d['acceptance']['current_official_graph_freshness'] and not d['acceptance']['full_Exposition']
original=[]
for n in ['inputs.manifest.initial-SCI.json','inputs.manifest.final.json','inputs.manifest.negatives.json']:
 for z in ld(n)['inputs']:
  b=Path(z['RAW_snapshot']['path']).read_bytes();l=Path(z['LF_snapshot']['path']).read_bytes();assert sha(b)==z['original']['RAW_sha256'] and l==b.replace(b'\r\n',b'\n')
  original.append({'finite_original_RAW_LF_map':z,'complete_exact_RAW_UTF8_text':b.decode('utf-8')})
science=[]
for z in ld('SCI67-native-immutable-precheck.json')['nine_science_Lean_publication_lesson_audit_Git_bytes']:
 b=Path(z['Git_RAW']['path']).read_bytes();assert sha(b)==z['Git_RAW']['RAW_sha256'];science.append({'exact_SCI_Git_RAW_LF_map':z,'complete_exact_Git_RAW_UTF8_text':b.decode('utf-8')})
inp={'schema':'repository67-SEPARATE-COMPLETE-RAW-INPUT-v1','scope':'Complete selected99 original finite text inputs and nine exact SCI science texts; all594 exact historical receipt maps, complete immutable parent bindings, full generated graph/site/PNG byte pins with bounded one-hop graph projection. No whole-history or repeated primary-source copy.','original_inputs':original,'SCI_science_exact_inputs':science,'complete_receipt_input_maps':ld('root-gates-and-finite-snapshot-maps.json'),'large_current_generated_and_native_parents_by_complete_exact_pins':{'closed_parents':ld('SCI67-native-immutable-precheck.json')['closed_native_packages'],'current_generated':ld('current-graph-and-publication-bindings.json'),'reader':ld('reader-final67.json')}}
wr('RAW-input-payload.json',inp)
names=['SCI67-native-immutable-precheck.json','stable-static-reader-contract.json','root-gates-and-finite-snapshot-maps.json','reader-final67.json','current-graph-and-publication-bindings.json','shared-authored-finite-delta.json','python296-exact-reuse67.json','prior64-priority-and-INT66-historical-boundary.json','whitespace-exact-byte-diagnosis67.json','independent-gates67.result.json','audit-final67.result.json','negative.process-and-observer.json','observer-negatives.initial.json','observed-tools.pre-final.json','synthesis67.result.json']
pending={'foreground-finalizer.stdout.RAW.log','foreground-finalizer.stderr.RAW.log'}
pre=[pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.relative_to(O).as_posix() not in pending]
run={'schema':'repository67-COMPLETE-logical-RAW-review-run-v1','reviewer':'/root/independent_source64','actual_finalizer_PID':os.getpid(),'finalized_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_SCI_commit':d['exact_SCI_commit'],'decisions':[d],'complete_named_RAW_INPUT':{'file':'RAW-input-payload.json','binding':pin(O/'RAW-input-payload.json'),'complete_payload':inp},'analytical_evidence':{n:ld(n) for n in names},'pre_finalization_owned_RAW_LF_bindings':pre,'run_hash_rule':'SHA256 of entire parsed logical object deleting ONLY top-level run_sha256; recursively sorted compact UTF8 JSON ensure_ascii=false; no newline; no field projection.','closure_contract':{'exact_pending_finalizer_files':sorted(pending),'future_terminal_and_self_layers':'Actual foreground finalizer/readback/close-validator logs+receipts, their result files, RAW payload bindings, prelease record, exhaustive owned manifest and CLOSED_LAST final lease. Every owned byte including scripts/negatives/self/terminals is bound by final manifest and final lease; final lease self RAW hash returned externally.','COMPLETE_RAW_REVIEW':'Whole review-run.json exact bytes with NO deletion; distinct from logical run hash.','COMPLETE_RAW_DECISION':'Whole complete-RAW-decision.json exact bytes with NO deletion.','SEPARATE_COMPLETE_RAW_INPUT':'Whole RAW-input-payload.json exact bytes with NO deletion.','postclose':'Read-only external console observation with actual PID/EXIT, zero owned writes.'},'full_Exposition':False,'PURIFIED':False,'main_live':False,'whole_Goal_complete':False,'canonical_writes':False}
run['run_sha256']=sha(cj(run));wr('review-run.json',run)
b={'schema':'repository67-distinct-complete-named-RAW-payload-bindings-v1','whole_logical_run_sha256':run['run_sha256'],'COMPLETE_RAW_REVIEW':pin(O/'review-run.json'),'COMPLETE_RAW_DECISION':pin(O/'complete-RAW-decision.json'),'SEPARATE_COMPLETE_RAW_INPUT':pin(O/'RAW-input-payload.json')};wr('raw-payload-bindings.json',b)
wr('finalizer.result.json',{'schema':'repository67-actual-foreground-finalizer-result-v1','actual_foreground_PID':os.getpid(),'status':'ACCEPT_SCOPED_CURRENT_FINAL_ADMIN','bindings':b,'actual_exit':'External foreground runner must observe; this field asserts no self-observed exit.'})
print(json.dumps({'actual_PID':os.getpid(),'whole_logical_run_sha256':run['run_sha256'],'COMPLETE_RAW_REVIEW_sha256':b['COMPLETE_RAW_REVIEW']['RAW_sha256'],'COMPLETE_RAW_DECISION_sha256':b['COMPLETE_RAW_DECISION']['RAW_sha256'],'SEPARATE_COMPLETE_RAW_INPUT_sha256':b['SEPARATE_COMPLETE_RAW_INPUT']['RAW_sha256']}))
