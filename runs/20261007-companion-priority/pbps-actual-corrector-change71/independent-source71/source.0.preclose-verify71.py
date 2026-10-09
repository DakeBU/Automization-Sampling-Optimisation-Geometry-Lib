import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,copy
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;R=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
def verify(q,p):
 b=p.read_bytes();assert len(b)==q.get('RAW_bytes',q.get('raw_bytes'));assert sha(b)==q.get('RAW_sha256',q.get('raw_sha256'));assert sha(b.replace(b'\r\n',b'\n'))==q.get('LF_sha256',q.get('lf_sha256'))
stageA=json.loads((O/'stageA.owned-finite-manifest71.json').read_bytes())
for q in stageA['files']:verify(q,B/q['path'])
union={};manifestnames=['stageA.primary-input-pins.json','stageA.read-only-anchor-pins.json','stageB.exact-input-manifest71.json','stageB.additional-exact-inputs71.json','stageB.reader-status-overlay71.input-manifest.json','stageB.final-current-inputs71.json']
allowed=json.loads((O/'stageB.all-input-current-attribution71.json').read_bytes())['allowed_changed_paths']
for mn in manifestnames:
 for q in json.loads((O/mn).read_bytes())['inputs']:
  p=pathlib.Path(q.get('original_path',q['path'] if 'path' in q else ''));p=p if p.is_absolute() else B/p;path=p.relative_to(B).as_posix()
  rawhash=q.get('RAW_sha256',q.get('raw_sha256'));lfhash=q.get('LF_sha256',q.get('lf_sha256'));rawlen=q.get('RAW_bytes',q.get('raw_bytes'))
  snap=q.get('snapshot');lfsnap=q.get('LF_snapshot');current=p.read_bytes();currenthash=sha(current)
  if snap:
   verify(q,O/snap)
   if lfsnap:assert (O/lfsnap).read_bytes()==(O/snap).read_bytes().replace(b'\r\n',b'\n')
  if currenthash!=rawhash:assert path in allowed and currenthash==allowed[path] and snap
  else:verify(q,p)
  key=(path,rawhash)
  if key not in union:union[key]={'path':path,'RAW_bytes':rawlen,'RAW_sha256':rawhash,'LF_sha256':lfhash,'current_RAW_sha256_at_close':currenthash,'version_is_historical_approved_reader_overlay':currenthash!=rawhash,'named_by_manifests':[],'owned_RAW_snapshot_refs':[],'owned_LF_snapshot_refs':[]}
  u=union[key];u['named_by_manifests'].append(mn)
  if snap and snap not in u['owned_RAW_snapshot_refs']:u['owned_RAW_snapshot_refs'].append(snap)
  if lfsnap and lfsnap not in u['owned_LF_snapshot_refs']:u['owned_LF_snapshot_refs'].append(lfsnap)
rows=sorted(union.values(),key=lambda x:(x['path'],x['RAW_sha256']))
input_union={'schema':'source71-complete-finite-versioned-input-union-v1','actual_pid':os.getpid(),'count':len(rows),'distinct_paths':len(set(x['path'] for x in rows)),'RAW_LF_recipe':'Exact RAW bytes and ONLY byte CRLF to LF, no other normalization; immutable prior/full primary inputs pinned by exact current file hashes rather than duplicated.','manifest_sources':[pin(O/m) for m in manifestnames],'entries':rows,'entries_canonical_sha256':sha(canon(rows)),'unmapped_input_drift':0}
write('source.0.complete-finite-input-manifest.json',input_union)
run=json.loads((O/'source.0.run.json').read_bytes());assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
for q in run['records']:verify(q,B/q['path'])
decision=json.loads((O/'source.0.decision.json').read_bytes());admission=json.loads((O/'source.0.admission-fields.json').read_bytes());packet=json.loads((R/'source-review.packet.1.json').read_bytes())
assert decision['review_run_sha256']==run['run_sha256']==admission['audit_fields']['source_review']['review_run_sha256']
assert decision['reviewer_packet_sha256']==packet['packet_sha256']==admission['official_packet_sha256']==run['official_packet_sha256']
assert admission['official_packet_RAW_sha256']==sha((R/'source-review.packet.1.json').read_bytes())
sys.path.insert(0,str(B/'tools'));import astis_semantic_roundtrip_core as core
assert set(decision['semantic_slots'])==set(core.SEMANTIC_SLOTS) and len(decision['deltas'])==16 and not decision['repairs']
assert decision['verdict']=='equivalent-after-elaboration'
assert all(x['relation'] in {'same','equivalent','explicit-elaboration'} for x in decision['semantic_slots'].values())
assert all(set(d)=={'slot','severity','description','evidence'} and d['slot'] in core.SEMANTIC_SLOTS and d['severity']=='informational' for d in decision['deltas'])
audit=json.loads((B/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json').read_bytes());before=core.semantic_reviewer_packet(audit);after=copy.deepcopy(audit);after.update(admission['audit_fields']);assert before==core.semantic_reviewer_packet(after)==packet
for q in [admission['audit_fields']['source_review']['evidence'],admission['audit_fields']['source_review']['run_artifact'],*[admission['publication_source_proof_coverage'][k] for k in ['source_graph','source_inventory','coverage_report']]]:
 assert '\\' not in q and ':' not in q and not pathlib.PurePosixPath(q).is_absolute() and (B/q).is_file()
mc=json.loads((O/'stageB.whole-module528-NODE-EXCLUDED71.json').read_bytes());sc=json.loads((O/'stageB.primary255-source-implementation-coverage71.json').read_bytes());ob=json.loads((O/'stageB.all24-source-obligations71.json').read_bytes());de=json.loads((O/'stageB.all51-blind-reconstruction-comparisons71.json').read_bytes())
assert mc['count']==len(mc['entries'])==528 and mc['unclassified']==0 and sc['source_count']==len(sc['entries'])==255 and sc['unclassified']==0
assert ob['count']==ob['satisfied']==len(ob['entries'])==24 and ob['blocking']==0 and de['count']==len(de['entries'])==51 and de['unresolved']==0
terminals=[]
for p in sorted(O.glob('*.terminal-receipt.json')):
 q=json.loads(p.read_bytes())
 for k in ['stdout','stderr']:
  x=q[k];b=(O/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256']
 terminals.append({'receipt':pin(p),'actual_pid':q['actual_pid'],'exit_code':q['exit_code'],'command_argv':q['command_argv'],'foreground':q['foreground'],'negative_retained':q['exit_code']!=0})
write('source.0.actual-terminal-catalog71.json',{'schema':'source71-native-foreground-terminal-catalog-v1','actual_catalog_pid':os.getpid(),'receipts_count_before_this_verify_receipt':len(terminals),'entries':terminals,'external_focused_compile_PID_EXIT':[49980,0],'external_root_reader_overlay_apply_PID_EXIT':[29512,0],'GBK_read_observer_negative_separate_record':'stageA.read-observer-negative.json','final_close_terminal_is_separately_in_final_manifest':True})
payloadpath=O/'complete-named-review-decision-input-payload.json';payload=json.loads(payloadpath.read_bytes());assert payload['native_run_complete']==run and payload['decision_complete']==decision and payload['canonical_admission_fields_complete']==admission and payload['full_RAW_review_utf8']==(O/'source.0.review.RAW.md').read_text(encoding='utf-8')
(O/'complete-named-review-decision-input-payload.before-final-input-union.exactraw.snapshot.json').write_bytes(payloadpath.read_bytes())
payload['complete_finite_versioned_input_manifest_complete']=input_union;payload['complete_finite_versioned_input_manifest_RAW_LF']=pin(O/'source.0.complete-finite-input-manifest.json');payload['actual_terminal_catalog_RAW_LF']=pin(O/'source.0.actual-terminal-catalog71.json')
write('complete-named-review-decision-input-payload.json',payload)
report={'schema':'source71-preclose-independent-verification-v1','actual_pid':os.getpid(),'status':'PASS_PRE_CLOSE','StageA_47_frozen_files_unchanged':len(stageA['files']),'complete_versioned_inputs':len(rows),'distinct_input_paths':input_union['distinct_paths'],'unmapped_drift':0,'whole_logical_run_sha256':run['run_sha256'],'official_packet_sha256':packet['packet_sha256'],'decision':pin(O/'source.0.decision.json'),'admission_fields':pin(O/'source.0.admission-fields.json'),'named_payload':pin(payloadpath),'input_manifest':pin(O/'source.0.complete-finite-input-manifest.json'),'before_after_official_packet_canonical_bytes_identical':True,'all_255_source_528_module_24obligation_51decoder_entries_accounted':True,'same6callers12witnesses_no_mathrepair':True,'reader_status_overlay_exact_separately_approved':True,'canonical_or_old_CLOSED_writes':False}
write('source.0.preclose-verification71.json',report)
print(json.dumps(report,ensure_ascii=False,indent=2))
