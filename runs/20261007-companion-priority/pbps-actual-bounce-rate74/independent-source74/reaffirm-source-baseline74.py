from pathlib import Path
import json,hashlib,os,sys
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
P=R/'runs/20261007-companion-priority/pbps-bounce-rate-preproof74/independent-header-source74'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
def get(n):return json.loads((P/n).read_bytes())
lease=get('lease.final.json');assert lease['state']=='CLOSED' and lease['whole_owned_file_count']==38
assert sha((P/'lease.final.json').read_bytes())=='8e26413602672e647bd5b6692d6b9519ca003807ad1c44c4bd3a276a7c6abd67'
manifest=get('manifest.final.json')
for q in manifest['members']:
 b=(R/q['path']).read_bytes();assert sha(b)==q['RAW_sha256'] and len(b)==q['RAW_bytes'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
for n in ['source-header.0.run.json','stageA.freeze74.json']:
 q=get(n);h=q.pop('run_sha256');assert h==sha(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
expect=get('source-expectations.before-header74.json');coverage=get('source95-item-classification74.json');graph=get('source-proof-graph74.json');projection=get('header74.coverage-projection.json')
assert coverage['counts']=={'total':95,'NODE':38,'EXCLUDED':57}
assert graph['counts']=={'nodes':28,'edges':52} and len(projection['13_internal_bridges'])==13
primary=R/expect['primary']['path'];assert pin(primary)['RAW_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
names=['lease.final.json','manifest.final.json','stageA.freeze74.json','source-expectations.before-header74.json','source95-item-classification74.json','source-inputs74.json','source-formulas21.exact74.json','source-proof-graph74.json','source-obligations26.before-header74.json','header74.coverage-projection.json','source-header.0.decision.json','source-header.0.run.json']
report={'stage':'SOURCE_BASELINE_REAFFIRMED_BEFORE_FIRST74_BODY_READ','actual_PID':os.getpid(),'EXIT':0,'immutable_CLOSED38_members_verified':36,'prior_native_pins':[pin(P/n) for n in names],'fixed_primary_opaque_hash':pin(primary),'source_expectations_reused_without_change':expect,'source_graph_is_independent_source_graph_not_Lean_graph':True,'counts':{'source_items':95,'NODE':38,'EXCLUDED':57,'regions':15,'blocks':53,'formulas':21,'nodes':28,'edges':52,'obligations':26,'internal_bridges':13},'internal_required_bridges':projection['13_internal_bridges'],'exposure_record':{'earlier70_71_72_73_whole_module_source_exposure':True,'74_prospective_header_already_reviewed':True,'74_BODY_read_before_this_artifact':False,'other74_math_preread_verdict_or_decoder_read':False,'not_source_blind':True},'new_scope_current_phase':'OPEN implementation coverage preparation; official semantic packet and final freeze not yet supplied','will_not_pin_mutable_semantic_audit_cell_globalledger':True,'no_source_scan_repeat_or_old_native_write':True,'no_final_source_admission':True}
out=O/'source-baseline-reaffirmation74.json';assert not out.exists();out.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'actual_PID':os.getpid(),'EXIT':0,'baseline':pin(out),'source_contract_reaffirmed_before_BODY':True}))
print(json.dumps(expect,ensure_ascii=True))
