from pathlib import Path
import json,gzip,hashlib,subprocess,sys,datetime,copy,os
sys.path.insert(0,'tools');import astis_advance as a;import astis_publication as pub
ADV='ASTIS-SA-20261107-GaussianComplexityFixedSpectrumQuery';OWNER='huanjian_gc_20261107_fixed_spectrum_query_integration';DECL='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query';OUT=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-query-integration-20261107')
sha=lambda b:hashlib.sha256(b).hexdigest()
def unpack(row):
 raw=Path(row['path']).read_bytes();assert sha(raw)==row['gzip_sha256'],row['path'];data=gzip.decompress(raw);assert sha(data)==row['raw_sha256'];return data
states=a.current_advances();s=states[ADV];assert s['state']=='STABILIZING' and s['latest_evidence']['integration_owner']==OWNER and [k for k,v in states.items() if v['state']=='STABILIZING']==[ADV]
pub.check_advance([DECL],reviewed=True);report=OUT/'independent-integration-reader-review/preparation-report.json';assert sha(report.read_bytes())=='d18f57fb92715929a4270794b48e1616020d4b12ae48b29164460c224eb7055d';x=json.loads(report.read_bytes());assert x['publication_binding_sha256']=='fafc6866bd79667295b685939cb04e42374863753ab3e205c43ce6d0780e3970'
for p,h in x['source_test_publication_lesson_pins'].items():assert sha(Path(p).read_bytes())==h
assert len(x['shared_paths'])==7 and not (OUT/'shared-integration-manifest.json').exists();head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head=='dd661f1bd36a83de9efe6bb5d0784e0ab1e56802';subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],check=True)
plans=[]
for row in x['shared_paths']:
 p=Path(row['path']);old=p.read_bytes() if p.exists() else None;assert (old is not None)==row['before_exists'] and (sha(old) if old is not None else None)==row['before_sha256'],str(p)
 if old is not None:assert subprocess.check_output(['git','show',head+':'+str(p)])==old
 new=unpack(row['planned_after_archive']);assert sha(new)==row['planned_after_sha256'];plans.append((row,old,new))
for path,record in x['ledger_protection'].items():
 raw=Path(path).read_bytes();assert raw.startswith(unpack(record['raw_prefix']));foreign=json.loads(unpack(record['foreign_projection']));now=a.current_advances() if 'advances' in path else a.current_discoveries();assert all(now[k]==v for k,v in foreign.items())
protected=json.loads(unpack(x['foreign_source_content_inputs']))
for p,row in protected.items():
 q=Path(p);raw=os.fsencode(os.readlink(q)) if q.is_symlink() else q.read_bytes();assert sha(raw)==row['sha256'],p
frontier=next((old,new) for row,old,new in plans if row['path']=='website/content/samplewiki_companion_frontiers.json');old,new=map(json.loads,frontier);assert old['execution']==new['execution'] and old['cases'][4]['theorems'][0]==new['cases'][4]['theorems'][0]
assert new['cases'][4]['theorems'][1]['boundary'].endswith(x['old_frontier']['Section4_4_limitation_suffix'])
for v in [old,new]:v['cases'][4]['reader_guide'][3]='<FSQ>';v['cases'][4]['theorems'][1]['boundary']='<FSQ>'
assert old==new
functorpath=Path(x['typed_substrate_delta']['FunctorHypergraph_model_path']);fb=functorpath.read_bytes();assert sha(fb)==x['typed_substrate_delta']['FunctorHypergraph_model_exact_raw_sha256_unchanged'];bridge=next(v for v in json.loads(fb)['hyperedges'] if v['id']=='transport:gaussian-quadratic-oracle-factorization');assert bridge['formal_refs']==[] and bridge['status']=='not-Lean-certified'
gmo,gmn=next((old,new) for row,old,new in plans if row['path']=='website/content/graph_memory_index.json');gmo,gmn=map(json.loads,[gmo,gmn]);fam=next(f for f in gmn['families'] if f['id']=='family:gaussian-oracle-hardness');assert fam['compiled_substrate_bindings'][-2:]==x['typed_substrate_delta']['two_new_source_present_module_bindings'];fam['compiled_substrate_bindings']=fam['compiled_substrate_bindings'][:-2];assert gmo==gmn
lb=Path('runs/substantive_advances.jsonl').read_bytes();db=Path('runs/substantive_discoveries.jsonl').read_bytes()
for row,old,new in plans:
 p=Path(row['path']);p.parent.mkdir(exist_ok=True,parents=True);p.write_bytes(new);assert sha(p.read_bytes())==row['planned_after_sha256']
assert Path('runs/substantive_advances.jsonl').read_bytes()==lb and Path('runs/substantive_discoveries.jsonl').read_bytes()==db and a.current_advances()==states and functorpath.read_bytes()==fb
manifest={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_commit':head,'integration_owner':OWNER,'mathematical_candidate':'1ff1cb79413a853e977a50e598ce04211806dad8','actual_source_verified_metadata_commit':'de220a52922fc2aa2c007ea14bf2c2949030b8d2','accepted_source_V_first_carrying_commit':head,'source_verifier':'/root/reader_361904','reviewed_proposal_raw_sha256':sha(report.read_bytes()),'paths':[{'path':row['path'],'before_sha256':sha(old) if old is not None else None,'after_sha256':sha(new)} for row,old,new in plans],'case_scalar_pointer_delta':['/cases/4/reader_guide/3','/cases/4/theorems/1/boundary'],'determinant_index0_all_other_case_values_and_execution_preserved':True,'Section4_4_limitation_suffix_preserved_verbatim':True,'all_old_Registry_entries_and_bytes_preserved':True,'new_canonical_entries':1,'count_change':'616->617 administrative inventory only','new_conceptual_bridge':False,'existing_typed_bridge':'transport:gaussian-quadratic-oracle-factorization','actual_ASTIS_proof_parents':[],'FOQ_is_conceptual_sibling_only':True,'conceptual_formal_refs':[],'FunctorHypergraph_model_exact_bytes_unchanged':sha(fb),'all_old_family_fields_and_bindings_preserved':True,'ledger_and_all_advance_states_unchanged_by_shared_write':True,'protected_foreign_source_inputs_checked':len(protected),'state':'Exact guarded seven-path STAB shared write completed; actual canonical gates/reader acceptance pending'}
(OUT/'shared-integration-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'shared_paths':len(plans),'one_canonical_node_added':True,'existing_model_unchanged':True,'no_formal_transport_or_FOQ_parent':True,'protected_foreign_inputs':len(protected)}))
