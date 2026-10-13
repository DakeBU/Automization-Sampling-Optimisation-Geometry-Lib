import datetime
import hashlib
import json
from pathlib import Path

BASE = Path('E:/Samplinglib')
OUT = BASE / 'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/independent-topology-repair91'
PRIMARY = BASE / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
OUT.mkdir(parents=True, exist_ok=True)
raw = PRIMARY.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
s = raw.decode('utf-8')

def write(name, obj):
    (OUT / name).write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

extracts = []
for anchor, start, end in [
    ('A.1 fixed recursion and nonexplosion proof', s.index('Fix', s.index('id="A1.SS1"')), s.index('With the process now constructed')),
    ('A.1 strict simplex, exact A7 and cap/simplex absolute-convergence sentence', s.index('To pass from these identities'), s.index('Integrate', s.index('id="A1.E7"'))),
    ('A.1 nonnegative Tonelli and signed decomposition', s.index('This identity matches the initial density'), s.index('Taking', s.index('This identity matches the initial density'))),
    ('A.2 Borel finite recursion and nonexplosion terminal-state limit', s.index('Since', s.index('id="A1.SS2"')), s.index('Finally', s.index('Since', s.index('id="A1.SS2"'))))
]:
    extracts.append({'anchor': anchor, 'start_char': start, 'end_char': end, 'html': s[start:end]})
write('primary-anchors91.private.json', extracts)

write('source-first91.native.json', {
    'reviewer_id': '/root/exposition_repair89',
    'phase': 'FROZEN_PRIMARY_FIRST_PRE_OVERLAY_REASONING',
    'primary': {'path': str(PRIMARY), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'version': 'arXiv2609.06905v1'},
    'primary_read_observed_utc': '2026-10-11T01:26:56.311367+00:00',
    'overlay_or_existing_graph_opened': False,
    'source_facts': [
        'The actual independent Exp(1) integrated-hazard recursion uses the literal flow/reflection finite update and stops when the wait is infinite.',
        'The source proves nonexplosion before A7. Its proof uses preservation of shifted harmonic energy, a finite rate cap M on that energy orbit, finite-wait lower bounds E_j/M and divergence of partial sums of independent exponentials; M=0 is a separate no-jump case.',
        'A7 sums over strict ordered times 0<t1<...<tn<t. Its weight is exp(-integral_0^t lambda(path_s)ds) times the product of the n pre-jump rates. The path is the finite prescribed flow/reflection composition.',
        'Immediately after A7, the source explicitly justifies absolute convergence by simplex volume t^n/n! and the bounded rate M.',
        'The source later invokes Tonelli for nonnegative terms and decomposes signed bounded functions. A2 provides Borel hazard, crossing and finite recursion; nonexplosion then permits a physical-time terminal-state limit.'
    ],
    'common_unproved_assembly_inputs': [
        'For every n, identify the actual exact-count restricted path/history measure with the n-jump simplex weight, using iterated finite jump density, literal state updates, waiting-to-absolute-time transport and final survival factor.',
        'Construct measurable prescribed-path/test evaluations with the correct pre-jump/post-jump convention and every source endpoint convention.',
        'Handle n=0, t=0, zero rate, stopped/infinite next wait and deterministic endpoint coincidences exactly. Strict source endpoints cannot be replaced silently by closed endpoints. Any needed null-boundary fact must be derived internally from the available clock/density construction rather than inserted as a new public premise.'
    ],
    'sufficient_routes': [
        {
            'id': 'source-printed-cap-simplex',
            'source_status': 'Printed immediately after A7',
            'assembly_inputs': ['common exact n-count/simplex identification', 'finite preserved-energy rate cap M along every prescribed path', 'Lebesgue simplex volume t^n/n!', 'bounded measurable Psi'],
            'argument': ['Nonnegative hazard gives survival factor at most one.', 'For |Psi|<=B, the absolute n-term integral is bounded by B*M^n*t^n/n!.', 'The numerical majorant sums to B*exp(M*t), so the displayed series converges absolutely.', 'Combine the exact finite-count identities and exhaustive actual finite-count decomposition to identify the sum with the actual expectation.'],
            'boundary': 'Numerical summability by itself does not establish normalization, the probability path law, exact-count identification or endpoint coverage.'
        },
        {
            'id': 'finite-count-partition-mass-one-tonelli',
            'source_status': 'Source-implicit sufficient route using the already preceding nonexplosion result and nonnegative summation; not asserted to be the printed convergence sentence',
            'assembly_inputs': ['common exact n-count/simplex identification', 'actual probability input space and finite-count/nonexplosion on [0,t]', 'measurable disjoint exact-count events E_n covering probability one', 'Tonelli/nonnegative countable additivity'],
            'argument': ['For every n, the exact restricted-law identity gives I_n(Psi)=integral_(E_n) Psi(actual_path)dP.', 'Nonexplosion and the exact endpoint conventions make the E_n a probability-one partition. Therefore sum_n I_n(1)=sum_n P(E_n)=1; mass one comes from the actual partition, not from assuming A7.', 'For every nonnegative measurable Psi, Tonelli gives sum_n I_n(Psi)=integral sum_n 1_(E_n)*Psi(actual_path)dP=E[Psi(actual_path)], allowing infinity.', 'For a bounded signed measurable Psi with |Psi|<=B, sum_n integral_(E_n)|Psi|dP<=B*sum_n P(E_n)=B. In particular sum_n |I_n(Psi)|<=B, and positive/negative decomposition yields the signed expectation identity.'],
            'formulae': ['sum_n mass(q_n)=sum_n P(E_n)=1', 'sum_n integral |Psi| dq_n <= B', 'E[Psi(path)]=sum_n integral Psi(path(z0,times)) dq_n'],
            'boundary': 'This route does not need the separate factorial/simplex numerical majorant at the final assembly node once exact n-count laws and finite-count partition are available. The source proof of upstream nonexplosion still uses its rate cap. This is an OR route at expectation/convergence assembly, not a claim that all upstream cap mathematics disappears.'
        }
    ],
    'topology_constraints_for_later_overlay_review': [
        'Keep the printed cap/simplex route as a valid sufficient route.',
        'Retain finite-count/nonexplosion plus exact nonnegative partition/mass-one/Tonelli as an alternative sufficient route; do not force the cap/simplex numerical estimate into every convergence/expectation AND junction.',
        'Do not call nonexplosion alone sufficient: the exact count-weight law, survival factor and measurable/endpoint partition obligations remain.',
        'Do not infer mass one from an assumed full A7 formula; derive it by the actual finite-count partition.',
        'Do not add source binders, a measurability/normalization/density provider premise, physical-time Markov restart, a separate no-atom prerequisite, new91 target scope, or whole-paper completion.',
        'Preserve global proof truth and route provenance; conceptual similarity is not a compiled Lean edge.'
    ],
    'no91_header_Seal_claim_or_BODY_read': True,
    'no_canonical_changes': True,
    'source_data_not_published': True,
    'full_primary_copy_created': False,
    'frozen_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'next_action': 'Wait for exact overlay, packet and manifest hashes from root before opening any proposal or candidate.'
})

write('source-first91.chronology.native.json', {
    'reviewer_id': '/root/exposition_repair89',
    'events': [
        {'order': 1, 'action': 'Receive request for primary-first preparation only; no proposed overlay path or hash supplied.'},
        {'order': 2, 'action': 'Read the exact pinned primary Appendix A1 and A2 including exact A7, printed cap/simplex sentence and nonnegative/signed arguments.', 'observed_utc': '2026-10-11T01:26:56.311367+00:00'},
        {'order': 3, 'action': 'Reconstruct both sufficient routes independently and save native source-first reasoning plus bounded .private. extracts.'},
        {'order': 4, 'action': 'Freeze source-first artifacts before any overlay/graph comparison and wait for root exact hashes.'}
    ],
    'phase': 'PRE_OVERLAY_ONLY',
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()
})
artifacts = []
for p in sorted(OUT.glob('*')):
    if p.is_file() and p.name != 'source-first91.raw-manifest.json':
        data = p.read_bytes()
        artifacts.append({'path': str(p), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
write('source-first91.raw-manifest.json', {
    'reviewer_id': '/root/exposition_repair89',
    'phase': 'PRE_OVERLAY_FROZEN_INPUT_AND_OUTPUTS',
    'inputs': [{'path': str(PRIMARY), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'read_mode': 'fixed primary directly read before any overlay'}],
    'artifacts': artifacts,
    'self_hash_returned_externally': True,
    'full_primary_copy_created': False
})
for name in ['source-first91.native.json', 'source-first91.chronology.native.json', 'source-first91.raw-manifest.json']:
    data = (OUT / name).read_bytes()
    print(json.dumps({'path': str(OUT / name), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}))
