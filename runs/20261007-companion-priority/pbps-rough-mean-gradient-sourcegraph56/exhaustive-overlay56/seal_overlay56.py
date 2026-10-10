from pathlib import Path
import json,hashlib,datetime
stage=Path(__file__).parent;base=stage.parent
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):
    with path.open('rb') as handle:return handle.read()
def receipt(path):
    data=read(path);lf=data.replace(b'\r\n',b'\n')
    return {'path':str(path.resolve()),'raw_bytes':len(data),'raw_sha256':sha(data),'lf_bytes':len(lf),'lf_sha256':sha(lf),'normalization':'literal CRLF bytes to LF; otherwise unchanged'}
def seal(name,obj):
    path=stage/name;assert not path.exists(), 'No reclosure or overwrite of native stage output allowed.'
    canonical=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    obj=dict(obj);obj['self_digest']={'recipe':'Remove self_digest; JSON sort_keys=True ensure_ascii=False separators=(comma,colon), UTF8 no newline','named_payload_bytes':len(canonical),'named_payload_sha256':sha(canonical)}
    with path.open('w',encoding='utf-8',newline='\n') as handle:json.dump(obj,handle,indent=2,ensure_ascii=False);handle.write('\n')
    return receipt(path)
negative=json.loads(read(stage/'lease-discipline-correction.json').decode('utf-8'))
for original in negative['restorations']:
    data=read(Path(original['original_path']));before=read(Path(original['preserved_original_path']))
    assert data==before and sha(data)==original['raw_sha256']
graph=json.loads(read(stage/'sourceproofgraph56.json').decode('utf-8'))
assert graph['coverage']['parent_contract_slots']==87
run=seal('run.json',{'schema_version':1,'kind':'DISTINCT_EXHAUSTIVE_SOURCEGRAPH_OVERLAY_RUN','creator':'/root/sourcegraph_creator56','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'COMPLETE_PENDING_INDEPENDENT_TOPOLOGY_REVIEW','open_lease':receipt(stage/'lease.open.json'),'observed_process_completion':[{'script':'create_overlay56.py','exit_code':0},{'script':'readback_overlay56.py','exit_code':0}],'final_writer':'Synchronous foreground seal_overlay56.py; tool exit0 is required for actual process closure','negative_and_restoration':receipt(stage/'lease-discipline-correction.json'),'original_before_binding_validation':'PASS','source_admission':False,'target56_implementation_read':False,'compiler_started':False})
files={p.name:receipt(p) for p in sorted(stage.iterdir()) if p.is_file()}
manifest=seal('manifest.json',{'schema_version':1,'kind':'DISTINCT_EXHAUSTIVE_SOURCEGRAPH_OVERLAY_MANIFEST','status':'CREATOR_COMPLETE_PENDING_INDEPENDENT_REVIEW','overlay_files':files,'base_original_closed_receipts':{name:receipt(base/name) for name in ['manifest.json','run.json','complete.json','lease.json','read.lease.json','write.lease.json','python.lease.json','compiler.lease.json']},'base_exact_primary_first_freeze':receipt(base/'primary-before-signature.freeze.json'),'base_source_and_provider_receipts':{name:receipt(base/name) for name in ['primary-source-anchor-inventory.json','provider-contract-snapshots.json','provider-physical-context-receipts56.json','external-semantic-context-snapshots.json','prospective-statement.target.raw.snapshot.txt','prospective-statement.target.lf.snapshot.txt']},'run':run,'original_closed_paths_never_reclosed':True})
complete=seal('complete.json',{'schema_version':1,'kind':'DISTINCT_EXHAUSTIVE_SOURCEGRAPH_OVERLAY_COMPLETE','status':'COMPLETE_PENDING_INDEPENDENT_TOPOLOGY_REVIEW','creator':'/root/sourcegraph_creator56','manifest':manifest,'run':run,'sourcegraph':receipt(stage/'sourceproofgraph56.json'),'exhaustive_coverage':receipt(stage/'exhaustive-parent-contract-coverage56.json'),'coverage':{'source_items':92,'covered':49,'excluded':43,'target_slots':29,'parent_contract_slots':87,'source_nodes':29,'step_refinements':7,'full_residual_deep_boundaries':4},'unresolved_count':0,'unresolved_count_meaning':'Every source/contract item explicitly covered, excluded, or full-residual typed opaque boundary. No assertion that deep boundaries or target proof are complete.','compiler':'NOT_STARTED_CLOSED','source_admission':False,'before_after_correction':receipt(stage/'lease-discipline-correction.json'),'isolation_limitations':receipt(stage/'read-isolation-and-chronology56.json')})
common={'schema_version':1,'kind':'DISTINCT_OVERLAY_ACTUAL_RESOURCE_LEASE','creator':'/root/sourcegraph_creator56','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'CLOSED','scope':str(stage.resolve()),'open_lease':receipt(stage/'lease.open.json'),'run':run,'manifest':manifest,'complete':complete,'closure_policy':'All explicit read/write handles use context managers; lease write closes before synchronous writer returns. Parent-observed exec_command exit0 proves final writer process termination. No persistent sessions, background jobs, or compiler started.','retained_sessions':0,'retained_background_jobs':0,'original_closed_paths':'Exact before-byte equality rechecked; no reclosure or status rewriting.','source_admission':False}
resources={}
for name,kind,extra in [('read.lease.json','READ',{'readback':'PASS; originalbefore and exact target/provider physical bindings'}),('write.lease.json','WRITE',{'write_scope':'Distinct overlay only; original closed filenames have no further writes.'}),('python.lease.json','PYTHON',{'foreground_only':True,'parent_tool_exit_required':True}),('compiler.lease.json','COMPILER',{'compiler_state':'NOT_STARTED_CLOSED','started':False,'processes_started':0})]:
    resources[name]=seal(name,dict(common,resource=kind,**extra))
lease=seal('lease.json',dict(common,resource='COMPOSITE',compiler_state='NOT_STARTED_CLOSED',named_resource_leases=resources))
print(json.dumps({'manifest':manifest,'run':run,'complete':complete,'lease':lease,'status':'CREATOR_COMPLETE_PENDING_INDEPENDENT_REVIEW','compiler':'NOT_STARTED_CLOSED'}))
