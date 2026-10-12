from pathlib import Path
import gzip
import hashlib
import json
import re

ROOT = Path('E:/Samplinglib')
B = 'runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106'
O = ROOT / B / 'final-source106'
P = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedGibbsDuality.lean'
L = 'website/content/declaration_lessons/pbps-actual-bounded-gibbs-duality.json'
U = 'website/content/publications/pbps-actual-bounded-gibbs-duality.json'
PRE = 'runs/20261007-companion-priority/pbps-bounded-gibbs-duality-preread106'
OLD = 'runs/20261007-companion-priority/pbps-actual-countable-endpoint105/next-primary106'
D = 'runs/semantic-roundtrip/anonymous106/decoder-native'
inputs = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def ref(path):
    path = path.replace('E:/Samplinglib/', '').replace('\\', '/')
    b = (ROOT / path).read_bytes()
    d = {'path': path, 'raw_sha256': sha(b), 'bytes': len(b)}
    inputs[path] = d
    return d


def load(path):
    ref(path)
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def put(name, obj):
    p = O / name
    assert not p.exists()
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode())
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}


frozen = load(B + '/final-source106/primary-first106.native.json')
primary = ref(frozen['primary']['path'])
assert primary == frozen['primary']
rawprimary = (ROOT / primary['path']).read_bytes()
for row in frozen['all21_source_regions_rehashed']:
    assert sha(rawprimary[row['byte_start']:row['byte_end_exclusive']]) == row['raw_sha256']
packet = load(B + '/reviewer-packet106.json')
packet_hash = packet['packet_sha256']
assert packet_hash == '39e68938cdc13a08fc1bebea01a8b5b6f1c16cddfcf018211028c5ff374896e1'
assert sha(json.dumps({k: v for k, v in packet.items() if k != 'packet_sha256'}, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()) == packet_hash
assert all(v is False for v in packet['anti_anchoring'].values())
binding = packet['publication_binding_sha256']
assert binding == '749440152478c976a357af4e6f2ad8c98031682582839d2b63370224131994dc'
prod = ref(P)
raw = (ROOT / P).read_bytes()
assert prod['raw_sha256'] == '4fad17d78149b7a4a784170309e9de3f70941ef533f90228b0405dee5fc2707d'
lines = raw.splitlines(keepends=True)
assert len(lines) == 247
s = raw.decode('utf8').replace('\r\n', '\n')
header = ref(PRE + '/Header106.lean')
hs = (ROOT / header['path']).read_text(encoding='utf8')
assert s[s.index('    {E : Type*}'):s.index('\n\n\nset_option maxHeartbeats')] == hs[hs.index('    {E : Type*}'):hs.index('\n\n#check candidate')]
context = load(OLD + '/literal-definition-context106.native.json')
assert s[s.index('    let c :'):s.index('    ∃ Z :')] == context['literal37_LF_text']
assert s[s.index('    ∃ Z :'):s.index('      (∀ y xRef : E, ∀ T : ℝ≥0,')] == context['global_witness_prefix_LF_text']
prop = s[s.index('private def '):s.index('\n\n\nset_option maxHeartbeats')]
assert len(re.findall(r'^\s+let ', prop, re.M)) == 39
assert packet['candidate_publication_context']['current_lean_module'] == s
assert packet['candidate_publication_context']['file'] == prod['raw_sha256']
unit = load(L)['units'][0]
pub = load(U)['items'][0]
assert unit['statement'] == pub['statement'] == packet['source']['original_text']
assert unit['lean_statement'] == unit['statement']
assert unit['statement'].count('\\n') == 0 and unit['statement'].count('\n') == 12

manifest = load(D + '/manifest.json')
decoder = load(D + '/decoder.json')
recon = ref(D + '/reconstruction.txt')
assert (ROOT / recon['path']).read_text(encoding='utf8') == packet['blind_reconstruction']['text']
for name, digest in manifest['output_hashes'].items():
    assert ref(D + '/' + name)['raw_sha256'] == digest
assert ref(manifest['input_path'])['raw_sha256'] == manifest['input_raw_sha256']
assert inputs[D + '/manifest.json']['raw_sha256'] == packet['blind_reconstruction']['decoder_run_sha256']
assert manifest['packet_sha256'] == packet['blind_reconstruction']['decoder_packet_sha256']
assert manifest['decoder_identity']['agent_id'] == '/root/blind_decoder106'
assert all(manifest[k] is False for k in ['source_visible', 'informal_proof_visible', 'publication_visible', 'repair_visible', 'reviewer_visible'])
wm = load(B + '/independent-whole-math106/whole-math-decision106.native.json')
kernel = load(B + '/independent-whole-math106/fresh-kernel-receipt106.native.json')
assert wm['decision'] == 'ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL'
assert kernel['exit_code'] == 0 and kernel['terminal_closed']
assert wm['production'] == prod == kernel['production']
for name in ['input', 'stdout', 'stderr']:
    assert ref(kernel[name]['path']) == kernel[name]
fresh = (ROOT / kernel['input']['path']).read_bytes()
assert fresh.startswith(raw)
assert 'import ' + 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality' not in fresh.decode('utf8')
assert all(a['axioms'] == ['propext', 'Classical.choice', 'Quot.sound'] for a in wm['kernel_contract']['axioms'])
ref(B + '/independent-whole-math106/closed-RAW-manifest106.native.json')
ref(wm['seal']['path'])
graph = load(B + '/source-graph106.effective.json')
top = load(OLD + '/independent-topology106/topology-admission106.native.json')
overlay = load(B + '/independent-whole-math106/route-topology106/route-topology-admission106.native.json')
assert overlay['decision'] == 'ACCEPT_MINIMAL_SELECTED_DIRECT_MARGINAL_OVERLAY'
assert ref(overlay['proposal']['path']) == overlay['proposal']
assert ref(overlay['original_graph']['path']) == overlay['original_graph']
assert ref(overlay['selected_route']['path']) == overlay['selected_route']
assert graph['effective_counts'] == {'nodes': 62, 'edges': 123, 'primary_regions': 21}
assert ref(graph['independent_overlay_admission']['path'])['raw_sha256'] == graph['independent_overlay_admission']['raw_sha256']
oldcoverage = ref(graph['inherited_compiled_source_coverage105']['path'])
assert oldcoverage == graph['inherited_compiled_source_coverage105']
nodes = top['effective_graph']['nodes']
edges = top['effective_graph']['edges'] + overlay['exact_delta']['new_edges']
assert len(nodes) == 62 and len(edges) == 123


def span(a, b):
    data = b''.join(lines[a - 1:b])
    return {'file': P, 'line_start': a, 'line_end': b, 'RAW_sha256': sha(data),
            'LF_sha256': sha(data.replace(b'\r\n', b'\n')), 'bytes': len(data)}


step_judgments = [
    'One extraction from105 returns Z and forwards its four original contracts; no second93/83 witness.',
    '103 and the unit clock producer provide actual probabilities; same-Z specialization gives endpoint/M measurability and105 gives Q probability/J preservation.',
    'Literal momentum flip preserves standard Gaussian by negation isometry and preserves exact position-first phase product.',
    'Selected direct marginal composition M→J→fst→R is the actual endpoint; P mass1 is essential. Explanation distinguishes ASTIS route from printed F=1.',
    'The actual product integrand is Borel and bounded by CF*CG under a probability product, yielding genuine real L1.',
    'Product L1 gives the outer L1; signed Fubini and measurable pushforward identify its value. No unproved integrability premise.',
    'The flipped pair uses swapped bounds and measurable R; both required outer integrabilities are provided.',
    'J action yields F(R end)G(R start); scalar commutation matches G(R start)F(R end), preserving the source duality orientation.'
]
steps = []
for i, (step, judgment) in enumerate(zip(unit['steps'], step_judgments), 1):
    r = step['lean_source_region']
    a, b = r['start_line'], r['end_line']
    code = b''.join(lines[a - 1:b])
    assert code.replace(b'\r\n', b'\n').decode('utf8') == step['lean']
    assert sha(step['lean'].encode()) == r['exact_code_raw_sha256']
    assert r['source_raw_sha256'] == prod['raw_sha256']
    runs = [len(m.group()) for m in re.finditer(r'\\+', step['formula'])]
    assert runs and set(runs) == {1}
    steps.append({'step': i, 'title': step['title'], 'span': span(a, b), 'display_code_RAW_sha256': sha(step['lean'].encode()),
                  'formula_RAW_sha256': sha(step['formula'].encode()), 'decoded_backslash_run_lengths': runs,
                  'explanation_RAW_sha256': sha(step['text'].encode()), 'judgment': judgment, 'accepted': True})
assert len(steps) == 8
assert [(r['span']['line_start'], r['span']['line_end']) for r in steps] == [(164, 168), (169, 185), (186, 193), (194, 204), (205, 217), (218, 228), (229, 236), (237, 243)]
for formula in [unit['formula']] + [f['tex'] for f in pub['formulae']]:
    assert set(len(m.group()) for m in re.finditer(r'\\+', formula)) == {1}
parents = [
    {'declaration': 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw.actual_countable_endpoint_law', 'span': span(164, 168), 'discharge': 'Six original analytic binders; single globally chosen actual Z and exact endpoint law. Q/J literals reduce to105 definitions at180–185.'},
    {'declaration': 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization', 'span': span(169, 174), 'discharge': 'Same six analytic binders and y; exact product identification transports phase probability.'},
    {'declaration': 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws', 'span': span(175, 176), 'discharge': 'Unconditional exact unit-rate clock probability; finite/SFinite product and fst marginal mass.'}
]
assert [p['declaration'] for p in parents] == unit['astis_dependencies']
exposition = put('exposition106.native.json', {
    'verdict': 'ACCEPT_BOUNDED_AUTHORED_EIGHT_STEP_EXPOSITION_ONLY', 'reviewer': '/root/source_final96',
    'reviewer_packet_sha256': packet_hash, 'publication_binding_sha256': binding,
    'production': prod, 'lesson': inputs[L], 'publication': inputs[U], 'steps': steps,
    'statement_review': 'Complete original six conditions, actual37 inherited objects, one global witness, H/R/Vy/pi/gamma/nu/op/endpoint notation, every-time and bounded-observable quantifiers, both L1 conclusions and phase-first pushforward are explicit. All global-Z clauses retain their original senses.',
    'source_route_attribution': 'Step4 explicitly labels direct marginal proof as implementation completion and retains printed F=1 source consequence. Independent route overlay already admitted. Steps5–8 fully prove signed averaging separately.',
    'exact_code_contract': 'Eight adjacent lesson code strings equal their production spans after CRLF-to-LF only. Both original span RAW and displayed string RAW are recorded; exact_code_raw_sha256 denotes displayed LF code, not original CRLF bytes.',
    'formula_rendering': {'decoded_TeX_commands_all_one_backslash': True, 'statement_actual_newlines': 12, 'literal_backslash_n_in_statement': 0, 'matrix_row_separators': 'none'},
    'folded_reader_contract': 'One named private Prop helper and public declaration support folded full statement, full proof and eight adjacent code regions. This review checks authored content/bindings only; generated DOM folding and actual browser are later delivery checks.',
    'private_helper': unit['helpers'], 'actual_public_parents': parents,
    'source_theorem_repairs': [], 'exposition_repairs': [], 'defects': [],
    'full_Exposition_Seal': False, 'actual_browser_acceptance': False, 'whole_paper_complete': False
})

regions = []
for row in frozen['all21_source_regions_rehashed']:
    r = dict(row)
    rid = r['id']
    r['compiled106_disposition'] = (
        'Original analytic assumptions at13–20 and153–160; exact header equality.' if rid in ['standing-curvature', 'standing-eta'] else
        'Literal target phase law119–123; probability169–176; momentum symmetry186–193.' if rid in ['target-position-energy', 'phase-gibbs-law'] else
        'Literal actual context23–118 and same global witness124–133, forwarded164–168; no changed representative or fixed-count semantics.' if rid in ['actual-phase', 'event-convention', 'simplex', 'prescribed'] else
        'Selected signed averaging205–243 and direct marginal194–204. Printed F=1 retained as source alternative; trailing L2 extension remains red.' if rid == 'weight-matching-and-invariance' else
        'Actual joint Gibbs-clock law M,Q at180–185; signed transfer205–228, using existing105 count assembly rather than repeating it.' if rid == 'average' else
        'Future full L2/operator semantics excluded; bounded signed scalar identity is the only selected portion.' if rid == 'A3-boundary' else
        'License reference only; no new full-primary archive.' if rid == 'source-license' else
        'Inherited unchanged source mechanism in exact105 compiled coverage; consumed through105 endpoint law or103 normalization. No new proof credit for this region.')
    regions.append(r)
clock = parents[2]['declaration']
selected_nodes = {'COUNT93': [(164, 179)], 'ENDPOINT-LAW105': [(164, 185)], 'NORM': [(169, 174)],
                  clock: [(175, 176)], 'PHASE-FLIP106': [(186, 193)], 'INV100': [(194, 204)],
                  'SIGNED-FUBINI106': [(205, 228)], 'AVG100': [(229, 243)], 'H99': [(13, 20), (153, 160)]}
node_rows = []
for node in nodes:
    if node in selected_nodes:
        row = {'id': node, 'disposition': 'current selected compiled producer/projection/adapter', 'spans': [span(*x) for x in selected_nodes[node]]}
    elif node in ['L2A3', 'RESTART']:
        row = {'id': node, 'disposition': 'future source obligation excluded from106', 'new_credit': False}
    else:
        row = {'id': node, 'disposition': 'unchanged inherited source mechanism; exact prior node disposition reused', 'inherited_coverage': oldcoverage, 'lookup_node_id': node, 'new_credit': False}
    node_rows.append(row)
edge_rows = []
for a, b in edges:
    disposition = ('retained printed F=1 source alternative, not a direct invoked Lean step' if (a, b) == ('AVG100', 'INV100') else
                   'selected direct marginal incidence at184,194–204, independently admitted overlay' if (a, b) == ('ENDPOINT-LAW105', 'INV100') else
                   'future excluded consumer edge' if b in ['L2A3', 'RESTART'] else
                   'current source dependency incidence; actual proof spans given by endpoint node dispositions' if b in selected_nodes else
                   'unchanged inherited source incidence; exact105 coverage reused')
    edge_rows.append({'source': a, 'target': b, 'disposition': disposition, 'not_a_new_kernel_dependency_certificate': True})
allspans = [(1, 11, 'Imports/context; no mathematical target'), (12, 146, 'Private exact sealed Prop with39lets and global witness'),
            (147, 160, 'Resource controls/comment/public six-binder target'), (161, 163, 'Expose exact literal Prop'),
            *[(r['span']['line_start'], r['span']['line_end'], r['judgment']) for r in steps],
            (244, 247, 'Axiom print and section/namespace closure')]
assert [i for a, b, _ in allspans for i in range(a, b + 1)] == list(range(1, 248))
cov = put('compiled-source-coverage106.native.json', {
    'kind': 'independently owned complete compiled106 source coverage', 'reviewer': '/root/source_final96',
    'reviewer_packet_sha256': packet_hash, 'publication_binding_sha256': binding, 'production': prod,
    'source_primary': primary, 'source_graph': inputs[B + '/source-graph106.effective.json'],
    'independent_base_topology': inputs[OLD + '/independent-topology106/topology-admission106.native.json'],
    'independent_overlay_admission': inputs[B + '/independent-whole-math106/route-topology106/route-topology-admission106.native.json'],
    'topology_self_validation': False, 'effective_counts': {'nodes': 62, 'edges': 123, 'source_regions': 21, 'production_lines': 247, 'statement_lets': 39, 'actual_parents': 3, 'exposition_regions': 8},
    'source_regions': regions, 'node_dispositions': node_rows, 'edge_dispositions': edge_rows,
    'all_production_regions': [dict(span(a, b), disposition=d) for a, b, d in allspans],
    'whole_module': 'All247lines read; private Prop and public theorem owned by this review, including internal htest and all have/let constructions. No hidden helper/provider or mangled API.',
    'literal_definition_audit': {'header': header, 'private_Prop_equal_original_header': True, 'inherited37_LF_equal': True, 'global_Z_contract_equal': True, 'new_let_names': ['op', 'endpoint'], 'all39_expanded': True},
    'actual_parent_discharge': parents, 'proof_ingredient_vs_source_binder': 'All probability, symmetry, measurability and signed-integrability facts derived internally; only six analytic binders plus source observable conditions remain.',
    'source_route': 'Printed AVG→INV is preserved as an alternative; selected direct105→INV has its own independently admitted edge. SIGNED-FUBINI/AVG is fully implemented separately.',
    'proof_sense': 'Stepwise source-to-implementation coverage, not source-graph creator self-admission. Fresh Lean/kernel evidence reused independently of fidelity judgment.',
    'fresh_kernel': inputs[B + '/independent-whole-math106/fresh-kernel-receipt106.native.json'],
    'whole_math': inputs[B + '/independent-whole-math106/whole-math-decision106.native.json'],
    'remaining_reds': ['L2A3', 'RESTART', 'Actual semigroup/Chapman–Kolmogorov', '83 witness identification', 'Hypocoercivity/errors/actual costs/full papers/composition']
})

expected = frozen['expected_semantic_slots']
slot_info = {
    'objects': ('objects', decoder['objects'], 'same', 'All37 inherited definitions literally equal frozen105 context; new op/endpoint use same produced Z.39let Prop matches original Header106 exactly.'),
    'domains': ('domains', decoder['domains'], 'explicit-elaboration', 'Finite inner-product Borel E including rank0; all y,r, finite NNReal T; pointwise bounded Borel real F,G. Canonical coordinate-free generalization is explicit; no restricted observables.'),
    'quantifiers': ('quantifiers', decoder['quantifiers'], 'equivalent', 'One global existential Z precedes all parameters, times and observables. Zero initialization remains parameterwise a.e.; test bounds are independent universal variables.'),
    'assumptions': ('assumptions', decoder['hypotheses'], 'same', 'Six original analytic binders and nested source test-class hypotheses only. No probability, integrability, kernel, normalizer or arbitrary provider premise.'),
    'conclusion': ('conclusion', decoder['conclusions'], 'explicit-elaboration', 'Actual endpoint MeasurePreserving plus both outer L1 conclusions and correctly oriented flipped signed identity. Source suppressed integrability is proved at205–228, then applied twice.'),
    'scopes': ('scopes_senses', decoder['scope'], 'same', 'Only actual fixed-time phase law and bounded signed duality. No semigroup/Markov/L2,83-witness identification or jumpwise path reversal assertion.'),
    'constant_dependencies': ('constant_dependencies', decoder['dependencies'], 'same', 'Exact sqrtη,1/(2η),unit exponential and standard Gaussian factors; arbitrary CF,CG swapped correctly on right. Zero bounds/rates/dimension/time remain included.')
}
slots = {k: {'original': expected[v[0]], 'reconstructed': v[1], 'relation': v[2], 'evidence': v[3]} for k, v in slot_info.items()}
deltas = [
    {'slot': 'domains', 'severity': 'informational', 'description': 'Explicit coordinate-free finite-dimensional and rank-zero elaboration.', 'source': 'Euclidean phase formulas.', 'lean': 'Finite-dimensional real inner-product Borel E.', 'evidence': 'All exact volume/Gaussian/flow conventions retained; original six conditions unchanged and no dimension-positive premise.', 'blocking': False},
    {'slot': 'conclusion', 'severity': 'informational', 'description': 'Expose signed L1 obligations and actual endpoint measure equality.', 'source': 'Bounded bilinear identity and F=1 stationarity.', 'lean': 'Two Integrable conclusions and MeasurePreserving actual endpoint.', 'evidence': 'Internal finite-probability bound, signed Fubini and actual endpoint law discharge all obligations; no extra public premise.', 'blocking': False},
    {'slot': 'scopes', 'severity': 'informational', 'description': 'Use separately admitted equivalent direct-marginal route for the fixed-time consequence.', 'source': 'Printed F=1 route after signed duality.', 'lean': 'Compose M,J,fst,R at194–204 and separately prove full signed duality205–243.', 'evidence': 'Independent one-edge route overlay preserves source alternative and exact header. No Markov/L2 extension credited.', 'blocking': False}
]
run = put('source-review-run106.native.json', {
    'reviewer': '/root/source_final96', 'formalizer': packet['roles']['formalizer'], 'decoder': '/root/blind_decoder106',
    'reviewer_packet': inputs[B + '/reviewer-packet106.json'], 'reviewer_packet_sha256': packet_hash,
    'publication_binding_sha256': binding, 'production': prod, 'primary_first': inputs[B + '/final-source106/primary-first106.native.json'],
    'compiled_coverage': cov, 'exposition': exposition, 'decoder_manifest': inputs[D + '/manifest.json'],
    'source_input_read_before_production_and_decoder': True, 'prior_semantic_verdict_slots_deltas_or_repairs_used': False,
    'prior_involvement': frozen['prior_involvement'], 'independently_owned_whole_module_review': True,
    'independent_math_evidence_use': 'Rehash fresh exact source-plus-original-header kernel evidence and standard3 axioms; fidelity and exposition judgments independently authored.',
    'no_topology_self_validation': True, 'no_shared_mutation': True, 'no_VERIFIED_transition': True,
    'browser_acceptance': False, 'full_paper_credit': False
})
decision = put('source-review106.native.json', {
    'semantic_slots': slots, 'deltas': deltas, 'verdict': 'equivalent-after-elaboration', 'repairs': [],
    'reviewer_packet_sha256': packet_hash, 'publication_binding_sha256': binding, 'review_run_sha256': run['raw_sha256'],
    'source_review': {'state': 'accepted', 'reviewer': '/root/source_final96',
                      'independent_from_formalizer': True, 'independent_from_decoder': True,
                      'reviewer_packet_sha256': packet_hash, 'review_run_sha256': run['raw_sha256'],
                      'publication_binding_sha256': binding, 'run_artifact': run['path'],
                      'evidence': 'Fresh primary-first freeze and exact21slice rehash, independent seven-slot comparison with current anonymous106 reconstruction, whole247line/39let/3producer review, effective62node123edge compiled coverage with independent overlay admission, and all8 authored formula/code regions accepted. No blocker or source repair. Fixed-time law/duality only; browser/full-paper/Markov/L2 remain separate.',
                      'prior_verdicts_or_slots_used': False, 'whole_module_private_helper_reviewed': True,
                      'independently_owned_exposition_audit': True, 'source_graph_creator_self_validation': False},
    'compiled_source_coverage': cov, 'bounded_exposition': exposition,
    'whole_module': {'production': prod, 'lines': 247, 'private_Prop': 'actual_bounded_gibbs_duality_statement', 'public_theorem': packet['lean']['declaration'], 'all_internal_helpers_reviewed': True},
    'defects': [], 'browser_acceptance': False, 'full_Exposition_Seal': False, 'full_paper_completion': False
})
archives = []
for p in sorted(O.iterdir()):
    if p.is_file():
        data = p.read_bytes()
        z = Path(str(p) + '.raw.gz')
        assert not z.exists()
        z.write_bytes(gzip.compress(data, mtime=0))
        assert gzip.decompress(z.read_bytes()) == data
        archives.append({'raw_path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(data), 'archive': z.relative_to(ROOT).as_posix(), 'archive_raw_sha256': sha(z.read_bytes())})
owned = [{'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}
         for p in sorted(O.iterdir()) if p.is_file()]
closure = put('closed-RAW-final-source106.native.json', {
    'kind': 'closed independent final source/exposition106 RAW manifest', 'decision': decision,
    'reviewer_packet_sha256': packet_hash, 'publication_binding_sha256': binding, 'run': run,
    'selected_inputs': list(inputs.values()), 'owned_artifacts': owned, 'original_RAW_archives': archives,
    'no_full_primary_archive': True, 'self_hash_intentionally_omitted': True
})
print(json.dumps({'decision': decision, 'coverage': cov, 'exposition': exposition, 'run': run, 'closure': closure}, indent=2))
