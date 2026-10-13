from pathlib import Path
import hashlib,json,datetime
stage=Path(__file__).parent;base=stage.parent
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):
    with path.open('rb') as handle:return handle.read()
def write(name,obj):
    with (stage/name).open('w',encoding='utf-8',newline='\n') as handle:json.dump(obj,handle,indent=2,ensure_ascii=False);handle.write('\n')
write('lease.open.json',{'schema_version':1,'status':'OPEN','scope':str(stage.resolve()),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'resource':'READ_WRITE_PYTHON','reason':'Distinct exhaustive source-graph correction overlay; base CLOSED outputs restored to original exact bytes.'})
for name in ['sourceproofgraph56.json','creator-complete56.json','read-isolation-and-chronology56.json','exhaustive-parent-contract-coverage56.json']:
    with (stage/name).open('wb') as handle:handle.write(read(base/name))
restorations=[]
for name in ['manifest.json','run.json','complete.json','lease.json','read.lease.json','write.lease.json','python.lease.json','compiler.lease.json','sourceproofgraph56.json','creator-complete56.json','read-isolation-and-chronology56.json']:
    original=read(base/(name+'.before-exhaustive-expansion.raw.snapshot'))
    before=read(base/name)
    if before!=original:
        with (base/name).open('wb') as handle:handle.write(original)
    assert read(base/name)==original
    restorations.append({'original_path':str((base/name).resolve()),'preserved_original_path':str((base/(name+'.before-exhaustive-expansion.raw.snapshot')).resolve()),'raw_bytes':len(original),'raw_sha256':sha(original),'was_modified_before_correction':before!=original,'restored_exact':True})
manifest=json.loads(read(base/'manifest.json').decode('utf-8'))
for name,record in manifest['files'].items():
    data=read(base/name)
    assert len(data)==record['raw_bytes'] and sha(data)==record['raw_sha256'],name
assert sha(read(base/'primary-before-signature.freeze.json'))=='031343dd45d286aef4a97771cb95b8c2a4e48285abd92faca12466d3663cbe88'
graph=json.loads(read(stage/'sourceproofgraph56.json').decode('utf-8'))
graph['base_evidence_directory']=str(base.resolve());graph['overlay_directory']=str(stage.resolve())
for key in ['opaque_provider_binding','binder_expansion','physical_source_inventory']:
    graph[key]=str((base/graph[key]).resolve())
graph['exhaustive_parent_contract_coverage']=str((stage/'exhaustive-parent-contract-coverage56.json').resolve())
graph['read_isolation_limitation_path']=str((stage/'read-isolation-and-chronology56.json').resolve())
write('sourceproofgraph56.json',graph)
write('lease-discipline-correction.json',{'schema_version':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ORIGINAL_CLOSED_OUTPUTS_RESTORED_EXACT_OVERLAY_OPEN','observed_sequence':'Original base stage closed successfully. Expansion script preserved every base output before changing three original filenames. Parent lease discipline clarification arrived after that script exited. This overlay copies the expanded material to a new scope and restores every original filename byte-for-byte. No hidden restart or recovered-original claim.','restorations':restorations,'original_manifest_all_payload_validation':'PASS','original_primary_first_freeze_validation':'PASS','initial_Lp_89_91_fragment':'Earlier extractor overwrote it; tool-transcript evidence only. Other superseded lexical files retained. No fabricated original file or hash.'})
print(json.dumps({'overlay':str(stage.resolve()),'status':'OPEN','base_manifest_all_payload_validation':'PASS','base_original_outputs_restored':True,'primary_first_original':'UNCHANGED'}))
