from pathlib import Path
import datetime, hashlib, json, re

root = Path('E:/Samplinglib')
lane = root / 'runs/20261007-companion-priority/pbps-actual-absolute-next-event-time91'
out = lane / 'independent-source91'
preread = root / 'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def info(p): return {'path':str(p).replace('\\','/'),'raw_sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def write(name,obj):
    with (out/name).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,indent=2,ensure_ascii=False); f.write('\n')

packetpath=lane/'anti-anchored.review91.json'
p=read(packetpath)
canonical=dict(p);canonical.pop('packet_sha256')
assert sha(json.dumps(canonical,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==p['packet_sha256']
module=root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean'
lessonpath=root/'website/content/declaration_lessons/pbps-actual-absolute-next-event-time.json'
pubpath=root/'website/content/publications/pbps-actual-absolute-next-event-time.json'
lesson=read(lessonpath)['units'][0];pub=read(pubpath)['items'][0]
raw=module.read_bytes();text=raw.decode();lines=raw.splitlines(keepends=True)
assert sha(raw)=='8e28fb218233358a9b1c7a2b41689071ca3c410faa58a0883a0885243d588ab2'
assert p['candidate_publication_context']['current_lean_module']==text
assert p['candidate_publication_context']['statement']==pub['statement']==lesson['statement']
assert all(lesson[k]==v for k,v in p['candidate_publication_context']['lesson'].items())
decoderpath=root/'runs/semantic-roundtrip/anonymous91/decoder-output/reconstruction.json'
decoder=read(decoderpath);decoderinput=root/'runs/semantic-roundtrip/anonymous91/input.json'
assert read(decoderinput)['lean']['statement']==p['lean']['statement']
assert sha(p['lean']['statement'].encode())==p['lean']['statement_sha256']
assert sha(decoder['reconstructed_theorem_text'].encode())==decoder['reconstructed_text_sha256']
seal=read(lane/'root.statement-seal91.json')['expanded_literal_Prop']
anonymous_seal=seal.replace('actual_absolute_next_event_time_statement','',1).replace(' : Prop :=',' :',1)
assert anonymous_seal.strip()==p['lean']['statement'].strip()
assert (out/'primary-first-freeze.md').exists()
assert sha((out/'primary-first-freeze.md').read_bytes())=='ebaeee1a488895cda6d81ccd8bea19dc4583634c3e2baf8a3a4e5b6691666c89'

definitions={
'c':'Literal center y-eta grad V(reference), source (3.4).',
'Φ':'Literal two-coordinate harmonic flow; real negative times are auxiliary domain extension.',
'S':'Literal reflection, zero denominator gives zero scalar and hence R_0=I.',
'rate':'Literal nonnegative residual bounce rate with sqrt(eta) normalization.',
'Λ':'Elapsed-time integrated actual rate, NNReal horizon; no arbitrary hazard provider.',
'τ':'Closed threshold hittingAfter from zero; empty hitting set top; equality retained.',
'next':'Actual live cumulative time plus finite wait and reflected flowed state; infinite wait becomes stopped, stopped remains stopped.',
'record':'Deterministic-depth Nat recursion starting live(0,z0), consuming clock k at transition k to k+1.',
'P':'Literal countable Exp(1) product; probability/independence not user premises.',
'ε':'Nonnegative clipping of raw real clocks; agrees with positive clocks almost surely; negative/zero carrier points explicit.',
'history':'Whole tuple through depth n of actual recursively generated records; not last-state-only surrogate.',
'waitObs':'Actual waiting time from live last state; stopped returns auxiliary zero.',
'timeObs':'Finite wait extraction with zero default at top; not an assertion that infinity equals zero.',
'density':'Actual rate times exponential survival along raw real flow; hazard horizon clipped; stopped density zero.',
'Rec':'Borel disjoint union of live nonnegative-time phase records and stopped singleton.',
'Hist':'All abstract record tuples indexed 0 through n, not a realizability subtype.',
'HistNext':'All abstract record tuples indexed 0 through n+1.',
'last':'Index n of current history.',
'lastNext':'Index n+1 of next history.',
'H':'Actual current whole history as function of countable clocks.',
'Hnext':'Actual next whole history from same recursion and same countable input.',
'readTime':'Stored real cumulative time on live, auxiliary zero on stopped; tags retain semantics.',
'a':'Last current record time, not an independent supplied previous-time map.',
'U':'Last next record time read from Hnext, not defined by a+wait.',
'appendRel':'Fin.snoc preserves all old coordinates; live appends time q+max(s,0) and S(Phi_s z), stopped appends stopped. Raw negative flow and clipped increment remain distinct.',
'appendAbs':'Relative append evaluated at u-a(h), defined even off strict support.',
'liftAbs':'Pairs absolute appended history with unchanged u.',
'd':'Positive part b(h)-a(h), permitting empty interval when b<=a.',
'μ':'Actual full-history pushforward of P, not a supplied stationary law.',
'D':'Strict a(h)<u<b(h) indicator times shifted density; zero elsewhere including stopped fibers.',
'Brel':'Strict positive finite waiting event below d(H), using actual next unused coordinate w_n.',
'B':'Both last records live and a(H)<U<b(H); real zero defaults alone cannot replace tags.',
'X':'Joint actual old history and next absolute-time observer.',
'Y':'Joint actual next history and next absolute-time observer.',
'ν':'Unnormalized weighted product of actual old-history law and real Lebesgue measure.'}
names=re.findall(r'^\s+let (\S+)',text[:text.index('set_option maxHeartbeats')],re.M)
assert names==list(definitions) and len(names)==35

slots={
'objects':{
'original':'Primary (3.4),(A.1),(A.2): actual harmonic PBPS flow, residual gradient rate, reflection, independent Exp(1) thresholds, successive cumulative times and poststates. A.7 consumes whole prescribed trajectories; A.2 supplies Borel recursion.',
'reconstructed':decoder['objects'],
'relation':'explicit-elaboration',
'evidence':'All 35 literal definitions are audited below. U is read from the next real record; the a+wait relation is proved on B. Complete generated records and fresh w_n replace no part of the actual recursion. Source stopping is represented by an absorbing sum tag; zero observers are auxiliary, guarded by live tags.'},
'domains':{
'original':'Primary finite Euclidean phase space, real positive eta, positive alpha<=beta, nonnegative time with infinity for empty crossing sets. A.7 has a strict ordered-time simplex at a finite horizon.',
'reconstructed':decoder['domains'],
'relation':'explicit-elaboration',
'evidence':'Finite-dimensional real inner-product Borel E is a coordinate-free Euclidean formulation; dimension zero is an explicit harmless extension with zero positive-event density. WithTop NNReal retains infinite waits. Hist includes unrealizable tuples, and real auxiliary time arguments permit negative flow; strict D and B isolate physical forward finite events. This is a restricted one-coordinate result, not equality of its global real U with the source extended T after stopping.'},
'quantifiers':{
'original':'Every fixed y,reference and initial phase; every deterministic recursion depth. Source A.7 later quantifies bounded measurable full-path tests at a fixed finite horizon.',
'reconstructed':decoder['quantifiers'],
'relation':'explicit-elaboration',
'evidence':'The statement fixes source parameters and n, then allows every fixed Borel finite-valued history cutoff b, all abstract-history fiber bounds, all measurable old-history sets A including null sets, and all jointly measurable ENNReal tests. The Borel cutoff is random only through evaluation on H; this is not a physical-time stopping theorem. Extended nonnegative tests are a justified stronger integration class for this bounded ingredient and do not assert the full path-functional source identity.'},
'assumptions':{
'original':'Source (1.1): V in C^2, 0<alpha<=beta, alpha I<=Hess V<=beta I. Section 2.2: 0<eta<=1/beta. Euclidean/Borel typing and the source clock construction.',
'reconstructed':decoder['assumptions'],
'relation':'equivalent',
'evidence':'Six analytic binders exactly retain these standing conditions. Hessian quadratic-form bounds are the coordinate-free symmetric Hessian bounds under C^2; beta>0 follows from alpha>0 and alpha<=beta, so beta*eta<=1 is equivalent to the source upper step bound. No density, independence, normalization, finite-wait, no-atom, path-coverage or measurability theorem is moved into a public premise. b,G,F,A measurability specifies observable classes.'},
'conclusion':{
'original':'The source recursion yields T_(n+1)=T_n+S_(n+1) on finite next waits and a reflected poststate; A.2 derives Borel coordinates. Iterating clock laws is a source-implicit ingredient of A.7, whose full conclusion also needs all event counts, final survival and complete paths.',
'reconstructed':decoder['conclusion'],
'relation':'explicit-elaboration',
'evidence':'Every conjunct is supported by exact BODY regions 1-7: six Borel maps, all old-coordinate preservation, joint D and every-history mass<=1, exact Brel=B, two guarded actual identities, three restricted pushforwards, mass<=1, and both parameter-measurable test identities. The written attribution explicitly calls this an ASTIS completion, not a printed standalone theorem. Full A.7 remains outside this theorem.'},
'scopes':{
'original':'Fixed-reference evolution, elapsed hazard argument, absolute event times, post-jump versus pre-jump distinction, stopping at empty threshold sets, and full path horizon in A.7.',
'reconstructed':decoder['scopes'],
'relation':'explicit-elaboration',
'evidence':'On B, u-a>0 and the density evaluates the pre-bounce rate at Phi_(u-a)(last poststate); append then applies S. Previous records stay fixed. Stopped/default zero observations and negative auxiliary flow are not physical events. Null sets use unnormalized restriction. The no-event/infinite-wait mass is omitted from this strict finite restriction, not normalized away; no survival or endpoint atom conclusion is smuggled in.'},
'constant_dependencies':{
'original':'Literal sqrt(eta) time scale, unit exponential thresholds, reflection coefficient two, initial time zero, alpha/beta/eta standing bounds; no new universal estimate constant for this identity.',
'reconstructed':decoder['constant_dependencies'],
'relation':'same',
'evidence':'The rate, flow, density exponent and Exp(1) parameter match the primary source. Mass bound one comes from the actual probability law, not an extra normalization premise. No uniform cutoff bound, dimension-dependent constant, hidden regularity bound or higher derivative assumption occurs.'}}

region_evidence=[
'Reintroduces exactly the sealed actual model and complete histories. h90 and h89 are invoked with the six analytic premises only. U is a record projection, so the proof cannot obtain clock equality by defining it so.',
'Borel coordinate projection, sum elimination and subtraction composition yield H,Hnext,a,U,appendAbs,liftAbs. The old-prefix identity is pointwise for every abstract input; no realizability assumption is needed.',
'D is a Borel piecewise shifted density. hcutoff treats b<=a and s<=0 correctly, hshift is exact, and fixed-history translation carries the existing relative fiber bound to the absolute fiber. This is not a separately exported product-shear theorem.',
'The stopped, live-top and live-finite branches of actual next are exhausted. Finite v yields stored time q.1+v, zero v is excluded by both guards, top cannot satisfy a finite cap. Thus event equality is pointwise, and the guarded previous complete-history identity gives actual absolute append.',
'oldPrefix is Borel and agrees both on actual next histories and relative appends. Composing G with oldPrefix and addition applies the genuine previous joint test law. Fiber translation and parameter integration derive the absolute G identity for every measurable A, without dividing by its probability.',
'UnitExponentialProduct first component supplies only IsProbabilityMeasure P. Test-function measure extensionality, Tonelli and withDensity yield the weighted product-reference law; actual guarded composition yields both next-history pushforwards. Probability of B gives mass<=1; missing mass remains missing.',
'Compose arbitrary ENNReal F with liftAbs and use the actual guarded Y identity to derive the final test formula. Joint measurability supplies the measurable parameter integral, including infinite-valued tests and null A. No full ordered iteration or terminal path assembly is asserted.'
]
regions=[]
for i,(s,ev) in enumerate(zip(lesson['steps'],region_evidence),1):
    r=s['lean_source_region'];chunk=b''.join(lines[r['start_line']-1:r['end_line']])
    assert sha(chunk)==r['exact_code_raw_sha256'] and chunk.decode()==s['lean']
    regions.append({'region':i,'title':s['title'],'start_line':r['start_line'],'end_line':r['end_line'],'module_raw_sha256':sha(raw),'exact_BODY_raw_sha256':sha(chunk),'lesson_region_pointer':f'/units/0/steps/{i-1}','lesson_formula':s['formula'],'lesson_text_sha256':sha(s['text'].encode()),'exact_BODY_matches_lesson':True,'source_and_exposition_verdict':'accepted-for-bounded-coordinate','evidence':ev})

coveragepath=preread/'independent-source-first91/source-coverage91.v2.native.json'
coverage=read(coveragepath)
primarypath=root/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
primaryraw=primarypath.read_bytes()
coverage_audit=[]
for c in coverage['coverage']:
    s=c['source_span'];span=primaryraw[s['byte_start']:s['byte_end_exclusive']]
    assert sha(span)==s['raw_sha256'] and len(span)==s['bytes']
    coverage_audit.append({'id':c['id'],'anchor':c['anchor'],'source_span_hash_verified':True,'independent_disposition':'agrees-with-frozen-primary-expectation','scope':c['local_disposition'],'nodes':c['nodes'],'restatement_checked':c['restatement']})
assert len(coverage_audit)==27

inputpaths=[primarypath,out/'primary-first-freeze.md',out/'primary-first-manifest.json',out/'primary-first-seal.sha256',packetpath,decoderpath,root/'runs/semantic-roundtrip/anonymous91/decoder-output/run.json',root/'runs/semantic-roundtrip/anonymous91/decoder-output/raw-manifest.json',decoderinput,module,lessonpath,pubpath,lane/'root.statement-seal91.json',preread/'source-proof-graph91.accepted-successor.json',coveragepath,lane/'implementation-source-map91.json',root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean',root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean',root/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',root/'lean-toolchain',root/'lake-manifest.json',root/'.agents/skills/astis-semantic-roundtrip/SKILL.md',root/'docs/proof-digestion-protocol.md',root/'docs/theorem-publication-protocol.md',root/'tools/astis_semantic_roundtrip.py']
for name in ['leaf-build.receipt.native.json','leaf-build.stdout.log','leaf-build.stderr.log','kernel.receipt.native.json','kernel.stdout.log','kernel.stderr.log','statement-scan.native.json','closed-manifest91.native.json']:
    inputpaths.append(lane/'independent-math91'/name)
mathmanifest=read(lane/'independent-math91/closed-manifest91.native.json')
mathbyname={Path(x['path']).name:x for x in mathmanifest['files'] if 'attempt1-' not in x['path']}
for path in inputpaths:
    if path.parent.name=='independent-math91' and path.name!='closed-manifest91.native.json':assert sha(path.read_bytes())==mathbyname[path.name]['raw_sha256']
scan=re.findall(r'\b(?:sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',text)
assert not scan
write('review-run91.native.json',{
'schema_version':1,'record_kind':'independent-primary-first-source-review-run','reviewer':'/root/primary_source91','independent_from_formalizer':True,'independent_from_decoder':True,'utc_closed':datetime.datetime.now(datetime.timezone.utc).isoformat(),
'primary_first_freeze_sha256':'ebaeee1a488895cda6d81ccd8bea19dc4583634c3e2baf8a3a4e5b6691666c89','chronology':'Stage 1 source-only freeze sealed before canonical packet, decoder, candidate Lean and exposition were opened. Stage 2 retained that file unchanged. No earlier semantic or repair verdict was used as authority. Graph/coverage proposals were independently compared with primary source; compiler receipts only were read from mathematical verifier.',
'reviewer_packet_sha256':p['packet_sha256'],'reviewer_packet_raw_sha256':sha(packetpath.read_bytes()),'publication_binding_sha256':p['publication_binding_sha256'],'inputs':[info(x) for x in inputpaths],
'verification':{'canonical_packet_hash_verified':True,'packet_module_current':True,'decoder_statement_identical':True,'seal_anonymization_only':True,'seal_transform':'Remove only leading statement name; replace declaration : Prop := with anonymous proposition colon. Remaining binder and literal body exact.','all_35_literal_definitions_reviewed':True,'all_6_analytic_binders_reviewed':True,'all_7_semantic_slots_reviewed':True,'all_7_BODY_regions_exact':True,'all_27_coverage_dispositions_reviewed':True,'all_9_source_spans_verified':True,'current_module_fake_closure_findings':scan},
'compiler_evidence_scope':'Independent verifier receipts/logs read and byte-bound; this source reviewer did not rerun Lean or adopt that verifier source/mathematical verdict. Focused kernel and leaf build exit 0, checked base HEAD 204fd4eee61724db77963cb33ddaddbcd90b906d, exact module SHA. Repository-wide astis.py check and postmerge purification are outside this source verdict.',
'output':'source-review91.native.json','hash_link_design':'Run binds all exact inputs; result binds this run file; closed manifest binds result/run without circular hashes.'})

result={
'schema_version':1,'record_kind':'native-independent-anti-anchored-source-review','reviewer':'/root/primary_source91','independent_from_formalizer':True,'independent_from_decoder':True,
'verdict':'equivalent-after-elaboration','accepted':True,'acceptance_scope':'Only the explicitly attributed ASTIS strict next absolute-event-time/complete-history coordinate completion. Not a claim of full printed A.7, whole paper, repository gate, publication completion or Goal completion.',
'semantic_slots':slots,
'deltas':[
{'id':'D91-1','blocking':False,'classification':'source-implicit','description':'Absorbing stopped tag, time-zero observers, clipped raw thresholds and globally total append define explicit auxiliary semantics. They agree with source live finite recursion; B excludes stopped and nonpositive/infinite waits. The theorem never equates source infinite absolute time with its zero observer.'},
{'id':'D91-2','blocking':False,'classification':'generalization','description':'Coordinate-free finite-dimensional real inner-product carrier, including rank zero, and ENNReal joint tests are explicit elaborations/extensions. They introduce no extra analytic assumptions and do not replace the full-path target.'},
{'id':'D91-3','blocking':False,'classification':'source-implicit','description':'History-dependent Borel finite cutoffs and unnormalized history-event integrals expose the source iteration ingredient; the fixed-horizon case is a specialization. Neither positive conditioning probability nor random physical-time restart is asserted.'},
{'id':'D91-4','blocking':False,'classification':'scope-boundary','description':'The infinite-wait/no-event atom and terminal survival are outside the strict restricted law; no mass is renormalized. Ordered iteration, final factor/path/count identification and full A.7 remain open. Existing actual-input nonaccumulation78/half-open coverage79 are upstream retained facts, not reopened or re-proved here.'},
{'id':'D91-5','blocking':False,'classification':'proof-route-realization','description':'Planned S91-T text includes a broader unweighted shear/inverse preservation theorem. This implementation realizes exactly the needed weighted coordinate law via fixed-history translation plus Tonelli; it does not separately close that broader theorem. Current lesson and proposed implementation mapping state this accurately.'}
],
'repairs':[],
'review_evidence':'Independent source-only freeze, fresh canonical packet, complete blind reconstruction, full production statement/proof, exact lesson/publication, 27 source dispositions/9 byte spans and seven BODY regions compared. No blocking source mismatch or excess premise found. Compiler/fake-scan logs are supporting Lean evidence, not source-equivalence evidence.',
'review_run_sha256':sha((out/'review-run91.native.json').read_bytes()),'reviewer_packet_sha256':p['packet_sha256'],'reviewer_packet_raw_sha256':sha(packetpath.read_bytes()),'publication_binding_sha256':p['publication_binding_sha256'],'production_module':info(module),'lesson':info(lessonpath),'publication':info(pubpath),
'binder_audit':[{'name':n,'classification':'STANDING','meaning':v} for n,v in [('hα','alpha>0'),('hαβ','alpha<=beta'),('hV','V globally C2'),('hH','all x,v Hessian quadratic-form lower/upper bounds'),('hη','eta>0'),('hβη','beta*eta<=1')]],
'additional_binders':{'E_structures':'TYPING; finite-dimensional real inner-product Borel space','V_alpha_beta_eta_y_reference_z0_n':'TYPING and universally quantified source parameters','b_G_F_A_measurability':'TYPING/admissible observable classes for stated completion','EXCESS':[]},
'literal_definition_audit':[{'name':n,'checked':True,'evidence':v} for n,v in definitions.items()],
'body_exposition_audit':regions,
'source_coverage_audit':coverage_audit,
'source_graph_audit':{'graph':info(preread/'source-proof-graph91.accepted-successor.json'),'coverage':info(coveragepath),'independently_checked':True,'scope':'Exhaustive for supplied bounded 27-disposition/9-span target; no claim of a fresh whole-paper global inventory review. Source outside target has explicit downstream/terminal exclusions.','actual_route':'h90 supplies actual complete history and relative joint tests; h89 supplies Borel density and each-history fiber bound; hcutoff/hshift and htranslate supply scalar translation; hGtests then hmapX use parameter integration/Tonelli/withDensity; hclock/hactual supply actual clock/append identification.','S91_T_mapping':'Accepted as bounded implementation mapping only. htranslate proves the weighted fixed-history substitution and hmapX proves the exact weighted product-reference law. No general standalone unweighted shear/inverse declaration is present or awarded source credit.','AND_OR':'Relative-vector induction then global triangular substitution remains alternative to conditional one-step absolute translation. Final survival88 is adjacent, not a premise of this coordinate. Existing78/79 do not close actual count/prescribed-path identification or full A7.','still_open':['S91-J','S91-F','S91-B when endpoint equality asserted','S91-P','S91-AC source cap/simplex route','S91-A7','S91-REL alternative route','S91-TRI alternative route','S91-ALG','S91-PATH']},
'exposition_seal':{'accepted_for_current_bounded_theorem':True,'all_7_exact_regions':True,'full_attributed_statement_and_assumptions':True,'formula_proof_matches_Lean':True,'source_implicit_attribution_explicit':True,'off_support_defaults_explicit':True,'remaining_boundary_visible':True,'no_separate_shear_certificate_claim':True,'no_reader_render_or_postmerge_purification_claim':True},
'compiler_and_fake_closure':{'base_HEAD':'204fd4eee61724db77963cb33ddaddbcd90b906d','leaf_build_receipt':info(lane/'independent-math91/leaf-build.receipt.native.json'),'kernel_receipt':info(lane/'independent-math91/kernel.receipt.native.json'),'statement_scan_receipt':info(lane/'independent-math91/statement-scan.native.json'),'own_text_scan_findings':scan,'scope':'Exact module focused evidence reviewed; whole-repository gate not rerun here.'},
'uncertainties':['No material unresolved source-semantic issue within this bounded theorem. Full A7 and its named future source nodes are not certified.','Canonical publication still carries conservative pending-proof/purification lifecycle wording; this review does not itself transition those records or certify rendered-site delivery.'],
'changes_made':'Only reviewer-owned files in independent-source91; no code, shared metadata, status transition, source graph mutation or repair overlay.'}
write('source-review91.native.json',result)
write('closed-RAW91.native.json',{'schema_version':1,'record_kind':'RAW','closed':True,'reviewer':'/root/primary_source91','utc_closed':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':[info(x) for x in inputpaths],'outputs':[info(out/x) for x in ['primary-first-freeze.md','primary-first-manifest.json','primary-first-seal.sha256','review-run91.native.json','source-review91.native.json','close-source-review91.py']],'closure':'All exact inputs and outputs listed; manifest excludes itself to avoid circularity. No further mutation of these outputs intended. Prior primary-first chronology is preserved.'})
for n in ['review-run91.native.json','source-review91.native.json','closed-RAW91.native.json']:print(n,sha((out/n).read_bytes()))
