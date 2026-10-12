import gzip
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PRE = OUT.parent
SOURCE = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-flip-duality108/next-primary109'
inputs = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def bind(p):
    p = Path(p)
    b = p.read_bytes()
    v = {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}
    inputs[v['path']] = v
    return v


def read(p):
    bind(p)
    return json.loads(p.read_text(encoding='utf-8'))


def emit(name, obj):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    return bind(p)


frozen = read(SOURCE / 'primary-first109.native.json')
primary = ROOT / frozen['primary']['path']
assert bind(primary) == frozen['primary']
raw = primary.read_bytes()
for r in frozen['regions']:
    assert sha(raw[r['byte_start']:r['byte_end_exclusive']]) == r['raw_sha256']
for name in ['recommendation109.native.json', 'actual-interface109.native.json', 'retrieval109.native.json', 'source-proof-graph-delta109.native.json', 'source-coverage109.native.json', 'closed-RAW-manifest109.native.json']:
    bind(SOURCE / name)
topology = bind(SOURCE / 'independent-topology109/decision109.native.json')
bind(SOURCE / 'independent-topology109/closed-RAW-topology109.native.json')
delivery = bind(SOURCE.parent / 'integration108/postpush-binding108.json')
header = bind(PRE / 'Header109.lean')
assert header['raw_sha256'] == '927043eaaace6083ec00c750037e4c69f21173595b85646bb9a5a1b63795e31b'
receipt = read(PRE / 'type-only1/receipt.json')
assert receipt['exit_code'] == 0 and receipt['header_raw_sha256'] == header['raw_sha256']
bind(PRE / 'type-only1/stdout.log')
bind(PRE / 'type-only1/stderr.log')
for name in ['companion-papers-handoff.md.current.exactraw', 'samplewiki_companion_frontiers.json.current.exactraw', 'ASTIS-SW-PBPS-actual-l2-flip-duality.json.current.exactraw', 'lean-toolchain.current.exactraw', 'lake-manifest.json.current.exactraw']:
    bind(PRE / name)
prod = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2FlipDuality.lean'
producer = bind(prod)
assert producer['raw_sha256'] == '2358ce3e7a74b5d1ebdf857be873588db3ffdefd08239b7f2df37bf6b72349cd'
h = (PRE / 'Header109.lean').read_text(encoding='utf-8')
p = prod.read_text(encoding='utf-8')
hl = h.splitlines(keepends=True)


def span(a, b):
    return {'start': a, 'end': b, 'utf8_lf_sha256': sha(''.join(hl[a - 1:b]).encode('utf-8'))}


expected = emit('expected-slots109.reused.native.json', {
    'kind': 'immutable primary-first109 expectation reuse for header review',
    'original_primary_first': bind(SOURCE / 'primary-first109.native.json'),
    'original_record_predates_Header109': True,
    'read_order': 'Reuse source-only expected slots authored and frozen before Header109 existed. This header review opened the header then revalidated all24 original slice hashes; it does not claim a new pre-header reading pass.',
    'primary': frozen['primary'], 'regions': frozen['regions'], 'expected_semantic_slots': frozen['expected_semantic_slots'],
    'prior_involvement': 'Reviewer authored source-only109 graph/interface and reviewed108 source; separate blind_decoder106 admitted graph topology. Current task is exact prospective header source comparison only.',
    'no_new_primary_copy': True})

literal_h = h[h.index('    let c :'):h.index('    ∃ Z :')]
literal_p = p[p.index('    let c :'):p.index('    ∃ Z :')]
assert literal_h == literal_p
prefix_h = h[h.index('    ∃ Z :'):h.index('            (∀ T : ℝ≥0, (A T).adjoint')]
prefix_p = p[p.index('    ∃ Z :'):p.index('            ∀ T : ℝ≥0, (A T).adjoint')]
assert prefix_h == prefix_p
binders_h = h[h.index('    {E : Type*}'):h.index(' : Prop := by')]
binders_p = p[p.index('    {E : Type*}'):p.index(' : Prop := by')]
assert binders_h == binders_p
literal_matches = list(re.finditer(r'^    let (\S+)', literal_h, re.M))
literal_records = []
for i, m in enumerate(literal_matches):
    end = literal_matches[i + 1].start() if i + 1 < len(literal_matches) else len(literal_h)
    text = literal_h[m.start():end]
    literal_records.append({'name': m.group(1), 'exact_equal_108': True, 'utf8_sha256': sha(text.encode('utf-8'))})
assert len(literal_records) == 37
assert len(re.findall(r'^\s*let ', h, re.M)) == 47
comparison = emit('header-comparison109.native.json', {
    'header': header, 'producer108': producer, 'original_six_binders_exact_text': True,
    'literal_definitions': literal_records, 'literal37_span': span(23, 123),
    'all47_let_names': re.findall(r'^\s*let (\S+)', h, re.M),
    'inherited_globalZ_prefix_exact_text': True, 'inherited_prefix_span': span(124, 168),
    'inherited_adjoint_clause': {'span': span(169, 170), 'difference': 'Only parentheses delimit forallT before conjoining109 outputs; same adjoint identity and same A/J remain.'},
    'public_assumptions': ['hα', 'hαβ', 'hV', 'hH', 'hη', 'hβη'],
    'new_output_binders_are_not_input_premises': ['exists hfst after same hR/J', 'forall hG:MemLp for Gaussian output representative', 'forall hf:MemLp for tested position observable', 'exists hbar/hk:MemLp derived outputs'],
    'same_witness_scope': 'GlobalZ outside all parameters; existsA under y,xRef and before allT/G; hR and canonicalJ before new mu/hfst/B/M/Kpos. No second process/operator existential.',
    'technical_definitions': {'mu': span(171, 171), 'hfst_B_M': span(172, 175), 'gbar': span(180, 180), 'Kpos': span(185, 186), 'kTf': span(190, 191)},
    'edge_cases': ['rank0 retained without a nontriviality premise', 'T0 output from same A0 and M B=id', 'n0/empty sectors remain in unchanged37 algorithm definitions', 'no division by norm of a test function or dimension', 'all AE scopes parameterwise, no uniform exceptional set', 'arbitrary MemLp representative handled only AE, no pointwise quotient identity']})

slot_text = {
    'objects': 'Header retains actual37 algorithm literals and globalZ, same A and canonical phase flip J. New B is canonical fst pullback and M=B*. Kpos is literally M A_T B, not a supplied provider.',
    'domains': 'Real Hilbert L2(mu) and L2(nu y); mu is actual tilted position measure, nu position-first product with stdGaussian E. All finite dimensions including0; T:NNReal; raw observables require exactly MemLp2.',
    'quantifiers': 'One globalZ, same all-time A per y,xRef and same J from108. Derived hfst precedes B/M; Gaussian statement quantifies allG/hG, Kpos everyT and allf/hf. Both hbar and hk are output existence. All inherited outputs remain.',
    'assumptions': 'The original six analytic binders match108 literally. Finite/SFinite laws, measurability, Gaussian section L1, quotient identity and flip absorption are proof obligations/outputs, not added public assumptions. Observable MemLp is the domain condition, not an extra source analytic premise.',
    'conclusion': 'B/M representatives, norms<=1, M B=id; allG Gaussian-average identification and integrable sections; J B=B and M J=M; Kpos0=id, Kpos self-adjoint contraction, actual nested Gaussian-clock expectation with inner and outer integrability and MemLp quotient identification.',
    'scopes': 'Matches bounded source A.1 Gaussian-averaging slice. No Markov positivity/constants, strong continuity, semigroup/restart, reference average A2 or full-paper assertion. No pathwise right-continuous reversal introduced.',
    'constant_dependencies': 'Exact Vy=V+norm(x-y)^2/(2 eta), standard Gaussian probability averaging, contraction1 and all nonnegative times. No extra Gaussian density factor/normalizer; Gaussian outer, actual P-clock inner order is exact.'}
slots = {k: {'status': 'match', 'source': frozen['expected_semantic_slots'][k], 'header': v, 'evidence': [header, comparison]} for k, v in slot_text.items()}
new_regions = [
    {'lines': [171, 178], 'nodes': ['MOMENTUM-LIFT109'], 'meaning': 'literal position law and canonical B/M, representative, contractions and left inverse'},
    {'lines': [179, 182], 'nodes': ['MOMENTUM-L1-FUBINI109', 'MOMENTUM-IDENTIFY109'], 'meaning': 'universal Gaussian integral and quotient/section contract'},
    {'lines': [183, 184], 'nodes': ['FLIP-ABSORB109'], 'meaning': 'same J absorption on both sides'},
    {'lines': [185, 188], 'nodes': ['POSITION-OP109'], 'meaning': 'literal compression, zero time, self-adjointness and contraction'},
    {'lines': [189, 196], 'nodes': ['POSITION-REP109', 'POSITION-AVG109'], 'meaning': 'sameZ actual nested expectation and both section-integrability levels'}]
coverage = emit('header-source-coverage109.native.json', {
    'kind': 'prospective header/source coverage, not compiled proof coverage', 'header': header,
    'source_graph': bind(SOURCE / 'source-proof-graph-delta109.native.json'),
    'independent_topology_admission': topology, 'reviewer_does_not_self_validate_graph': True,
    'source_regions': [{**r, 'disposition': ('selected averaging109 statement; Markov clause not exported' if r['id'] == 'gaussian-momentum-averaging' else 'future boundary only' if r['id'] in ['strong-continuity-after-A3', 'averaged-halfturn-consumer'] else 'unchanged inherited source context/assumptions/license; exact raw rehashed')} for r in frozen['regions']],
    'all24_regions_rehashed': True, 'all21_inherited_regions_preserved': True,
    'header_partition': [{'lines': [1, 12], 'kind': 'imports and type-only scaffolding'}, {'lines': [13, 20], 'kind': 'exact six source binders and ambient structure'}, {'lines': [21, 123], 'kind': '37 exact actual definitions'}, {'lines': [124, 170], 'kind': 'all108 outputs and same witnesses'}, *new_regions, {'lines': [197, 201], 'kind': 'type-only check and namespace closure'}],
    'no_new_source_hypothesis': True, 'proof_ingredients_remain_obligations': ['Gaussian signed Fubini and section integrability', 'adjoint identification via indicator tests', 'AE transport through canonical B/J', 'adjoint/norm composition', 'same108 expectation and nested section identification'],
    'remaining_red': ['positivity/constant preservation and full Markov conclusion', 'strong continuity and semigroup/restart', 'A2 independent-reference integral and actual kernel identification', 'complex L2', 'hypocoercivity and complexity', 'whole-paper/Goal completion']})
run = emit('header-source-review-run109.native.json', {
    'kind': 'independent exact prospective header source review', 'reviewer': '/root/source_final96',
    'expected_slots': expected, 'comparison': comparison, 'coverage': coverage,
    'header': header, 'type_only_receipt': bind(PRE / 'type-only1/receipt.json'), 'prior108_delivery': delivery,
    'independence': 'Source graph author; separate topology admission is referenced, never self-issued. Header judgment independently compares frozen primary expectations and literal108 interface. No109 implementation exists or was read; no earlier final semantic verdict used.',
    'diagnostics': ['Initial type receipt absent; positive decision held until exact exit0 receipt appeared.', 'A read-only directory loop attempted UTF8 decode on topology .gz and failed; exact JSON was already read. Binary archive was not changed; subsequent reads targeted explicit JSON only.'],
    'typecheck_boundary': 'Only candidate:Prop elaboration and #check, not theorem proof. Expected six unused-Prop-binder warnings preserve source assumptions.',
    'mutations': 'Only owned independent-header-source109 output files; no production/header/shared/source-graph changes'})
decision = emit('header-source-decision109.native.json', {
    'kind': 'exact prospective109 source-header decision', 'verdict': 'ACCEPT_EXACT_PROSPECTIVE_HEADER_SOURCE_BOUNDARY',
    'reviewer': '/root/source_final96', 'header': header, 'semantic_slots': slots,
    'deltas': [{'slot': 'scopes', 'severity': 'informational', 'description': 'Bounded selection retains actual Gaussian averaging/self-adjoint contraction; Markov clauses stay red.', 'source': 'A.1(iii) and final Gaussian paragraph also assert Markovness.', 'header': 'No positivity/constant preservation/full Markov export.', 'evidence': [coverage], 'blocking': False}],
    'repairs': [], 'blocking_findings': [], 'run_artifact': run,
    'source_graph_admission_external': topology,
    'truth_boundary': 'Source-facing type-only header acceptance only. No109 theorem/proof/Statement Seal/claim, compiled fidelity, VERIFIED transition or topology self-admission.',
    'proof_still_required': True})

archive_dir = OUT / 'raw-archives'
archive_dir.mkdir(exist_ok=False)
artifacts = []
archives = []
for p in sorted(OUT.iterdir()):
    if not p.is_file():
        continue
    original = bind(p)
    b = p.read_bytes()
    dst = archive_dir / (p.name + '.gz')
    dst.write_bytes(gzip.compress(b, mtime=0))
    assert gzip.decompress(dst.read_bytes()) == b
    artifacts.append(original)
    archives.append({'original': original, 'archive': {'path': dst.relative_to(ROOT).as_posix(), 'raw_sha256': sha(dst.read_bytes()), 'bytes': dst.stat().st_size}})
manifest = emit('closed-RAW-header-source109.native.json', {'kind': 'immutable exact header source review closure109', 'decision': decision, 'artifacts': artifacts, 'inputs': list(inputs.values()), 'archives': archives, 'lossless_roundtrips': True, 'no_full_primary_archive': True})
print(json.dumps({'decision': decision, 'coverage': coverage, 'run': run, 'closure': manifest}, indent=2))
