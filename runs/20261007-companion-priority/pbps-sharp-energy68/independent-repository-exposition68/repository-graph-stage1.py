from pathlib import Path
import json,hashlib,os,sys,datetime,subprocess,copy
sys.dont_write_bytecode=True
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-sharp-energy68';O=B/'independent-repository-exposition68'
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
rows=[]
def freeze(p,label,j=False):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');i=len(rows);raw=f'inputs/{i:03d}.RAW.snapshot';ln=f'inputs/{i:03d}.LF.snapshot';(O/raw).write_bytes(b);(O/ln).write_bytes(lf);rows.append({'source_path':p.relative_to(R).as_posix(),'label':label,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'raw_snapshot':raw,'lf_snapshot':ln,'LF_binary_projection_not_text_or_image_semantics':p.suffix.lower() in {'.png','.jpg'}});return json.loads(b) if j else b
notes=freeze(B/'integration.notes.json','SYNTHESIS_FIRST_ROOT_CAPSULE',True);visual=freeze(B/'visual.inspection.json','ROOT_SCOPED_VISUAL_CAPSULE',True);admin=freeze(B/'integration68/final-admin.json','FINAL_CELL_ADMIN_BEFORE_GRAPH',True)
head=subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,check=True);write('git-HEAD.receipt.json',{'actual_reader_pid':os.getpid(),'command':['git','rev-parse','HEAD'],'exit_code':head.returncode,'stdout_RAW':head.stdout.decode(),'HEAD':head.stdout.decode().strip()});assert head.stdout.decode().strip()==notes['proof_commit']==admin['proof_commit']=='3ad3b127b5a645be9cf71b3d14520b2d8fea3122'
neg={'status':'OBSERVER_LIMITS_RETAINED','initial_combined_display_truncated':True,'initial_full_notes_visual_output_is_not_authoritative':'Complete finite RAW snapshots are authoritative; bounded key projections subsequently read. No mathematical verdict based on clipped console.','nonexistent_optional_rg_path':'AutoSamplingTheory/ExampleCases/ProximalBPS.lean does not exist; rg returned EXIT1 (chunk37e0a5). Actual aggregate is AutoSamplingTheory/ExampleCases.lean, explicitly found and inspected. No proof or source failure inferred.','own_compiler_started':False};write('negative.observer-display-and-path.json',neg)
closed=[]
for sub,count,expected in [('independent-source68',363,'e5962c11b38f64e3d782175c959e2c25c4b5e2bcad750eaf963cf4f547c89aeb'),('independent-source-delta-schema68',24,'3a6254f1334127de61473688605872877e9caef3c109975864c852f0d9f7f828'),('independent-energy-alias-overlay68',80,'36e61c3fa58d67967e0b7a80cbdef45664e03f6153b9f013228b447c08442465')]:
 l=freeze(B/sub/'lease.final.json','EXACT_NATIVE_CLOSED_REUSE',True);assert sha((B/sub/'lease.final.json').read_bytes())==expected and l['status']=='CLOSED_LAST';assert len([p for p in (B/sub).rglob('*') if p.is_file()])==count;closed.append({'folder':sub,'count':count,'lease_RAW_sha256':expected,'whole_logical_run_sha256':l['whole_logical_run_sha256'],'not_treated_as_all_old_inputs_current_RAW':True})
for sub,files in [('independent-source68',['source.0.decision.json','source.1.decision.json','source.consumer.decision.json','packet-bindings-and-context.readback.json','eleven-literal-BODY-spans.readback.json']),('independent-energy-alias-overlay68',['complete-RAW-decision.json','finite-diffs-and-unchanged-bindings.audit.json'])]:
 for n in files:freeze(B/sub/n,'BOUNDED_SEALED_NATIVE_SOURCE_OR_ALIAS_EVIDENCE')
verifyadopt=freeze(B/'root.exact-verification68.adoption.json','CORRECTED_EXACT_VERIFICATION_ADOPTION',True);assert verifyadopt['native_verified'] and verifyadopt['verified_commit']==notes['proof_commit'];l=freeze(B/'exact-science-verification68-corrected/lease.final.json','CORRECTED_CLOSED74_VERIFIER_LEASE',True);assert l['status']=='CLOSED_LAST' and l['VERIFIED'] and l['owned_file_count_including_self']==74;assert sha((B/'exact-science-verification68-corrected/lease.final.json').read_bytes())==verifyadopt['native_lease_RAW_sha256'];assert l['whole_logical_run_sha256']==verifyadopt['native_whole_logical_run_sha256']
for e in l['all_owned_outputs_except_only_self']:
 b=Path(e['path']).read_bytes();assert len(b)==e['raw_bytes'] and sha(b)==e['raw_sha256']
transition=freeze(B/'exact-science-verification68-corrected/transition.receipt.json','PROPER_INDEPENDENT_VERIFIED_TRANSITION_RECEIPT',True)
old=freeze(B/'exact-science-verification/lease.final.json','PRESERVED_OLD_CLOSED131_NEGATIVE',True);assert old['status']=='CLOSED_LAST' and not old['VERIFIED'] and old['owned_file_count_including_self']==131 and old['required_frontier_obstruction_preserved']
alias=freeze(B/'root.energy-alias-overlay68.adoption.json','EXACT_ALIAS_ADOPTION_FINITE_MAPS',True);assert alias['native_whole_logical_run_sha256']==closed[2]['whole_logical_run_sha256'] and alias['only_specific_alias_limitation_closed']
for e in alias['finite_application_maps']:
 for key,hashkey in [('before_snapshot','before_RAW_sha256'),('after_snapshot','after_RAW_sha256')]:
  b=freeze(e[key],'FINITE_ALIAS_'+key.upper());assert sha(b)==e[hashkey]
 assert sha((R/e['canonical_path']).read_bytes())==e['after_RAW_sha256']
rootchecks=[]
for x in notes['checks']:
 rr=freeze(x['receipt']['path'],'REUSED_ROOT_FOREGROUND_CHECK_RECEIPT',True);assert sha((R/x['receipt']['path']).read_bytes())==x['receipt']['raw_sha256'];assert rr['exit_code']==0 and rr['terminal_closed'];streams={}
 for stream in ['stdout','stderr']:
  e=x[stream];b=freeze(e['path'],'REUSED_ROOT_CHECK_'+stream.upper());assert len(b)==e['bytes'] and sha(b)==e['raw_sha256'];streams[stream]=sha(b)
 rootchecks.append({'label':x['label'],'actual_foreground_pid':rr['actual_foreground_pid'],'exit_code':rr['exit_code'],'terminal_closed':rr['terminal_closed'],'receipt_RAW_sha256':x['receipt']['raw_sha256'],'streams_RAW_sha256':streams})
mandatory=json.loads((B/'integration68/mandatory-astis-check-final/receipt.json').read_bytes());current=[]
for e in mandatory['inputs']:
 b=freeze(e['path'],'CURRENT_CANONICAL_OR_INTEGRATION_INPUT_FROM_ROOT_RECEIPT');current.append({'path':e['path'],'at_root_check_RAW_sha256':e['raw_sha256'],'current_RAW_sha256':sha(b),'equal':sha(b)==e['raw_sha256']})
# Only two Frontier Cells receive final administration after the full Lean check.
changed=[e for e in current if not e['equal']];assert len(changed)==3 and {Path(e['path']).name for e in changed}=={'ASTIS-SHARED-hilbert-corrector-square-bound.json','ASTIS-SW-PBPS-sharp-corrector-energy.json','companion-papers-handoff.md'}
def exactdiff(a,b,p=''):
 if type(a)!=type(b):return [{'pointer':p,'before':a,'after':b}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append({'pointer':p+'/'+k,'before':a.get(k,'__ABSENT__'),'after':b.get(k,'__ABSENT__')})
   else:out+=exactdiff(a[k],b[k],p+'/'+k)
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [{'pointer':p,'before':a,'after':b}]
  out=[]
  for i,(x,y) in enumerate(zip(a,b)):out+=exactdiff(x,y,p+'/'+str(i))
  return out
 return [] if a==b else [{'pointer':p,'before':a,'after':b}]
finite_changes=[]
for e in changed:
 snap=next(s['exact_raw_snapshot'] for s in mandatory['input_snapshots'] if s['original']['path']==e['path']);before=freeze(snap['path'],'EXACT_BEFORE_ROOT_CHECK_FINITE_CHANGED_INPUT');after=Path(e['path']).read_bytes();assert sha(before)==e['at_root_check_RAW_sha256']
 if e['path'].endswith('.json'):delta=exactdiff(json.loads(before),json.loads(after))
 else:
  import difflib
  delta=list(difflib.unified_diff(before.decode().splitlines(),after.decode().splitlines(),fromfile='at mandatory check',tofile='current',n=3))
 finite_changes.append(dict(e,exact_before_snapshot=snap['path'],changes=delta))
write('exact-three-postcheck-finite-maps.json',{'status':'23_MATCHING_CURRENT_INPUTS_PLUS_EXACT_TWO_CELL_AND_HANDOFF_MAPS','actual_pid':os.getpid(),'finite_changes':finite_changes,'Lean_source_toolchain_dependencies_publication_lessons_and_audits_unchanged':True,'broad_exclusions':False})
for e in notes['final_cells']:
 b=freeze(e['path'],'EXACT_FINAL_CELL_RAW_AFTER_ADMIN');assert sha(b)==e['raw_sha256'] and len(b)==e['bytes'];assert e in admin['cells']
for p in ['research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.md','website/scripts/publication_reader.py','website/scripts/underlying_lean_graph.py','tools/astis_publication.py','tools/astis_semantic_roundtrip_core.py','tools/astis_site.py','website/scripts/declaration_lessons.py','website/scripts/inline_lean.py']:freeze(p,'CURRENT_SCOPED_CARD_OR_VALIDATOR_CODE')
graph=freeze('_site/data/underlying-lean-graph.json','EXACT_CURRENT_FULL_GRAPH',True);site=freeze('_site/data/site-data.json','CURRENT_GENERATED_SITE_INVENTORY',True);freeze('_site/lean-foundations.html','CURRENT_GRAPH_READER_HTML');freeze('_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html','CURRENT_COMPANION_READER_HTML')
assert sha((R/notes['current_graph']['path']).read_bytes())==notes['current_graph']['raw_sha256']=='ab01e1c4a11eb08eda0ec239840552582007309c13d14d6a0197067272f261ad'
for e in visual['capture_files']:
 b=freeze(e['path'],'FINITE_ROOT_VISUAL_CAPTURE_INPUT');assert len(b)==e['bytes'] and sha(b)==e['raw_sha256']
for p in sorted((B/'integration68/visual68').glob('inspection-*')):freeze(p,'CONTACT_SHEET_OR_CONTACT_MANIFEST')
prior=freeze(notes['reused_python_tests']['prior_receipt']['path'],'UNCHANGED_CODE_REUSED_296_TEST_RECEIPT',True);assert prior['actual_foreground_pid']==1392 and prior['exit_code']==0 and prior['terminal_closed']
for k in ['stdout','stderr']:
 b=freeze(prior[k]['path'],'REUSED_296_TEST_'+k.upper());assert sha(b)==prior[k]['raw_sha256']
delta=subprocess.run(['git','diff',prior['checked_science_parent'],'--','tools','website/scripts'],cwd=R,capture_output=True,check=True);assert not delta.stdout;write('regression-code-unchanged.receipt.json',{'actual_reader_pid':os.getpid(),'command':['git','diff',prior['checked_science_parent'],'--','tools','website/scripts'],'exit_code':delta.returncode,'stdout_RAW_sha256':sha(delta.stdout),'stderr_RAW_sha256':sha(delta.stderr),'count':296,'rerun':False,'prior_actual_foreground_pid':1392})
sys.path[:0]=[str(R/'tools'),str(R/'website/scripts')]
import publication_reader as pr
import underlying_lean_graph as ug
import astis_publication as pub
computed=pr.graph_input_digest();assert computed==graph['publication_inputs_sha256']==notes['publication_inputs_sha256']=='1e926312e39b1a7e55a8b6ad3826af6514658b05aa374ef6de1b58ec0dae7136'
errors=pr.validate_graph(graph,site);assert not errors;ug.validate(R/'_site',graph)
cells=[Path(e['path']).stem for e in notes['final_cells']];reports=[pub.graph_report(c,R/'_site') for c in cells]
for c,e in zip(cells,notes['final_cells']):assert sha((R/e['path']).read_bytes())==e['raw_sha256']
names=['AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.quadratic_corrector_bound_of_square_identity','AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound'];nodes={x['id']:x for x in graph['nodes']};edges={(x['source'],x['target'],x['relation']) for x in graph['edges']}
for name in names:
 n=nodes['decl:'+name];assert n['kind']=='declaration' and n['status']=='compiled';module=name.rsplit('.',1)[0];assert ('module:'+module,'decl:'+name,'declares') in edges
leaf,actual=['decl:'+n for n in names];parent='decl:AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation'
assert (leaf,actual,'source reference (scanner)') in edges and (parent,actual,'source reference (scanner)') in edges;assert not any((a,b,'depends-on') in edges for a,b in [(leaf,actual),(parent,actual)]);assert ('module:'+names[0].rsplit('.',1)[0],'module:'+names[1].rsplit('.',1)[0],'imports') in edges
assert 'decl:Tests.ProximalBPSSharpCorrectorEnergy.genuine_actual_modified_energy_equivalence' not in nodes
assert len(site['registry_declarations'])==518 and sum(x['status']=='formalizedLocal' for x in site['registry_declarations'])==516
out={'status':'INDEPENDENT_CURRENT_GRAPH_FULL_VALIDATOR_AND_TWO_CELL_REPORTS_PASS','actual_checker_pid':os.getpid(),'HEAD':notes['proof_commit'],'current_graph_RAW_sha256':notes['current_graph']['raw_sha256'],'recomputed_publication_inputs_sha256':computed,'full_publication_graph_validator_errors':errors,'full_underlying_graph_validator':'PASS_READ_ONLY','exact_final_cell_RAW':notes['final_cells'],'two_cell_graph_reports':reports,'two_exact_nodes':[nodes[leaf],nodes[actual]],'all_incident_edges':[e for e in graph['edges'] if e['source'] in {leaf,actual} or e['target'] in {leaf,actual}],'registry_formalizedLocal':516,'registry_all_entries_including_two_port_candidates':518,'scanner_precision_debt':'LogConcaveOn.prod reference is a .prod name-scan artifact, labelled scanner reference and dashed. It is not an actual theorem dependency or proof certificate. Genuine source dependencies are exact module imports plus compiled parent/leaf use independently source-reviewed.','Test_scope':'Genuine original-input compiled Test consumer retained; no invented production graph node.','old_source_inputs_not_declared_all_current':'Reuse CLOSED363 source science and CLOSED80 alias approval, then exact current finite maps. Old146 native input entries are not relabelled current RAW.','own_compiler_started':False,'canonical_writes':False,'full_Exposition_Seal':False,'PURIFIED':False,'full_paper_or_Goal_complete':False}
write('current-graph-and-integration.readback.json',out);write('current-root-check-inputs.finite-map.json',{'matching_current_inputs':len(current)-3,'changed_current_inputs':changed,'all_rows':current,'final_current_cells':notes['final_cells'],'three_finite_changes_only_final_cell_admin_and_handoff_prose_after_full_root_check':True});write('reused-root-checks.terminal-map.json',{'entries':rootchecks,'all_authoritative_foreground_EXIT0':True,'own_full_root_Lean_rerun':False});write('native-closures-reuse.json',{'closed':closed,'corrected_verification_CLOSED74':verifyadopt,'old_CLOSED131_negative_preserved':{'status':old['status'],'VERIFIED':old['VERIFIED'],'required_frontier_obstruction_preserved':old['required_frontier_obstruction_preserved']},'source_math_reproved':False,'new_blind_decode':False});write('stage1-inputs.manifest.json',{'schema':1,'actual_checker_pid':os.getpid(),'entries':rows,'entry_count':len(rows),'finite_named_inputs_only':True,'no_future69_candidate_read':True})
print('REPOSITORY_GRAPH_STAGE1_EXIT0',os.getpid(),len(rows),'INPUTS','CURRENT_GRAPH_FULL_VALIDATOR_PASS','2_CELLS_PASS',computed)
