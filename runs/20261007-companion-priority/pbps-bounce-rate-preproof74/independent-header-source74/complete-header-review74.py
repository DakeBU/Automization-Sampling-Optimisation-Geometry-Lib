from pathlib import Path
import hashlib,json,os,sys,difflib

ROOT=Path('E:/Samplinglib');OWN=Path(__file__).resolve().parent
PRE=ROOT/'runs/20261007-companion-priority/pbps-bounce-rate-preproof74'
R73=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73'
H=PRE/'header74.proposed.lean';SEAL=PRE/'root.statement-seal74.json'
P73=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/header73.proposed.lean'
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def pin(p):
    b=p.read_bytes();q=b.replace(b'\r\n',b'\n')
    return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(q),'LF_sha256':sha(q)}
def write(n,x):
    p=OWN/n;assert not p.exists(),n
    p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def read(n):return json.loads((OWN/n).read_bytes())
raw=H.read_bytes();lines=raw.splitlines(keepends=True)
assert len(raw)==3537 and sha(raw)=='d72435795cd225af382948e8da683b6eb4b9e5b05509f8e3b0d10a3ed5a5a96e'
assert len(lines)==70 and raw.endswith(b':= by\n')
assert raw.count(b'    (h\xce\xb1 :')==2
def linepin(a,z):
    i=sum(map(len,lines[:a-1]));j=sum(map(len,lines[:z]));q=raw[i:j]
    return {'lines_inclusive':[a,z],'RAW_start_inclusive':i,'RAW_end_exclusive':j,'RAW_bytes':len(q),'RAW_sha256':sha(q),'LF_sha256':sha(q.replace(b'\r\n',b'\n'))}
prefix_start=b'    {E : Type*}';prefix_end=b' : Prop :='
prefix=raw[raw.index(prefix_start):raw.index(prefix_end)]
old=P73.read_bytes();p73=old[old.index(prefix_start):old.index(prefix_end)]
assert prefix==p73 and len(prefix)==466
public=raw[raw.index(prefix_start,raw.index(b'theorem actual_bounce_rate_energy_laws')):]
pubprefix=public[:public.index(b' :\n')]
assert pubprefix==prefix
assert [q.decode().strip() for q in lines if q.startswith(b'import ')]==[
 'import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization',
 'import Mathlib.Analysis.InnerProductSpace.Projection.Reflection',
 'import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic']
assert b'ActualHarmonicFlow' not in raw and b'ActualCorrectorChange' not in raw
seal=json.loads(SEAL.read_bytes());assert seal['header']['RAW_sha256']==sha(raw)
stage=read('stageA.freeze74.json');check=dict(stage);hh=check.pop('run_sha256');assert sha(canon(check))==hh
for p in read('stageA.manifest74.json')['stageA_finite_artifacts']:
    q=(ROOT/p['path']).read_bytes();assert sha(q)==p['RAW_sha256']
coverage=read('source95-item-classification74.json');graph=read('source-proof-graph74.json')
oblig=read('source-obligations26.before-header74.json');forms=read('source-formulas21.exact74.json')
primary=PRIMARY.read_bytes();assert sha(primary)==stage['expectations']['RAW_sha256'] or sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
anchors=['S2.E4','S3.E4','S3.E9','alg1','A1.Ex4','A1.Ex5','A1.Ex6','A1.SS1','A1.SS2.p3','S3.Thmtheorem1']
assert all(('id="'+s+'"').encode() in primary for s in anchors)

# Predicate-driver repair is limited typing context, never a proof.
original=PRE/'header74.typecheck.lean';fixed=PRE/'header74.typecheck-closed-sections.lean'
oa=original.read_bytes();fa=fixed.read_bytes()
assert sha(oa)=='1dd0d07c3d21fd3e5c0e1989755d15103ad495852defb1ce261484fc7f12c672'
assert sha(fa)=='3866b26c9a19e92b442c2861b1887c17d9b9423f334ea27b7ba25f7adcbab5f0'
namespace_end=b'end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate'
assert fa==oa.replace(namespace_end,b'end\n'+namespace_end)
failreceipt=R73/'typecheck-prospective-header74/receipt.json'
passreceipt=R73/'typecheck-prospective-header74-section-close-repair/receipt.json'
fr=json.loads(failreceipt.read_bytes());pr=json.loads(passreceipt.read_bytes())
assert fr['actual_foreground_PID']==52824 and fr['exit_code']==1 and fr['terminal_closed']
assert pr['actual_foreground_PID']==53780 and pr['exit_code']==0 and pr['terminal_closed']
diagnosis=PRE/'typecheck-driver-diagnosis74.json'

inputs=[H,SEAL,P73,PRIMARY,original,fixed,diagnosis,failreceipt,passreceipt]
for receipt in [fr,pr]:
    for stream in ['stdout','stderr']:
        p=Path(receipt[stream]['path']);assert sha(p.read_bytes())==receipt[stream]['RAW_sha256'];inputs.append(p)
inputs=list(dict.fromkeys(inputs))
snapshots=[]
for name,p in [('header74.proposed.exactraw.snapshot.lean',H),('root.statement-seal74.exactraw.snapshot.json',SEAL)]:
    (OWN/name).write_bytes(p.read_bytes());snapshots.append({'snapshot':pin(OWN/name),'source':pin(p)})
(OWN/'header74.proposed.CRLF-only-LF.snapshot.lean').write_bytes(raw.replace(b'\r\n',b'\n'))
snapshots.append({'snapshot':pin(OWN/'header74.proposed.CRLF-only-LF.snapshot.lean'),'source':pin(H),'recipe':'CRLF->LF only'})

binders=[
 ('E','TYPING','finite-dimensional real Euclidean realization'),('NormedAddCommGroup E','TYPING','ambient normed additive structure'),('InnerProductSpace real E','TYPING','real inner product realizes dot product'),('FiniteDimensional real E','TYPING','paper R^d; no positive-rank condition'),('MeasurableSpace E','TYPING','ambient measurable structure'),('BorelSpace E','TYPING','measurable structure equals Borel of topology'),
 ('V','SOURCE_INPUT','same C2 potential'),('alpha','SOURCE_INPUT','NNReal parameter under original alpha>0'),('beta','SOURCE_INPUT','NNReal curvature upper constant'),('eta','SOURCE_INPUT','same positive proximal scale'),
 ('h_alpha','STANDING_SOURCE_HYPOTHESIS','alpha>0'),('h_alpha_beta','STANDING_SOURCE_HYPOTHESIS','alpha<=beta'),('hV','STANDING_SOURCE_HYPOTHESIS','C2 potential'),('hH','STANDING_SOURCE_HYPOTHESIS','both global Hessian quadratic-form bounds'),('h_eta','STANDING_SOURCE_HYPOTHESIS','eta>0'),('h_beta_eta','STANDING_SOURCE_HYPOTHESIS','beta*eta<=1')]
definition_specs=[
 ('c',25,25,['S3.E4.m1'],'Exact actual center y-eta*gradient V xRef; same V/eta/reference.'),
 ('h',26,26,['S3.E4.m1'],'Exact actual residual gradient V x-gradient V xRef; not an arbitrary supplied normal.'),
 ('R',27,28,['S2.E4.m1','A1.Ex3.m2'],'At nonzero n this is (I-2nn^T/normn^2)p. At zero n, real total division and smul_zero give p, the exact R0=I extension. No normal-nonzero premise.'),
 ('S',29,30,['A1.Ex3.m2','alg1.l7.m1'],'Actual position is fixed; reflection uses same h(xRef,z.1) and actual momentum z.2.'),
 ('rate',31,32,['S3.E9.m1','A1.Ex1.m1'],'Exact sqrteta*positive_part(inner(p,h)); max0 ordering and positive sign match source.'),
 ('H',33,34,['A1.Ex4.m1'],'Exact half of weighted SUM of separate squared norms; same c, no product-norm substitution.')]
definitions=[{'name':n,'header':linepin(a,z),'source_math_ids':ids,'decision':'exact source semantics after elaboration','reason':reason} for n,a,z,ids,reason in definition_specs]
clausespec=[
 ('C01',35,35,['N11','N17'],['A1.SS2.p3'],'Actual bounce jointly Borel over reference and phase. Source allows discontinuity at h=0; header correctly asks only Measurable. Internal zero/nonzero Borel bridge required.'),
 ('C02',36,36,['N05','N16'],['A1.SS2.p3','A1.Ex1'],'Actual rate jointly continuous: gradient continuity from C2 and continuous inner/max/sqrt(fixed eta). A source-derived regularity consequence, not an added caller.'),
 ('C03',37,37,['N16'],['A1.SS2.p3'],'Actual rate jointly Borel, directly source-asserted and follows from C02 with BorelSpace products.'),
 ('C04',38,38,['N09'],['S2.E4.m1','A1.EGx1'],'Separate R0=p forces exact source zero extension of the total-division definition.'),
 ('C05',39,40,['N10'],['S2.E4.context74','A1.SS1.p1.3'],'All n,p reflection involution/norm conservation/negative normal inner product. Real inner symmetry matches p^T n; includes zero normal.'),
 ('C06',41,42,['N12','N13'],['A1.EGx1','A1.SS1.p1.3'],'Actual S fixes position and is involutive because the second bounce uses the unchanged same residual.'),
 ('C07',43,44,['N18','N19'],['A1.Ex4','A1.SS1.p3.2'],'Same actual H conserved by bounce for every y,xRef,z: first coordinate fixed and momentum norm preserved.'),
 ('C08',45,49,['N14','N15','N10'],['A1.Ex1','S2.E4.context74'],'Nonnegative rate plus exact flipped positive part and rate difference. Last two are source-derived algebraic auxiliaries: a_+-(-a)_+=a and the normal-sign law; not a path or invariance theorem.'),
 ('C09',50,51,['N09','N12','N15'],['A1.SS1.p1.3','A1.EGx1'],'Actual zero residual implies identity bounce and zero rate, including all rank-zero and p-zero cases.'),
 ('C10',52,59,['N18','N20','N21','N22','N23','N24'],['A1.Ex4','A1.Ex5','A1.Ex6','A1.SS1.p3.3'],'Same actual H nonnegative, exact two norm bounds and rate cap on each deterministic energy equality layer H(z)=H(z0). Universal z0 is a phase reference, not a random path producer. beta-Lipschitz gradient must be internal from original hV/hH. All coefficients/order/signs agree.')]
clauses=[{'clause_id':k,'header':linepin(a,z),'source_nodes':ns,'source_ids':ss,'decision':'accept prospective source-backed conclusion','reason':why,'implementation_status':'not reviewed; empty proof body'} for k,a,z,ns,ss,why in clausespec]
node_targets={
 'N01':('original typing and local universal inputs',[17,19,35,59]),'N02':('original caller hV',[20,20]),'N03':('original curvature callers',[20,23]),'N04':('original eta callers',[24,24]),'N05':('internal C2-to-gradient continuity obligation',[36,37]),
 'N06':('local actual residual',[26,26]),'N07':('local actual center',[25,25]),'N08':('local total reflection',[27,28]),'N09':('zero extension C04/C09',[38,38,50,51]),'N10':('reflection algebra C05/C08',[39,40,45,49]),'N11':('internal R joint-Borel ingredient for C01',[35,35]),'N12':('actual S definition and C06',[29,30,41,42]),'N13':('actual S algebra C06',[41,42]),'N14':('actual rate definition',[31,32]),'N15':('rate algebra and zero residual C08/C09',[45,51]),'N16':('actual rate continuity/Borel C02/C03',[36,37]),'N17':('actual S Borel C01',[35,35]),'N18':('same actual H',[33,34]),'N19':('bounce H conservation C07',[43,44]),'N20':('same-H norm bounds C10',[52,59]),'N21':('internal beta-Lipschitz gradient ingredient for C10',[52,59]),'N22':('internal residual growth ingredient for C10',[52,59]),'N23':('internal positive-part Cauchy ingredient for C10',[52,59]),'N24':('statewise same-H cap C10',[52,59]),
 'N25':('inherited source flow/Borel context: not asserted, imported or used as formal parent',[]),'N26':('actual-path conservation/cap remains open',[]),'N27':('PDMP/Proposition3.1 remains open',[]),'N28':('terminal kernel/operator remains open',[])}
projection=[]
for q in coverage['rows']:
    n=q['source_node']
    projection.append({'item_id':q['item_id'],'StageA_classification':q['classification'],'StageA_source_node':n,'source_id':q['source_id'],'header_projection':node_targets[n][0] if n else 'EXCLUDED remains outside theorem','header_lines':node_targets[n][1] if n else [],'implementation_credit':False})
assert len(projection)==95
bridge=[]
for n in graph['nodes']:
    if 'INTERNAL_OBLIGATION' in n['kind']:
        bridge.append({'source_node':n['node_id'],'meaning':n['meaning'],'required_for_header':node_targets[n['node_id']][0],'producer_status':'MUST_BE_INTERNALLY_PROVED_LATER; NO_PUBLIC_CALLER','source_anchor':n['source_id']})
assert len(bridge)==13
obmap=[]
for o in oblig['obligations']:
    i=int(o['id'][1:]);status='satisfied as prospective syntax/semantics; proof not supplied'
    if i in [4,10,11,14,18,19,20,21]:status='internal future proof obligation required by accepted header; not a new binder'
    if i in [22,24,25,26]:status='scope boundary preserved; no corresponding completed result claimed'
    obmap.append({'id':o['id'],'expectation':o['expectation'],'header_decision':status,'blocking':False})
linecoverage=[]
for i,l in enumerate(lines,1):
    if not l.strip():label='presentation blank'
    elif i<=3:label='imports: typing/reusable mathematics; no73 formal parent'
    elif 5<=i<=9:label='attribution and explicit stochastic truth boundary'
    elif 10<=i<=14:label='namespace/options/type conventions'
    elif i==16:label='private literal Prop declaration; specification not provider'
    elif 17<=i<=24:label='private original16 binders (6typing+4source inputs+6standing)'
    elif 25<=i<=34:label='source-exact local actual definitions'
    elif 35<=i<=59:label=next(k for k,a,z,_,_,_ in clausespec if a<=i<=z)
    elif i==61:label='public theorem identity'
    elif 62<=i<=69:label='public original16 binders byte-identical to private and73'
    elif i==70:label='public return is same private literal; empty by tail, no proof'
    else:raise AssertionError(i)
    linecoverage.append({'line':i,'classification':label,'RAW_sha256':sha(l)})
write('header74.coverage-projection.json',{'source_item_count':95,'source_counts_unchanged':coverage['counts'],'source_graph_unchanged':stage['graph'],'whole_header_lines':70,'top_level_clauses':10,'source_item_projection':projection,'all70_line_classification':linecoverage,'all28_node_projection':[{'node_id':n,'header_projection':v[0],'header_lines':v[1]} for n,v in node_targets.items()],'all26_obligations':obmap,'13_internal_bridges':bridge,'not_a_Lean_graph_or_proof':True})
write('header74.binders-definitions-clauses.review.json',{'binders_per_declaration':{'total':16,'TYPING':6,'SOURCE_INPUT':4,'STANDING_SOURCE_HYPOTHESIS':6,'EXCESS':0},'binders':[{'name':a,'class':b,'reason':c} for a,b,c in binders],'exact_six_prefix_comparison73':{'RAW_bytes':len(prefix),'RAW_sha256':sha(prefix),'private_public_and73_equal':True},'definitions':definitions,'conclusions':clauses,'all_ten_clauses_reviewed':True,'retained_versus_required':'All original six callers are retained. Local reflection algebra needs no curvature; rate regularity needs C2 gradient continuity; H and its energy norm bounds use eta>0; the cap needs an internally derived beta-Lipschitz gradient. This header-only review does not determine which assumptions an eventual proof actually uses. alpha>0, alpha<=beta and beta*eta<=1 may be retained standing context beyond this deterministic edge.','no_12witness_claim':'This is a sibling bounce/rate theorem, not an extension of the earlier corrector tuple; it neither imports73 nor restates its nine flow conclusions.'})

review='''The exact70-line prospective header is accepted for source-facing statement admission only. It retains the six original analytic callers with the same466-byte prefix as73 and repeats that prefix exactly in private/public declarations. There are6 typing binders,4 source input parameters and6 standing analytic hypotheses per declaration, with0 excess public premise. MeasurableSpace/BorelSpace specify the ordinary finite-dimensional Borel realization. No CompleteSpace, nonzero normal, positive rank, strict alpha*eta<1, gradient-continuity/Lipschitz, integrability, invariant-kernel or nonexplosion premise is introduced.

The six local definitions all use the SAME V,eta,reference and actual center. The total real-division reflection is equivalent to the source nonzero formula plus R0=I: at n=0 the inner product and denominator vanish and real division by zero is0, leaving p unchanged. At n!=0 it is the rank-one reflection fromS2.E4. The separate R0 clause confirms the total extension. S reflects the actual gradient difference and fixes x; the second bounce uses the unchanged x/reference. Rate is exactly sqrteta times max(0,inner(p,h)). H is exactly half of the weighted SUM of the individual squared norms, not a product norm.

All10 top-level clauses were compared to the frozen source expectations. C01 requests joint Borel, correctly allowing the source discontinuity at zero normal. C02/C03 obtain rate continuity/Borel from the same C2 gradient. C04--C07 are zero-safe reflection/bounce algebra and SAME-H preservation. C08 adds useful source-derived auxiliary identities: reflected normal inner changes sign, hence reflected rate is sqrteta*(-a)_+, and lambda-lambda_after=sqrteta*a because a_+-(-a)_+=a. These are algebraic consequences of the cited reflection/rate, not extra source hypotheses or a claim of invariance. C09 exactly retains the source zero-rate/identity convention.

C10 now includes the optional envelope identified before seeing the header. It quantifies an arbitrary phase point z0 and the SAME actual energy equality layer H(z)=H(z0). Nonnegative H yields normp<=sqrt(2H0) and norm(x-c)<=sqrt(2etaH0). Original C2/Hessian data must internally produce gradient beta-Lipschitz; this gives normh<=beta*norm(x-xRef)<=beta*(norm(x-c)+norm(c-xRef)). Positive-part Cauchy gives max(0,inner(p,h))<=normp*normh. Multiplication by nonnegative sqrteta and substitution give exactly the header/source cap with the same coefficient order and center. No arbitrary cap provider or beta-Lipschitz caller is allowed. The layer condition is a local quantified mathematical relation, not a new original analytic caller and not a theorem that an actual recursive random path stays in that layer.

The complete frozen95-item source classification is projected without alteration:38 NODE source ingredients and57 EXCLUDED source items. All28 source nodes and52 edges remain the independently frozen source graph. N25 is retained flow source context, not a74 formal dependency; N26--N28 actual-path/PDMP/terminal consumers remain open. The70 header lines,10 clauses,6 local definitions,26 source obligations and13 internal bridges all have finite records. NODE and an asserted prospective conclusion grant no implementation credit.

Attribution names Chen--Chewi--Lu--Zhang match the primary author tags. The precise source URLs/anchors are verified against the fixed local HTML:2609.06905v1#S2.E4,#S3.E4,#S3.E9,#alg1,#A1.Ex4--Ex6 and#A1.SS2.p3. The broad AppendixA.1 attribution in the comment is accurate; A1.SS2.p3 is the more precise later publication anchor for the Borel ingredient. No current publication exists in this review scope and no URL repair is needed. Eventual reader publication must expose the complete private literal adjacent to the public signature under its exact full identity, as a definition/specification and never a mathematical provider.

No theorem proof or production74 BODY was supplied or read. External predicate driver52824 EXIT1 was preserved; its sole section-end insertion was mechanically compared and driver53780 EXIT0 is only predicate typing context. It is not a theorem compile. Source/preread judgments from other agents were not read. The seal includes an opaque source-plan locator/hash and the typing receipt includes opaque73 adoption locators; none of their judgments were used. Earlier70--73 exposure was disclosed before74. The original StageA files remain byte-identical and were frozen before any74 candidate/hash. No canonical/Git/ledger/old CLOSED write, SAU/VERIFIED/fullpaper/Goal claim or self-approved repair occurs.
'''
(OWN/'source-header.0.review.md').write_text(review,encoding='utf-8',newline='\n')
decision={
 'schema':'ASTIS_BOUNDED_PROSPECTIVE_SOURCE_HEADER_REVIEW_V1',
 'status':'ACCEPT_PROSPECTIVE_HEADER_SOURCE_ONLY',
 'verdict':'equivalent-after-elaboration',
 'candidate':pin(H),'statement_seal':pin(SEAL),
 'StageA_before_header':pin(OWN/'stageA.freeze74.json'),
 'StageA_whole_logical_run_sha256':stage['run_sha256'],
 'primary':pin(PRIMARY),
 'source_contract_counts':{'source_regions':15,'source_blocks':53,'source_items':95,'NODE':38,'EXCLUDED':57,'exact_formulas':21,'source_nodes':28,'source_edges':52,'source_obligations':26,'internal_future_bridges':13,'header_lines':70,'definitions':6,'top_level_conclusions':10,'original_analytic_callers':6,'excess_public_premises':0},
 'binder_definition_clause_review':pin(OWN/'header74.binders-definitions-clauses.review.json'),
 'exhaustive_coverage_projection':pin(OWN/'header74.coverage-projection.json'),
 'source_anchors':[{'url':'https://arxiv.org/html/2609.06905v1#'+a,'primary_id_verified':True} for a in anchors],
 'mathematical_or_source_blocking_deltas':[], 'required_statement_repairs':[], 'repair_proposals_authored':[],
 'independent_findings':['Total-division R matches exact source R0=I extension; separate zero clause included.','Actual S jointly Borel only; no false global continuity assertion.','Rate flip/difference clauses are exact source-derived algebraic consequences.','Last clause is SAME actual H equality-layer envelope, not a produced random path cap.','beta-Lipschitz and all regularity/Borel/energy bridges remain internal proof obligations, never new original callers.','73 and74 are siblings; no formal73/68/corrector parent is invented.','All original six standing analytic callers retained; rank0 and alpha*eta=1 allowed.'],
 'header_only_reader_contract':{'private_literal_full_identity':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_statement','meaning':'complete Prop definition/specification, never provider','future_publication_must_expose_complete_adjacent_literal':True,'current_reader_acceptance':False},
 'typing_context_only':{'original_predicate_driver_PID':52824,'original_EXIT':1,'section_end_repaired_driver_PID':53780,'repaired_EXIT':0,'predicate_body_byte_preserved':True,'no_theorem_proof_or_compile_credit':True},
 'anti_anchoring':{'StageA_precedes_first74_header_hash':True,'earlier70_71_72_73_exposure_disclosed':True,'other_agent_preread_or_header_math_verdict_read':False,'seal_sourceplan_and_receipt73_adoption_hashes_opaque_only':True,'74_proof_or_production_BODY_read':False},
 'remaining_boundary':['future74 proof and independent whole-module source review','actual path conservation/cap and integrated hazard/clocks','PDMP/nonexplosion/Markov/Proposition3.1','invariance/stationarity and H_y/K/r_rho/B27/B28','main/errors/caps/expected-query cost/fullExposition/PURIFIED/wholepaper/Goal'],
 'credits':{'prospective_source_header_admission':True,'implementation_source_fidelity':False,'Lean_theorem_compile':False,'proof_search':False,'SAU_claim':False,'VERIFIED':False,'wholepaper':False,'Goal':False},
 'canonical_changes_made':False,'old_closed_writes':False
}
write('source-header.0.decision.json',decision)
input_payload={'LF_recipe':'CRLF byte pairs -> LF only; preserve bare CR and every other byte','external_current_and_context_pins':[pin(p) for p in inputs],'exact_current_small_snapshots':snapshots,'exact_header_RAW_UTF8':raw.decode('utf-8'),'exact_header_CRLF_only_LF_UTF8':raw.replace(b'\r\n',b'\n').decode('utf-8'),'statement_seal_RAW_UTF8':SEAL.read_bytes().decode('utf-8'),'StageA_native_reuse':{'freeze':pin(OWN/'stageA.freeze74.json'),'manifest':pin(OWN/'stageA.manifest74.json'),'full_named_source_payload':pin(OWN/'stageA.complete-named-source-payload74.json'),'unchanged_verified':True},'type_driver_one_end_insertion_only':{'original':pin(original),'fixed':pin(fixed),'diagnosis':pin(diagnosis),'failure_receipt':pin(failreceipt),'success_receipt':pin(passreceipt),'other73judgments_not_loaded':True},'no_recursive_old_payload_or_base64':True}
write('source-header.0.input-payload.json',input_payload)
write('terminal.header-review74.receipt.json',{'actual_PID':os.getpid(),'EXIT':0,'argv':sys.argv,'scope':'prospective header source review only','independent_readonly_checks_observed':[{'PID':52096,'EXIT':0,'meaning':'exact74 hash and private caller prefix vs73'},{'PID':45880,'EXIT':0,'meaning':'primary authors and all source anchor IDs'}],'root_predicate_context_no_proof_credit':[{'PID':52824,'EXIT':1},{'PID':53780,'EXIT':0}],'StageA_and_all_external_pins_rechecked':True,'no_Lean_rerun':True,'no_canonical_old_closed_or_Git_write':True})
named={'review':{'path':pin(OWN/'source-header.0.review.md'),'complete_text':review},'decision':decision,'input_payload':input_payload,'source_coverage_projection':read('header74.coverage-projection.json'),'binders_definitions_clauses':read('header74.binders-definitions-clauses.review.json'),'terminal':read('terminal.header-review74.receipt.json')}
write('complete-named-review-decision-input-payload.json',named)
run={'kind':'INDEPENDENT_SOURCE_HEADER74_NATIVE_RUN','complete_named_review_decision_input_payload':named,'named_payload_artifact':pin(OWN/'complete-named-review-decision-input-payload.json'),'StageA_frozen_native_reused_unchanged':pin(OWN/'stageA.freeze74.json'),'logical_hash_recipe':'Delete ONLY the top-level run_sha256 key, then UTF8 JSON ensure_ascii=False sort_keys=True separators=(comma,colon); preserve all nested keys.','no_theorem_or_implementation_credit':True}
run['run_sha256']=sha(canon(run));write('source-header.0.run.json',run)
print(json.dumps({'actual_PID':os.getpid(),'EXIT':0,'decision':pin(OWN/'source-header.0.decision.json'),'run':pin(OWN/'source-header.0.run.json'),'whole_logical_run_sha256':run['run_sha256'],'review_files_written_before_close':True}))
