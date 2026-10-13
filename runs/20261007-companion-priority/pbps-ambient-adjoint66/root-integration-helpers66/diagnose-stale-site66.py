from pathlib import Path
import json,hashlib
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66/integration66');p=Path('_site/data/site-data.json');b=p.read_bytes();decl='AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition'
assert decl.encode() not in b
source=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean');assert b'theorem actual_ambient_adjoint_centered_decomposition' in source.read_bytes()
q=json.loads((r/'official-graph-ci-output/receipt.json').read_bytes());assert q['exit_code']==1 and q['terminal_closed']
x=dict(status='GRAPH_GATE_PREBUILD_INVENTORY_MISMATCH',negative_receipt=(r/'official-graph-ci-output/receipt.json').as_posix(),stale_site_inventory=dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),current_declaration_present=False),canonical_production_decl_present=True,Lean_and_independent_review_unchanged=True,diagnosis='Standalone graph enrichment reads _site/data/site-data.json. The previous release inventory omits SCI66; this command was run before rebuilding site data.',repair='Run actual build_site.py to refresh source-derived inventory, then rerun the standalone graph gate against the new inventory. No canonical graph/Lean/source contract patch.',unchanged_retry_retired=True)
out=r/'graph-prebuild-order-diagnosis66.json';assert not out.exists();out.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS typed graph prebuild-order diagnosis: exact stale emitted inventory; no Lean/source defect or code patch.')
