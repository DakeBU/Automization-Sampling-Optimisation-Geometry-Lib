from pathlib import Path
import json,hashlib,os,sys,datetime
sys.dont_write_bytecode=True
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-sharp-energy68';O=B/'independent-source-delta-schema68';S=B/'independent-source68'
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
rows=[]
def freeze(p,label):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');i=len(rows);raw=f'inputs/{i:02d}.RAW.snapshot';ln=f'inputs/{i:02d}.LF.snapshot';(O/raw).write_bytes(b);(O/ln).write_bytes(lf);rows.append({'source_path':p.relative_to(R).as_posix(),'label':label,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'raw_snapshot':raw,'lf_snapshot':ln});return json.loads(b)
p=freeze(B/'source-delta-schema-adapter68/proposal.json','EXACT_ROOT_SCHEMA_ONLY_PROPOSAL');assert rows[0]['RAW_sha256']=='5c935327f649dcfe8ce5329f027c7206849fa4989f22db227ca72b7af8a924fd'
lease=freeze(S/'lease.final.json','IMMUTABLE_CLOSED_LAST363');assert lease['status']=='CLOSED_LAST' and lease['total_owned_file_count_including_manifest_and_final_lease']==363 and rows[1]['RAW_sha256']=='e5962c11b38f64e3d782175c959e2c25c4b5e2bcad750eaf963cf4f547c89aeb'
run=freeze(S/'review-run.json','EXACT_NATIVE_WHOLE_LOGICAL_SOURCE_RUN');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']=='e987d89be0647776605af9fdd96c49ce309355540bf927823ae1fda9f7d534ce'
limit=freeze(S/'nonblocking-exposition-limitation-S-T.json','EXACT_NONBLOCKING_READER_SCOPE_LIMIT')
expected=['scopes','domains','scopes','objects','scopes'];assert p['slot_map']==expected and len(p['entries'])==3;assert p['source_mathematical_repair'] is False and p['canonical_inputs_modified'] is False
out=[]
reasons=[
'Bound weight identifier alpha-renaming belongs to binder/scope hygiene; retained analytic omega and all mathematical quantifiers are unchanged. Evidence includes exact CLOSED91 six-token maps as referenced by native decision. It is not a new assumption or constant delta.',
'Coordinate-free E/rank0 is a domain elaboration of actual PBPS consumer, not a finite-dimensional requirement added to the generic arbitrary-H lemma. The generic packet context explicitly supplies its actual PBPS consumer; informational metadata remains cross-context and does not strengthen the leaf.',
'AE per-observable kernel action, HP0-only inverse and ambient-to-intrinsic adjoint adapters are valid scope qualifications. They add no uniform null set, full-HP inverse, surjectivity or pointwise integrability claim.',
'S,T are missing prose aliases for existing real-valued energy expressions, appropriately classified in objects. Exact definitions and formula/Lean scopes are retained in the sealed limitation. This informational source decision does not close the outstanding reader exposition limitation.',
'Applied V2 changes prose identity-use count and source BODY span scope endpoints; scopes is valid. Exact current packets and bindings already encode the applied metadata, and this schema adapter itself changes none of them.'
]
for i,e in enumerate(p['entries']):
 d=freeze(R/e['native_decision'],'NATIVE_DECISION_'+str(i));assert rows[-1]['RAW_sha256']==e['native_RAW_sha256'];assert e['native_deltas']==d['deltas'];assert len(d['deltas'])==len(e['canonical_deltas'])==5
 for j,(native,adapted) in enumerate(zip(d['deltas'],e['canonical_deltas'])):
  assert {k:adapted[k] for k in native}==native and set(adapted)==set(native)|{'slot','severity','description','evidence'}
  assert adapted['slot']==expected[j] and adapted['severity']=='informational' and adapted['description']==native['detail'];assert native['blocking'] is False
  evidence='Native nonblocking source classification: '+native['class']+'; '+native['necessity']+'. '+d['semantic_slots'][expected[j]]['evidence'];assert adapted['evidence']==evidence
 out.append({'native_decision':e['native_decision'],'native_RAW_sha256':e['native_RAW_sha256'],'all_five_native_records_and_fields_preserved':True,'exact_added_fields_only':['slot','severity','description','evidence'],'five_slot_mappings':[{'delta_index':j,'slot':expected[j],'severity':'informational','approved':True,'independent_reason':reasons[j]} for j in range(5)],'verdict_changed':False,'source_Lean_statement_packet_binding_changed':False})
write('complete-RAW-input-payload.json',{'schema':1,'actual_pid':os.getpid(),'entries':rows,'entry_count':len(rows),'native_CLOSED363_reopened_or_modified':False})
a={'schema':'independent-native-source-delta-schema-review68-v1','reviewer':'/root/independent_header_source68','scope':'Schema adapter only, separate sibling after immutable native source review closure','proposal_RAW_sha256':rows[0]['RAW_sha256'],'decision':'APPROVED_EXACT_FINITE_SCHEMA_ADAPTER','native_source_whole_logical_run_sha256':run['run_sha256'],'native_source_lease_RAW_sha256':rows[1]['RAW_sha256'],'entries':out,'repairs':[],'canonical_writes':False,'native_decisions_modified':False,'source_mathematical_repair':False,'full_Exposition_Seal':False,'PURIFIED':False,'full_paper_or_Goal_complete':False,'open_exposition_limit_unchanged':limit,'actual_author_pid':os.getpid()}
r={'schema':'whole-logical-independent-schema-adapter-review68-v1','decision':a,'input_payload_RAW_sha256':sha((O/'complete-RAW-input-payload.json').read_bytes()),'actual_author_pid':os.getpid(),'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};r['run_sha256']=sha(canon(r));write('review-run.json',r);a['review_run_sha256']=r['run_sha256'];write('complete-RAW-decision.json',a)
print('ADAPTER_REVIEW_APPROVED_EXIT0',os.getpid(),'7_FINITE_INPUTS','15_EXACT_DELTA_MAPS',r['run_sha256']);print('RAW_DECISION',sha((O/'complete-RAW-decision.json').read_bytes()));print('RAW_INPUT',sha((O/'complete-RAW-input-payload.json').read_bytes()))
