"""Record bounded integration evidence without granting visual or paper completion."""
from pathlib import Path
import hashlib,json,sys,datetime,subprocess
R=Path.cwd();r=Path(__file__).parent;out=r/'integration93'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
labels=['integration-tests-final','integration-astis','integration-canonical-after-main','integration-publication-after-main','integration-publication-main-after-main','integration-contributor-after-main','integration-semantic','integration-frontier','integration-python-compile','integration-site-build-current-gate','integration-site-check-current-gate','integration-graph-current-gate','integration-underlying-graph-current-gate','integration-site-regressions','contributor-regressions','integration-diff-check','integration-harness-utf8']
checks=[]
for label in labels:
    p=r/'checks93'/label/'receipt.json';a=load(p);assert a['terminal_closed'] and a['exit_code']==0,label
    checks.append(dict(label=label,receipt=pin(p),stdout=pin(p.parent/'stdout.log'),stderr=pin(p.parent/'stderr.log')))
sys.path[:0]=[str(R/'tools'),str(R/'website/scripts')]
import astis_site,astis_advance,publication_reader,underlying_lean_graph
gate=load('.astis/site-lean-gate.json');assert gate['passed'] and gate['source_digest']==astis_site.source_digest()
assert gate['commit']==subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
graph=load('_site/data/underlying-lean-graph.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
underlying_lean_graph.validate(Path('_site'),graph)
site=load('_site/data/site-data.json');assert site['gate']['passed'] and site['gate']['source_digest']==gate['source_digest']
claim=load(r/'claim.json');assert astis_advance.current_advances()[claim['advance_id']]['state']=='VERIFIED'
assert pin(claim['proposed_files'][0])['raw_sha256']=='5467078f497e0d40e1916550b2e5e9a5be992a69b20fc143bda06dd988d86d9d'
manifest=load(r/'exact-commit-verification93/closed-RAW-manifest93.json')
for d in manifest['checked_science_inputs']:
    if d['path'].startswith(('website/content/declaration_lessons/','website/content/publications/','research-wiki/semantic-roundtrip/')):
        assert pin(d['path'])['raw_sha256']==d['raw_sha256'],d['path']
for d in manifest['preserved_collaborator_inputs']:assert pin(d['path'])['raw_sha256']==d['raw_sha256'],d['path']
lanes=[v['advance_id'] for v in astis_advance.current_advances().values() if v['state']=='STABILIZING'];assert lanes==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
view=load(out/'static-svg/viewed.json');assert view['viewed_by_root'] and pin(view['input'])['raw_sha256']==view['input_RAW_sha256'] and pin(view['output'])['raw_sha256']==view['output_RAW_sha256']
assert Path('docs/module-graph.svg').read_bytes()==Path('docs/assets/astis_lean_arsenal_module_graph.svg').read_bytes()
reader=load(out/'offline-reader.json');assert reader['exact_step_Lean_regions']==9
note=dict(status='LOCAL_AGGREGATE_AND_GENERATED_READER_PASS_VISUAL_PENDING',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),science_commit=load(out/'integration-scope.json')['science_commit'],integration_base_commit=load(out/'main-sync.json')['merge_commit'],registry_count=542,verification=pin(r/'exact-commit-verification93/verified.json'),checks=checks,source_digest=gate['source_digest'],publication_inputs_sha256=graph['publication_inputs_sha256'],offline_reader=pin(out/'offline-reader.json'),browser_recheck=pin(out/'browser-recheck.json'),line_ending_repair=pin(out/'line-ending-repair/receipt.json'),static_svg=pin(out/'static-svg/viewed.json'),graph_delta='One finite-count complete-history and coordinate-product path integration node. Nine direct actual ASTIS dependencies independently reviewed. Density is the ordered prefix product times terminal survival. Formal structure remains distinct from scanned and curated overlays. No new conceptual mirror.',independent_dependency_certificate=pin(r/'exact-commit-verification93/verified.json'),preserved_collaborator_modified_files=21,sole_lane=lanes[0],state_distinctions=dict(proved_locally=True,independently_verified=True,local_aggregate_and_generated_site_gates=True,stabilized=False,merged=False,purified=False,live_verified=False,full_Exposition_Seal=False,main_theorem_complete=False),remaining=[claim['truth_boundary'],'Actual page/fine branch visual acceptance and main merge/postmerge purification remain open.'],Goal_complete=False)
assert not (r/'integration.notes.json').exists()
(r/'integration.notes.json').write_text(json.dumps(note,indent=2)+'\n',encoding='utf8',newline='\n')
print('Recorded integration gates; visual/main/PURIFIED/wholepaper acceptance remains open.')
