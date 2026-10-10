import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
ACTOR = '/root/anonymous_decoder58'
SLOTS = ['objects', 'domains', 'quantifiers', 'assumptions', 'conclusion', 'scopes', 'constant_dependencies']

def canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def artifact(path):
    raw = path.read_bytes()
    lf = raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    return {'path': path.name, 'raw_bytes': len(raw), 'raw_sha256': digest(raw), 'lf_bytes': len(lf), 'lf_sha256': digest(lf)}

def write(path, obj):
    path.write_bytes(canon(obj) + b'\n')

def inputs():
    out = []
    for i in range(3):
        path = ROOT / f'packet{i}.json'
        obj = json.loads(path.read_bytes())
        actual = digest(canon({k: v for k, v in obj.items() if k != 'packet_sha256'}))
        assert actual == obj['packet_sha256']
        assert obj['lean']['compiled'] is True
        assert obj['non_disclosure']['source_text_included'] is False
        assert obj['non_disclosure']['source_identity_included'] is False
        out.append((obj, dict(artifact(path), canonical_decoder_packet_sha256=actual)))
    return out

DECODES = [
    {
        'reconstructed_theorem': 'Let X and Y be arbitrary measurable spaces, let μ and ν be measures on them, and let f:X→Y be measure preserving (measurable with f_*μ=ν). Canonical pullback g↦g∘f is a real linear isometry from L²(Y,ν;ℝ) to L²(X,μ;ℝ). Its image is exactly the real linear subspace of L²(X,μ;ℝ) consisting of classes that admit μ-almost-everywhere strongly measurable representatives for the pullback σ-algebra f⁻¹Σ_Y. No finiteness or probability assumption is imposed on either measure.',
        'semantic_slots': {
            'objects': 'X,Y; their measurable structures Σ_X,Σ_Y; measures μ,ν; f; real L² equivalence-class spaces; canonical composition linear isometry C_f; the submodule lpMeas for f⁻¹Σ_Y.',
            'domains': 'Arbitrary types X,Y with measurable spaces. μ∈Measure(X), ν∈Measure(Y), f:X→Y. Domain of C_f is L²(Y,ν;ℝ); codomain and both sides of the range equality lie in real L²(X,μ). Measures may be infinite.',
            'quantifiers': 'Universally over X,Y, their measurable structures, μ,ν, and f, subject to measure preservation. The submodule equality means every pullback class lies in lpMeas and every class in lpMeas is the pullback of some marginal L² class.',
            'assumptions': 'Only the supplied measurable-space structures and MeasurePreserving f μ ν: f is measurable and its pushforward of μ is ν. No finite-measure, probability, standard-Borel, countable-generation or invertibility hypothesis appears.',
            'conclusion': 'range(C_f)=lpMeas(ℝ,ℝ,f⁻¹Σ_Y,2,μ), as actual real linear submodules of L²(X,μ;ℝ).',
            'scopes': 'Equality of submodules of almost-everywhere equivalence classes, not pointwise equality of all function representatives. lpMeas uses almost-everywhere strong measurability for the comap measurable structure. No conditional-expectation, centeredness or probability conclusion is stated.',
            'constant_dependencies': 'Scalar field and function values are ℝ and exponent is exactly 2. No numerical bound or variable constant occurs; the range submodule depends on f,Σ_Y,μ and pullback depends also on ν through measure preservation.'
        },
        'confidence': 0.99,
        'unresolved_ambiguities': []
    },
    {
        'reconstructed_theorem': 'Let E be any finite-dimensional real inner-product space with its Borel measurable structure and canonical volume, including dimension zero. Let V:E→ℝ be C² and let α,β≥0 satisfy 0<α≤β and α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for all x,v∈E. Let η>0 with βη≤1. Define μ as normalized exponential tilting of volume by −V, J as the image of μ⊗N(0,I_E) under (x,z)↦(x,x+√η z), and ν as the second marginal of J. Let M:L²(ν;ℝ)→L²(J;ℝ) be the canonical second-coordinate pullback linear isometry and let P be conditional expectation onto the second-coordinate σ-algebra, regarded as an endomorphism of joint L². Then J and ν are probability measures, range(M)=range(P), and ∫Mu dJ=∫u dν for every u∈L²(ν;ℝ). Moreover M maps exactly all zero-integral marginal L² classes onto the zero-integral classes in range(P).',
        'semantic_slots': {
            'objects': 'E,V,nonnegative α,β,real η; normalized tilted measure μ; standard Gaussian on E; joint measure J on E×E; second marginal ν; canonical pullback M; conditional-expectation projection P onto the second-coordinate σ-algebra; centered L² subsets.',
            'domains': 'Finite-dimensional real inner-product normed additive space E with Borel measurable structure, including dimension zero. V:E→ℝ; α,β∈ℝ≥0; η∈ℝ; x,v∈E. M:L²(E,ν;ℝ)→L²(E×E,J;ℝ) is a real linear isometry; P is a continuous real linear endomorphism of the latter space.',
            'quantifiers': 'Universally over E and the given structures,V,α,β,η satisfying the assumptions; Hessian inequalities hold for every x,v∈E. After defining μ,J,ν,M,P, all five conclusions hold conjunctively. Integral preservation is for every u∈L²(ν). Centered-image equality includes both containment directions and existence of a centered marginal preimage for every centered projection-range class.',
            'assumptions': 'Finite-dimensional real inner-product normed group structure and Borel measurable structure on E; V is C²; 0<(α:ℝ); α≤β; for every x,v both α‖v‖²≤D²V(x)[v,v] and D²V(x)[v,v]≤β‖v‖²; η>0; (β:ℝ)η≤1. μ is defined by normalized exponential tilt and the independent product Gaussian pushforward defines J. Probability of J,ν and onto centered-range identification are conclusions, not extra premises.',
            'conclusion': 'IsProbabilityMeasure(J) and IsProbabilityMeasure(ν); range(M)=range(P); ∀u, ∫Mu dJ=∫u dν; M({u:∫u dν=0})={f:f∈range(P) and ∫f dJ=0}.',
            'scopes': 'All ranges and centered sets consist of real L² almost-everywhere equivalence classes. P is the actual second-coordinate conditional expectation embedded in joint L²; the displayed range is its actual image. Integral equalities use the designated measures. The proposition does not assert a sampling iteration, convergence rate, or finite dimension of L² itself.',
            'constant_dependencies': 'The Gaussian is standard and noise scale is √η; Hessian constants α,β and step restriction βη≤1 determine the admitted potential/noise parameters. The asserted equalities and probability conclusions contain no rate or hidden dimension-dependent constant. The definitions μ,J,ν,M,P depend on E,V,η and their measures.'
        },
        'confidence': 0.99,
        'unresolved_ambiguities': []
    },
    {
        'reconstructed_theorem': 'Let E be a finite-dimensional real inner-product Borel space with canonical volume, including dimension zero. Let V:E→ℝ be C² and α,β≥0 satisfy 0<α≤β and α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for all x,v∈E. Let η>0 and βη≤1. Let μ be the normalized exponential tilt of volume by −V and let J be the image of μ⊗N(0,I_E) under (x,z)↦(x,x+√η z). Set F(x,y)=(x,2x−y) and let P denote conditional expectation onto the second-coordinate σ-algebra as a joint L² endomorphism. There exists a real linear isometry U:L²(J;ℝ)→L²(J;ℝ) such that Ug=g∘F J-almost everywhere for every g, U²=I, and U is self-adjoint. For this U, set A=P∘U∘P and B=(I−P)∘U∘P. Every f∈range(P) with ∫f dJ=0 satisfies ‖Af‖≤[(1−αη)/(1+αη)]‖f‖ and [4αη/(1+αη)²]‖f‖²≤‖Bf‖². The endpoint αη=1 is included.',
        'semantic_slots': {
            'objects': 'E,V,α,β,η; normalized Gibbs tilt μ; standard Gaussian and joint pushforward J; reflection F(x,y)=(x,2x−y); real joint L²; actual second-coordinate conditional-expectation projection P; an existential linear isometry U implementing F almost everywhere; continuous operators A and B.',
            'domains': 'E is a finite-dimensional real inner-product normed additive space with Borel measurable structure and canonical volume, possibly of dimension zero. V:E→ℝ; α,β∈ℝ≥0 and η∈ℝ. J is a measure on E×E. U is a real linear isometry of L²(E×E,J;ℝ); P,A,B are continuous real linear endomorphisms of this L² space. This L² space is not asserted finite dimensional.',
            'quantifiers': 'Universally over E,V,α,β,η with their structures and hypotheses; the Hessian bounds quantify over all x,v∈E. After defining μ,J,F,P, there exists U for which all implementation, involution, self-adjointness and norm conclusions hold simultaneously. The AE implementation holds for every g∈L²(J). Both norm inequalities hold for every f∈L²(J) provided f∈range(P) and ∫f dJ=0.',
            'assumptions': 'Finite-dimensional real inner-product/Borel structure; V∈C²; 0<α≤β with α,β nonnegative; global lower and upper Hessian quadratic-form bounds α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for every x,v; η>0; βη≤1. μ,J,F,P are precisely the displayed definitions. No assumed reflection isometry, involutivity, self-adjointness, onto certificate or bound for U is an input: these are produced properties.',
            'conclusion': '∃ real linear isometry U with ∀g, Ug=g∘F J-AE, Function.Involutive(U), and IsSelfAdjoint(U) as a continuous real linear map. With A=PUP and B=(I−P)UP, ∀ centered f∈range(P), ‖Af‖≤((1−αη)/(1+αη))‖f‖ and (4αη/(1+αη)²)‖f‖²≤‖Bf‖².',
            'scopes': 'Ug=g∘F is an almost-everywhere statement about representatives under J, whereas U²=I and self-adjointness are properties of L² operators. Multiplication is composition; 1 is identity on joint L². Both inequalities are L² norm bounds restricted to actual projection-range zero-integral classes, not all joint classes. The non-strict step bound includes αη=1, where the first coefficient is zero and the second is one. No defect square root, inverse, weak-Sobolev equivalence, trajectory or algorithmic/query cost is concluded.',
            'constant_dependencies': 'Norm coefficients depend exactly on the product t=αη: c=(1−t)/(1+t) and d=4t/(1+t)². Assumptions give 0<t≤1, so denominators are positive and c≥0. β enters the Hessian upper bound and restriction βη≤1, but not the displayed norm coefficients. No dimension factor or unstated constant appears; operators depend on E,V,η and J.'
        },
        'confidence': 0.99,
        'unresolved_ambiguities': []
    }
]

def worker():
    packet_inputs = inputs()
    raw = (ROOT / 'lease.json').read_bytes()
    assert json.loads(raw)['status'] == 'OPEN'
    snapshot = ROOT / 'lease-open.json'
    with snapshot.open('xb') as out:
        out.write(raw)
    for i, (packet, meta) in enumerate(packet_inputs):
        result = dict(DECODES[i])
        result.update({
            'schema_version': 1,
            'packet_id': packet['packet_id'],
            'decoder': ACTOR,
            'actor_identity': ACTOR,
            'decoder_run_id': 'anonymous_decoder58',
            'decoder_packet_sha256': meta['canonical_decoder_packet_sha256'],
            'source_text_visible': False,
            'source_identity_visible': False,
            'input_artifact': meta,
            'reconstructed_theorem_text': result['reconstructed_theorem'],
            'reconstructed_text_sha256': digest(result['reconstructed_theorem'].encode('utf-8'))
        })
        result.update(result['semantic_slots'])
        write(ROOT / f'result{i}.json', result)
    print(json.dumps({'status': 'RESULTS_WRITTEN', 'result_count': 3, 'pid': os.getpid()}, ensure_ascii=False))

def verify():
    packet_inputs = inputs()
    for i, (_, meta) in enumerate(packet_inputs):
        result = json.loads((ROOT / f'result{i}.json').read_bytes())
        assert result['decoder_packet_sha256'] == meta['canonical_decoder_packet_sha256']
        assert result['reconstructed_theorem']
        assert all(result['semantic_slots'][slot] for slot in SLOTS)
        assert result['source_text_visible'] is False and result['source_identity_visible'] is False
        assert result['reconstructed_text_sha256'] == digest(result['reconstructed_theorem'].encode('utf-8'))
    print(json.dumps({'status': 'READBACK_PASSED', 'result_count': 3, 'semantic_slot_count': 21, 'pid': os.getpid()}))

def run():
    process_evidence = []
    for phase in ['worker', 'verify']:
        command = [sys.executable, '-X', 'utf8', str(Path(__file__).resolve()), phase]
        child = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        process_evidence.append({'phase': phase, 'argv': command, 'actual_exit_code': child.returncode, 'stdout': child.stdout, 'stderr': child.stderr})
        assert child.returncode == 0, process_evidence
    packet_inputs = inputs()
    payload = {'actor_identity': ACTOR, 'decoder_run_id': 'anonymous_decoder58', 'input_packets': [m for _, m in packet_inputs], 'result_artifacts': [artifact(ROOT / f'result{i}.json') for i in range(3)], 'result_count': 3, 'semantic_slot_count': 21, 'source_text_visible': False, 'source_identity_visible': False}
    run_record = {
        'schema_version': 1,
        'actor_identity': ACTOR,
        'decoder_run_id': 'anonymous_decoder58',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'RESULTS_AND_READBACKS_COMPLETE',
        'compiler_status': 'NOT_STARTED_CLOSED',
        'compiler_started': False,
        'source_text_visible': False,
        'source_identity_visible': False,
        'input_read_attempts': [{'phase': 'initial-console-read', 'actual_exit_code': 1, 'reason': 'UnicodeEncodeError in gbk stdout'}, {'phase': 'utf8-console-read', 'actual_exit_code': 0}, {'phase': 'canonical-input-digest-check', 'actual_exit_code': 0}],
        'initial_open_lease_snapshot': artifact(ROOT / 'lease-open.json'),
        'script_artifact': artifact(Path(__file__).resolve()),
        'foreground_child_processes': process_evidence,
        'payload': payload,
        'payload_sha256': digest(canon(payload)),
        'run_sha256_algorithm': 'SHA256(canonical sorted compact ensure_ascii=false UTF-8 JSON of whole run excluding only run_sha256)'
    }
    run_record['run_sha256'] = digest(canon(run_record))
    write(ROOT / 'run.json', run_record)
    print(json.dumps({'status': run_record['status'], 'actual_child_exit_codes': [p['actual_exit_code'] for p in process_evidence], 'result_count': 3, 'semantic_slot_count': 21, 'run_sha256': run_record['run_sha256'], 'payload_sha256': run_record['payload_sha256']}))

def close():
    run_record = json.loads((ROOT / 'run.json').read_bytes())
    assert run_record['run_sha256'] == digest(canon({k: v for k, v in run_record.items() if k != 'run_sha256'}))
    assert run_record['payload_sha256'] == digest(canon(run_record['payload']))
    verify()
    for item in run_record['payload']['result_artifacts']:
        assert item == artifact(ROOT / item['path'])
    assert run_record['initial_open_lease_snapshot'] == artifact(ROOT / 'lease-open.json')
    raw_open = (ROOT / 'lease-open.json').read_bytes()
    assert raw_open == (ROOT / 'lease.json').read_bytes()
    lease = json.loads(raw_open)
    assert lease['status'] == 'OPEN'
    lease.update({'status': 'CLOSED', 'actor_identity': ACTOR, 'compiler_started': False, 'compiler_status': 'NOT_STARTED_CLOSED', 'result_count': 3, 'semantic_slot_count': 21})
    closed_bytes = canon(lease) + b'\n'
    run_record.update({'status': 'CLOSED', 'foreground_wrapper_actual_exit_code': 0, 'foreground_wrapper_exit_code_evidence': 'Prior tools.exec_command invocation of decode_run.py run returned actual exit_code=0 before this closure invocation.', 'readback_status': 'PASSED', 'closed_lease_artifact': {'path': 'lease.json', 'raw_bytes': len(closed_bytes), 'raw_sha256': digest(closed_bytes)}, 'closed_utc': datetime.now(timezone.utc).isoformat()})
    run_record.pop('run_sha256')
    run_record['run_sha256'] = digest(canon(run_record))
    write(ROOT / 'run.json', run_record)
    reread = json.loads((ROOT / 'run.json').read_bytes())
    assert reread['run_sha256'] == digest(canon({k: v for k, v in reread.items() if k != 'run_sha256'}))
    summary = {'status': 'CLOSED', 'result_count': 3, 'semantic_slot_count': 21, 'compiler_status': 'NOT_STARTED_CLOSED', 'run_sha256': run_record['run_sha256'], 'payload_sha256': run_record['payload_sha256'], 'closed_lease_sha256': digest(closed_bytes), 'input_packets': run_record['payload']['input_packets'], 'result_artifacts': run_record['payload']['result_artifacts']}
    # The lease write is deliberately the last filesystem mutation.
    (ROOT / 'lease.json').write_bytes(closed_bytes)
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__':
    {'worker': worker, 'verify': verify, 'run': run, 'close': close}[sys.argv[1]]()
