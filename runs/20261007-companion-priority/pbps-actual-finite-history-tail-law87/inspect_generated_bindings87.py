from pathlib import Path
import hashlib,json
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
module=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean')
download=Path('_site/downloads/lean')/module
assert module.read_bytes()==download.read_bytes()
assert sha(module.read_bytes())=='01fcff944f1dbd42be2af30063b9baf4e191e2cde959e008724387cadb4fc899'
graph=load('_site/data/underlying-lean-graph.json');decl=load(r/'claim.json')['target_declarations'][0]
nodes=[x for x in graph['nodes'] if x['id']=='decl:'+decl];assert len(nodes)==1
refs=[x['value'] for x in nodes[0]['details'] if x['label']=='References (name scan; incomplete)'];assert len(refs)==1
parents=load(r/'claim.json')['dag_inputs'];assert all(x in refs[0] for x in parents)
kernel=load(r/'independent-math87/kernel-dependency-summary87.json')
out=r/'integration87/generated-bindings.json';assert not out.exists()
out.write_text(json.dumps(dict(status='PASS_GENERATED_DATA_ONLY',Lean_download=download.as_posix(),Lean_download_RAW_sha256=sha(download.read_bytes()),node=nodes[0],expected_public_ASTIS_parents=parents,kernel_certificate=(r/'independent-math87/kernel-dependency-summary87.json').as_posix(),graph_contract='Generated references are explicitly incomplete name scans; exact elaborated dependencies are only claimed by the independent kernel certificate.',visual_branch_inspected=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Exact Lean download and bounded graph data match verified87; no browser/fine-graph visual credit.')
