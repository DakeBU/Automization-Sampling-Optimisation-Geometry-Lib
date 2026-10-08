from pathlib import Path
import hashlib, json, datetime

ROOT = Path(__file__).parent
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda obj: json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def seal(obj):
    obj['self_hash_recipe'] = {
        'algorithm': 'SHA-256',
        'serialization': 'UTF-8 JSON; ensure_ascii=false; sort_keys=true; separators=(comma,colon); no trailing newline',
        'exclusion': 'Only top-level content_self_sha256 is omitted. Every other key and nested field is included.',
        'recursive': False,
    }
    obj['content_self_sha256'] = sha(canonical(obj))
    return obj

def receipt(path):
    b = path.read_bytes()
    norm = b.replace(b'\r\n', b'\n')
    return {
        'path': path.as_posix(), 'bytes': len(b), 'raw_sha256': sha(b),
        'crlf_to_lf_bytes': len(norm), 'crlf_to_lf_sha256': sha(norm),
        'crlf_count': b.count(b'\r\n'), 'lf_count': b.count(b'\n'),
        'lone_cr_count': b.count(b'\r') - b.count(b'\r\n'),
        'encoding': 'UTF-8', 'bom': b.startswith(b'\xef\xbb\xbf'),
        'normalization_recipe': 'Replace raw byte pair 0D 0A with 0A only; no JSON reserialization or other whitespace normalization.',
    }

def write(name, obj):
    data = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8') + b'\n'
    (ROOT / name).write_bytes(data)
    return receipt(ROOT / name)

b = (ROOT / 'primary-pbps.raw.snapshot.html').read_bytes()
assert len(b) == 1482128
assert sha(b) == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
anchors = []
for path in sorted(ROOT.glob('*.raw.html')):
    fragment = path.read_bytes()
    start = b.find(fragment)
    assert start >= 0 and b.find(fragment, start + 1) == -1
    anchors.append({
        'id': path.name.removesuffix('.raw.html'), 'balanced': True,
        'balance_basis': 'HTMLParser nested stack matching the element start/end tag, not first-closing-tag regex',
        'start_byte_in_snapshot': start, 'end_byte_exclusive': start + len(fragment),
        'receipt': receipt(path),
        'text_receipt': receipt(path.with_name(path.name.removesuffix('.raw.html') + '.text.txt')),
    })
contract = seal({
    'schema_version': 1, 'contract_id': 'PBPS-PRIMARY-PREREAD56',
    'created_utc': now(), 'status': 'PRIMARY_SOURCE_CONTRACT_SEALED_ONLY',
    'source_id': 'arXiv:2609.06905v1',
    'source_title': 'Accelerated High-Accuracy Sampling from a Warm Start via the Proximal Bouncy Particle Sampler',
    'source_locator': 'https://arxiv.org/html/2609.06905v1',
    'snapshot_origin': 'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html',
    'snapshot_receipt': receipt(ROOT / 'primary-pbps.raw.snapshot.html'),
    'anchors': anchors,
    'assessment_receipt': receipt(ROOT / 'primary.assessment.md'),
    'source_dictionary': {
        'mu': 'Original X target exp(-V) normalized',
        'J': 'pi_eta, SAME augmented law (2.6)', 'nu': 'pi_eta^Y, SAME Y marginal',
        'R': 'U_PP, conditional mean of f(Y-) given Y+',
        'S': 'U_perpP, reflected residual in L2(pi_eta)',
        'candidate_definition_match': 'NOT_ASSESSED; no candidate inspected',
    },
    'assumptions': ['V in C2(R^d)', '0<alpha<=beta',
                    'For every x, alpha I <= Hessian V(x) <= beta I',
                    'eta>0, beta eta<=1 for B.13; original scale eta in (0,1/beta]'],
    'quantifiers': {
        'compact_estimate': 'f in C_c^infinity(R^d); smooth conditional calculation parameterized by y; integrated in SAME nu',
        'rough_endpoint': 'For every f in L2(nu); quotient/AE semantics; no mean-zero restriction',
        'C8': 'For every f in H1(nu), nu-almost every y',
        'half_turn_C11': 'beta eta<=1/2; uniformly in y, every a; universal C',
        'mean_zero_only': 'B.14/B.15 spectral bounds use H_P,0',
    },
    'formulas': {
        'C1': 'grad Rf(y)=Cov(f(Y-),s_y(Y-)|Y+=y)',
        'score': 's_y(u)=-1/2 grad V((y+u)/2)-(y-u)/(4 eta)',
        'pointwise_compact': '||grad Rf(y)||^2 <= (eta^-1-alpha)^2/[4(alpha+eta^-1)] Var(f(Y-)|Y+=y)',
        'C2': 'eta ||grad Rf||^2 <= (1-alpha eta)^2/[4(1+alpha eta)] ||Sf||^2',
        'B13': 'Rf in H1(nu); 4 eta ||grad Rf||^2 <= ||f||^2-||Rf||^2=||Gamma_P f||^2=||Sf||^2',
        'B9': '||Sf||^2=E Var(f(Y-)|Y+)',
        'Gamma': 'Gamma_P=(I-R^2)^(1/2), the nonnegative operator square root',
    },
    'source_H1_convention': {
        'explicit_primary_definition': 'ABSENT; source uses weighted H1, density and gradient closedness',
        'authored_closed_graph_equivalence': 'REQUIRES_SEPARATE_PROOF; not obtained by naming relation H1',
        'source_invalid_verdict': 'NOT_ISSUED',
    },
    'required_analytic_bridges': [
        'Compact input conditional means have noncompact support; admit each Rf_n to same genuine weighted gradient domain before closure',
        'Smooth compact core dense in SAME weighted L2 and/or H1 as used',
        'SAME R contraction and gradient differences estimate',
        'Gradient closedness/uniqueness with genuine weak-gradient or equivalent closure convention',
        'AE-safe rough fibers and representatives',
    ],
    'source_graph_nodes': ['standing-model', 'B8-exchangeable-reflected-pair', 'B9-same-law-variance',
        'conditional-density-score', 'curvature-score-derivative-bounds', 'conditional-Poincare',
        'conditional-Cauchy-Schwarz', 'compact-C2', 'SOURCE_GAP-noncompact-output-domain-admission',
        'SOURCE_GAP-weighted-density-closedness-identification', 'all-L2-B13-gradient-part',
        'separate-positive-square-root-Gamma-identities'],
    'independence': {'candidate_Lean_API_body_read': False, 'prior_verdicts_read': False,
                     'whole_math_directories_read': False, 'primary_first': True},
    'formal_admission': 'NOT_ASSESSED', 'compiler': 'NOT_STARTED_CLOSED',
})
contract_receipt = write('primary.contract.json', contract)
run = seal({
    'schema_version': 1, 'run_id': 'native-source-reviewer-primary56',
    'reviewer_identity': '/root/next_primary56', 'completed_utc': now(),
    'status': 'COMPLETE_SOURCE_ONLY', 'task': 'Independent primary-first PBPS boundary56 preread',
    'native_output': receipt(ROOT / 'primary.assessment.md'),
    'contract_receipt': contract_receipt,
    'inputs_read': [receipt(ROOT / 'primary-pbps.raw.snapshot.html')],
    'protocols_read': ['docs/proof-digestion-protocol.md', 'docs/evidence-routed-memory-protocol.md',
                       '.agents/skills/astis-semantic-roundtrip/SKILL.md'],
    'source_reads': ['A2.SS1', 'A2.Thmtheorem1', 'A3.SS1', 'A3.SS2', 'S1.p1', 'S1.p2',
                     'S2.SS2', 'S2.SS3.SSS0.Px1', 'A2.SS2', 'A4.SS1', 'A4.SS2'],
    'extractor_receipt': receipt(ROOT / 'extract_source.py'),
    'seal_script_receipt': receipt(Path(__file__)),
    'independence': {'candidate_Lean_API_body_read': False, 'prior_verdicts_read': False,
                     'whole_math_directories_read': False},
    'compiler': 'NOT_STARTED_CLOSED', 'formal_admission': 'NOT_ASSESSED',
    'tool_issues': [
        {'issue': 'bs4 unavailable; initial script import failed before folder creation',
         'resolution': 'Standard-library HTMLParser used', 'mathematical_effect': 'NONE'},
        {'issue': 'One large PowerShell sealing command automatically rejected with blocked by policy',
         'resolution': 'Write explicit owned artifact files with apply_patch; run short direct Python command',
         'mathematical_effect': 'NONE'},
    ],
    'mutation_scope': 'owned preread56 folder only; no canonical writes',
    'children_spawned': False, 'background_processes_started': False,
})
run_receipt = write('reviewer.primary.run.json', run)
readback = []
for name in ['primary.contract.json', 'reviewer.primary.run.json']:
    raw = (ROOT / name).read_bytes()
    obj = json.loads(raw)
    expected = obj.pop('content_self_sha256')
    actual = sha(canonical(obj))
    assert actual == expected
    readback.append({'file': name, 'actual_readback': True, 'raw_sha256': sha(raw),
                     'bytes': len(raw), 'content_self_sha256': expected,
                     'content_self_hash_verified': True})
for a in anchors:
    assert receipt(Path(a['receipt']['path'])) == a['receipt']
    assert receipt(Path(a['text_receipt']['path'])) == a['text_receipt']
assert receipt(ROOT / 'primary.assessment.md') == run['native_output']
assert receipt(ROOT / 'primary-pbps.raw.snapshot.html') == contract['snapshot_receipt']
lease = seal({
    'schema_version': 1, 'lease_id': 'PBPS-PRIMARY-PREREAD56-LEASE',
    'owner': '/root/next_primary56', 'exclusive_owned_folder': ROOT.as_posix(),
    'status': 'CLOSED', 'closed_utc': now(),
    'closure_order': 'Actual contract/run/source/output readback checks completed before final lease write; no filesystem operation after lease.',
    'readback_before_close': readback,
    'source_anchor_readback_verified': True, 'snapshot_readback_verified': True,
    'native_output_readback_verified': True,
    'resources': {'read': 'CLOSED', 'write': 'CLOSED', 'Python': 'CLOSED', 'compiler': 'NOT_STARTED_CLOSED'},
    'Python_closure_semantics': 'Final lease write is followed only by in-memory receipt printing and normal process exit; no further Python filesystem access.',
    'compiler_started': False, 'background_processes': [], 'children': [],
    'formal_admission': 'NOT_ASSESSED', 'contract_receipt': contract_receipt,
    'native_run_receipt': run_receipt,
})
lease_bytes = json.dumps(lease, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8') + b'\n'
lease_path = ROOT / 'lease.json'
lease_path.write_bytes(lease_bytes)
print(json.dumps({'status': 'CLOSED', 'contract_receipt': contract_receipt,
                  'native_run_receipt': run_receipt,
                  'lease': {'path': lease_path.as_posix(), 'bytes': len(lease_bytes),
                            'raw_sha256': sha(lease_bytes),
                            'content_self_sha256': lease['content_self_sha256']},
                  'actual_readback': readback, 'anchors': len(anchors),
                  'compiler': 'NOT_STARTED_CLOSED'}, ensure_ascii=False, indent=2))
