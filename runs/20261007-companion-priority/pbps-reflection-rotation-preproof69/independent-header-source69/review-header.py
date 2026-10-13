import collections,datetime,hashlib,json,os,pathlib,re
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def read(n):return (out/n).read_bytes()
definition=read('candidate.statement0.definition.lean');expanded=read('candidate.header0-expanded.lean');public=read('candidate.header0-public.lean');parent=read('parent67.statement.exact-RAW.fragment.lean')
text=definition.decode('utf-8');xt=expanded.decode('utf-8');pt=public.decode('utf-8')
start=text.index('                          let D : Hperp')
end=text.index('                          (∀ f : Lp ℝ 2 J',start)
delta=text[start:end]
assert delta==('                          let D : Hperp →L[ℝ] Hperp :=\n'
 '                            R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL\n'
 '                          (∀ h : Hperp, (D h : Lp ℝ 2 J)=\n'
 '                            U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J))) ∧\n'
 '                          V0.adjoint ∘L D = -(A0 ∘L V0.adjoint) ∧\n')
reconstructed=(text[:start]+text[end:]).replace('private def actual_reflection_intertwining_statement\n','private def actual_same_root_inverse_commutation_statement\n',1)
assert reconstructed.rstrip('\r\n')==parent.decode('utf-8').rstrip('\r\n')
body_marker='    let μ :='
assert xt[xt.index(body_marker):]==text[text.index(body_marker):]
xp=xt[:xt.index(body_marker)].split('\n',1)[1]
dp=text[:text.index(body_marker)].split('\n',1)[1]
assert xp.rstrip().removesuffix(':').rstrip()==dp.rstrip().removesuffix(': Prop :=').rstrip() if hasattr(str,'removesuffix') else xp.rstrip()[:-1].rstrip()==dp.rstrip()[:-len(': Prop :=')].rstrip()
public_prefix=pt[:pt.index(' : actual_reflection_intertwining_statement')]
expanded_prefix=xt[:xt.index(body_marker)].rstrip()
assert public_prefix.rstrip()==expanded_prefix[:-1].rstrip()
assert pt.endswith('actual_reflection_intertwining_statement (E := E) (V := V) (α := α) (β := β) (η := η) hα hαβ hV hH hη hβη\n')
for b in [definition,expanded,public,parent]:
 assert not re.search(rb'\b(?:sorry|admit|axiom)\b|:=\s*by\b',b)
source_graph=json.loads(read('prior-primary69.source-proof-graph.json'))
expect=json.loads(read('prior-primary69.source-expectations.json'))
coverage=json.loads(read('prior-primary69.finite-coverage-manifest.json'))
source_regions=json.loads(read('prior-primary69.source-input-regions.json'))
source_nodes={x['id']:x for x in source_graph['nodes']}
assert expect['before_candidate69'] and source_graph['no_prior_graph_or_verdict_used']
assert sha(read('prior-primary69.source-proof-graph.json'))=='1b464d9452b722abbaa6e274872366d8771780f96bc263dfeeb86322c2e88b8c'
assert sha(read('prior-primary69.source-expectations.json'))=='c4580c95682580e8a3a0bc68585efa98c9c659e52c928a0a6dbfdbaa6dcc62cf'
assert coverage['count']==419 and coverage['unclassified']==0
regions={x['name']:x for x in source_regions['regions']}
for x in coverage['entries']:
 b=read('source.'+x['region']+'.RAW.html');offset=regions[x['region']]['source_RAW_range_end_exclusive'][0]
 a,z=x['source_RAW_range_end_exclusive'];assert sha(b[a-offset:z-offset])==x['RAW_sha256']
delta_bytes=delta.encode('utf-8')
(out/'new-D-semantics-and-intertwining.exact-RAW.fragment.lean').write_bytes(delta_bytes)
continuity=dict(schema='header-source69-exact-parent-contract-continuity-v1',actual_pid=os.getpid(),
 candidate_definition_RAW_sha256=sha(definition),expanded_header_RAW_sha256=sha(expanded),public_header_RAW_sha256=sha(public),
 parent_fragment_RAW_sha256=sha(parent),parent_full_module_RAW_sha256='8567673eba335e7c1209f8bd90ce510954426bd5bbcdef6ff53ea97889762748',
 normalization_only=['delete the exact five new D/semantic/intertwining lines','reverse private declaration identifier','ignore terminal CR/LF bytes when comparing the complete literal Prop'],
 entire_parent_contract_retained=True,no_other_propositional_or_binder_change=True,
 candidate_definition_and_expanded_body_exact=True,public_reference_and_original_callers_exact=True,
 new_delta_RAW_bytes=len(delta_bytes),new_delta_RAW_sha256=sha(delta_bytes),
 new_delta_definition_RAW_range=[len(text[:start].encode('utf-8')),len(text[:end].encode('utf-8'))],
 candidate_theorem_proof_body_seen=False,parent_proof_body_seen=False,Lean_elaboration_or_compiler_run=False)
put('exact-parent-continuity.json',continuity)

binders=[
 dict(name='E and five typeclasses',kind='representation',condition='finite-dimensional real inner product space with its Borel measurable structure',source='R^d with real L2; does not exclude d=0'),
 dict(name='V,alpha,beta,eta',kind='original-data',condition='V:E->R; alpha,beta nonnegative real types; eta:R',source='P0 original potential/curvature/scale'),
 dict(name='h_alpha',kind='original-source-hypothesis',condition='0<(alpha:R)',source='0<alpha'),
 dict(name='h_alpha_beta',kind='original-source-hypothesis',condition='alpha<=beta',source='0<alpha<=beta'),
 dict(name='hV',kind='original-source-hypothesis',condition='ContDiff R 2 V',source='V in C^2'),
 dict(name='hH',kind='original-source-hypothesis',condition='for all x,v, alpha||v||²<=D²V(x)[v,v]<=beta||v||²',source='S1.E1.m1 Hessian Loewner bounds'),
 dict(name='h_eta',kind='original-source-hypothesis',condition='0<eta',source='eta in (0,1/beta]'),
 dict(name='h_beta_eta',kind='original-source-hypothesis',condition='beta eta<=1 inclusive',source='same capped scale; endpoint retained')]
definitions=[
 dict(name='mu,J,nu,Lambda,F',kind='actual-source-definitions',meaning='normalized tilted target; independent Gaussian augmentation; Y marginal; reflected Y+/Y- pair; actual reflection'),
 dict(name='HP,P,M',kind='actual-source-definitions',meaning='Y-measurable L2 subspace; exact condExpL2; pullback isometry from actual marginal'),
 dict(name='S,e,U,T',kind='existential-source-witness-conclusions',meaning='actual explicit conditional kernel; exact macro identification; actual reflection pullback; compressed conditional operator'),
 dict(name='A,B',kind='actual-block-definitions',meaning='A=macro compression of SAME U; B=Pperp U P inclusion'),
 dict(name='Gamma,GammaP',kind='same-positive-root-output',meaning='positive square root equation for SAME T; exact e-transport and square equation for SAME A; commutation output'),
 dict(name='q,qP,HP0',kind='actual-constant-and-centered-space',meaning='q=1 a.e.; qP=e q; HP0=ker inner(qP,.), with exact mean-zero equivalence'),
 dict(name='GammaP0,Inv,A0',kind='centered-restriction-and-inverse-output',meaning='SAME root and A restrict to HP0; inverse only HP0, two-sided; all commutations and positivity are conclusions'),
 dict(name='Hperp,B0,V0,R',kind='actual-micro-and-polar-output',meaning='ker P; exact centered B; V0=B0 Inv and B0=V0 GammaP0; isometry into Hperp; Rg=g-Pg; full B* adapter retained'),
 dict(name='D',kind='new-canonical-local-definition',meaning='D=R U inclusion:Hperp->Hperp, not a free witness or public premise'),
 dict(name='D compression equation',kind='new-semantic-output',meaning='forall h:Hperp, inclusion(Dh)=U(inclusion h)-P(U(inclusion h)); exact Uperpperp compression'),
 dict(name='V0* D=-A0 V0*',kind='sole-new-mathematical-output',meaning='bounded-map equality Hperp->HP0; covers EVERY h in Hperp, outside retained forall-centered-f clause'),
 dict(name='forall centered f exists fP; fperp; fV',kind='retained-original-actual-decomposition-conclusion',meaning='original centered observable, exact actual projections, adjoint compatibility, Pythagoras and coefficient norm budget')]
put('binder-and-definition-audit.json',dict(schema='header-source69-binder-definition-audit-v1',
 public_binders=binders,definitions_and_output_quantifiers=definitions,public_analytic_hypothesis_count=6,
 new_public_hypotheses=[],missing_public_source_hypotheses=[],free_operator_providers=[],
 ingredient_equals_dependency_edge=True,source_hypothesis_equals_public_binder=True,
 all_original_parent_witnesses_and_conclusions_exactly_retained=True))

findings=[
 dict(id='R1',status='PASS',topic='original scope',detail='The six original analytic hypotheses are unchanged; finite-dimensional real Borel representation adds no analytic restriction or dimension positivity.'),
 dict(id='R2',status='PASS',topic='actual compression',detail='D is a let-bound map R U inclusion using the SAME inherited actual conditional projector and reflection. Its explicit all-h compression equation prevents an arbitrary operator substitute.',source_nodes=['P3','P4','P11']),
 dict(id='R3',status='PASS',topic='same root and polar',detail='Gamma is positive with Gamma²=I-T²; GammaP is its exact transport; GammaP0 is the exact centered restriction; Inv is two-sided only there; V0 is exactly B0 Inv. All are witness conclusions.',source_nodes=['P5','P6','P7','P8']),
 dict(id='R4',status='PASS',topic='centered cancellation domains',detail='V0*:Hperp->HP0 and A0:HP0->HP0 give both sides the correct centered codomain. The full B* adapter is retained; there is no new range or centeredness premise.',source_nodes=['P7','P9','P10']),
 dict(id='R5',status='PASS',topic='quantifier scope and sign',detail='V0.adjoint composed with D equals negative(A0 composed with V0.adjoint), as bounded maps on ALL Hperp. It is outside the retained centered-f conclusion and has the exact source negative sign.',source_nodes=['P11']),
 dict(id='R6',status='PASS',topic='rank zero and endpoint',detail='No nontrivial-space instance or positive-rank condition appears; beta eta<=1 remains inclusive; no alpha eta<1, gamma<1, or logarithmic denominator is introduced.'),
 dict(id='R7',status='PASS',topic='no onto V',detail='Only V0* V0=I and norm preservation are retained. No V0 V0*=I or surjectivity premise/conclusion appears; the microscopic orthogonal residual remains possible.',source_nodes=['P8','P12']),
 dict(id='R8',status='PASS',topic='parent continuity',detail='Deleting exactly the five new D/semantic/intertwining lines and reversing the private name reproduces the complete parent Prop, modulo terminal line endings only.'),
 dict(id='R9',status='PASS',topic='actual-input meaning',detail='The relation concerns actual source-built U,P,root,inverse,V0 and all actual micro inputs, rather than an arbitrary coefficient-vector rotation lemma.',source_nodes=['P11','P14','P19']),
 dict(id='R10',status='PASS',topic='consumer and completion boundary',detail='Frozen SPG real consumers are P14/B21 actual second projected component and P19/B4 shared error. No sharp-energy68 parent is needed or introduced. Rotation, B21 corrector change, and B4 decay remain subsequent obligations.'),
 dict(id='R11',status='UNASSESSED',topic='formal validity',detail='No body, proof search, compiler, implementation/API inspection, SAU claim, or proof verification is part of this header-only source admission.')]
decision=dict(schema='header-source69-independent-source-admission-v1',verdict='ADMIT_HEADER_ONLY_FOR_STATEMENT_SEAL_CONSIDERATION',
 exact_candidate_expanded_RAW_sha256=sha(expanded),source_expectations_frozen_prior_to_candidate=True,
 frozen_source_graph_RAW_sha256='1b464d9452b722abbaa6e274872366d8771780f96bc263dfeeb86322c2e88b8c',
 frozen_expectations_RAW_sha256='c4580c95682580e8a3a0bc68585efa98c9c659e52c928a0a6dbfdbaa6dcc62cf',
 findings=findings,missing_source_premises=[],extra_public_premises=[],source_semantic_repairs_required=[],
 exact_delta='forall h:Hperp, V0*(D h)=-A0(V0*h), SAME actual root/inverse/polar and actual D compression',
 direct_primary_anchors=source_nodes['P11']['primary_math'],real_consumers=[source_nodes['P14'],source_nodes['P19']],
 proof_checked=False,compiled=False,Statement_Seal=False,SAU_claim=False,B21_complete=False,B4_complete=False,full_paper_complete=False,
 visibility=dict(candidate_header_only=True,parent_complete_Prop_fragment_only=True,parent_module_opaque_hash_only=True,
  no_68_reviews_or_decoders_or_bodies=True,no_candidate_proof_body=True,no_canonical_Git_or_ledger_edits=True))
put('header-source-decision.json',decision)

anchors=[
 ('signature-and-original-callers',0,xt.index(body_marker),['P0']),
 ('actual-law-and-projector-definitions',xt.index(body_marker),xt.index('    IsProbabilityMeasure'),['P1','P2','P3']),
 ('actual-source-witnesses-S-e-U-T',xt.index('    IsProbabilityMeasure'),xt.index('            let A :'),['P1','P2','P3','P4']),
 ('actual-A-B-compression',xt.index('            let A :'),xt.index('            ∃ Γ :'),['P4']),
 ('same-positive-root-and-transport',xt.index('            ∃ Γ :'),xt.index('              ∃ q :'),['P5']),
 ('constants-and-centered-macro-space',xt.index('              ∃ q :'),xt.index('                ∃ ΓP0 :'),['P6','P7']),
 ('centered-root-inverse-and-A0',xt.index('                ∃ ΓP0 :'),xt.index('                    let Hperp :='),['P6','P7']),
 ('actual-micro-polar-adjoint-adapters',xt.index('                    let Hperp :='),xt.index('                          let D :'),['P8','P9','P10']),
 ('new-D-compression-and-all-micro-intertwining',xt.index('                          let D :'),xt.index('                          (∀ f : Lp ℝ 2 J'),['P4','P10','P11']),
 ('retained-original-centered-observable-decomposition',xt.index('                          (∀ f : Lp ℝ 2 J'),len(xt),['P12'])]
segments=[]
assert anchors[0][1]==0 and anchors[-1][2]==len(xt)
for j,(name,a,z,nids) in enumerate(anchors):
 assert j==0 or a==anchors[j-1][2]
 b=xt[a:z].encode('utf-8');ab=len(xt[:a].encode('utf-8'));zb=len(xt[:z].encode('utf-8'))
 segments.append(dict(id=name,RAW_range=[ab,zb],RAW_bytes=len(b),RAW_sha256=sha(b),
  first_line=xt[:a].count('\n')+1,last_line=xt[:z].count('\n'),source_nodes=nids,
  outcome='PASS-source-and-binder-match',primary_math_ids=sorted(set(r['id'] for n in nids for r in source_nodes[n]['primary_math']))))
assert sum(x['RAW_bytes'] for x in segments)==len(expanded)
draft=json.loads(read('candidate.header-draft69.RAW.json'))
metadata=[dict(field=k,role='review-scope-and-attribution-only-not-a-source-hypothesis',covered=True) for k in sorted(draft)]
finite=dict(schema='header-source69-finite-coverage-manifest-v1',
 current_named_input_count=22,candidate_files_fully_covered=4,parent_complete_header_fragment_fully_covered=True,
 expanded_header_RAW_bytes=len(expanded),expanded_header_lines=len(xt.splitlines()),expanded_header_segments=len(segments),
 expanded_header_uncovered_bytes=0,expanded_header_segments_entries=segments,
 metadata_fields=len(metadata),metadata_entries=metadata,metadata_unclassified_fields=0,
 source_math_count=419,source_math_entries=coverage['entries'],source_math_unchecked=0,
 assertion_checks=len(findings),source_decision='ADMIT_HEADER_ONLY_FOR_STATEMENT_SEAL_CONSIDERATION',
 no_whole_paper_inventory_claim=True)
finite['coverage_entries_canonical_sha256']=sha(canon(dict(header_segments=segments,metadata=metadata,source_math=coverage['entries'])))
put('finite-coverage-manifest.json',finite)
report=dict(schema='header-source69-bounded-synthesis-v1',actual_reviewer_pid=os.getpid(),review_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 verdict=decision['verdict'],candidate_expanded_RAW_sha256=sha(expanded),new_delta_RAW_sha256=sha(delta_bytes),
 parent_contract_retained_exactly=True,extra_public_premises=0,missing_source_premises=0,repairs_required=0,
 source_math_count=419,expanded_header_segments=len(segments),expanded_header_lines=len(xt.splitlines()),
 source_consumers=['P14/B21 actual projected rotation','P19/B4 shared error vector'],
 retained_endpoints=['rank zero','alpha eta=1','V need not be onto'],
 proof_or_compilation_claim=False,Statement_Seal=False,SAU_claim=False,B21_or_B4_completion_claim=False,
 next_boundary='Root may decide Statement Seal; this packet does not prove, elaborate, or compile the statement.')
put('bounded-synthesis.json',report)
print(json.dumps(report,sort_keys=True))
