from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');pre=r.parent/'pbps-clock-preproof75'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
gp=pre/'independent-source-baseline75/source-proof-graph75.json';g=load(gp)
lesson=load('website/content/declaration_lessons/pbps-actual-hazard-clock.json')['units'][0];regions=[x['lean_source_region'] for x in lesson['steps']];assert len(regions)==9
mapping={
 'N01':('original-six-callers-retained;ordinary-finite-Hilbert-Borel-types',list(range(9))),
 'N02':('literal-center-and-residual-inside-rate',[0,1]),
 'N03':('actual73-producer-used-internally',[0,1]),
 'N04':('actual74-continuous-nonnegative-rate-used-internally',[0,1]),
 'N05':('no-refresh-source-context;no-new-bounce-or-continuity-claim',[]),
 'N06':('literal-weighted-sum-energy-used-in-C',[0]),
 'N07':('actual73-H-conservation-used-on-each-deterministic-orbit',[0]),
 'N08':('actual74-exact-same-energy-layer-C-used-at-Phi',[0]),
 'N09':('joint-actual-orbit-integrand-continuity',[1]),
 'N10':('finite-interval-integrability-and-joint-primitive-continuity-Borel',[1]),
 'N11':('zero-nonnegative-monotone-on-NNReal',[2]),
 'N12':('literal-hittingAfter-with-empty-set-infinity',[3]),
 'N13':('continuous-closed-sublevel-and-attained-infimum',[3]),
 'N14':('finite-threshold-value-via-IVT;infinity-positive-zero-threshold-branches',[3,4]),
 'N15':('finite-time-first-crossing-equivalence',[3]),
 'N16':('joint-clock-Borel-from-finite-and-top-sublevels',[5]),
 'N17':('substitute-actual-orbit-in-actual-energy-layer-cap',[0]),
 'N18':('integrate-the-derived-nonnegative-C-bound',[2]),
 'N19':('extended-waiting-lower-bound-and-zero-C-infinity',[8]),
 'N20':('fixed-unit-rate-expMeasure-input;probability-proved-not-supplied',[6]),
 'N21':('direct-all-real-survival-preimage-and-nonnegative-endpoint-CDF;standalone-support-or-zero-atom-lemmas-not-claimed',[6,7]),
 'N22':('literal-measurable-pushforward-waiting-law',[6]),
 'N23':('exact-strict-survival-including-infinite-waiting',[7]),
 'N24':('general-zero-C-positive-e-and-e-zero-branches;rank0-H0-specializations-valid-without-extra-public-claims',[4,8]),
 'N25':('open-recursive-actual-state-consumer-not-produced-here',[]),
 'N26':('open-full-recursive-PDMP-path-and-initial-draws',[]),
 'N27':('open-pathwise-energy-conservation-across-bounces',[]),
 'N28':('open-iid-support-moments-SLLN-nonaccumulation',[]),
 'N29':('open-global-path-Markov-memorylessness',[]),
 'N30':('excluded-invariance-terminal-kernel-main-cost-and-Davis-context',[]),
 'N31':('actual74-canonical-internal-gradient-Lipschitz-producer-transitively-reused',[0,1]),
 'N32':('initial-Gaussian-draws-context-only-not-ongoing-refresh',[])
}
assert len(g['nodes'])==len(mapping)==32 and {n['id'] for n in g['nodes']}==set(mapping)
rows=[dict(source_node=n['id'],source_kind=n['kind'],meaning=n['meaning'],classification=mapping[n['id']][0],BODY_regions=[regions[i] for i in mapping[n['id']][1]],source_node_not_rewritten=True) for n in g['nodes']]
gaps=[n['id'] for n in g['nodes'] if n['kind']=='ASTIS_INTERNAL_BRIDGE'];assert len(gaps)==13
p=r/'implementation-source-map75.json';assert not p.exists()
p.write_text(json.dumps(dict(status='FOCUSED_COMPILED_IMPLEMENTATION_MAP_PENDING_INDEPENDENT_SOURCE_REVIEW',actual_root_PID=os.getpid(),source_graph=pin(gp),original_graph_preserved=True,source_graph_nodes=32,source_graph_edges=len(g['edges']),source_gap_ids=gaps,internal_bridges_have_BODY_mapping_not_yet_independently_admitted=True,route_qualification='N21 uses exact all-real survival-preimage plus the nonnegative-endpoint CDF directly. No standalone support or zero-atom result is claimed. N24 is supplied by general zero-C/e-zero branches, without publishing separate rank0/H0 theorems.',total_source_coverage_reference=pin(pre/'independent-header-source75/header-source-coverage75.json'),module=pin('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean'),lesson=pin('website/content/declaration_lessons/pbps-actual-hazard-clock.json'),nodes=rows,no_new_source_binders=True,no_recursive_path_or_cost_claims=True,source_and_Lean_graph_edges_distinct=True,full_paper=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS75 finite32-node source map;13one-clock bridge mappings await independent admission; recursive/global path and all main costs remain open.')
