"""Independent source-only review closure; never writes canonical state."""
from pathlib import Path
import hashlib
import json
import subprocess
from datetime import datetime, timezone

R = Path('E:/Samplinglib')
D = R / 'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89/header-math89'
A = D.parent / 'independent-source-first89'
UTC = datetime.now(timezone.utc).isoformat()
HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip()
assert HEAD == '7c108c3181cee58bb9305445f903c5f71efda9c5', HEAD

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': p.as_posix(), 'raw_sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def read(p):
    return json.loads(Path(p).read_text(encoding='utf8'))

def out(name, value):
    p = D / name
    assert not p.exists(), p
    with p.open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return pin(p)

manifest_path = A / 'closed-raw-manifest.source-first89.native.json'
m = read(manifest_path)
assert pin(manifest_path)['raw_sha256'] == 'e77601f0a12d56aa95a7f891c72fe18fa60d4f014d786a1b561d3424e585ca22'
hash_checked = []
for kind in ('inputs', 'outputs'):
    for item in m[kind]:
        actual = pin(item['path'])
        assert actual['raw_sha256'] == item['raw_sha256'] and actual['bytes'] == item['bytes'], item
        hash_checked.append({**actual, 'author_manifest_role': kind,
            'semantic_read_in_current89_stage': Path(item['path']).name in (
                'primary-pbps.exactraw.snapshot.html', 'source-proof-graph86.single-edge-proposed-successor.json',
                'source-inventory86.exhaustive-successor.json', 'chronology.source-first89.native.jsonl',
                'source-coverage89.native.json', 'source-first89.native.json', 'source-proof-graph89.native.json',
                'terminal-completion.source-first89.native.json', 'unchanged-global-source-evidence89.native.json')})
primary_path = Path(m['inputs'][0]['path'])
primary = primary_path.read_bytes()
spans = []
for s in m['primary_spans']:
    b = primary[s['byte_start_zero_based']:s['byte_end_exclusive']]
    assert hashlib.sha256(b).hexdigest() == s['raw_span_sha256']
    spans.append({**s, 'independent_direct_read_tool_chunk': '5e1ae3', 'hash_verified': True})
g = read(A / 'source-proof-graph89.native.json')
c = read(A / 'source-coverage89.native.json')
f = read(A / 'source-first89.native.json')
gg_path = Path(g['global_evidence']['graph']['path'])
gi_path = Path(g['global_evidence']['inventory']['path'])
gg, gi = read(gg_path), read(gi_path)
assert len(g['nodes']) == 8 and len(g['edges']) == 11 and len(g['AND_junctions']) == 4
assert len(c['items']) == 18
assert len(gg['nodes']) == 38 and len(gg['edges']) == 76 and len(gi['items']) == 47
assert len(gi['atomic_dispositions']) == 72
ids = {n['id'] for n in g['nodes']}
assert all(e['source'] in ids and e['target'] in ids for e in g['edges'])
assert all(set(j['all_of']) == {e['source'] for e in g['edges'] if e['target'] == j['target']} for j in g['AND_junctions'])
assert not g['alternative_routes']
assert not any('88' in e['source'] or 'atom' in e['source'].lower() for e in g['edges'])
assert sum(bool(e['dependency_edge']) for e in gg['edges']) == 73
assert sum(not e['dependency_edge'] for e in gg['edges']) == 3
assert sum(x['disposition'] == 'NODE' for x in c['items']) == 11
assert sum(x['disposition'] == 'EXCLUDED' for x in c['items']) == 7
reconstruction = pin(D / 'primary-source-reconstruction89.json')
assert reconstruction['raw_sha256'] == '96df1a8a026a4ba51edfcb507bd9b95b7b626bc9aeb54f117b5fef40ea43d9ad'

edge_checks = [
    ('S89-D1', 'S89-A1', 'Literal source maps determine the joint Borel/arc regularity task; no supplied surrogate.'),
    ('S89-D1', 'S89-A2', 'The reused86 producer concerns this exact literal crossing, under its internally constructed actual Exp1 input law.'),
    ('S89-A1', 'S89-A2', 'Continuous nonnegative free-arc rate gives C1 finite hazard, needed inside the already verified deterministic density parent.'),
    ('S89-A1', 'S89-P1', 'Joint Borel maps, not merely separate sections, supply measurable guarded integrands before integration.'),
    ('S89-D1', 'S89-P1', 'Finite/stopped tags and actual crossing specify what the observable encodes; no phase at infinity.'),
    ('S89-A2', 'S89-P2', 'Restrict the exact Ioc density measure equality by the strict Borel Iio cutoff on BOTH sides.'),
    ('S89-P1', 'S89-P2', 'Every fixed history supplies a measurable time section and finite cutoff; admissible jointly Borel tests can be evaluated.'),
    ('S87-I3', 'S89-T', 'Actual H_n and full unused tail have a product law, so the state/history may be random without illicit correlated substitution.'),
    ('S89-P1', 'S89-T', 'Joint measurable density/guard/test and sigma-finite time measure allow nonnegative parameter integration.'),
    ('S89-P2', 'S89-T', 'Integrate each exact finite section against the actual history law; obtain a subprobability law without normalization.'),
    ('S89-T', 'S87-I5-assembly', 'A genuine next-jump factor for later finite iteration; necessary within that source route but not sufficient for A.7.')
]
assert [(e['source'], e['target']) for e in g['edges']] == [(a,b) for a,b,_ in edge_checks]
coverage_checks = [
    'Standing C2/Hessian/curvature conditions retained; not extra analytic estimates as binders.',
    'Positive scale and range retained exactly.',
    'Actual center and gradient difference retained.',
    'Actual free flow/rate/reflection and zero-normal convention retained.',
    'Exp1 source input is consumed internally by BOTH reused deterministic86 density and actual87 history/tail product. The compressed local slice treats these as existing producer nodes, not new axiomatic derivations from regularity alone. Global G86-03->G86-10/G86-11 remains pinned.',
    'Closed >= crossing with possible infinity determines the actual waiting variable.',
    'Finite update and absorbing stopped tag supply Borel constructor semantics without stopped phase.',
    'Free arc determines prejump density at prospective wait s.',
    'Strict ordered times consume Ioo, obtained by exact measure restriction; endpoint equality is not asserted.',
    'A.7 iteration is refined into distinct existing density, product, Borel section, strict restriction and new target, while full assembly remains OPEN.',
    'A.2 finite Borel recursion supplies internal measurability; no public provider premise.',
    'Final survival factor is adjacent88 and future assembly, not a false AND prerequisite for this finite-density target.',
    'Signed path functional, absolute series convergence and trajectory assembly are excluded with reasons and preserved globally.',
    'Infinite-jump terminal limit/nonexplosion is not needed for deterministic finite-depth histories.',
    'Global reversal/invariance/Markovness/operator branches are explicitly outside local89 and retained in the unchanged exhaustive global inventory.',
    'Endpoint no-atom bridge is not needed for restriction; any later closed/strict mass equivalence must derive it internally.',
    'No total finite-mass normalization/infinity-defect limit claim; only subprobability bound.',
    'No external source theorem supplied as a provider; standard product/Tonelli contracts are internal proof dependencies.'
]
topology = out('source-topology89.decision.json', {
    'schema': 1, 'reviewer_id': '/root/exact_verify77', 'creator_id': '/root/fresh_source87',
    'status': 'ACCEPTED_INDEPENDENT_SOURCE_ONLY_TOPOLOGY_AND_COVERAGE', 'created_utc': UTC,
    'checked_workspace_commit': HEAD, 'primary': pin(primary_path),
    'independent_primary_reconstruction': reconstruction,
    'own_primary_reconstruction_frozen_before_author_graph_read': True,
    'author_graph_first_read_tool_chunk': 'ab636a', 'candidate89_seen': False, 'BODY89_seen': False,
    'author_private_extraction_or_freeze_scripts_semantically_read': False,
    'implementation_Lean_used_to_determine_source_topology': False,
    'reviewed_graph': pin(A / 'source-proof-graph89.native.json'),
    'reviewed_coverage': pin(A / 'source-coverage89.native.json'),
    'reviewed_author_freeze': pin(A / 'source-first89.native.json'),
    'reviewed_author_closed_manifest': pin(manifest_path),
    'counts': {'local_nodes':8,'local_edges':11,'local_AND_junctions':4,'local_dispositions':18,'NODE':11,'EXCLUDED':7,'primary_spans':7,'global_items':47,'global_nodes':38,'global_relations':76,'global_dependencies':73,'global_excluded_associations':3,'global_atomic_dispositions':72},
    'node_checks': [
        {'id': n['id'], 'accepted_as': n['kind'], 'reason': reason}
        for n,reason in zip(g['nodes'], [
            'Literal source construction, reused without invented phase/clock replacement.',
            'Joint Borel maps and C1 finite hazard are derivable internal ingredients, not assumptions supplied by caller.',
            'Already verified86 deterministic actual Exp1 finite density is a reusable parent; not re-proved or credited by this source-only review.',
            'Already verified87 actual complete history/full raw-tail product is the finite-depth independence parent.',
            'Joint Borel density/test/finite-observable and parameter integration are essential internal work, with sigma-finite canonical time measure.',
            'Ioc density law restricted by Iio yields Ioo exactly; includes all arbitrary Borel sections.',
            'Strictly new random-history joint test/density and subprobability interface, attributed ASTIS completion rather than a printed theorem.',
            'Future iteration/final-survival/path-functional/count-sum assembly remains OPEN.'
        ])],
    'edge_checks': [{'source':a,'target':b,'status':'ACCEPT','reason':r} for a,b,r in edge_checks],
    'AND_checks': [{'target':j['target'],'all_of':j['all_of'],'status':'ACCEPT_AS_CONJUNCTIVE_SELECTED_ROUTE'} for j in g['AND_junctions']],
    'reused_parent_boundary': 'S89-A2 and S87-I3 denote actual verified producer contracts including their internally derived actual Exp1 laws. The local lineage under A2 is not a new sufficient proof from flow regularity alone. The pinned global OR routes explicitly retain G86-03 clock-law edges. No density or independence provider binder is admitted.',
    'coverage_checks': [{'item':x['item'],'disposition':x['disposition'],'status':'ACCEPT','independent_reason':r} for x,r in zip(c['items'],coverage_checks)],
    'global_OR_preserved': {'deterministic_density':'CDF route OR monotone-hazard transport; each route has conjunctive source ingredients. The new slice reuses verified86 instead of forcing both routes.', 'path_series':'Fixed-state analytic summability remains a sufficient optional route; nonexplosion/positive event partition alternative remains distinct.', 'no_global_mutation':True},
    'global_excluded_associations_preserved': ['E86-64 optional law representation is not pathwise invariance premise','E86-65 typed probability kernel does not prove temporal Markov/CK','E86-66 heuristic generator exponentiation is not accepted implication'],
    'endpoint_audit': 'For fixed h put t=d(h). Restrict both sides of mu|Ioc(0,t)=rho*nu|Ioc(0,t) by Iio(t); intersections are exactly Ioo(0,t), including t=0. Do not equate closed and open masses. Mass<=1 follows from restricting a probability pushforward. No no-atom theorem is an AND parent.',
    'test_measure_audit': 'd is a fixed Borel finite NNReal-valued history function, possibly globally unbounded; F is a jointly Borel ENNReal nonnegative test, possibly unbounded/infinite. These select admissible tests and are not additional PBPS analytic/provider assumptions. Canonical NNReal Lebesgue trace must match any future header exactly. Weighted tests need not have finite integrals; the unweighted kernel mass is <=1.',
    'degenerate_cases': ['n=0','A null or empty without point division','d(h)=0','finite wait exactly d(h) excluded on both sides','live next wait infinity contributes zero finite mass','already stopped has zero kernel and no next phase','rank0 or identically zero orbit hazard','initial rate0 need not imply whole orbit rate0','flat hazard without inverse differentiability','nonpositive raw threshold clipped to0 and strict positive guard excludes it','all abstract histories allowed; actual history measure weights only realized ones'],
    'source_implicit_classification': 'Deterministic finite density, actual finite-history product, joint measurable random-section integration and the new joint test law are explicit ASTIS completions of the authors A.7 clock iteration. No source gap is silently made a premise. No additional analytic source assumption found.',
    'required_repairs': [], 'proposed_overlay': None,
    'remaining_obligations': ['Exact future whole-header mathematical and pinned Lean type review','Internal joint Borel/guard/test/section derivations','Exact parent definitions and canonical time measure interface audit','Independent whole BODY, decoder, final source and later named-commit admission if implemented','Full S87-I5/G86-11/A.7 iteration and final survival/path/count assembly remain OPEN','Physical-time restart/Markov/CK/invariance/all-L2/cost/main/PURIFIED/reader/whole-paper/Goal remain OPEN'],
    'credit': {'StatementSeal':False,'new_proof':False,'theorem_complete':False,'VERIFIED':False,'shared_state_mutation':False,'Goal_complete':False}
})
checks = out('source-topology89.evidence.json', {
    'schema':1, 'reviewer_id':'/root/exact_verify77', 'checked_workspace_commit':HEAD,
    'hash_check_inputs':len(m['inputs']), 'hash_check_outputs':len(m['outputs']), 'hash_check_spans':len(spans),
    'author_manifest_entries_checked':hash_checked, 'primary_spans':spans,
    'semantic_reads': [pin(A/x) for x in ('source-proof-graph89.native.json','source-coverage89.native.json','source-first89.native.json','closed-raw-manifest.source-first89.native.json','chronology.source-first89.native.jsonl','terminal-completion.source-first89.native.json','unchanged-global-source-evidence89.native.json')]+[pin(gg_path),pin(gi_path)],
    'hash_only_not_semantic_reads': [pin(A/x) for x in ('primary89.direct-read.private.json','read_primary_first89.py','seal_source_first89.py','primary-source89.raw-manifest.native.json')],
    'author_counts_verified':True, 'all_AND_parents_have_exact_corresponding_edges':True,
    'source_graph_and_inventory_unchanged':True, 'no_Lean_compiler_run_at_this_source_only_stage':True,
    'no_whole_global_new_completion_claim':True
})
run = out('source-topology89.run.json', {
    'schema':1,'reviewer_id':'/root/exact_verify77','completed_utc':UTC,'checked_workspace_commit':HEAD,
    'status':'CLOSED_SOURCE_ONLY_TOPOLOGY_REVIEW',
    'terminal_observations':[
        {'tool_chunk':'cd5d91','exit_code':0,'scope':'Direct complete primary A.1/A.2 read before author graph/header; preserved reconstruction chronology.'},
        {'tool_chunk':'330ce7','exit_code':0,'scope':'Foreground primary-only reconstruction freeze script; no author graph read yet.'},
        {'tool_chunk':'ab636a','exit_code':0,'scope':'Read CLOSED author graph after own reconstruction freeze.'},
        {'tool_chunk':'3790bf','exit_code':0,'scope':'Read author local coverage.'},
        {'tool_chunk':'1d030f','exit_code':0,'scope':'Read source-only freeze.'},
        {'tool_chunk':'8df359','exit_code':0,'scope':'Read author closed manifest.'},
        {'tool_chunk':'9bb872','exit_code':0,'scope':'Read author source-first chronology.'},
        {'tool_chunk':'bd8f66','exit_code':0,'scope':'Validate all8inputs/10outputs/7spans; inspect global nodes and inventory.'},
        {'tool_chunk':'a8a6e9','exit_code':0,'scope':'Inspect all global edges/junctions and remaining inventory; OR and excluded associations preserved.'},
        {'tool_chunk':'5e1ae3','exit_code':0,'scope':'Direct reread seven exact primary spans including original standing hypotheses/scale and A7/A2; no long primary text published.'},
        {'tool_chunk':'9730e6','exit_code':0,'scope':'Read own frozen chronology, author terminal closure and unchanged-global descriptor.'}
    ],
    'outputs':[topology,checks], 'foreground_only':True,'compiler_credit':False,'native_hidden_trajectory_fabricated':False,
    'writes_confined_to':D.as_posix(), 'failures_at_this_comparison_stage':[]
})
owned = [pin(p) for p in sorted(D.iterdir()) if p.is_file()]
closed = out('source-topology89.closed-RAW-manifest.json', {
    'schema':1,'status':'CLOSED_INDEPENDENT_SOURCE_ONLY_TOPOLOGY_REVIEW_NOT_STATEMENT_SEAL_OR_PROOF',
    'reviewer_id':'/root/exact_verify77','checked_workspace_commit':HEAD,
    'frozen_current_inputs':[pin(primary_path),pin(manifest_path)]+[pin(A/x) for x in ('source-proof-graph89.native.json','source-coverage89.native.json','source-first89.native.json','chronology.source-first89.native.jsonl','terminal-completion.source-first89.native.json','unchanged-global-source-evidence89.native.json')]+[pin(gg_path),pin(gi_path)],
    'author_recursive_manifest_entries_verified':hash_checked,
    'owned_artifacts':owned, 'decision':topology,'run':run,'evidence':checks,
    'closure':'Self excluded; prior primary-only manifest remains immutable. All exact input RAWs rechecked. Author private extraction/scripts hashed only, not used as scientific evidence. No candidate/header/BODY read or Lean proof created.'
})
print(json.dumps({'decision':topology,'run':run,'closed_manifest':closed},ensure_ascii=False))
