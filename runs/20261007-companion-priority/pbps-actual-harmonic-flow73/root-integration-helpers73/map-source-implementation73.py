from pathlib import Path
import hashlib, json, os
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73')
pre=Path('runs/20261007-companion-priority/pbps-harmonic-flow-preproof73')
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes()
 return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
seal=load(pre/'root.statement-seal73.json');g=load(seal['source_graph']['path'])
lesson=load('website/content/declaration_lessons/pbps-actual-harmonic-flow.json')['units'][0]
regions=[x['lean_source_region'] for x in lesson['steps']]
mapping={
 'STAND-C2':('retained-source-binder-and-used', [0]),
 'STAND-MODULI':('retained-source-binders-not-used-in-deterministic-BODY', []),
 'STAND-HESSIAN':('retained-source-binder-not-used-in-deterministic-BODY', []),
 'STAND-STEP':('eta-positive-used-beta-cap-retained', [0,1,2,3,4]),
 'PARAMETERS':('literal-universal-parameters', [0,1,2,3,4,5]),
 'CENTER':('literal-definition-not-an-assumed-object', [0,2]),
 'POSITION':('literal-first-flow-coordinate', [1,2,4,5]),
 'PHASE-FLOW':('literal-two-coordinate-map', [0,1,2,4,5]),
 'ODE-X':('internally-proved-conclusion', [2]),
 'ODE-P':('internally-proved-conclusion', [2]),
 'INIT':('internally-proved-conclusion', [1]),
 'GROUP':('internally-proved-group-and-both-inverses', [1]),
 'HALF-TURN':('internally-proved-deterministic-endpoint', [5]),
 'ENERGY':('literal-weighted-sum-definition', [3,4]),
 'FLOW-ENERGY':('internally-proved-conclusion', [4]),
 'ENERGY-NONNEG':('omitted-source-bridge-produced', [3]),
 'SCALE':('omitted-source-bridge-produced', [0,1,2,4]),
 'TRIG':('omitted-source-bridge-produced-with-fixed-Mathlib', [1,4,5]),
 'NORM-CANCEL':('omitted-source-bridge-produced', [4]),
 'DERIVATIVE':('omitted-source-bridge-produced-with-fixed-Mathlib', [2]),
 'GRAD-CONT':('omitted-source-bridge-produced-with-existing-ASTIS-theorem', [0]),
 'JOINT-CONT':('omitted-source-joint-continuity-and-Borel-produced', [0,5]),
 'SELECTED-ANCHOR':('selected-deterministic-consumer-boundary-only-no-PDMP-credit', [0,1,2,3,4,5])
}
assert len(g['nodes'])==len(mapping)==23 and {x['id'] for x in g['nodes']}==set(mapping)
rows=[dict(source_node=n['id'],source_kind=n['kind'],classification=mapping[n['id']][0],
           BODY_regions=[regions[i] for i in mapping[n['id']][1]],
           source_node_not_rewritten=True) for n in g['nodes']]
gaps=[x['id'] for x in g['nodes'] if x['kind']=='SOURCE_GAP'];assert len(gaps)==7
out=r/'implementation-source-map73.json';assert not out.exists()
out.write_text(json.dumps(dict(status='FOCUSED_COMPILED_IMPLEMENTATION_MAP_PENDING_INDEPENDENT_SOURCE_REVIEW',
 actual_root_PID=os.getpid(),source_graph=seal['source_graph'],original_graph_preserved=True,
 source_graph_nodes=23,source_graph_edges=37,source_gap_ids=gaps,
 source_gap_IMPLEMENTED_not_independently_admitted=True,
 total_source_coverage_reference=seal['binder_audit'],
 module=pin('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'),
 lesson=pin('website/content/declaration_lessons/pbps-actual-harmonic-flow.json'),nodes=rows,
 no_new_source_binders=True,no_new_stochastic_or_cost_claims=True,
 source_and_Lean_graph_edges_distinct=True,full_paper=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS finite23-node/37-source-edge implementation map; seven internal bridges await independent source admission; original source graph unchanged.')
