from pathlib import Path
import datetime,hashlib,json,sys,re
r=Path(__file__).parent;out=r/'integration88';load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
labels=['canonical','integration-pythoncompile','integration-contributor','integration-publication','integration-semantic','integration-frontier','integration-site-regressions','publication-main','site-build','underlying-graph','graph','site-check','integration-windows-whitespace-check']
checks=[]
for label in labels:
 p=r/'checks88'/label/'receipt.json';a=load(p);assert a['terminal_closed'] and a['exit_code']==0,label
 checks.append(dict(label=label,receipt=pin(p),stdout=pin(p.parent/'stdout.log'),stderr=pin(p.parent/'stderr.log')))
assert load(r/'checks88/graph/receipt.json')['argv'][-1]=='ASTIS-SW-PBPS-actual-conditional-next-wait-survival'
sys.path.insert(0,str(Path.cwd()/'tools'));sys.path.insert(0,str(Path.cwd()/'website/scripts'))
import astis_site,astis_advance as advance,publication_reader,underlying_lean_graph
gate=load('.astis/site-lean-gate.json');assert gate['passed'] and gate['source_digest']==astis_site.source_digest()
graph=load('_site/data/underlying-lean-graph.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
underlying_lean_graph.validate(Path('_site'),graph)
claim=load(r/'claim.json');assert advance.current_advances()[claim['advance_id']]['state']=='VERIFIED'
source=load(r/'independent-source88/source-review88.decision.native.json')
for name,key in [(claim['proposed_files'][0],'lean_module_raw_sha256'),('website/content/declaration_lessons/pbps-actual-conditional-next-wait-survival.json','lesson_raw_sha256'),('website/content/publications/pbps-actual-conditional-next-wait-survival.json','publication_raw_sha256')]:assert pin(name)['RAW_sha256']==source[key],name
view=load(out/'static-svg/viewed-or-reused.json')
assert view['viewed_by_root'] and pin(view['input'])['RAW_sha256']==view['input_RAW_sha256'] and pin(view['output'])['RAW_sha256']==view['output_RAW_sha256']
assert Path('docs/module-graph.svg').read_bytes()==Path('docs/assets/astis_lean_arsenal_module_graph.svg').read_bytes()

assert any(n.get('id')=='decl:'+claim['target_declarations'][0] for n in graph['nodes'])
lanes=[s['advance_id'] for s in advance.current_advances().values() if s['state']=='STABILIZING']
assert lanes==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
saved=load(r.parent/'pbps-conditional-next-wait-preread88/pre-fetch88.workspace-RAW.json')['tracked_modified'];assert len(saved)==21
for p,h in saved.items():assert pin(p)['RAW_sha256']==h,p
builds=re.findall(r'Build completed successfully \((\d+) jobs\)',(r/'checks88/canonical/stdout.log').read_text(encoding='utf8'))
assert len(builds)>=2
note=dict(status='LOCAL_SHARED_AGGREGATE_AND_GENERATED_READER_GATES_PASS_VISUAL_PENDING',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),science_commit='456e13f9561abcf01a285133e91b3951bf2ed892',independent_verifier='/root/exact_verify77',verification=pin(r/'exact-commit-verification88/verified.json'),root_jobs=int(builds[-2]),test_jobs=int(builds[-1]),registry_count=537,checks=checks,lean_source_digest=gate['source_digest'],publication_inputs_sha256=graph['publication_inputs_sha256'],current_graph=pin('_site/data/underlying-lean-graph.json'),graph_delta='One actual deterministic-depth history-dependent next-wait survival theorem. Exact kernel audit certifies actual87 history/tail law, actual75 integrated hazard and actual77 iid product as immediate public ASTIS parents; private/generated closure is certified separately. Generated graph reference signals are not elaborated kernel edges. No conceptual mirror added.',kernel_dependency_certificate=pin(r/'independent-math88/kernel-dependency-summary88.json'),actual_visual_inspection=dict(static_view_evidence=pin(out/'static-svg/viewed-or-reused.json'),static_svg_scope='Shared leaf module overview explicitly excludes paper consumer branches.',browser_page_and_interactive_branch='PENDING: existing bound browser has no inspectable tab; discovery only exposes mcpapps, no alternate backend substitution attempted.',full_Exposition_Seal=False),sole_stabilization_owner='companion_root_20261005',sole_stabilization_lane=lanes[0],state_distinctions=dict(proved_locally=True,independently_verified=True,local_aggregate_and_generated_site_gates=True,stabilized=False,merged=False,purified=False,live_verified=False,main_theorem_complete=False),remaining=[claim['truth_boundary'],'Actual page/fine branch visual acceptance, full Exposition Seal, main merge/live and postmerge purification remain OPEN.'],offline_reader=pin(out/'offline-reader.json'),preserved_collaborator_modified_files=21,windows_whitespace=dict(accepted_check=pin(r/'checks88/integration-windows-whitespace-check/receipt.json'),diagnosis='Existing Windows CRLF evidence and shared files retained; only the coordinator-owned new ledger tail normalized. Plain git diff --check is captured after integration commit.'),remote_CI='Independent remote results; no remote Lean PASS claimed.',Goal_complete=False)
p=r/'integration.notes.json';assert not p.exists();p.write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Recorded local aggregate/reader checks only; visual/main/PURIFIED/fullpaper/Goal remain open.')
