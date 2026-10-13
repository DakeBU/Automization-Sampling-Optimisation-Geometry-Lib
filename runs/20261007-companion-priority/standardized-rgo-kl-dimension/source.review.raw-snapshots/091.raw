# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,re,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).resolve().parent
P=Path('runs/20261007-companion-priority/standardized-rgo-kl-dimension-preread45')
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def put(n,o):(D/n).write_bytes(dump(o))
def text(n):return (D/n).read_text(encoding='utf-8-sig')
inputs=[]
def pin(id,p,extra=None):
    b=Path(p).read_bytes();lf=b.replace(b'\r\n',b'\n')
    (D/(id+'.raw.snapshot')).write_bytes(b);(D/(id+'.lf.snapshot')).write_bytes(lf)
    item={'id':id,'source_path':str(p),'raw_sha256':sha(b),'lf_sha256':sha(lf),'raw_bytes':len(b),'lf_bytes':len(lf),'local_lines':len(lf.decode('utf-8-sig').splitlines())}
    if extra:item.update(extra)
    inputs.append(item);return item
pre=json.loads((P/'input-bindings.json').read_text(encoding='utf-8-sig'))
pri=pre['inputs'][0]
pin('primary',P/'primary.raw.snapshot.html',{'physical_ranges':pri['selected_physical_ranges'],'frozen_whole_primary_raw_sha256':pri['whole_raw_sha256'],'raw_matches_frozen':sha((P/'primary.raw.snapshot.html').read_bytes())==pri['raw_sha256']})
pin('preread-detail',P/'source-detail.json',{'role':'historical source-before-seal preread, not currentapproval'})
put('source-before-sealed-graph.contract.json',{'actor':'gaussian_noncompact_preread_42','historical_preread_detail_sha256':'e86fb1a54ca2a086736b29c9d7f1026ca9b5bb234bf455c53b0f5109f174c789','historical_preread_run_sha256':'4acf5f8c90d1c75bae0816ad759bd28b6ae8761cc0371b2642198075a78ec23b','primary_first_record':'preread45/primary-before-parent-interfaces.contract.json remainsCLOSEDimmutable','exposure':'historical43sourcegraph/prereadroles and prior41metadata/32earlybody disclosure retained; notfreshblind','actual_lease':'lease.json OPEN beforeallcurrentreads/writes/Python; sourcegraphnotimplementation'})
parents=json.loads(text('preread-detail.lf.snapshot'))['parents']
for sid in ['031public','043public']:
    old=next(i for i in pre['inputs'] if i['id']==sid)
    item=pin(sid,P/(sid+'.raw.snapshot.txt'),{'actual_provider':old['path'],'original_physical_start':old['original_physical_start'],'original_physical_end':old['original_physical_end'],'selection':'publicheaderonly before :=by; body opaque'})
    assert item['lf_sha256']==old['lf_sha256']
    # Current exact signature extraction only; no proofbody exposed/copied.
    allraw=Path(old['path']).read_bytes();start=allraw.index(('theorem '+old['name']).encode());end=allraw.index(b':= by',start)
    hdr=allraw[start:end].rstrip()+b'\r\n' if b'\r\n' in allraw else allraw[start:end].rstrip()+b'\n'
    assert hdr==(D/(sid+'.raw.snapshot')).read_bytes(),sid
    item['current_public_raw_bytes_identical']=True
    item['current_whole_file_hash_only']=sha(allraw)
    namespaces=[{'physical_line':allraw[:start].decode('utf-8-sig').splitlines().index(l)+1,'literal':l} for l in allraw[:start].decode('utf-8-sig').splitlines() if l.startswith('namespace ')]
    item['namespace_only_resolution']=namespaces
seal=pin('45seal','runs/20261007-companion-priority/standardized-rgo-kl-dimension-preproof45/statement-seals.accepted.json',{'role':'StatementSealmetadata only; implementation forbidden'})
sealed=json.loads(text('45seal.lf.snapshot'))
st=sealed['signatures'][0]['signature_text'];b=st.encode('utf-8');assert len(b)==1357 and sha(b)=='6b54ac62b436aeb4032aafb15b12c26a5661450013151633e01da02dd08b163d'
assert b==(P/'prospective-minimal-target.txt').read_bytes().replace(b'\r\n',b'\n')
(D/'45signature.lf.snapshot').write_bytes(b);(D/'45signature.raw.snapshot').write_bytes(b)
inputs.append({'id':'45signature','source_path':'embeddedexactsignature in45StatementSeal','raw_sha256':sha(b),'lf_sha256':sha(b),'raw_bytes':len(b),'lf_bytes':len(b),'local_lines':len(st.splitlines()),'original_root_candidate_raw_sha256':sealed['signatures'][0]['signature_raw_sha256'],'raw_boundary':'embeddedJSONdecoded signatureLF;rootoriginalcandidate rawhash recordedseparately, not silently equated'})
for sid,n in [('authored-route','authored-route.md'),('primitives','mathematical-primitives.txt')]:pin(sid,D/n,{'role':'authored independent mathematical source reconstruction; not Leanproof/API'})
put('source-inputs.json',{'inputs':inputs,'current_parent_status':'45seal namesactual31+43VERIFIED19b569ae; opaqueproducerinterfaces, noownimplementationverification','original_preread_status':'historical43PROVED_LOCAL remainsfrozen; currentseal administrativepromotionrecordedseparately','body_expansion_boundary':'No31/43proof selected; no45implementation exists/read/written; nocompiler/sharedleaseuse'})
nodes=[];edges=[];rows=[];inventory=[]
def node(id,kind,claim,**kw):nodes.append(dict(id=id,kind=kind,claim=claim,**kw))
def edge(a,b,source,line,why,kind='planned-mathematical-use'):
    id='edge:%03d'%(len(edges)+1);site={'source':source,'lines':line}
    edges.append(dict(id=id,prerequisite=a,consumer=b,caller=site,reason=why,kind=kind))
    inventory.append(dict(id='caller:%03d'%(len(inventory)+1),edge=id,caller=site,callee=a,kind=kind,observed_Lean_call=False))
def cov(src,l,n=None,why=None,original=None):rows.append(dict(source=src,local_line=l,original_physical_line=original,classification='NODE' if n else 'EXCLUDED',node=n,reason=why))
def span(src,a,b,n,why=None):
    original=next(i.get('original_physical_start') for i in inputs if i['id']==src)
    for l in range(a,b+1):cov(src,l,n,why,original+l-1 if original else None)
root='paper:2609.06906v1:'
for id,claim,lines in [
 ('standing','C² normalizedV,kappa^-1I<=Hessian<=I,beta1',[606,609]),('prox','positiveeta proximalminimizer',[612,618]),('RGO','actualrestrictedGaussian density',[627,632]),('KL','canonicalKLdensityorientation/+inftywithoutAC',[657,660]),('stationarity','sourcegradientV(p)=(y-p)/eta',[1289,1290]),('rho-law','negativelinear-cross rho,actualaffine standardizedRGO',[1295,1300]),('FIRSTcontext','W2/Fisher/moment wholechain;contextonly,no45W2claim',[1306,1308]),('LSI-invocation','FIRST invokesGaussianLSI/Talagrand; canonicalhalfFisher public43opaque',[1310,1311]),('numeric-Fisher-source','gradientrhozero/Lipschitz eta,momentIBP d; numericI<=eta²d public31opaque',[1312,1314])]:node(root+id,'CONTEXT_ONLY' if id=='FIRSTcontext' else 'PRIMARY_SOURCE',claim,original_physical_lines=lines)
node('boundary:T2','EXTERNAL_UNEXPANDED_NOT45_PREREQUISITE','Source Talagrand invocation; actual44analyticblocker retained, not supplied to45')
node('boundary:GaussianLSI','OPAQUE_SOURCE_PARENT_BOUNDARY','Source-invokedLSI already incorporated inverified43; no42/43proofexpansion')
edge('boundary:T2',root+'FIRSTcontext','primary',[1310,1311],'Namedsourceinvocation contextual branch;not45requirement','source-prose-named-use')
edge('boundary:GaussianLSI',root+'FIRSTcontext','primary',[1310,1311],'NamedGaussianLSIsourceinvocation;45usesopaque43only','source-prose-named-use')
pmap={606:'standing',607:'standing',608:'standing',609:'standing',612:'prox',613:'prox',618:'prox',620:'prox',627:'RGO',632:'RGO',652:'KL',657:'KL',660:'KL',1289:'stationarity',1290:'stationarity',1295:'rho-law',1298:'rho-law',1299:'rho-law',1300:'rho-law',1301:'FIRSTcontext',1306:'FIRSTcontext',1308:'FIRSTcontext',1310:'LSI-invocation',1311:'LSI-invocation',1312:'numeric-Fisher-source',1313:'numeric-Fisher-source',1314:'numeric-Fisher-source'}
k=0
for a,b in pri['selected_physical_ranges']:
    for physical in range(a,b+1):
        k+=1;tag=pmap.get(physical);cov('primary',k,root+tag if tag else None,None if tag else ('W2couplingsemanticbranchseparate' if physical==661 else 'HTMLstructure/spacing without mathematicalingredient'),physical)
for sid,p in zip(['031public','043public'],parents):node('parent:'+sid,'OPAQUE_VERIFIED_PRODUCER_INTERFACE',p['declaration'],qualified_identifier=p['declaration'],proof_selected=False,status_basis='accepted45seal reportsactual31+43VERIFIED19b569ae;notcreatorproofverification')
for id,kind,claim in [
 ('binder:inputs','EXACT_INPUT_CONTRACT','Identical31/43/45carrier,C2/Hessian/kappa,measurableS/eta/y,eta>0'),
 ('defs:literal','LITERAL_DEFINITION_CONTRACT','rho,Q for31,mu,R,r andgamma; witness-dependent rho/Q/r, truegradient/integrals;mu/R/gammaindependent'),
 ('slot31:stationarity','PRODUCED_OUTPUT','measurablep31,stationarity'),('slot31:numericFisher','PRODUCED_OUTPUT','actualgradientrho squared integral underactualr <=eta²*realfinrank'),
 ('slot31:domains-context','CONTEXT_OUTPUT_NOT_REPROVED','actualprobability/positionL2/norm²integrable/momentbound/gradientrhoL2; availableparentoutputs,no45publicpremises'),
 ('slot43:witness','PRODUCED_OUTPUT','measurableunique stationaryp43'),('slot43:domains','PRODUCED_OUTPUT','actualrprobability,ACgamma,canonicalKL!=top,actualgradientrhoL2'),('slot43:halfFisher','PRODUCED_OUTPUT','actualcanonicalKL.toReal<=half*actualrho-gradient energy forsamestandardizedr'),
 ('gap:standalone45','SOURCE_GAP','PaperdoesnotseparatelyprintcanonicalKLnumeric45; standaloneleaf andtwoexistentialwitnessjoininternallyauthored, noextrasourcepremise'),
 ('target:45','SEALED_TARGET','exact1357canonicalKLnumeric outputwithmeasurableuniqueprox/prob/AC/finiteKL/rhogradL2'),
 ('typing:extensions','AUTHORED_SOURCE_EXTENSION','Unitfixedparameters;measurablefamilies/finiteHilbert/rank0;allpositiveunboundedeta inherited;no extraEpositivity'),
 ('boundary:remaining','SCOPE_ONLY','NoT2/W2/FIRSTfullchain/bias/main/querycost/PURIFIEDcompletion')]:node(id,kind,claim)
map31={1:'parent:031public',**{l:'binder:inputs' for l in range(2,10)},10:'slot31:stationarity',11:'slot31:stationarity',**{l:'defs:literal' for l in range(12,18)},**{l:'slot31:domains-context' for l in range(26,31)},33:'slot31:numericFisher',34:'slot31:numericFisher'}
map43={1:'parent:043public',**{l:'binder:inputs' for l in range(2,10)},10:'slot43:witness',11:'slot43:witness',12:'slot43:witness',**{l:'defs:literal' for l in range(13,19)},19:'slot43:domains',20:'slot43:domains',21:'slot43:domains',22:'slot43:halfFisher',23:'slot43:halfFisher'}
for l in range(1,35):span('031public',l,l,map31.get(l),'Unusedintermediatecurvature/gradientzero/firstmomentFisherclausesalreadyopaqueproduceroutputs; finalnumericclauseused' if l not in map31 else None)
for l in range(1,24):span('043public',l,l,map43[l])
for l in range(1,24):span('45signature',l,l,'binder:inputs' if 2<=l<=9 else ('defs:literal' if 13<=l<=18 else 'target:45'))
for sid,slot,slot_range in [('031public','slot31:stationarity',[10,11]),('031public','slot31:numericFisher',[33,34]),('031public','slot31:domains-context',[26,30]),('043public','slot43:witness',[10,12]),('043public','slot43:domains',[19,21]),('043public','slot43:halfFisher',[22,23])]:edge('parent:'+sid,slot,sid,slot_range,'Exactpublicoutputclause;generatedprojectionisnot mathematicalcall','public-contract-projection')
for i,l in enumerate(text('primitives.lf.snapshot').splitlines(),1):
    m=re.match(r'P(\d\d) ',l)
    if m:node('primitive:P'+m[1],'FOUNDATIONAL_MATHEMATICAL_CONTRACT' if i<7 else 'FOUNDATION_SCOPE',l,Lean_API_claim=False);cov('primitives',i,'primitive:P'+m[1])
steps={}
for i,l in enumerate(text('authored-route.lf.snapshot').splitlines(),1):
    m=re.match(r'R(\d\d) ',l)
    if m:
        id='obligation:R'+m[1];steps[m[1]]=(id,i);node(id,'INTERNAL_MATHEMATICAL_OBLIGATION' if int(m[1])<8 else 'SCOPE_CONTRACT',l,compiled=False);cov('authored-route',i,id)
    else:cov('authored-route',i,None,'heading/spacing')
def use(a,n,why):id,l=steps[n];edge(a,id,'authored-route',[l,l],why)
for a,n,why in [
 ('parent:031public','01','Callactual31producer'),('parent:043public','01','Callactual43producer'),('binder:inputs','01','Exactlysharedsourceandtypinginputs'),
 ('obligation:R01','02','Bothactualfamiliesobtained'),('slot31:stationarity','02','Antecedentfor43uniqueatz=p31'),('slot43:witness','02','Uniqueconclusionp31s=p43s'),('primitive:P01','02','Functionextensionality'),
 ('obligation:R02','03','Actualfamilyequality'),('defs:literal','03','Allp-dependentdefs includingaffinepushforward'),('primitive:P02','03','Equalitysubstitution'),
 ('slot43:witness','04','Retainmeasurableunique stationarywitness'),('slot43:domains','04','Retainactualoutputdomains'),
 ('obligation:R03','05','Coherenttruegradient/law/integral'),('slot31:numericFisher','05','31finalactualFisherbound'),('slot43:halfFisher','05','43actualcanonicalhalfFisherbound'),
 ('obligation:R05','06','Tworealnumericinequalities'),('primitive:P03','06','Multiply31boundbynonnegativehalf'),('primitive:P04','06','Transitivity'),('primitive:P05','06','ExactRHSarithmeticeveryreal includingzero'),('primitive:P06','06','SameNat-toReal dimensioncast'),
 ('obligation:R04','07','Alltargetwitness/domainoutputs'),('obligation:R06','07','ActualKLnumericconclusion'),('typing:extensions','07','Rank0/family/allpositiveeta boundary'),
 ('gap:standalone45','08','Explicit sourceomission/internalextension'),(root+'FIRSTcontext','08','Restpaperchainnotproved'),('boundary:remaining','08','Remainingtruthboundary')]:use(a,n,why)
id,l=steps['07'];edge(id,'target:45','authored-route',[l,l],'Routeintendedtoestablishexactsealedtarget;notcompiledclaim','intended-conclusion')
for a,b in [(root+'standing','binder:inputs'),(root+'prox','defs:literal'),(root+'RGO','defs:literal'),(root+'KL','slot43:halfFisher'),(root+'stationarity','slot31:stationarity'),(root+'rho-law','defs:literal'),(root+'LSI-invocation','slot43:halfFisher'),(root+'numeric-Fisher-source','slot31:numericFisher')]:edge(a,b,'primary',next(n['original_physical_lines'] for n in nodes if n['id']==a),'Exactsourcecorrespondence;notcompileddependencyedge','source-correspondence')
for item in inputs:
    if item['id'] in ['preread-detail','45seal']:
        for l in range(1,item['local_lines']+1):cov(item['id'],l,None,'Metadata/provenance/admission only; notmathematicalsourceingredient')
put('sourcegraph.json',{'schema':'bounded-independent-sourcegraph45-v1','schema_contract':{'direction':'prerequisite->consumer','edges':'plannedmathematicaluses,publiccontractprojections,sourcecorrespondence,sourceprosenameduses,intendedconclusion clearlydistinct','parentproofs':'publicinterfacesopaque; no31momentor43LSIproofexpansion','primitive_boundary':'explicitmathematicalfoundations,not inventedLeanQNames/compiledcalls','source_extension':'sourcegap plusauthoredfamily/rank0/internalwitnessjoin; noextra publicpremises','OR':'One sufficient AND join; no genuinelydifferent45route needingOR claimed','approval':'Creatorcannotadmittopology;noneawarded'},'nodes':nodes,'edges':edges,'OR_nodes':[]})
put('source-coverage.json',{'unit':'Everyselectedphysicalprimaryline mappedto localexcerptline plusoriginal line;publiccontractlines andmathematicalprimitives/authoredroute exhaustive;metadata EXCLUDED','rows':rows,'mixed_semantic_exclusions':{'primary:657':'W2definitionhalf is contextualoutside45canonicalKLleaf','primary:1306':'WholeW2/Fisher/momentchain contextual only; numericalFisher correspondence useslasttwobounds, noW2conclusion','primary:1310-1311':'T2sourceinvocation outside45prerequisites;GaussianLSIconsumer expandedonlyopaque43'},'proof_boundary':'terminal :=by suffix andallparentbodies excluded; noimplementationinventory'})
put('caller-inventory.json',{'kind':'plannedindependent mathematicalsourceuses, notobserved45Leancalls','line_basis':'Primary callers useoriginalHTMLphysical lines; publicparent/authoredroute callers usepinnedexcerptlocal lines, withoriginalparentoffsets in source-inputs/coverage','records':inventory,'public_signature_token_classes':{'mathematicalobjects':['actualgradient/fderiv','literalvolume.tilted andMeasure.map','literalstdGaussian','canonicalInformationTheory.klDiv','realnorm²energyintegral','Module.finrank Nat->Real cast'],'typing_or_generated_not_calls':['carrierinstances','existentialwitnesses','measurability/conjunctionfields','letbindings','conjunctionprojections','attributes/structurefields'],'expansion':'Allinsideopaquecompiledproducercontract boundary; notseparatelyinventedproofingredients'}})
put('sourcecontract.json',{'actor':'gaussian_noncompact_preread_42','status':'INDEPENDENT_GRAPH_AUTHORED_AWAIT_DISTINCT_TOPOLOGY_REVIEW','source_before_graph':'source-before-sealed-graph.contract.json bindsclosedfrozenpreread before45seal','exact45_LF_sha256':sha(st.encode('utf-8')),'parents':'31/43actualpublicheaders rawLFidenticaltoclosedpreread; acceptedsealnamesalreadyVERIFIED19b569ae;proofopaque','route':'choose43p;43unique+31stationary+funext;transportallrho/Q/r;retain43actualdomains;31numericFisher+43canonicalhalfFisher;halfscaling/transitivity/fieldarith/cast','binder_classes':'sourceC2/Hessian/kappa/positiveeta;typing/familyextensions;allbound/coherence/domainoutputs internalderivedingredients notnewinputs','domain_boundaries':'actualprob/AC/finiteKL/rhogradL2 retained;31positiondomains contextavailable; canonicalllrnotdifferentiated;no totalizedinfiniteKLtoRealshortcut','zero_rank_eta':'allpositiveeta unbounded;rank0 andzeroenergy;noNontrivial/dimpositive/additionalsteprestriction','source_gap':'standalonecanonicalKLnumeric45 omittedfrompaper;actualLSI/Fisherchain andopaqueparents justifyinternalauthoredjoin;not fullFIRST','exposure':'Prior41metadata/decoderbinding originaltext and32earlybody exposure retained;prior43graphcreator and45preread;current45seal metadata and31/43publicheaders only. No43body/lesson/review/decoder or45implementation/Tests','no_compiler_claim_sharedwrites':True,'no_topology_self_admission':True,'root_site_compiler_lease':'KnownOPEN perroot;neverused ormodified','remaining':['distincttopologyreview','rootproof andindependent exactcompiler/blind/sourceimplementationreview','44GaussianT2/W2/restFIRST/main/querycost/PURIFIED']})
ids={n['id'] for n in nodes};errors=[]
if len(rows)!=len({(r['source'],r['local_line']) for r in rows}):errors.append('duplicatecoverage')
for item in inputs:
    wanted=set(range(1,item['local_lines']+1));actual={r['local_line'] for r in rows if r['source']==item['id']}
    if wanted!=actual:errors.append('coverage:'+item['id'])
for e in edges:
    if e['prerequisite'] not in ids or e['consumer'] not in ids:errors.append('danglingedge')
if any(r['node'] not in ids for r in rows if r['classification']=='NODE'):errors.append('danglingcoverage')
adj={n:[] for n in ids}
for e in edges:adj[e['prerequisite']].append(e['consumer'])
seen=set();active=set()
def visit(n):
    if n in active:errors.append('cycle:'+n);return
    if n in seen:return
    active.add(n)
    for x in adj[n]:visit(x)
    active.remove(n);seen.add(n)
for n in ids:visit(n)
put('structural-check.json',{'status':'PASS' if not errors else 'FAIL','errors':errors,'nodes':len(nodes),'edges':len(edges),'caller_records':len(inventory),'planned_named_math_uses':sum(r['kind'] in ['planned-mathematical-use','source-prose-named-use'] for r in inventory),'physical_rows':len(rows),'NODE_rows':sum(r['classification']=='NODE' for r in rows),'EXCLUDED_rows':sum(r['classification']=='EXCLUDED' for r in rows),'claim':'Bookkeepingconsistencyonly;notselftopologyvalidation,theoremadmission orcompileevidence'})
assert not errors,errors
