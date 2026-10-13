from pathlib import Path
import datetime, hashlib, json, re

ROOT = Path(__file__).parent
REPO = ROOT.parents[2]
PRIMARY = REPO / 'runs/20261007-companion-priority/phase-pbps-primary-preread56'
BASE = REPO / 'runs/20261007-companion-priority/pbps-rough-mean-gradient-preproof56'
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def receipt(p):
    b = p.read_bytes()
    lf = b.replace(b'\r\n', b'\n')
    return {'path': p.as_posix(), 'bytes': len(b), 'raw_sha256': sha(b),
            'crlf_to_lf_bytes': len(lf), 'crlf_to_lf_sha256': sha(lf),
            'crlf_count': b.count(b'\r\n'), 'lf_count': b.count(b'\n'),
            'lone_cr_count': b.count(b'\r') - b.count(b'\r\n'),
            'encoding': 'UTF-8', 'bom': b.startswith(b'\xef\xbb\xbf'),
            'normalization_recipe': 'Replace ONLY raw byte pair 0D 0A with 0A; no JSON reserialization or other normalization.'}

def seal(o):
    o['self_hash_recipe'] = {'algorithm': 'SHA-256',
        'payload': 'Complete artifact object excluding only the top-level content_self_sha256 field. Includes schema, recipe, identities, verdict, metadata and every nested receipt.',
        'serialization': 'UTF-8 JSON; ensure_ascii=false; sort_keys=true; separators=(comma,colon); no newline',
        'recursive': False}
    o['content_self_sha256'] = sha(canonical(o))
    return o

def write(n, o):
    (ROOT / n).write_bytes(json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8') + b'\n')
    return receipt(ROOT / n)

def verify_self(p):
    raw = p.read_bytes()
    o = json.loads(raw)
    expected = o.pop('content_self_sha256')
    assert sha(canonical(o)) == expected
    return {'path': p.as_posix(), 'actual_readback': True, 'bytes': len(raw),
            'raw_sha256': sha(raw), 'content_self_sha256': expected, 'complete_payload_self_hash_verified': True}

primary_receipts = [receipt(PRIMARY / n) for n in ['primary.contract.json', 'reviewer.primary.run.json', 'lease.json']]
assert primary_receipts[2]['raw_sha256'] == 'd1e3545eaf1028260a57c79a66e75b0c98557459b0fd116cae89c0796a8d7135'
primary_checks = [verify_self(PRIMARY / n) for n in ['primary.contract.json', 'reviewer.primary.run.json', 'lease.json']]
primary_lease = json.loads((PRIMARY / 'lease.json').read_bytes())
assert primary_lease['status'] == 'CLOSED'
candidate_names = ['root.statement-proposal.json', 'prospective-statement.txt', 'statement.typecheck.0.status.json',
                   'statement.typecheck.0.log', 'statement.typecheck.0.source.raw.snapshot.lean', 'statement.typecheck.0.compiler.lease.json']
candidate_receipts = [receipt(ROOT / n) for n in candidate_names]
for n in candidate_names:
    assert (ROOT / n).read_bytes() == (BASE / n).read_bytes()
raw_statement = (ROOT / 'prospective-statement.txt').read_bytes()
lf_statement = raw_statement.replace(b'\r\n', b'\n')
assert len(lf_statement) == 1755
assert sha(lf_statement) == 'fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
proposal = json.loads((ROOT / 'root.statement-proposal.json').read_bytes())
assert proposal['signature_text'].encode('utf-8') == lf_statement
status = json.loads((ROOT / 'statement.typecheck.0.status.json').read_bytes())
compiler_lease = json.loads((ROOT / 'statement.typecheck.0.compiler.lease.json').read_bytes())
assert status['exit_code'] == compiler_lease['exit_code'] == 0
assert compiler_lease['status'] == 'CLOSED'
snapshot = (ROOT / 'statement.typecheck.0.source.raw.snapshot.lean').read_bytes()
actual_path = REPO / '.astis/pbps-marginal-gradient51/Statement56.lean'
assert actual_path.read_bytes() == snapshot
assert sha(snapshot) == status['source_raw_sha256'] == compiler_lease['source_raw_sha256']
assert sha((ROOT / 'statement.typecheck.0.log').read_bytes()) == status['log_raw_sha256']
body = lf_statement.decode('utf-8').split('    {E : Type*}', 1)[1]
body = '    {E : Type*}' + body.replace('(hβη : (β : ℝ)*η ≤ 1) :', '(hβη : (β : ℝ)*η ≤ 1) =>')
assert '#check fun\n' + body in snapshot.decode('utf-8').replace('\r\n', '\n')
for forbidden in ['sorry', 'axiom', 'theorem ']:
    assert forbidden not in snapshot.decode('utf-8')

definition_slices = []
for relative, first, last in [
    ('.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean', 37, 44),
    ('.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean', 76, 84),
    ('.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/LinearPMap.lean', 60, 71),
    ('.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/LinearPMap.lean', 95, 98),
    ('.lake/packages/mathlib/Mathlib/LinearAlgebra/LinearPMap.lean', 40, 49),
    ('.lake/packages/mathlib/Mathlib/LinearAlgebra/LinearPMap.lean', 733, 737),
    ('.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean', 55, 68),
]:
    source = REPO / relative
    lines = source.read_text(encoding='utf-8').splitlines()
    data = ('\n'.join(lines[first-1:last]) + '\n').encode('utf-8')
    path = ROOT / (source.stem + '-' + str(first) + '-' + str(last) + '.definition-slice.txt')
    path.write_bytes(data)
    definition_slices.append({'source_file': source.as_posix(), 'first_line': first, 'last_line': last,
                              'slice_recipe': 'UTF-8 text splitlines; selected inclusive lines; joined LF plus one final LF',
                              'receipt': receipt(path)})

binders = [
    {'binder': 'E; NormedAddCommGroup; InnerProductSpace real; FiniteDimensional', 'class': 'TYPING',
     'meaning': 'Recorded Euclidean coordinate-invariant finite Hilbert extension, including rank0; not extra analytic regularity'},
    {'binder': 'MeasurableSpace E; BorelSpace E', 'class': 'TYPING', 'meaning': 'Source Euclidean Borel measurable convention'},
    {'binder': 'V : E -> real; alpha beta : NNReal; eta : real', 'class': 'TYPING', 'meaning': 'NNReal signs already follow from source positive alpha and alpha<=beta'},
    {'binder': 'h_alpha', 'class': 'SOURCE', 'meaning': '0<alpha'},
    {'binder': 'h_alpha_beta', 'class': 'SOURCE', 'meaning': 'alpha<=beta'},
    {'binder': 'hV', 'class': 'SOURCE', 'meaning': 'C2 potential; no higher derivative bounds'},
    {'binder': 'hH', 'class': 'SOURCE', 'meaning': 'For every x,v, both Hessian quadratic-form bounds alpha||v||^2 <= Hess V(x)[v,v] <= beta||v||^2'},
    {'binder': 'h_eta', 'class': 'SOURCE', 'meaning': 'eta>0'},
    {'binder': 'h_beta_eta', 'class': 'SOURCE', 'meaning': 'beta eta<=1'},
]
review = seal({
    'schema_version': 1, 'artifact_kind': 'native-independent-statement-binder-source-review',
    'reviewer_identity': '/root/next_primary56', 'created_utc': now(),
    'schema_receipt': receipt(ROOT / 'statement.review.schema.json'),
    'verdict': 'ACCEPT_SCOPED_STATEMENT_ONLY', 'statement_seal_recommendation': 'ADMIT_EXACT_SCOPED_STATEMENT_AFTER_SEPARATE_TOPOLOGY_GATE',
    'primary_stage_receipts': primary_receipts,
    'candidate_receipts': candidate_receipts, 'actual_candidate_source_receipt': receipt(actual_path),
    'named_signature_payload': {'name': 'root.statement-proposal.json/signature_text',
        'recipe': 'JSON decode signature_text then UTF-8 encode its exact string; matches prospective-statement raw CRLF->LF only',
        'bytes': len(lf_statement), 'sha256': sha(lf_statement),
        'scope': 'NAMED_SIGNATURE_PAYLOAD_ONLY; not complete proposal object or raw proposal file'},
    'actual_typecheck': {'exit_code': 0, 'compiler_lease': 'CLOSED', 'kind': 'Prop-only #check; no theorem proof',
        'log_hash_verified': True, 'source_hash_verified': True, 'exact_signature_framing_verified': True, 'repeated': False},
    'binder_audit': binders, 'excess_public_premises': [],
    'definition_audit': {
        'mu_J_nu': 'Literal normalized target, independent standard Gaussian augmentation map and SAME J.snd',
        'S': 'Literal every-y p_y on Y-minus variable; symbol differs from residual S in primary dictionary; source formula exact',
        'tilted_fallback': 'Zero if nonintegrable; source assumptions must discharge normalization for mu and every-y S internally',
        'G': 'Exact iff graph of smooth compact phi and its actual gradient representatives in SAME weighted L2(nu)',
        'gradient_fallback': 'No non-differentiability branch on smooth compact core',
        'closure_fallback': 'G.IsClosable is produced; graph closure is single-valued; fallback closure=G cannot supply the intended result',
        'T_K': 'Uniform continuous linear maps before all u; source conditional mean AE and same-closure gradient pair',
        'slices': definition_slices,
    },
    'seven_semantic_slots': {
        'objects': 'SAME actual mu/J/nu and literal source p_y kernel S; genuine compact-gradient partial map and uniform T/K',
        'domains': 'Scalar/vector L2(nu); exact compact smooth gradient core; its closure rather than separately defined weak H1',
        'quantifiers': 'Source hH every x,v; G/T/K existential before every rough u; rough mean/fiber conclusions nu-AE',
        'assumptions': 'Only original C2/two Hessian/positive capped eta with finite real Hilbert Borel extension; no excess certificate',
        'conclusion': 'Probability nu, dense closable real compact-gradient G, closed closure, all-L2 conditional mean image pair and sharp/4eta defect inequalities',
        'scopes_senses': 'Explicit bounded closed-gradient delta; not full source weak-H1/Gamma B13; every-y literal law vs AE rough representatives',
        'constant_dependencies': 'Exact c=(1-alpha eta)^2/[4(1+alpha eta)] and4eta; no unspecified constants; c in [0,1/4], including alpha eta=1 and rank0',
    },
    'blocking_deltas': [], 'minimal_source_repair': 'NONE_FOR_EXPLICIT_SCOPED_DELTA',
    'weak_H1_omission': 'Acceptable for explicitly scoped genuine closed-gradient result; a later equivalence adapter is mandatory before full printed H1 admission',
    'remaining_boundaries': [
        'Every-y normalization/source kernel same-law identity and AE representative compatibility proved internally',
        'Real compact-core density/closability and noncompact compact-mean admission in same closure',
        'Sharp compact estimate on differences; uniform K extension; continuity/density energy passage',
        'Separately defined weak-H1 equivalence and Gamma positive square root not claimed',
        'Half-turn/main/cost/composition and full B13/paper completion not claimed',
        'Independent exhaustive source topology and preceding55 exact verification/serialized cycle pending; no claim/proof yet',
    ],
    'endpoint_audit': {'rank0': 'Explicit permitted extension; singleton carrier, zero vector gradient, no positive-dimension assumption',
                       'alpha_eta_1': 'Sharp coefficient zero; K must vanish; consistent quadratic Gaussian endpoint; no stricter cap allowed'},
    'metadata_observations': ['Proposal status still says NOT_TYPED; separate completed EXIT0 typecheck is current typing evidence',
                              'Unused binder-name warnings are expected for Prop-only check and do not remove source premises'],
    'native_output_receipt': receipt(ROOT / 'statement.review.md'),
    'independence': {'own_primary_closed_before_candidate_task': True, 'own_primary_close_utc': primary_lease['closed_utc'],
        'candidate_existing_project_proof_bodies_read': False, 'creator_source_proof_graph_read': False,
        'another_review_verdict_read': False, 'canonical_artifacts_mutated': False},
    'source_only': True, 'proof_admission': False, 'formal_theorem_truth_assessed': False,
    'compiler': 'NOT_STARTED_CLOSED',
})

schema = json.loads((ROOT / 'statement.review.schema.json').read_bytes())
# Check every validation keyword used by this simple authored schema; reject unsupported ones.
def validate(value, spec):
    supported = {'$schema', 'title', 'type', 'required', 'properties', 'const', 'minItems', 'maxItems', 'pattern', 'additionalProperties'}
    assert not (set(spec) - supported)
    if 'type' in spec:
        assert {'object': isinstance(value, dict), 'array': isinstance(value, list),
                'string': isinstance(value, str)}[spec['type']]
    if 'const' in spec: assert value == spec['const']
    if 'required' in spec: assert all(k in value for k in spec['required'])
    if 'minItems' in spec: assert len(value) >= spec['minItems']
    if 'maxItems' in spec: assert len(value) <= spec['maxItems']
    if 'pattern' in spec: assert re.search(spec['pattern'], value)
    for k, child in spec.get('properties', {}).items():
        if k in value: validate(value[k], child)
validate(review, schema)
review_receipt = write('statement.review.json', review)
run = seal({'schema_version': 1, 'artifact_kind': 'native-statement-source-review-run',
    'run_id': 'PBPS-STATEMENT-REVIEW56', 'reviewer_identity': '/root/next_primary56', 'completed_utc': now(),
    'status': 'COMPLETE_SOURCE_ONLY_STATEMENT_REVIEW', 'verdict': review['verdict'],
    'review_receipt': review_receipt, 'native_output_receipt': receipt(ROOT / 'statement.review.md'),
    'schema_receipt': receipt(ROOT / 'statement.review.schema.json'),
    'schema_validation': 'PASS; explicit checker evaluates every validation keyword occurring in authored schema, rejects unsupported keywords',
    'primary_stage_receipts': primary_receipts, 'candidate_receipts': candidate_receipts,
    'script_receipt': receipt(Path(__file__)),
    'independent_chronology': 'Own source-only primary contract and CLOSED lease preceded receipt/inspection of candidate56; source stage unchanged',
    'candidate_proof_bodies_read': False, 'creator_source_graph_read': False, 'other_verdicts_read': False,
    'compiler': 'NOT_STARTED_CLOSED', 'typecheck_repeated': False,
    'source_only': True, 'proof_admission': False, 'children': [], 'background_processes': [],
    'receipt_diagnosis': 'First local assertion compared 1755 LF length to 1786 raw CRLF bytes; corrected by explicit CRLF->LF only recipe, snapshots untouched',
})
run_receipt = write('reviewer.statement.run.json', run)
readback = [verify_self(ROOT / n) for n in ['statement.review.json', 'reviewer.statement.run.json']]
read_review = json.loads((ROOT / 'statement.review.json').read_bytes())
validate(read_review, schema)
for rec in candidate_receipts + primary_receipts:
    assert receipt(Path(rec['path'])) == rec
for field in ['native_output_receipt', 'schema_receipt']:
    assert receipt(Path(review[field]['path'])) == review[field]
for d in definition_slices:
    assert receipt(Path(d['receipt']['path'])) == d['receipt']
lease = seal({'schema_version': 1, 'artifact_kind': 'native-statement-review-lease',
    'lease_id': 'PBPS-STATEMENT-REVIEW56-LEASE', 'owner': '/root/next_primary56',
    'status': 'CLOSED', 'closed_utc': now(), 'exclusive_owned_folder': ROOT.as_posix(),
    'resources': {'read': 'CLOSED', 'write': 'CLOSED', 'Python': 'CLOSED', 'compiler': 'NOT_STARTED_CLOSED'},
    'readback_before_close': readback, 'primary_readback_before_close': primary_checks,
    'all_embedded_source_candidate_output_receipts_reverified': True, 'schema_readback_validation': 'PASS',
    'review_receipt': review_receipt, 'native_run_receipt': run_receipt,
    'original_primary_lease_preserved': primary_receipts[2],
    'closure_order': 'Actual readback/hash/schema checks completed before final lease write; no further filesystem operations',
    'Python_closure_semantics': 'Final lease write followed only by in-memory receipt printing and normal process exit',
    'compiler_started': False, 'compiler_repeated': False, 'source_only': True, 'proof_admission': False,
    'children': [], 'background_processes': [],
})
lease_bytes = json.dumps(lease, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8') + b'\n'
(ROOT / 'lease.json').write_bytes(lease_bytes)
print(json.dumps({'verdict': review['verdict'], 'review_receipt': review_receipt,
    'native_run_receipt': run_receipt, 'lease_raw_bytes': len(lease_bytes), 'lease_raw_sha256': sha(lease_bytes),
    'lease_content_self_sha256': lease['content_self_sha256'], 'actual_readbacks': readback,
    'status': 'CLOSED', 'compiler': 'NOT_STARTED_CLOSED', 'proof_admission': False}, ensure_ascii=False, indent=2))
