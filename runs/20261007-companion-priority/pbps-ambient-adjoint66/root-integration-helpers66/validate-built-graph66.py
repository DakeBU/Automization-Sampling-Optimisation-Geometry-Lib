from pathlib import Path
import hashlib,json,sys
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66/integration66');build=json.loads((r/'website-ci-build/receipt.json').read_bytes());assert build['exit_code']==0 and build['terminal_closed']
sys.path.insert(0,str(Path('website/scripts').resolve()));import underlying_lean_graph as ulg,publication_reader
site=Path('_site');gpath=site/'data/underlying-lean-graph.json';g=json.loads(gpath.read_bytes());decl='AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition'
assert any(n.get('id')=='decl:'+decl for n in g['nodes'])
assert g['publication_inputs_sha256']==publication_reader.graph_input_digest()
ulg.validate(site,g)
x=dict(status='CURRENT_BUILT_OFFICIAL_GRAPH_VALIDATION_PASS',actual_graph_generator='website/scripts/build_site.py invokes current underlying_lean_graph.enrich_site; actual successful build receipt retained',actual_validation='underlying_lean_graph.validate on the newly emitted current graph plus exact publication input digest',negative_prebuild_receipt=(r/'official-graph-ci-output/receipt.json').as_posix(),current_declaration='decl:'+decl,graph_RAW_sha256=hashlib.sha256(gpath.read_bytes()).hexdigest(),publication_inputs_sha256=g['publication_inputs_sha256'],no_second_graph_regeneration=True,formal_semantics_unchanged=True)
p=r/'official-built-graph66.validation.json';assert not p.exists();p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS current official graph validation: newly built inventory contains exact SCI66 declaration; full official validator and publication digest accepted. Old negative retained.')
