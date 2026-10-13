from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-bounce-rate74');pre=r.parent/'pbps-bounce-rate-preproof74'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
gp=pre/'independent-header-source74/source-proof-graph74.json';g=load(gp);lesson=load('website/content/declaration_lessons/pbps-actual-bounce-rate.json')['units'][0];regions=[x['lean_source_region'] for x in lesson['steps']];assert len(regions)==7
mapping={
'N01':('literal-universal-parameters',list(range(7))),
'N02':('retained-C2-source-binder-used-in-gradient-producer',[0]),
'N03':('Hessian-binder-used-internal-Lipschitz;positive-alpha-and-order-retained-unused',[0]),
'N04':('eta-positive-used;beta-step-cap-retained-unused',[4,5]),
'N05':('internal-gradient-continuity-from-canonical-Lipschitz-producer',[0]),
'N06':('actual-residual-literal',[1,2,3,6]),
'N07':('actual-center-literal',[3,4,5,6]),
'N08':('exact-zero-safe-reflection-literal',[1,2]),
'N09':('total-zero-reflection-proved',[1,3]),
'N10':('reused-Mathlib-reflection;compiled-involution-norm-pairing;no-extra-tangential-claim',[1]),
'N11':('actual-total-reflection-expression-Borel-under-residual-substitution;no-joint-continuity-claim',[2]),
'N12':('actual-S-substitution',[2,3]),
'N13':('actual-position-involution-and-momentum-norm',[3]),
'N14':('actual-rate-literal',[2,3]),
'N15':('actual-rate-nonnegative-and-zero-residual-case',[3]),
'N16':('actual-rate-joint-continuity-and-Borel',[2]),
'N17':('actual-S-joint-Borel',[2]),
'N18':('exact-weightedSUM-H-literal',[3,4,5]),
'N19':('actual-bounce-preserves-same-H',[3]),
'N20':('nonnegative-H-and-two-energy-radii',[4,5]),
'N21':('canonical-QuadraticRegularization-r0-producer-used-internally',[0]),
'N22':('triangle-and-internal-Lipschitz-residual-bound',[6]),
'N23':('Cauchy-Schwarz-and-positive-part-bound',[6]),
'N24':('exact-pointwise-same-energy-layer-Lambda',[6]),
'N25':('existing73-sibling-source-ingredient;NOT-a-formal74-parent;no-new-credit',[]),
'N26':('open-actual-path-consumer;not-proved-by-pointwise-layer-estimate',[]),
'N27':('open-integrated-hazard-clocks-nonexplosion-Markov-consumer',[]),
'N28':('open-terminal-kernel-and-operator-consumer',[])}
assert len(g['nodes'])==len(mapping)==28 and {n['node_id'] for n in g['nodes']}==set(mapping)
rows=[dict(source_node=n['node_id'],source_kind=n['kind'],meaning=n['meaning'],classification=mapping[n['node_id']][0],BODY_regions=[regions[i] for i in mapping[n['node_id']][1]],source_node_not_rewritten=True) for n in g['nodes']]
gaps=[n['node_id'] for n in g['nodes'] if n['kind'] in ['INTERNAL_OBLIGATION','OPTIONAL_INTERNAL_OBLIGATION']];assert len(gaps)==13
p=r/'implementation-source-map74.json';assert not p.exists();p.write_text(json.dumps(dict(status='FOCUSED_COMPILED_IMPLEMENTATION_MAP_PENDING_INDEPENDENT_SOURCE_REVIEW',actual_root_PID=os.getpid(),source_graph=pin(gp),original_graph_preserved=True,source_graph_nodes=28,source_graph_edges=len(g['edges']),source_gap_ids=gaps,source_gap_IMPLEMENTED_not_independently_admitted=True,total_source_coverage_reference=pin(pre/'independent-header-source74/header74.coverage-projection.json'),module=pin('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean'),lesson=pin('website/content/declaration_lessons/pbps-actual-bounce-rate.json'),nodes=rows,no_new_source_binders=True,no_new_stochastic_or_cost_claims=True,source_and_Lean_graph_edges_distinct=True,full_paper=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('PASS74 finite28-node source map;13internal bridges await independent admission;73sibling/path/clocks/terminal kernel not newly certified.')
