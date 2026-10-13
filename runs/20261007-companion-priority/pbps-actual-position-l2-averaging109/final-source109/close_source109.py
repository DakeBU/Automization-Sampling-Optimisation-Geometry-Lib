import copy
import gzip
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
RUN = OUT.parent
PRE = ROOT / 'runs/20261007-companion-priority/pbps-actual-position-l2-preread109'
SRC = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-flip-duality108/next-primary109'
inputs = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def bind(p):
    b = p.read_bytes()
    obj = {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}
    inputs[obj['path']] = obj
    return obj


def read(p):
    bind(p)
    return json.loads(p.read_text(encoding='utf-8'))


def emit(name, value):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    return bind(p)


frozen = read(OUT / 'primary-first109.native.json')
primary_path = ROOT / frozen['primary']['path']
assert bind(primary_path) == frozen['primary']
primary_raw = primary_path.read_bytes()
for r in frozen['regions']:
    assert sha(primary_raw[r['byte_start']:r['byte_end_exclusive']]) == r['raw_sha256']
packet_path = RUN / 'reviewer109.input.json'
packet = read(packet_path)
packet_canonical = sha(json.dumps({k: v for k, v in packet.items() if k != 'packet_sha256'}, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))
assert packet_canonical == packet['packet_sha256'] == '6a236c1c44d59540c93f3ec79987c926f42e3d4d81d9bb9d29df77967a850b29'
assert all(v is False for v in packet['anti_anchoring'].values())
binding = packet['publication_binding_sha256']
assert binding == 'b6a33bb707739b8d84bcf58ba8e78a227b0a053ee46527c61f63215d121ce3f6'
production_path = ROOT / packet['lean']['file']
production = bind(production_path)
assert production['raw_sha256'] == '21c6b4e95b729b41f555eecf6a42185ab2f63bff7bcab3f6dc2ab82da171e85e'
raw = production_path.read_bytes()
lines = raw.splitlines(keepends=True)
text = raw.decode('utf-8')
assert len(lines) == 349
header = bind(PRE / 'Header109.lean')
assert lines[12:196] == (PRE / 'Header109.lean').read_bytes().splitlines(keepends=True)[12:196]
assert packet['candidate_publication_context']['current_lean_module'] == text
assert len(re.findall(r'^\s*let ', ''.join(x.decode('utf-8') for x in lines[12:196]), re.M)) == 47
algorithm = text[text.index('    let c :'):text.index('    ∃ Z :')]
assert len(re.findall(r'^    let ', algorithm, re.M)) == 37
producer_path = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2FlipDuality.lean'
producer = bind(producer_path)
producer_text = producer_path.read_text(encoding='utf-8')
assert algorithm == producer_text[producer_text.index('    let c :'):producer_text.index('    ∃ Z :')]
assert text.count('ActualL2FlipDuality.actual_l2_flip_duality') == 1
lesson_path = ROOT / 'website/content/declaration_lessons/pbps-actual-position-l2-averaging.json'
publication_path = ROOT / 'website/content/publications/pbps-actual-position-l2-averaging.json'
lesson = read(lesson_path)['units'][0]
publication = read(publication_path)['items'][0]
for k, v in packet['candidate_publication_context']['lesson'].items():
    assert lesson[k] == v, k
assert lesson['statement'].count('\n') == 21 and lesson['statement'].count('\\n') == 0
graph_path = RUN / 'route-adapter109/source-proof-graph109.route-adapted.proposal.json'
graph = read(graph_path)
assert len(graph['nodes']) == 123 and len(graph['edges']) == 247
admission_path = RUN / 'independent-route-adapter109/admission109.native.json'
admission = read(admission_path)
assert admission['decision'] == 'ACCEPT_EXACT_ROUTE_ADAPTER109_PROPOSAL'
assert admission['graph_RAW_sha256'] == bind(graph_path)['raw_sha256']
bind(RUN / 'independent-route-adapter109/closed-RAW-admission109.native.json') if (RUN / 'independent-route-adapter109/closed-RAW-admission109.native.json').exists() else None
for name in ['route-adapter-proposal109.native.json', 'pinned-api-adapter109.native.json', 'closed-RAW-route-adapter109.native.json']:
    bind(RUN / 'route-adapter109' / name)
original_graph = read(SRC / 'source-proof-graph-delta109.native.json')
bind(SRC / 'source-coverage109.native.json')
bind(SRC / 'primary-first109.native.json')
bind(PRE / 'root.statement-seal109.json')
whole_path = RUN / 'independent-whole-math109/whole-math-decision109.native.json'
whole = read(whole_path)
assert whole['production'] == production and whole['kernel_contract']['no_sorryAx']
for name in ['closed-RAW-manifest109.native.json', 'fresh-kernel-receipt109.native.json', 'FreshExactProductionAndHeader109.lean', 'fresh-kernel.stdout.log', 'fake-closure-scan109.native.json']:
    bind(RUN / 'independent-whole-math109' / name)
bind(RUN / 'focused109/full3/receipt.json')
anonymous = ROOT / 'runs/semantic-roundtrip/anonymous109'
decoder = read(anonymous / 'decoder-native/decoder.json')
decoder_manifest = read(anonymous / 'decoder-native/manifest.json')
bind(anonymous / 'input.json')
reconstruction = bind(anonymous / 'decoder-native/reconstructed-theorem.txt')
assert packet['blind_reconstruction']['text'] == decoder['reconstructed_theorem']
assert sha(packet['blind_reconstruction']['text'].encode('utf-8')) == reconstruction['raw_sha256']
assert all(decoder_manifest[k] is False for k in ['source_text_visible', 'source_identity_visible', 'source_anchor_visible', 'prior_audits_visible', 'repairs_visible'])
assert decoder_manifest['input']['raw_sha256'] == bind(anonymous / 'input.json')['raw_sha256']
for a in decoder_manifest['outputs']:
    p = Path(a['path'])
    assert bind(p)['raw_sha256'] == a['sha256']
inherited_coverage_path = SRC.parent / 'final-source108/compiled-source-coverage108.native.json'
inherited_coverage = read(inherited_coverage_path)


def span(a, b):
    original = b''.join(lines[a - 1:b])
    displayed = original.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
    return {'line_start': a, 'line_end': b, 'source_span_RAW_sha256': sha(original), 'displayed_LF_UTF8_sha256': sha(displayed.encode('utf-8'))}


region_specs = [
    (1, 12, 'Imports, namespace and private proposition scaffolding; UnitExponentialProduct import is not a producer invocation.'),
    (13, 20, 'Ambient structure and all six exact original source hypotheses.'),
    (21, 123, 'Literal actual37 algorithm/clock/path/phase definitions, byte-equivalent to108.'),
    (124, 170, 'Global Z and all108 contracts, same A and canonical J, fixed-time realL2 flip identity.'),
    (171, 196, 'New actual position law, canonical B/M, Gaussian identity, same-A compression and actual nested expectation.'),
    (197, 212, 'Public theorem exact same six binders, options and unfolding; no helper assumptions introduced.'),
    (213, 222, 'Exactly one108 invocation; retain global Z, same L/A,hR,J and every inherited output.'),
    (223, 235, 'Internal projection preservation; canonical lift representative, B/M norm bounds and MB=id.'),
    (236, 244, 'Universal Gaussian average obligation; derive G L1, gbar L1 and M[G] L1 independently.'),
    (245, 279, 'Indicator-set uniqueness argument using selected L1-indicator restriction, adjoint pairing and signed Fubini.'),
    (280, 284, 'Transport L2 only after AE equality; return Gaussian sections and exact quotient identity.'),
    (285, 306, 'AE flip transport gives JB=B; J*=J by inner products; taking adjoints gives MJ=M.'),
    (307, 332, 'Kpos0=id, adjoint compression and exact contraction1.'),
    (333, 345, 'Lift raw f; same-A expectation; Gaussian averaging and correctly qualified product-AE slicing; no integral-order exchange.'),
    (346, 349, 'Axiom print and namespace closure; no additional mathematical declaration.')]
module_regions = [{**span(a, b), 'disposition': why} for a, b, why in region_specs]
assert [i for a, b, _ in region_specs for i in range(a, b + 1)] == list(range(1, 350))
new_mapping = {
    'MOMENTUM-LIFT109': [(223, 235)], 'MOMENTUM-L1-FUBINI109': [(240, 244), (253, 259), (271, 279)],
    'MOMENTUM-IDENTIFY109': [(245, 284)], 'FLIP-ABSORB109': [(285, 306)],
    'POSITION-OP109': [(307, 332)], 'POSITION-REP109': [(333, 345)], 'POSITION-AVG109': [(223, 345)]}
api_mapping = {
    'MeasureTheory.measurePreserving_fst': [(223, 224)], 'MeasureTheory.Lp.compMeasurePreservingₗᵢ': [(173, 175), (223, 225)],
    'MeasureTheory.Lp.coeFn_compMeasurePreserving': [(226, 228)], 'LinearIsometry.norm_toContinuousLinearMap_le': [(229, 229)],
    'ContinuousLinearMap.adjoint': [(175, 175), (230, 233), (305, 306)], 'LinearIsometry.adjoint_comp_self': [(234, 235)],
    'MeasureTheory.MemLp.integrable': [(240, 244)], 'MeasureTheory.Integrable.integral_prod_left': [(241, 242)],
    'MeasureTheory.Integrable.prod_right_ae': [(282, 282)], 'MeasureTheory.Integrable.ae_eq_of_forall_setIntegral_eq': [(245, 248)],
    'MeasureTheory.indicatorConstLp': [(249, 249)], 'MeasureTheory.indicatorConstLp_coeFn': [(250, 251)],
    'MeasureTheory.Integrable.indicator': [(253, 259)], 'ContinuousLinearMap.adjoint_inner_right': [(261, 263)],
    'MeasureTheory.L2.inner_def': [(264, 270)], 'MeasureTheory.integral_prod': [(271, 271)],
    'MeasureTheory.MemLp.coeFn_toLp': [(267, 270), (284, 284), (336, 339)], 'MeasureTheory.MemLp.ae_eq': [(280, 281)],
    'MeasureTheory.Lp.ext': [(283, 284), (286, 291), (337, 339)], 'ContinuousLinearMap.adjoint_inner_left': [(292, 301)],
    'LinearIsometry.inner_map_map': [(300, 301)], 'ContinuousLinearMap.adjoint_comp': [(304, 306), (314, 317)],
    'ContinuousLinearMap.adjoint_adjoint': [(317, 317)], 'ContinuousLinearMap.opNorm_comp_le': [(323, 332)],
    'MeasureTheory.MemLp.comp_measurePreserving': [(334, 335)], 'MeasureTheory.Measure.ae_ae_of_ae_prod': [(340, 342)]}
projection_mapping = {'L2A3': [(218, 221), (317, 322)], 'FLIP-L2-108': [(218, 221), (285, 301)], 'PHASE-FLIP106': [(218, 221), (287, 291)], 'L2-LIFT107': [(218, 219), (310, 332)], 'L2-IDENTIFY107': [(218, 219), (340, 345)], 'AE-REP107': [(336, 345)]}
node_coverage = []
for n in graph['nodes']:
    ident = n['id']
    if ident in new_mapping:
        disposition = 'current109 selected obligation discharged by explicit local proof'
        spans = new_mapping[ident]
    elif ident in api_mapping:
        disposition = 'exact current109 API realization; not an extra source binder'
        spans = api_mapping[ident]
    elif ident in projection_mapping:
        disposition = 'inherited output of the SAME single108 invocation, consumed here; no separate producer call'
        spans = projection_mapping[ident]
    elif ident in ['MeasureTheory.isZeroOrProbabilityMeasure_tilted', 'ProbabilityTheory.isProbabilityMeasure_stdGaussian']:
        disposition = 'pinned typeclass instances for literal tilted/standard Gaussian laws provide finite/SFinite/probability requirements internally'
        spans = [(171, 175), (223, 244)]
    elif ident == 'MeasureTheory.L2.integrable_inner':
        disposition = 'inherited108 ancestry and retained unselected109 alternative only; NOT a direct109 invocation or selected L1-indicator premise'
        spans = [(253, 259)]
    else:
        disposition = 'unchanged inherited/future source/API ancestry; no fresh109 proof credit or direct-call claim; exact prior compiled coverage retained'
        spans = [(213, 221)]
    node_coverage.append({'id': ident, 'disposition': disposition, 'regions': [span(a, b) for a, b in spans], 'inherited_coverage': bind(inherited_coverage_path) if ident not in new_mapping else None})
node_by_id = {n['id']: n for n in node_coverage}
edge_coverage = []
for e in graph['edges']:
    if e.get('route_membership') == 'unselected-L2-inner-alternative-only':
        disposition = 'preserved alternative-only edge; independently admitted conditional AND excludes it from selected route'
    elif e['target'] in new_mapping:
        disposition = 'selected109 dependency; consumed within exact target proof spans'
    else:
        disposition = 'unchanged inherited/future graph edge, no new109 direct-call or completion credit'
    edge_coverage.append({'source': e['source'], 'target': e['target'], 'disposition': disposition, 'source_disposition': node_by_id[e['source']]['disposition'], 'target_regions': node_by_id[e['target']]['regions']})
regions = []
for r in frozen['regions']:
    r = copy.deepcopy(r)
    if r['id'] == 'gaussian-momentum-averaging':
        r['compiled_disposition'] = 'Selected actual Gaussian-average identification and self-adjoint contraction discharged223–345; Markov positivity/constants explicitly excluded.'
    elif r['id'] in ['strong-continuity-after-A3', 'averaged-halfturn-consumer']:
        r['compiled_disposition'] = 'Future independent boundary/consumer only; not proved by109.'
    elif r['id'] in ['standing-curvature', 'standing-eta']:
        r['compiled_disposition'] = 'Six literal source hypotheses13–20 and202–209; no additional analytic premises.'
    elif r['id'] in ['target-position-energy', 'phase-gibbs-law']:
        r['compiled_disposition'] = 'Actual Vy/nu119–123 and mu171; canonical position-first Gaussian averaging223–284.'
    elif r['id'] == 'source-license':
        r['compiled_disposition'] = 'Attribution/source license retained; no full primary archive made.'
    else:
        r['compiled_disposition'] = 'Unchanged inherited source boundary via one108 producer213–221 and all literal/global contracts23–170. No new109 completion credit.'
    regions.append(r)
coverage = emit('compiled-source-coverage109.native.json', {
    'kind': 'independent compiled source correspondence109', 'reviewer': '/root/source_final96',
    'production': production, 'header': header, 'primary': frozen['primary'], 'regions': regions,
    'all24regions_rehashed': True, 'all21_inherited_regions_retained': True, 'module_regions': module_regions, 'all349lines_disposed': True,
    'private_literalProp_lines': [12, 196], 'literal_sealed_body_exact_match': True,
    'statement_let_count': 47, 'algorithm_let_count': 37, 'source_binder_count': 6,
    'genuine_direct_producers': [{'declaration': 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality.actual_l2_flip_duality', 'source': producer, 'span': span(213, 215), 'count': 1}],
    'effective_graph': bind(graph_path), 'independent_topology_admission': bind(admission_path),
    'node_coverage': node_coverage, 'edge_coverage': edge_coverage, 'counts': {'nodes': 123, 'edges': 247, 'source_regions': 24, 'module_lines': 349},
    'selected_AND_OR': graph['conditional_route_groups109'],
    'actual_equivalent_API_realizations': ['Indicator pairing uses L2.inner_indicatorConstLp_one262, within the admitted indicator/L2 pairing obligation.', 'Selected indicator integrability is hprod.indicator259 after hG.integrable240; no direct L2.integrable_inner call.', 'Product-AE slicing is MeasureTheory.Measure.ae_ae_of_ae_prod342; historical short namespace is corrected by external admission.', 'J self-adjointness uses ext_inner_right295, adjoint_inner_left297, inner_map_map300 and inherited involution301.'],
    'source_creator_does_not_self_admit_topology': True, 'whole_mathematics_evidence': bind(whole_path),
    'no_exposition_or_browser_acceptance_in_this_coverage': True})

step_judgments = [
    'One actual108 invocation and scope-preserving extraction correspond exactly to retained Z/A/J; no separately chosen witness.',
    'Actual projection/pullback and adjoint norm/left-inverse calculations establish the claimed canonical B/M.',
    'hprod, hbar1 and hMg establish the L1 basis without circularity. Gaussian section integrability follows from hprod and is returned explicitly in step5 at282.',
    'Exact selected L1 restriction route proves H integrable before signed Fubini; all indicator and raw representative changes are AE.',
    'Existing heq transports L2 membership and Lp.ext yields the Gaussian quotient identity; sections are returned from hprod.prod_right_ae.',
    'AE flip transport, isometry/involution and adjoint identity prove both absorption equations.',
    'Same A0 and MB establish K0; adjoint composition and both absorption facts give symmetry, while norm multiplication yields1.',
    'Lifted f, inherited same-A expectation and universal havg yield literal Gaussian-outer clock-inner representative, with nested section integrability; no order exchange.'
]
step_records = []
for i, s in enumerate(lesson['steps']):
    reg = s['lean_source_region']
    a, b = reg['start_line'], reg['end_line']
    code = b''.join(lines[a - 1:b]).decode('utf-8').replace('\r\n', '\n')
    assert code == s['lean']
    assert sha(s['lean'].encode('utf-8')) == reg['exact_code_raw_sha256']
    assert reg['source_raw_sha256'] == production['raw_sha256']
    backslashes = [len(m.group()) for m in re.finditer(r'\\+', s['formula'])]
    assert all(n == 1 for n in backslashes)
    step_records.append({'step': i + 1, 'title': s['title'], 'formula': s['formula'], 'prose': s['text'], 'region': span(a, b), 'displayed_code_raw_sha256': sha(s['lean'].encode('utf-8')), 'literal_TeX_backslash_run_lengths': backslashes, 'judgment': 'accepted', 'evidence': step_judgments[i]})
assert len(step_records) == 8
assert [j for s in step_records for j in range(s['region']['line_start'], s['region']['line_end'] + 1)] == list(range(213, 346))
exposition = emit('exposition109.native.json', {
    'kind': 'bounded authored statement and adjacent formula proof exposition review', 'reviewer': '/root/source_final96',
    'verdict': 'ACCEPT_AUTHORED_EIGHT_STEP_EXPOSITION_ONLY', 'publication_binding_sha256': binding,
    'lesson': bind(lesson_path), 'publication': bind(publication_path), 'production': production,
    'full_statement': {'complete_source_conditions': True, 'all37_actual_literals': True, 'same_globalZ_and_all108_outputs': True, 'new_mu_B_M_K_and_nested_integrability': True, 'parameterwise_AE': True, 'real_newlines': 21, 'literal_backslash_n_count': 0, 'attribution': lesson['sources']},
    'steps': step_records, 'exact_contiguous_proof_coverage': [213, 345],
    'definition_notation': 'Statement uses conventional one-based event tuple t1..tn with s0=0; Lean Fin n coordinates are zero-based and shifted by Fin.cons. Both define the same ordered gaps and z_i recursion. New proof formulae do not use event indices. mu/pi_y denote the identical tilted law; Kpos/K_T denote position compression, distinct from history K.',
    'formula_run_check': 'All decoded TeX command backslash runs have length1; JSON transport escapes are not treated as extra literal slashes.',
    'code_storage': {'production_line_endings': 'LF', 'normalization': 'displayed UTF8/LF text equals exact source-span bytes for every region; both hashes recorded'},
    'private_statement_and_public_proof': 'Full private literal Prop12–196 and public theorem201–345 separately inspected. Helper label references the actual private statement; no missing mathematical helper or assumed provider.',
    'adjacent_fold_contract': 'Eight exact Lean blocks are attached to their eight formula explanations; complete literal helper statement remains a separate folded reader block. Potential initially-folded/generated reader behavior requires later site checks; no rendered/browser verification is claimed here.',
    'browser_acceptance': False, 'generated_reader_acceptance': False, 'fullExpositionSeal': False,
    'boundary': lesson['boundary'], 'repairs_required': []})

evidence_text = 'Primary-first frozen expectations and all24 raw slices compared independently with fresh anonymous109 reconstruction, literal private Prop/public theorem, whole349-line module and all eight exact adjacent explanation regions. Same108 Z/A/J retained, actual Gaussian adjoint representative and nested section integrability checked. Accepted external route adapter supplies corrected MeasureTheory.Measure API and selected L1-indicator route; no absent L2.inner integrability call asserted. Source-boundary judgment is independent of whole-math kernel acceptance.'
run = emit('reviewer-run109.native.json', {
    'kind': 'independent anti-anchored final source/exposition review109', 'reviewer': '/root/source_final96',
    'independent_from_formalizer': True, 'independent_from_decoder': True,
    'prior_involvement': frozen['prior_involvement'], 'primary_first': bind(OUT / 'primary-first109.native.json'),
    'read_original_source': True, 'read_current_lean_module': True, 'read_candidate_exposition': True, 'read_fresh_blind_reconstruction': True,
    'prior_semantic_verdict_slots_deltas_repairs_used': False, 'source_graph_self_admitted': False,
    'reviewer_packet': bind(packet_path), 'reviewer_packet_sha256': packet_canonical, 'publication_binding_sha256': binding,
    'native_decoder': bind(anonymous / 'decoder-native/decoder.json'), 'native_decoder_manifest': bind(anonymous / 'decoder-native/manifest.json'),
    'decoder_identity': decoder['decoder'], 'decoder_originals_unchanged': True,
    'decoder_hash_conventions': 'Native decoder manifest/input/output RAWs preserved; canonical decoder_run_sha256 is adapter metadata and is not misreported as native manifest RAW.',
    'compiled_coverage': coverage, 'exposition': exposition, 'whole_math_kernel_evidence_only': bind(whole_path),
    'source_evidence': evidence_text, 'blocking_findings': [],
    'owned_scope': 'final-source109 only; no canonical/production/header/source-graph changes; no new primary archive'})
slot_comments = {
    'objects': ('same', 'Literal actual process/clock/phase constructions and canonical position lift B, adjoint M, compression Kpos match. Decoder retains actual definitions and separate history/operator A identities.'),
    'domains': ('explicit-elaboration', 'Finite real Hilbert Borel E includes rank0; phase/position realL2 quotient spaces and arbitrary MemLp representatives match. Canonical volume/Gaussian give the Euclidean source model up to isometric coordinates.'),
    'quantifiers': ('same', 'One global Z before every parameter; same A under y,r before all T and observables; same hR/J then canonical B/M. Existential integrability witnesses are conclusions. AE statements retain each measure and nesting.'),
    'assumptions': ('same', 'Six original analytic binders exact; all probability/finite-measure, Gaussian section L1, quotient and adjoint facts are discharged internally. Measurable/bounded/MemLp conditions classify universally tested observables.'),
    'conclusion': ('explicit-elaboration', 'Complete Gaussian L2 representative and both nested integrability levels make source averaging precise. B/M contraction and MB=id, flip absorption, Kpos0/self-adjoint contraction and literal same-process expectation all match decoder and compiled declaration.'),
    'scopes': ('same', 'Only bounded fixed-reference realL2 averaging/self-adjoint contraction of A.1(iii) is selected. Full Markov, continuity, semigroup, independent-reference A2 and costs remain excluded explicitly.'),
    'constant_dependencies': ('same', 'Exact eta energy factor2, sqrteta flow/rate, unit-rate clocks, probability stdGaussian and norm bound1 retained. Gaussian outer/clock inner order unchanged; no Gaussian density factor or new normalizer.')}
slots = {k: {'original': frozen['expected_semantic_slots'][k], 'reconstructed': msg, 'relation': rel, 'evidence': f'{evidence_text} Coverage: {coverage["path"]}; exposition: {exposition["path"]}.'} for k, (rel, msg) in slot_comments.items()}
deltas = [
    {'slot': 'domains', 'severity': 'informational', 'description': 'Euclidean source is expressed in a finite real Hilbert Borel space, including rank0.', 'source': 'Euclidean phase and Gaussian momentum law.', 'lean': 'Canonical finite real Hilbert volume/stdGaussian with no nontriviality binder.', 'evidence': 'Exact source hypotheses and literal phase/position laws13–20,119–123,171; same constants and dimensions.', 'blocking': False},
    {'slot': 'conclusion', 'severity': 'informational', 'description': 'The Gaussian averaging argument receives explicit L1/AE/L2 representative and same-process nested-integral obligations.', 'source': 'A.1 final averaging uses Pi_p and its adjoint without detailing representative construction.', 'lean': 'havg and same-A nested expectation prove these internally, with the selected finite-L1 indicator route.', 'evidence': 'Production236–284 and333–345; independently admitted123/247 route adapter; no extra source binder.', 'blocking': False},
    {'slot': 'scopes', 'severity': 'informational', 'description': 'Bounded source slice excludes the source proposition Markov clauses and later process/sampler properties.', 'source': 'A.1(iii) also asserts Markovness; A.2 averages references.', 'lean': 'Actual fixed-reference self-adjoint contraction/expectation only, with explicit remaining boundaries.', 'evidence': lesson['boundary'], 'blocking': False}]
source_review = {
    'state': 'accepted', 'reviewer': '/root/source_final96', 'independent_from_formalizer': True, 'independent_from_decoder': True,
    'read_original_source': True, 'read_current_lean_module': True, 'read_candidate_exposition': True, 'read_blind_reconstruction': True,
    'prior_semantic_verdict_slots_deltas_repairs_used': False, 'reviewer_packet_sha256': packet_canonical,
    'review_run_sha256': run['raw_sha256'], 'run_artifact': run['path'], 'evidence': evidence_text,
    'independently_owned_whole_module_review': {'private_literal_statement': [12, 196], 'public_theorem': [201, 345], 'local_helpers': ['havg', 'hJB', 'hJadj', 'hMJ', 'Kpos compression', 'same-process nested representative'], 'all349_lines': True, 'single_actual108_producer': True, 'compiled_coverage': coverage},
    'exposition_review': exposition, 'source_topology_admission': bind(admission_path),
    'actual_browser_acceptance': False, 'fullExpositionSeal': False}
decision = emit('source-review109.native.json', {
    'verdict': 'equivalent-after-elaboration', 'semantic_slots': slots, 'deltas': deltas, 'repairs': [],
    'source_review': source_review, 'reviewer': '/root/source_final96', 'independent_from_formalizer': True, 'independent_from_decoder': True,
    'reviewer_packet_sha256': packet_canonical, 'publication_binding_sha256': binding, 'review_run_sha256': run['raw_sha256'],
    'review_evidence': evidence_text, 'compiled_source_coverage': coverage, 'exposition': exposition,
    'no_VERIFIED_or_canonical_mutation': True, 'wholepaper_or_browser_completion_claim': False})

archive_dir = OUT / 'raw-archives'
archive_dir.mkdir(exist_ok=False)
artifacts = [bind(p) for p in sorted(OUT.iterdir()) if p.is_file()]
archives = []
for v in list(inputs.values()):
    if v['path'] == frozen['primary']['path']:
        continue
    b = (ROOT / v['path']).read_bytes()
    dst = archive_dir / (v['raw_sha256'] + '.gz')
    if not dst.exists():
        dst.write_bytes(gzip.compress(b, mtime=0))
    assert gzip.decompress(dst.read_bytes()) == b
    archives.append({'original': v, 'archive': {'path': dst.relative_to(ROOT).as_posix(), 'raw_sha256': sha(dst.read_bytes()), 'bytes': dst.stat().st_size}})
closure = emit('closed-RAW-final-source109.native.json', {'kind': 'immutable packet-bound final109 source RAW closure', 'decision': decision, 'inputs': list(inputs.values()), 'artifacts': artifacts, 'archives': archives, 'all_archive_roundtrips_pass': True, 'primary_policy': 'Exact existing snapshot and24 slices referenced; no full primary archive.', 'no_shared_mutation': True})
print(json.dumps({'decision': decision, 'run': run, 'coverage': coverage, 'exposition': exposition, 'closure': closure}, indent=2))
