import os,sys,json,pathlib,hashlib,subprocess,datetime
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-ambient-adjoint66';O=R/'independent-repository-exposition66';INT='eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176';SCI='a115115d42b3fa2b67885d87fe4d5300af36fcd1'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'website/scripts')]
import astis_publication as pub,astis_site as site,publication_reader
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def pin(p,b=None):
 p=pathlib.Path(p);b=p.read_bytes() if b is None else b;v=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(v),'LF_sha256':sha(v)}
def write(n,j):(O/n).write_bytes(json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2).encode()+b'\n')
def match(p,z):
 b=pathlib.Path(p).read_bytes();assert sha(b)==z['raw_sha256'];assert len(b)==z['bytes'];assert sha(b.replace(b'\r\n',b'\n'))==z['lf_sha256'];return b
pid=os.getpid();print(json.dumps({'actual_foreground_PID':pid,'stage':'reader-native-audit'}),flush=True)
visual=load(R/'visual.inspection.json');capture=load(R/'integration66/visual66/render-capture.json');copy=load(R/'integration66/visual66/copy-actual-copy-and-download.inspect.json')
for z in visual['capture_files']:match(ROOT/z['path'],z)
assert len(capture['records'])==8 and capture['ownedBrowserExit']==0
assert copy['initialFolded'] and not copy['physicalOSClipboardTest'] and copy['copyProbeUsesIsolatedPageClipboardCallback']
lesson_path=ROOT/'website/content/declaration_lessons/pbps-ambient-adjoint-corrector.json';unit=load(lesson_path)['units'][0]
main=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean';test=ROOT/'Tests/ProximalBPSAmbientAdjointCorrector.lean'
body=main.read_text(encoding='utf-8');header=body[body.index('theorem actual_ambient_adjoint_centered_decomposition'):body.index(' := by',body.index('theorem actual_ambient_adjoint_centered_decomposition'))]
proof=body[body.index(' := by',body.index('theorem actual_ambient_adjoint_centered_decomposition'))+len(' := by\n'):];proof=proof[:proof.index('\nend AutoSamplingTheory')].rstrip()
assert len(copy['panels'])==2
assert copy['panels'][0]['code'].rstrip()==header.rstrip()
assert copy['panels'][1]['code'].rstrip()==(header+' := by\n'+proof).rstrip()
for z in copy['panels']:assert z['callbackCalled'] and z['copiedExactly'] and z['status']=='Copied'
for z in copy['downloads']:assert z['status']==200 and z['text'].encode('utf-8')==main.read_bytes()
steps=[]
for i,(s,c) in enumerate(zip(unit['steps'],copy['steps']),1):
 z=s['lean_source_region'];p=ROOT/z['path'];raw=p.read_bytes();lines=raw.splitlines(keepends=True);literal=b''.join(lines[z['start_line']-1:z['end_line']]);assert sha(raw)==z['source_raw_sha256'] and sha(literal)==z['exact_code_raw_sha256']
 assert c['initiallyFolded'] and c['lean']==s['lean'];assert s['lean'].encode()==literal
 steps.append({'step':i,'title':s['title'],'formula':s['formula'],'literal_BODY_region':z,'captured_initially_folded':True,'captured_Lean_equals_canonical_lesson_equals_literal_BODY':True})
assert len(steps)==6
pubpath=ROOT/'website/content/publications/pbps-ambient-adjoint-corrector.json';auditpath=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSAmbientAdjointCorrector.json'
science=[]
for p in [main,test,lesson_path,pubpath,auditpath]:
 rel=p.relative_to(ROOT).as_posix();a=subprocess.check_output(['git','show',SCI+':'+rel],cwd=ROOT);b=subprocess.check_output(['git','show',INT+':'+rel],cwd=ROOT);assert a==b==p.read_bytes();science.append(pin(p,b))
ctx=load(O/'independent-gates-v3/publication-current-context/stdout.RAW.log');bindings=load(R/'exact-science-verification66/bindings.result.json')
assert ctx['publication_binding_sha256']==bindings['publication_binding_sha256'];assert sha(canon(ctx['publication_context']))==bindings['publication_context_sha256']
dec=R/'anonymous-decoder';cl=load(dec/'closure_manifest.json');lease=load(dec/'lease.json');run=load(dec/'final_run.json');h=run.pop('run_sha256');assert sha(canon(run))==h==lease['run_sha256']==bindings['native_decoder20_whole']
for z in cl['artifacts']:
 p=dec/z['path'];b=p.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['raw_sha256']
for k,n in [('closure_manifest_raw_sha256','closure_manifest.json'),('final_run_raw_sha256','final_run.json'),('self_manifest_raw_sha256','self_manifest.json'),('terminal_manifest_raw_sha256','terminal_manifest.json'),('reconstruction_payload_raw_sha256','reconstruction_payload.json')]:assert sha((dec/n).read_bytes())==lease[k]
assert lease['status']=='CLOSED_LAST' and len(cl['artifacts'])+2==20
extras=sorted({p.name for p in dec.iterdir() if p.is_file()}-{z['path'] for z in cl['artifacts']}-{'closure_manifest.json','lease.json'})
assert extras==['decoded0.root-adapter.json','initial-lease.raw.snapshot.json','packet0.json','parent-lease.open.json']
write('reader-and-native-decoder.json',{'schema':'repo66-exact-reader-and-blind-native-bindings-v1','actual_foreground_PID':pid,'status':'PASS','SCI_INT_current_science_files_RAW_identical':science,'current_publication_binding_sha256':ctx['publication_binding_sha256'],'current_publication_context_sha256':sha(canon(ctx['publication_context'])),'eight_PNGs_viewed_by_independent_reviewer':True,'render_browser_PID':capture['pid'],'render_browser_exit':capture['ownedBrowserExit'],'render_records':capture['records'],'capture_file_pins':visual['capture_files'],'copy_callbacks':2,'physical_OS_clipboard_test':False,'RAW_downloads':2,'RAW_download_utf8_bytes_each':len(main.read_bytes()),'JS_reported_download_bytes_is_decoded_codepoint_count':len(copy['downloads'][0]['text']),'exact_copied_alias_header_and_theorem_BODY':True,'private_literal_Prop_expansions_reused_as_whole_module_review_not_math_providers':True,'six_literal_BODY_steps':steps,'blind_native_files':20,'blind_root_copy_extra_exact_names':extras,'blind_lease':pin(dec/'lease.json'),'blind_whole_logical_run_sha256':h,'blind_complete_RAW':pin(dec/'reconstruction_payload.json'),'full_Exposition':False,'PURIFIED':False,'local_capture_only':True,'reader_debts':['Dense graph and broken long qualified-name wrapping.','Inherited underscored/plain-Unicode statement notation and dense statement.','Full literal private statements/complete Lean disclosure placement remain under ungranted full Exposition Seal.','First-corrector geometry and norm budget only, no sharp B23/B21/dynamics/cost/composition.']})
# Finite exact commit source inventory. Never exclude a folder or delete a future input.
tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',INT],cwd=ROOT).decode().splitlines())
paths=[ROOT/'AutoSamplingTheory.lean',*sorted((ROOT/'AutoSamplingTheory').rglob('*.lean')),ROOT/'Tests.lean',*sorted((ROOT/'Tests').rglob('*.lean')),ROOT/'lakefile.lean',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
d=hashlib.sha256();exact=[];future=[]
for p in paths:
 if not p.exists():continue
 rel=p.relative_to(ROOT).as_posix()
 if rel not in tracked:future.append(pin(p));continue
 b=p.read_bytes();gb=subprocess.check_output(['git','show',INT+':'+rel],cwd=ROOT);assert b==gb,(rel,'unmapped tracked source RAW drift')
 d.update(rel.encode()+b'\0'+b+b'\0');exact.append(pin(p,b))
assert {pathlib.Path(x['path']).relative_to(ROOT).as_posix() for x in future}=={'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareCommute.lean','Tests/ProximalBPSActualRootCommutation.lean'}
data=pub.inputs();items=pub.load();cells={b['cell']:data['cells'].get(b['cell']) for i in items for b in i['bindings']}
graphpath=ROOT/'_site/data/underlying-lean-graph.json';sitepath=ROOT/'_site/data/site-data.json';g=load(graphpath);s=load(sitepath)
current_digest=pub.digest({'lean':d.hexdigest(),'items':items,'cells':cells})
receipt=load(R/'integration66/official-graph-ci-output-final-v2/receipt.json');z=next(x for x in receipt['input_snapshots'] if x['original']['path'].endswith('ASTIS-SW-PBPS-ambient-adjoint-corrector.json'))
hist=load(z['exact_raw_snapshot']['path']);hist['__path__']='research-wiki/frontier-cells/ASTIS-SW-PBPS-ambient-adjoint-corrector.json';cells['ASTIS-SW-PBPS-ambient-adjoint-corrector']=hist
historical_digest=pub.digest({'lean':d.hexdigest(),'items':items,'cells':cells});assert historical_digest==g['publication_inputs_sha256'];assert current_digest!=historical_digest
actualfunc=publication_reader.graph_input_digest
try:
 publication_reader.graph_input_digest=lambda: historical_digest
 errors=publication_reader.validate_graph(g,s,[i for i in items if i['id']=='pbps-ambient-adjoint-corrector']);assert not errors,errors
 publication_reader.graph_input_digest=lambda: current_digest
 errors_current=publication_reader.validate_graph(g,s,[i for i in items if i['id']=='pbps-ambient-adjoint-corrector']);assert errors_current==['Generated contribution graph is stale; rebuild the site'],errors_current
finally:publication_reader.graph_input_digest=actualfunc
target='decl:AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition'
incident=sorted([e for e in g['edges'] if target in (e['source'],e['target'])],key=lambda e:(e['relation'],e['source'],e['target']))
rootreport=load(R/'integration66/cell-graph-check-actual/stdout.log');assert incident==rootreport['contributions'][0]['connections']
write('graph-finite-freshness-diagnosis.json',{'schema':'repo66-exact-INT-versus-historical-generated-graph-v1','actual_foreground_PID':pid,'generated_graph':pin(graphpath),'generated_site_data':pin(sitepath),'exact_tracked_source_inventory':exact,'exact_future_untracked_files_outside_INT66':future,'exact_INT_source_digest':d.hexdigest(),'generated_graph_digest':g['publication_inputs_sha256'],'historical_pre_final_cell_digest':historical_digest,'exact_INT_current_cell_digest':current_digest,'historical_cell_explicit_receipt_snapshot':z,'historical_generated_target_coverage_PASS':True,'current_INT_freshness_PASS':False,'current_freshness_error':errors_current,'affected_incident_edges_equal_root_observed_PASS':incident,'private_Prop_math_provider_edges':0,'future67_credit':False,'repair_kind':'process-only generated graph freshness after exact cell metadata freeze','repair_applied_by_reviewer':False,'mathematical_source_repair':False,'required_future_action':'Root must regenerate/recheck an exact66 output after current metadata freeze, or retain explicitly historical rendered/graph admission with current freshness debt. No proof67/main/live/full Exposition claim.'})
old=ROOT/'runs/20261007-companion-priority/pbps-centered-root64/independent-stale-cell-overlay64';proposal=load(old/'proposal.raw.json');after=load(old/'proposed-after.raw.json');cp=ROOT/proposal['canonical_path'];current=load(cp)
assert current['source_anchor']==after['source_anchor'] and current['evidence']['truth_boundary']==after['evidence']['truth_boundary']
exec_path=ROOT/'website/content/samplewiki_companion_frontiers.json';execution=load(exec_path)['execution'];assert execution['targets']==['ASTIS-SW-PBPS-2026','ASTIS-SW-SPHMC-2026','ASTIS-SW-GAUSSIAN-CLOUD-2026','ASTIS-SW-MIDPOINT-2026']
assert 'no added third-or-higher derivative assumptions' in execution['phase_order'][2]['scope']
write('prior64-and-four-paper-priority.json',{'schema':'repo66-prior64-fields-and-user-priority-preservation-v1','actual_foreground_PID':pid,'prior64_review_decision':pin(old/'decision.json'),'prior64_review_lease':pin(old/'lease.final.json'),'exact_accepted_prior64_after':pin(old/'proposed-after.raw.json'),'current_cell':pin(cp),'exact_fields_preserved':{'source_anchor':current['source_anchor'],'evidence.truth_boundary':current['evidence']['truth_boundary']},'canonical_D1_spectral_unique_root_background_vs_ASTIS_auxiliary_order_distinction':True,'execution':execution,'current_execution_file':pin(exec_path),'status':'PASS'})
print(json.dumps({'actual_foreground_PID':pid,'reader':'PASS_BOUNDED','native_decoder20':'PASS','graph':'HISTORICAL_COVERAGE_PASS_CURRENT_FRESHNESS_DEBT','prior64_priorities':'PASS'}))
