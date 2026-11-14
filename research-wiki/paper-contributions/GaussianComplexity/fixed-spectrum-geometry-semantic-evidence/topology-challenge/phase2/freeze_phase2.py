"""Freeze this challenger's independent bounded preproof decision and actual inputs."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import shutil

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
BASE = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-semantic-evidence'
OUT = BASE / 'topology-challenge/phase2'
P1 = BASE / 'topology-challenge/phase1'


def digest(p):
    raw = p.read_bytes()
    return {'path': str(p.relative_to(ROOT)), 'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def dump(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


required = [
    ('preproof-raw-interface-packet.json', '22eb732ccf7f4311f2c099e659e008dd0f87aa855c99f995b65a5132a9752207'),
    ('definition-context-supplement-v1/manifest.json', '5335e7dde540c1035156c98c473f47d00f98f012233c1cfcf23a18d1258fe6fc'),
    ('definition-context-supplement-v1/PiLp-addendum.json', '3457814d7df119ba72109e0557e4908de0b53d458c94adcd39f751534e797f94'),
    ('source-only-review/phase1/source-graph.json', '78a48478d25d53743937c99bc566d0c986e8aea223219ea76ecd3c1ee173755c'),
    ('source-only-review/phase1/source-coverage.json', 'f993e44e2bfca8e928c61eec97ca78947b19d78d054558291c201bc400cce8aa'),
    ('source-only-review/phase1/phase1-freeze.json', '2a8155895c3f7e94113783e329e6c902e055c271adf023fd3edc46b86bd80169'),
    ('source-only-review/phase2/source-graph-v2.proposal.json', 'dc15368281877aeaada92f65e0c116b9e7c42e12ff090c9f297f73ae2c4fcf4f'),
    ('source-only-review/phase2/source-coverage-v2.proposal.json', '3d36214668b2d13f44a35f66a1038244e0110706dd2f429aa88794f11a493466'),
    ('source-only-review/phase2/phase2-freeze.json', 'c78b6cb22364fa09feb8e967abff3a45e9aba95c470c97084c8292e92aacd17e'),
]
actual_inputs = []
copy_dir = OUT / 'raw-inputs'
copy_dir.mkdir(exist_ok=True)
for rel, expected in required:
    p = BASE / rel
    rec = digest(p)
    assert rec['sha256'] == expected, rel
    copy_to = copy_dir / rel.replace('/', '__')
    shutil.copyfile(p, copy_to)
    actual_inputs.append({'original': rec, 'frozen_copy': digest(copy_to)})

packet = json.loads((BASE / 'preproof-raw-interface-packet.json').read_text())
assert sha256(packet['producer']['signature'].encode()).hexdigest() == '832f0009d61ff4f9bb0e568a1350d1c8906b3cf029f6dd130987d6fa1f62281f'
assert sha256(packet['private_consumer']['signature'].encode()).hexdigest() == '1ea7d90b1fd7d19e2d2839e0771f3edba30db262bd6cae7d24b9718aa46c6740'
standard_windows = []
for rec in packet['raw_standard_definition_windows']:
    standard_windows.append(rec['raw_window'])
supplement = json.loads((BASE / 'definition-context-supplement-v1/manifest.json').read_text())
standard_windows.extend(supplement['files'])
standard_windows.append(json.loads((BASE / 'definition-context-supplement-v1/PiLp-addendum.json').read_text())['raw_window'])
for rec in standard_windows:
    p = ROOT / rec['path']
    assert digest(p)['sha256'] == rec['sha256']
    copy_to = copy_dir / p.relative_to(BASE).as_posix().replace('/', '__')
    shutil.copyfile(p, copy_to)
    actual_inputs.append({'original': digest(p), 'frozen_copy': digest(copy_to)})

graph = json.loads((BASE / 'source-only-review/phase2/source-graph-v2.proposal.json').read_text())
coverage = json.loads((BASE / 'source-only-review/phase2/source-coverage-v2.proposal.json').read_text())
gap_nodes = [n for n in graph['nodes'] if n['kind'] == 'SOURCE_GAP']

review = {
    'decision': 'PREPROOF_ADMIT_EXACT_PACKET_TO_BOUNDED_IMPLEMENTATION',
    'source_topology_review': 'ACCEPTED_FOR_REVIEWED_V2_LOCAL_SLICE_WITH_OPEN_INTERNAL_OBLIGATIONS',
    'scope': ['actual S4.SS1/E11 cosine-grid family', 'S4.Thmtheorem6 source dependency context', 'A3.SS4 actual potential geometry', 'S2 fixed-input actual-oracle Borel bridge'],
    'source': digest(P1 / 'raw-source/2610.20492v1.html'),
    'own_pre_interface_source_cognition_manifest': digest(P1 / 'manifest.json'),
    'raw_interface_packet_sha256': required[0][1],
    'producer_signature_sha256': packet['producer']['signature_sha256'],
    'private_consumer_signature_sha256': packet['private_consumer']['signature_sha256'],
    'reviewed_graph': digest(BASE / 'source-only-review/phase2/source-graph-v2.proposal.json'),
    'reviewed_coverage': digest(BASE / 'source-only-review/phase2/source-coverage-v2.proposal.json'),
    'reviewed_extractor_freeze': digest(BASE / 'source-only-review/phase2/phase2-freeze.json'),
    'binder_finding': {'EXCESS': [], 'noEXCESS': True, 'evidence': 'exact-interface-review.json; only source hd/hkappa/full-O inputs plus concrete typing, no project-owned hypothesis bundles'},
    'earlier_holds': [
        {
            'id': 'T01-ACTUAL-ORACLE-IDENTITY',
            'status': 'RESOLVED_IN_ACTUAL_V2',
            'checked_nodes_routes': ['D.oracle', 'S.gradient', 'G.derivatives', 'G.actualoracleidentification', 'R.actualoracleidentification', 'R.oracle-borel'],
            'raw_source_use_site': 'S2.E1 equality between actual first-order pair and numeric pair; consumed at S2.SS0.SSS0.Px2.p1.1.',
            'independent_reason': 'D.oracle now specifies the numeric pair only. R.actualoracleidentification consumes S.gradient and hence G.derivatives; R.oracle-borel separately conjoins numeric continuity with actual-gradient identification. The actual-oracle closure no longer bypasses the open derivative bridge. Numeric-pair continuity remains independent of calculus.',
        },
        {
            'id': 'T02-CONJUGATION-NORM-ORDER',
            'status': 'RESOLVED_IN_ACTUAL_V2',
            'checked_nodes_routes': ['G.conjugation', 'R.conjugation', 'G.orthogonalnorm', 'R.bounds', 'S.bounds'],
            'raw_source_use_site': 'A3.SS4.p1.1: As A=O Lambda O^T with O orthogonal, this gives the Loewner sandwich.',
            'independent_reason': 'G.conjugation states the exact weighted sum and intermediate bounds in ||O^T x||^2 only. R.bounds consumes G.orthogonalnorm before interpreting the ||x||^2 sandwich as Loewner inequalities. No Euclidean norm-identification ingredient is used before its edge.',
        },
    ],
    'independent_topology_assessment': [
        {'branch': 'angle/cosine/eigenvalues/admissibility', 'judgment': 'Correct source direction and inherited parameter scope. Index arithmetic, kappa-1 positivity, symmetry, square orthogonality and quadratic-form interpretation are explicit source-gap obligations. Lemma attribution is not reversed into a premise.'},
        {'branch': 'global C-infinity', 'judgment': 'Polynomial branch depends only on literal finite-dimensional potential and Euclidean carrier. It does not falsely require Haar randomness, positivity, normalizer or main lower-bound ingredients.'},
        {'branch': 'gradient/Hessian', 'judgment': 'Quadratic differentiation consumes symmetry and literal potential; gradient and Hessian are separate source assertions from the common derivative bridge. The exact real Euclidean CLM action agrees with A acting on coordinates.'},
        {'branch': 'strong convexity and smoothness', 'judgment': 'The grouped Hessian-criteria node is a conjunction of two consequences of the source Hessian sandwich, not an AND of alternative routes. Constants and global Euclidean domain are preserved; lower/upper criterion and induced-norm conversion remain internal work.'},
        {'branch': 'origin/global unique minimizer', 'judgment': 'R.zero, R.growth, R.positive and R.unique preserve the actual source direct argument. Backward closure reaches the lower quadratic bound and strict off-origin gap, without calculus or normalizer as false prerequisites.'},
        {'branch': 'actual fixed-input Borel', 'judgment': 'v2 separates numeric continuity from actual-gradient identity and requires both at the Borel use site. Both completion options for numeric continuity remain OR and auditor-attributed; neither is a supplied public hypothesis or claimed author alternative.'},
        {'branch': 'coverage/exclusions', 'judgment': 'Raw source comparison independently matched all 32 units and 120 formula/link atoms, including all selected-region paragraph/theorem/display/math/link membership. v2 changes only the S2.E1 unit and formula node list; raw text/hashes/dispositions/exclusions remain identical. Every substantive C.4 paragraph is represented or explicitly excluded by clause/display.'},
        {'branch': 'external inputs and boundaries', 'judgment': 'The construction citation [22] is provenance, not an invoked C.4 geometry theorem. Normalizer integration, affine-kappa query reduction, Krylov/moment/hardness branches, TV, deterministic caps and expected costs remain explicitly excluded. Full O(d) including determinant -1 is preserved despite excluded probabilistic component laws.'},
    ],
    'phase1_questions_resolution': [
        {'questions': ['Q01','Q12'], 'finding': 'Concrete actual family lets; recursively audited no excess bundles/premises. Proof ingredients remain internal edges.'},
        {'questions': ['Q02','Q03','Q13'], 'finding': 'Full O(d), exact zero-based midpoint shift, d>=2/kappa>=2, no main-theorem parameter leakage.'},
        {'questions': ['Q04','Q05','Q06','Q07'], 'finding': 'Global real Frechet Hessian via Euclidean gradient; exact CLM A action; half-factor strong convexity; actual Euclidean gradient norm constant kappa.'},
        {'questions': ['Q08','Q15'], 'finding': 'Global origin existence and uniqueness via IsMinOn biconditional. Literal potential/oracle, no fallback, shift, chosen eigenbasis or characterized minimizer.'},
        {'questions': ['Q09'], 'finding': 'Private literal same-A fixed-input Borel statement accepted; genuine producer use and actual gradient identification must still be demonstrated by implementation.'},
        {'questions': ['Q10','Q11','Q14'], 'finding': 'Actual v2 node/route/use-site and coverage records inspected against source; both initial graph holds resolved, alternatives OR, all local/main/TV/cap/cost boundaries preserved.'},
    ],
    'open_internal_source_obligations': [
        {'id': n['id'], 'statement': n['statement'], 'status': 'NOT_DISCHARGED_BY_THIS_PREPROOF_REVIEW', 'source_anchors': n['source_anchors']}
        for n in gap_nodes
    ],
    'implementation_admission_requirements': [
        'Implement exactly producer signature 832f0009... and private consumer signature 1ea7d90b..., with the same literal definitions and standard constant resolution; do not add scoped or public convenience assumptions.',
        'Discharge the actual derivative, quadratic-bound, norm, convexity, origin/minimizer and Borel identity obligations internally by checked source-compatible dependencies. This review neither asserts them newly proved nor determines which existing compiled parents may be reused.',
        'The private test must actually call the producer and use its regularity result for the same f before pairing with the same A-query. A nominal test name or independently reproved numeric-pair theorem is not evidence of that consumer dependency.',
        'Keep the actual gradient-query identity internal and mapped to the source graph. The private measurable numeric response has actual-first-order meaning only after that identity is discharged.',
        'After implementation, perform the normal focused Lean, axiom/fake-closure, source/semantic round-trip, whole-module and publication checks. No such result is supplied by this review.',
    ],
    'nonclaims': [
        'No Lean proof, build, compiler truth, axiom audit, VERIFIED transition, SAU claim, source-V or full-module source-fidelity verdict.',
        'No current production implementation or existing Gaussian proof module was read. Open source-gap markers remain open in this preproof evidence.',
        'No new normalizer proof, source-wide completion, query lower bound, TV transfer, adaptive transcript/output theorem, joint-in-O measurability, deterministic-cap composition or expected-cost conclusion.',
    ],
    'decision_basis': 'Independent source cognition was frozen before interfaces; actual raw interface/18 standard windows and actual v1/v2 graph/coverage were reviewed. The extractor private rationale/exact-interface proposal and root full seal/classifications/reuse rationale were not read. The final decision is independent of their summaries and is bounded to statement/source-topology admission for implementation.',
}
dump(OUT / 'final-review.json', review)

exposure = {
    'phase': 'phase2',
    'role': 'different-role source-topology/binder/definition/consumer challenger',
    'own_pre_interface_phase1_manifest': digest(P1 / 'manifest.json'),
    'actual_inputs': actual_inputs,
    'additional_source_access': [digest(ROOT / '.astis/huanjian-resume-20261103/2610.20492v1.html'), digest(P1 / 'independent-expectations.json')],
    'standard_window_verification': 'Read authorized window bytes, hashed their upstream whole files and compared exact pinned line slices without displaying/searching other upstream contents. The supplied Euclidean-norm/action windows include short generic theorem proof lines; no target proof/API search occurred.',
    'root_messages': 'Parent supplied hashes, scope, progress, and summaries of proposed changes. Actual files and source use-site semantics were independently inspected before final judgment; summaries were not treated as acceptance evidence.',
    'unread': ['root full statement seal', 'root exposure/classification/reuse rationale', 'root private preseal rationale', 'extractor phase1 initial cognition/private rationale', 'extractor exact-interface-admission.proposal.json', 'Gaussian implementation Lean or proof capsules', 'source-V/full-module review material'],
    'local_check_note': 'Independent HTMLParser helper first failed because a method name collided with an existing integer offset attribute; renamed the helper and reran successfully. This was a local checking-script implementation failure, not negative mathematical evidence.',
    'prohibited_actions_performed': [],
    'no_extra_agents': True,
    'no_build_browser_network_remote_ATLAS_model_or_canonical_mutation': True,
}
dump(OUT / 'exposure.json', exposure)

capsule = '''# Independent phase 2 bounded preproof admission

Decision: **admit the unchanged exact packet to bounded implementation**. The reviewed v2 source topology/coverage is accepted for this local slice with all internal proof obligations still explicit. No Lean proof, SAU/VERIFIED transition, source-V, whole-module source verdict, or source result completion is certified.

This judgment binds producer signature `832f0009d61ff4f9bb0e568a1350d1c8906b3cf029f6dd130987d6fa1f62281f`, private consumer signature `1ea7d90b1fd7d19e2d2839e0771f3edba30db262bd6cae7d24b9718aa46c6740`, raw packet `22eb732ccf7f4311f2c099e659e008dd0f87aa855c99f995b65a5132a9752207`, actual graph v2 `dc15368281877aeaada92f65e0c116b9e7c42e12ff090c9f297f73ae2c4fcf4f`, and coverage v2 `3d36214668b2d13f44a35f66a1038244e0110706dd2f429aa88794f11a493466`. Independent source cognition was frozen first under manifest `da6e262c62c354086cd9439e25795b4ab08c521d864165812a8a6226778eeeb4`.

No EXCESS binder was found: dimension and real scalar carriers are typing; d>=2 and kappa>=2 are inherited source conditions; O is any element of full real O(d), including determinant -1. All actual objects are literal lets. The midpoint grid has the correct zero-based half shift. The potential is exactly dot(x,A*x)/2 on all Euclidean R^d, with no fallback or additive shift. The real Frechet derivative of its Euclidean gradient, using the exact CLM action A*x, faithfully expresses the pointwise Hessian. Raw strong convexity unfolds to modulus r^2/2; smoothness is the actual Euclidean gradient norm bound with constant kappa. The global minimizer biconditional includes both existence at zero and uniqueness.

I challenged two defects in the original graph before accepting the successor. The actual-oracle Borel closure initially bypassed the open gradient identity. v2 now makes the numeric definition separate and has the actual identification consume S.gradient/G.derivatives before Borel interpretation. The conjugation node initially blurred when norm preservation was used. v2 retains the intermediate bounds in ||O^T x|| and consumes orthogonal norm preservation at R.bounds. Both resolutions were checked in actual node/edge/use-site records against Eq. (1) and C.4, rather than accepted from a summary. Originals and the initial HOLD questions remain preserved.

All 32 source units and 120 formula/link atoms match the pinned raw HTML, including independently reconstructed selected-region membership. v2 changes only the Eq. (1) node mapping; source bytes, dispositions and exclusions are unchanged. Polynomial smoothness, derivative/Hessian, lower-bound minimizer and fixed-input Borel branches remain distinct. The numeric continuity options are explicit OR alternatives. The normalizer paragraph, query equivalence, main lower bound, Haar component laws, TV, deterministic caps and expected costs are represented as context or explicitly excluded without narrowing deterministic full-O conclusions.

Eleven source-gap/adapter obligations remain unproved by this review: grid arithmetic, symmetry, orthogonal isometry, conjugated quadratic bounds, class membership, polynomial regularity, actual derivatives, Hessian criteria, numeric continuity, actual-oracle identification and Borel conversion. Implementation may reuse checked source-compatible parents, but cannot move these conclusions into public premises. The private consumer must actually use the producer for the same f and pair it with the same A-query; its signature alone does not demonstrate genuine producer consumption. Actual gradient=query must also be discharged internally.

`final-review.json` records all semantic slots, challenge resolutions, phase-1 question resolutions, exact input references and remaining obligations. Eighteen raw standard windows match their pinned upstream full-file hashes and exact line slices. `exposure.json` records the actual inputs and allowed generic definition/action lines. Root full seal/classifications/private rationale, extractor private rationale/interface-admission proposal, target implementation and prior verdicts were not opened. Stop after freeze; further implementation and normal independent postproof gates belong to the owner.
'''
(OUT / 'phase2-capsule.md').write_text(capsule)
dump(OUT / 'phase2-freeze.json', {
    'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
    'decision': review['decision'],
    'source_topology_review': review['source_topology_review'],
    'producer_signature_sha256': packet['producer']['signature_sha256'],
    'private_consumer_signature_sha256': packet['private_consumer']['signature_sha256'],
    'source_graph_sha256': required[6][1],
    'source_coverage_sha256': required[7][1],
    'noEXCESS': True,
    'open_internal_obligations': [n['id'] for n in gap_nodes],
    'no_proof_or_VERIFIED_claim': True,
    'stop': True,
})
files = [digest(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in {'manifest.json', 'manifest.sha256'}]
dump(OUT / 'manifest.json', {'schema': 1, 'phase': 'independent-phase2-exact-interface-and-source-topology-preproof-review', 'files': files, 'self_hash_policy': 'Manifest excludes itself and its detached digest.'})
(OUT / 'manifest.sha256').write_text(sha256((OUT / 'manifest.json').read_bytes()).hexdigest() + '  manifest.json\n')
for name in ['phase2-capsule.md','final-review.json','phase2-freeze.json','manifest.json']:
    print(json.dumps(digest(OUT / name), ensure_ascii=False))
