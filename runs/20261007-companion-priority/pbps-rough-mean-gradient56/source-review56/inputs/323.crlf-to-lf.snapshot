from pathlib import Path
import json,hashlib,datetime
stage=Path(__file__).parent;base=stage.parent
def sha(data):return hashlib.sha256(data).hexdigest()
def rawread(path):
    with path.open('rb') as handle:return handle.read()
def save(name,obj):
    with (stage/name).open('w',encoding='utf-8',newline='\n') as handle:json.dump(obj,handle,indent=2,ensure_ascii=False);handle.write('\n')
for name in ['target-binder-semantic-expansion56.json','provider-physical-context-receipts56.json','opaque-provider-semantic-expansion56.json']:
    with (stage/name).open('wb') as handle:handle.write(rawread(base/name))
negative=json.loads(rawread(stage/'lease-discipline-correction.json').decode('utf-8'))
negative['actual_post_closed_mutations']=[{'file':name,'operation':'expand_parent_contracts56.py saved expanded JSON at existing CLOSED base filename after preserving original snapshot','status':'ACTUAL_OBSERVED_SCRIPT_COMPLETED_EXIT0; subsequent exact restoration documented','residual_before_gap':'Original compact provider15-row summaries and target29 rows did not separately enumerate45 parent input binder instances and42 parent returned-object/quantifier slots; full lexical parent headers themselves were present.'} for name in ['sourceproofgraph56.json','creator-complete56.json','read-isolation-and-chronology56.json']]
negative['operation_sequence']=[{'order':1,'operation':'seal_creatorgraph56.py','observed_exit_code':0,'result':'original CLOSED receipts emitted'}, {'order':2,'operation':'expand_parent_contracts56.py','observed_exit_code':0,'result':'before snapshots all11 outputs preserved; three existing filenames modified after CLOSED'}, {'order':3,'operation':'parent lease discipline clarification received','result':'require distinct overlay and original restoration'}, {'order':4,'operation':'create_overlay56.py','observed_exit_code':0,'result':'overlay OPEN; exact snapshot-to-original bytes and whole original manifest payloads verified; original statuses unchanged'}, {'order':5,'operation':'current readback in OPEN overlay','result':'every original snapshot binding rechecked, exact target/source/parent header bindings rechecked, no original write'}]
save('lease-discipline-correction.json',negative)
for restore in negative['restorations']:
    data=rawread(Path(restore['original_path']));original=rawread(Path(restore['preserved_original_path']))
    assert data==original and sha(data)==restore['raw_sha256']
target=json.loads(rawread(stage/'target-binder-semantic-expansion56.json').decode('utf-8'))
coverage=json.loads(rawread(stage/'exhaustive-parent-contract-coverage56.json').decode('utf-8'))
assert len(target['rows'])==29 and len(coverage['rows'])==87
assert target['target']['lf_sha256']=='fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
for p in json.loads(rawread(stage/'provider-physical-context-receipts56.json').decode('utf-8')):
    data=rawread(Path(p['physical_path']));assert sha(data)==p['whole_file_raw_sha256']
    header=rawread(base/(p['declaration']+'.raw.contract.lean'))
    assert sha(header)==p['header_raw_sha256'] and b':= by' not in header
coverage['covered_excluded_report']={'covered_source_items':sum(x['disposition']=='NODE' for x in json.loads(rawread(base/'primary-source-anchor-inventory.json').decode('utf-8'))['inventory']),'excluded_source_items':sum(x['disposition']=='EXCLUDED' for x in json.loads(rawread(base/'primary-source-anchor-inventory.json').decode('utf-8'))['inventory']),'target_semantic_slots':29,'parent_input_binder_slots':45,'parent_total_slots':87,'unnamed_step_routes':7,'deep_boundary_full_residuals':4,'review_admission':'PENDING_INDEPENDENT_REVIEW','original_coverage_gap':'Compact summaries did not enumerate each parent binder/output separately; exact header snapshots existed. Overlay enumerates them without source topology self-admission.'}
save('exhaustive-parent-contract-coverage56.json',coverage)
save('operations-readback56.json',{'schema_version':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'OPEN_STAGE_READBACK_PASS_NOT_SOURCE_ADMISSION','target_lf_sha256':target['target']['lf_sha256'],'target_lf_bytes':1755,'base_original_before_binding_validation':'PASS','current_provider_physical_raw_header_context_validation':'PASS','target_slot_count':29,'parent_slot_count':87,'deep_full_residual_count':4,'compiler':'NOT_STARTED_CLOSED','compiler_started':False,'explicit_negative_retained':'lease-discipline-correction.json','incidental_exposure_retained':'read-isolation-and-chronology56.json'})
print(json.dumps({'readback':'PASS','original_before_bindings':'PASS','parent_slots':87,'covered_excluded':coverage['covered_excluded_report'],'compiler':'NOT_STARTED_CLOSED'}))
