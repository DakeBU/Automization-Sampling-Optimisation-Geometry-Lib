from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent
def data(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,o):(D/n).write_bytes(data(o))
def read(n):return json.loads((D/n).read_text(encoding='utf-8-sig'))
lp=D/'lease.json';initial=lp.read_bytes();lease=read('lease.json');assert lease['state']=='OPEN'
(D/'lease.initial.raw.snapshot.json').write_bytes(initial)
source={
 'schema_version':1,'actor':'gaussian_noncompact_preread_42','stage':'independent GaussianTalagrand44 source/API preread','status':'TYPED_OBSTRUCTION_NO_THEOREM_APPROVAL',
 'source':{'primary':'arxiv:2609.06906v1','anchors':['S2.Ex2','S2.p5.2','S4.Ex8','S4.E6','S4.SS1.p4.3'],'exact_background':'Chewi August9 2026: §1.3.1 Def1.3.4/(1.3.5), §1.4.2(1.4.3)/Thm1.4.5, Exercise1.16, §2.1.1 T2 definition and LSI implication;Example2.4.4','omission':'SPHMC FIRST namesTalagrand without proof or local citation;general CHE26 bibliography is not an exact citation claim for that sentence;Chewi transport calculus is sketched and regularity not silently supplied'},
 'true_target_shape':{'carrier':'complete finite realHilbert/Borel E, includingrank0; second countability internally derived','inputs':'µ:MeasureE, IsProbabilityMeasureµ, Integrable norm² µ (genuine textbookP2domain)','reference':'literal ProbabilityTheory.stdGaussian E,covarianceI','conclusion':'WassersteinSpace.wassersteinDistance µ (stdGaussian E)^2 <= (2:ENNReal)*InformationTheory.klDiv µ (stdGaussian E)','domain_extension':'Allprobability withoutP2 could be true with finiteKL=>moment derivation, but separately reviewed and not needed by sourceP2leaf','public_excess':['optimalcoupling/map','Brenier smoothness/Jacobian','flow/speed/convergence','law/density normalization','GaussianT2/desired inequality certificates']},
 'normalization':{'W2':'ENNReal sqrt of actual coupling infimum of integral ENNReal.ofReal(norm(x-y)^2);not a fixedcoupling pseudodistance','order':'W2(r,gamma)^2<=2 KL(r||gamma);KL ordercannotreverse;W2 symmetric','composition':'eventual coherent43 KL<=Fisher/2 givesW2²<=Fisher;thenrealnonnegative sqrt;actual31provides separatelyreported numericFisher bound','toReal':'RequirefiniteKL andW2 first;P2+Gaussianmoment givesfiniteW2 internally','covariance':'standardized covarianceI only;original RGO etaI scaling not substituted;varianceσ² wouldchangeconstant','rank0':'internal uniqueprobability/Dirac law impliesW2=KL=0;noNontrivial/dimpos hypothesis'},
 'reusable_actual_source_declarations':[
 'AutoSamplingTheory.TechnicalLemmas.Measure.Transport.IsCoupling',
 'AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost',
 'AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSpace.wassersteinDistance',
 'AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSpace.wassersteinDistance_sq',
 'AutoSamplingTheory.TechnicalLemmas.Measure.OptimalContinuousCost.exists_optimal_coupling',
 'AutoSamplingTheory.TechnicalLemmas.Measure.QuadraticOptimalBrenierMap.exists_base_map_gradient_eq_of_quadraticOptimal',
 'AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinFiniteSecondMoment.wassersteinDistance_lt_top_of_integrable_norm_sq',
 'AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSymmetry.wassersteinDistance_comm',
 'AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity',
 'ProbabilityTheory.IsGaussian.memLp_id','InformationTheory.klDiv_ne_top_iff'],
 'API_status':'Source declarations/contracts inspected; no compiler or own implementation verification. No genuineGaussianT2 producer found inbounded queriedsurfaces;not universalabsenceclaim.',
 'routes':[{'id':'static-displacement','source':'Chewi1.4.3/Thm1.4.5','available':'genuineoptimalcoupling/Breniermap, potentialenergy, matrixlogdet andconditionalCov/entropyalgebra','missing_producer_edges':['actualproducedBreniermap AE derivative/PSD onmeasurablefull effectiveinterior','actualdisplacement density/logJacobian identity pluslogdet/entropyintegrability andendpoint/approximation passage','canonicalGaussianKL chord assembly'],'strict_smallest_delta':'actualAE differentiability/PSD Jacobian ofinternallyproducedRockafellar gradient, withoutglobalC1 supplied'}, {'id':'dynamic-Otto-Villani','source':'ChewiExercise1.16/§2.1.1','available':'actual42functionLSI opaqueparent andabstractscalarjoins','missing_producer_edges':['genuineGaussianflow/evolvedcanonicaldomains','actualKLdissipation/Fisher','metric speed','convergence toactualGaussian'],'not_new_public_inputs':True}],
 'typed_blocker':{'class':'missing-actual-measure-level-transport-entropy-producer','strict_reduction':'W2 semantics/constant/sourceP2domain and actualoptimizer/Breniersubstrate fixed; entropyregularity gap isolated;dynamicroute distinctmissingflowedges','next_actual_consumer':'After43verification, actualsame-witnessSPHMC canonicalKL<=eta²finrank/2 via43androotreported31;31interfacealignment pending, noW2credit'},
 'proof_strategy_max7':'source-detail.md has seven candidate steps; missing producers explicitly unresolved; no proof implemented',
 'independence_boundary':['no43production/Test/wholemath/blind/finalsource read','no31proof/publicheader read','no44Lean/compiler/proofsearch/claim/Goal/cell/sourcegraph/canonicaledit','no selfstatement/topology/theoremapproval']}
put('source-detail.json',source)
put('sourcecontract.json',{'actor':source['actor'],'status':'PREREAD_CLOSED_TYPED_OBSTRUCTION','source_first':'PrimaryW2/FIRST/actualrho source beforedeliberateAPIretrieval; sourcecontract records thischronology, notfreshblindcertificate','inputs':'input-bindings.json exactrawLF plusbinarybookhash; pinning scripts available','exposure':'search-audit.md records currentregistry32/41/42metadata and prior41decoder-binding/32earlybody exposure; no43 forbiddenmaterials','named_source_API_facts':'source-detail.json reusable declarations;conditionalConsumers explicitly distinguished','inference_vs_source':'Target/rank0Hilbert extension/static7steps/smaller43+31consumer areprospective authoredwork;sourcepaperbookfacts separatelyanchored','leases':'actualleaseJSON writtenCLOSEDlast, initialrawpreserved','bibliographic_web_lookup':'OttoVillani DOI pagefound, no mathematicaltheoremtext used;onlypinnedprimary/Chewi supportscontracts','source_gap':'NeitherT2norregularity/flow certificate may become publicpremise ofsourcefaithfulGaussianleaf','no_approval':True})
bindings=read('input-bindings.json');checks=[]
for i in bindings['inputs']:
    if 'pdf_page_1_based' in i:
        stem=i['id'];raw=(D/(stem+'.raw.snapshot.txt')).read_bytes();lf=(D/(stem+'.lf.snapshot.txt')).read_bytes()
        assert sha(raw)==i['extracted_text_raw_sha256'];assert sha(lf)==i['extracted_text_lf_sha256']
    else:
        raw=(D/(i['id']+'.raw.snapshot')).read_bytes();lf=(D/(i['id']+'.lf.snapshot')).read_bytes()
        assert sha(raw)==i['raw_sha256'];assert sha(lf)==i['lf_sha256']
    checks.append({'id':i['id'],'raw_LF_consistent':raw.replace(b'\r\n',b'\n')==lf})
put('input-validation.json',{'status':'PASS','checks':checks,'book_pdf_sha256':sha((D/'chewi-pinned.raw.snapshot.pdf').read_bytes()),'not_compiler_or_theorem_validation':True})
lease.update(state='CLOSED',closed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_close_last_filesystem_operation=True)
closed=data(lease)
put('leases.closed.json',{'status':'ALL_REAL_LEASES_CLOSED','real_lease':'lease.json','initial_bytes':'lease.initial.raw.snapshot.json','method':'FinalCLOSEDleasebytes hashedwhileOPEN; actualclosedwriteafterallreceiptwrites aslastfilesystemoperation'})
outs=[]
for p in sorted(D.iterdir()):
    if p.is_file() and p.name!='preread-run.json':
        b=closed if p.name=='lease.json' else p.read_bytes()
        outs.append({'path':p.name,'raw_sha256':sha(b),'lf_sha256':None if p.suffix=='.pdf' else sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)})
run={'actor':source['actor'],'stage':source['stage'],'status':'PREREAD_COMPLETE_TYPED_OBSTRUCTION_NO_PROOF_OR_ADMISSION','real_leases':'ALL_CLOSED','closed_at_utc':lease['closed_at_utc'],'source_detail_sha256':sha((D/'source-detail.json').read_bytes()),'sourcecontract_sha256':sha((D/'sourcecontract.json').read_bytes()),'exact_inputs':'input-bindings.json/input-validation.json','outputs':outs,'compiler':False,'proof_claim':False,'canonical_write':False,'graph_authored':False,'goal_created':False,'independent_source_review43_consumer_not_verified_by_this_actor':True}
rb=data(run);(D/'preread-run.json').write_bytes(rb)
print('source-detail.json '+run['source_detail_sha256'])
print('sourcecontract.json '+run['sourcecontract_sha256'])
print('preread-run.json '+sha(rb))
lp.write_bytes(closed)
