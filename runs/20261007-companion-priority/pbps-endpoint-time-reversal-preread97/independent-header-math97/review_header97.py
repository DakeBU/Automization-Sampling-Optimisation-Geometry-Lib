"""Close an independent mathematical header audit. No theorem implementation."""
from pathlib import Path
import hashlib,json,re,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;P=O.parent
N=R/'runs/20261007-companion-priority/pbps-actual-phase-reversal-volume96/next-primary97'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def rel(p):return p.relative_to(R).as_posix()
def info(p):return dict(path=rel(p),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(n,v):
 p=O/n;assert not p.exists(),p;p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
H=P/'Header97.lean';F=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean';M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseReversalVolume.lean'
assert info(H)['raw_sha256']=='2f27a049026ab398bfc85cecf1b2a450e8fef17c45e3a79e8b492c731343800b'
ht=H.read_text(encoding='utf8');ft=F.read_text(encoding='utf8');ft=ft[ft.index('private def actual_finite_count_path_statement'):]
normal=lambda s:re.sub(r'\s+',' ',s).strip()
def binders(t):return t[t.index('{E : Type*}'):t.index(': Prop := by')]
assert normal(binders(ht))==normal(binders(ft))
def block(t,name):
 start=re.search(r'^    let '+re.escape(name)+r'(?=\s|:)',t,re.M);assert start,name
 end=re.search(r'^    (?:let |∃ |∀ )',t[start.end():],re.M)
 return t[start.start():start.end()+end.start()] if end else t[start.start():]
names=['c','Φ','S','Rec','Hist','Δ','Prefix','m','zAt','K','Path','Ψ','Γ']
matches=[]
for name in names:
 assert normal(block(ht,name))==normal(block(ft,name)),name
 matches.append(dict(name=name,literal_equal_after_whitespace_normalization=True))
receipt=load(P/'type-only1/receipt.json');assert receipt['exit_code']==0 and receipt['header_raw_sha256']==info(H)['raw_sha256'] and not receipt['theorem_credit']
assert (P/'type-only1/Header97.exactraw.lean').read_bytes()==H.read_bytes()
paths=[H,F,M,P/'type-only1/receipt.json',P/'type-only1/stdout.log',P/'type-only1/stderr.log',N/'next-edge-recommendation97.native.json',N/'jump-convention-audit97.native.json',N/'source-proof-graph97.native.json',N/'source-proof-graph97.preimplementation.native.json',N/'reuse-search97.native.json',R/'lean-toolchain',R/'lake-manifest.json']
paths += [R/'.lake/packages/mathlib/Mathlib'/x for x in ['Data/Fin/Rev.lean','MeasureTheory/Constructions/Pi.lean','MeasureTheory/Measure/Prod.lean','Dynamics/Ergodic/MeasurePreserving.lean','MeasureTheory/Measure/Typeclasses/SFinite.lean','MeasureTheory/Measure/Map.lean','MeasureTheory/Measure/Restrict.lean','MeasureTheory/Group/Measure.lean']]
snap=O/'inputs';snap.mkdir(exist_ok=False);inputs=[]
for i,p in enumerate(paths):
 q=snap/(str(i).zfill(2)+'.'+p.name+'.exactraw');q.write_bytes(p.read_bytes());inputs.append(dict(**info(p),snapshot=rel(q)))
decision=dict(kind='independent-mathematical-header-review',reviewer='/root/exact_verifier96',decision='ACCEPT_MATHEMATICALLY_SOUND_EXACT_HEADER_FOR_STATEMENT_SEAL',header=info(H),theorem_credit=False,implementation_created=False,formal_proof_started=False,required_repairs=[],independent_from_formalizer=True,source_review_role=False,scope='Independent mathematical plausibility/correctness and exact existing-definition audit, with pinned API inspection. Root successful type-only elaboration reused; no new Lean theorem or independent source-fidelity verdict.',inputs=inputs,literal_binder_audit=dict(six_analytic_binders_identical_to_actual93=True,ambient_instances_identical=True,extra_public_binders=[],analysis=['The ambient finite-dimensional real Borel Hilbert structures are the same as actual93/96. There is no positive-dimension or Nontrivial premise.','The six hAlpha,hAlphaBeta,hV,hH,hEta,hBetaEta binders are unchanged. No extra differentiability, nonzero-normal, positive-rate, volume, endpoint-inverse, joint-measurability or stationary-law provider is assumed.','The existential rho is inside forall n,T and outside forall y,r,z: it depends only on event count and horizon. Its coordinate equation uniquely determines it, including empty and singleton Prefix cases.']),existing_literal_matches=matches,
mathematical_challenges=[
 dict(topic='strict simplex and Fin.rev',verdict='sound',reason='StrictMono(cons 0 t) gives 0<t_i and t_i<t_j for i<j. Fin.rev reverses strict order. Thus 0<T-t_(rev i)<T and increasing i gives increasing complemented coordinate. Applying the map twice yields T-(T-t_i)=t_i. No positive-T premise is needed: positive n at T=0 has no Prefix inhabitants.'),
 dict(topic='exact time measure',verdict='sound',reason='On ambient Fin n -> R the affine map q(t)_i=T-t_(rev i) is coordinate reversal followed by scalar reflections. Both preserve the finite product Lebesgue volume, including n=0. The measurable strict simplex is exactly invariant. Restrict ambient volume to Delta, then use map_comap_subtype_coe and injectivity of pushforward by the measurable subtype embedding. This proves preservation of the literal comap measure, with no factorial or probability normalization.'),
 dict(topic='actual endpoint identification',verdict='sound',reason='All thirteen inherited literals c,Phi,S,Rec,Hist,Delta,Prefix,m,zAt,K,Path,Psi,Gamma match actual93. At terminal evaluation the last history time is <=T: it is zero for n=0 and t_(n-1)<T otherwise. No larger Fin(n+1) index exists. ActualFiniteCountPath final-interval clause therefore gives exactly the displayed final-flow formula. NNReal truncated subtraction equals the real difference because this inequality is proved.'),
 dict(topic='joint measurability',verdict='sound',reason='At fixed n,T the actual93 Gamma is jointly measurable in ((y,r),z,t). Evaluation at the fixed terminal coordinate is measurable for the coordinate-product path sigma algebra. R is measurable; rho is a continuous ambient affine map restricted to measurable subtype. Pairing yields the stated joint Theta. This does not assert joint measurability in a varying dependent horizon or continuity of the state-dependent bounce.'),
 dict(topic='finite phase volume',verdict='sound',reason='Let t_0=0,t_(n+1)=T and d_j=t_(j+1)-t_j. zAt_j consists of j factors S after Phi_d. At fixed t every factor preserves the exact ell=volume_E.prod volume_E by actual96. Its finite composition and final flow preserve ell, and so does R after the endpoint.'),
 dict(topic='finite reversed-word inverse',verdict='sound',reason='Forward endpoint P_d=Phi_(d_n) o S o Phi_(d_(n-1)) o ... o S o Phi_(d_0). The reversed tuple has gaps d_n,...,d_0, so P_rev=Phi_(d_0) o S o ... o S o Phi_(d_n). Since R Phi_d R=Phi_-d, R S R=S and S inverse=S, one has P_rev=R o P_d^{-1} o R; equivalently P_rev(R(P_d z))=R z. This is precisely the header equality. State dependence of S is harmless because S is one fixed global map at fixed r; no reflection matrix is frozen across positions.'),
 dict(topic='Theta involution and product order',verdict='sound',reason='Its square has phase R(P_rev(R(P_d z)))=z and time rho(rho(t))=t. For preservation use (t,z)->(rho(t),R(A(z,t))) on Prefix x phase. rho preserves m and every jointly measurable fiber preserves ell. skew_product gives m.prod ell preservation. Conjugating by the product swap yields exactly ell.prod m in the header. One must not feed phase as base while the base map depends on t.'),
 dict(topic='SFinite obligation',verdict='derived internally',reason='Delta is Borel from finitely many strict inequalities. map(Subtype.val,m)=volume.restrict Delta, which is sigma-finite. SigmaFinite.of_map with measurable_subtype_coe derives SigmaFinite m, hence SFinite m; finite-dimensional phase volume and its product are sigma-finite. The skew-product hypotheses are therefore consequences, not missing public binders.'),
 dict(topic='degenerate cases',verdict='sound',reason='n=0: Prefix is singleton with product-volume mass one; A=Phi_T and Theta=R Phi_T with square identity. n>0,T=0: Prefix empty, m=0. n=T=0: Theta phase map R because Phi_0=id. rank(E)=0: ell has singleton mass one and only time reversal remains. At zero gradient residual S=id and the maps remain Borel; tuples are not restricted to positive-probability or positive-rate jumps.'),
 dict(topic='jump values and downstream boundary',verdict='correctly excluded',reason='Only the endpoint and finite time tuple are reversed. The header does not assert equality of right-continuous paths at jumps; reversed post-bounce values correspond to original pre-bounce values. No Gibbs density cocycle, weight matching, fixed-time invariance, restart/Markovness, cost, main-paper or actual-input composition theorem is hidden in the conclusion.')],
api_audit=[
 dict(names=['Fin.rev_involutive','Fin.revPerm','Fin.rev_lt_rev'],role='Exact finite index reversal; no n>0 restriction.'),
 dict(names=['volume_measurePreserving_piCongrLeft','volume_preserving_pi','Measure.measurePreserving_sub_left'],role='Ambient finite product volume; scalar T-x API is to_additive counterpart of the inspected measurePreserving_div_left declaration.'),
 dict(names=['MeasurePreserving.restrict_preimage','measurePreserving_subtype_coe','Measure.map_comap_subtype_coe','MeasurableEmbedding.map_injective'],role='Invariant measurable restriction and exact subtype comap transport; no change of measure.'),
 dict(names=['SigmaFinite.of_map','MeasurePreserving.skew_product','Measure.measurePreserving_swap'],role='Actual SFinite instances, jointly measurable fibers and correct product coordinate order.'),
 dict(names=['actual_finite_count_path_law','actual_phase_reversal_volume_laws'],role='Public compiled parents supply actual endpoint/Borel and individual phase map laws; private source helper names are not assumed public callable APIs.')],
route_at_most_seven_steps=[
 'Project actual93 joint Gamma and terminal interval identification and actual96 phase laws using the exact literal binders; record terminal gap for n=0 explicitly.',
 'Build the unique rho subtype map from complement after Fin.rev; prove strict-simplex membership, coordinate equation, measurability and involution.',
 'Prove ambient affine permutation preserves finite product volume; restrict to invariant Borel Delta and transport through subtype comap. Derive SigmaFinite m from its mapped restricted volume.',
 'Define the finite arc gaps and identify actual zAt/final endpoint with the alternating flow-bounce word. Induct to obtain phase-fiber volume preservation and retain inherited endpoint joint measurability.',
 'Prove reversed tuple gaps are exactly the reversed original gaps, including the first/terminal arcs; cancel the reversed word using both flow inverses, S involution, R conjugation and RS=SR.',
 'Construct Theta as the actual endpoint followed by R paired with rho. Derive its exact involution from the endpoint inverse and rho involution.',
 'Apply skew_product on Prefix x phase using derived SFinite and joint Borel fibers; swap both sides to ell.prod m and package precisely the proposed conclusions.' ],
failure_policy='If finite word/index or subtype-measure APIs stall, classify the concrete route as API/implementation blocked and isolate the smallest needed exact lemma. Do not replace Gamma with an unrelated word, add inverse/measure-preserving providers, weaken to a.e. endpoint equality, or assume positive dimension/rate/horizon. The header is mathematically sound but this review is not a completed proof.',
type_only_evidence=dict(origin='root type-only1',exit_code=0,header_raw_sha256=info(H)['raw_sha256'],independent_duplicate_build=False,no_theorem_proof=True),
source_graph_boundary='Read source-only recommendation/graphs as proposed topology, not theorem certificates or a prior header approval. Their K97 label denotes the conceptual endpoint/time map; the concrete header correctly names that map Theta and retains K for history. Separate independent source review is still required.',
observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),mathlib_revision=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=R).decode().strip())
assert len(decision['route_at_most_seven_steps'])==7
write('header-math-decision97.native.json',decision)
for x in inputs:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
write('closed-RAW-manifest97.native.json',dict(kind='closed-independent-header-mathematical-review',reviewer='/root/exact_verifier96',header_raw_sha256=info(H)['raw_sha256'],theorem_credit=False,self_excluded=True,files=[info(p) for p in sorted(O.rglob('*')) if p.is_file() and '__pycache__' not in p.parts],all_input_raws_rechecked=True,no_shared_edits=True,no_96_closed_raw_edits=True))
for name in ['header-math-decision97.native.json','closed-RAW-manifest97.native.json']:print(json.dumps(info(O/name)),flush=True)
