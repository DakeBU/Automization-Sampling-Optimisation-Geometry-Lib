import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

BASE = Path(r'E:/Samplinglib/.astis/decoder-68-consumer')
OUT = BASE / 'independent'
INPUTS = ['packet0.json', 'lease.json', 'initial-lease.raw.snapshot.json']
SLOTS = ['objects', 'domains', 'quantifiers', 'assumptions', 'conclusion', 'scopes', 'constant_dependencies']
FLAGS = {'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def save(name, obj):
    (OUT / name).write_bytes((json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8'))

def read(name):
    return json.loads((OUT / name).read_bytes())

def original(name):
    assert name in INPUTS
    return (BASE / name).read_bytes()

def file_rows(names):
    result = []
    for name in sorted(names):
        path = OUT / name
        raw = path.read_bytes()
        result.append({'path': name, 'bytes': len(raw), 'raw_sha256': sha(raw), 'mtime_ns': path.stat().st_mtime_ns})
    return result

def exact_rows(rows):
    for row in rows:
        p = OUT / row['path']
        raw = p.read_bytes()
        assert sha(raw) == row['raw_sha256'] and len(raw) == row['bytes']
        assert p.stat().st_mtime_ns == row['mtime_ns']

def process_record(stage):
    return {'stage': stage, 'process_id': os.getpid(), 'parent_process_id': os.getppid(), 'completed_work_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), **FLAGS}

def original_checks():
    mf = read('raw_input_manifest.json')
    for name,row in mf['inputs'].items():
        raw = original(name)
        assert sha(raw) == row['raw_sha256'] and len(raw) == row['bytes']
        assert (BASE / name).stat().st_mtime_ns == row['mtime_ns']
        assert (OUT / row['raw_snapshot']).read_bytes() == raw
        assert (OUT / row['lf_snapshot']).read_bytes() == raw.replace(b'\r\n', b'\n')
    assert original('lease.json') == original('initial-lease.raw.snapshot.json')
    assert json.loads(original('lease.json'))['status'] == 'OPEN'
    return mf

def payload_checks():
    packet = json.loads(original('packet0.json'))
    payload = read('reconstruction_payload.json')
    assert list(payload['reconstructions']) == [packet['packet_id']]
    rec = payload['reconstructions'][packet['packet_id']]
    assert rec['lean_statement_literal'] == packet['lean']['statement']
    assert rec['lean_statement_literal'] in rec['reconstructed_theorem_text']
    raw = rec['reconstructed_theorem_text'].encode('utf-8')
    assert (OUT / rec['named_reconstruction_file']).read_bytes() == raw
    assert sha(raw) == rec['reconstructed_text_sha256']
    assert all(rec[s].strip() and rec['seven_slot_coverage'][s]['status'] == 'covered' for s in SLOTS)
    assert all(row['status'] == 'retained' for row in rec['clause_coverage'])
    for obj in [payload,rec,read('lease.json')]:
        assert all(obj[key] is False for key in FLAGS)
    return packet,payload,rec

def run_check():
    run = read('final_run.json')
    logical = dict(run)
    claimed = logical.pop('run_sha256')
    assert sha(canon(logical)) == claimed
    _,payload,rec = payload_checks()
    assert payload['decoder_run_sha256'] == rec['decoder_run_sha256'] == claimed
    assert all(run[key] is False for key in FLAGS)
    assert run['packet_records'][rec['packet_id']]['seven_slots'] == {slot: rec[slot] for slot in SLOTS}
    assert run['packet_records'][rec['packet_id']]['clause_coverage'] == rec['clause_coverage']
    return run,payload,rec

def terminal_check(name):
    t = read(name)
    assert t['actual_process_completed'] is True and t['exit_code'] == 0 and t['exit_status'] == 'EXIT0'
    assert t['process_id'] > 0 and t['parent_process_id'] == t['shell_process_id']
    return t

TEXT = '''For every type E equipped with the displayed normed additive commutative group and real inner-product-space structures, finite dimension over ℝ, and a measurable-space structure that is Borel for its topology, let V:E→ℝ, α,β∈ℝ≥0 and η∈ℝ be arbitrary. The only input mathematical conditions are 0<(α:ℝ), α≤β, ContDiff ℝ 2 V, and, for every x,v∈E,
  (α:ℝ)‖v‖² ≤ ((fderiv ℝ (fderiv ℝ V) x) v) v,
  ((fderiv ℝ (fderiv ℝ V) x) v) v ≤ (β:ℝ)‖v‖²,
with these two inequalities conjoined for each x,v, together with 0<η and (β:ℝ)η≤1. V is twice continuously differentiable; no stronger differentiability, probability, kernel, inverse, decomposition, or integrability premise is supplied by the caller.

Define μ=volume.tilted(x↦−V(x)), with normalized exponential tilting. Let G=stdGaussian E. Define J as the pushforward of μ⊗G under (x,z)↦(x,x+√η·z), ν=J.snd, Λ as the pushforward of J under (x,y)↦(y,2x−y), and F(x,y)=(x,2x−y). Define mY as the comap of the measurable σ-algebra of E along the second-coordinate map. Use the product measurable space on E×E and the internally derived Fact that mY is below it. Write HJ=Lp ℝ 2 J and Hν=Lp ℝ 2 ν for the real Hilbert spaces of square-integrable equivalence classes modulo almost-everywhere equality. Define HP=lpMeas ℝ ℝ mY 2 J, the closed mY-measurable subspace of HJ. Define P:HJ→L[ℝ]HJ as inclusion of HP composed with condExpL2 for mY,J. The second-coordinate projection is internally supplied as a measure-preserving map from J to ν; M:Hν→ₗᵢ[ℝ]HJ is its pullback linear isometry.

The conclusions are that μ,J,ν are probability measures, HP equals the range of the underlying linear map of P, and P(f:HJ)=(f:HJ) for every f∈HP.

There exists S:Kernel E E such that S is a Markov kernel, and for EVERY y∈E,
  S(y)=volume.tilted(x↦−V((y+x)/2)−‖y−x‖²/(8η)).
This equality is every-state, not merely almost everywhere. In addition Λ.IsCondKernel S holds and Λ.fst=ν and Λ.snd=ν. There exists a real-linear isometric equivalence e:Hν≃HP with (eu:HJ)=Mu for every u∈Hν. There exists a real-linear isometry U:HJ→HJ such that, for every g∈HJ, the representative Ug equals g∘F J-almost everywhere, U is involutive, and the associated bounded real-linear map is self-adjoint.

There exists a bounded real-linear T:Hν→Hν such that T is self-adjoint and, for every u∈Hν, all three statements hold:
  ‖Tu‖≤‖u‖,
  (Tu)(y)=∫x u(x)dS(y)(x) for ν-almost every y,
  ∫y(Tu)(y)dν(y)=∫y u(y)dν(y).
All representative actions are per observable: the statement does not assert one common pointwise equality outside one null set for all g or all u. Define A:HP→L[ℝ]HP as HP.orthogonalProjectionOnto composed with U and HP.subtypeL. Define B:HP→L[ℝ]HJ as (I−P)∘U∘P composed with HP.subtypeL. Then A=eTe⁻¹ (the displayed isometric conjugation), A is self-adjoint, ‖Af‖≤‖f‖ for every f∈HP, and P(Bf)=0 for every f∈HP.

There exists a bounded real-linear Γ:Hν→Hν with Γ positive (self-adjoint and nonnegative quadratic form), Γ∘Γ=I−T∘T, and Γ commuting with T. Define ΓP=eΓe⁻¹:HP→HP. Then ΓP is positive, ΓP∘ΓP=I−A∘A, ΓP commutes with A, and B.adjoint∘B=ΓP∘ΓP.

There exists q∈Hν whose representative equals 1 ν-almost everywhere, such that Tq=q and, for every u∈Hν, ⟨q,u⟩ℝ=∫y u(y)dν(y). Define qP=e q and HP0=ker(innerSL ℝ qP), a subspace of HP with the internally inherited normed additive group, real inner-product, and complete-space structures. Define the exact scalar
  γ=2√((α:ℝ)η)/(1+(α:ℝ)η).
For every f∈HP, f∈HP0 if and only if ∫y(e⁻¹f)(y)dν(y)=0. Moreover ΓP qP=0 and 0<γ.

There exists a bounded real-linear ΓP0:HP0→HP0 such that for every f∈HP0, (ΓP0 f:HP)=ΓP(f:HP), ΓP0 is positive, ΓP0−γI is positive, and ΓP0 is a unit in the bounded endomorphism algebra. There exists a bounded real-linear Inv:HP0→HP0 with Inv∘ΓP0=I, ΓP0∘Inv=I, ‖Inv‖≤1/γ, and Inv self-adjoint. These are two inverse identities for the SAME ΓP0 and the SAME Inv.

There exists a bounded real-linear A0:HP0→HP0 such that for every u∈HP0, (A0u:HP)=A(u:HP), A0 is self-adjoint, A0 commutes with ΓP0, A0∘A0+ΓP0∘ΓP0=I, A0 commutes with Inv, A0∘Inv is self-adjoint, and I+(A0∘Inv)∘(A0∘Inv)=Inv∘Inv. Define C:HP0→HP0→ℝ by
  C(u,v)=(1/2)(‖u‖²−‖v‖²)−⟨(A0∘Inv)u,v⟩ℝ.
For EVERY u,v∈HP0,
  |C(u,v)|≤(‖u‖²+‖v‖²)/(2γ).

Define Hperp=ker P⊆HJ, with internally inherited normed group, real inner-product, and complete-space structures. This is the kernel of the conditional-expectation operator P, not the entire globally zero-mean space. There exists a bounded real-linear B0:HP0→Hperp with (B0f:HJ)=B(f:HP) for every f∈HP0. There exists a bounded real-linear V0:HP0→Hperp such that V0=B0∘Inv, B0=V0∘ΓP0, V0.adjoint∘V0=I on HP0, and ‖V0f‖=‖f‖ for every f∈HP0. This asserts an isometry INTO Hperp; no surjectivity or reverse-product identity is asserted.

There exists a bounded real-linear R:HJ→Hperp such that (Rg:HJ)=g−Pg for EVERY g∈HJ. Also, for EVERY g∈HJ, the full ambient adjoint B.adjoint:HJ→HP satisfies
  B.adjoint(g)=HP0.subtypeL(B0.adjoint(Rg)).

For EVERY f∈HJ with zero Bochner integral ∫z f(z)dJ(z)=0, there exists fP∈HP0 for which
  HP0.subtypeL(fP)=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f.
Define fperp=Rf∈Hperp and fV=V0.adjoint(fperp)∈HP0. All SIX preceding decomposition and quadratic conclusions hold together:
  B.adjoint(fperp:HJ)=HP0.subtypeL(ΓP0 fV),
  HP0.subtypeL(ΓP0 fV)=ΓP(HP0.subtypeL fV),
  ‖f‖²=‖fP‖²+‖fperp‖²,
  ‖fV‖≤‖fperp‖,
  ‖fP‖²+‖fV‖²≤‖f‖²,
  |C(fP,fV)|≤‖f‖²/(2γ).
In the SAME scope and using these SAME fP,fperp,fV, for EVERY real omegaWeight satisfying 0<omegaWeight and omegaWeight≤γ, define
  L=‖f‖²+omegaWeight·C(fP,fV).
All FOUR exact inequalities then hold together:
  (1/2:ℝ)·‖f‖²≤L,
  L≤(3/2:ℝ)·‖f‖²,
  |L−‖f‖²|≤(omegaWeight/(2γ))·‖f‖²,
  (omegaWeight/(2γ))·‖f‖²≤(1/2:ℝ)·‖f‖².
The scalar interval is universally quantified inside the centered-f conclusion, after the existence of fP; fP is therefore selected before omegaWeight and the SAME fP works for every admissible omegaWeight. Neither omegaWeight nor its interval is an initial caller premise. L is a let-defined real scalar, not an independently assumed or existentially selected energy. The endpoint omegaWeight=γ is included, while omegaWeight=0 is excluded from this interval.

Every existential S,e,U,T,Γ,q,ΓP0,Inv,A0,B0,V0,R, and every per-f witness fP, is concluded data rather than an input hypothesis. Successive existential scopes retain all earlier properties and reuse the same witnesses. A private Prop definition only records the entire proposition; it supplies neither proof nor additional mathematical premise. All operators are bounded real-linear maps unless explicitly declared linear isometries/equivalences; multiplication is composition; adjoints are Hilbert adjoints; and all L² equalities concern equivalence classes with the displayed subtype inclusions. Integrals are the displayed Bochner integrals for their specified measures.

Legal cases include dimension-zero E, possibly trivial HP0 or Hperp, zero vectors and zero observables, α=β>0, (β:ℝ)η=1, and (α:ℝ)η=1 when the premises permit it (then γ=1). The final scalar endpoint omegaWeight=γ is legal, including γ=1 in that case. The statement does not require positive dimension, nontrivial centered subspaces, nonzero f, a strict upper step-size inequality, α<β, higher-derivative bounds, or surjectivity of V0. α=0 and η=0 are excluded by the explicit strict input hypotheses. No source identity or source-fidelity conclusion is inferred.
'''

SLOT_TEXT = {
    'objects': 'Caller objects E,V,α,β,η and five displayed structures/six proof hypotheses. Internal lets μ,J,ν,Λ,F,mY,HP,P,hp,M,A,B,ΓP,qP,HP0,γ,C,Hperp,fperp,fV and the final real L. Global concluded existential witnesses S,e,U,T,Γ,q,ΓP0,Inv,A0,B0,V0,R; per-centered-f existential fP. Final omegaWeight is universally quantified real conclusion data. Every formula, witness property and universal conclusion is in the complete reconstruction and verbatim literal statement.',
    'domains': 'E is any finite-dimensional real inner-product Borel measurable space with the exact five displayed structures, including dimension zero. V:E→ℝ; α,β:ℝ≥0 with explicit coercions to ℝ; η:ℝ. μ,ν:Measure E; J,Λ:Measure(E×E); S:Kernel E E; F:E×E→E×E; mY=comap Prod.snd. HJ=Lp ℝ 2 J and Hν=Lp ℝ 2 ν are Hilbert AE classes. HP=lpMeas ℝ ℝ mY 2 J⊆HJ; HP0=ker(innerSL ℝ (e q))⊆HP; Hperp=ker P⊆HJ. P:HJ→L[ℝ]HJ; M:Hν→ₗᵢ[ℝ]HJ; e:Hν≃ₗᵢ[ℝ]HP; U:HJ→ₗᵢ[ℝ]HJ; T,Γ:Hν→L[ℝ]Hν; A,ΓP:HP→L[ℝ]HP; B:HP→L[ℝ]HJ; ΓP0,Inv,A0:HP0→L[ℝ]HP0; B0,V0:HP0→L[ℝ]Hperp; R:HJ→L[ℝ]Hperp; C:HP0→HP0→ℝ. B*:HJ→HP, B0*:Hperp→HP0, V0*:Hperp→HP0. omegaWeight,L:ℝ; final weight interval (0,γ] is inside the conclusion. Inherited complete subspace structures are internal.',
    'quantifiers': 'Universally quantify E, all five structures, V,α,β,η and the six input proof binders. hH universally quantifies every x,v:E and conjoins the two Hessian bounds. After the initial lets, conclude the probability/range/fixed-subspace clauses and nested ∃S,∃e,∃U,∃T,∃Γ,∃q,∃ΓP0,∃Inv,∃A0,∃B0,∃V0,∃R. Preserve every universal f:HP, y:E, u:Hν, g:HJ, and f/u:HP0 in the literal statement and ∀u,v:HP0 pair estimate. Every-state S equality is ∀y, while representative U and T actions are respectively per-g J-AE and per-u ν-AE. The final quantifier is ∀f:HJ, integral(f)=0 → ∃fP:HP0 with its exact conditional-mean equality, then fperp=Rf and fV=V0* fperp, six decomposition/estimate clauses, AND ∀omegaWeight:ℝ, 0<omegaWeight → omegaWeight≤γ → let L=‖f‖²+omegaWeight*C fP fV in all FOUR inequalities. The same fP precedes and serves every weight; no ∃weight and no weight-dependent fP is substituted.',
    'assumptions': 'Exactly [NormedAddCommGroup E], [InnerProductSpace ℝ E], [FiniteDimensional ℝ E], [MeasurableSpace E], [BorelSpace E], {V:E→ℝ}, {α β:ℝ≥0}, {η:ℝ}, hα:0<(α:ℝ), hαβ:α≤β, hV:ContDiff ℝ 2 V, hH:∀x,v ((α:ℝ)‖v‖²≤((fderiv ℝ (fderiv ℝ V) x)v)v ∧ that same Hessian value≤(β:ℝ)‖v‖²), hη:0<η, hβη:(β:ℝ)η≤1. All later probability/kernel/operator/root/inverse/isometry/centeredness/decomposition/energy assertions are conclusions, and the measurable-space Fact and Hilbert instances are derived internally. The conditions integral(f)=0 and 0<omegaWeight≤γ are local antecedents of universally quantified conclusions, not extra public assumptions. No extra derivative, integrability, positive-dimension or witness premise.',
    'conclusion': TEXT[TEXT.index('The conclusions are'):TEXT.index('Every existential S')].strip(),
    'scopes': 'Keep all lets and nested witness scopes in the literal complete value. μ is normalized tilted volume; J Gaussian product pushforward; ν second marginal; Λ reflected-pair law with both marginals ν; F fixes first coordinate/reflection in second. HP is the mY-measurable closed L² subspace, P conditional expectation followed by inclusion. ΓP=eΓe⁻¹; qP=e q; HP0 is exactly kernel of pairing with qP; ΓP0 and A0 are restrictions to this SAME centered space; same ΓP0 and Inv occur in both inverse identities, A0*Inv, C and V0. Hperp=ker P concerns conditional mean zero, not merely global mean zero. R and B* formulas quantify all joint observables. Final f only needs global zero integral, and its centered witness fP is produced internally before ∀omegaWeight. fperp and fV use the SAME R,V0; L uses SAME fP,fV,C and each universal weight. Four final inequalities are a conjunction, in addition to all prior conclusions. Per-observable AE actions preserve representatives/measures; every-state S identity is stronger. V0 is isometry into Hperp, with no onto conclusion. All endpoint and degenerate cases in the reconstruction are retained.',
    'constant_dependencies': 'Only caller scalars α,β∈ℝ≥0,η∈ℝ have the exact input constraints. J uses √η; the kernel uses midpoint 1/2 and denominator 8η; reflection coefficient is 2. γ=2√((α:ℝ)η)/(1+(α:ℝ)η), with positivity concluded. Same γ gives ΓP0−γI positivity, inverse norm≤1/γ, pair estimate /(2γ), and global quadratic estimate ‖f‖²/(2γ). C=(1/2)(‖u‖²−‖v‖²)−inner((A0*Inv)u,v). For every real omegaWeight∈(0,γ], L=‖f‖²+omegaWeight*C fP fV and exact coefficients 1/2,3/2,omegaWeight/(2γ) appear in all four final inequalities. No unspecified constants, strict endpoint replacement, extra β dependence in γ, or higher-derivative constant is introduced.'
}

COVERAGE = [
    ('input-structures','All five structures and dimension-zero case.'),
    ('input-scalars','V, NNReal α β, real η and coercions.'),
    ('input-hypotheses','All six hypotheses; both universal Hessian bounds; C² and closed step endpoint.'),
    ('mu','Normalized exponential tilt by −V.'),
    ('J','Product with standard Gaussian and exact √η pushforward.'),
    ('nu-Lambda-F','Second marginal and both exact reflection maps.'),
    ('mY-HP-P','Comap, internal product instance and Fact, measurable closed subspace, conditional expectation inclusion.'),
    ('hp-M','Internal measure-preserving second projection and pullback isometry.'),
    ('probabilities','All three probability conclusions.'),
    ('range-fixed','HP=P range and every HP element fixed.'),
    ('S','Existential Markov kernel; every-state exact tilt; conditional law; both marginals.'),
    ('e','Existential isometric equivalence and every-u equality with M.'),
    ('U','Existential isometry; every-g AE reflection action; involutive; self-adjoint.'),
    ('T','Existential self-adjoint contraction; every-u kernel AE action and integral preservation.'),
    ('A-B','Exact definitions, conjugation, A self-adjoint contraction, PB=0.'),
    ('Gamma','Positive root, square identity and commutation.'),
    ('GammaP','Conjugated positive root, square identity, commutation and B*B.'),
    ('q','Constant-one AE, fixed point, every-u integral pairing.'),
    ('HP0','Exact kernel, inherited complete Hilbert structures, every-f zero-mean iff.'),
    ('gamma','Exact positive scalar, ΓPqP=0.'),
    ('GammaP0','Every-f restriction, positive root/lower bound and unit.'),
    ('Inv','Same two-sided inverse, norm bound and self-adjointness.'),
    ('A0','Every-u restriction, self-adjoint, root commute, squares sum I, inverse commute.'),
    ('A0Inv','Self-adjoint product and exact I+product²=Inv².'),
    ('C','Exact quadratic formula and every-pair bound.'),
    ('Hperp','Exact conditional-expectation kernel and inherited complete structures.'),
    ('B0','Existential restriction with every-f ambient equality.'),
    ('V0','Two factorization identities, V0*V0=I, every-f norm equality, no onto addition.'),
    ('R','Existential residual map; every-g ambient equality g−Pg.'),
    ('adjoint-all','Every-g full ambient adjoint using R and B0*.'),
    ('centered-forall','Every globally centered joint f implies existential centered fP.'),
    ('fP','Exact conditional-expectation equation.'),
    ('fperp-fV','Internal lets from same R and V0*.'),
    ('adjoint-two','Both corrector adjoint/restriction equalities.'),
    ('energy-three','Pythagorean identity, corrector norm bound, combined norm-square bound.'),
    ('C-global','Global quadratic bound with exact denominator 2γ.'),
    ('weight-quantifier','∀omegaWeight:ℝ after ∃fP, antecedents 0<weight and weight≤γ; same fP for all weights.'),
    ('L','Exact let-defined L=‖f‖²+weight*C fP fV.'),
    ('L-lower','(1/2:ℝ)*‖f‖²≤L.'),
    ('L-upper','L≤(3/2:ℝ)*‖f‖².'),
    ('L-perturbation','|L−‖f‖²|≤(weight/(2γ))*‖f‖².'),
    ('L-cap','(weight/(2γ))*‖f‖²≤(1/2:ℝ)*‖f‖².'),
    ('scopes','Every existential conclusion, subtype, AE scope and earlier conjunction retained.'),
    ('endpoints','Zero dimensions/subspaces/observables, α=β, βη=1, legal αη=1 and weight=γ retained; excluded α=0,η=0,weight=0.'),
]

stage = sys.argv[1]
if stage == 'build':
    assert not (OUT / 'raw_input_manifest.json').exists()
    (OUT / 'snapshots').mkdir()
    (OUT / 'reconstructions').mkdir()
    raws = {name: original(name) for name in INPUTS}
    assert raws['lease.json'] == raws['initial-lease.raw.snapshot.json']
    assert json.loads(raws['lease.json'])['status'] == 'OPEN'
    manifest = {'schema_version': 1, 'normalization': 'CRLF byte pairs replaced by LF only; all other bytes preserved.', 'inputs': {}, **FLAGS}
    pins = []
    for name,raw in raws.items():
        raw_name = 'snapshots/' + name + '.raw.snapshot'
        lf_name = 'snapshots/' + name + '.lf.snapshot'
        lf = raw.replace(b'\r\n',b'\n')
        (OUT / raw_name).write_bytes(raw)
        (OUT / lf_name).write_bytes(lf)
        manifest['inputs'][name] = {'original_path': str(BASE / name), 'raw_sha256': sha(raw), 'bytes': len(raw), 'mtime_ns': (BASE / name).stat().st_mtime_ns, 'raw_snapshot': raw_name, 'lf_snapshot': lf_name, 'lf_sha256': sha(lf), 'lf_bytes': len(lf)}
        pins.append({'input': name,'raw_snapshot':raw_name,'lf_snapshot':lf_name,'raw_sha256':sha(raw),'lf_sha256':sha(lf)})
    save('raw_input_manifest.json',manifest)
    save('finite_pin_mappings.json',{'input_count':3,'pins':pins,'no_other_input_files_read':True})
    packet = json.loads(raws['packet0.json'])
    assert sha(packet['lean']['statement'].encode('utf-8')) == packet['lean']['statement_sha256']
    complete = TEXT + '\nFULL LITERAL STATEMENT (verbatim supplied Lean type):\n' + packet['lean']['statement'] + '\n'
    named = 'reconstructions/packet0.complete-reconstruction.txt'
    raw_complete = complete.encode('utf-8')
    (OUT / named).write_bytes(raw_complete)
    rec = {
        'packet_id':packet['packet_id'],'input_filename':'packet0.json',
        'lean_statement_literal':packet['lean']['statement'], 'lean_statement_sha256':packet['lean']['statement_sha256'],
        'approved_definition_context_used':packet['lean']['approved_definition_context'],
        'reconstructed_theorem_text':complete,'reconstructed_text_sha256':sha(raw_complete),'named_reconstruction_file':named,
        **SLOT_TEXT,
        'seven_slot_coverage':{slot:{'status':'covered','field':slot} for slot in SLOTS},
        'clause_coverage':[{'clause_id':cid,'status':'retained','description':desc} for cid,desc in COVERAGE],
        'decoder':'independent-source-blind-semantic-reconstructor','decoder_run_sha256':'',**FLAGS,
        'source_fidelity_verdict':'not assessed',
        'remaining_uncertainty':'Supplied statement/context reconstruction only. No source identity/text, source comparison, compiler, or mathematical proof was inspected. compiled=true remains unverified packet metadata.'
    }
    save('reconstruction_payload.json',{'schema_version':1,'task':'independent-source-blind-semantic-reconstruction','decoder':rec['decoder'],'decoder_run_sha256':'',**FLAGS,'reconstructions':{packet['packet_id']:rec}})
    save('lease.json',{'status':'OPEN','allowed_inputs':INPUTS,'root_parent_lease_writable':False,**FLAGS})
    save('build_process.json',process_record(stage))
    print(json.dumps({'status':'BUILD_DONE',**process_record(stage)},sort_keys=True))

elif stage == 'finalizer':
    manifest = original_checks()
    packet,payload,rec = payload_checks()
    terminal_check('terminal_build.json')
    run = {
        'schema_version':1,'task':'independent-source-blind-semantic-reconstruction','decoder':payload['decoder'],**FLAGS,
        'allowed_input_count':3,'allowed_inputs':sorted(INPUTS),'packet_count':1,
        'packet_records':{packet['packet_id']:{'packet_filename':'packet0.json','statement_sha256':rec['lean_statement_sha256'],'reconstruction_file':rec['named_reconstruction_file'],'reconstruction_raw_sha256':rec['reconstructed_text_sha256'],'seven_slots':{slot:rec[slot] for slot in SLOTS},'clause_coverage':rec['clause_coverage']}},
        'raw_input_manifest_sha256':sha((OUT/'raw_input_manifest.json').read_bytes()),
        'finite_pin_mappings_sha256':sha((OUT/'finite_pin_mappings.json').read_bytes()),
        'actual_build_terminal_receipt_sha256':sha((OUT/'terminal_build.json').read_bytes()),
        'reconstruction_payload_path':'reconstruction_payload.json',
        'hash_rule':'SHA256 UTF-8 JSON ensure_ascii=false, sort_keys=true, separators=(comma,colon), removing ONLY top-level run_sha256. No other field removal/normalization.',
        'parent_lease_preserved_open':True,
        'semantic_scope':'Only neutral statement and approved definitions; no source/proof verification.',
        'finalizer_process_id':os.getpid(),'finalizer_parent_process_id':os.getppid()
    }
    run_hash = sha(canon(run))
    run['run_sha256'] = run_hash
    save('final_run.json',run)
    payload['decoder_run_sha256'] = run_hash
    rec['decoder_run_sha256'] = run_hash
    save('reconstruction_payload.json',payload)
    run_check()
    save('finalizer_results.json',{'status':'PASS','logical_run_sha256':run_hash,'logical_run_rule_removes_only_top_run_sha256':True,'packet_count':1,'seven_slots_checked':7,'clause_coverage_count':len(COVERAGE),'complete_literal_statement_retained':True,'four_exact_final_inequalities_retained':True,'weight_forall_after_fP_exists_retained':True,'all_input_raw_and_lf_snapshots_exact':True,'parent_lease_open_raw_and_mtime_unchanged':True,**FLAGS,'source_fidelity_verdict':'not assessed','verified_transition':False})
    save('finalizer_process.json',process_record(stage))
    print(json.dumps({'status':'FINALIZER_DONE','logical_run_sha256':run_hash,**process_record(stage)},sort_keys=True))

elif stage == 'readback':
    original_checks()
    run,payload,rec = run_check()
    terminal_check('terminal_build.json')
    terminal_check('terminal_finalizer.json')
    save('readback_results.json',{'status':'PASS','logical_run_sha256':run['run_sha256'],'logical_run_removes_only_top_run_sha256':True,'raw_input_manifest_sha256':sha((OUT/'raw_input_manifest.json').read_bytes()),'reconstruction_payload_raw_sha256':sha((OUT/'reconstruction_payload.json').read_bytes()),'named_complete_reconstruction_raw_sha256':rec['reconstructed_text_sha256'],'seven_slots_checked':7,'clause_coverage_count':len(rec['clause_coverage']),'lean_literal_exact':True,'snapshots_raw_and_crlf_to_lf_only_exact':True,'parent_lease_open_raw_and_mtime_unchanged':True,'source_fidelity_verdict':'not assessed','verified_transition':False,**process_record(stage)})
    save('readback_process.json',process_record(stage))
    print(json.dumps({'status':'READBACK_DONE','logical_run_sha256':run['run_sha256'],**process_record(stage)},sort_keys=True))

elif stage == 'close':
    manifest = original_checks()
    run,payload,rec = run_check()
    assert read('lease.json')['status'] == 'OPEN'
    assert read('finalizer_results.json')['status'] == read('readback_results.json')['status'] == 'PASS'
    receipts = []
    for name in ['terminal_build.json','terminal_finalizer.json','terminal_readback.json']:
        t = terminal_check(name)
        receipts.append({'receipt_file':name,'receipt_raw_sha256':sha((OUT/name).read_bytes()),**t})
    save('terminal_manifest.json',{'completed_stage_count':3,'actual_completed_stage_receipts':receipts,'final_closing_process_id':os.getpid(),'final_closing_parent_process_id':os.getppid(),'final_closing_exit_evidence_location':'Authoritative exec_command return/stdout; no owned write after CLOSED_LAST lease.',**FLAGS})
    base_names = ['decoder_evidence.py','raw_input_manifest.json','finite_pin_mappings.json','reconstruction_payload.json','build_process.json','terminal_build.json','final_run.json','finalizer_results.json','finalizer_process.json','terminal_finalizer.json','readback_results.json','readback_process.json','terminal_readback.json','reconstructions/packet0.complete-reconstruction.txt']
    for name in INPUTS:
        base_names.extend(['snapshots/'+name+'.raw.snapshot','snapshots/'+name+'.lf.snapshot'])
    self_rows = file_rows(base_names+['terminal_manifest.json'])
    exact_rows(self_rows)
    save('self_manifest.json',{'schema_version':1,'finite_file_count':len(self_rows),'files':self_rows,'finite_rows_sha256':sha(canon(self_rows)),'exclusions':['self_manifest.json','closure_readback_results.json','closure_manifest.json','lease.json'],'exclusion_reason':'Avoid cyclic self-hashes; subsequent manifests and final lease bind these files.',**FLAGS})
    original_checks()
    save('closure_readback_results.json',{'status':'PASS','process_id':os.getpid(),'parent_process_id':os.getppid(),'self_manifest_raw_sha256':sha((OUT/'self_manifest.json').read_bytes()),'self_manifest_rows_count':len(self_rows),'self_manifest_rows_exact_hash_size_mtime_readback':True,'parent_lease_open_unchanged_raw_and_mtime':True,'logical_run_sha256_verified_removing_only_top_run_sha256':run['run_sha256'],**FLAGS,'remaining_uncertainty':'Reconstruction only; no source fidelity or proof correctness assessment.'})
    closure_names = base_names+['terminal_manifest.json','self_manifest.json','closure_readback_results.json']
    closure_rows = file_rows(closure_names)
    exact_rows(closure_rows)
    save('closure_manifest.json',{'schema_version':1,'finite_file_count':len(closure_rows),'files':closure_rows,'finite_rows_sha256':sha(canon(closure_rows)),'normalization_for_rows_hash':'UTF-8 JSON list; ensure_ascii=false; sort_keys=true; separators=(comma,colon). File digests are RAW; mtime_ns integer.','excluded_self':'closure_manifest.json','excluded_mutable_final_lease':'lease.json','closure_manifest_itself_bound_by_final_lease':True})
    final_names = closure_names+['closure_manifest.json']
    final_rows = file_rows(final_names)
    actual_names = sorted(str(p.relative_to(OUT)).replace('\\','/') for p in OUT.rglob('*') if p.is_file())
    assert actual_names == sorted(final_names+['lease.json'])
    exact_rows(final_rows)
    assert read('closure_manifest.json')['files'] == closure_rows
    original_checks()
    closure_hash = sha(canon(final_rows))
    lease = {
        'status':'CLOSED_LAST','allowed_inputs':INPUTS,**FLAGS,
        'parent_lease_open_and_unchanged':True,'parent_lease_raw_sha256':manifest['inputs']['lease.json']['raw_sha256'],'initial_parent_lease_raw_sha256':manifest['inputs']['initial-lease.raw.snapshot.json']['raw_sha256'],
        'whole_logical_run_sha256':run['run_sha256'],'reconstruction_payload_raw_sha256':sha((OUT/'reconstruction_payload.json').read_bytes()),
        'named_reconstructions':{rec['packet_id']:{'path':rec['named_reconstruction_file'],'raw_sha256':rec['reconstructed_text_sha256']}},
        'raw_input_manifest_raw_sha256':sha((OUT/'raw_input_manifest.json').read_bytes()),'closure_manifest_raw_sha256':sha((OUT/'closure_manifest.json').read_bytes()),
        'closure_manifest_file_count_excluding_itself_and_lease':len(closure_rows),'closure_count':len(final_rows),'closure_count_scope':'All immutable owned files including closure_manifest.json; excludes final lease.json only.',
        'closure_sha256':closure_hash,'closure_hash_rule':'SHA256 canonical JSON list sorted path,bytes,raw_sha256,mtime_ns; includes closure_manifest.json and excludes lease.json only.','immutable_file_rows':final_rows,'total_owned_file_count_including_lease':len(final_rows)+1,
        'exact_finite_count_hash_size_mtime_readback_before_close':True,
        'actual_completed_terminal_pids':[t['process_id'] for t in receipts],'actual_completed_terminal_shell_pids':[t['shell_process_id'] for t in receipts],'actual_completed_terminal_exit_statuses':[t['exit_status'] for t in receipts],
        'last_writer_process_id':os.getpid(),'last_writer_parent_process_id':os.getppid(),'last_writer_exit_evidence':'Authoritative exec_command stdout/exit code; no owned writes follow this lease.','closed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'last_owned_write':'lease.json',
        'source_fidelity_verdict':'not assessed','verified_transition':False,'remaining_uncertainty':'No source text/identity or compiler consulted. Statement/context reconstruction only; no source fidelity, independent proof or VERIFIED claim.'
    }
    save('lease.json',lease)
    # Read-only after the final owned write.
    raw_lease = (OUT/'lease.json').read_bytes()
    assert json.loads(raw_lease)['status'] == 'CLOSED_LAST'
    print(json.dumps({'status':'CLOSED_LAST','last_writer_process_id':os.getpid(),'last_writer_parent_process_id':os.getppid(),'whole_logical_run_sha256':run['run_sha256'],'complete_reconstruction_payload_raw_sha256':lease['reconstruction_payload_raw_sha256'],'named_reconstructions':lease['named_reconstructions'],'separate_raw_input_manifest_sha256':lease['raw_input_manifest_raw_sha256'],'closure_count':len(final_rows),'closure_sha256':closure_hash,'closure_manifest_raw_sha256':lease['closure_manifest_raw_sha256'],'lease_raw_sha256':sha(raw_lease),'actual_completed_terminal_pids':lease['actual_completed_terminal_pids'],'actual_completed_terminal_exit_statuses':lease['actual_completed_terminal_exit_statuses'],'parent_lease_status':'OPEN','parent_lease_unchanged':True,**FLAGS,'exit_evidence':'Actual close process exit supplied by exec_command after stdout.'},sort_keys=True))
else:
    raise SystemExit('Unknown evidence stage')
