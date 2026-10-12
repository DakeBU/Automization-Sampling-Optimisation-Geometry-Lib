from pathlib import Path
import json
import hashlib
import gzip
import re

ROOT = Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority'
RUN = BASE / 'pbps-actual-l2-flip-duality108'
OUT = RUN / 'final-source108'
SOURCE = BASE / 'pbps-actual-l2-expectation107/next-primary108'


def bind(p):
    data = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def save(name, obj):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    return bind(p)


packet_path = RUN / 'reviewer108.v2.input.json'
packet = read(packet_path)
assert packet['packet_sha256'] == 'bd708f85e27fc1138b96983ef06a093e37a2594a06b66faa905072f604e43a17'
assert packet['publication_binding_sha256'] == 'f9236569dac3fd0a3d57346165556a193c3b65d019b37bb5db13bdc84df1a4dd'
first = read(OUT / 'first-reviewer108.input.exactraw.snapshot.json')
for key in ['source', 'lean', 'blind_reconstruction']:
    assert packet[key] == first[key]
prod = ROOT / packet['lean']['file']
assert bind(prod)['raw_sha256'] == '2358ce3e7a74b5d1ebdf857be873588db3ffdefd08239b7f2df37bf6b72349cd'
lines = prod.read_bytes().splitlines(keepends=True)
assert len(lines) == 289
assert b'\r' not in prod.read_bytes()
header = BASE / 'pbps-actual-l2-flip-preread108/Header108.lean'
assert prod.read_text(encoding='utf-8').splitlines()[13:171] == header.read_text(encoding='utf-8').splitlines()[12:170]
lesson_path = ROOT / 'website/content/declaration_lessons/pbps-actual-l2-flip-duality.json'
publication_path = ROOT / 'website/content/publications/pbps-actual-l2-flip-duality.json'
lesson = read(lesson_path)['units'][0]
publication = read(publication_path)['items'][0]
assert all(lesson.get(k) == v for k, v in packet['candidate_publication_context']['lesson'].items())
assert set(lesson) - set(packet['candidate_publication_context']['lesson']) == {'boundary'}
assert lesson['statement'] == publication['statement']
assert lesson['statement'].count('\\n') == 0
repair_path = RUN / 'independent-adjacency-repair108/admission108.native.json'
repair = read(repair_path)
assert bind(repair_path)['raw_sha256'] == '9b269166fdc277f6e6cfec00f199ec388f0a3796593cd39bbcb684323c51862f'
assert repair['decision'] == 'ACCEPT_EXACT_ADJACENCY_REPAIR108'
assert repair['after_lesson_RAW_sha256'] == bind(lesson_path)['raw_sha256']
whole_path = RUN / 'independent-whole-math108/whole-math-decision108.native.json'
whole = read(whole_path)
assert bind(whole_path)['raw_sha256'] == 'fcdaf68a68da172879306129d16c4ca0baa9760dda19d5f453277bb4ae2dab8e'
assert whole['decision'] == 'ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL'
assert whole['production'] == bind(prod)
decoder_dir = ROOT / 'runs/semantic-roundtrip/anonymous108/decoder-native'
manifest = read(decoder_dir / 'manifest.json')
decoder = read(decoder_dir / 'decoder.json')
for name, data in manifest['outputs'].items():
    assert bind(decoder_dir / name)['raw_sha256'] == data['raw_sha256']
assert packet['blind_reconstruction']['text'] == decoder['reconstructed_theorem_text']
assert packet['blind_reconstruction']['text_sha256'] == bind(decoder_dir / 'reconstructed-theorem.txt')['raw_sha256']
assert all(value is False for key, value in manifest.items() if key.endswith('_visible'))

explanations = [
    'One107 call yields Z and h107; the same family L and all prior conclusions are retained. No fresh105/106 witness.',
    'Actual product law is preserved using Gaussian negation and map_prod_map, including all hR proof lines after the independently admitted region correction.',
    'The literal J pullback has AE representatives; quasi-MP AE transport plus Lp.ext and R squared=id proves involution. Isometry is supplied by the literal type.',
    'Universal inherited same-L toLp identity gives the actual clock-integral representative AE, preserving arbitrary MemLp input.',
    'Simple representatives carry their own MemLp/measurability. Every quotient and reflected quotient is aligned by AE equality and Lp.ext.',
    'Finite range gives bounds enlarged by maxC0. Same-Z bounded signed duality is applied and AE substitutions convert the two integrals to L2 pairings.',
    'Two-variable denseRange induction applies to the closed equality locus of jointly continuous pairings on real L2.',
    'adjoint_inner_left, J.inner_map_map, J involution and real_inner_comm give the correct orientation; ext_inner_right and operator extensionality finish.'
]
regions = []
previous = 186
for index, step in enumerate(lesson['steps']):
    region = step['lean_source_region']
    a, z = region['start_line'], region['end_line']
    assert a == previous + 1
    previous = z
    raw = b''.join(lines[a-1:z])
    assert step['lean'].encode('utf-8') == raw
    assert hashlib.sha256(raw).hexdigest() == region['exact_code_raw_sha256']
    runs = [len(m.group()) for m in re.finditer(r'\\+', step['formula'])]
    assert all(n == 1 for n in runs)
    regions.append({'step': index + 1, 'title': step['title'], 'line_start': a, 'line_end': z,
                    'raw_source_span_sha256': hashlib.sha256(raw).hexdigest(),
                    'displayed_code_UTF8_sha256': hashlib.sha256(step['lean'].encode()).hexdigest(),
                    'normalization': 'none; source and displayed code both LF and byte-identical',
                    'formula': step['formula'], 'literal_backslash_run_lengths': runs,
                    'source_formula_alignment': explanations[index], 'verdict': 'accepted'})
assert previous == 285 and len(regions) == 8
exposition = save('exposition108.native.json', {
    'verdict': 'ACCEPT_EIGHT_AUTHORED_ADJACENT_FORMULA_REGIONS_ONLY',
    'reviewer': '/root/source_final96', 'reviewer_packet': bind(packet_path),
    'reviewer_packet_sha256': packet['packet_sha256'],
    'publication_binding_sha256': packet['publication_binding_sha256'],
    'lesson': bind(lesson_path), 'publication': bind(publication_path), 'production': bind(prod),
    'regions': regions, 'all99_proof_lines187_285_exact_once': True,
    'statement': {'complete_attributed_restatement': True, 'all6_conditions_present': True,
                  'algorithm_context_and_H_R_pi_gamma_nu_op_bracket_notation_complete': True,
                  'actual_newline_count': lesson['statement'].count('\n'), 'literal_backslash_n_count': 0,
                  'all_inherited_outputs_and_new_sameA_adjoint_present': True},
    'original_finding': bind(OUT / 'exposition-adjacency-finding108.native.json'),
    'separate_repair_admission': bind(repair_path),
    'repair_scope': 'Only exact-code boundaries for steps2/3 and their hashes changed; no source theorem repair. Original packet/finding preserved.',
    'bounded_exposition_seal': {'state': 'accepted-for-authored-eight-step-formula-proof',
                               'generated_reader_acceptance': False, 'live_browser_acceptance': False,
                               'full_exposition_seal': False, 'whole_paper_completion': False},
    'source_vs_ASTIS': 'Source explicitly says extend by density; canonical pullback, exact representatives and two-variable closed-locus extension are attributed ASTIS details. No generator exponentiation or extra source assumption.'
})

slot_text = {
    'objects': ('Actual conditional phase process, fixed phase Gibbs law and momentum pullback in source Eq3.1/A3.',
                'Fresh blind reconstruction identifies all37 actual definitions, one globalZ, fixed nu_y, actual clock expectation A and canonical J.',
                'explicit-elaboration', 'LiteralProp14–171 matches header; source dynamics/clock/phase order retained. Direct107 once187–189; actualR/J194–212.'),
    'domains': ('Euclidean finite-dimensional phase, nonnegative times, real L2 realization of sourceA3.',
                'Finite real Hilbert Borel E including rank0, H=E×E position first, T:NNReal and all real L2 classes.',
                'explicit-elaboration', 'No positive dimension/horizon premise. Real scalar restriction stated in title, formula proof and boundary; complex-L2 not claimed.'),
    'quantifiers': ('For each fixed center/reference and time, adjoint flip relation for all L2 inputs of the same actual process.',
                    'One globalZ before parameters; for each y,r oneA family covers allT/allMemLp tests and new hR/J/Aadjoint outputs.',
                    'explicit-elaboration', 'SameZ retained190; sameL retained192–193; hrep213–218 universal; no independently chosen105/106 Z or newA.'),
    'assumptions': ('Original positive lower curvature, upper curvature, C2 V, Hessian bounds and positive capped eta.',
                    'Exactly six analytic binders; test bounds and MemLp are local observable clauses, not new dynamics assumptions.',
                    'same', 'Original six binders14–21/176–183. hR existential output; finite-factor instances internally inferred; simple classes have ownMemLp.'),
    'conclusion': ('A_T*=R A_T R on L2, obtained by extending bounded duality through density.',
                   'Exact CLM equality (A T).adjoint=J.comp((A T).comp J), sameA as all107 outputs; J AE pullback and involution.',
                   'explicit-elaboration', 'Bounded pair219–268; both arguments extended269–275; full real adjoint276–285. Canonical output specifies every operator, not a supplied relation.'),
    'scopes': ('Fixed-time sourceA3; later strong continuity, semigroup and averaged-position statements are separate.',
               'Quotient equalities exact, representatives AE per input; no common exceptional set, pathwise jump reversal or semigroup conclusion.',
               'equivalent', 'Parameterwise initialization134; arbitraryMemLp160–163; canonicalJ167–169. SourceA3 label corrected before packet, realL2 boundary explicit.'),
    'constant_dependencies': ('Exact phase law, harmonic sqrt eta/rate scaling; reversal has no added coefficient.',
                             'Unit clockP; nu_y independent ofr; J determined only byR/nu_y; contraction1 and A0=id inherited.',
                             'same', 'All37 literal definitions unchanged. New hR under y,r is proof witness only; actualJ166 and relation170–171 have no extra scaling or time restriction.')
}
slots = {k: {'original': a, 'reconstructed': c, 'relation': rel, 'evidence': e}
         for k, (a, c, rel, e) in slot_text.items()}
deltas = [
    {'slot': 'domains', 'severity': 'informational', 'description': 'Explicit real Hilbert/Borel realization includes rank zero; complex-L2 is outside the accepted boundary.',
     'source': 'Euclidean phase L2 inA3', 'lean': 'FiniteDimensional realHilbertBorel E and Lp R 2', 'evidence': 'Header/Prop ambient telescope and publication explicit realL2 boundary', 'blocking': False},
    {'slot': 'conclusion', 'severity': 'informational', 'description': 'ASTIS exposes the canonical flip and dense-subspace extension as derived outputs/internal proofs; no source ingredient becomes a premise.',
     'source': 'Density-extension sentence3210–3227', 'lean': 'SameA, derivedhR, literalJ, all-class adjoint equality', 'evidence': 'Source-first expectation and exact194–285 proof coverage', 'blocking': False},
    {'slot': 'scopes', 'severity': 'informational', 'description': 'Actual total raw-path and AE quotient contracts remain explicit; source fixed-time identity grants no restart/semigroup or whole-paper completion.',
     'source': 'A.1 fixed-time A3 with separate subsequent consequences', 'lean': 'Retained107 globalZ plus new fixed-time realL2 relation', 'evidence': 'Fresh blind reconstruction scopes and exactProp outputs', 'blocking': False}
]
coverage = bind(OUT / 'compiled-source-coverage108.native.json')
run = save('source-review-run108.native.json', {
    'kind': 'independent final108 source/exposition review', 'reviewer': '/root/source_final96',
    'primary_first': bind(OUT / 'primary-first108.native.json'),
    'primary_first_stage_closure': bind(OUT / 'primary-first108.closed-RAW.native.json'),
    'reviewer_packet': bind(packet_path), 'reviewer_packet_sha256': packet['packet_sha256'],
    'publication_binding_sha256': packet['publication_binding_sha256'],
    'production': bind(prod), 'compiled_source_coverage': coverage, 'exposition': exposition,
    'whole_mathematics': bind(whole_path),
    'whole_mathematics_used_for': 'Exact compilation/original-seal witness/standard3axioms, not source fidelity verdict.',
    'blind_manifest': bind(decoder_dir / 'manifest.json'),
    'blind_reconstruction': bind(decoder_dir / 'reconstructed-theorem.txt'),
    'native_decoder_run_sha256': manifest['decoder_run_sha256'],
    'canonical_adopted_decoder_run_sha256': packet['blind_reconstruction']['decoder_run_sha256'],
    'decoder_run_distinction': 'Native authored run hash and canonical adoption binding are distinct, both preserved; reconstruction text/statement/input identity unchanged.',
    'anti_anchoring': {'primary_before_current_production_publisher_decoder': True,
                       'prior_final_verdict_slots_deltas_used': False,
                       'prior_header_and_source_creator_involvement_disclosed': True,
                       'independent_from_formalizer': True, 'independent_from_decoder': True,
                       'topology_admission_by_separate_reviewer_only': True},
    'independently_owned_scope': 'Whole module289lines, private literalProp and public theorem/local proof, all21source slices,107node196edge dispositions and eight adjacent exposition regions.',
    'repair_history': {'first_packet': bind(OUT / 'first-reviewer108.input.exactraw.snapshot.json'),
                       'finding': bind(OUT / 'exposition-adjacency-finding108.native.json'),
                       'independent_admission': bind(repair_path), 'source_theorem_repairs': []},
    'semantic_slots': slots, 'deltas': deltas,
    'verdict': 'equivalent-after-elaboration', 'repairs': [],
    'no_canonical_mutation_or_VERIFIED_transition': True
})
evidence = 'Primary-first receipt, exact source21slices, complete289-line module/privateProp review, compiled-source-coverage108 and eight-region exposition108; same107 witness and full realL2 density extension checked. Original adjacency defect preserved and closed by separate exact repair admission. No browser/fullpaper acceptance.'
source_review = {'state': 'accepted', 'reviewer': '/root/source_final96',
                 'independent_from_formalizer': True, 'independent_from_decoder': True,
                 'reviewer_packet_sha256': packet['packet_sha256'],
                 'review_run_sha256': run['raw_sha256'], 'run_artifact': run['path'],
                 'evidence': evidence, 'publication_binding_sha256': packet['publication_binding_sha256'],
                 'primary_first': True, 'prior_verdicts_read': False,
                 'whole_module_review': True, 'private_helpers_reviewed': True,
                 'compiled_source_coverage': coverage, 'exposition': exposition,
                 'topology_creator_self_admission': False}
decision = save('source-review108.native.json', {
    'verdict': 'equivalent-after-elaboration', 'semantic_slots': slots, 'deltas': deltas, 'repairs': [],
    'source_review': source_review, 'reviewer': '/root/source_final96',
    'reviewer_packet_sha256': packet['packet_sha256'], 'review_run_sha256': run['raw_sha256'],
    'publication_binding_sha256': packet['publication_binding_sha256'],
    'independent_from_formalizer': True, 'independent_from_decoder': True,
    'review_evidence': evidence, 'blocking_findings': [],
    'remaining_scope': 'Fixed-time realL2 A3 only. Strong continuity, restart/Markov/semigroup, complexL2, separately chosen kernel identification, averaged position construction, hypocoercivity, costs, composition, fullpaper and live browser acceptance remain separate.'
})
inputs = [packet_path, prod, header, lesson_path, publication_path, whole_path,
          RUN / 'independent-whole-math108/fresh-kernel-receipt108.native.json',
          RUN / 'independent-whole-math108/FreshExactProductionAndHeader108.lean',
          RUN / 'independent-whole-math108/closed-RAW-manifest108.native.json',
          RUN / 'focused108/full2/receipt.json',
          ROOT / 'runs/semantic-roundtrip/anonymous108/input.json',
          decoder_dir / 'manifest.json', decoder_dir / 'decoder.json', decoder_dir / 'reconstructed-theorem.txt',
          SOURCE / 'recommendation108.native.json', SOURCE / 'retrieval108.native.json',
          SOURCE / 'route-policy-repair108/source-proof-graph-delta108.v2.native.json',
          SOURCE / 'route-policy-repair108/source-coverage108.v2-overlay.native.json',
          SOURCE / 'independent-topology108/v2-admission/admission108.v2.native.json',
          RUN / 'adjacency-repair108/proposal108.json', RUN / 'adjacency-repair108/lesson-before.exactraw.json',
          RUN / 'adjacency-repair108/lesson-after.exactraw.json', repair_path,
          RUN / 'independent-adjacency-repair108/closed-RAW-adjacency-repair108.native.json',
          ROOT / 'lean-toolchain', ROOT / 'lake-manifest.json']
primary = read(OUT / 'primary-first108.native.json')['primary']
inputs.append(ROOT / primary['path'])
artifacts = [p for p in sorted(OUT.iterdir()) if p.is_file() and p.suffix != '.gz']
archive_dir = OUT / 'RAW-archives'
archive_dir.mkdir()
archives = []
for index, p in enumerate(inputs + artifacts):
    if p == ROOT / primary['path']:
        continue
    archive = archive_dir / (str(index) + '.raw.gz')
    archive.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
    assert gzip.decompress(archive.read_bytes()) == p.read_bytes()
    archives.append({'original': bind(p), 'archive': bind(archive)})
closure = save('closed-RAW-final-source108.native.json', {
    'kind': 'immutable independent final108 source review closure',
    'inputs': [bind(p) for p in inputs], 'artifacts': [bind(p) for p in artifacts],
    'archives': archives, 'decision': decision, 'review_run': run,
    'coverage': coverage, 'exposition': exposition,
    'no_new_full_primary_archive': True, 'no_mutable_canonical_audit_binding_required': True,
    'exact_final_packet_binding': packet['packet_sha256'],
    'native_originals_preserved': True, 'no_shared_mutation': True
})
print(json.dumps({'decision': decision, 'run': run, 'coverage': coverage, 'exposition': exposition, 'closure': closure}, indent=2))
