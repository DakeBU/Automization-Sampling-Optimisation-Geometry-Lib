from pathlib import Path
import json
import hashlib
import re
import copy
import gzip

R = Path('E:/Samplinglib')
BASE = R / 'runs/20261007-companion-priority'
B = BASE / 'pbps-actual-countable-endpoint105'
P = BASE / 'pbps-countable-endpoint-preread105'
O = B / 'final-source105'
S = BASE / 'pbps-actual-normalized-endpoint104/next-primary105'
PROD = R / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCountableEndpointLaw.lean'
LESSON = R / 'website/content/declaration_lessons/pbps-actual-countable-endpoint-law.json'
PUB = R / 'website/content/publications/pbps-actual-countable-endpoint-law.json'
DECODE = R / 'runs/semantic-roundtrip/anonymous105'
PRIMARY = BASE / 'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load(p):
    return json.loads(p.read_text(encoding='utf8'))


def ref(p):
    b = p.read_bytes()
    return {'path': p.relative_to(R).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}


def put(n, d):
    p = O / n
    assert not p.exists(), n
    p.write_bytes((json.dumps(d, ensure_ascii=False, indent=2) + '\n').encode())
    return ref(p)


def canonical(d):
    return sha(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


packet = load(B / 'reviewer-packet105.json')
packet_hash = packet['packet_sha256']
unhashed = dict(packet)
unhashed.pop('packet_sha256')
assert canonical(unhashed) == packet_hash == '56f8817eb6f0664b920cb98c0ef0b1ddc6b66d5185435b08316421aec19856a5'
binding = packet['publication_binding_sha256']
assert binding == 'bfe6a0010aa9d52b30f3725385f03dc310d2ce5d7293078ce4fdce14248fa720'
assert all(v is False for v in packet['anti_anchoring'].values())
assert ref(PROD)['raw_sha256'] == '31003aa5df1826329f8e57740860e9a0e7c1b866ab110108974e1a339a96bbca'
assert packet['candidate_publication_context']['current_lean_module'] == PROD.read_text(encoding='utf8')
expected = load(O / 'primary-first/expected-semantic-slots105.native.json')['semantic_slots']
decoder = load(DECODE / 'decoder-native/reconstruction.json')
drun = load(DECODE / 'decoder-native/decoder-run.json')
assert all(drun[k] is False for k in ['source_text_visible', 'source_identity_visible', 'theorem_number_visible', 'prior_audit_visible', 'repair_visible'])
assert ref(DECODE / 'input.json')['raw_sha256'] == drun['input_sha256']
for path, want in drun['output_hashes'].items():
    assert sha(Path(path).read_bytes()) == want
assert packet['blind_reconstruction']['text'] == (DECODE / 'decoder-native/reconstruction.txt').read_text(encoding='utf8')
assert packet['blind_reconstruction']['decoder_run_sha256'] == ref(DECODE / 'decoder-native/decoder-run.json')['raw_sha256']
unit = load(LESSON)['units'][0]
original_lesson = load(B / 'exposition-notation-repair105/lesson.before.exactraw.snapshot')
repair_dir = B / 'exposition-notation-repair105/independent-review'
repair = load(repair_dir / 'decision105.native.json')
assert repair['decision'] == 'ACCEPT_AUTHORED_NOTATION_CLARIFICATION_ONLY'
assert ref(repair_dir / 'decision105.native.json')['raw_sha256'] == '4c1a40cce8ecc96458dd319787561bb2234b2f38ced537a31b402a69e5f81a1a'
new_lesson = load(LESSON)
assert new_lesson['units'][0]['steps'][1]['text'] == repair['exact_new']
unrepair = copy.deepcopy(new_lesson)
unrepair['units'][0]['steps'][1]['text'] = repair['exact_old']
assert unrepair == original_lesson
assert unit['steps'][1]['formula'] == repair['unchanged_formula']
wm_path = B / 'independent-whole-math105/whole-math-decision105.native.json'
wm = load(wm_path)
kr_path = R / wm['fresh_kernel']['path']
kr = load(kr_path)
assert kr['terminal_closed'] and kr['exit_code'] == 0
for k in ['input', 'stdout', 'stderr', 'production']:
    assert ref(R / kr[k]['path'])['raw_sha256'] == kr[k]['raw_sha256']
assert (R / kr['input']['path']).read_bytes().startswith(PROD.read_bytes())
assert wm['kernel_contract']['target_module_not_imported'] and wm['kernel_contract']['literal_header_seal_privateProp_equal']
assert all(set(x['axioms']) == {'propext', 'Classical.choice', 'Quot.sound'} for x in wm['kernel_contract']['axioms'])
top_path = P / 'independent-header-math105/source-topology-admission105.native.json'
top = load(top_path)
assert top['reviewer'] != '/root/source_final96'
graph = top['effective_graph']
assert graph['node_count'] == 60 and graph['edge_count'] == 112
base_coverage_path = BASE / 'pbps-actual-normalized-endpoint104/final-source104/compiled-source-coverage104.native.json'
base_coverage = load(base_coverage_path)
source_coverage = load(S / 'source-coverage-delta105.native.json')
raw_source = PRIMARY.read_bytes()
assert sha(raw_source) == source_coverage['primary']['raw_sha256']
for r in source_coverage['regions']:
    assert sha(raw_source[r['byte_start']:r['byte_end_exclusive']]) == r['raw_sha256']
lines = PROD.read_bytes().splitlines(keepends=True)


def span(lo, hi):
    b = b''.join(lines[lo - 1:hi])
    return {'path': PROD.relative_to(R).as_posix(), 'line_start': lo, 'line_end': hi,
            'raw_sha256': sha(b), 'bytes': len(b), 'LF_text_sha256': sha(b.replace(b'\r\n', b'\n'))}


# Retain all inherited identities, but name new proof evidence separately.
clock = 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
selected = {
    'H99': ('unchanged-original-six-binders', [(21, 28), (159, 167)], 'No public proof-ingredient assumptions; parameterized actual producers receive the six binders unchanged.'),
    'D99': ('literal-actual-definitions', [(31, 153)], '34 actual93 definitions plus R,Vy,nu and B,sigma,L,M,Q,J. Global Z contract remains literal.'),
    'COUNT93': ('existing-public-projection-consumed', [(171, 175), (189, 199), (231, 253)], 'One global Z; joint Gamma/rho and fixed-state count law. No new arbitrary process or joint count premise.'),
    'MEASDENS93': ('existing-public-projection-consumed', [(194, 199)], 'Actual density joint measurability from same93 producer.'),
    'NORM': ('existing-public-normalization-consumed', [(176, 181)], 'Actual normalized phase probability transported to literal tilted-position times standard Gaussian.'),
    clock: ('existing-public-clock-law-consumed-twice', [(182, 188), (254, 257)], 'Clock probability gives Q probability and SFinite P for product Tonelli. The independently admitted extra ASSEMBLY105 edge is actually used.'),
    'SECTOR-INTEGRAL-MEAS105': ('new-internal-adapter', [(189, 230)], 'Joint B/rho, measurable strict simplex and SigmaFinite m imply measurable D_n via lintegral_prod_right\'.'),
    'ASSEMBLY105': ('new-internal-countable-assembly', [(223, 280)], 'Measurable Nat fibers partition each fixed-state clock space, then nonnegative Tonelli and lintegral_tsum identify Q=sum L. No infinity subtraction or uniform energy bound.'),
    'ENDPAIR104': ('existing-public-fixed-sector-reversal-consumed', [(281, 283)], 'Every n sector uses the same literal J and actual104 public theorem.'),
    'ENDPOINT-LAW105': ('new-public-bounded-law', [(171, 188), (223, 288)], 'Same actual Z, Q=sum L, probability Q and flipped-swap preservation. No later process theorem.'),
    'A795': ('existing-alternative-not-invoked', [], 'Actual95 fixed-initial signed path expansion remains available;105 directly uses93 nonnegative count-law projections instead. No invented95 proof edge.'),
    'AVG100': ('future-signed-averaging-boundary', [], 'Countable nonnegative endpoint assembly is supplied by105; signed bounded bilinear theorem remains a separate public obligation.'),
    'INV100': ('future-excluded', [], 'Actual marginal phase invariance is not a conclusion of105.'),
    'L2A3': ('future-excluded', [], 'L2 extension and associated semigroup/generator claims remain outside105.'),
    'RESTART': ('future-excluded', [], 'Restart/Markov/semigroup claims remain outside105.')
}
oldnodes = {n['id']: n for n in base_coverage['node_dispositions']}
nodes = []
for name in graph['nodes']:
    if name in selected:
        disposition, bounds, explanation = selected[name]
        nodes.append({'id': name, 'disposition': disposition, 'current_evidence': [span(*x) for x in bounds], 'explanation': explanation})
    else:
        assert name in oldnodes
        nodes.append({'id': name, 'disposition': 'unchanged-inherited-ingredient-via-actual-parents', 'inherited_node_record': oldnodes[name], 'inherited_compiled_coverage': ref(base_coverage_path), 'current_consuming_calls': [span(171, 173), span(176, 181), span(281, 283)], 'explanation': 'Preserve inherited source identity and exact previous spans. Reused through actual93/103/104 as appropriate; no new105 proof credit for the inherited lemma or implication.'})
node_lookup = {n['id']: n for n in nodes}
edges = []
for src, dst in graph['edges']:
    edges.append({'source': src, 'target': dst,
                  'disposition': 'future-consumer-only' if dst in ['AVG100', 'INV100', 'L2A3', 'RESTART'] else ('current-selected-proof-ingredient' if dst in ['COUNT93', 'SECTOR-INTEGRAL-MEAS105', 'ASSEMBLY105', 'ENDPOINT-LAW105'] else 'unchanged-inherited-source-incidence'),
                  'target_evidence': node_lookup[dst].get('current_evidence', []),
                  'not_a_new_kernel_edge_certificate': True})
assert len(nodes) == 60 and len(edges) == 112
source_regions = []
for item in source_coverage['regions']:
    row = dict(item)
    row['fresh_RAW_verified'] = True
    if item['id'] in ['standing-curvature', 'standing-eta']:
        row['compiled105_evidence'] = [span(21, 28), span(159, 167)]
    elif item['id'] in ['target-position-energy', 'phase-gibbs-law']:
        row['compiled105_evidence'] = [span(127, 131), span(176, 188)]
    elif item['id'] == 'A7':
        row['compiled105_evidence'] = [span(171, 175), span(231, 253)]
    elif item['id'] == 'average':
        row['compiled105_evidence'] = [span(223, 280)]
    elif item['id'] == 'weight-matching-and-invariance':
        row['compiled105_evidence'] = [span(254, 288)]
        row['remaining_subregions'] = '3216-3222 signed bounded bilinear identity;3224-3227 marginal invariance/L2 remain future, despite selected nonnegative assembly being proved.'
    elif item['id'] in ['actual-phase', 'event-convention', 'simplex', 'prescribed']:
        row['compiled105_evidence'] = [span(31, 126), span(171, 175), span(189, 253)]
    else:
        row['compiled105_evidence'] = []
        row['inherited_coverage'] = ref(base_coverage_path)
    source_regions.append(row)
module_regions = [(1, 19, 'imports, source attribution and environment'), (20, 153, 'full private literal proposition'), (154, 170, 'public signature and definition introduction'), (171, 175, 'single actual process'), (176, 188, 'actual phase/clock probabilities and endpoint measurability'), (189, 199, 'joint actual sector measurability'), (200, 222, 'strict simplex and sigma-finiteness'), (223, 230, 'measurable sector integrals'), (231, 253, 'fixed-state count partition'), (254, 280, 'initial Gibbs averaging and measure equality'), (281, 288, 'countable reversal'), (289, 292, 'axiom print and namespace closure')]
assert [i for lo, hi, _ in module_regions for i in range(lo, hi + 1)] == list(range(1, len(lines) + 1))
coverage = put('compiled-source-coverage105.native.json', {
    'kind': 'independently owned compiled source coverage105', 'reviewer': '/root/source_final96',
    'reviewer_packet_sha256': packet_hash, 'publication_binding_sha256': binding, 'production': ref(PROD),
    'source_primary': ref(PRIMARY), 'source_graph': ref(R / top['v2_graph']['path']), 'independent_noncreator_topology': ref(top_path),
    'topology_self_validation': False, 'effective_counts': {'nodes': 60, 'edges': 112, 'source_regions': 21, 'production_lines': 292, 'exposition_regions': 8, 'direct_public_parents': 4},
    'source_regions': source_regions, 'node_dispositions': nodes, 'edge_dispositions': edges,
    'all_production_regions': [dict(span(lo, hi), purpose=purpose) for lo, hi, purpose in module_regions],
    'whole_module': {'independently_owned': True, 'private_statement_reviewed': True, 'public_proof_reviewed': True, 'private_helpers': 'No separate private proof helpers; all local facts and43 literal definitions inspected.', 'literal_header_body_match': True},
    'actual_parent_discharge': [dict(declaration=x['declaration'], role=x['use']) for x in wm['genuine_direct_parents']],
    'proof_ingredient_vs_source_binder': 'Original six assumptions only. Actual93/103/104/clock and Mathlib supply measurability, probabilities, sigma-finiteness and exchange internally. No additional provider assumption.',
    'new_public_target': 'Actual normalized countable endpoint law is the countable sector sum, probability, and preserved by flipped swap.',
    'remaining_reds': ['AVG100 signed bilinear statement', 'INV100 marginal invariance', 'L2A3', 'RESTART/Markov/semigroup', 'cost/full-paper/composition', 'browser/merge/purification'],
    'fresh_kernel': ref(kr_path), 'whole_math': ref(wm_path), 'mathematical_review_use': 'Fresh exact kernel/axioms and producer discharge evidence only; own source verdict independently compares frozen source, current exact Lean and fresh decoder.'
})

step_judgments = [
    'Same global actual93 Z extracted once; all identification clauses returned before y,r,T. Source actual process is preserved.',
    'Exact normalized nu and unit-clock probability give Q probability. Correct measurable endpoint embedding. Repaired aliases H/pi_y/gamma now explicit and original text retained.',
    'Joint Gamma is evaluated at T and paired with initial state; actual rho includes terminal survival. Measurability is derived, not assumed.',
    'Strict simplex uses product coordinate inequalities; map-comap is restricted volume; SigmaFinite m follows, including n0 and empty simplexes.',
    'Arbitrary measurable ENNReal F gives jointly measurable F(B_n)*rho and measurable D_n. No signed or finite-integral condition.',
    'Nat-valued total selector gives fixed-state measurable, disjoint, exhaustive fibers; actual93 test law handles raw exceptional fallback measure. No joint count assumption.',
    'Tonelli over phase-first nu.prod P and nu.prod m, with clock probability supplying SFinite P, and lintegral_tsum yield exact sum of endpoint measures. ENNReal infinity allowed.',
    'Every sector is preserved by the same J; its measurable map commutes with countable Measure.sum. Reuses probability of actual Q, not fictitious sector mass one.'
]
step_records = []
for index, step in enumerate(unit['steps']):
    region = step['lean_source_region']
    raw = b''.join(lines[region['start_line'] - 1:region['end_line']])
    code = step['lean'].encode()
    assert raw.replace(b'\r\n', b'\n') == code
    assert sha(code) == region['exact_code_raw_sha256']
    assert region['source_raw_sha256'] == ref(PROD)['raw_sha256']
    runs = [len(m.group()) for m in re.finditer(r'\\+', step['formula'])]
    assert all(n == 1 for n in runs)
    step_records.append({'index': index + 1, 'title': step['title'], 'text': step['text'], 'formula': step['formula'], 'source_span': span(region['start_line'], region['end_line']), 'display_LF_RAW_sha256': sha(code), 'code_region_metadata_matches_display_LF_string': True, 'literal_backslash_run_lengths': runs, 'judgment': step_judgments[index], 'accepted': True})
exposition = put('exposition105.native.json', {
    'verdict': 'ACCEPT_BOUNDED_EIGHT_STEP_EXPOSITION_ONLY', 'reviewer': '/root/source_final96',
    'reviewer_packet_sha256': packet_hash, 'publication_binding_sha256': binding,
    'production': ref(PROD), 'lesson': ref(LESSON), 'publication': ref(PUB), 'steps': step_records,
    'statement_review': 'Complete authored statement includes all six source assumptions, actual34 algorithm definitions plus phase/endpoint laws, existential global process contract, probability and countable sum/reversal. Definitions are not hypotheses. Rank0/n0/T0 and raw exceptional conventions retained.',
    'notation': 'Mathematical event coordinates are consistently one-based in exposition; Lean Fin coordinates use the exact displayed code. No reversed-index formula appears. Decoded formula commands have literal single backslashes; statement paragraph separators are real newlines.',
    'exact_code_hash_convention': 'source_span.raw_sha256 hashes original physical source bytes. display_LF_RAW_sha256 hashes UTF8 step.lean; these differ only by CRLF-to-LF conversion when present. The extra exact_code_raw_sha256 metadata denotes the displayed LF string.',
    'retained_initial_finding': ref(O / 'initial-exposition-finding105.native.json'),
    'separately_reviewed_notation_repair': [ref(B / 'exposition-notation-repair105/proposal105.json'), ref(repair_dir / 'decision105.native.json'), ref(repair_dir / 'closed-RAW105.native.json'), ref(B / 'exposition-notation-repair105/applied105.json')],
    'repair_transfer_exact': 'Undoing the single accepted step2 prefix produces the original lesson JSON exactly. Source theorem, formulas, code and decoder unchanged. No source-theorem repair.',
    'full_Exposition_Seal': False, 'actual_browser_page_viewed': False, 'interactive_reader_acceptance': False,
    'scope': 'Authored eight-step local mathematical explanation and adjacent exact source regions only; no generated-site/live-browser/merge/purification or full-paper credit.'
})

evidence = {
    'objects': 'Private Prop20-153 matches exact header body; current decoder reconstructs all43 definitions including totalized clock/process conventions. Source A7 actual Gamma/rho and Eq3.1 initial law retained.',
    'domains': 'E finite-dimensional real Borel, rank0; phase-first products and strict Prefix comap exact. All horizons NNReal including0, count allNat, and source nonpositive raw clocks are explicit ambient totalization only.',
    'quantifiers': 'Same global exists Z is extracted171-175 before forall y,r,T. Pointwise arc/fallback and parameterwise P-a.e. initialization retained; decoder correctly avoids one common null set or all-clock zero-time claim.',
    'assumptions': 'Exactly original six binders21-28/159-167. All four genuine public producers discharge probability, measurability, sigma-finiteness and fixed-sector preservation internally. No joint count, finite test integral or uniform energy bound.',
    'conclusion': 'Q actual endpoint pushforward equals countable Measure.sum L, is probability and satisfies J_*Q=Q. Current decoder matches this triple and same actual Z; no sector mass-one assertion. Proof223-288 realizes source nonnegative averaging.',
    'scopes': 'A7 and initial averaging/positive Tonelli slice3210-3215 are completed at endpoint-law level. Signed duality3216-3222, marginal invariance3224-3227, L2/restart/Markov/cost remain excluded in Lean, decoder and prose.',
    'constant_dependencies': 'Exact sqrteta flow/rate, factor2 reflection, rate1 clocks, coefficient1/(2eta), standard Gaussian and uncapped count sum. alpha/beta constrain V/eta without new bounds on y,r,z,T.'
}
slots = {k: {'original': expected[k], 'reconstructed': decoder[k], 'relation': 'explicit-elaboration' if k in ['objects', 'domains', 'scopes'] else 'equivalent', 'evidence': evidence[k]} for k in expected}
deltas = [
    {'slot': 'domains', 'severity': 'informational', 'description': 'Finite-dimensional Hilbert and totalized raw-clock/path conventions elaborate the Euclidean source calculation, including rank zero and exceptional inputs.', 'source': 'Pinned standing hypotheses and AppendixA1 actual-path/count construction.', 'lean': 'Literal actual93 recursion, stopped records, toNNReal, fallback and strict-comap definitions retained.', 'evidence': 'Actual clock probability law and exact process contract preserve source almost-sure dynamics; no source binder strengthened.', 'blocking': False},
    {'slot': 'conclusion', 'severity': 'informational', 'description': 'Nonnegative averaging is packaged as equality of actual endpoint measures, plus probability and flipped-swap preservation of that same law.', 'source': 'A7, initial Gibbs averaging3171-3175 and nonnegative Tonelli3210-3215.', 'lean': 'Q=Measure.sum L, IsProbabilityMeasure Q and MeasurePreserving J Q Q.', 'evidence': 'Measurable ENNReal tests and countable Tonelli prove measure equality; probability uses actual103 and actual clock law, not fixed-sector104 alone.', 'blocking': False},
    {'slot': 'scopes', 'severity': 'informational', 'description': 'The selected source slice ends before signed bilinear duality and marginal invariance.', 'source': 'Later3216-3227 source conclusions remain separate.', 'lean': 'No full-path, Markov/semigroup, signed duality, marginal invariance, convergence or cost conclusion.', 'evidence': 'Current public triple, blind reconstruction and all eight authored steps agree on this boundary.', 'blocking': False}
]
run = put('source-review-run105.native.json', {
    'kind': 'native independent primary-first final source review', 'reviewer': '/root/source_final96',
    'reviewer_packet': ref(B / 'reviewer-packet105.json'), 'reviewer_packet_sha256': packet_hash, 'publication_binding_sha256': binding,
    'primary_first': ref(O / 'primary-first/primary-first-reconstruction105.native.json'),
    'expected_slots_frozen_before_current_Lean_prose_decoder': ref(O / 'primary-first/expected-semantic-slots105.native.json'),
    'production': ref(PROD), 'decoder_run': ref(DECODE / 'decoder-native/decoder-run.json'),
    'blind_reconstruction': [ref(DECODE / 'decoder-native/reconstruction.txt'), ref(DECODE / 'decoder-native/reconstruction.json')],
    'compiled_coverage': coverage, 'bounded_exposition': exposition,
    'read_order': 'Fixed primary and frozen source-only expectations first; current exact proof/prose then fresh canonical anti-anchored packet and anonymous decoder. Separate accepted notation overlay verified exactly.',
    'independence': 'Different from root formalizer and blind_decoder105. Prior header/source graph authorship explicitly known; separate graph topology acceptance reused, never self-validated. No earlier final semantic slots/verdict/deltas used as decision inputs.',
    'whole_math_evidence_only': ref(wm_path), 'fresh_kernel': ref(kr_path), 'new_Lean_run': False, 'shared_writes': False
})
source_review = {
    'state': 'accepted', 'reviewer': '/root/source_final96', 'independent_from_formalizer': True, 'independent_from_decoder': True,
    'reviewer_packet_sha256': packet_hash, 'review_run_sha256': run['raw_sha256'], 'publication_binding_sha256': binding, 'run_artifact': run['path'],
    'evidence': 'Primary-first frozen slots independently compared with actual compiled whole module, current source-facing restatement and fresh anonymous decoder. All21 source regions,60 nodes112 edges,292 physical lines,43 literal lets, four public producers and eight exact exposition regions accounted. Original six assumptions only. One notation-only prefix independently reviewed and transferred; source theorem repairs empty. Browser/site/merge/purification remain separate.',
    'source_primary_read': True, 'source_primary_read_before_current_Lean_and_decoder': True,
    'current_full_Lean_module_read': True, 'candidate_exposition_read': True, 'blind_reconstruction_read': True,
    'prior_semantic_slots_read': False, 'prior_deltas_read': False, 'prior_verdict_read': False, 'prior_source_theorem_repairs_read': False,
    'prior_header_involvement_disclosed': True, 'source_graph_creator': True, 'topology_self_validation': False,
    'independently_owned_whole_module_review': True, 'private_helpers_reviewed': True, 'exposition_reviewed': True,
    'compiled_source_coverage': coverage, 'bounded_exposition': exposition, 'full_Exposition_Seal': False
}
decision = put('source-review105.native.json', {
    'semantic_slots': slots, 'deltas': deltas, 'verdict': 'equivalent-after-elaboration', 'repairs': [],
    'source_review': source_review, 'reviewer_packet_sha256': packet_hash, 'publication_binding_sha256': binding, 'review_run_sha256': run['raw_sha256'],
    'reviewer': '/root/source_final96', 'independent_from_formalizer': True, 'independent_from_decoder': True,
    'review_evidence': source_review['evidence'], 'VERIFIED_transition': False
})
inputs = [PRIMARY, PROD, LESSON, PUB, B / 'reviewer-packet105.json', P / 'Header105.lean', P / 'root.statement-seal105.json', wm_path, kr_path, top_path, base_coverage_path,
          DECODE / 'input.json', DECODE / 'decoder-native/decoder-run.json', DECODE / 'decoder-native/reconstruction.txt', DECODE / 'decoder-native/reconstruction.json',
          B / 'exposition-notation-repair105/lesson.before.exactraw.snapshot', B / 'exposition-notation-repair105/proposal105.json', B / 'exposition-notation-repair105/applied105.json',
          repair_dir / 'decision105.native.json', repair_dir / 'run105.native.json', repair_dir / 'closed-RAW105.native.json',
          S / 'source-coverage-delta105.native.json', S / 'expected-semantic-slots105.native.json', S / 'literal-definition-context105.native.json', S / 'retrieval105.native.json']
inputs += [R / kr[k]['path'] for k in ['input', 'stdout', 'stderr']]
inputs += [R / top[k]['path'] for k in ['v2_graph', 'coverage_overlay', 'proposal', 'creator_repair_closure']]
inputs += [R / 'AutoSamplingTheory/ExampleCases/ProximalBPS' / f for f in ['ActualFiniteCountPath.lean', 'ActualPhaseNormalization.lean', 'ActualNormalizedEndpointSector.lean']]
inputs += [R / 'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
originals = [p for p in sorted(O.rglob('*')) if p.is_file() and not p.name.endswith('.gz')]
archives = []
for p in originals:
    q = Path(str(p) + '.raw.gz')
    assert not q.exists()
    q.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
    assert gzip.decompress(q.read_bytes()) == p.read_bytes()
    archives.append({'original': ref(p), 'archive': ref(q), 'lossless': True})
closure = put('closed-RAW-final-source105.native.json', {
    'kind': 'immutable native final source/exposition RAW closure', 'reviewer': '/root/source_final96', 'decision': decision,
    'selected_inputs': [ref(p) for p in sorted(set(inputs))], 'owned_artifacts': [ref(p) for p in sorted(O.rglob('*')) if p.is_file()],
    'original_RAW_archives': archives, 'self_hash_intentionally_omitted': True, 'primary_full_snapshot_not_copied': True,
    'reviewer_packet_sha256': packet_hash, 'publication_binding_sha256': binding, 'no_shared_mutations': True
})
print(json.dumps({'decision': decision, 'coverage': coverage, 'exposition': exposition, 'run': run, 'closure': closure}, indent=2))
