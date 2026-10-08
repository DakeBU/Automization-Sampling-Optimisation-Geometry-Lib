from pathlib import Path
import hashlib, json, datetime
task=Path(__file__).parent; root=Path(r'E:\Samplinglib')
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def rawread(path):
    with path.open('rb') as handle:return handle.read()
def record(path):
    data=rawread(path); lf=data.replace(b'\r\n',b'\n')
    return {'path':str(path),'raw_bytes':len(data),'raw_sha256':sha(data),'lf_bytes':len(lf),'lf_sha256':sha(lf),'normalization':'literal bytes CRLF to LF'}
def sealed_write(name,payload):
    # The self digest is intentionally a named canonical payload, not an impossible hash of itself.
    canonical=json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    obj=dict(payload);obj['self_digest']={'recipe':'Remove self_digest; serialize remaining JSON with sort_keys=True, ensure_ascii=False, separators=(comma,colon), UTF8, no newline','payload_bytes':len(canonical),'payload_sha256':sha(canonical)}
    with (task/name).open('w',encoding='utf-8',newline='\n') as handle:json.dump(obj,handle,indent=2,ensure_ascii=False);handle.write('\n')
    return record(task/name)
providers=json.loads(rawread(task/'provider-contract-snapshots.json').decode('utf-8'))
for entry in providers:
    data=rawread(Path(entry['physical_path']));text=data.decode('utf-8');lines=text.splitlines(keepends=True)
    assert sha(data)==entry['whole_file_raw_sha256']
    selected=[]; ranges=[]
    for number,line in enumerate(lines[:entry['line_start']-1],start=1):
        if line.startswith(('import ','open ','open scoped ','namespace ','section','noncomputable section','variable ')):
            selected.append(line);ranges.append({'line':number,'literal':line})
    context=''.join(selected).encode('utf-8')
    stem=entry['declaration']+'.typing-context'
    with (task/(stem+'.raw.lean')).open('wb') as handle:handle.write(context)
    with (task/(stem+'.lf.lean')).open('wb') as handle:handle.write(context.replace(b'\r\n',b'\n'))
    entry['physical_typing_context_rows']=ranges
    entry['typing_context_raw_snapshot']=record(task/(stem+'.raw.lean'))
    entry['typing_context_lf_snapshot']=record(task/(stem+'.lf.lean'))
with (task/'provider-physical-context-receipts56.json').open('w',encoding='utf-8',newline='\n') as handle:json.dump(providers,handle,indent=2);handle.write('\n')
first=json.loads(rawread(task/'primary-before-signature.freeze.json').decode('utf-8'))
for name,metadata in first['first_stage_artifacts'].items():
    data=rawread(task/name);assert len(data)==metadata['bytes'] and sha(data)==metadata['raw_sha256']
assert sha(rawread(task/'primary-before-signature.freeze.json'))=='031343dd45d286aef4a97771cb95b8c2a4e48285abd92faca12466d3663cbe88'
run=sealed_write('run.json',{'schema_version':1,'kind':'SOURCE_GRAPH_CREATOR_RUN','creator':'/root/sourcegraph_creator56','utc':utc(),'status':'COMPLETE_PENDING_INDEPENDENT_REVIEW','actual_foreground_calls':[{'script':'extract_stage2_contracts.py','exit_code':0},{'script':'extract_semantics.py','exit_code':0,'note':'Repeated only to correct precise lexical ranges; no proof search or compiler.'},{'script':'build_creatorgraph56.py','exit_code':0}],'primary_first_originals':'PRESERVED_AND_HASH_VERIFIED','resource_retention':'No compiler/background/job/session resources started or retained. Final sealing writer exits synchronously; parent tool exit is authoritative process completion.','isolation_limitation':'read-isolation-and-chronology56.json','named_payloads':{name:record(task/name) for name in ['sourceproofgraph56.json','target-binder-semantic-expansion56.json','opaque-provider-semantic-expansion56.json','creator-complete56.json','read-isolation-and-chronology56.json']}})
excluded={'manifest.json','lease.json','complete.json','compiler.lease.json','read.lease.json','write.lease.json','python.lease.json'}
files={path.name:record(path) for path in sorted(task.iterdir()) if path.is_file() and path.name not in excluded}
manifest=sealed_write('manifest.json',{'schema_version':1,'kind':'SOURCE_GRAPH_CREATOR_MANIFEST','utc':utc(),'status':'COMPLETE_PENDING_INDEPENDENT_REVIEW','files':files,'active_context_inventory':'external-semantic-context-snapshots.json','superseded_lexical_snapshots':['Lp.83-91.raw.context.lean','Lp.83-91.lf.context.lean','Lp.89-93.raw.context.lean','Lp.89-93.lf.context.lean'],'superseded_snapshot_reason':'Preserved read observability; active Lp definition/carrier context is89-91, not the earlier truncated89-91 or structural89-93 range.','first_stage_freeze':record(task/'primary-before-signature.freeze.json'),'run':run})
complete=sealed_write('complete.json',{'schema_version':1,'kind':'SOURCE_GRAPH_CREATOR_COMPLETE','status':'COMPLETE_PENDING_INDEPENDENT_TOPOLOGY_REVIEW','utc':utc(),'creator':'/root/sourcegraph_creator56','manifest':manifest,'run':run,'payload':record(task/'creator-complete56.json'),'target_lf_sha256':'fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8','target_lf_bytes':1755,'canonical_mutation':False,'source_admission':False,'compiler':'NOT_STARTED_CLOSED'})
lease_common={'schema_version':1,'kind':'ACTUAL_RESOURCE_CLOSURE_LEASE','creator':'/root/sourcegraph_creator56','utc':utc(),'status':'CLOSED','closure_scope':'Resources opened by this creator; not global workspace processes or parent/reviewer compilers','run':run,'manifest':manifest,'complete':complete,'handles':'All file reads/writes use with context managers; payload and final lease write handles close before this synchronous writer returns.','retained_jobs':0,'persistent_tool_sessions':0,'parent_observation_required':'Synchronous exec_command exit_code0 is actual final writer process closure evidence; self-written receipt is not substituted for process observation.'}
for name,kind,extra in [('read.lease.json','READ',{'read_scope':'Source raw; exact target; provider opaque headers/import typing rows; definitions and opaque Mathlib extension headers. Disclosed incidental lines only.'}),('write.lease.json','WRITE',{'write_scope':'Exclusive run directory only; primary-first originals unchanged.'}),('python.lease.json','PYTHON',{'foreground_only':True,'compiler_started':False}),('compiler.lease.json','COMPILER',{'compiler_state':'NOT_STARTED_CLOSED','started':False,'processes_started':0})]:
    payload=dict(lease_common);payload['resource']=kind;payload.update(extra);sealed_write(name,payload)
lease=sealed_write('lease.json',dict(lease_common,resource='COMPOSITE',compiler_state='NOT_STARTED_CLOSED',named_resource_leases={name:record(task/name) for name in ['read.lease.json','write.lease.json','python.lease.json','compiler.lease.json']}))
print(json.dumps({'manifest':manifest,'run':run,'complete':complete,'lease':lease,'status':'COMPLETE_PENDING_INDEPENDENT_TOPOLOGY_REVIEW','compiler':'NOT_STARTED_CLOSED'}))
