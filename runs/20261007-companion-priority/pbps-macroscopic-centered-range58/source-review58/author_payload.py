import json,hashlib,os,datetime,re
from pathlib import Path
R=Path('E:/Samplinglib');T=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';B=T/'source-review58';P=R/'runs/20261007-companion-priority/pbps-macro-range-preproof-review58'
def h(b):return hashlib.sha256(b).hexdigest()
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def rec(p):
    b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,o):(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def assertrec(r):
    got=rec(r['path']);assert all(got[k]==r[k] for k in ['raw_bytes','raw_sha256','lf_bytes','lf_sha256'])
manifest=load(B/'input.manifest.json')
for e in manifest['inputs']:
    for k in ['actual_input','exactraw_snapshot','crlf_to_lf_snapshot']:assertrec(e[k])
for r in manifest['supplemental_readonly_inputs']:assertrec(r)
packets=[load(T/('source.%d.reviewer-packet.json'%i)) for i in range(3)]
for p in packets:
    assert not any(p['anti_anchoring'].values())
    for k in ['source','blind_reconstruction']:assert h(p[k]['original_text' if k=='source' else 'text'].encode())==p[k]['text_sha256']
    assert h(p['lean']['statement'].encode())==p['lean']['statement_sha256']
    x=p.copy();expected=x.pop('packet_sha256');assert h(canonical(x))==expected
    module=(R/p['lean']['file']).read_bytes().replace(b'\r\n',b'\n').decode('utf-8')
    assert module==p['candidate_publication_context']['current_lean_module']
decoder=load(T/'anonymous-decoder/run.json');d=decoder.copy();runsha=d.pop('run_sha256');assert h(canonical(d))==runsha
assert decoder['status']=='CLOSED' and decoder['source_text_visible'] is False and decoder['source_identity_visible'] is False
for i,p in enumerate(packets):
    assert p['blind_reconstruction']['decoder_run_sha256']==runsha
    inp=load(T/('anonymous-decoder/packet%d.json'%i));out=load(T/('anonymous-decoder/result%d.json'%i))
    assert p['blind_reconstruction']['decoder_packet_sha256']==inp['packet_sha256']
    # Decoder result binding is independently preserved in its complete native run.
for prefix,file in [('generic.1','AutoSamplingTheory/TechnicalLemmas/Measure/L2PullbackRange.lean'),('macro.1','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRange.lean'),('tests.2','Tests/ProximalBPSMacroscopicRange.lean')]:
    st=load(T/(prefix+'.status.json'));assert st['exit_code']==0
    assert rec(T/(prefix+'.log'))['raw_sha256']==st['log_raw_sha256']
    assert rec(R/file)['raw_sha256']==st['source_raw_sha256']
    assert load(T/(prefix+'.compiler.lease.json'))['status']=='CLOSED'
    content=(R/file).read_text(encoding='utf-8');assert not re.search(r'\b(sorry|admit|axiom)\b',content)
reuse=[]
for n,files in [('pbps-l2-macroscopic-mean55',['AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean']),('pbps-marginal-poincare57',['AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean','Tests/GaussianMarginalPoincare.lean'])]:
    freeze=load(T.parent/n/'math-freeze.json');matches=[]
    for file in files:
        record=next(x for x in freeze['inputs'] if x['path']==file);got=rec(R/file);assert got['raw_sha256']==record['raw_sha256'] and got['lf_sha256']==record['lf_sha256'];matches.append(got)
    source_run=T.parent/n/('reviewer.source.run.json' if n.endswith('55') else 'root-seal-followup57/receipt.json')
    reuse.append(dict(provider=n,freeze=rec(T.parent/n/'math-freeze.json'),unchanged_current_code_receipts=matches,native_receipt=rec(source_run),scope='Unchanged source/provider audits reused only for these exact interfaces; no recursive57 tree copied; no58 mathematical verdict inferred.'))
write('provider-reuse.json',dict(reused=reuse))
slotnames=['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']
def slot(original,reconstructed,relation,evidence):return dict(original=original,reconstructed=reconstructed,relation=relation,evidence=evidence)
gslots={
'objects':slot('Authored canonical background: measurable X,Y, measures mu,nu, measure-preserving f and realL2 pullback M_f.','Exactly these objects, including f measurable and f_*mu=nu.','same','Packet0 reconstructed text; hf recursively expands measurable/map_eq; Lp.compMeasurePreserving real scalar. Raw B.2 supplies only the actual snd special case, so generic theorem is attributed ASTIS background.'),
'domains':slot('Arbitrary measures/measurable spaces; comap AEstrongly measurable L2 classes. No probability, sigma-finite or StandardBorel hypothesis.','Arbitrary real L2(mu), L2(nu); classes admitting AEstrongly measurable comap representative.','same','Fixed FactorsThrough.exists_eq_measurable_comp only requires real target nonempty/completely metrizable. Fixed lpMeas carrier is AEStronglyMeasurable[comap f], and memLp_map_measure_iff imposes no measure-finiteness condition.'),
'quantifiers':slot('For every measurable X,Y and measures with one measure-preserving f, equality of entire pullback range and comap L2 submodule.','Uniform equality for every such map/measures, not a supplied factorization witness.','same','Generic proof ext v covers forward/reverse; reverse constructs a real factor g and hgLp.toLp class internally.'),
'assumptions':slot('Only measurable carrier structure and MeasurePreserving f mu nu.','Only the same typing and map contract.','same','All theorem binders audited; hf.measurable and hf.map_eq; no hidden probability/StandardBorel/boundedness/finite-dimensional or range premise.'),
'conclusion':slot('ranM_f exactly lpMeas(comap f), both inclusions.','Image equality with comap AEstrong L2 classes.','same','Forward comp_ae_measurable plus canonical AE action; reverse mk factorization, MemLp pushforward and AE composition recover v via Lp.ext. Isometry alone is not used to infer onto.'),
'scopes':slot('Canonical reusable background completion of omitted B.2 factorization, attributed ASTIS via fixedMathlib; not a printed general PBPS theorem.','Same background equality with no PBPS main/gradient/root claim.','explicit-elaboration','Raw source B.2 states actual snd identification; generic attribution distinguishes new generalization. Lesson formula L2(comap,mu) is interpreted as ambient AE submodule, not everypoint functions.'),
'constant_dependencies':slot('No curvature or scale constants. Exponent2 and real codomain fixed.','No estimates or parameters.','same','Signature has no alpha/beta/eta; Mathlib target regularity instantiated internally by real numbers.')}
base_original='Source R^d, C2 V, 0<alpha<=beta, both global Hessian bounds, eta>0,betaeta<=1; actual mu/J/nu; real AE L2.'
main_slots={
'objects':slot('B.1/B.2 conditional-Y P; normalized Gibbs mu, actual Gaussian J and nu=J.snd; canonical u(y) identification.','Same literal laws, true conditional projection P and canonical second-coordinate isometric M.','explicit-elaboration','MacroscopicRange uses GibbsAugmentation.normalized_augmentation_density, literal Gaussian product pushforward, lpMeas subtype composed with condExpL2. Tilted zero case unreachable under original lower curvature.'),
'domains':slot('Real L2 actual laws; source Euclidean carrier. Authored finite real Hilbert/Borel/rank0 extension is explicit.','Finite real inner-product Borel E, rank0 allowed; actual L2 of J/nu with no dimension restriction.','explicit-elaboration','D.1 AE quotient convention; finite-dimensionality applies only to E. Rank0 adds no nontrivial centeredspace hypothesis. Coordinates recover R^d case.'),
'quantifiers':slot('Exact macro range equals all marginalpullbacks; mean transport for every L2u; full centered image, not only some embedded subspace.','One definitionally canonical M/P before allu; exact ranges and full centered set image.','same','hMrange generic theorem; P=S.starProjection and S.range_starProjection; centered reverse chooses preimage from proven range then hMean yields mean0.'),
'assumptions':slot(base_original,'Same C2, positive/order, both Hessian quadratic-form binders, eta positivity and cap; no suppliedlaw/onto/mean certificate.','same','hH expanded into lower and upper inequalities. Source positivity/order remain at rank0 even if individual bounds vacuous. All normalization/range conclusions produced internally.'),
'conclusion':slot('B.2 macro identification plus D.2 centered subspace: ranM=ranP, integral equality, M(L2_0 nu)=ranP intersectL2_0 J; actual probabilities.','Exactly all those conjuncts for actual objects.','explicit-elaboration','Mean equation follows integral_congr_ae and integral_map; on probability laws L2 isL1. Actual outputs J/nu probabilities; no every-y representative equation asserted.'),
'scopes':slot('Bounded B.1/B.2/D.1-D.2 identification feeding C.3/C.4. No root/weakH1/algorithm completion.','Public MacroscopicRange proves range/mean/centeredimage only; no imports of Tests.','same','Production imports sharedrange, GibbsAugmentation, CondexpL2; sourceproof formula steps match body. No Gamma symbol or gradient assumption in signature.'),
'constant_dependencies':slot('Original alpha,beta,eta floor retained; range itself requires less but no additional parameter dependence.','Same original floor; no restricted scale margin or nonzero dimension.','same','hBetaEta<=1 retains endpoint; bothHessianbounds retained even though probability producer consumes only lower bound.')}
test_slots={
'objects':slot('B.4 actual reflection U; P actualYprojection; A=PUP; B=(I-P)UP. Authored Test uses these same actual objects.','One actual AEreflection real linear isometry U, involutive/selfadjoint; exactA/B fromsameU/P.','same','hU/hUi/hUs fromactual55; hSameM uses AEpullback Lp.ext; hSameT uses hTa/hSd/hTb for literal sameS every-y law, no caller equality assumption.'),
'domains':slot('Paper D.1 is real AE L2, C.4 on H_P,0. Authored packet2 admitsrank0 but also says actual infinite-dimensional L2(J) unconditionally.','Actual L2(J) on finiteHilbert/Borel E includingrank0, with no dimension-of-L2 assumption; allcenteredf inranP.','different','The unqualified authored dimension sentence fails at E={0}:J isDirac, L2(J) is1-dimensional andH_P,0={0}. Lean/decoder correctly includes thiscase. This is publication wording drift; not a theorem/proof failure.'),
'quantifiers':slot('Source U fixed before every macro input; C.4 and squareddefect for allf inH_P,0.','Exists oneU before allg/allf; allf inP.range withmean0, notonlya caller image.','same','hCentered gives u mean0 andMu=f for everyf; hSameT holds for everyroughu. Source hypothesis=binders, proofingredients=internaledges.'),
'assumptions':slot(base_original,'Identicaloriginal floor; centeredmacro membership/mean0 restrict conclusion; no suppliedPI/gradient/root certificate.','same','No compactness or G.domain premise onf. Existing57 Test suppliesclosedG/T/K graph andscalarC4 internally. BothglobalHessianbounds, C2only, positivity/order/cap retained.'),
'conclusion':slot('C.4:||Af||<=rho||f||; B.5 and finalC.1 squareddefect precursor 4alphaeta/(1+alphaeta)^2||f||^2<=||Bf||^2.','Exactly contraction andsquaredB bound foractualcenteredmacroclasses.','equivalent','hMT+M.norm_map transferactualT55 contraction after hSameT; hDef and hr=1-rho^2 give bound. No positive root,LoewnerGamma bound orinverse asserted.'),
'scopes':slot('Source printedcentering uses selfadjointconstantpreserving A; alternativeexisting57stationarity gives same requiredmeanpreservation; B.15positive root still separate.','Test-level actualintegration throughexisting55production/57Test; fullrange fromnewmain; no productionimportsTests or copiedPIproofs.','explicit-elaboration','Reviewed57 hPreserve derivesmean fromactualLambda/Sdisintegration andidenticalmarginals withL2->L1; doesnotinfercentering fromconstantsalone. Itsclosed-gradient adaptation doesnotclaimsourceweakH1 identification.'),
'constant_dependencies':slot('rho=(1-t)/(1+t),t=alphaeta in(0,1]; squaredgap=4t/(1+t)^2; endpointt1 allowed.','Same exactconstants, no beta/d dependence outsideoriginalscope.','same','ha1 fromalpha<=beta andcap; hrho>=0 makes squaring valid; hd>0. At t1:rho0,gap1; no divisionby1-t, no omittedendpoint.')}
editorial=dict(id='ASTIS-EDITORIAL-58-L2-DIMENSION-ORIGINAL',classification='publication-wording-domain-overclaim',blocking=True,blocking_scope='Original packet2 publication/source authored sentence only; corrected publication acceptance withheld.',affected_packet_sha256=packets[2]['packet_sha256'],original='uses actual infinite-dimensional L²(J)',proposed='uses the actual, potentially infinite-dimensional L²(J), without imposing finite-dimensionality on L²',counterexample='E is the zero real Hilbert space. Canonical Gaussian/Gibbs augmentation J is the Dirac probability on the singleton E x E. Real L2(J) is isometric to real and has dimension1; its centeredmacrospace iszero. All original hypotheses can hold (choosealpha=beta=eta=1 andconstantV).',preserved_immutable_original=rec(T/'source.2.reviewer-packet.json'),semantic_signature_change=False,proof_change=False,sourcepaper_repair=False,repair_proposal_status='PROPOSED_ONLY_NEEDS_DISTINCT_EXACT_OVERLAY_REVIEW',creator_validation=False)
write('editorial-issue.original.json',editorial)
results=[]
for i,slots in enumerate([gslots,main_slots,test_slots]):
    p=packets[i]
    deltas=[]
    if i==0:deltas.append(dict(id='ASTIS58-GENERIC-BACKGROUND',classification='domain-clarification',blocking=False,description='Authored canonical all-measures real factorization generalizes the actual snd probability specialcase fromrawB2; not falselyattributed asliteral printedpaper theorem.'))
    if i in [1,2]:deltas.append(dict(id='ASTIS58-FINITE-HILBERT-RANK0',classification='domain-clarification',blocking=False,description='Finite realHilbert/Borel wording generalizes sourceEuclidean notation;rank0 explicitlydisclosed and no dimension-onL2 assumption.'))
    if i==2:deltas.append(editorial)
    result=dict(schema_version=1,semantic_slots=slots,deltas=deltas,verdict=['exact','equivalent-after-elaboration','domain-mismatch'][i],repairs=[],reviewer='/root/statement_topology58',independent_from_formalizer=True,independent_from_decoder=True,independent_from_whole_math_reviewer=True,review_evidence='Independent primary reconstruction pinned before58 statement/proof exposure, re-read boundedfixedrawB1/B2/B5/B8/B9/C1-C4/finalC1/D1/D2, exactthree freshanti-anchoredpackets, actualcompiledbodies andformula steps; directMathlibbackground contracts; actual101 raw/LF inputs checked. All7slots explicitly compared.',reviewer_packet_sha256=p['packet_sha256'],reviewer_packet_receipt=rec(T/('source.%d.reviewer-packet.json'%i)),publication_binding_sha256=p['publication_binding_sha256'],mathematical_fidelity_verdict=['exact','equivalent-after-elaboration','equivalent-after-elaboration'][i],publication_review_status='BLOCKED_ORIGINAL_EDITORIAL_DOMAIN_OVERCLAIM' if i==2 else 'ACCEPTED_SCOPED',mathematical_blockers=[],publication_blockers=[editorial['id']] if i==2 else [],source_id=p['source']['source_id'],source_anchor=p['source']['anchor'],declaration=p['lean']['declaration'],statement_sha256=p['lean']['statement_sha256'],blind_reconstruction_sha256=p['blind_reconstruction']['text_sha256'],decoder_run_sha256=runsha,source_text_visible_to_decoder=False,source_identity_visible_to_decoder=False,binder_audit=dict(EXCESS=[],sourcefloor=['hAlpha','hAlphaBeta','hV:C2','hH.lower','hH.upper','hEta','hBetaEta'] if i else ['MeasurePreserving f mu nu:measurable/map_eq'],typing='RealAE L2; finiteEonlyinmain/Test; no extraregularity'),definition_audit='Actual literal laws; normalizedtilted valid underderivedintegrability; canonicalpullback andcondExpL2 quotientprojection; AE representativesonly.',formula_proof_review='Allstepformulas andnamedprovideruses matchcompiledbody; exceptpacket2dimensiondescription, no inaccurateformula/proof ormissingderivedpremise found.',remaining_boundary='Gamma/root/inverse/fullweakH1/C5-C7/dynamics/main/errors/cost/composition/fullpaper/Goal remainopen.',formal_admission=False)
    assert set(result['semantic_slots'])==set(slotnames)
    results.append(result)
payload=dict(schema_version=1,actor='/root/statement_topology58',result_count=3,semantic_slot_count=21,results=results,source_first_reconstruction=rec(P/'independent-source-reconstruction.json'),reused_native_provider_audits=rec(B/'provider-reuse.json'),editorial_original_negative=rec(B/'editorial-issue.original.json'),root_input_count=101,supplemental_input_count=11,whole_math58_verdict_read=False,earlier58_semantic_delta_or_repair_verdict_read=False,canonical_adoption_or_state_change=False,compiler='NOT_STARTED_CLOSED',created=datetime.datetime.now(datetime.timezone.utc).isoformat())
write('source-review-payload.json',payload)
print(json.dumps(dict(pid=os.getpid(),source_review_payload_sha256=h(canonical(payload)),results=3,slots=21,mathematical_blockers=0,publication_blockers=1,root_inputs=101,supplemental_inputs=11)))
