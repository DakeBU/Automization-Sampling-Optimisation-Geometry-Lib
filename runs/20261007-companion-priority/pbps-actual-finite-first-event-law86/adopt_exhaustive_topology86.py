from pathlib import Path
import json,hashlib
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):p=Path(p);return dict(path=p.as_posix(),RAW_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n')
def check(p,h,groups):
 assert pin(p)['RAW_sha256']==h,p
 m=load(p)
 for group in groups:
  for x in m[group]:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'],x['path']
 return m
a=r/'topology-repair-review86';b=r/'independent-source86/fifth-edge-review86'
check(a/'closed-RAW-manifest86.json','a2b020ffb69c5368f4409d47cbdffcca51d6b76f747115fb70e896345122a806',['frozen_current_inputs','owned_artifacts','excluded_private_artifacts'])
check(b/'fifth-edge-review86.native-RAW-manifest.json','b6ddf38e496c28c706c0a7489f79187e959ddb5308e038fd9afd18b678076ebd',['inputs','outputs'])
x=load(a/'decision86.json');y=load(b/'fifth-edge-review86.decision.json')
assert pin(a/'decision86.json')['RAW_sha256']=='ef07c53cf2c614a3a5610137953d8a91da98acbb99fa418e8f36886cb364635a'
assert x['status']=='CONDITIONAL_ACCEPT_ORIGINAL_ADDITIONS_PENDING_EXACT_FIFTH_EDGE_REVIEW'
assert len(x['required_repairs'])==1
assert y['verdict']=='ACCEPTED_EXACT_FIFTH_EDGE' and y['independent_from_proposal_creator']
assert y['proposal_sha256']==x['required_repairs'][0]['proposal']['raw_sha256']
base=load(r/'independent-source86/source-proof-graph86.exhaustive-successor.json');new=load(a/'source-proof-graph86.single-edge-proposed-successor.json');proposal=load(a/'minimal-strict-overlay86.json')
assert new['edges']==base['edges']+[proposal['operations'][0]['value']]
for k in ['nodes','junctions','route_boundary','exhaustive_scope','source_inventory']:assert new[k]==base[k],k
assert len(new['nodes'])==38 and len(new['edges'])==76
assert sum(bool(e['dependency_edge']) for e in new['edges'])==73
report=r/'root.exhaustive-topology86.adoption.json';assert not report.exists()
record=dict(status='COMPOSED_DISTINCT_EXACT_SOURCE_TOPOLOGY_REVIEWS_ACCEPTED',initial_additions_review=pin(a/'decision86.json'),initial_closed_manifest=pin(a/'closed-RAW-manifest86.json'),strict_single_edge=pin(a/'minimal-strict-overlay86.json'),distinct_single_edge_review=pin(b/'fifth-edge-review86.decision.json'),single_edge_closed_manifest=pin(b/'fifth-edge-review86.native-RAW-manifest.json'),effective_graph=pin(a/'source-proof-graph86.single-edge-proposed-successor.json'),effective_inventory=pin(r/'independent-source86/source-inventory86.exhaustive-successor.json'),counts=dict(inventory=47,nodes=38,relations=76,dependency_edges=73,excluded_associations=3,independent_source_anchors=72,leaf_atoms=65,equation_row_anchors=7),original_Statement_Seal_unchanged=True,Lean_source_statement_proof_lesson_unchanged=True,global_source_conclusions_remain_OPEN=True,source_graph_is_not_Lean_dependency_graph=True,final_source_semantic_review='pending',VERIFIED=False,Goal_complete=False)
save(report,record)
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-first-event-law.json');c=load(cp)
(r/'cell.before-exhaustive-topology86.exactraw.snapshot.json').write_bytes(cp.read_bytes())
c['source_proof_coverage'].update(source_graph=record['effective_graph']['path'],source_inventory=record['effective_inventory']['path'],coverage_report=report.as_posix(),reviewed_adapter_overlay=report.as_posix(),coverage_status='Distinct source-only reviews of initial7items/1node/4edges and strict fifth-edge accepted; exhaustive47inventory/38nodes/76relations=73dependencies+3excluded associations, all72independent anchors(65leafatoms+7equation rows). All frozen originals preserved, no Statement Seal/proposition/Lean/lesson change. Complete source-local semantic review still pending; global conclusions OPEN.')
save(cp,c);print('Accepted composed distinct source topology repairs; final source fidelity still pending')
