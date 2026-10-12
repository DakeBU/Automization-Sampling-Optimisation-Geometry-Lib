import gzip
import hashlib
import json
import re
from pathlib import Path

ROOT=Path('E:/Samplinglib')
OUT=Path(__file__).resolve().parent
PRE=OUT.parent
PROD=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2FlipDuality.lean'
PRIOR=ROOT/'runs/20261007-companion-priority/pbps-actual-l2-flip-duality108/next-primary109/independent-topology109'
def digest(b): return hashlib.sha256(b).hexdigest()
def binding(p):
    b=p.read_bytes()
    return dict(path=str(p),raw_sha256=digest(b),bytes=len(b))
def save(name,value):
    p=OUT/name
    if p.exists(): raise RuntimeError('Preserve native output: '+str(p))
    p.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    return p
def segment(t,start,end):
    i=t.index(start)
    return t[i:t.index(end,i)]

header=PRE/'Header109.lean'
hb=header.read_bytes()
h=hb.decode('utf-8')
p=PROD.read_bytes().decode('utf-8')
receiptpath=PRE/'type-only1/receipt.json'
receipt=json.loads(receiptpath.read_bytes().decode('utf-8'))
stdout=PRE/'type-only1/stdout.log'
stderr=PRE/'type-only1/stderr.log'
bindpat=r'    \{E : Type\*\}.*? : Prop := by'
adjpat=r'∀ T : ℝ≥0, \(A T\).adjoint =\s+J.toContinuousLinearMap.comp \(\(A T\).comp J.toContinuousLinearMap\)'
hd=segment(h,'    let c :','    ∃ Z :')
pd=segment(p,'    let c :','    ∃ Z :')
checks=dict(kind='independent exact Header109 comparison and type receipt',
 reviewer='/root/blind_decoder106',header=binding(header),producer108=binding(PROD),
 expected_header_hash_matches=digest(hb)=='927043eaaace6083ec00c750037e4c69f21173595b85646bb9a5a1b63795e31b',
 expected_producer_hash_matches=binding(PROD)['raw_sha256']=='2358ce3e7a74b5d1ebdf857be873588db3ffdefd08239b7f2df37bf6b72349cd',
 six_binders_and_ambient_literal_equal=re.search(bindpat,h,re.S).group()==re.search(bindpat,p,re.S).group(),
 inherited37_definitions_literal_equal=hd==pd,inherited_definition_count=len(re.findall(r'^    let ',hd,re.M)),
 globalZ_through_J_involution_prefix_literal_equal=segment(h,'    ∃ Z :','            (∀ T : ℝ≥0, (A T).adjoint')==segment(p,'    ∃ Z :','            ∀ T : ℝ≥0, (A T).adjoint'),
 inherited_all_time_adjoint_block_literal_equal=re.search(adjpat,h,re.S).group()==re.search(adjpat,p,re.S).group(),
 globalZ_existential_count=h.count('∃ Z :'),familyA_existential_count=h.count('∃ A : ℝ≥0'),
 hR_existential_count=h.count('∃ hR :'),hfst_existential_count=h.count('∃ hfst :'),
 new_constructs=['mu := volume.tilted(-Vy_y)','hfst : MeasurePreserving Prod.fst (nu y) mu as output','B := canonical Lp pullback along Prod.fst','M := B.toContinuousLinearMap.adjoint','Kpos T := M.comp ((A T).comp B.toContinuousLinearMap)'],
 type_receipt=receipt,type_receipt_binding=binding(receiptpath),stdout_binding=binding(stdout),stderr_binding=binding(stderr),
 type_receipt_exact_header_hash_matches=receipt['header_raw_sha256']==digest(hb),type_exit_code=receipt['exit_code'],
 stdout_unused_Prop_binder_warning_count=stdout.read_text(encoding='utf-8').count('warning: Variable name'),
 stderr_empty=stderr.stat().st_size==0,
 typecheck_provenance='Root-run lake env lean; this reviewer checked the final exit0 receipt, exact header hash, #check signature and logs. No independent rerun or109 proof compilation is asserted.',
 prior_independent_graph_decision=binding(PRIOR/'decision109.native.json'),
 prior_independent_graph_RAW_closure=binding(PRIOR/'closed-RAW-topology109.native.json'),
 comparison_method='Nonempty exact string slices and exact regular-expression matches; the only inherited logical formatting change is wrapping its final all-time adjoint block in parentheses before appending the new conjunct.')
assert all(checks[k] for k in ('expected_header_hash_matches','expected_producer_hash_matches','six_binders_and_ambient_literal_equal','inherited37_definitions_literal_equal','globalZ_through_J_involution_prefix_literal_equal','inherited_all_time_adjoint_block_literal_equal','type_receipt_exact_header_hash_matches','stderr_empty'))
assert receipt['exit_code']==0 and checks['inherited_definition_count']==37
assert all(checks[k]==1 for k in ('globalZ_existential_count','familyA_existential_count','hR_existential_count','hfst_existential_count'))
save('header-comparison109.native.json',checks)
review=[
 dict(topic='Original binders and all108 outputs',status='PASS',reason='Full ambient typeclasses and original six analytic hypotheses match108 literally. All37 original lets match literally. The complete globalZ contract, same existential all-time A family, contraction/section-integrability/actual-expectation quotient/square bound, hR, canonical J representative and involution, and all-time flip adjoint identity remain conjuncts. No original output was dropped or weakened.'),
 dict(topic='Witness and quantifier scope',status='PASS',reason='One Z precedes all y,xRef. Inside each parameter pair one A precedes all T and all G. hR and its canonical J remain in that same existential scope. Only then mu, hfst, B and M are introduced, followed by a universal Gaussian-average property and the definition Kpos. B/M are fixed before G; Kpos is fixed before T/f. No separately existential replacement Z, A or J is introduced. The extra exists hfst is a proof output, not a source hypothesis.'),
 dict(topic='Canonical lift and averaging types',status='PASS',reason='mu is exactly volume.tilted(fun x => -Vy y x), definitionally the first factor of nu y. hfst proves projection measure preservation. B is exactly Lp.compMeasurePreservingₗᵢ ℝ Prod.fst hfst from position L2 to phase L2, and M is its continuous-linear-map adjoint in the reverse direction. The B representative is f(z.1) AE. Both norm bounds are <=1, appropriate even for trivial spaces. M.comp B=id is the isometry adjoint identity.'),
 dict(topic='Finite tilted measure is sufficient',status='PASS',reason='The literal tilted measure has an internal zero-or-probability instance, hence finite and SFinite. stdGaussian E is probability, hence finite and SFinite; the product is finite. measurePreserving_fst needs Gaussian probability, not a new position probability or positive-normalizer premise. Finite measures give L2-to-L1 and the pinned product Fubini/slicing hypotheses. Completeness of real L2 is already supplied by Mathlib. A separate103 producer or dimension-positivity assumption is unnecessary.'),
 dict(topic='Arbitrary Gaussian representative identification',status='PASS',reason='For every raw G and hG:MemLp G 2 (nu y), the conclusion gives mu-AE Gaussian-integrable sections and exists hbar:MemLp gbar 2 mu with M[hG]=[gbar], for literal gbar(x)=integral G(x,p) dstdGaussian. M was constructed before testing G. Internally prove raw G and gbar are L1, compare every measurable-set integral via the adjoint pairing with L2 indicators and signed Fubini, obtain AE equality with the existing L2 class M[G], then transfer MemLp and identify toLp. This needs no Borel or extra integrability binder and avoids circular use of gbar in L2.'),
 dict(topic='Flip absorption, adjoint direction and contraction',status='PASS',reason='J(B f)=B f follows from the two canonical AE pullback representatives, transport by hR and fst(R z)=fst z. J is an involutive isometry, so internally J.adjoint=J; taking adjoints of J B=B yields M J=M. Kpos is exactly M A_T B. Thus Kpos.adjoint=M A_T.adjoint B=M J A_T J B=Kpos; norm composition and the three inherited/derived bounds give <=1. No sign, time rescaling or Gaussian normalization factor is introduced. The internal J self-adjointness is a proof ingredient, not a requested premise.'),
 dict(topic='Actual nested position expectation',status='PASS',reason='For each T and arbitrary f with hf:MemLp f 2 mu, kTf is exactly the Gaussian-outer, P-clock-inner integral of the position component of the same Z(y,xRef,(x,p),T,w). Lift F=f composed fst using hfst, identify B[f]=[F], then use the same A_T108 universal expectation property. Its clock-section integrability slices to mu-AE x, Gaussian-AE p using ae_ae_of_ae_prod. Its MemLp opF input satisfies the universal M Gaussian-identification clause, yielding outer integrability mu-AE and hk:MemLp kTf with Kpos_T[f]=[kTf]. There is no reversed integral order, omitted position projection or assertion of every-section integrability.'),
 dict(topic='AE scope, zero time and rank zero',status='PASS',reason='Every AE claim is after its observable and parameters; no uniform null set or pointwise arbitrary-quotient representative equality is claimed. T=0 is included and Kpos0=id follows from A0=id and M B=id. Finite-dimensional rank0 remains allowed. If the generic tilted measure were zero, position and phase L2 become trivial and the stated inequalities/identities and AE claims remain valid. No hidden nontrivial-space binder is needed.'),
 dict(topic='Ingredient and source boundary',status='PASS',reason='Every mathematical obligation matches the already independently admitted109 graph: lift/adjoint construction, L1 Fubini, universal Gaussian identification, flip absorption, compressed operator and nested position identification. No new source premise or strict smaller prerequisite is exposed by this exact header. It leaves Markov positivity/constant preservation, strong continuity, semigroup/restart, independent-reference half-turn averaging, complexL2, cost and full-paper conclusions outside the statement.'),
 dict(topic='Type-only result',status='PASS',reason='The exact header raw hash matches the final root receipt with exit0. stdout contains #check candidate and exactly six unused-Prop-binder lint warnings; stderr is empty. These binders remain visible in #check and are intentionally retained for source fidelity. This compiles a Prop-valued definition only and supplies no proof of that proposition.')
]
decision=dict(kind='independent exact prospective Header109 mathematical admission',reviewer='/root/blind_decoder106',
 decision='ACCEPT_EXACT_HEADER109_FOR_SEAL_AND_PROOF',input_path=str(header),input_RAW_sha256=digest(hb),
 producer108_RAW_sha256=binding(PROD)['raw_sha256'],type_receipt_RAW_sha256=binding(receiptpath)['raw_sha256'],
 type_only_exit_code=0,mathematical_review=review,blocking_findings=[],required_repairs=[],
 implementation_pitfalls=['Keep the exact108 Z/A/J witnesses throughout all new conjuncts.','Prove Gaussian-average L1 before identifying it with M[G]; derive its MemLp only after AE equality.','Use AE transport for pullback representatives; arbitrary MemLp raw inputs need not be Borel.','Keep Gaussian outer and clock inner integrals in the stated order; derive the two AE integrability outputs separately.','Derive finite/SFinite/probability instances internally; do not turn them into source binders.'],
 scope=dict(header_review_only=True,blind_decoder=False,proof109_written=False,new_SAU_claim=False,canonical_mutation=False,source_graph_mutation=False,
  theorem_completion_admitted=False,prior_reviews_preserved=True,
  remaining='Statement Seal, implementation, independent compiled/source verification, publication and integration are separate gates.'),
 evidence='header-comparison109.native.json')
save('header-math-decision109.native.json',decision)
for src,name in ((header,'Header109.reviewed.exactraw.lean'),(receiptpath,'type-only1.receipt.exactraw.json'),(stdout,'type-only1.stdout.exactraw.log'),(stderr,'type-only1.stderr.exactraw.log')):
    dest=OUT/name
    if dest.exists(): raise RuntimeError('Preserve snapshot')
    dest.write_bytes(src.read_bytes())
artifacts=[]
for f in sorted(OUT.iterdir()):
    if f.is_file() and not f.name.endswith('.raw.gz'):
        raw=f.read_bytes()
        gz=f.with_name(f.name+'.raw.gz')
        if gz.exists(): raise RuntimeError('Preserve RAW archive')
        gz.write_bytes(gzip.compress(raw,mtime=0))
        back=gzip.decompress(gz.read_bytes())
        assert back==raw
        artifacts.append(dict(path=f.name,raw_sha256=digest(raw),bytes=len(raw),archive=gz.name,gzip_sha256=digest(gz.read_bytes()),decompressed_sha256=digest(back),roundtrip_verified=True))
assert header.read_bytes()==hb
closure=save('closed-RAW-header-math109.native.json',dict(kind='closed independent Header109 mathematical RAW evidence',reviewer='/root/blind_decoder106',status='closed',
 decision=decision['decision'],input_header_RAW_sha256=digest(hb),output_hashes=artifacts,
 closure_excluded_from_own_hash_list=True,no_theorem_credit=True,no_production_or_canonical_mutation=True))
print(json.dumps(dict(decision_raw_sha256=binding(OUT/'header-math-decision109.native.json')['raw_sha256'],closure_raw_sha256=binding(closure)['raw_sha256']),indent=2))
