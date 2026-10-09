import datetime
import hashlib
import json
import os
from pathlib import Path

BASE = Path(r'E:/Samplinglib/.astis/decoder-68')
OUT = BASE / 'independent'
INPUTS = ['packet0.json', 'packet1.json', 'lease.json', 'initial-lease.raw.snapshot.json']

def sha(b):
    return hashlib.sha256(b).hexdigest()

def enc(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')

def save(name, value):
    (OUT / name).write_bytes(enc(value))

def statrow(path):
    raw = path.read_bytes()
    st = path.stat()
    return {'raw_sha256': sha(raw), 'bytes': len(raw), 'mtime_ns': st.st_mtime_ns}

raws = {name: (BASE / name).read_bytes() for name in INPUTS}
assert raws['lease.json'] == raws['initial-lease.raw.snapshot.json']
assert json.loads(raws['lease.json'])['status'] == 'OPEN'
(OUT / 'snapshots').mkdir()
(OUT / 'reconstructions').mkdir()
manifest = {'schema_version': 1, 'normalization': 'Replace CRLF byte pairs by LF only; preserve every other byte.', 'inputs': {}, 'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False}
pins = []
for name in INPUTS:
    raw = raws[name]
    raw_name = 'snapshots/' + name + '.raw.snapshot'
    lf_name = 'snapshots/' + name + '.lf.snapshot'
    lf = raw.replace(b'\r\n', b'\n')
    (OUT / raw_name).write_bytes(raw)
    (OUT / lf_name).write_bytes(lf)
    manifest['inputs'][name] = {'original_path': str(BASE / name), **statrow(BASE / name), 'raw_snapshot': raw_name, 'lf_snapshot': lf_name, 'lf_sha256': sha(lf), 'lf_bytes': len(lf)}
    pins.append({'input': name, 'raw_snapshot': raw_name, 'lf_snapshot': lf_name, 'raw_sha256': sha(raw), 'lf_sha256': sha(lf)})
save('raw_input_manifest.json', manifest)
save('finite_pin_mappings.json', {'input_count': 4, 'pins': pins, 'no_other_input_files_read': True})

p0 = json.loads(raws['packet0.json'])
p1 = json.loads(raws['packet1.json'])
for p in (p0, p1):
    assert sha(p['lean']['statement'].encode('utf-8')) == p['lean']['statement_sha256']

text0 = '''For every type H with the stated normed additive commutative group, real inner-product-space, and complete-space structures, for every pair K,D of bounded real-linear endomorphisms of H, assume that K and D are self-adjoint and that I+K∘K=D∘D. For every real number c satisfying 0≤c and ‖D‖≤c, and every u,v∈H, the conclusion is
  |(1/2)(‖u‖²−‖v‖²)−⟨Ku,v⟩ℝ| ≤ (c/2)(‖u‖²+‖v‖²).
Here I is the identity endomorphism, multiplication of operators is composition, ‖D‖ is the operator norm, and the other norms and the inner product are those of H. All the displayed operator conditions and inequalities on c are assumptions; the absolute-value inequality is the conclusion. There is no existential witness and no premise containing u or v other than membership in H. The statement permits the zero Hilbert space, c=0 when its other premises hold, zero or equal vectors, and equality in the operator-norm bound. It does not assume c>0 or nonzero vectors.
'''

text1 = '''For every type E with the displayed normed additive commutative group and real inner-product-space structures, finite dimension over ℝ, and a measurable-space structure which is Borel for its topology, let V:E→ℝ, α,β∈ℝ≥0, and η∈ℝ be arbitrary. The only input mathematical conditions are 0<(α:ℝ), α≤β, V is ContDiff ℝ 2 (twice continuously differentiable), and, for every x,v∈E,
  (α:ℝ)‖v‖² ≤ ((fderiv ℝ (fderiv ℝ V) x) v) v ≤ (β:ℝ)‖v‖²,
together with 0<η and (β:ℝ)η≤1. The two Hessian inequalities are conjoined at each x,v. No probability, integrability, kernel, inverse, decomposition, or higher-derivative premise is supplied by the caller.

Define μ=volume.tilted(x↦−V(x)), using normalized exponential tilting. Let G=stdGaussian E. Define J as the pushforward of μ⊗G under (x,z)↦(x,x+√η·z), ν as the second marginal of J, Λ as the pushforward of J under (x,y)↦(y,2x−y), and F(x,y)=(x,2x−y). Define mY as the pullback of the measurable σ-algebra of E along the second-coordinate map. Use the product measurable space on E×E and the internally derived fact that mY is a sub-σ-algebra of it. Put HJ=Lp ℝ 2 J and Hν=Lp ℝ 2 ν, the real Hilbert spaces of square-integrable equivalence classes modulo the respective almost-everywhere equalities. Define HP=lpMeas ℝ ℝ mY 2 J, the closed subspace of HJ measurable for mY. Define P:HJ→L[ℝ]HJ as the inclusion of HP composed with condExpL2 for mY and J. The projection of the second coordinate from J to ν is internally supplied as measure preserving. Let M:Hν→ₗᵢ[ℝ]HJ be its pullback isometry.

The conclusions begin with μ, J, and ν being probability measures; HP is exactly the range of the underlying linear map of P; and for every f∈HP, P applied to its ambient HJ inclusion equals that inclusion.

There exists S:Kernel E E which is a Markov kernel and satisfies, for every state y∈E (not merely almost every y),
  S(y)=volume.tilted(x↦−V((y+x)/2)−‖y−x‖²/(8η)).
Moreover S is a conditional kernel for Λ, and both the first and second marginals of Λ equal ν. There exists a real-linear isometric equivalence e:Hν≃HP such that for every u∈Hν the inclusion of e(u) into HJ equals M(u). There exists a real-linear isometry U:HJ→HJ such that, for every g∈HJ, its representative Ug equals g∘F J-almost everywhere; U is involutive and its associated bounded real-linear operator is self-adjoint. Every such almost-everywhere assertion is per observable and concerns equivalence-class representatives, not a single universal pointwise equality for all observables.

There exists a bounded real-linear operator T:Hν→Hν which is self-adjoint, and, for every u∈Hν, satisfies all three conclusions
  ‖Tu‖≤‖u‖,
  (Tu)(y)=∫x u(x) dS(y)(x) for ν-almost every y,
  ∫y (Tu)(y) dν(y)=∫y u(y) dν(y).
Define A:HP→HP as orthogonal projection onto HP composed with U and the inclusion of HP into HJ. Define B:HP→HJ as (I−P)∘U∘P composed with that inclusion. Then A=eTe⁻¹ (the displayed isometric conjugation), A is self-adjoint, ‖Af‖≤‖f‖ for every f∈HP, and P(Bf)=0 for every f∈HP.

There exists a bounded real-linear Γ:Hν→Hν which is positive (self-adjoint with nonnegative quadratic form), satisfies Γ∘Γ=I−T∘T, and commutes with T. Define ΓP=eΓe⁻¹:HP→HP. Then ΓP is positive, ΓP∘ΓP=I−A∘A, ΓP commutes with A, and B.adjoint∘B=ΓP∘ΓP.

There exists q∈Hν whose representative is the constant function 1 ν-almost everywhere, for which Tq=q, and such that ⟨q,u⟩ℝ=∫y u(y)dν(y) for every u∈Hν. Define qP=e(q) and HP0=ker(innerSL ℝ qP), a subspace of HP, with its internally inherited normed additive group, real inner-product, and complete structures. Define
  γ=2√((α:ℝ)η)/(1+(α:ℝ)η).
For every f∈HP, f∈HP0 if and only if ∫y (e⁻¹f)(y)dν(y)=0. In addition ΓP(qP)=0 and 0<γ.

There exists a bounded real-linear ΓP0:HP0→HP0 restricting the SAME ΓP: for every f∈HP0, its inclusion (ΓP0 f:HP) equals ΓP(f:HP). The operator ΓP0 is positive, ΓP0−γI is positive, and ΓP0 is a unit in the bounded-endomorphism algebra. There exists a bounded real-linear Inv:HP0→HP0 with Inv∘ΓP0=I and ΓP0∘Inv=I, ‖Inv‖≤1/γ, and Inv self-adjoint. Both inverse identities concern this same ΓP0 and this same Inv.

There exists a bounded real-linear A0:HP0→HP0 such that, for every u∈HP0, its HP inclusion (A0u:HP) equals A(u:HP). It is self-adjoint, commutes with ΓP0, satisfies A0∘A0+ΓP0∘ΓP0=I, commutes with Inv, has A0∘Inv self-adjoint, and satisfies I+(A0∘Inv)∘(A0∘Inv)=Inv∘Inv. Define the real-valued function on HP0×HP0
  C(u,v)=(1/2)(‖u‖²−‖v‖²)−⟨(A0∘Inv)u,v⟩ℝ.
For every u,v∈HP0, |C(u,v)|≤(‖u‖²+‖v‖²)/(2γ).

Define Hperp=ker P as a subspace of HJ, with its internally inherited complete real Hilbert structures. This is the kernel of conditional expectation P, not the whole globally zero-mean subspace. There exists a bounded real-linear B0:HP0→Hperp such that for every f∈HP0 its ambient HJ inclusion equals B(f:HP). There exists a bounded real-linear V0:HP0→Hperp for which V0=B0∘Inv, B0=V0∘ΓP0, V0.adjoint∘V0=I on HP0, and ‖V0f‖=‖f‖ for every f∈HP0. This asserts isometry into Hperp, with no surjectivity or reverse-product identity as an additional stated conclusion.

There exists a bounded real-linear R:HJ→Hperp such that, for every g∈HJ, its ambient inclusion (Rg:HJ)=g−Pg. For every g∈HJ, the full ambient adjoint B.adjoint:HJ→HP satisfies
  B.adjoint(g)=HP0.subtypeL(B0.adjoint(Rg)).
Finally, for EVERY f∈HJ whose Bochner integral ∫z f(z)dJ(z) is zero, there exists fP∈HP0 with
  HP0.subtypeL(fP)=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f.
For this f define fperp=Rf∈Hperp and fV=V0.adjoint(fperp)∈HP0. All of the following then hold together:
  B.adjoint(fperp:HJ)=HP0.subtypeL(ΓP0 fV),
  HP0.subtypeL(ΓP0 fV)=ΓP(HP0.subtypeL fV),
  ‖f‖²=‖fP‖²+‖fperp‖²,
  ‖fV‖≤‖fperp‖,
  ‖fP‖²+‖fV‖²≤‖f‖²,
  |C(fP,fV)|≤‖f‖²/(2γ).
The witness fP is produced separately for each such f; fperp and fV are internal definitions from the SAME R and V0. Every existential witness S,e,U,T,Γ,q,ΓP0,Inv,A0,B0,V0,R and every such fP is conclusion data, not a public hypothesis. The successive existential scopes retain all preceding properties and use the same selected witnesses throughout.

Legal cases include zero-dimensional E and consequently possibly trivial centered subspaces, zero vectors and zero observables, α=β>0, and the step-size endpoint (β:ℝ)η=1. In particular αη=1 is legal when the remaining premises permit it; then γ=1. The statement does not require positive dimension or nontrivial HP0/Hperp, a strict step-size upper bound, nonzero observables, α<β, extra higher derivatives, or a surjective V0. α=0 and η=0 are excluded by the explicit strict premises. All integrals are the displayed Lean/Bochner integrals for the specified measures, and all L² operator identities are identities on equivalence classes with the displayed subtype coercions.
'''

slots0 = {
    'objects': 'H; its real Hilbert structures; bounded real-linear K,D:H→H; real c; vectors u,v; identity I; Hilbert norms and inner product; operator norm. No existential witness.',
    'domains': 'H is any complete normed real inner-product space, including the zero space. K,D∈H→L[ℝ]H; c∈ℝ; u,v∈H. Operator multiplication is composition; inner product is real-valued.',
    'quantifiers': 'Universally quantify H and its three displayed structures, K,D, their self-adjointness and square-identity proofs, c and the proofs 0≤c and ‖D‖≤c, then all u,v∈H. There is no existential quantifier and no nonzero-vector restriction.',
    'assumptions': 'Exactly [NormedAddCommGroup H], [InnerProductSpace ℝ H], [CompleteSpace H], IsSelfAdjoint K, IsSelfAdjoint D, I+K*K=D*D, c:ℝ, 0≤c, ‖D‖≤c, u,v:H. Neither c>0 nor any additional relation between u and v is assumed.',
    'conclusion': '|(1/2:ℝ)*(‖u‖^2−‖v‖^2)−inner ℝ (K u) v|≤(c/2)*(‖u‖^2+‖v‖^2). This is the sole mathematical conclusion.',
    'scopes': 'All assumptions apply to the same H,K,D,c and arbitrary u,v. Norm D is the operator norm, other norms are on H. c=0, equality in the norm bound, u=0, v=0, u=v, and trivial H are retained when the premises hold. No AE representatives occur.',
    'constant_dependencies': 'The estimate uses exactly the caller-supplied real c with 0≤c and ‖D‖≤c. Numerical factors are exactly 1/2 and c/2; there is no unnamed existential constant and no strict positivity requirement for c.'
}

slots1 = {
    'objects': 'Caller objects: E,V,α,β,η and the displayed structures and six hypothesis proofs. Internally defined objects: μ,J,ν,Λ,F,mY,HP,P,hp,M,A,B,ΓP,qP,HP0,γ,C,Hperp,fperp,fV. Concluded global existential witnesses: S,e,U,T,Γ,q,ΓP0,Inv,A0,B0,V0,R. A witness fP is additionally concluded for every centered joint f. All types, formulae, equalities, and witness properties are given in the complete reconstruction and literal statement.',
    'domains': 'E is any finite-dimensional real inner-product space with its displayed normed group, measurable space and Borel compatibility, including dimension zero. V:E→ℝ; α,β:ℝ≥0 with explicit coercions to ℝ; η:ℝ. μ,ν are measures on E; J,Λ on E×E; S:Kernel E E. HJ=Lp ℝ 2 J; Hν=Lp ℝ 2 ν; HP=lpMeas ℝ ℝ mY 2 J⊆HJ; HP0=ker(innerSL ℝ (e q))⊆HP; Hperp=ker P⊆HJ. M:Hν→ₗᵢ[ℝ]HJ; e:Hν≃ₗᵢ[ℝ]HP; U:HJ→ₗᵢ[ℝ]HJ; T,Γ:Hν→L[ℝ]Hν; P:HJ→L[ℝ]HJ; A,ΓP:HP→L[ℝ]HP; B:HP→L[ℝ]HJ; ΓP0,Inv,A0:HP0→L[ℝ]HP0; B0,V0:HP0→L[ℝ]Hperp; R:HJ→L[ℝ]Hperp; C:HP0→HP0→ℝ. Adjoint domains are B*:HJ→HP, B0*:Hperp→HP0, V0*:Hperp→HP0. Subtype inclusions and inherited complete structures have exactly the literal scopes.',
    'quantifiers': 'Universally quantify E and all five displayed typeclass structures, V,α,β,η. hH is universally quantified over all x,v:E and conjoins both Hessian bounds. After the six input hypotheses hα,hαβ,hV,hH,hη,hβη and the internal lets, the conclusion has probability/range/fixed-subspace clauses, then nested ∃S, ∃e, ∃U, ∃T, ∃Γ, ∃q, ∃ΓP0, ∃Inv, ∃A0, ∃B0, ∃V0, ∃R. Each retains preceding conclusions for the same witnesses. Universal conclusions quantify every f:HP (P fixed, A contraction, PB=0, centered iff), every y:E (exact kernel equality), every u:Hν (pullback, T contraction/AE action/integral preservation, q integral pairing), every g:HJ (U AE action, R inclusion and ambient B* action), every u/f:HP0 (restrictions, V0 norm), and every pair u,v:HP0 (C estimate). The terminal ∀f:HJ with ∫f dJ=0 implies ∃fP:HP0, followed by all six displayed equalities/inequalities using internally defined fperp=Rf and fV=V0* fperp. Each AE conclusion is per specified observable, not jointly pointwise in all observables.',
    'assumptions': 'Exactly [NormedAddCommGroup E], [InnerProductSpace ℝ E], [FiniteDimensional ℝ E], [MeasurableSpace E], [BorelSpace E], V:E→ℝ, α,β:ℝ≥0, η:ℝ, 0<(α:ℝ), α≤β, ContDiff ℝ 2 V, ∀x,v (α:ℝ)‖v‖²≤((fderiv ℝ (fderiv ℝ V) x)v)v AND that same Hessian value≤(β:ℝ)‖v‖², 0<η, (β:ℝ)η≤1. The local measurable-space Fact, all inherited Hilbert instances, probability assertions, exact kernel, self-adjoint operators, centeredness characterization, positive root, unit, inverse, isometry, quadratic bounds and terminal fP are internal definitions or conclusions. No extra higher-derivative, integrability, dimension-positive, source, or witness premise is added.',
    'conclusion': text1[text1.index('The conclusions begin'):text1.index('Legal cases include')].strip(),
    'scopes': 'The complete reconstruction and literal statement preserve every let and successive existential scope. μ is normalized exponential tilting by −V; J is the Gaussian product pushforward and ν its second marginal; Λ is the reflected pair law with both marginals ν; F fixes the first coordinate and reflects the second. mY is comap along Prod.snd, HP its measurable L² subspace, and P is the inclusion of conditional expectation. ΓP=eΓe⁻¹, qP=e q, HP0 is exactly the kernel of pairing with qP, ΓP0 and A0 are restrictions to this SAME HP0, and Inv in both inverse identities is the SAME Inv used in A0*Inv, C and V0. Hperp=ker P is conditional mean zero and differs from merely global mean zero. R acts on all joint observables and implements g−Pg. The terminal implication concerns all globally centered joint f and constructs fP internally; it does not require Pf=0. μ,J,ν probabilities are conclusions. Kernel equality holds for every y, while U and T representative actions are respectively per-g J-AE and per-u ν-AE. V0 is isometric into Hperp with no onto assertion. Dimension zero, trivial centered subspaces, zero observables, α=β>0, βη=1, and legal αη=1 are retained; α=0 and η=0 are excluded. Private proposition staging supplies no mathematical assumption or provider.',
    'constant_dependencies': 'The only caller scalars are α,β∈ℝ≥0 and η∈ℝ with the exact stated constraints. J uses Real.sqrt η; the kernel uses midpoint coefficient 1/2 and denominator 8*η; reflection uses coefficient 2. γ is exactly 2*Real.sqrt((α:ℝ)*η)/(1+(α:ℝ)*η), positive as a conclusion, with no dependence on β except through the admissible input constraints. The same γ appears in ΓP0−γI positivity, ‖Inv‖≤1/γ, pair bound denominator 2*γ, and final bound ‖f‖²/(2*γ). C uses exactly coefficient 1/2 and A0*Inv. No unspecified multiplicative constant, positive-dimension condition, stricter endpoint, or extra derivative bound is introduced.'
}

coverage0 = [
    ('p0-types', 'All original universal objects and three structures retained.'),
    ('p0-operator-premises', 'Both self-adjointness premises and I+K*K=D*D retained.'),
    ('p0-scalar-premises', 'c:ℝ, 0≤c, ‖D‖≤c retained, including equality and c=0.'),
    ('p0-vectors', 'Every u,v:H retained without nonzero restriction.'),
    ('p0-bound', 'Entire sole absolute-value inequality, both factors and all norms retained.'),
    ('p0-degenerate', 'Trivial H and zero/equal vectors explicitly retained conditionally on premises.')
]
coverage1 = [
    ('p1-input-structures', 'All five typeclasses; finite-dimensional real Borel inner-product E, including dimension zero.'),
    ('p1-input-scalars', 'V, NNReal α β, real η and every coercion scope.'),
    ('p1-input-hypotheses', 'All six caller hypotheses; both universally quantified Hessian inequalities; C² only; ηβ≤1 endpoint.'),
    ('p1-mu', 'Normalized exponential tilted volume by −V.'),
    ('p1-joint', 'Gaussian product pushforward (x,z)↦(x,x+√ηz).'),
    ('p1-marginal-reflection', 'ν=J.snd, Λ pushforward (x,y)↦(y,2x−y), F=(x,2x−y).'),
    ('p1-measurable-subspace', 'mY, internal product instance/Fact, HP=lpMeas, P=inclusion∘conditional expectation.'),
    ('p1-pullback', 'Internal hp and M pullback linear isometry.'),
    ('p1-probabilities', 'All μ,J,ν probability conclusions.'),
    ('p1-range-fixed', 'HP=P range and P fixes every HP element.'),
    ('p1-S', '∃ Markov S, exact normalized kernel for every y, Λ conditional-kernel property and both marginals ν.'),
    ('p1-e', '∃ isometric equivalence e, ambient equality to M for every u.'),
    ('p1-U', '∃ linear isometry U; per-g AE reflection action, involutive, bounded operator self-adjoint.'),
    ('p1-T', '∃ self-adjoint bounded T; every u contraction, ν-AE kernel action, and integral preservation.'),
    ('p1-A-B', 'Both exact let definitions, A=eTe⁻¹, self-adjointness/contraction, PB=0.'),
    ('p1-Gamma', '∃ positive Γ, Γ²=I−T², commutation with T.'),
    ('p1-GammaP', 'Conjugate ΓP positive, square I−A², commute A, B*B=ΓP².'),
    ('p1-q', '∃ constant-one AE q, Tq=q, integral pairing every u.'),
    ('p1-centered', 'qP, exact HP0 kernel, all inherited complete Hilbert structures, ∀f zero-mean iff.'),
    ('p1-gamma', 'Exact γ formula, ΓP qP=0, γ>0.'),
    ('p1-restricted-root', '∃ ΓP0 with every-f restriction, positivity, ΓP0−γI positivity and IsUnit.'),
    ('p1-Inv', '∃ same two-sided inverse, exact norm bound and self-adjointness.'),
    ('p1-A0', '∃ every-u restriction, self-adjointness, root commutation, squares sum I, Inv commutation.'),
    ('p1-product-square', 'Self-adjoint A0*Inv and I+(A0*Inv)²=Inv².'),
    ('p1-C', 'Exact C let formula and ∀u,v pair estimate.'),
    ('p1-Hperp', 'Exact Hperp=ker P and all internally inherited complete Hilbert structures.'),
    ('p1-B0', '∃ B0 and every-f ambient equality to restricted B.'),
    ('p1-V0', '∃ V0=B0∘Inv, B0=V0∘ΓP0, V0*V0=I and every-f norm equality; no onto addition.'),
    ('p1-R', '∃ R; every-g ambient Rg=g−Pg.'),
    ('p1-adjoint-all', 'Every-g full ambient adjoint action using R and B0* with HP0 inclusion.'),
    ('p1-terminal-forall', 'Every globally centered joint f, not only conditionally centered f, implies ∃fP in same HP0.'),
    ('p1-fP', 'Exact conditional-expectation equality with HP0 subtype inclusion.'),
    ('p1-terminal-lets', 'Same R gives fperp; same V0* gives fV in HP0.'),
    ('p1-terminal-adjoints', 'Both B* fperp=incl ΓP0 fV and incl ΓP0 fV=ΓP incl fV.'),
    ('p1-terminal-energy', 'Exact Pythagorean identity, corrector contraction, combined energy inequality.'),
    ('p1-terminal-C', 'Final |C fP fV|≤‖f‖²/(2γ).'),
    ('p1-scope-AE', 'Every nested witness retained as conclusion, every per-observable AE scope retained.'),
    ('p1-endpoints', 'βη=1, legal αη=1, α=β, zero dimension/subspaces/vectors/observables retained; α=0 and η=0 excluded.')
]

payload = {'schema_version': 1, 'task': 'independent-source-blind-semantic-reconstruction', 'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False, 'decoder': 'independent-source-blind-semantic-reconstructor', 'decoder_run_sha256': '', 'reconstructions': {}}
for ix, p, text, slots, coverage in [(0,p0,text0,slots0,coverage0),(1,p1,text1,slots1,coverage1)]:
    complete = text + '\nFULL LITERAL STATEMENT (verbatim supplied Lean type):\n' + p['lean']['statement'] + '\n'
    name = f'reconstructions/packet{ix}.complete-reconstruction.txt'
    raw = complete.encode('utf-8')
    (OUT / name).write_bytes(raw)
    payload['reconstructions'][p['packet_id']] = {
        'packet_id': p['packet_id'],
        'input_filename': f'packet{ix}.json',
        'lean_statement_literal': p['lean']['statement'],
        'lean_statement_sha256': p['lean']['statement_sha256'],
        'approved_definition_context_used': p['lean']['approved_definition_context'],
        'reconstructed_theorem_text': complete,
        'reconstructed_text_sha256': sha(raw),
        'named_reconstruction_file': name,
        **slots,
        'seven_slot_coverage': {key: {'status': 'covered', 'field': key} for key in slots},
        'clause_coverage': [{'clause_id': cid, 'status': 'retained', 'description': desc} for cid,desc in coverage],
        'decoder': 'independent-source-blind-semantic-reconstructor',
        'decoder_run_sha256': '',
        'source_text_visible': False,
        'source_identity_visible': False,
        'compiler_started': False,
        'source_fidelity_verdict': 'not assessed',
        'remaining_uncertainty': 'No source text, source identity, compiler, independent mathematical proof or source comparison was inspected. This reconstructs the supplied statement and approved context only; compiled=true is packet metadata, not independently verified.'
    }
save('reconstruction_payload.json', payload)
save('lease.json', {'status': 'OPEN', 'allowed_inputs': INPUTS, 'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False, 'owned_directory': str(OUT), 'root_parent_lease_writable': False})
save('build_process.json', {'process_id': os.getpid(), 'parent_process_id': os.getppid(), 'started_and_observed_in_process': True, 'action': 'read only allowed input bytes; create owned snapshots and semantic reconstructions', 'completed_work_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'compiler_started': False})
print(json.dumps({'process_id': os.getpid(), 'parent_process_id': os.getppid(), 'status': 'BUILD_DONE', 'packet_count': 2, 'allowed_input_count': 4}, sort_keys=True))
