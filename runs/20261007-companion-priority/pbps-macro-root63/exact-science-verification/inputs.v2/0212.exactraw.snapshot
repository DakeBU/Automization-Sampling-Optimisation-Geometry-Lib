import hashlib,json,os,pathlib,re
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;P=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def j(n):return json.loads((O/n).read_bytes())
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
m=j('candidate.input.manifest.json');primary=j('primary.first.manifest.json');top=j('source.topology.receipt.json')
for table in [m,primary]:
 for row in table['qualified_raw_LF_pairs']:
  for k in ['original','raw_snapshot','lf_snapshot']:assert pin(R/row[k]['path'])==row[k]
lookup={x['original']['path']:x for x in m['qualified_raw_LF_pairs']}
def frozen(p):return R/lookup[p.relative_to(R).as_posix()]['raw_snapshot']['path']
headers=[frozen(P/f'header{i}.lean').read_text(encoding='utf8') for i in [0,1]]
candidate=json.loads(frozen(P/'statement-candidate.json').read_bytes())
for q in candidate['inputs']:assert pin(R/q['path'])['raw_sha256']==q['raw_sha256']
typechecks=[]
for i in [0,1]:
 rec=json.loads(frozen(P/f'named-type{i}-ambient-corrected/receipt.json').read_bytes());out=frozen(P/f'named-type{i}-ambient-corrected/stdout.log').read_text(encoding='utf8');err=frozen(P/f'named-type{i}-ambient-corrected/stderr.log').read_bytes();probe=frozen(P/f'named-type{i}.lean').read_text(encoding='utf8')
 marker=f'ASTIS63_NAMED_TYPE_{i}_ELABORATED_NO_PROOF'
 assert rec['exit_code']==1 and rec['terminal_closed'] and err==b'' and out.count('error:')==1 and marker in out and out.count(marker)==1
 assert probe.count(headers[i].strip())==1 and re.search(r'fail\s+"'+marker+'"',probe)
 # All full named TYPE pre/post maps checked. Initial negatives use their own qualified historical snapshots.
 for q in rec['inputs']:
  now=pin(pathlib.Path(q['path']));assert now['raw_sha256']==q['raw_sha256'] and now['lf_sha256']==q['lf_sha256']
 for row in rec['input_snapshots']:
  q=row['original']
  for key in ['exact_raw_snapshot','LF_snapshot']:
   z=row[key];b=pathlib.Path(z['path']).read_bytes();assert sha(b)==z['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['lf_sha256']
 assert rec['inputs_after']==rec['inputs']
 typechecks.append(dict(item=i,receipt=pin(P/f'named-type{i}-ambient-corrected/receipt.json'),named_probe=pin(P/f'named-type{i}.lean'),header=pin(P/f'header{i}.lean'),actual_foreground_compiler_pid=rec['actual_foreground_pid'],compiler_exit_code=1,classification='FULL_NAMED_TYPE_ELABORATED_EXPECTED_INTENTIONAL_FAIL_ONLY_NO_PROOF',marker=marker,stderr_empty=True,pre_post_inputs_unchanged=True,input_snapshots_mapping=rec['input_snapshots']))
neg=json.loads(frozen(P/'named-type0-initial/receipt.json').read_bytes());assert neg['exit_code']==1 and neg['terminal_closed']
initials=[frozen(P/f'header{i}.lean.initial-ambient-negative.exactraw.snapshot').read_text(encoding='utf8') for i in [0,1]]
for i in [0,1]:
 reverse=headers[i].replace('    letI : MeasurableSpace (E × E) := Prod.instMeasurableSpace\n','').replace('condExpL2 ℝ ℝ (μ := J) measurable_snd.comap_le','condExpL2 ℝ ℝ measurable_snd.comap_le')
 assert reverse==initials[i]
diff=headers[1].replace('genuine_actual_macroscopic_root_consumer','actual_unique_positive_macroscopic_defect_root').replace('‖f‖^2-‖A f‖^2 ∧ ‖ΓP f‖ ≤ ‖f‖','‖f‖^2-‖A f‖^2')
assert diff==headers[0]
api=[]
for w in m['API_windows_qualified']:
 q=w['whole_original'];p=pathlib.Path(q['path']);b=p.read_bytes();assert sha(b)==q['raw_sha256'];span=b''.join(b.splitlines(keepends=True)[w['line_start']-1:w['line_end']]);assert span==pathlib.Path(w['exact_raw_selected_bytes']['path']).read_bytes();api.append(dict(qualified=w,inspected_text=span.decode('utf8')))
assert any('CompleteSpace (lpMeas F 𝕜 m p μ)' in w['inspected_text'] for w in api)
binders=[
 dict(binder='E + NormedAddCommGroup/InnerProductSpace ℝ/FiniteDimensional ℝ/MeasurableSpace/BorelSpace',classification='structural-typing-and-explicit-coordinate-extension',source='S1 Rd, D1 realHilbert; finite base admits rank0, not finiteL2'),
 dict(binder='V:E→ℝ; α β:NNReal; η:ℝ',classification='source-objects',source='S1 real potential/positive curvature/positive capped step'),
 dict(binder='hα,hαβ,hV,hH,hη,hβη',classification='source-hypotheses',source='0<α≤β,C2,lower/upper Hessian for everyx/v,η>0,βη≤1 literalS1/S2cap/A2cap'),
 dict(binder='μ,J,ν,Λ,F',classification='canonical-definition-lets',source='Normalized volume.tilted(-V), independent augmentation Y=X+sqrtηZ, marginalJ.snd,reflected(Y,2X-Y),jointreflection(x,2x-y)'),
 dict(binder='mY',classification='source-domain-definition-let',source='Comap snd sigma algebra expresses y-only macro functions inB2; not a new ambient measurable space'),
 dict(binder='letI ambient Product instance',classification='internal-typing-clarification',source='Restores SAME ambient Product sigma algebra used byJ; exactreversebytes recovers initialheader; no public assumption'),
 dict(binder='letI Fact(mY≤ambient)',classification='internally-derived-typing-fact',source='Derived measurable_snd.comap_le; nocaller containment/completeness certificate'),
 dict(binder='HP,P,hp,M',classification='canonical-definition-lets',source='HP=lpMeas ℝ ℝ mY2J closed fromMathlib;P=subtype∘condExpL2 μ=J;hp sndmeasurepreserving rfl;M canonicalL2pullback isometry'),
 dict(binder='Probability μ/J/ν;HP=rangeP;Pf=f;S Markov/density/disintegration/stationarity',classification='existential/conjunctive-conclusions',source='Actualsource laws/kernels produced under originalmodel;S everyy tilted normalizeddensity, no callerprobability/normalizer/kernel'),
 dict(binder='e,∀u subtype(eu)=Mu',classification='internally-produced-domain-isometry-onto',source='e scalarL2ν≃li exactHP, not arbitrary callerontoM certificate;B2 marginaldefinitionadapter'),
 dict(binder='U AEpullback/involution/selfadjoint',classification='internally-produced-actual-reflection',source='B4/SS1p3; SAME everyg per-gAE reflection, no arbitraryisometry witness'),
 dict(binder='T selfadjoint/contractive/conditional-AE-action/mean',classification='internally-produced-actual-scalar-operator',source='B9/C1 sourceS; per-observableνAE action separate everyy density;integrability fromprobability/L2 internally'),
 dict(binder='A,B',classification='canonical-dependent-definition-lets',source='A=HP.projection∘U∘subtype;B=(I_joint-P)UP∘subtype:HP→joint, not HPendomorphism;P(Bf)=0 concludes exactmicroscopicimage'),
 dict(binder='A=e.conjStarAlgEquiv T,selfadjoint,all-fcontraction',classification='conclusions-and-SAME-object-identification',source='eTu=Aeu equivalent toM(Tu)=PUP(Mu); no duplicateT that merely sharesnorms'),
 dict(binder='Γpositive;Γ²=I_scalar-T²;ΓP=e.conjStarAlgEquiv Γ',classification='internally-produced-root-and-canonical-transport',source='Compiled61/62 real scalar existence/uniqueness internal; macroΓP positive squareI_HP-A²; no publicCFC/rootpreservation certificate'),
 dict(binder='B.adjoint∘B=ΓP²;∀f normBf=normΓPf and macroenergy',classification='selected-source-B11-conclusions',source='TypedB:HP→joint makesadjoint:joint→HP; isometricmicroinclusion leavesGram/normequalities unchanged; no I_joint substitution'),
 dict(binder='∀G:HPoperator,Gpositive→G²=I_HP-A²→G=ΓP',classification='ALL-alternatives-conclusion',source='D1 canonical positive-root uniqueness on completeHP; quantifiedoutsideall-fenergy, no alternativeenergy or commutation premise'),
 dict(binder='header1 additional∀f ΓPcontraction',classification='genuine-Test-extra-mathematical-corollary',source='Macroenergy plusnorm(Af)²≥0 yieldsΓPcontraction; not an extra source hypothesis or strictcenteredrate')
]
route=[
 'Reuse genuine actual59 normalized laws/S/U/M59/T and scalar positiveD. IdentifyM59 with canonicalM by SAME per-u AE sndpullback, not matchingnorms; no63body/proof supplied here.',
 'Canonical58/sharedL2PullbackRange provides rangeM=lpMeas; internally derivedFact yieldscompleteHP. condExpL2 isorthogonalProjection, soP=HP.starProjection andHP=ranP. Form e=M.equivRange followedbyofEq; no calleronto/completeness.',
 'Use actual59MT=PUPM and subtype(eu)=Mu to identifytypedmacroA=e.conj T. Actualreflection witnesses fromReflectionL2 and59 must be equalby SAMEper-gAEFformula before reusingjointblockidentity.',
 'Reusegeneric61positiveREALscalarroot on SAME D; admittedgeneric62uniqueness canonizesit. TransportΓ with e.conjStarAlgEquiv, preservingpositivity/mul/one/sub; proof-localcomplexCFC remainsinsidecompiled61/62, not publicmacrocalculus.',
 'Restrict SAME jointGram=P-Ajoint² throughsubtype. subtype†=orthogonalProjection andPf=f onHP give B†∘B=I_HP-Amacro². Theambientmicroscopiccodomainembedding isisometric, so correcttypedB11Gram follows.',
 'Use root-square/adjoint norm pairing for ALLmacro f toobtainnormBf=normΓPf andscalarenergytransport; invert e for allpositivemacroalternatives and usegeneric62equalpositivesquares.',
 'GenuineoriginalinputTest obtainsallmacroΓPcontraction fromenergy; no strictgap/rootorder/inverse/polar or higherdynamics conclusions. Any futurefailure gets a typedsmaller SAMEoperator/domainadapter, not sourcepremiseaddition.'
]
review=dict(verdict='accepted-source-statement-conditional-on-verified62-parent',reviewer='/root/next_primary59',independent_from_formalizer=True,source_first=True,source_graph_sealed_before_candidate=True,current_exact_headers=[pin(P/f'header{i}.lean') for i in [0,1]],source_regions=24,coverage_items=56,source_nodes=19,source_hyperedges=13,expanded_binder_classification=binders,excess_count=0,repairs=[],blocking_statement_issues=[],named_TYPE_classification=typechecks,ambient_overlay=dict(initial_negative_actual_pid=neg['actual_foreground_pid'],initial_exit_code=1,retained_receipt=pin(P/'named-type0-initial/receipt.json'),reversible_exact_original_headers=True,only_changes='InternalProductmeasurable instance plus explicitμ=J oncondExpL2; identical publicassumptions/objects/source domains; no proofcredit'),source_vs_implementation='Independent literal sourcegraph definesGammaP directlyfrompositiveI_HP-A² viaD1, firstB5 andB11. Proposed scalarcanonical61/62 rootconjugation,lpMeas completeness/range/canonicale andtypedGram adapters are ASTIS background/detail completion, not printed source proofgraph.',definition_semantics='All local structural/typeclass lets derive existingProduct/comapcontainment/Lpcompleteness. Scalar/jointspaces are fullAEquotients, nofiniteL2/nontrivial. Btargetjoint withPB=0 exactly embedsprintedmicroblock;B†∘B typedonHP. SamecanonicalM/e actualU/T relation enforced in conclusions;ΓP transports SAMEΓ.',seven_step_route=route,API_inventory=api,source_hypothesis_map='SourceS1C2/bothHessians0alpha<=beta andexactpositivecappedS2/βη≤1 preserved. Rank0 explicitcoordinateextension;αη1 legalendpoint;finitebase≠finiteL2. Everyy normalized S density versusper-uνAEaction retained; nocommon-nullset claim.',source_cap=primary['source_regions'][-1],remaining_boundary='Preproofstatement/topology only. Parent62exactscience9d7f7b640c7cb18fea133ccbd300de129af40b83 verification remainsrequired; no63proof/claim/admission. Afterproofthis would coverprintedB10/B11andfirstB5 onexactHP only. SecondB5/centeredorder/inverse/polar/H1/dynamics/main/errors/querycost/composition/fullpaper/Goal remainopen.',compiler_started=False,mathematical_proof_credit=False,state_transition=False)
wr('statement-binder.review.json',review)
wr('named-TYPE-and-overlay.review.json',dict(current_types=typechecks,negative_initial=review['ambient_overlay'],intentional_fail_is_type_evidence_only=True,source_statement_accepted_conditionally=True,parent62_verified_not_assumed=True))
wr('author.receipt.json',dict(actual_foreground_pid=os.getpid(),verdict=review['verdict'],excess_count=0,source_before_candidate=True,root_named_type_PIDs=[x['actual_foreground_compiler_pid'] for x in typechecks],expected_compiler_exit_codes=[1,1],reviewer_compiler_started=False,repairs=[]))
print(json.dumps(dict(actual_foreground_pid=os.getpid(),verdict=review['verdict'],excess=0,repairs=[],TYPEonly_PIDs=[x['actual_foreground_compiler_pid'] for x in typechecks],parent62_verification_required=True)))
