from pathlib import Path
import gzip
import hashlib
import json
import re

ROOT = Path('E:/Samplinglib')
RUN = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-expectation107'
OUT = RUN / 'final-source107'
PRE = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-expectation-preread107'
SRC = ROOT / 'runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106/next-primary107'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def ref(p):
    if isinstance(p, str):
        p = ROOT / p
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}


def load(p):
    return json.loads(p.read_text(encoding='utf8'))


def put(name, x):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode())
    return ref(p)


freeze = load(OUT / 'primary-first107.native.json')
primary = ROOT / freeze['primary']['path']
assert ref(primary) == freeze['primary']
for r in freeze['all21_source_regions_rehashed']:
    assert sha(primary.read_bytes()[r['byte_start']:r['byte_end_exclusive']]) == r['raw_sha256']
packet_path = RUN / 'reviewer-packet107.json'
assert ref(packet_path)['raw_sha256'] == '5b301f118683e88574e4a2034fd63a41a59dd32f151ae4c2d548a5bb64346360'
packet = load(packet_path)
canonical = sha(json.dumps({k: v for k, v in packet.items() if k != 'packet_sha256'}, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
assert canonical == packet['packet_sha256'] == 'bc88acaa8e46caf95ffbb218346d14fa2893dca905b81ce486dbbb62bab9c983'
binding = packet['publication_binding_sha256']
assert binding == 'c479ce9043d6693b5669974f1d1ff1f9eab6aba210ddb4621c00bf5c0b934740'
assert all(v is False for v in packet['anti_anchoring'].values())
prod = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2Expectation.lean'
assert ref(prod)['raw_sha256'] == '4c35e0b71362bec3563e3d07c9f122d6b7ca4cae604f7a88aad397d2a028f4d6'
b = prod.read_bytes()
s = b.decode()
assert b.count(b'\n') == 345 and b'\r' not in b
assert packet['candidate_publication_context']['current_lean_module'] == s
header = PRE / 'Header107.lean'
h = header.read_text(encoding='utf8')
assert s[s.index('    {E : Type*}'):s.index('\nset_option maxHeartbeats')].strip() == h[h.index('    {E : Type*}'):h.index('#check candidate')].strip()
stmt = s[s.index('private def actual_l2_expectation_statement'):s.index('\nset_option maxHeartbeats')]
assert len(re.findall(r'^\s*let ', stmt, re.M)) == 40
assert len(re.findall(r'^    let ', stmt[:stmt.index('    ∃ Z :')], re.M)) == 37

decoder_dir = ROOT / 'runs/semantic-roundtrip/anonymous107/decoder-native'
manifest = load(decoder_dir / 'manifest.json')
decoder = load(decoder_dir / 'decoder.json')
assert ref(decoder_dir / 'manifest.json')['raw_sha256'] == 'c0b377fcc402e92a6e5ca31cffbc4e36e5bdd60c49b53b17fe8548a34f7d10cb'
assert all(x is False for x in manifest['visibility'].values())
assert manifest['agent_identity'] == '/root/blind_decoder107'
input_path = Path(manifest['input_path'])
assert sha(input_path.read_bytes()) == manifest['input_raw_sha256']
for name, r in manifest['outputs'].items():
    raw = (decoder_dir / name).read_bytes()
    assert sha(raw) == r['sha256'] and len(raw) == r['bytes']
assert packet['blind_reconstruction']['text'] == (decoder_dir / 'reconstruction.txt').read_text(encoding='utf8')
assert manifest['decoder_run_sha256'] == sha(('\n'.join([manifest['agent_identity'], manifest['input_raw_sha256'], manifest['packet_canonical_sha256'], decoder['reconstructed_text_sha256']])).encode())

graph_path = RUN / 'source-graph107.effective.json'
assert ref(graph_path)['raw_sha256'] == 'a56c0953ffc5d09a507769cc90d2b117a54486e46865e60d16b00528a993727d'
graph = load(graph_path)
assert graph['counts'] == {'nodes': 85, 'edges': 161}
route_admission = RUN / 'independent-route107/route-admission107.native.json'
assert ref(route_admission)['raw_sha256'] == '6e8bf4de75be73d27f4f16b1e647242c2778c6f00083671863372be67b18cc5d'
assert load(route_admission)['decision'] == 'ACCEPT_EXACT_QUOTIENT_IDENTIFICATION_OR_OVERLAY'
assert not any(g['target'] == 'AE-REP107' for g in graph['AND_groups'])
assert 'AE-REP107' in graph['AND_route_alternatives']
assert 'ae_ae_of_ae_prod' not in s
whole_path = RUN / 'independent-whole-math107/whole-math-decision107.native.json'
whole = load(whole_path)
assert whole['decision'] == 'ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL'
kernel_path = RUN / 'independent-whole-math107/fresh-kernel-receipt107.native.json'
kernel = load(kernel_path)
assert kernel['exit_code'] == 0 and kernel['terminal_closed']
for key in ['production', 'input', 'stdout', 'stderr']:
    assert ref(ROOT / kernel[key]['path']) == kernel[key]
assert (ROOT / kernel['input']['path']).read_bytes().startswith(b)
assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation\n' not in (ROOT / kernel['input']['path']).read_text(encoding='utf8')
assert all(x['axioms'] == ['propext', 'Classical.choice', 'Quot.sound'] for x in whole['kernel_contract']['axioms'])

lesson_path = ROOT / 'website/content/declaration_lessons/pbps-actual-l2-expectation.json'
publication_path = ROOT / 'website/content/publications/pbps-actual-l2-expectation.json'
unit = load(lesson_path)['units'][0]
item = load(publication_path)['items'][0]
assert unit['statement'] == unit['lean_statement'] == item['statement'] == packet['source']['original_text']
assert packet['candidate_publication_context']['statement'] == unit['statement']
assert unit['statement'].count('\n') == 15 and '\\n' not in unit['statement']
assert len(unit['steps']) == 10
parents = [
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality.actual_bounded_gibbs_duality',
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization',
    'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
assert unit['astis_dependencies'] == parents
assert all(p in s for p in parents)
line_bytes = b.splitlines(keepends=True)


def span(lo, hi, meaning):
    raw = b''.join(line_bytes[lo - 1:hi])
    return {'line_start': lo, 'line_end': hi, 'raw_sha256': sha(raw), 'bytes': len(raw), 'meaning': meaning}


step_judgments = [
    'One106 call returns one global Z before every subsequent parameter and test, and all inherited106 results are re-exported at284.',
    'Actual product-pullback Hilbert isometries and B.adjoint C yield norm≤1 and the pairing. Formula pullback identities are identities of L2 classes, with a.e. representatives208-211; no pointwise representative assertion.',
    'Arbitrary MemLp input pulls back to product L2 then L1. Both operator output and clock average are L1 before uniqueness. Section L1 is exported by prod_right_ae at270.',
    'Finite-measure indicators are L2; indicator product integrability is explicit244-249 before signed Fubini261. heq follows L1 set-integral uniqueness237.',
    'Only after heq, MemLp.ae_eq gives output membership269, and Lp.ext identifies classes271-272. This universal one-operator result entails representative independence structurally.',
    'The square integral is equal to quotient norm squared via toLp a.e. representative and real Hilbert inner product; input membership discharges integrability.',
    'Joint Borel total integral has no boundedness premise; every-section L1 and boundC are asserted only for bounded Borel G. Actual P supplies probability/SFinite.',
    'Actual103 derives probability of literal nu, actual unit exponential law derives probability P, and h106 supplies endpoint preservation for the same Z. Choice of family has no time-regularity claim.',
    'Parameterwise clock-a.e. Z0=z suffices for each initial z. Pointwise equality of its clock integral is then transported to equality of L2 maps; no uniform exceptional set required.',
    'Every MemLp G receives AE section L1, exact output class identity and finite square-integral contraction. Full momentum-flip L2 identity remains a subsequent argument.'
]
step_regions = []
for i, st in enumerate(unit['steps']):
    r = st['lean_source_region']
    code = st['lean'].encode()
    raw = b''.join(line_bytes[r['start_line'] - 1:r['end_line']])
    assert raw == code
    assert sha(code) == r['exact_code_raw_sha256']
    assert r['source_raw_sha256'] == ref(prod)['raw_sha256']
    runs = [len(m.group()) for m in re.finditer(r'\\+', st['formula'])]
    assert runs and all(n == 1 for n in runs)
    step_regions.append({'step': i + 1, 'title': st['title'], 'formula': st['formula'],
                         'source_span': span(r['start_line'], r['end_line'], step_judgments[i]),
                         'displayed_UTF8_code_raw_sha256': sha(code), 'display_equals_source_span_bytes': True,
                         'decoded_TeX_backslash_run_lengths': runs, 'verdict': 'accepted'})
exposition = put('exposition107.native.json', {
    'kind': 'bounded source/exposition seal for ten authored adjacent formula/proof regions',
    'reviewer': '/root/source_final96', 'reviewer_packet_sha256': canonical, 'publication_binding_sha256': binding,
    'lesson': ref(lesson_path), 'publication': ref(publication_path), 'production': ref(prod),
    'whole_statement_audit': 'Full literal mathematical restatement includes original six conditions, phase order, true normalization, all algorithm definitions, pointwise arc/fallback, parameterwise AE initialization, sameZ bounded106 results and all107 operator quantifiers. H,R,nu,op,brackets and operator family are explained. Source finite-prefix indexing is explicitly1-based in the restatement with initial s0/z0; finite Lean indices implement that standard shift. A history guard and later operator A occupy different scopes.',
    'statement_newline_audit': {'actual_newlines': 15, 'literal_backslash_n': 0},
    'steps': step_regions, 'source_attribution': item['source'],
    'direct_ASTIS_parents': parents,
    'dependency_label_note': 'mathlib memLp_congr_ae is indirect support through directly invoked MemLp.ae_eq, not a claimed explicit call. The independently admitted graph retains ae_ae_of_ae_prod only for an alternate route.',
    'byte_format': 'Production has345 LF newlines and noCR. Every decoded lesson lean string exactly equals its raw source-line interval including finalLF. No CRLF or whitespace normalization is required for this module.',
    'adjacency_contract': 'Ten authored formula steps each carry the exact corresponding Lean interval. Full privateProp and public declaration require initially folded adjacent reader rendering; actual generated DOM/browser acceptance remains a separate delivery check.',
    'exposition_verdict': 'ACCEPT_BOUNDED_TEN_STEP_EXPOSITION', 'blocking_defects': [], 'repairs': [],
    'fullExpositionSeal': False, 'actual_browser_acceptance': False, 'whole_paper_completion': False})

prior_coverage_path = ROOT / 'runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106/final-source106/compiled-source-coverage106.native.json'
prior = load(prior_coverage_path)
prior_ids = {x['id'] for x in prior['node_dispositions']}
current_map = {
    'COUNT93': ([180, 182], 'Same-Z joint/arc/fallback/zero projections obtained through single actual106 producer; no direct93 call.'),
    'AVG100': ([180, 182], 'Inherited bounded signed duality h106 re-exported284, not reproved in107.'),
    'INV100': ([311, 318], 'Same-Z actual endpoint measure preservation from h106 supplies actual lift.'),
    'NORM': ([302, 308], 'Actual103 probability and exact nu product equality, no extra premise.'),
    parents[2]: ([285, 286], 'Actual clock probability invoked here and309-310.'),
    'BOREL-OP107': ([284, 301], 'Joint Borel literal expectation plus bounded sections and boundC.'),
    'L2-PRODUCT107': ([189, 195], 'Initial and endpoint pullback L2 isometries; actual instantiation311-319.'),
    'L2-CONSTRUCT107': ([183, 215], 'One Hilbert contraction and pairing constructed before all tests.'),
    'PRODUCT-L1-FUBINI107': ([228, 235], 'Product/outer L1 precede identification; indicator product L1 at244-249 and sectionAE at270.'),
    'L2-IDENTIFY107': ([236, 272], 'Indicator pairing, signed Fubini, L1 uniqueness, membership transfer and quotient identity.'),
    'AE-REP107': ([216, 272], 'Structural consequence of universal one-operator class identity; selected L2-IDENTIFY107 route. No standalone cross-representative theorem or ae_ae_of_ae_prod call.'),
    'L2-LIFT107': ([302, 341], 'Actual same-Z family, A0=id and norm/representative/square conclusions.'),
    'MeasureTheory.StronglyMeasurable.integral_prod_right': ([289, 293], 'Direct invoked Borel integral theorem.'),
    'MeasureTheory.measurePreserving_fst': ([189, 191], 'Semantic ingredient constructed directly via measurable_fst and Measure.map_fst_prod, repeated228-230; this exact named lemma is not invoked.'),
    'MeasureTheory.Lp.compMeasurePreservingₗᵢ': ([192, 195], 'Direct pullback isometry constructors.'),
    'ContinuousLinearMap.adjoint': ([196, 207], 'Direct construction B.adjoint C and adjoint norm/pairing support.'),
    'ContinuousLinearMap.adjoint_inner_right': ([205, 207], 'Direct pairing theorem.'),
    'MeasureTheory.Lp.coeFn_compMeasurePreserving': ([208, 211], 'Direct representative formulas.'),
    'MeasureTheory.MemLp.comp_measurePreserving': ([231, 232], 'Direct actual product MemLp transport.'),
    'MeasureTheory.MemLp.integrable': ([231, 235], 'Direct finite-probability L2-to-L1 conversion.'),
    'MeasureTheory.Integrable.prod_right_ae': ([269, 272], 'Direct sectionAE export at270.'),
    'MeasureTheory.Integrable.integral_prod_left': ([231, 233], 'Direct outerL1 before uniqueness.'),
    'MeasureTheory.L2.inner_def': ([205, 207], 'Direct Hilbert pairing representation.'),
    'MeasureTheory.integral_prod': ([244, 264], 'Direct signed Fubini261 after integrability.'),
    'MeasureTheory.indicatorConstLp': ([238, 240], 'Direct finite-set L2 indicator.'),
    'MeasureTheory.indicatorConstLp_coeFn': ([239, 242], 'Direct a.e. indicator representative.'),
    'MeasureTheory.Integrable.ae_eq_of_forall_setIntegral_eq': ([233, 268], 'Direct L1 uniqueness237; bothL1 proven before.'),
}
node_dispositions = []
for n in graph['nodes']:
    ident = n['id']
    if ident in current_map:
        rg, meaning = current_map[ident]
        node_dispositions.append({'id': ident, 'disposition': meaning, 'production_span': span(*rg, meaning), 'compiled107_credit': ident not in prior_ids})
    elif ident == 'MeasureTheory.ae_ae_of_ae_prod':
        node_dispositions.append({'id': ident, 'disposition': 'Retained unselected alternative support; no direct current call and no new107 proof credit.', 'selected': False})
    elif ident in ['L2A3', 'RESTART']:
        node_dispositions.append({'id': ident, 'disposition': 'Future source boundary remains red and outside this theorem.', 'compiled107_credit': False})
    else:
        assert ident in prior_ids, ident
        node_dispositions.append({'id': ident, 'disposition': 'Unchanged inherited106 source mechanism; exact previous node disposition reused without new107 theorem credit.', 'inherited_coverage': ref(prior_coverage_path), 'lookup_node_id': ident, 'compiled107_credit': False})
assert len(node_dispositions) == 85
edges = []
for e in graph['edges']:
    a, z = e['source'], e['target']
    if z == 'AE-REP107':
        disp = 'selected structural quotient consequence' if a == 'L2-IDENTIFY107' else 'retained unselected planned iterated-AE alternative'
    elif z in ['L2A3', 'RESTART']:
        disp = 'future source consumer incidence; not a completed theorem or direct107 call'
    elif a in prior_ids and z in prior_ids:
        disp = 'unchanged inherited source incidence; exact prior coverage reused'
    else:
        disp = 'current analytic support incidence; source/target node dispositions provide exact spans and distinguish semantic constructed facts from named calls'
    edges.append({'source': a, 'target': z, 'disposition': disp, 'kernel_call_certificate': False})
assert len(edges) == 161
regions = []
for r in freeze['all21_source_regions_rehashed']:
    rr = dict(r)
    if r['id'] == 'A3-boundary':
        disp = 'Current strict fixed-time realL2 domain/contraction prerequisite, not fullA3, strong continuity, semigroup, position averaging or formal generator argument.'
    elif r['id'] == 'weight-matching-and-invariance':
        disp = 'Bounded identity and invariance inherited106; current107 fills actual L2 operator/representative/contraction requirement before final density sentence. A3 remains red.'
    elif r['id'] in ['standing-curvature', 'standing-eta']:
        disp = 'Exact original six assumptions preserved, with no new integrability/operator/probability source binder.'
    elif r['id'] == 'source-license':
        disp = 'Pinned arXiv nonexclusive license; no full source archive created.'
    else:
        disp = 'Unchanged inherited106 mathematical/definition source region; exact prior coverage reused without new proof credit.'
    rr['disposition107'] = disp
    regions.append(rr)
all_spans = [span(1, 13, 'Imports/namespace/options'), span(14, 164, 'Full exact sealed private proposition'), span(165, 179, 'Options/public six-binder theorem/unfold/literal context')]
all_spans += [x['source_span'] for x in step_regions]
all_spans += [span(342, 345, 'Standard axiom print and namespace closure')]
assert sorted(i for x in all_spans for i in range(x['line_start'], x['line_end'] + 1)) == list(range(1, 346))
coverage = put('compiled-source-coverage107.native.json', {
    'kind': 'independently owned whole-module source/compiled-coverage107', 'reviewer': '/root/source_final96',
    'reviewer_packet_sha256': canonical, 'publication_binding_sha256': binding,
    'production': ref(prod), 'source_primary': ref(primary), 'source_graph': ref(graph_path),
    'independent_base_topology': ref(SRC / 'independent-topology107/v2-admission/admission107.v2.native.json'),
    'independent_route_admission': ref(route_admission), 'topology_self_validation': False,
    'effective_counts': {'nodes': 85, 'edges': 161, 'source_regions': 21, 'production_lines': 345, 'statement_lets': 40, 'actual_parents': 3, 'exposition_regions': 10},
    'source_regions': regions, 'node_dispositions': node_dispositions, 'edge_dispositions': edges,
    'all_production_regions': all_spans, 'whole_module': 'Private fullProp, public theorem and all three proof-local helpers reviewed; no unreviewed mathematical span.',
    'literal_definition_audit': {'global_lets': 37, 'scoped_lets': ['op', 'endpoint', 'opG'], 'same_Z': True, 'rank0_time0': True, 'header_identity': 'Exact full body text after type-only declaration name, including same original six conditions.'},
    'actual_parent_discharge': [{'declaration': parents[0], 'lines': [180, 182], 'use': 'One same-Z producer; all bounded106 results re-exported284, actual endpointMP used318.'}, {'declaration': parents[1], 'lines': [303, 308], 'use': 'Actual nu probability from derived phase normalization/product identity.'}, {'declaration': parents[2], 'lines': [285, 286], 'additional_lines': [309, 310], 'use': 'Actual P probability/SFinite/finite product support.'}],
    'proof_ingredient_vs_source_binder': 'Generic helper μ,ν,Z and preservation/probability hypotheses are proof-local and instantiated by actual parents; public statement adds no such premise.',
    'AE_REP': 'Universal haverage_core fixes A before allG. heq/hOp/Lp.ext identify every actual expectation class; equal input classes yield equal outputs. This is a structural consequence, not a separately invoked ae_ae_of_ae_prod proof.',
    'OR_semantics': 'Original AE-REP AND group is superseded; selected L2-IDENTIFY107 alternative is sufficient. Retained planned iterated-AE edges are not mandatory current-call dependencies.',
    'fresh_kernel': ref(kernel_path), 'whole_math': ref(whole_path),
    'remaining_reds': ['Full L2 momentum-flip A3', 'strong continuity', 'restart/Markov/semigroup', 'older separate kernel witness identification', 'momentum averaged selfadjointness', 'hypocoercivity, errors, costs, composition and paper completion']})

descriptions = {
    'objects': ('Actual source phase law, clock dynamics and real expectation on the one global process; L2 equivalence classes, not a supplied transition provider.', 'All40 lets reconstructed; privateProp14-164 matches approved header; same-Z extraction180-182 and re-export284. No abstract helper escapes as a public premise.', 'explicit-elaboration'),
    'domains': ('Source finite-dimensional Euclidean phase and nonnegative finite time, with bounded Borel tests and the real L2 extension domain.', 'Coordinate-free finite-dimensional real Hilbert/Borel E includesrank0. Arbitrary MemLp input requires onlyAE strong measurability; Borel joint parameter claim applies separately to measurable G.', 'explicit-elaboration'),
    'quantifiers': ('One actual process fixed before centers, references, times and tests; operator family fixed before its input representatives.', 'Global∃Z and inherited universal contracts126-148; ∀BorelG149; ∀y,r∃A before allT,G,hG156-164. Generichaverage_core similarly fixesA beforeG; no function-dependent operator.', 'same'),
    'assumptions': ('Exactly hα,hαβ,hV,hH,hη,hβη plus ambient real finite-dimensional Borel structure. Source analysis supplies normalization/invariance/integrability as consequences.', 'Original six preserved inprivate andpublic binders. Probability, MP, L1/L2 output, same-process operator are internally derived. Test boundC andMemLp are observable domains only.', 'same'),
    'conclusion': ('Actual fixed-time L2 contraction/representative domain needed for printed density extension, retaining bounded source duality and invariance on the same Z.', 'Fresh decoder reconstructs all inherited106 and new107 outputs exactly. Compiled local averaging provesnorm1,classidentity,AEsections,squarebound,A0identity; no fullA3 asserted.', 'explicit-elaboration'),
    'scopes': ('Pointwise arc/fallback, parameterwise clockAE initialization; L2 identities only modulo nuAE. Fixed-time construction does not assert temporal semigroup structure.', 'No uniform nullset, pointwise arbitrary representative equality, joint operator regularity, restart orMarkov. AE-REP is a structural quotient consequence with separately admitted route.', 'same'),
    'constant_dependencies': ('Exact eta andsqrteta dynamics, normalized phase law and unit clocks; contraction1 and unchanged finite test boundC.', 'All rates,weights,phaseorder andconstants preserved. Norm/square coefficient1 follows actual probability andstationarity; no extra dimension,time ornormalizer constant.', 'same')}
slots = {}
for k in packet['review_contract']['semantic_slots']:
    original, evidence, relation = descriptions[k]
    slots[k] = {'original': original, 'reconstructed': decoder[k], 'relation': relation, 'evidence': evidence}
deltas = [
    {'slot': 'domains', 'severity': 'informational', 'description': 'Explicit coordinate-free ambient realization includes rank zero.', 'source': 'Finite-dimensional Euclidean phase.', 'lean': 'Finite real inner-product Borel space with canonical volume/Gaussian, includingrank0.', 'evidence': 'Exact formulas and original six inequalities retained; no infinite-dimensional extension.', 'blocking': False},
    {'slot': 'conclusion', 'severity': 'informational', 'description': 'Bounded domain completion for the source density step is made explicit.', 'source': 'A.1 extends bounded duality by density toA.3.', 'lean': 'Closes actual expectation measurability, L1/L2 representative construction and fixed-time contraction; preserves source bounded duality but leavesA3 andsemigroup red.', 'evidence': 'Complete statement and all10 explanation regions disclose ASTIS completion and exact exclusion boundary.', 'blocking': False},
    {'slot': 'scopes', 'severity': 'informational', 'description': 'Representative independence uses the independently admitted universal quotient-identification alternative.', 'source': 'Well-defined realL2 expectation is required; the source prescribes no exclusive representative-transfer proof.', 'lean': 'L2-IDENTIFY107 structurally suppliesAE-REP107 for oneoperator fixedbeforeallG.', 'evidence': 'Exact independent route admission6e8bf4de...; heq236-268,hOp/Lp.ext269-272 andactualinstantiation311-341. No explicit ae_ae_of_ae_prod call claimed.', 'blocking': False}]
run = put('source-review-run107.native.json', {
    'reviewer': '/root/source_final96', 'formalizer': packet['roles']['formalizer'], 'decoder': manifest['agent_identity'],
    'reviewer_packet': ref(packet_path), 'reviewer_packet_sha256': canonical, 'publication_binding_sha256': binding,
    'production': ref(prod), 'primary_first': ref(OUT / 'primary-first107.native.json'),
    'compiled_coverage': coverage, 'exposition': exposition, 'decoder_manifest': ref(decoder_dir / 'manifest.json'),
    'primary_before_current_publication_decoder': True, 'prior_semantic_verdict_slots_deltas_or_repairs_used': False,
    'prior_involvement': freeze['anti_anchoring']['prior_involvement'],
    'independently_owned_whole_module_review': True,
    'independent_math_evidence_use': 'Rehash exact fresh source-plus-original-header kernel and standard3 axioms; source andexposition judgments authored independently.',
    'no_topology_self_validation': True, 'no_shared_mutation': True, 'no_VERIFIED_transition': True,
    'browser_acceptance': False, 'full_paper_credit': False})
decision = put('source-review107.native.json', {
    'semantic_slots': slots, 'deltas': deltas, 'verdict': 'equivalent-after-elaboration', 'repairs': [],
    'reviewer_packet_sha256': canonical, 'publication_binding_sha256': binding, 'review_run_sha256': run['raw_sha256'],
    'source_review': {'state': 'accepted', 'reviewer': '/root/source_final96',
        'independent_from_formalizer': True, 'independent_from_decoder': True,
        'reviewer_packet_sha256': canonical, 'review_run_sha256': run['raw_sha256'],
        'run_artifact': run['path'], 'publication_binding_sha256': binding,
        'source_read_before_current_publication_and_decoder': True, 'prior_semantic_slots_read': False,
        'prior_deltas_read': False, 'prior_verdict_read': False, 'prior_repairs_read': False,
        'prior_involvement': freeze['anti_anchoring']['prior_involvement'],
        'independently_owned_whole_module_review': True, 'private_helpers_reviewed': True,
        'coverage_artifact': coverage, 'exposition_artifact': exposition,
        'evidence': 'Fresh primary-first21slices and exactheader, all7semantic slots and anonymous107 reconstruction, entire345-line module/40lets/3actualparents, independently admitted85/161 graph coverage and10exactformula/code regions reviewed. Sourcehypotheses unchanged; L1 beforeL2 identification; sameZ andAE-vs-Borel scopes preserved. No repairs. Exact LF source regions equaldisplaybytes. AE-REP follows universal quotient identity; unselectedae_ae_of_ae_prod isnotdirectcall. Boundedfixedtimecompletion only, noA3/semigroup/browser/fullpaper claim.'},
    'reviewer': '/root/source_final96', 'independent_from_formalizer': True, 'independent_from_decoder': True,
    'review_evidence': coverage['path'], 'compiled_source_coverage': coverage, 'exposition': exposition,
    'blocking_findings': [], 'no_VERIFIED_transition': True})

inputs = [primary, packet_path, prod, header, lesson_path, publication_path, graph_path,
          route_admission, whole_path, kernel_path, ROOT / kernel['input']['path'], ROOT / kernel['stdout']['path'], ROOT / kernel['stderr']['path'],
          decoder_dir / 'manifest.json', decoder_dir / 'decoder.json', decoder_dir / 'reconstruction.txt', input_path,
          SRC / 'recommendation107.native.json', SRC / 'literal-context107.native.json', SRC / 'graph-expansion107/source-proof-graph-delta107.v2.native.json',
          SRC / 'graph-expansion107/source-coverage107.v2-overlay.native.json', SRC / 'independent-topology107/v2-admission/admission107.v2.native.json',
          RUN / 'source-route107/quotient-identification107.proposal.native.json', prior_coverage_path, PRE / 'root.statement-seal107.json']
for p in ['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedGibbsDuality.lean', 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean', 'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']:
    inputs.append(ROOT / p)
archives = []
for p in sorted(OUT.iterdir()):
    if p.is_file() and not p.name.endswith('.gz'):
        a = p.with_name(p.name + '.raw.gz')
        if a.exists():
            assert gzip.decompress(a.read_bytes()) == p.read_bytes()
        else:
            a.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
        assert gzip.decompress(a.read_bytes()) == p.read_bytes()
        archives.append({'raw_path': ref(p)['path'], 'raw_sha256': ref(p)['raw_sha256'], 'archive': ref(a)['path'], 'archive_raw_sha256': ref(a)['raw_sha256']})
closure = put('closed-RAW-final-source107.native.json', {
    'kind': 'closed independent final source/exposition107 RAW manifest', 'decision': decision,
    'reviewer_packet_sha256': canonical, 'publication_binding_sha256': binding, 'run': run,
    'selected_inputs': [ref(p) for p in inputs], 'owned_artifacts': [ref(p) for p in sorted(OUT.iterdir()) if p.is_file()],
    'original_RAW_archives': archives, 'no_full_primary_archive': True, 'self_hash_intentionally_omitted': True})
print(json.dumps({'decision': decision, 'coverage': coverage, 'exposition': exposition, 'run': run, 'closure': closure}, indent=2))
