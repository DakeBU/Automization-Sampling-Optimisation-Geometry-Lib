from pathlib import Path
import hashlib,json,sys,datetime
R=Path.cwd();r=Path(__file__).parent;out=r/'integration91'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
labels=['integration-tests','integration-astis','integration-publication','integration-publication-main','integration-contributor','integration-semantic','integration-frontier','integration-python-compile','integration-site-build-final','integration-site-check-after-graph','integration-graph-after-overlay','integration-underlying-graph','site-regressions','contributor-regressions','integration-windows-whitespace']
checks=[]
for label in labels:
 p=r/'checks91'/label/'receipt.json';a=load(p);assert a['terminal_closed'] and a['exit_code']==0,label
 checks.append(dict(label=label,receipt=pin(p),stdout=pin(p.parent/'stdout.log'),stderr=pin(p.parent/'stderr.log')))
sys.path.insert(0,str(R/'tools'));sys.path.insert(0,str(R/'website/scripts'))
import astis_site,astis_advance,publication_reader,underlying_lean_graph
gate=load('.astis/site-lean-gate.json');assert gate['passed'] and gate['source_digest']==astis_site.source_digest()
graph=load('_site/data/underlying-lean-graph.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
underlying_lean_graph.validate(Path('_site'),graph)
site=load('_site/data/site-data.json');assert site['gate']['passed'] and site['gate']['source_digest']==gate['source_digest']
claim=load(r/'claim.json');assert astis_advance.current_advances()[claim['advance_id']]['state']=='VERIFIED'
math=load(r/'independent-math91/decision91.native.json')
assert pin(claim['proposed_files'][0])['raw_sha256']==math['production']['raw_sha256']
manifest=load(r/'exact-commit-verification91/closed-RAW-manifest91.json')
for d in manifest['checked_science_inputs']:
 if d['path'].startswith(('website/content/declaration_lessons/','website/content/publications/','research-wiki/semantic-roundtrip/')):
  assert pin(d['path'])['raw_sha256']==d['raw_sha256'],d['path']
for d in manifest['preserved_collaborator_inputs']:assert pin(d['path'])['raw_sha256']==d['raw_sha256'],d['path']
lanes=[v['advance_id'] for v in astis_advance.current_advances().values() if v['state']=='STABILIZING'];assert lanes==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
view=load(out/'static-svg/viewed.json');assert view['viewed_by_root'] and pin(view['input'])['raw_sha256']==view['input_RAW_sha256'] and pin(view['output'])['raw_sha256']==view['output_RAW_sha256']
assert Path('docs/module-graph.svg').read_bytes()==Path('docs/assets/astis_lean_arsenal_module_graph.svg').read_bytes()
reader=load(out/'offline-reader.json');assert reader['exact_step_Lean_regions']==7
note=dict(status='LOCAL_AGGREGATE_AND_GENERATED_READER_PASS_VISUAL_PENDING',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),science_commit=load(out/'integration-scope.json')['science_commit'],registry_count=540,verification=pin(r/'exact-commit-verification91/verified.json'),checks=checks,source_digest=gate['source_digest'],publication_inputs_sha256=graph['publication_inputs_sha256'],offline_reader=pin(out/'offline-reader.json'),static_svg=pin(out/'static-svg/viewed.json'),graph_delta='One actual strict next absolute-event-time law. Three direct public kernel parents: complete-history extension90, conditional density89, canonical exponential-product probability. Fiberwise translation and Tonelli; no separately proved general shear. Reference scans remain distinct from elaborated kernel dependencies.',independent_dependency_certificate=pin(r/'independent-math91/decision91.native.json'),preserved_collaborator_modified_files=21,sole_lane=lanes[0],state_distinctions=dict(proved_locally=True,independently_verified=True,local_aggregate_and_generated_site_gates=True,stabilized=False,merged=False,purified=False,live_verified=False,full_Exposition_Seal=False,main_theorem_complete=False),remaining=[claim['truth_boundary'],'Actual page/fine branch visual acceptance and main merge/postmerge purification remain open.'],Goal_complete=False)
assert not (r/'integration.notes.json').exists()
(r/'integration.notes.json').write_text(json.dumps(note,indent=2)+'\n',encoding='utf8',newline='\n')
print('Recorded integration checks; no visual/main/PURIFIED/wholepaper credit.')
