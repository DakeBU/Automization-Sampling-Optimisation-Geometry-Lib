import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,copy
O=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('E:/Samplinglib');N=O.parent/'independent-source70'
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def put(n,x):assert not (O/n).exists();(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
known={'lease.final.json':'d3974254b5a27965de598361a64dc52439441357a5f95a2a30863d7ac4b09779','source.0.decision.json':'35bbf2d2fdb493bc47719a24e03a103ba83c6a83406c62c812dca274ce1315b3','owned-manifest.json':'53d7d0669404903075e9dbb9e6f735470c7301df52d720d23e84407361be9fdd'}
for n,h in known.items():assert H((N/n).read_bytes())==h
lease=json.loads((N/'lease.final.json').read_bytes());m=json.loads((N/'owned-manifest.json').read_bytes());mr={x['path']:x for x in m['files']}
assert lease['status']=='CLOSED_LAST' and lease['owned_count']==319
pins=[]
for n in ['source.0.admission-fields.json','source.0.decision.json','source.0.review-run.json','lease.final.json']:
 b=(N/n).read_bytes();expected=known.get(n,mr.get(n,{}).get('RAW_sha256'));assert H(b)==expected
 pins.append({'path':(N/n).relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':H(b),'LF_bytes':len(b.replace(b'\r\n',b'\n')),'LF_sha256':H(b.replace(b'\r\n',b'\n')),'LF_recipe':'replace ONLY CRLF bytes with LF','original_mtime_ns':(N/n).stat().st_mtime_ns,'immutable_native_file_not_copied':True})
original=json.loads((N/'source.0.admission-fields.json').read_bytes());proposed=copy.deepcopy(original)
prefix=N.relative_to(ROOT).as_posix()+'/'
mapping=[]
def change(obj,key,new,pointer):
 old=obj.get(key);obj[key]=new;mapping.append({'JSON_pointer':pointer,'before':old,'after':new})
change(proposed['audit_fields']['source_review'],'evidence',prefix+'source.0.review.complete-RAW.txt','/audit_fields/source_review/evidence')
change(proposed['audit_fields']['source_review'],'run_artifact',prefix+'source.0.decision.json','/audit_fields/source_review/run_artifact')
for key,n in [('source_graph','stageA.source-proof-graph70.frozen.json'),('source_inventory','stageB.primary419-current-exhaustive-decisions.json'),('coverage_report','stageB.all24-obligation-decisions.json')]:change(proposed['publication_source_proof_coverage'],key,prefix+n,'/publication_source_proof_coverage/'+key)
targets=[]
for q in mapping:
 p=ROOT/q['after'];assert p.is_file() and not pathlib.PurePosixPath(q['after']).is_absolute() and '\\' not in q['after'] and '..' not in pathlib.PurePosixPath(q['after']).parts
 b=p.read_bytes();targets.append({'path':q['after'],'RAW_bytes':len(b),'RAW_sha256':H(b)})
# Undo exact5field map and demand the ENTIRE original object, including7slots13deltas, unchanged.
recovered=copy.deepcopy(proposed)
recovered['audit_fields']['source_review']['evidence']=original['audit_fields']['source_review']['evidence'];del recovered['audit_fields']['source_review']['run_artifact']
for k in ['source_graph','source_inventory','coverage_report']:recovered['publication_source_proof_coverage'][k]=original['publication_source_proof_coverage'][k]
assert recovered==original
assert len(original['audit_fields']['semantic_slots'])==7 and len(original['audit_fields']['deltas'])==13
run=json.loads((N/'source.0.review-run.json').read_bytes());assert H(C({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']=='828e2f967924bdd4f35941c540623bb202051850621276bda8f6e19e550f672b'
assert proposed['review_run_sha256']==run['run_sha256'] and proposed['official_packet_sha256']=='47d6ccfb1422007c0b18f8be0cebffbdbe642f7d3068ee12206e27ecf472cce8'
put('original-native-RAW-pins.json',{'schema':'portable70-original-CLOSED319-exact-pins-v1','pins':pins,'original_native_manifest_RAW_sha256':known['owned-manifest.json'],'original_native_owned_count':319,'no_original_writes':True})
put('portable-admission-fields.proposed.json',proposed)
put('exact-five-field-pointer-map.json',{'schema':'portable70-exact-five-field-map-v1','count':5,'changes':mapping,'existing_repo_relative_targets':targets,'other_entire_object_exactly_equal_after_inverse_map':True,'all7slots13deltas0repairs_run_packet_unchanged':True})
decision={'schema':'portable70-independent-path-only-approval-v1','reviewer':'independent_primary69 / independent-source70-portable-admission','actual_pid':os.getpid(),'decision':'APPROVE_EXACT_FIVE_LOCATOR_FIELDS_ONLY','scope':'Canonical path portability only; no new mathematical/source verdict, repair, proof, compilation or VERIFIED/Exposition credit. Original CLOSED319 and all native bytes remain immutable. Root sole canonical writer.','original_admission_RAW_sha256':pins[0]['RAW_sha256'],'proposed_portable_admission_RAW_sha256':H((O/'portable-admission-fields.proposed.json').read_bytes()),'pointer_map_RAW_sha256':H((O/'exact-five-field-pointer-map.json').read_bytes()),'native_standard_decision_unchanged':True,'source_review_run_artifact':'Transparent repository-relative locator to original native standard source.0.decision.json; core source_review schema does not require this optional artifact field, but it is legitimate provenance.','existing_targets_byte_pinned':True,'whole_logical_original_run_sha256':run['run_sha256'],'official_reviewer_packet_sha256':proposed['official_packet_sha256'],'no_large_payload_or_whole_logs_copied':True,'canonical_applied':False}
put('portability-only.decision.json',decision)
put('complete-named-portability-review-input.json',{'schema':'portable70-complete-named-bounded-review-v1','original_inputs_RAW_pins':pins,'proposed_portable_admission':proposed,'exact_pointer_map':mapping,'target_RAW_pins':targets,'independent_approval':decision,'original_native_decision_run_lease_not_modified_or_copied':True})
print(json.dumps(decision,ensure_ascii=False))
