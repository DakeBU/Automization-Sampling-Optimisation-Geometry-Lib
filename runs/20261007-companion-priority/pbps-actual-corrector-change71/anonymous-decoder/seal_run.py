import hashlib
import json
import os
import pathlib
import re

OUT = pathlib.Path('E:/Samplinglib/.astis/decoder-71/independent')
BASE = OUT.parent
DECODER = 'anonymous-independent-decoder-71'
PID = os.getpid()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def serialized(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2).encode('utf-8') + b'\n'


def write_new(name, raw):
    with (OUT / name).open('xb') as handle:
        handle.write(raw)


expected_initial = {
    'packet0.json.raw.sealed', 'lease.open.json.raw.sealed',
    'input-payload.json', 'reconstruction.utf8.txt', 'seal_run.py'
}
assert {p.name for p in OUT.iterdir()} == expected_initial
payload_raw = (OUT / 'input-payload.json').read_bytes()
payload = json.loads(payload_raw)
packet_raw = (OUT / 'packet0.json.raw.sealed').read_bytes()
lease_input_raw = (OUT / 'lease.open.json.raw.sealed').read_bytes()
assert sha(packet_raw) == '782cfb7c81a54acc94392f0a6557a78b7654c8080b3a9fa1d16daadb51ef69bb'
assert sha(lease_input_raw) == '29f767902728ae065609488dad637434d1c9d2094bb40a7817e0026442e94157'
assert packet_raw == (BASE / 'packet0.json').read_bytes()
assert lease_input_raw == (BASE / 'lease.open.json').read_bytes()
packet = json.loads(packet_raw.decode('utf-8-sig'))
lease_input = json.loads(lease_input_raw.decode('utf-8-sig'))
assert lease_input['status'] == 'OPEN'
assert lease_input['source_text_visible'] is False
assert lease_input['search_or_compiler_allowed'] is False
assert payload['packet_sha256'] == sha(canonical(packet))
assert payload['packet_sha256'] == 'b40612aa42fec0d1ccecc0780f358189c4930ff0fb9f76dc113f72cd8c17906a'
assert sha(packet['lean']['statement'].encode('utf-8')) == packet['lean']['statement_sha256']
context = packet['lean']['approved_definition_context']
assert len(context) == 12
assert payload['approved_definition_context_canonical_sha256'] == sha(canonical(context))
for entry, value in zip(payload['approved_definition_context_item_sha256'], context):
    assert entry['utf8_sha256'] == sha(value.encode('utf-8'))

reconstruction_raw = (OUT / 'reconstruction.utf8.txt').read_bytes()
assert not reconstruction_raw.startswith(b'\xef\xbb\xbf')
assert b'\r' not in reconstruction_raw
assert reconstruction_raw.endswith(b'\n')
reconstruction = reconstruction_raw.decode('utf-8')
matches = list(re.finditer(r'(?m)^\[(\d{2})\] ', reconstruction))
assert [m.group(1) for m in matches] == [f'{i:02d}' for i in range(51)]
slot_text = {}
for index, match in enumerate(matches):
    stop = matches[index + 1].start() if index + 1 < len(matches) else len(reconstruction)
    slot_text[match.group(1)] = reconstruction[match.start():stop].strip()

decisions = [
    ('00', 'ambient-input', 'Finite-dimensional real Hilbert-type ambient space with Borel measurable structure; V, nonnegative alpha/beta and real eta are input data.'),
    ('01', 'caller-condition', 'Strict positivity is on the real coercion of alpha.'),
    ('02', 'caller-condition', 'The nonnegative parameters satisfy alpha <= beta; this is distinct from either Hessian bound.'),
    ('03', 'caller-condition', 'Global C2 Frechet regularity; no extra derivatives or local domain.'),
    ('04', 'caller-condition', 'One universally quantified x,v pair carries the conjunction of lower and upper Hessian quadratic-form bounds.'),
    ('05', 'caller-condition', 'Strict positivity of eta is a public input condition.'),
    ('06', 'caller-condition', 'The exact upper product constraint is beta*eta <= 1.'),
    ('07', 'scope-decision', 'Only the first six named condition binders are caller premises. Every later existential and all internal instances are concluded or defined.'),
    ('08', 'internal-measure-definition', 'tilted is normalized exponential tilt; the probability property is subsequently concluded.'),
    ('09', 'internal-joint-definition', 'The input to the pushforward is (X,Z); its output is (X,X+sqrt(eta)Z), and nu is the second marginal.'),
    ('10', 'internal-map-definitions', 'Lambda uses (x,y)->(y,2x-y), while F uses (x,y)->(x,2x-y). Keep the distinct first coordinates.'),
    ('11', 'internal-subspace-definition', 'HP is the closed sigma(Y)-measurable subspace of joint L2, with internally derived sigma-algebra inclusion.'),
    ('12', 'internal-operator-definitions', 'condExpL2 lands in HP; P includes it into H. M is the actual measure-preserving second-coordinate pullback.'),
    ('13', 'global-conclusion', 'Three probabilities, exact range equality, and pointwise-in-HP operator fixedness are simultaneous conclusions.'),
    ('14', 'global-witness-and-conclusion', 'S is a produced Markov kernel with every-state equality of normalized measures and exact V((y+x)/2), 8*eta constants.'),
    ('15', 'global-conclusion', 'S disintegrates Lambda in its second coordinate given its first; both Lambda marginals are the same nu.'),
    ('16', 'global-witness-and-conclusion', 'e is onto HP and its inclusion agrees exactly in Lp with M. Use this very e for every subsequent conjugation.'),
    ('17', 'global-witness-and-conclusion', 'U is a produced joint linear isometry, an involution, and selfadjoint; its action is observable-wise J-AE pullback by F.'),
    ('18', 'global-witness-and-conclusion', 'One selfadjoint T contracts every K observable, realizes the same S nu-AE, and preserves its nu integral.'),
    ('19', 'internal-operator-definitions', 'A compresses U to HP; B has domain HP and ambient codomain H, retaining the exact (I-P)UP factorization.'),
    ('20', 'global-conclusion', 'A equals eTe^-1 and is a selfadjoint contraction on all HP.'),
    ('21', 'global-conclusion', 'PBf=0 is proved for every HP input; it does not change the declared codomain of B.'),
    ('22', 'global-witness-and-conclusion', 'Gamma is positive, squares to I-T*T, and commutes with T; it is not supplied by the caller.'),
    ('23', 'internal-definition-and-conclusions', 'GammaP uses the same conjugation, with transported positivity/root/commutation and exact B*B=GammaP^2.'),
    ('24', 'global-witness-and-conclusion', 'q is the produced nu-AE constant one, is fixed by T, and represents the integral pairing for all K.'),
    ('25', 'internal-subspace-definition', 'qP=e q; HP0 is the kernel of inner(qP,-) inside HP, with inherited complete Hilbert structures.'),
    ('26', 'global-conclusion', 'Centering is exactly the zero nu integral of e^-1 f, for every f in HP.'),
    ('27', 'internal-constant-and-conclusions', 'GammaP kills qP; gamma is exactly 2*sqrt(alpha*eta)/(1+alpha*eta) and is strictly positive.'),
    ('28', 'global-witness-and-conclusion', 'GammaP0 is the same-root restriction to HP0; positivity, lower bound by gamma I, and being a unit are concluded.'),
    ('29', 'global-witness-and-conclusion', 'Inv is one bounded, selfadjoint two-sided inverse of that GammaP0, with operator norm <=1/gamma.'),
    ('30', 'global-witness-and-conclusion', 'A0 is the same-A restriction; its selfadjointness, root commutation, square-sum identity and inverse commutation are concluded.'),
    ('31', 'internal-subspace-definition', 'Hperp means ker P, not the global zero-mean space; closed-kernel completeness is internal.'),
    ('32', 'global-witness-and-conclusion', 'B0 restricts B to centered HP0 inputs and has exact codomain Hperp.'),
    ('33', 'global-witness-and-conclusion', 'V0 uses B0 and the already produced Inv, and factors the same B0 through the same GammaP0.'),
    ('34', 'global-conclusion', 'V0*V0=I and norm preservation give an isometry into Hperp; do not infer a claimed onto property or reverse product.'),
    ('35', 'global-witness-and-conclusion', 'R has all H as domain and ker P as codomain, with inclusion Rg=g-Pg.'),
    ('36', 'global-conclusion', 'The ambient adjoint B*:H->HP is recovered as i0 B0* R for every joint input.'),
    ('37', 'internal-definition-and-conclusion', 'D=R U iPerp is the residual compression of the same U; its ambient action subtracts P after applying U.'),
    ('38', 'global-conclusion', 'The exact negative adjoint intertwining is V0* D= -A0 V0* on every Hperp input, not only the V0 range.'),
    ('39', 'local-premise-and-produced-witness', 'The final implication quantifies all f in H with zero J integral and produces fP in HP0 as its actual conditional component.'),
    ('40', 'local-definitions-and-conclusions', 'fperp=Rf and fV=V0* fperp; both adjoint/root inclusion equations refer to these actual objects.'),
    ('41', 'local-conclusions', 'Pythagoras retains ||fperp||^2, while the separate contraction uses ||fV||<=||fperp||.'),
    ('42', 'local-definition-and-conclusion', 'g is exactly U(Pf-(f-Pf)); zero J integral of g is concluded from centered f, not assumed.'),
    ('43', 'local-produced-witness-and-definitions', 'gP is the actual conditional component of g; gperp=Rg and gV=V0* gperp are actual residual constructions.'),
    ('44', 'local-conclusions', 'The two update equations have minus GammaP0 fV in gP and plus A0 fV in gV; neither output is defined by these equations.'),
    ('45', 'local-conclusion', 'The conserved pair norm uses macro and V0-adjoint corrector components, not the whole conditional complement.'),
    ('46', 'local-functional-definition-and-conclusion', 'C=(||u||^2-||v||^2)/2-inner(A0(Inv u),v); its output-minus-input difference is exactly -||fP||^2+||fV||^2.'),
    ('47', 'existential-scope-decision', 'Twelve common outer existential witnesses precede all final inputs; fP and gP are the two input-local witnesses.'),
    ('48', 'quantifier-decision', 'Every-state kernel equality and whole-domain operator identities are stronger than the explicitly per-observable AE representative formulas.'),
    ('49', 'domain-and-mean-decision', 'nu centers observable classes; J centers joint inputs/outputs; HP0 and ker P remain distinct; adjoint domains and inclusions are preserved.'),
    ('50', 'verification-boundary', 'No unresolved semantic slot. The compiled input flag is unverified metadata here; no body, source or fidelity assessment was consulted.')
]
assert [item[0] for item in decisions] == [f'{i:02d}' for i in range(51)]
slot_records = [
    {'slot': sid, 'role': role, 'resolved': True, 'decision': decision,
     'reconstructed_slot_text': slot_text[sid], 'unresolved': []}
    for sid, role, decision in decisions
]
decision_object = {
    'schema_version': 1,
    'decoder': DECODER,
    'packet_sha256': payload['packet_sha256'],
    'reconstructed_text_sha256': sha(reconstruction_raw),
    'source_text_visible': False,
    'source_identity_visible': False,
    'proof_BODY_visible': False,
    'slot_count': 51,
    'caller_condition_count': 6,
    'common_existential_witness_count': 12,
    'input_local_existential_witness_count': 2,
    'existential_witness_count': 14,
    'unresolved_count': 0,
    'unresolved': [],
    'slots': slot_records
}
decision_raw = serialized(decision_object)
write_new('slot-decisions.json', decision_raw)

context_hashes = {
    'list_canonical_sha256': payload['approved_definition_context_canonical_sha256'],
    'item_utf8_sha256': payload['approved_definition_context_item_sha256']
}
run = {
    'schema_version': 1,
    'decoder': DECODER,
    'writer_actual_pid': PID,
    'freeze_actual_pid': payload['freeze_pid'],
    'source_text_visible': False,
    'source_identity_visible': False,
    'proof_BODY_visible': False,
    'search_performed': False,
    'compiler_invoked': False,
    'external_source_used': False,
    'input_artifacts': payload['input_artifacts'],
    'packet_sha256': payload['packet_sha256'],
    'packet_hash_rule': payload['packet_hash_rule'],
    'approved_definition_context_hashes': context_hashes,
    'lean_statement_utf8_sha256': payload['lean_statement_utf8_sha256'],
    'reconstruction_file': 'reconstruction.utf8.txt',
    'reconstructed_text_sha256': sha(reconstruction_raw),
    'decision_file': 'slot-decisions.json',
    'decision_raw_sha256': sha(decision_raw),
    'input_payload_file': 'input-payload.json',
    'input_payload_raw_sha256': sha(payload_raw),
    'slot_count': 51,
    'caller_condition_count': 6,
    'common_existential_witness_count': 12,
    'input_local_existential_witness_count': 2,
    'unresolved_count': 0,
    'run_hash_rule': 'SHA256 of UTF-8 canonical JSON of this exact run object after deleting ONLY its top-level run_sha256 key; sort_keys=True; separators=(comma,colon); ensure_ascii=False.',
    'no_self_referential_output_hash': True,
    'closure_protocol': 'Write CLOSED_LAST lease after every other owned file; afterward only a separate read-only verification may inspect owned files.',
    'intended_success_exit_code': 0
}
run_hash = sha(canonical(run))
run['run_sha256'] = run_hash
run_raw = serialized(run)
write_new('decoder-run.json', run_raw)
sealed_run = json.loads((OUT / 'decoder-run.json').read_bytes())
assert sealed_run.pop('run_sha256') == run_hash
assert sha(canonical(sealed_run)) == run_hash

global_witnesses = [
    {'name': 'S', 'type': 'Markov kernel E -> E', 'scope': 'common outer existential'},
    {'name': 'e', 'type': 'real-linear isometric equivalence K -> HP', 'scope': 'common outer existential'},
    {'name': 'U', 'type': 'real-linear isometry H -> H', 'scope': 'common outer existential'},
    {'name': 'T', 'type': 'bounded real-linear endomorphism of K', 'scope': 'common outer existential'},
    {'name': 'Gamma', 'type': 'bounded real-linear endomorphism of K', 'scope': 'common outer existential'},
    {'name': 'q', 'type': 'K', 'scope': 'common outer existential'},
    {'name': 'GammaP0', 'type': 'bounded real-linear endomorphism of HP0', 'scope': 'common outer existential'},
    {'name': 'Inv', 'type': 'bounded real-linear endomorphism of HP0', 'scope': 'common outer existential'},
    {'name': 'A0', 'type': 'bounded real-linear endomorphism of HP0', 'scope': 'common outer existential'},
    {'name': 'B0', 'type': 'bounded real-linear map HP0 -> Hperp', 'scope': 'common outer existential'},
    {'name': 'V0', 'type': 'bounded real-linear map HP0 -> Hperp', 'scope': 'common outer existential'},
    {'name': 'R', 'type': 'bounded real-linear map H -> Hperp', 'scope': 'common outer existential'}
]
local_witnesses = [
    {'name': 'fP', 'type': 'HP0', 'scope': 'for each f in H with integral_J f=0', 'identification': 'i0 fP = EY f'},
    {'name': 'gP', 'type': 'HP0', 'scope': 'inside that same centered-input conclusion, after g=U(Pf-(f-Pf))', 'identification': 'i0 gP = EY g'}
]
objects = [
    {'name': 'E', 'type': 'finite-dimensional real inner product space with Borel measurable structure', 'status': 'ambient input'},
    {'name': 'V', 'type': 'E -> R', 'status': 'input function'},
    {'name': 'alpha,beta', 'type': 'nonnegative real parameters', 'status': 'input parameters'},
    {'name': 'eta', 'type': 'real parameter', 'status': 'input parameter'},
    {'name': 'mu', 'type': 'Measure E', 'definition': 'volume.tilted(-V)'},
    {'name': 'J', 'type': 'Measure (E product E)', 'definition': 'pushforward of mu product stdGaussian by (x,z)->(x,x+sqrt(eta)z)'},
    {'name': 'nu', 'type': 'Measure E', 'definition': 'J.snd'},
    {'name': 'Lambda', 'type': 'Measure (E product E)', 'definition': 'J.map((x,y)->(y,2x-y))'},
    {'name': 'F', 'type': '(E product E) -> (E product E)', 'definition': '(x,y)->(x,2x-y)'},
    {'name': 'mY', 'type': 'measurable sub-sigma-algebra on E product E', 'definition': 'comap of the second projection'},
    {'name': 'H', 'type': 'real Hilbert space', 'definition': 'Lp R 2 J'},
    {'name': 'K', 'type': 'real Hilbert space', 'definition': 'Lp R 2 nu'},
    {'name': 'HP', 'type': 'closed Hilbert subspace of H', 'definition': 'lpMeas R R mY 2 J'},
    {'name': 'EY', 'type': 'bounded real-linear map H -> HP', 'definition': 'displayed condExpL2 under J'},
    {'name': 'P', 'type': 'bounded real-linear endomorphism of H', 'definition': 'HP inclusion composed with EY'},
    {'name': 'hp', 'type': 'MeasurePreserving Prod.snd J nu', 'definition': 'internally assembled from measurability and the definition nu=J.snd'},
    {'name': 'M', 'type': 'real-linear isometry K -> H', 'definition': 'pullback by Prod.snd using hp'},
    {'name': 'A', 'type': 'bounded real-linear endomorphism of HP', 'definition': 'orthogonalProjectionOnto HP composed with U composed with HP inclusion'},
    {'name': 'B', 'type': 'bounded real-linear map HP -> H', 'definition': '(I_H-P) U P composed with HP inclusion'},
    {'name': 'GammaP', 'type': 'bounded real-linear endomorphism of HP', 'definition': 'e Gamma e^-1'},
    {'name': 'qP', 'type': 'HP', 'definition': 'e q'},
    {'name': 'HP0', 'type': 'closed complete Hilbert subspace of HP', 'definition': 'ker inner(qP,-)'},
    {'name': 'gamma', 'type': 'real number', 'definition': '2 sqrt(alpha eta)/(1+alpha eta)'},
    {'name': 'Hperp', 'type': 'closed complete Hilbert subspace of H', 'definition': 'ker P'},
    {'name': 'D', 'type': 'bounded real-linear endomorphism of Hperp', 'definition': 'R composed with U composed with Hperp inclusion'},
    {'name': 'f', 'type': 'H', 'status': 'arbitrary final universally quantified input with integral_J f=0'},
    {'name': 'fperp', 'type': 'Hperp', 'definition': 'R f'},
    {'name': 'fV', 'type': 'HP0', 'definition': 'V0.adjoint fperp'},
    {'name': 'g', 'type': 'H', 'definition': 'U(P f-(f-P f))'},
    {'name': 'gperp', 'type': 'Hperp', 'definition': 'R g'},
    {'name': 'gV', 'type': 'HP0', 'definition': 'V0.adjoint gperp'},
    {'name': 'C', 'type': 'HP0 -> HP0 -> R', 'definition': '(||u||^2-||v||^2)/2-inner_R(A0(Inv u),v)'}
] + global_witnesses + local_witnesses
assert len(global_witnesses) == 12 and len(local_witnesses) == 2
conclusion_start = reconstruction.index('[08] ')
conclusion_stop = reconstruction.index('[47] ')
decoded = {
    'schema_version': 1,
    'decoder': DECODER,
    'decoder_run_sha256': run_hash,
    'decoder_run_file': 'decoder-run.json',
    'decoder_run_hash_rule': run['run_hash_rule'],
    'packet_sha256': payload['packet_sha256'],
    'packet_hash_rule': payload['packet_hash_rule'],
    'embedded_packet_sha256': payload['embedded_packet_sha256'],
    'embedded_packet_field_is_not_the_computed_digest': True,
    'source_text_visible': False,
    'source_identity_visible': False,
    'proof_BODY_visible': False,
    'source_fidelity_assessed': False,
    'input_artifacts': payload['input_artifacts'],
    'approved_definition_context_hashes': context_hashes,
    'approved_definition_context': context,
    'input_statement_utf8_sha256': payload['lean_statement_utf8_sha256'],
    'compiled_flag_as_supplied_metadata': packet['lean']['compiled'],
    'compiler_invoked': False,
    'search_performed': False,
    'reconstructed_theorem_text': reconstruction,
    'reconstructed_text_sha256': sha(reconstruction_raw),
    'text_sha256': sha(reconstruction_raw),
    'text_hash_rule': 'SHA256 of exact reconstruction.utf8.txt UTF-8 bytes; no BOM, LF newlines, final LF included.',
    'objects': objects,
    'domains': {
        'measure_domains': {'mu': 'E', 'J': 'E product E', 'nu': 'E', 'Lambda': 'E product E', 'S(y)': 'E'},
        'H': 'real joint L2(J)',
        'K': 'real observable L2(nu)',
        'HP': 'closed sigma(Y)-measurable subspace of H',
        'HP0': 'ker inner(qP,-) inside HP; exactly zero nu integral after e^-1',
        'Hperp': 'ker P inside H; zero conditional expectation, not merely zero global integral',
        'ambient_adjoint': 'B.adjoint : H -> HP',
        'intrinsic_adjoints': 'B0.adjoint,V0.adjoint : Hperp -> HP0',
        'whole_domain_intertwining': 'V0.adjoint D = -A0 V0.adjoint : Hperp -> HP0',
        'functional': 'C : HP0 -> HP0 -> R'
    },
    'quantifiers': {
        'ambient_data': 'for every E,V,alpha,beta,eta with the displayed structures and six caller conditions',
        'caller_conditions': [slot_text[f'{i:02d}'] for i in range(1,7)],
        'common_outer_existentials_in_order': global_witnesses,
        'local_existentials_in_order': local_witnesses,
        'final_universal_and_implication': 'for every f in H, integral_J f=0 implies the full construction and all conclusions in slots 39-46',
        'per_observable_AE': ['for each g in H: Ug=g composed F, J-AE', 'for each u in K: Tu(y)=integral u dS(y), nu-AE', 'q=1, nu-AE'],
        'every_state': 'for all y in E, S(y) is the displayed normalized tilted measure'
    },
    'assumptions': [
        {'name': 'h_alpha', 'slot': '01', 'statement': '0 < alpha'},
        {'name': 'h_alpha_beta', 'slot': '02', 'statement': 'alpha <= beta'},
        {'name': 'h_V', 'slot': '03', 'statement': 'ContDiff R 2 V'},
        {'name': 'h_H', 'slot': '04', 'statement': 'for all x,v: alpha ||v||^2 <= ((D(DV)(x))(v))(v) and ((D(DV)(x))(v))(v) <= beta ||v||^2'},
        {'name': 'h_eta', 'slot': '05', 'statement': '0 < eta'},
        {'name': 'h_beta_eta', 'slot': '06', 'statement': 'beta eta <= 1'}
    ],
    'conclusion': reconstruction[conclusion_start:conclusion_stop].strip(),
    'scopes': {
        'common_data': 'one nested existential choice of S,e,U,T,Gamma,q,GammaP0,Inv,A0,B0,V0,R satisfies every global and final-input conclusion',
        'same_inverse': 'Inv is both-sided inverse of the same GammaP0 and is reused in V0 and C',
        'local_data': 'fP is inside the centered f implication; gP is inside that same implication after actual g is formed',
        'output_components': 'gP is identified by EY g and gV by V0.adjoint(R g); update equations are conclusions about them',
        'internal_structures': 'measurable inclusion Fact and inherited closed-kernel complete Hilbert structures are internally supplied',
        'non_surjectivity_boundary': 'V0 is an isometry into Hperp; no onto or V0 V0.adjoint=I assertion',
        'conditional_boundary': 'Hperp=ker P is distinct from the global centered-input hypothesis integral_J f=0'
    },
    'constant_dependencies': {
        'joint_scale': 'sqrt(eta)',
        'reflection': '2x-y',
        'kernel_midpoint': '(y+x)/2',
        'kernel_quadratic_denominator': '8 eta',
        'gamma': '2 sqrt(alpha eta)/(1+alpha eta)',
        'inverse_norm_bound': '1/gamma',
        'functional_norm_coefficient': '1/2',
        'functional_inner_coefficient': '-1',
        'functional_difference_rhs': '-1*||fP||^2 + 1*||fV||^2'
    },
    'final_functional_identity': {
        'domain': 'HP0 product HP0',
        'definition': 'C(u,v)=(||u||^2-||v||^2)/2-inner_R(A0(Inv u),v)',
        'identity': 'C(gP,gV)-C(fP,fV)=-||fP||^2+||fV||^2',
        'scope': 'every f in H with integral_J f=0, for its actual conditional and residual-corrector input/output components',
        'construction_is_not_an_extra_hypothesis': True
    },
    'slot_decisions_file': 'slot-decisions.json',
    'slot_decisions_raw_sha256': sha(decision_raw),
    'slot_count': 51,
    'caller_condition_count': 6,
    'common_existential_witness_count': 12,
    'input_local_existential_witness_count': 2,
    'existential_witness_count': 14,
    'approved_definition_context_count': len(context),
    'unresolved': [],
    'unresolved_count': 0
}
decoded_raw = serialized(decoded)
write_new('decoded0.json', decoded_raw)

pre_manifest_names = expected_initial | {'slot-decisions.json', 'decoder-run.json', 'decoded0.json'}
assert {p.name for p in OUT.iterdir()} == pre_manifest_names
entries = []
for name in sorted(pre_manifest_names):
    raw = (OUT / name).read_bytes()
    entries.append({'name': name, 'byte_count': len(raw), 'raw_sha256': sha(raw)})
assert len(entries) == 8
manifest = {
    'schema_version': 1,
    'decoder': DECODER,
    'writer_actual_pid': PID,
    'input_payload': 'input-payload.json',
    'complete_reconstruction': 'reconstruction.utf8.txt',
    'complete_slot_decisions': 'slot-decisions.json',
    'complete_decoded_payload': 'decoded0.json',
    'sealed_run': 'decoder-run.json',
    'closure_lease': 'lease.closed.json',
    'packet_sha256': payload['packet_sha256'],
    'packet_raw_sha256': sha(packet_raw),
    'packet_lf_only_sha256': sha(packet_raw.replace(b'\r\n',b'\n')),
    'reconstructed_text_sha256': sha(reconstruction_raw),
    'decoder_run_sha256': run_hash,
    'decoder_run_raw_sha256': sha(run_raw),
    'decision_raw_sha256': sha(decision_raw),
    'decoded_raw_sha256': sha(decoded_raw),
    'input_payload_raw_sha256': sha(payload_raw),
    'approved_definition_context_hashes': context_hashes,
    'source_text_visible': False,
    'source_identity_visible': False,
    'proof_BODY_visible': False,
    'source_fidelity_assessed': False,
    'slot_count': 51,
    'caller_condition_count': 6,
    'common_existential_witness_count': 12,
    'input_local_existential_witness_count': 2,
    'existential_witness_count': 14,
    'approved_definition_context_count': 12,
    'unresolved_count': 0,
    'input_file_count': 2,
    'manifest_entry_count': 8,
    'owned_file_count_including_closure_lease': 10,
    'closure_covered_file_count_excluding_lease': 9,
    'files': entries,
    'hash_chain': 'CLOSED_LAST lease covers every owned file other than itself, including this manifest; manifest covers eight payload/script files. Run hash removes only top-level run_sha256, and run contains no hash of decoded0 or manifest.'
}
manifest_raw = serialized(manifest)
write_new('manifest.json', manifest_raw)
covered_names = pre_manifest_names | {'manifest.json'}
assert {p.name for p in OUT.iterdir()} == covered_names
covered = []
for name in sorted(covered_names):
    raw = (OUT / name).read_bytes()
    covered.append({'name': name, 'byte_count': len(raw), 'raw_sha256': sha(raw)})
assert len(covered) == 9
closed = {
    'schema_version': 1,
    'status': 'CLOSED_LAST',
    'decoder': DECODER,
    'writer_actual_pid': PID,
    'last_owned_write': True,
    'lease_name': 'lease.closed.json',
    'owned_directory': str(OUT),
    'source_text_visible': False,
    'packet_sha256': payload['packet_sha256'],
    'decoder_run_sha256': run_hash,
    'manifest_raw_sha256': sha(manifest_raw),
    'covered_file_count': 9,
    'owned_file_count_including_lease': 10,
    'covered_files': covered,
    'excluded_file': 'lease.closed.json',
    'post_close_policy': 'No subsequent owned writes; only separate external read-only verification and reporting.'
}
closed_raw = serialized(closed)
summary = {
    'writer_actual_pid': PID,
    'status': 'CLOSED_LAST',
    'packet_sha256': payload['packet_sha256'],
    'reconstructed_text_sha256': sha(reconstruction_raw),
    'decoder_run_sha256': run_hash,
    'manifest_raw_sha256': sha(manifest_raw),
    'closure_lease_raw_sha256': sha(closed_raw),
    'slot_count': 51,
    'caller_condition_count': 6,
    'common_existential_witness_count': 12,
    'input_local_existential_witness_count': 2,
    'existential_witness_count': 14,
    'context_count': 12,
    'unresolved_count': 0,
    'covered_file_count': 9,
    'owned_file_count': 10
}
# This is intentionally the final write to any owned path.
write_new('lease.closed.json', closed_raw)
print(json.dumps(summary, sort_keys=True, ensure_ascii=False))
