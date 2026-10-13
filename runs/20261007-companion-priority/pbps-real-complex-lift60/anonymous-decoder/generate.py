import hashlib, json, os
from pathlib import Path

BASE = Path('E:/Samplinglib/.astis/decoder-60')
OUT = BASE / 'independent'
IDENTITY = '/root/anonymous_decoder60'
def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
def sha(value):
    return hashlib.sha256(value).hexdigest()
def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

lease_raw = (BASE / 'lease.json').read_bytes()
(OUT / 'initial-lease.json').write_bytes(lease_raw)
manifest = []
packets = []
for name in ['packet0.json', 'packet1.json', 'lease.json']:
    raw = (BASE / name).read_bytes()
    obj = json.loads(raw)
    record = {'path': str(BASE / name), 'role': 'anonymous proposition and approved definitions' if name != 'lease.json' else 'initial neutral lease', 'raw_sha256': sha(raw), 'lf_sha256': sha(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')), 'canonical_json_sha256': sha(canonical(obj)), 'raw_byte_count': len(raw)}
    if name != 'lease.json':
        payload = {k: v for k, v in obj.items() if k != 'packet_sha256'}
        record.update({'claimed_packet_sha256': obj['packet_sha256'], 'canonical_decoder_packet_sha256': sha(canonical(payload)), 'canonical_decoder_packet_recipe': 'SHA256(UTF8(JSON sorted keys, compact separators, ensure_ascii=false), omitting only packet_sha256)', 'statement_sha256': sha(obj['lean']['statement'].encode('utf-8')), 'statement_hash_matches': sha(obj['lean']['statement'].encode('utf-8')) == obj['lean']['statement_sha256']})
        assert record['canonical_decoder_packet_sha256'] == obj['packet_sha256']
        assert record['statement_hash_matches']
        packets.append(obj)
    manifest.append(record)
write('input-manifest.json', {'decoder': IDENTITY, 'inputs': manifest, 'source_text_visible': False, 'source_identity_visible': False, 'no_other_inputs': True})
payload = {'decoder': IDENTITY, 'input_manifest': manifest, 'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False, 'mode': 'independent-anonymous-statement-reconstruction'}
payload_hash = sha(canonical(payload))
write('decoder-payload.json', {'payload': payload, 'payload_sha256': payload_hash, 'payload_sha256_recipe': 'SHA256(canonical JSON of the payload object only; sorted keys, compact separators, ensure_ascii=false, UTF8)'})

text0 = '''Let Ω be any measurable space, let μ be any measure on Ω, and let H_R = L²(Ω, μ; ℝ) and H_C = L²(Ω, μ; ℂ), understood as almost-everywhere equivalence classes. Let D : H_R → H_R be a bounded real-linear positive operator: D is selfadjoint and ⟨u, D u⟩ ≥ 0 for every u ∈ H_R. Define bounded real-linear maps ι : H_R → H_C, R,Q : H_C → H_R, and C : H_C → H_C by the actual compLpL lifts of scalar real inclusion, real part, imaginary part, and conjugation. Thus ιu, Rg, Qg and Cg are respectively represented almost everywhere by u, Re(g), Im(g) and conjugate(g).
Then (i) ‖ιu‖ = ‖u‖ for every u ∈ H_R; (ii) for every g ∈ H_C, Cg = g if and only if there exists u ∈ H_R with ιu = g; and (iii) there exists a bounded complex-linear positive operator D_c : H_C → H_C such that, for every g ∈ H_C,
D_c g = ι(D(Rg)) + i · ι(D(Qg)),
for every u ∈ H_R,
D_c(ιu) = ι(Du),
and, for every g ∈ H_C,
C(D_c g) = D_c(Cg).
All these are quotient-space operator equalities; pointwise descriptions are only almost-everywhere descriptions. Positivity of D_c includes complex Hilbert selfadjointness and a nonnegative quadratic form. The measure need not be finite or a probability measure. No operator square root, inverse, adjoint identity for C, norm bound for D_c, or spectral claim is asserted.'''

text1 = '''Let E be a finite-dimensional real inner-product normed space equipped with its Borel measurable structure and canonical volume measure, with dimension zero allowed. Let V : E → ℝ be C², let α, β be nonnegative real parameters with 0 < α ≤ β, and let η > 0 satisfy βη ≤ 1. Assume for every x,v ∈ E the global two-sided second-derivative bound
α‖v‖² ≤ ((D(DV)(x))(v))(v) ≤ β‖v‖².
Here the derivative is the iterated real Fréchet derivative appearing in the statement. Define μ as normalized exponential tilting of volume by −V. Define J as the pushforward of μ ⊗ γ_E, where γ_E is the standard Gaussian on E, under (z,w) ↦ (z,z+√η w). Let ν = J.snd. Define Λ as the pushforward of J under (z,y) ↦ (y,2z−y). On H_R = L²(E,ν;ℝ) and H_C = L²(E,ν;ℂ), let ι, R, Q and C be the actual compLpL lifts of scalar real inclusion, real part, imaginary part and conjugation.
Then μ, J and ν are probability measures, and there exists a measurable Markov kernel S : E → measures on E such that, at every y ∈ E,
S(y) = volume.tilted(x ↦ −V((y+x)/2) − ‖y−x‖²/(8η)).
The kernel S is a conditional kernel of Λ given its first coordinate, and Λ.fst = ν and Λ.snd = ν. Within this existential choice of S, there exists a bounded real-linear operator T : H_R → H_R such that T is selfadjoint and for every u ∈ H_R,
‖Tu‖ ≤ ‖u‖,
(Tu)(y) = ∫ u(x) S(y,dx) for ν-almost every y,
and ∫ Tu(y) ν(dy) = ∫ u(y) ν(dy).
The bounded real-linear squared defect D = Id − T∘T is positive (selfadjoint with nonnegative quadratic form). Moreover, ‖ιu‖ = ‖u‖ for every u ∈ H_R, and for every g ∈ H_C,
Cg = g ⇔ there exists u ∈ H_R with ιu = g.
Within the choices of S and T there exists a bounded complex-linear positive operator D_c : H_C → H_C satisfying for every g ∈ H_C,
D_c g = ι(D(Rg)) + i · ι(D(Qg)),
for every u ∈ H_R,
D_c(ιu) = ι(Du),
and for every g ∈ H_C,
C(D_c g) = D_c(Cg).
Kernel normalization, Markov measurability, disintegration, stationary marginals, T and its positive squared defect, and the complex lift are conclusions rather than extra caller hypotheses. The conditional-action identity is almost everywhere; the displayed tilted-kernel identity is for every state. No positivity of T, square root of D, inverse of D, strict positive lower bound for D, spectral gap, higher-derivative hypothesis, or convergence-rate claim is asserted.'''

common_scopes = 'L² elements are AE quotient classes, with square-integrability and measurability built into membership. Scalar compLpL maps act on those classes; C is pointwise conjugation lifted as a real-linear map, not operator adjoint. The exact range of ι is the whole C-fixed subspace. Complex positivity includes selfadjointness and nonnegative Hilbert quadratic form. All universally quantified operator equations hold for every quotient class, not every representative at every state.'
records = [
    {'reconstructed_theorem_text': text0,
     'objects': 'Ω, its measurable structure, μ, H_R, H_C, the given D, the defined maps ι,R,Q,C, and the produced D_c.',
     'domains': 'Arbitrary measurable Ω and arbitrary μ; real and complex Lp spaces at exponent 2 over exactly μ. D and ι,R,Q,C are continuous linear maps over ℝ; D_c is continuous linear over ℂ.',
     'quantifiers': 'For every choice of Ω, measurable structure, μ, and bounded real-linear positive D: norm equality for all real classes u; fixed-range equivalence for all complex classes g with an existential real witness u; then one existential D_c satisfying positivity and three separately universal equations. D is a caller parameter; D_c and each fixed-range u are conclusion witnesses.',
     'assumptions': 'Only the measurable structure, arbitrary measure μ, bounded real-linear endomorphism D and hD: D.IsPositive. No finite-measure, probability, strict-positivity, invertibility or norm hypothesis.',
     'conclusion': 'The conjunction of isometry of ι, exact conjugation-fixed range of ι, and existence of a positive bounded complex-linear D_c with the displayed real/imaginary formula, restriction compatibility and conjugation commutation.',
     'scopes': common_scopes + ' There is no all-state function equality, square-root existence, inverse existence, uniqueness claim, or asserted operator-norm estimate.',
     'constant_dependencies': 'No numerical bound or rate constant. The maps ι,R,Q,C depend on μ and the scalar maps; D_c is produced for μ and D. The formula uses only coefficient 1 and the imaginary unit i; Lp exponent is fixed at 2.'},
    {'reconstructed_theorem_text': text1,
     'objects': 'Finite-dimensional real Hilbert Borel space E, V, α,β,η, canonical volume, standard Gaussian γ_E, defined measures μ,J,ν,Λ; real/complex L² spaces over ν; defined ι,R,Q,C; produced S,T,D_c; defined real squared defect D=Id−T∘T.',
     'domains': 'E is a normed additive commutative group with real inner product, finite real dimension, measurable space and BorelSpace structure. V:E→ℝ; α,β:ℝ≥0; η:ℝ. S:Kernel E E. T:H_R→L[ℝ]H_R and D_c:H_C→L[ℂ]H_C. Dimension zero is included.',
     'quantifiers': 'Universally over E and all displayed structures and V,α,β,η satisfying the six named caller hypotheses; Hessian bounds are for all x,v. μ,J,ν,Λ and scalar lifts are let-definitions. Probability conclusions precede ∃S; kernel identity is ∀y; disintegration and both marginals hold for that S. Then ∃T inside the S scope, with selfadjointness, three properties for every u, positive defect, scalar-lift facts, and then ∃D_c inside the S,T scope, with positivity and equations for every g or u. No caller-supplied S,T,D,disintegration,stationarity or D_c.',
     'assumptions': 'hα:0<(α:ℝ), hαβ:α≤β, hV:ContDiff ℝ 2 V, hH:∀x v, α‖v‖²≤(fderiv ℝ (fderiv ℝ V) x v) v≤β‖v‖², hη:0<η, hβη:(β:ℝ)η≤1; plus exactly the displayed algebraic/measure structures. α,β are already nonnegative by their type. No further higher derivative, kernel, normalizer, operator or finite-input assumptions.',
     'conclusion': 'μ,J,ν are probability measures; existence of a measurable Markov S with the exact normalized tilted density at all states, conditional-kernel property for Λ and equal ν marginals; existence of a selfadjoint contraction T implementing the S-integral AE and preserving ν-integrals; positivity of Id−T∘T; isometry and full C-fixed range of the actual scalar lift; existence of the positive complex-linear lift of that squared defect with the exact formula, restriction and conjugation commutation.',
     'scopes': common_scopes + ' T-action equals the S-integral only ν-AE. S(y) is the displayed normalized tilt at every y. Λ.fst=Λ.snd=ν are exact measure equalities. Markov and conditional-kernel properties are conclusions. T is selfadjoint and contractive, but its positivity is not asserted; the positive real operator is Id−T∘T. No square root, inverse, strict defect lower bound, rate or uniqueness is stated.',
     'constant_dependencies': 'Global α,β are potential Hessian bounds; η obeys η>0 and βη≤1. μ depends on V and volume; J,ν,Λ additionally depend on η and γ_E. S depends on V,η and volume; T acts on ν and represents S; D_c is the lift of Id−T∘T. Exact coefficients are √η in J, 2 in reflection, 1/2 at the potential midpoint, 8η in the quadratic penalty, 1 in the contraction bound, and i in the complex lift. No unmentioned dimension-dependent constant, rate or uniform quantitative estimate is asserted.'}
]
for idx, record in enumerate(records):
    record.update({'schema_version': 1, 'packet_id': packets[idx]['packet_id'], 'reconstructed_text_sha256': sha(record['reconstructed_theorem_text'].encode('utf-8')), 'decoder': IDENTITY, 'decoder_run_sha256': payload_hash, 'decoder_run_sha256_meaning': 'Named immutable decoder-payload hash; not the native whole-run hash. See decoder-payload.json. Native whole-run hash is run.json.run_sha256.', 'source_text_visible': False, 'source_identity_visible': False, 'synthesis_first_verdict': 'Reconstruction evidence only. The anonymous statement and approved definition context support the reconstruction; no source fidelity verdict is possible from these inputs.', 'compiled_status': 'Compiled is asserted by the supplied anonymous packet; no compiler was run or inspected by this decoder.'})
    write(f'decoded{idx}.json', record)
write('generation-record.json', {'pid': os.getpid(), 'decoder': IDENTITY, 'source_text_visible': False, 'source_identity_visible': False, 'read_inputs': [str(BASE / n) for n in ['packet0.json','packet1.json','lease.json']]})
print(json.dumps({'pid': os.getpid(), 'decoder_payload_sha256': payload_hash, 'reconstructed_text_sha256': [r['reconstructed_text_sha256'] for r in records]}))
