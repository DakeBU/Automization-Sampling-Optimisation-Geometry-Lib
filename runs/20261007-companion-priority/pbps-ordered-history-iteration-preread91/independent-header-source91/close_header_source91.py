from pathlib import Path
import json,hashlib,re,datetime
ROOT=Path('E:/Samplinglib');PRE=ROOT/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91';OUT=PRE/'independent-header-source91';SF=PRE/'independent-source-first91'
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(n,x):
 p=OUT/n;assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return raw(p)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';assert raw(primary)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
packet=PRE/'header-review91.packet.json';assert raw(packet)['raw_sha256']=='5e4d8ea4a642aa2a86fa3e921372f1e9e177048c6a036deb203e3fb97ef027e3'
header=PRE/'header91.proposed.lean';assert raw(header)['raw_sha256']=='b8bba160f6134c7927167a0a34d99971ce75023ef7ea04f738a91b6862da2680' and raw(header)['bytes']==7767
accepted=PRE/'source-proof-graph91.accepted-successor.json';assert raw(accepted)['raw_sha256']=='0a1351bbb9aeeb5556892fcf6c0265527fba38618f297a0a75b9ebef076de5c5'
oldgraph=SF/'source-proof-graph91.v2.native.json';inv=read(SF/'source-inventory91.primary-first.native.json')
b=primary.read_bytes();ls=b.splitlines(keepends=True);spans=[]
for aid,a,z in [('license-version',257,261),('A1.E1-E2',2859,2911),('A1.E7',3147,3173),('A2-Borel',3325,3339)]:
 c=b''.join(ls[a-1:z]);spans.append({'id':aid,'line_start':a,'line_end':z,'byte_start':sum(map(len,ls[:a-1])),'byte_end_exclusive':sum(map(len,ls[:z])),'raw_sha256':hashlib.sha256(c).hexdigest(),'html':c.decode('utf8')})
private=write('header91.primary-reread.private.json',{'private_primary_extracts':True,'primary':raw(primary),'source_read_before_header_packet':True,'spans':spans,'license':'arXiv.org perpetual non-exclusive license','version':'arXiv:2609.06905v1 [math.ST] 07 Sep 2026'})
hb=header.read_bytes();h=hb.decode('utf8');old=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean';ob=old.read_bytes()
start=hb.index(b'    let c :');stop=hb.index('    ∀ y xRef :'.encode('utf8'));ostart=ob.index(b'    let c :');ostop=ob.index('    ∀ y xRef :'.encode('utf8'));assert hb[start:stop]==ob[ostart:ostop]
model_digest=hashlib.sha256(hb[start:stop]).hexdigest()
matches=list(re.finditer(r'^( {4}| {6}| {8})let ([^ :\n]+)',h,re.M));names=[m.group(2) for m in matches]
assert names[:14]==['c','Φ','S','rate','Λ','τ','next','record','P','ε','history','waitObs','timeObs','density']
assert len(names)==35,names
meaning={
 'c':'Literal source center y-eta gradient V(xRef).',
 'Φ':'Literal all-real harmonic flow with sqrt eta scaling; negative times are meaningful analytic flow values, not asserted negative waiting events.',
 'S':'Literal momentum reflection; Lean real division by0 and zero vector yield identity at zero normal, agreeing R0=I.',
 'rate':'sqrt eta times positive part of momentum dot gradient difference. Nonnegativity derived internally.',
 'Λ':'Integrated hazard on nonnegative NNReal time, real interval integral from0 to t.',
 'τ':'Actual threshold infimum hittingAfter of Λ-e into Ici0, on nonnegative time; infinity when no crossing.',
 'next':'Stopped absorbs; live infinite wait becomes stopped; finite wait adds to absolute NNReal time and applies literal flow/bounce.',
 'record':'Actual recursion starts live(0,z0), consumes e_k at step k, all finite depths.',
 'P':'Actual infinite product of expMeasure1 on raw real coordinates; probability and iid facts are internal dependencies, not provider binders.',
 'ε':'Clips each raw real threshold to NNReal; agrees almost surely with positive exponential input; no negative-coordinate event guarantee.',
 'history':'Complete tuple j=0,...,n of actual records; not just last state.',
 'waitObs':'Next actual τ from live record and raw unused coordinate, stopped0 auxiliary.',
 'timeObs':'Real finite wait extraction untopD0; live-infinite and stopped extraction0 auxiliary only, excluded by strict event.',
 'density':'Real-time deterministic rho converted by ENNReal.ofReal; stopped0. Negative time uses raw flow with clipped hazard time, but strict finite density uses positive relative time only.',
 'Rec':'NNReal cumulative-time/phase live sum Unit stopped tag, preserving infinity through tag rather than fictitious phase.',
 'Hist':'Fin(n+1) full current history.',
 'HistNext':'Fin(n+2) full next history.',
 'last':'Index n in current history, not random stopping index.',
 'lastNext':'Index n+1 in next complete history.',
 'H':'Actual current full history at fixed y,xRef,z0,n.',
 'Hnext':'Actual next complete history, not supplied constructor output.',
 'readTime':'Real time extracted from live record; stopped0 auxiliary, never infinity mass assertion.',
 'a':'Read actual/abstract current last-record time, nonnegative even with stopped fallback0.',
 'U':'Reads literal next actual record at n+1. Equality with a(H)+finiteWait is a conclusion on B, never imposed as a premise or used to redefine away the obligation.',
 'appendRel':'Exact90 complete-prefix append: live(T,z) appends live(T+max(s,0),SΦ_s z), stopped appends stopped. Raw negative-time flow/clipped increment auxiliary.',
 'appendAbs':'appendRel(h,u-a(h)); on arbitrary live h total cumulative time T+max(u-T,0); equals u only on a<u. Stopped branch absorbs and all old records retained.',
 'liftAbs':'Joint (complete appended history,u), Borel total map to next-history x real.',
 'd':'Positive part of b(h)-a(h), finite Borel relative cutoff; b<a or b=a gives0.',
 'μ':'Actual full history pushforward map H P; no supplied history distribution.',
 'D':'Strict a(h)<u<b(h) times rho_z(u-a(h)); stopped density0 even though live test is inside density rather than guard. Exactly strict positive relative support.',
 'Brel':'Actual next-wait guard0<W_n<d(H), with raw threshold w_n=source E_(n+1). No normalization.',
 'B':'Actual current and next record live, a(H)<U<b(H). Brel=B must be derived on every raw sample, including clipped-zero inputs.',
 'X':'Actual current complete history/next literal absolute time pair.',
 'Y':'Actual next complete history/next literal absolute time pair.',
 'ν':'True real product-reference density measure (μ product real Lebesgue).withDensity D; finite subprobability and density measurability are conclusions, no provider/fallback kernel.'}
defs=[]
for i,m in enumerate(matches):
 name=m.group(2);end=matches[i+1].start() if i+1<len(matches) else h.index('\n        Measurable (Function.uncurry D)',m.start())
 if name=='density':end=h.index('    ∀ y xRef :',m.start())
 if name=='liftAbs':end=h.index('\n      Measurable H',m.start())
 body=h[m.start():end];bp=hb[:len(h[:m.start()].encode('utf8'))];bs=body.encode('utf8')
 defs.append({'name':name,'class':'literal-model' if i<14 else 'literal-typed-coordinate/test-interface','exact_Lean':body,'byte_start':len(bp),'byte_end_exclusive':len(bp)+len(bs),'raw_sha256':hashlib.sha256(bs).hexdigest(),'source_restated_meaning':meaning[name],'relation':'equivalent-after-elaboration','source_force':'Author literal construction/standing notation' if i<11 else 'ASTIS bounded source-implicit observable/coordinate/test completion; auxiliary branches explicitly guarded','hidden_regularities':'All required model/observer/density/constructor measurability and law identities are conclusions/internal edges, no new premise.'})
assert set(names)==set(meaning)
binder_audit=[
 {'binder':'E; normed additive real inner-product finite-dimensional/Borel structures','classification':'TYPING','source':'Finite Euclidean source carrier; coordinate-free finite-dimensional formulation includes rank0. Compatible finite-dimensional Euclidean volume is used only for source phase elsewhere; time here is exactly real Lebesgue.'},
 {'binder':'V:E->R; alpha,beta:NNReal; eta:R','classification':'TYPING','source':'Source potential/curvature/scale parameters. Nonnegative alpha/beta types plus explicit positivity/order retain source assumptions.'},
 *[{'binder':a['id'],'classification':'STANDING','formula':a['formula'],'source_anchor':a['source_anchor']} for a in read(accepted)['source_hypotheses']],
 {'binder':'forall y,xRef:E,z0:E x E,n:Nat','classification':'TYPING','source':'Arbitrary fixed source parameters, starting phase and deterministic event depth. Never a random stopping depth.'},
 {'binder':'forall b:Hist->NNReal; Measurable b','classification':'TYPING-ADMISSIBLE-TEST-CLASS','source':'Fixed Borel finite-valued absolute horizon; can be globally unbounded. b(H) random via history, no independent random b, no unused-tail inspection. Constant b=T is real A7 consumer.'},
 {'binder':'forall G:Hist x R->ENNReal; Measurable G','classification':'TYPING-ADMISSIBLE-TEST-CLASS','source':'All nonnegative joint old-history/absolute-time tests; no boundedness or integrability premise.'},
 {'binder':'forall F:HistNext x R->ENNReal; Measurable F','classification':'TYPING-ADMISSIBLE-TEST-CLASS','source':'All nonnegative joint next-complete-history/absolute-time tests; generalized interface for internal Tonelli assembly, not replacement of printed bounded A7 path test.'},
 {'binder':'forall A:Set Hist; MeasurableSet A','classification':'TYPING-ADMISSIBLE-TEST-CLASS','source':'All Borel old-history localization events, possibly null; unnormalized restricted integral, no division or regular-conditional representative.'},
 {'binder':'forall p,j and forall w in B, forall h in Hist','classification':'TYPING-CONCLUSION-QUANTIFIERS','source':'Every-history prefix preservation/fiber bound and pointwise actual guarded identities. They are claims to prove, not provider inputs.'}]
slots={
 'objects':{'original':'Literal stopped iid exponential recursion, complete finite histories and next actual jump time from A1.E1/E2; absolute coordinate ingredient of strict A7 simplex.','reconstructed':'Full actual H,Hnext; U reads next literal record; ν is strict absolute-coordinate density under actual μ; appendAbs/liftAbs derive next complete-history transport.','evidence':'Header14modeldefs byte-identical to actual90; explicit U=readTime(Hnext lastNext),35literal defs expanded; private source spans A1.E1/E2/A7/A2.','relation':'equivalent-after-elaboration'},
 'domains':{'original':'Finite Euclidean phase, nonnegative waits with infinity/stopped convention, strict absolute times before finite horizon; all past events unnormalized.','reconstructed':'Finite-dimensional real inner-product Borel E; complete tagged Hist/HistNext; raw real iid input; real Lebesgue absolute u; b:Hist->NNReal finite, all Borel A and joint ENNReal tests.','evidence':'Private Prop binders and let Rec/Hist/HistNext,P,b,ν; stopped0 extraction guarded, no finite/infinite phase conflation.','relation':'equivalent-after-elaboration'},
 'quantifiers':{'original':'For fixed source parameters and deterministic event depth, future independent input conditional on generated past; final strict horizon fixed in A7.','reconstructed':'forall y,xRef,z0,n then every fixed Borel b; all abstract h for fiber bound; all p,j prefix entries; all actual w in B for identities; all G/F/A.','evidence':'Header forall y...n, forall b Measurable b, U and Brel raw coordinate n; constant b(h)=T supplies d_T.','relation':'equivalent-after-elaboration'},
 'assumptions':{'original':'V C2,0<alpha<=beta,global Hessian sandwich,0<eta<=1/beta and source iid Exp1 construction.','reconstructed':'Exactly six hα,hαβ,hV,hH,hη,hβη; probability input constructed as literal P. Other hypotheses only admissible Borel b/G/F/A and typing.','evidence':'Six recursively explicit analytic binders; no density/constructor/independence/probability/measurability provider assumption; beta positivity follows internally from alpha/order, beta*eta<=1 equivalent allowed eta bound.','relation':'equivalent-after-elaboration'},
 'conclusion':{'original':'ASTIS implicit strict one-step absolute-time coordinate law needed for ordered A7 iteration, derived from finite recurrence and conditional density.','reconstructed':'Joint Borel D and every-history fiber mass<=1; Brel=B; actual shift and complete append on B; exact actual pair ν law and next-history pushforwards; ν(univ)<=1; all nonnegative joint localized identities with measurable parameter integrals.','evidence':'Entire final private Prop conjunction; both sides strict, no endpoint mass comparison. New weighted product-reference identity exceeds mere renaming of90 relative law.','relation':'equivalent-after-elaboration'},
 'scopes_senses':{'original':'Fixed event-depth conditioning from iid unused tail; absent infinite/outside-cutoff mass retained. Full ordered-time/count/path A7 is future consumer.','reconstructed':'Unnormalized restricted P and actual μ; null A allowed; live infinite waits excluded by finite strict event, stopped finite density0; total auxiliary values off support never physical events.','evidence':'Brel=B as conclusion, explicit live tags in B, D stopped branch0, withDensity real product reference, header opening boundary and acceptedgraph S91C.','relation':'equivalent-after-elaboration'},
 'constant_dependencies':{'original':'Source parameters alpha,beta,eta,V,y,xRef,z0, finite depth and horizon; no new smoothness/cap certificate.','reconstructed':'Same parameters; no new numeric constant or bound required. b may vary by entire past; fiber mass1 derives internally.','evidence':'Six analytic binders unchanged; hypotheses contain no new derivative, rate-cap, endpoint-atom or survival assumption.','relation':'equivalent-after-elaboration'}}
coverage=[]
for item in read(SF/'source-coverage91.v2.native.json')['coverage']:
 entry={'id':item['id'],'anchor':item['anchor'],'frozen_disposition':item['local_disposition'],'header_disposition':'EXCLUDED/FUTURE_REMAINS_OPEN','reason':'Only S91C absolute-coordinate ingredient accepted prospectively; no full-A7 credit.'}
 if item['id'] in ['C02','C03']:entry.update({'header_disposition':'SOURCE_ANALYTIC/TYPING_RETAINED','reason':'Six source analytic binders explicitly retained.'})
 elif item['id'] in ['C04','C05','C06','C07']:entry.update({'header_disposition':'LITERAL_SOURCE_MODEL_RETAINED','reason':'Exact source formulas/actual iid recursion retained; model14 byte-identical to90.'})
 elif item['id'] in ['C08','C10','C11','C14','C15','C21','C25','C26','C27']:entry.update({'header_disposition':'PROSPECTIVE_S91C_INGREDIENT','reason':'Whole-history Borel positive-cutoff translation, actual record observer and derived strict restricted law; future induction/path part still open where item broader.'})
 elif item['id']=='C19':entry['reason']='Reuse existing actual78/79 as recorded; no redo/nonaccumulation provider and no full path/count identification claim.'
 coverage.append(entry)
relations=[
 {'id':'H91-D1','source':'Author A7 suppresses the conditional relative-to-absolute coordinate derivation.','lean':'All-history Borel b and D_abs, actual U observer, Brel=B and real weighted product law.','classification':'SOURCE_IMPLICIT_REQUIRED_COMPLETION','reason':'History-dependent translation and actual recurrence identification derive the needed ordered next-coordinate law; no extra public analytic hypothesis.','blocking':False},
 {'id':'H91-D2','source':'Printed A7 tests bounded measurable complete paths at fixed finite T.','lean':'All joint nonnegative finite-history/time tests and all Borel b/A.','classification':'FAITHFUL_INTERNAL_TEST_CLASS_GENERALIZATION','reason':'Measure identity/Tonelli substrate; constant b=T is source consumer. Does not assert arbitrary path functional A7 or add source analytic assumptions.','blocking':False},
 {'id':'H91-D3','source':'Infinite next wait stops recursion; physical phase update only finite positive times on probability-one positive thresholds.','lean':'Stopped readTime/timeObs0 and appendAbs raw negative relative flow/clipped increment on total carrier.','classification':'EXPLICIT_GUARDED_AUXILIARY_TOTALIZATION','reason':'Live tags/strict guard exclude stopped/infinite/zero/negative-event values; literal physical update derived on B. Off-support time T+max(u-T,0) retained accurately.','blocking':False},
 {'id':'H91-D4','source':'A7 strict absolute simplex.','lean':'Both density/event use a<u<b, Brel=B proved without comparing endpoint masses.','classification':'EXACT_STRICT_ENDPOINT_RESTRICTION','reason':'No no-atom binder or equal-Ioc/Ioo-mass assertion. Later count convention equivalence remains separate.','blocking':False},
 {'id':'H91-D5','source':'Six original analytic hypotheses and actual iid input construction.','lean':'Same six explicit analytics; Borel b/G/F/A only admissible test-domain conditions.','classification':'NO_EXCESS_ANALYTIC_OR_PROVIDER_PREMISE','reason':'All model/density/observer measurability, independence, actual equalities and subprobability facts are conclusions/internal proof ingredients.','blocking':False}]
decision=write('header91.source-decision.native.json',{'schema':'astis-independent-source-header-review91-v1','utc':now,'reviewer':'/root/fresh_source87','formalizer':'/root','review_type':'Prospective whole private Prop SOURCE semantic audit; no BODY/Seal/claim/proof completion','packet':raw(packet),'header':raw(header),'primary':raw(primary),'primary_first_freeze':raw(SF/'primary-first91.freeze.native.json'),'frozen_inventory':raw(SF/'source-inventory91.primary-first.native.json'),'frozen_manifest':raw(SF/'closed-raw-manifest.source-first91.v2.native.json'),'accepted_distinct_reviewed_source_graph':raw(accepted),'source_adoption':raw(PRE/'root.source91.adoption.json'),'graph_creator_self_independent_approval':False,
 'independence':'Source reviewer distinct from formalizer and77 mathematical/typecheck reviewer. Did not read77 prospective-header verdict, new91 BODY or prior source fidelity verdict as an anchor. Prior87-90 source/header/BODY and91 creator graph familiarity disclosed; exact graph repair accepted by another reviewer, not self-approved here.',
 'verdict':'equivalent-after-elaboration','prospective_header_source_acceptance':True,'repairs':[],'semantic_slots':slots,'deltas':relations,'literal_definition_audit':defs,'model14_exact_byte_identity':{'producer':raw(old),'byte_start':start,'byte_end_exclusive':stop,'bytes':stop-start,'raw_sha256':model_digest,'equal_to_exact90_prefix':True},'binder_audit':binder_audit,'analytic_binder_count':6,'literal_definition_count':35,'exhaustive_local_coverage':coverage,
 'graph_successor_scope':'Accepted successor modifies only final future S91A7 route indexing: printed cap/simplex convergence OR nonnegative finite-count/mass-one/Tonelli route. Header closes neither route nor A7. This source-header audit does not self-approve creator topology.',
 'source_reader_interpretation':'One actual next absolute-event-time/complete-history strict density coordinate law, source-implicit completion of A1.E1/E2/A7/A2. Source authors do not print this expanded conditional theorem verbatim.',
 'hidden_regularity_obligations':['Joint Borel a,b,d,D and actual U/H/Hnext/appendAbs/liftAbs derived internally.','Lebesgue shear and inverse transport derived internally using fixed Mathlib; no differentiability of Borel b/a required.','Actual finite clock/infinity/stopped cases yield pointwise Brel=B and U=a+timeObs on B.','withDensity is identified by jointly measurable density, not a theorem-shaped input.','All-history fiber mass1 from89 explicit facet or internal translation;89 not duplicated as two independent probability AND parents.'],
 'edge_cases':{'b_le_a':'d=0 and both strict event/density supports empty, including b=0.','stopped':'Brel false because waitObs0; B false because live tags; D0; U/readTime0 auxiliary.','infinite_live_wait':'Next record stopped, B false and finite cap excludes Brel; missing mass is unnormalized.','n0':'Initial history live at time0, U actual first next record; no random-depth inference.','nullA':'Restricted integrals vanish without division; probability of A need not be positive.','rank0_zero_rate':'Finite event density0; no nonzero reflection-normal/positive-hazard premise.','unrealizable':'Definitions, measurability and fiber bound on every history; guarded actual identities only actual samples.','raw_zero_negative_clocks':'Clipping can make wait0; then U=a and strict B/Brel both false. Positive-clocks a.s. property is not an eventwise premise.','strict_endpoints':'No endpoint no-atom or exact strict total-mass formula asserted.','auxiliary_negative_relative_time':'appendAbs total live time T+max(u-T,0); equals u only on strict support. Negative flow/time0 defaults receive no source dynamics credit.'},
 'actual_A7_consumer':'Fix b(h)=T. On current live time a<T, d=(T-a)+; strict new absolute coordinate a<u<T is exactly next ordered-simplex coordinate. Actual complete-history mapping supports subsequent finite-depth density induction. Final88 survival at d_T is a later genuine consumer, not an AND parent here.',
 'existing_actual78_79_preserved':raw(SF/'existing-actual-coverage91.native.json'),'closed_target_only':'Prospective S91C one strict coordinate-density edge inside S87-I5/G86-11; not full S87-I5 or G86-11.',
 'open':['91 Lean proof/wholeBODY and source-blind decoder/final source fidelity','finite ordered induction and product of all jump factors','final survival/path-hazard/count partition and endpoint equivalence where needed','fullA7 by either preserved sufficient route','physical-time residual restart/random stopping/Markovness/global path theorem beyond exact78/79','invariance/semigroup/hypocoercivity/errors/unbounded costs/main/composition/wholepaper/Goal'],
 'no_VERIFIED_Seal_claim_or_canonical_edit':True})
chron=write('header91.chronology.native.json',{'schema':'astis-source-header-chronology91-v1','utc':now,'events':[{'order':1,'event':'Created only independent-header-source91; direct pinned primary RAW and version/license/A1E1E2/A7/A2 reread before packet/header.'},{'order':2,'event':'Read exact clean header packet and whole7767B header; bound independent source-first freeze and exact accepted graph successor.'},{'order':3,'event':'Compared accepted successor to immutable creator v2: only futureA7 OR/junction additions; did not read77 header verdict or independent repair verdict as fidelity evidence.'},{'order':4,'event':'Independently reconstructed all35 literal definitions,6analytic binders, every test-domain quantifier and guard/observer/transport conclusions against primary.'},{'order':5,'event':'Closed native prospective source decision/run/RAW manifest. No proof search or canonical/header edits.'}],'prior_familiarity':'87-90 independent source and prospective header audits;91 primary-first creator graph/proposal. This is disclosed, not claimed blind.'})
run=write('header91.source-run.native.json',{'schema':'astis-independent-source-header-run91-v1','utc':now,'reviewer':'/root/fresh_source87','formalizer':'/root','packet_raw':raw(packet),'header_raw':raw(header),'primary_raw':raw(primary),'decision':decision,'chronology':chron,'source_read_before_header':True,'other_header_verdict_read':False,'BODY_exists_or_read':False,'terminal_closed':True,'proof_or_compiler_credit':False,'outcome':'Prospective exact-header source equivalent-after-elaboration; no repair; no final BODY fidelity acceptance.'})
def collect(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and 'raw_sha256' in x:
   p=Path(x['path']);p=p if p.is_absolute() else ROOT/p
   assert p.exists(),p;d=raw(p);assert d['raw_sha256']==x['raw_sha256'],(p,d,x)
   if 'bytes' in x:assert d['bytes']==x['bytes'],p
   yield d
  for v in x.values():yield from collect(v)
 elif isinstance(x,list):
  for v in x:yield from collect(v)
allinputs=[raw(primary),raw(packet),raw(header),raw(accepted),raw(old),raw(SF/'primary-first91.freeze.native.json'),raw(SF/'source-inventory91.primary-first.native.json'),raw(SF/'closed-raw-manifest.source-first91.v2.native.json'),raw(SF/'existing-actual-coverage91.native.json'),raw(PRE/'root.source91.adoption.json')]
allinputs+=list(collect(read(packet)))+list(collect(read(PRE/'root.source91.adoption.json')))
allinputs=list({d['path']:d for d in allinputs}.values())
snapshot=OUT/'header91.proposed.exactraw.lean';assert not snapshot.exists();snapshot.write_bytes(hb)
outputs=[raw(p) for p in sorted(OUT.iterdir()) if p.is_file()]
manifest=write('closed-raw-manifest.header-source91.native.json',{'schema':'astis-closed-raw-manifest.header-source91-v1','closed':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':allinputs,'outputs':outputs,'primary_spans':[{k:v for k,v in s.items() if k!='html'} for s in spans],'input_count':len(allinputs),'output_count':len(outputs),'manifest_self_hash_omitted':True,'no_proof_status_credit':True,'creator_self_independent_topology_approval':False})
for d in allinputs+outputs+[manifest]:assert raw(ROOT/d['path'])==d,d
print(json.dumps({'decision':decision,'run':run,'manifest':manifest,'chronology':chron,'inputs':len(allinputs),'outputs':len(outputs),'definitions':35,'analytics':6,'verdict':'equivalent-after-elaboration','repairs':[]},indent=2))
