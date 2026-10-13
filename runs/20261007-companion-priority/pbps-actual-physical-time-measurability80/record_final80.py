"""Bind terminal local checks and distinguish remaining reader/main boundaries."""
from pathlib import Path
import datetime,hashlib,json,sys
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80');out=r/'integration80'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
labels=['canonical-lean-gate','python-compile','contributor','publication','semantic','frontier','site-build','underlying-graph','graph-check','site-check','diff-check','ci-full-base-publication']
checks=[]
for label in labels:
 p=out/label/'receipt.json';a=load(p);assert a['terminal_closed'] and a['exit_code']==0,label
 checks.append(dict(label=label,receipt=pin(p),stdout=a['stdout'],stderr=a['stderr']))
sys.path.insert(0,str(Path.cwd()/'tools'));sys.path.insert(0,str(Path.cwd()/'website/scripts'))
import astis_site,astis_advance as advance,publication_reader,underlying_lean_graph
gate=load('.astis/site-lean-gate.json');assert gate['passed'] and gate['source_digest']==astis_site.source_digest()
graph=load('_site/data/underlying-lean-graph.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
underlying_lean_graph.validate(Path('_site'),graph)
claim=load(r/'claim.json');state=advance.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED'
assert any(n.get('id')=='decl:'+claim['target_declarations'][0] for n in graph['nodes'])
lanes=[s['advance_id'] for s in advance.current_advances().values() if s['state']=='STABILIZING'];assert lanes==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
admin=load(out/'final-admin.json');scope=load(out/'integration-scope.json')
note=dict(status='LOCAL_SHARED_AGGREGATE_AND_GENERATED_READER_GATES_PASS_VISUAL_PENDING',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),science_commit=scope['science_commit'],independent_verifier='/root/exact_verify77',verification=pin(r/'exact-commit-verification80/verified.json'),root_jobs=admin['root_jobs'],test_jobs=admin['test_jobs'],registry_count=admin['registry_count'],checks=checks,lean_source_digest=gate['source_digest'],publication_inputs_sha256=graph['publication_inputs_sha256'],current_graph=pin('_site/data/underlying-lean-graph.json'),graph_delta='One actual jointly measurable physical-time phase declaration with AE interpolation and initialization, consuming actual harmonic flow, finite recursion, positive input support and interval coverage. No conceptual mirror.',actual_visual_inspection=dict(static_svg=pin('docs/module-graph.svg'),static_raster=pin(out/'static-svg/module-graph.png'),static_svg_viewed_by_root=True,browser_page_and_interactive_branch='pending: available bound browser surface has no inspectable tab',full_Exposition_Seal=False),sole_stabilization_owner=lanes[0],state_distinctions=dict(proved_locally=True,independently_verified=True,local_aggregate_and_generated_site_gates=True,stabilized=False,merged=False,purified=False,live_verified=False,main_theorem_complete=False),remaining=['Path regularity/adaptedness/Markov/transition kernel/invariance/hypocoercivity/main/errors/query costs and PBPS-SPHMC actual-input composition remain OPEN.','No uniform-parameter AE event or arbitrary sample-correlated random initialization inferred.','Actual page/interactive branch visual acceptance, full Exposition Seal, main merge/live and postmerge purification remain open.'],reused_unchanged_audit=dict(ci_contract_regressions=pin('runs/20261007-companion-priority/pbps-actual-physical-time-cover79/integration79/ci-contract-regressions/receipt.json'),reason='No gate/schema/tool implementation changed since those 63 tests; actual source-bound checks run afresh.'),Goal_complete=False)
p=r/'integration.notes.json';assert not p.exists();p.write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Recorded exact local aggregate/reader acceptance; visual/main/PURIFIED/live remain pending.')
