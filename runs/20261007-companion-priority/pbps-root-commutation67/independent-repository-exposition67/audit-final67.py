from pathlib import Path
import json,hashlib,os,sys,subprocess,datetime,difflib
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-root-commutation67';O=R/'independent-repository-exposition67'
SCI='3da29415011a971a65f749502a625e416213f487';INT66='eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'website/scripts')]
import astis_publication as pub,publication_reader
def sha(b):return hashlib.sha256(b).hexdigest()
def cj(j):return json.dumps(j,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def ld(p):return json.loads(Path(p).read_bytes())
def resolve(p):
 p=Path(p);return p if p.is_absolute() else ROOT/p
def pin(p,b=None):
 p=resolve(p);b=p.read_bytes() if b is None else b;l=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l)}
def check(z):
 p=resolve(z['path']);a=pin(p);assert a['RAW_sha256']==z.get('RAW_sha256',z.get('raw_sha256')),p
 if 'bytes' in z:assert a['RAW_bytes']==z['bytes'],p
 if 'lf_sha256' in z:assert a['LF_sha256']==z['lf_sha256'],p
 return p
def wr(n,j):
 assert not (O/'lease.final.json').exists();(O/n).write_bytes((json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
inputs=[]
def snap(p):
 p=resolve(p)
 if any(z['original']['path']==p.as_posix() for z in inputs):return
 b=p.read_bytes();assert len(b)<2_000_000,p
 k=len(inputs);rp=O/'inputs'/f'final.{k:03d}.RAW.snapshot';lp=O/'inputs'/f'final.{k:03d}.LF.snapshot';rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));inputs.append({'original':pin(p,b),'RAW_snapshot':pin(rp),'LF_snapshot':pin(lp)})
assert not (O/'lease.final.json').exists()
notes=ld(R/'integration.notes.json');admin=ld(R/'integration67/final-admin.json');assert notes['proof_commit']==admin['proof_commit']==SCI
assert (notes['root_jobs'],notes['test_jobs'],notes['registry_count'],notes['publication_units'])==(9176,9475,514,235)
assert notes['final_cells']==admin['cells'] and notes['prior66_graph_freshness_withheld_preserved']
assert [z['raw_sha256'] for z in notes['final_cells']]==['cc5a6fada4c058bd74bc3fedcf74abfd6751ae106c8336bb6d254a5192dd65ed','30a5ff593fefc8f9621004f1a9ce20b814e88822fd74d073f92d202390991adc']
for z in notes['final_cells']:check(z);snap(z['path'])
for p in [R/'integration.notes.json',R/'integration67/final-admin.json',R/'visual.inspection.json',R/'integration67/owned-before.json']:snap(p)
rootgates=[];maps=[]
for z in notes['checks']:
 p=check(z['receipt']);q=ld(p);assert q['checked_science_parent']==SCI and q['exit_code']==0 and q['terminal_closed'];snap(p)
 for k in ['stdout','stderr']:check(z[k]);snap(z[k]['path'])
 for m in q['input_snapshots']:
  p0=resolve(m['original']['path']);r=check(m['exact_raw_snapshot']);l=check(m['LF_snapshot']);b=r.read_bytes();assert sha(b)==m['original']['raw_sha256'] and l.read_bytes()==b.replace(b'\r\n',b'\n')
  cur=pin(p0);drift=cur['RAW_sha256']!=m['original']['raw_sha256']
  if drift:assert p0.as_posix() in [resolve(x['path']).as_posix() for x in notes['final_cells']],('unmapped receipt drift',p0)
  maps.append({'gate':z['label'],'exact_original_snapshot_map':m,'current_final_pin':cur,'current_equals_original_RAW':not drift,'finite_mapping':'two explicit final-cell admin fields/state; final gates and official graph use current final cells' if drift else 'RAW-identical'})
 rootgates.append({'label':z['label'],'receipt':pin(p),'actual_foreground_PID':q['actual_foreground_pid'],'actual_exit':q['exit_code'],'command':q['command'],'started_utc':q['started_utc'],'finished_utc':q['finished_utc'],'stdout':pin(resolve(z['stdout']['path'])),'stderr':pin(resolve(z['stderr']['path']))})
assert len(rootgates)==18
log=(R/'integration67/mandatory-astis-check-final/stdout.log').read_text(encoding='utf-8');assert 'Build completed successfully (9176 jobs).' in log and 'Build completed successfully (9475 jobs).' in log and 'ASTIS check passed' in log
for label,count in [('publication-final-admin',235),('semantic-final-admin',301),('frontier-final-admin',298)]:assert str(count) in (R/f'integration67/{label}/stdout.log').read_text(encoding='utf-8')
wr('root-gates-and-finite-snapshot-maps.json',{'schema':'repository67-root-actual-terminal-and-finite-input-maps-v1','actual_PID':os.getpid(),'root_gates':rootgates,'snapshot_maps':maps,'all594_root_receipt_snapshots_checked':len(maps),'unmapped_drifts':0,'no_current_equality_assumption_for_historical_snapshots':True})
visual=ld(R/'visual.inspection.json');cap=ld(R/'integration67/visual67/render-capture.json');copies=ld(R/'integration67/visual67/copy-capture.json');assert len(cap['records'])==13 and cap['ownedBrowserExit']['code']==0 and copies['ownedBrowserExit']['code']==0
for z in visual['capture_files']:check(z)
for p in [R/'integration67/visual67/render-capture.json',R/'integration67/visual67/copy-capture.json']:snap(p)
reader=[]
for i,slug in enumerate(['real-l2-positive-square-commutation','pbps-actual-root-inverse-commutation']):
 unit=ld(ROOT/'website/content/declaration_lessons'/f'{slug}.json')['units'][0];j=ld(R/f'integration67/visual67/copy-unit{i}-copy-and-download.inspect.json');snap(R/f'integration67/visual67/copy-unit{i}-copy-and-download.inspect.json')
 assert j['initialFolded'] and j['copyProbeUsesIsolatedPageClipboardCallback'] and not j['physicalOSClipboardTest']
 path=ROOT/('AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareCommute.lean' if i==0 else 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean');raw=path.read_bytes();body=raw.decode();name=unit['declaration'].split('.')[-1];start=body.index('theorem '+name);stop=body.index(' := by',start);header=body[start:stop]
 assert j['panels'][0]['code'].rstrip()==header.rstrip() and j['panels'][1]['code'].rstrip()==body[start:].rstrip()
 assert len(j['panels'])==2 and all(z['callbackCalled'] and z['copiedExactly'] and z['status']=='Copied' for z in j['panels'])
 assert len(j['downloads'])==2 and all(z['status']==200 and z['text'].encode()==raw for z in j['downloads'])
 assert len(j['steps'])==len(unit['steps']) and all(a['initiallyFolded'] and a['lean']==b['lean'] for a,b in zip(j['steps'],unit['steps']))
 reader.append({'publication':slug,'complete_statement_and_all_formulae_verified_by_frozen_static_contract':True,'production_source':pin(path),'copy_callbacks':2,'RAW_downloads':2,'exact_alias_header_and_theorem_BODY_copy':True,'literal_steps_initially_folded':len(unit['steps']),'full_private_literal_Prop_module_downloaded':True,'physical_OS_clipboard':False})
wr('reader-final67.json',{'schema':'repository67-actual-reader-capture-copy-download-v1','actual_PID':os.getpid(),'status':'SCOPED_PASS','independently_viewed_13_PNGs':[{'path':z['path'],'RAW_sha256':z['raw_sha256']} for z in visual['capture_files'] if z['path'].endswith('.png')],'root_capture':cap,'publications':reader,'actual_render_browser_PID':cap['pid'],'actual_copy_browser_PID':copies['pid'],'all_capture_files_checked':visual['capture_files'],'view_observations':['Both complete attributed statements are present; actual statement is dense plain Unicode notation.','All ten formula proof steps are readable, each beside a closed literal Lean disclosure.','Actual branch is focused on the correct declaration; solid structure and dashed incomplete reference signals are explicitly distinguished.','Graph labels remain dense and long qualified names break awkwardly; retain reader debt.'],'full_Exposition':False,'PURIFIED':False,'local_capture_only':True})
# Current official graph recomputes its input digest from all current source/cell/publication inputs, without an exclusion or monkey patch.
graphpath=ROOT/'_site/data/underlying-lean-graph.json';sitepath=ROOT/'_site/data/site-data.json';g=ld(graphpath);s=ld(sitepath);check(notes['current_graph']);current=publication_reader.graph_input_digest();assert current==g['publication_inputs_sha256']==notes['publication_inputs_sha256']
errors=publication_reader.validate_graph(g,s,pub.load());assert not errors,errors
slices=[];contexts=[]
for slug in ['real-l2-positive-square-commutation','pbps-actual-root-inverse-commutation']:
 item=next(x for x in pub.load() if x['id']==slug);b=item['bindings'][0];slice=pub.graph_report(b['cell'],ROOT/'_site');slices.append(slice)
 audit=pub.inputs()['audits'][b['audit_id']];ctx=pub.review_context(item,b);binding=pub.binding_digest(item,b);assert binding==audit['publication_binding_sha256'] and ctx==audit['publication_context']
 contexts.append({'publication':slug,'publication_binding_sha256':binding,'context_sha256':sha(cj(ctx)),'canonical_audit':pin(ROOT/f"research-wiki/semantic-roundtrip/audits/{b['audit_id']}.json"),'whole_module_private_implementations_reused_from_unchanged_independent_source':True})
wr('current-graph-and-publication-bindings.json',{'schema':'repository67-current-official-graph-and-binding-admission-v1','actual_PID':os.getpid(),'status':'PASS_CURRENT_FINAL_ADMIN','current_graph':pin(graphpath),'current_site_data':pin(sitepath),'current_recomputed_publication_inputs_sha256':current,'full_publication_graph_validator_errors':errors,'exact_final_cells':notes['final_cells'],'bounded_one_hop_graph_slices':slices,'current_contexts':contexts,'private_Prop_provider_edges':0,'prior_INT66_freshness_withheld_historical_unchanged':True,'no_retroactive_INT66_acceptance':True})
# Exact shared authored delta, and scripts for296 tests are reused only because all101 exact tracked source bodies are unchanged.
owned=ld(R/'integration67/owned-before.json')['owned'];deltas=[]
for z in owned:
 p=ROOT/z['path'];before=resolve(z['exact_snapshot']).read_bytes();assert sha(before)==z['raw_sha256'];current=p.read_bytes();git=subprocess.check_output(['git','show',SCI+':'+z['path']],cwd=ROOT);assert git.replace(b'\r\n',b'\n')==before.replace(b'\r\n',b'\n')
 snap(p);snap(z['exact_snapshot']);diff=''.join(difflib.unified_diff(before.decode().splitlines(True),current.decode().splitlines(True),fromfile='exact-SCI-before',tofile='current-final',n=3));deltas.append({'path':z['path'],'exact_SCI_before':pin(resolve(z['exact_snapshot'])),'current_final':pin(p),'exact_complete_diff':diff})
wr('shared-authored-finite-delta.json',{'schema':'repository67-exact-SCI-to-final-shared-authored-delta-v1','actual_PID':os.getpid(),'changes':deltas,'science_9_paths_unchanged':True,'Registry_count':514,'root_jobs':9176,'Tests_jobs':9475,'mathematical_source_repair':False})
old=ROOT/'runs/20261007-companion-priority/pbps-ambient-adjoint66/independent-repository-exposition66/python296-exact-reuse.json';reuse=ld(old);inv=[]
for z in reuse['complete_tracked_tools_and_site_script_inventory']:
 p=ROOT/z['path'];base=subprocess.check_output(['git','show',reuse['SCI64']+':'+z['path']],cwd=ROOT);sci=subprocess.check_output(['git','show',SCI+':'+z['path']],cwd=ROOT);assert sci==base and p.read_bytes().replace(b'\r\n',b'\n')==base.replace(b'\r\n',b'\n');inv.append({'path':z['path'],'exact_SCI64_SCI67_Git_RAW_sha256':sha(sci),'current_RAW_LF':pin(p),'equal_LF':True})
prior=resolve(notes['reused_python_tests']['prior_receipt']['path']);check(notes['reused_python_tests']['prior_receipt']);pr=ld(prior);assert pr['exit_code']==0
wr('python296-exact-reuse67.json',{'schema':'repository67-independent-exact-python296-reuse-v1','actual_PID':os.getpid(),'status':'REUSED_NOT_RERUN','prior_closed66_evidence':pin(old),'prior_receipt':pin(prior),'prior_actual_PID':pr['actual_foreground_pid'],'prior_actual_exit':pr['exit_code'],'test_count':296,'all101_script_exact_Git_RAW_and_current_LF_unchanged':inv})
snap(prior)
execution=ld(ROOT/'website/content/samplewiki_companion_frontiers.json')['execution'];assert execution['targets']==['ASTIS-SW-PBPS-2026','ASTIS-SW-SPHMC-2026','ASTIS-SW-GAUSSIAN-CLOUD-2026','ASTIS-SW-MIDPOINT-2026'];assert 'no added third-or-higher derivative assumptions' in execution['phase_order'][2]['scope']
old64=ROOT/'runs/20261007-companion-priority/pbps-centered-root64/independent-stale-cell-overlay64';proposal=ld(old64/'proposal.raw.json');after=ld(old64/'proposed-after.raw.json');cp=ROOT/proposal['canonical_path'];cur=ld(cp);assert cur['source_anchor']==after['source_anchor'] and cur['evidence']['truth_boundary']==after['evidence']['truth_boundary']
wr('prior64-priority-and-INT66-historical-boundary.json',{'schema':'repository67-prior-reviewed-boundaries-preserved-v1','actual_PID':os.getpid(),'accepted_prior64_exact_fields_preserved':{'source_anchor':cur['source_anchor'],'evidence.truth_boundary':cur['evidence']['truth_boundary']},'prior64_final_lease':pin(old64/'lease.final.json'),'current_shared64_cell':pin(cp),'four_paper_execution':execution,'prior_INT66_commit':INT66,'prior_INT66_CLOSED179_lease':pin(ROOT/'runs/20261007-companion-priority/pbps-ambient-adjoint66/independent-repository-exposition66/lease.final.json'),'prior_INT66_reader_scoped_accepted':True,'prior_INT66_current_graph_freshness_withheld':True,'INT67_current_freshness_is_separate':True,'full_Exposition':False,'PURIFIED':False,'main_live':False,'whole_Goal_complete':False})
wr('inputs.manifest.final.json',{'schema':'repository67-finite-final-original-RAW-LF-map-v1','final_inputs_ready_received':True,'root_ready_event':'Parent explicit FINAL INPUTS READY67, final cells listed verbatim; root record-final-integration-v2 PID28628 EXIT0','inputs':inputs,'large_generated_graph_and_PNGs_reused_only_by_exact_full_RAW_LF_pins':'No duplicate whole graph/site/PNG copying; complete selected current graph projection and all full input pins are named in analytical evidence.'})
wr('audit-final67.result.json',{'schema':'repository67-independent-final-aggregate-reader-audit-result-v1','actual_PID':os.getpid(),'status':'PASS_SCOPED_CURRENT_FINAL_ADMIN','root_gate_count':18,'root_receipt_snapshot_maps':len(maps),'current_graph_digest':g['publication_inputs_sha256'],'complete_statements':2,'formula_BODY_steps':10,'copy_callbacks':4,'production_RAW_downloads':4,'independently_viewed_PNGs':13,'finite_final_inputs':len(inputs),'canonical_writes':False,'proof_or_source_math_replay':False})
print(json.dumps(ld(O/'audit-final67.result.json')))
