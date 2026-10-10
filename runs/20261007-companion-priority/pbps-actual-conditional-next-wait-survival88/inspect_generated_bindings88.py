from pathlib import Path
import hashlib,json
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
module=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitSurvival.lean')
download=Path('_site/downloads/lean')/module
assert module.read_bytes()==download.read_bytes()
assert sha(module.read_bytes())=='2f509ce49343d349f7a9fb21d2f7b1697c1a6de942353f6cd8ff16d522911569'
graph=load('_site/data/underlying-lean-graph.json');decl=load(r/'claim.json')['target_declarations'][0]
nodes=[x for x in graph['nodes'] if x['id']=='decl:'+decl];assert len(nodes)==1
refs=[x['value'] for x in nodes[0]['details'] if x['label']=='References (name scan; incomplete)'];assert len(refs)==1
parents=load(r/'claim.json')['dag_inputs'];assert all(x in refs[0] for x in parents)
kernel=load(r/'independent-math88/kernel-dependency-summary88.json')
out=r/'integration88/generated-bindings.json';assert not out.exists()
out.write_text(json.dumps(dict(status='PASS_GENERATED_DATA_ONLY',Lean_download=download.as_posix(),Lean_download_RAW_sha256=sha(download.read_bytes()),node=nodes[0],expected_public_ASTIS_parents=parents,kernel_certificate=(r/'independent-math88/kernel-dependency-summary88.json').as_posix(),graph_contract='Generated references are explicitly incomplete name scans; exact elaborated dependencies are only claimed by the independent kernel certificate.',visual_branch_inspected=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Exact Lean download and bounded graph data match verified88; no browser/fine-graph visual credit.')
