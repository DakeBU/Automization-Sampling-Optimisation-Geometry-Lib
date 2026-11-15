from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import textwrap

OUT = Path(__file__).resolve().parent
INPUT_ROOT = OUT.parent / 'roundtrip_inputs_4d87'
DECODER = ('Codex source-blind mathematical decoder; agent=/root/blind_decoder_4d87; '
           'run_id=blind_decoder_4d87; no unobserved model-version claim')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalized(text):
    return textwrap.dedent(text).strip()


def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def canonical_packet_bytes(obj):
    payload = dict(obj)
    payload.pop('packet_sha256', None)
    return json.dumps(payload, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':')).encode('utf-8')


run_semantics = normalized('''
    The generic run(next, update, oracle, N, s) returns ((s_final, r), c),
    where r is in Option X and c is a natural number. Its exact recursion is:
    first inspect next(s), even when N = 0. If next(s) = inl(x), return
    ((s, some(x)), 0). If next(s) = inr(q) and N = 0, return ((s, none), 0).
    If next(s) = inr(q) and N = n + 1, let a = oracle(q), evaluate
    run(next, update, oracle, n, update(s, q, a)) = (t, c), and return
    (t, c + 1). Thus the state/result pair in a recursive return is the
    tail's entire pair, and the count increases by one only in this last
    branch. A terminal result can be returned at zero fuel. A none result
    occurs when a query is requested with zero fuel; it is not a terminal
    result value. No count is charged by either nonrecursive branch.
''')

text_a = normalized('''
    Let S, Q, A, B, X, and Ω be arbitrary types, each with an arbitrary
    specified sigma algebra (and possibly different type universes).
    Products have the standard product sigma algebras and sums the standard
    disjoint-sum sigma algebras. Give Option X precisely the pullback sigma
    algebra under the map to Unit ⊕ X that sends none to inl(()) and some(x)
    to inr(x).

    For every probability measure μ on Ω, every next : S → X ⊕ Q,
    update : S → Q → B → S, oracle : Q → A, target : Q → B,
    decode : Q → A → B, and initial : Ω → S, assume that next is
    measurable, (s,q,b) ↦ update(s,q,b) is measurable, oracle is measurable,
    (q,a) ↦ decode(q,a) is measurable, and initial is measurable. Assume
    also that decode(q, oracle(q)) = target(q) for every q in Q.
    There is no separate measurability hypothesis on target.

    Use the run recursion specified below, with the answer type instantiated
    as appropriate. For every natural number N, define maps
    R,T : Ω → (S × Option X) × ℕ by
      R(ω) = run(next, (s,q,a) ↦ update(s,q,decode(q,a)), oracle,
                 N, initial(ω)),
      T(ω) = run(next, update, target, N, initial(ω)).
    Write c_R(ω) and c_T(ω) for their outer natural-number components.
    Then all the following hold together:
      1. R and T are measurable.
      2. For every ω in Ω, R(ω) = T(ω) and c_R(ω) ≤ N.
         This equality is of the entire returned record: the final state,
         the optional terminal result, and the count.
      3. The pushforward measures μ.map R and μ.map T are equal.
      4. μ.map R is a probability measure.
      5. The real-valued map ω ↦ (c_R(ω) : ℝ) is Bochner integrable under μ.
      6. ∫ (c_R(ω) : ℝ) dμ(ω) = ∫ (c_T(ω) : ℝ) dμ(ω).
      7. ∫ (c_R(ω) : ℝ) dμ(ω) ≤ (N : ℝ).
    Both integrals use this same μ; the counts and N are coerced from ℕ
    to ℝ for these real-valued integral assertions.
''') + '\n\n' + run_semantics

text_b = normalized('''
    For every natural number d with 2 ≤ d, and then every real number κ
    with 2 ≤ κ, let E = EuclideanSpace ℝ (Fin d), equipped with its Borel
    sigma algebra. Identify its coordinates with Fin d → ℝ by
    WithLp.ofLp and WithLp.toLp 2. Give Option E precisely the pullback
    sigma algebra under none ↦ inl(()) and some(x) ↦ inr(x) into Unit ⊕ E.
    Products and sums have their standard product and disjoint-sum sigma
    algebras.

    For every type S and type Ω, each with an arbitrary specified sigma
    algebra, every probability measure μ on Ω, every
      next : S → E ⊕ E,
      updateFO : S → E → (ℝ × E) → S,
      updateMV : S → E → E → S,
      initial : Ω → S,
    assume next is measurable, (s,x,a) ↦ updateFO(s,x,a) is measurable,
    (s,x,y) ↦ updateMV(s,x,y) is measurable, and initial is measurable.
    Here the left E in E ⊕ E is the terminal-result type and the right E
    is the query type. The two update functions are arbitrary; no relation
    between them is assumed.

    For every natural number N and then every O in the full real
    orthogonal group on Fin d, define, for each i in Fin d,
      θ_i = ((i.val : ℝ) + 1/2) · π / (d : ℝ),
      λ_i = (κ + 1)/2 + ((κ - 1)/2) · cos(θ_i),
      A = O · diagonal(i ↦ λ_i) · Oᵀ.
    Matrix indices are Fin d, whose index values are 0,...,d−1.
    For x in E, let x̄ = WithLp.ofLp x and define
      f(x) = (x̄ · (A x̄))/2,
      mv(x) = WithLp.toLp 2 (A x̄),
      fo(x) = (f(x), gradient f(x)).
    The dot here is the coordinate dot product; the matrix products and
    transpose are exactly the displayed real matrix operations. The
    gradient is the Riesz inverse of the totalized Fréchet derivative,
    gradient f(x) = (toDual ℝ E)⁻¹(fderiv ℝ f x). Its definition does not
    replace it in this theorem by an asserted coordinate formula.

    Use the run recursion specified below, with terminal type and query
    type both E and with the appropriate answer type. Define four maps
    Ω → (S × Option E) × ℕ by
      F(ω) = run(next, updateFO, fo, N, initial(ω)),
      F_M(ω) = run(next,
                  (s,x,y) ↦ updateFO(s,x,(⟨x,y⟩/2,y)),
                  mv, N, initial(ω)),
      M(ω) = run(next, updateMV, mv, N, initial(ω)),
      M_F(ω) = run(next,
                  (s,x,(r,y)) ↦ updateMV(s,x,y),
                  fo, N, initial(ω)).
    The inner product ⟨x,y⟩ in F_M is the real Euclidean inner product.
    Let c_H denote the outer natural-number component of any one of these
    returned maps H.

    All the following assertions hold together. First, for the pair
    (F_M,F): F_M and F are measurable; for every ω in Ω,
    F_M(ω) = F(ω) and c_{F_M}(ω) ≤ N; μ.map F_M = μ.map F;
    μ.map F_M is a probability measure; ω ↦ (c_{F_M}(ω) : ℝ) is Bochner
    integrable under μ;
      ∫ (c_{F_M}(ω) : ℝ) dμ(ω) = ∫ (c_F(ω) : ℝ) dμ(ω);
    and
      ∫ (c_{F_M}(ω) : ℝ) dμ(ω) ≤ (N : ℝ).
    Second, for the pair (M_F,M): M_F and M are measurable; for every
    ω in Ω, M_F(ω) = M(ω) and c_{M_F}(ω) ≤ N;
    μ.map M_F = μ.map M; μ.map M_F is a probability measure;
    ω ↦ (c_{M_F}(ω) : ℝ) is Bochner integrable under μ;
      ∫ (c_{M_F}(ω) : ℝ) dμ(ω) = ∫ (c_M(ω) : ℝ) dμ(ω);
    and
      ∫ (c_{M_F}(ω) : ℝ) dμ(ω) ≤ (N : ℝ).
    Each pointwise equality is equality of the entire final state,
    optional terminal result, and natural-number count, for every ω,
    not merely almost everywhere. All integrals are under the one
    displayed μ, with natural-number counts and N coerced to ℝ.
''') + '\n\n' + run_semantics.replace('Option X', 'Option E')

payload_a = {
    'reconstructed_theorem_text': text_a,
    'reconstructed_text_sha256': sha(text_a.encode('utf-8')),
    'objects': normalized('''
        S is the state type, Q the query type, A the oracle-answer type,
        B the decoded/target-answer type, X the terminal-result type, and Ω
        the probability-input type. The data are μ, next, update, oracle,
        target, decode, initial, and a natural fuel N. R is baseRun and T
        is targetRun. Each returned record is ((final state, optional
        terminal result), natural query count), not merely a terminal value.
    '''),
    'domains': normalized('''
        S : Type uS, Q : Type uQ, A : Type uA, B : Type uB,
        X : Type uX, Ω : Type uΩ, all with arbitrary MeasurableSpace
        instances. μ is a probability measure on Ω. next : S → X ⊕ Q;
        update : S → Q → B → S; oracle : Q → A; target : Q → B;
        decode : Q → A → B; initial : Ω → S. Products and disjoint sums
        use their standard sigma algebras. Option X has exactly the comap
        sigma algebra for none ↦ inl(()) and some(x) ↦ inr(x).
        R,T : Ω → (S × Option X) × ℕ; their count components are coerced
        to ℝ in Integrable and integral expressions.
    '''),
    'quantifiers': normalized('''
        First universally choose the six types S,Q,A,B,X,Ω and all six
        measurable-space instances; then install the specified Option X
        instance. Universally choose μ and its probability-measure
        instance, next, update, oracle, target, decode, initial in that
        order. Under the five displayed measurability hypotheses and the
        hypothesis ∀ q : Q, decode(q,oracle(q)) = target(q), universally
        choose fuel N : ℕ. Define R and T locally. The resulting conjunction
        contains ∀ ω : Ω, [R(ω)=T(ω) and c_R(ω)≤N], together with the
        measurability, pushforward, probability, integrability, integral
        equality, and integral bound assertions. There is no existential
        choice of algorithms, fuel, target, exceptional event, or constants.
    '''),
    'assumptions': normalized('''
        μ has total mass one. next is measurable. The uncurried map on
        S × (Q × B) given by (s,(q,b)) ↦ update(s,q,b) is measurable.
        oracle is measurable. The map on Q × A given by
        (q,a) ↦ decode(q,a) is measurable. initial is measurable.
        For every q, decode(q,oracle(q))=target(q). No separate
        measurability of target, equality of update functions, restriction
        on fuel, or termination hypothesis is among the assumptions.
    '''),
    'conclusion': normalized('''
        With R=baseRun and T=targetRun as defined in the reconstructed
        theorem: Measurable R and Measurable T; ∀ω, R(ω)=T(ω) and
        c_R(ω)≤N; μ.map R=μ.map T; IsProbabilityMeasure(μ.map R);
        Integrable(ω↦(c_R(ω):ℝ),μ);
        ∫(c_R:ℝ)dμ=∫(c_T:ℝ)dμ; and ∫(c_R:ℝ)dμ≤(N:ℝ).
        Every assertion is conjoined, for each fuel. The cost is exactly
        the returned recursive natural count. R updates with the decoded
        oracle answer; T updates with the target answer.
    '''),
    'scopes': normalized('''
        Both runs use the same next, update, initial(ω), and fuel; only the
        answer interface differs. The equality includes final state,
        some/none and any terminal value, and count, at every ω. Measures
        are pushforwards of this same μ onto the full record space.
        The explicitly asserted probability measure and integrable count
        are those of R. Both integrals use μ, and the bound is on R's
        integral. No equality between distinct probability inputs or
        almost-everywhere qualification appears. The recursive check of
        next precedes the fuel check, including at N=0; zero fuel may
        therefore still return some(x). Only a positive-fuel query branch
        performs an update and adds one to the tail count. The theorem
        does not assert termination within N queries.
    '''),
    'constant_dependencies': normalized('''
        There are no existential, asymptotic, or unspecified numerical
        constants. Both bounds use the very same universally supplied
        fuel N, exactly, with N coerced to ℝ for the integral bound. The
        type/sigma-algebra choices, μ, functions, and initial map precede
        N; the conclusions hold for every subsequent N with these data
        fixed. decode and target may depend on their earlier chosen data
        but satisfy the displayed pointwise identity for every q.
    '''),
    'decoder': DECODER,
    'source_text_visible': False,
}

payload_b = {
    'reconstructed_theorem_text': text_b,
    'reconstructed_text_sha256': sha(text_b.encode('utf-8')),
    'objects': normalized('''
        A dimension d and real parameter κ determine E=EuclideanSpace ℝ
        (Fin d). S is an arbitrary state type and Ω an arbitrary
        probability-input type. The data are μ, next, updateFO, updateMV,
        initial, fuel N, and orthogonal matrix O. θ_i, λ_i, matrix A,
        scalar quadratic f, vector oracle mv, and pair oracle fo are local
        definitions. F=foRun, F_M=foViaMV, M=mvRun, M_F=mvViaFO. The
        terminal and query types are both E, but occupy opposite sum
        constructors. FO answers are in ℝ × E; MV answers are in E.
    '''),
    'domains': normalized('''
        d : ℕ with 2≤d; κ : ℝ with 2≤κ; E has its Borel sigma algebra.
        i : Fin d has index value in {0,...,d−1}. O is in the full real
        Matrix.orthogonalGroup (Fin d), without a determinant-sign
        restriction or distribution. A : Matrix (Fin d) (Fin d) ℝ.
        S : Type uS and Ω : Type uΩ have arbitrary measurable spaces.
        μ is a probability measure on Ω. next : S → E ⊕ E;
        updateFO : S → E → (ℝ × E) → S;
        updateMV : S → E → E → S; initial : Ω → S; N : ℕ.
        f : E → ℝ, mv : E → E, fo : E → ℝ × E. All run maps take values
        in (S × Option E) × ℕ. Option E has exactly the pullback sigma
        algebra for none ↦ inl(()) and some(x) ↦ inr(x); products and
        sums carry standard sigma algebras. Coordinate maps are
        WithLp.ofLp and WithLp.toLp 2, and the inner product is real.
    '''),
    'quantifiers': normalized('''
        ∀ d:ℕ, 2≤d → ∀ κ:ℝ, 2≤κ → install Borel E and the specified
        Option E measurable space → ∀ S,Ω and their measurable-space
        instances, μ and its probability instance, next, updateFO,
        updateMV, initial. After the four measurability hypotheses,
        ∀ fuel N:ℕ, ∀ O in the full orthogonal group. Then define θ,A,f,mv,
        fo and the four run maps locally. For this same choice of all
        data, both conclusion blocks are conjoined. Each block has its
        own ∀ω:Ω governing full run equality and the pointwise cost bound.
        No random or existential O, algorithm, probability input, or
        constant is introduced. μ, next, both updates, and initial occur
        before the fuel and O quantifiers.
    '''),
    'assumptions': normalized('''
        The endpoint conditions are 2≤d and 2≤κ, with equality allowed in
        both. μ has total mass one. next and initial are measurable. The
        uncurried updateFO on S × (E × (ℝ × E)) is measurable and the
        uncurried updateMV on S × (E × E) is measurable. Membership of O
        in the full real orthogonal group is part of its quantified type.
        No relation between updateFO and updateMV, termination property,
        special initial-state distribution, almost-sure hypothesis,
        independence hypothesis, or measurability in O is assumed.
        No separate derivative-formula hypothesis is present.
    '''),
    'conclusion': normalized('''
        Use θ_i=((i.val:ℝ)+1/2)π/(d:ℝ),
        A=O diagonal(i↦(κ+1)/2+((κ−1)/2)cos θ_i) Oᵀ,
        f(x)=ofLp(x)·(A ofLp(x))/2,
        mv(x)=toLp 2(A ofLp(x)), fo(x)=(f(x),gradient f(x)).
        F_M uses mv with updateFO(s,x,(inner ℝ x y/2,y)); F uses fo
        with updateFO. M_F uses fo with updateMV(s,x,answer.2); M uses mv
        with updateMV. For each ordered pair (U,V)=(F_M,F) and (M_F,M),
        the asserted block is: Measurable U and Measurable V;
        ∀ω, U(ω)=V(ω) and c_U(ω)≤N; μ.map U=μ.map V;
        IsProbabilityMeasure(μ.map U); Integrable(ω↦(c_U(ω):ℝ),μ);
        ∫(c_U:ℝ)dμ=∫(c_V:ℝ)dμ; and ∫(c_U:ℝ)dμ≤(N:ℝ).
        Both blocks hold simultaneously. No equality between F and M
        (which use arbitrary distinct updates) is asserted.
    '''),
    'scopes': normalized('''
        Each comparison shares next, initial(ω), N, O, κ, d and μ.
        Equalities are pointwise for every ω and cover final state,
        optional terminal result, and count. Each pushforward is of μ on
        the full record space; each integral is under precisely μ.
        Probability and integrability are explicitly asserted for each
        simulated map F_M or M_F. The expectation equality compares that
        simulated map with its corresponding original F or M, and the
        bound is on the simulated map's real-coerced count. The FO-to-MV
        update discards the scalar answer and passes answer.2 to
        updateMV; the MV-to-FO update forms the ordered pair
        (inner ℝ x y/2,y), without extra oracle queries in the recursion.
        The generic run tests next before fuel, permits a some result at
        zero fuel, returns none only at a requested query with zero fuel,
        and increments only a positive-fuel query branch. gradient keeps
        its totalized Fréchet/Riesz definition; no derivative calculation
        is added to the theorem. No output-accuracy or termination
        assertion beyond these records and count bounds is present.
    '''),
    'constant_dependencies': normalized('''
        There are no existential or unspecified constants. The exact
        half-shift 1/2 and exact formula with (κ+1)/2 and (κ−1)/2 are
        retained; i has exactly the Fin d range. θ depends on i,d; A
        depends on d,κ,O; f,mv,fo depend on this A. The common fuel N is
        the exact pointwise bound and, after real coercion, the exact
        integral bound in both blocks. The statement chooses d and κ
        before S,Ω,μ and the algorithm data, then N and O after their
        measurability hypotheses. No distribution on O, dependence
        through hidden constants, or asymptotic relaxation is introduced.
    '''),
    'decoder': DECODER,
    'source_text_visible': False,
}

expected_input_sha = {
    'packet-a.json': '5a03a7e7a1bd085f958d13774a27f7bfa2b32223ba92e6f73357f6477b785822',
    'packet-b.json': 'f8f2ef0d5ebe8acd14b6e99ff357b61bbd199d9f5590dfa386001fad35e50194',
}
inputs = []
payloads = {}
for input_name, output_name, payload in [
        ('packet-a.json', 'result-a.json', payload_a),
        ('packet-b.json', 'result-b.json', payload_b)]:
    input_path = INPUT_ROOT / input_name
    raw = input_path.read_bytes()
    packet = json.loads(raw)
    input_hash = sha(raw)
    canonical_hash = sha(canonical_packet_bytes(packet))
    statement_hash = sha(packet['lean']['statement'].encode('utf-8'))
    assert input_hash == expected_input_sha[input_name]
    assert canonical_hash == packet['packet_sha256']
    assert statement_hash == packet['lean']['statement_sha256']
    assert packet['non_disclosure']['source_text_included'] is False
    payload.update({
        'packet_id': packet['packet_id'],
        'input_path': str(input_path),
        'input_bytes_sha256': input_hash,
        'canonical_packet_sha256': canonical_hash,
        'canonical_packet_hash_rule': 'SHA-256 of UTF-8 json.dumps(packet excluding packet_sha256, ensure_ascii=False, sort_keys=True, separators=(comma,colon)); no final newline',
        'lean_statement_sha256': statement_hash,
    })
    inputs.append({
        'path': str(input_path),
        'input_bytes_sha256': input_hash,
        'canonical_packet_sha256': canonical_hash,
        'lean_statement_sha256': statement_hash,
        'packet_id': packet['packet_id'],
    })
    payloads[output_name] = payload

# Freeze this capsule first. It contains the full reconstruction payloads
# before adding their decoder_run_sha256 fields, and not the final output
# file hashes, manifest bytes, index bytes, or its own hash.
capsule = {
    'schema_version': 1,
    'artifact_kind': 'frozen-source-blind-decoder-run-capsule',
    'run_id': 'blind_decoder_4d87',
    'decoder': DECODER,
    'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
    'allowed_input_artifacts': inputs,
    'mathematical_input_scope': ['lean.statement', 'lean.approved_definition_context'],
    'source_text_visible': False,
    'source_hidden_declaration': ('Only the two listed anonymous packet files were read as task inputs. '
        'No original source text, source identity, repository source, AGENTS files, '
        'implementations, audits, papers/books, prior decoder results, repair proposals, '
        'Git data, or other task messages were consulted. No proof search, build, source '
        'comparison, source-provenance inference, or fidelity verdict was performed.'),
    'decoder_program': {'path': str(Path(__file__).resolve()),
                        'bytes_sha256': sha(Path(__file__).read_bytes())},
    'hash_construction': ('decoder_run_sha256 is SHA-256 of this frozen capsule file exactly as '
        'written; this capsule omits its own hash and all final output/manifest/index hashes. '
        'Each final result is its capsule payload with decoder_run_sha256 appended.'),
    'outputs_before_decoder_run_sha256': payloads,
}
capsule_path = OUT / 'run-capsule.json'
capsule_path.write_bytes(json_bytes(capsule))
run_hash = sha(capsule_path.read_bytes())

outputs = []
contract_keys = {
    'reconstructed_theorem_text', 'reconstructed_text_sha256',
    'objects', 'domains', 'quantifiers', 'assumptions', 'conclusion',
    'scopes', 'constant_dependencies', 'decoder', 'decoder_run_sha256',
    'source_text_visible',
}
for output_name, payload in payloads.items():
    result = dict(payload)
    result['decoder_run_sha256'] = run_hash
    output_path = OUT / output_name
    output_path.write_bytes(json_bytes(result))
    parsed = json.loads(output_path.read_bytes())
    assert contract_keys <= set(parsed)
    assert parsed['source_text_visible'] is False
    assert sha(parsed['reconstructed_theorem_text'].encode('utf-8')) == parsed['reconstructed_text_sha256']
    assert parsed['decoder_run_sha256'] == run_hash
    outputs.append({
        'path': str(output_path),
        'bytes_sha256': sha(output_path.read_bytes()),
        'reconstructed_text_sha256': parsed['reconstructed_text_sha256'],
        'input_bytes_sha256': parsed['input_bytes_sha256'],
        'canonical_packet_sha256': parsed['canonical_packet_sha256'],
    })

manifest = {
    'schema_version': 1,
    'artifact_kind': 'actual-source-blind-decoder-run-manifest',
    'run_id': 'blind_decoder_4d87',
    'decoder': DECODER,
    'decoder_run_sha256': run_hash,
    'run_capsule': {'path': str(capsule_path), 'bytes_sha256': run_hash},
    'allowed_inputs': inputs,
    'source_text_visible': False,
    'source_hidden_declaration': capsule['source_hidden_declaration'],
    'outputs': outputs,
    'decoder_program': capsule['decoder_program'],
    'reconstruction_text_hash_rule': 'SHA-256 of the exact decoded JSON reconstructed_theorem_text string encoded as UTF-8; no extra newline appended',
    'canonical_packet_hash_rule': payload_a['canonical_packet_hash_rule'],
    'output_hash_rule': 'SHA-256 of exact output file bytes, including the final newline',
    'non_circular_hash_rule': capsule['hash_construction'],
    'verification_scope': 'Input/hash/contract/internal provenance checks only; no mathematical proof check or source-fidelity assessment',
    'completed_at_utc': datetime.now(timezone.utc).isoformat(),
}
manifest_path = OUT / 'run-manifest.json'
manifest_path.write_bytes(json_bytes(manifest))
index = {
    'schema_version': 1,
    'run_id': 'blind_decoder_4d87',
    'decoder_run_sha256': run_hash,
    'source_text_visible': False,
    'allowed_inputs': inputs,
    'results': outputs,
    'run_capsule': {'path': str(capsule_path), 'bytes_sha256': run_hash},
    'run_manifest': {'path': str(manifest_path), 'bytes_sha256': sha(manifest_path.read_bytes())},
    'decoder_program': capsule['decoder_program'],
}
index_path = OUT / 'index.json'
index_path.write_bytes(json_bytes(index))

for info in inputs:
    assert sha(Path(info['path']).read_bytes()) == info['input_bytes_sha256']
for info in outputs:
    assert sha(Path(info['path']).read_bytes()) == info['bytes_sha256']
assert sha(capsule_path.read_bytes()) == run_hash
assert json.loads(capsule_path.read_bytes())['outputs_before_decoder_run_sha256'] == payloads
for artifact in ['decode_run.py', 'run-capsule.json', 'result-a.json',
                 'result-b.json', 'run-manifest.json', 'index.json']:
    path = OUT / artifact
    print(artifact + ' ' + sha(path.read_bytes()))
print('decoder_run_sha256 ' + run_hash)
