from pathlib import Path
from html.parser import HTMLParser
import json, hashlib, re, os, sys, datetime, time
BASE=Path('E:/Samplinglib'); OUT=BASE/'runs/20261007-companion-priority/pbps-macro-range-sourcegraph58'; ROOT=OUT.parent
PRIMARY=ROOT/'phase-pbps-gamma-preread57'; reads=[]; writes=[]; started=time.time()
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p,b):
    lf=b.replace(b'\r\n',b'\n'); return dict(path=str(p).replace('\\','/'),bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def read(p):
    b=Path(p).read_bytes(); reads.append(pin(Path(p),b)); return b
def load(p): return json.loads(read(p).decode('utf-8-sig'))
def write(name,obj):
    p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(obj,dict):
        obj=dict(obj); obj['content_self_sha256']=sha(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
        b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    elif isinstance(obj,str): b=obj.encode()
    else: b=obj
    p.write_bytes(b); receipt=pin(p,b); writes.append(receipt); return receipt
def snapshots(p,label):
    b=read(p); return dict(actual_input=pin(Path(p),b),exactraw_snapshot=write('inputs/'+label+'.exactraw.snapshot',b),crlf_to_lf_snapshot=write('inputs/'+label+'.crlf-to-lf.snapshot',b.replace(b'\r\n',b'\n')))

class Spans(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=False); self.text=text; self.starts=[0]; self.stack=[]; self.regions=[]
        for m in re.finditer('\n',text): self.starts.append(m.end())
    def pos(self):
        row,col=self.getpos(); return self.starts[row-1]+col
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); ident=a.get('id'); cls=a.get('class',''); at=self.pos(); types=[]
        if tag=='p' and 'ltx_p' in cls: types.append('proof-paragraph')
        if 'ltx_equation' in cls and 'ltx_equationgroup' not in cls: types.append('equation/display')
        if 'ltx_theorem' in cls: types.append('theorem/definition')
        if 'ltx_proof' in cls: types.append('proof-container')
        if tag=='cite': types.append('external-citation')
        if tag=='math': types.append('math-formula')
        if tag in ['meta','link','br','hr','img','input','wbr']: return
        self.stack.append(dict(tag=tag,start=at,ident=ident,attrs=a,types=types,ancestors=[q['ident'] for q in self.stack if q['ident']]))
    def handle_endtag(self,tag):
        at=self.pos(); end=self.text.find('>',at)+1
        for n in range(len(self.stack)-1,-1,-1):
            if self.stack[n]['tag']==tag:
                closed=self.stack[n:]; self.stack=self.stack[:n]
                for item in closed:
                    if item['types']:
                        item['end']=end; self.regions.append(item)
                return

def assign(r,file):
    ancestors=r['ancestors']+[r['ident'] or '']; joined=' '.join(ancestors)
    if file.startswith('A2.SS1'):
        if any(x.startswith('A2.SS1.p4') or x in ['A2.E6','A2.E7','A2.Ex4','A2.Ex5'] for x in ancestors): return 'EXCLUDED',[], 'B6/B7 half-turn/Markov mixing blocks are later source regions; no58 theorem closure.'
        if r['types']==['external-citation']: return 'EXCLUDED',[], 'Hypocoercivity citations14/21 supply terminology here, not a spectral-root theorem or a58 proof prerequisite.'
        if 'A2.E1' in joined or 'A2.SS1.p1.3' in joined: return 'NODE',['S:P'],'Literal conditional resampling/expectation operator.'
        if 'A2.E2' in joined or 'A2.SS1.p1.4' in joined or 'A2.SS1.p1.5' in joined: return 'NODE',['S:M-onto','S:centered-onto'],'Macro range identification and orthogonal decomposition; reverse inclusion/background adapters must be discharged.'
        if 'A2.E3' in joined or 'A2.SS1.p2' in joined: return 'NODE',['S:blocks'],'Block source/target convention retained.'
        if 'A2.E4' in joined or 'A2.SS1.p3' in joined: return 'NODE',['S:U','S:blocks','S:block-defect'],'Actual reflection selfadjoint/unitary; block-square identities. Second B5 identity remains reused background, not a newly admitted58 result.'
        if 'A2.Ex1' in joined or 'A2.Ex2' in joined or 'A2.SS1.p1.2' in joined: return 'EXCLUDED',[], 'Algorithm transition kernel and full observable dynamics are later lanes; P branch is covered separately.'
        return 'NODE',['S:model','S:real-L2','S:P'],'Actual law and operator framework/background vocabulary; no full algorithm claim.'
    if file.startswith('A3.SS1'):
        if any(x.startswith('A3.SS1.p8') or x.startswith('A3.SS1.p9') or x.startswith('A3.Thmtheorem1') for x in ancestors): return 'EXCLUDED',[], 'LemmaC1/C8-C9 alternate derivative/IBP/cutoff/covariance/H1 approximation feeds later halfturn; outside58 and source weakH1 still OPEN.'
        if any(x.startswith('A3.SS1.p5') for x in ancestors): return 'EXCLUDED',[], 'C5-C7 uniform A>=-I/2 route uses Gaussian PI/difference estimate and spectral calculus; distinct from C4/squared gap, OPEN.'
        if any(x.startswith('A3.SS1.p4.4') or x.startswith('A3.SS1.p4.5') or x.startswith('A3.SS1.p4.6') for x in ancestors) or any(x in ['A3.E5','A3.E6','A3.Ex9'] for x in ancestors): return 'EXCLUDED',[], 'C5-C6 preparation belongs to independent negative-one-half spectral lower-bound route, not needed by squared-gap58.'
        if any(x.startswith('A3.SS1.p6') for x in ancestors): return 'NODE',['S:squared-gap','S:Gamma-gap'],'Final B15 proof: squared predecessor58 is NODE; positive-root/Loewner unsquaring remains OPEN consumer, not58 proof closure.'
        if any(x.startswith('A3.SS1.p7') for x in ancestors): return 'EXCLUDED',[], 'Transition paragraph to alternate derivative formula/halfturn.'
        if any(x.startswith('A3.SS1.p4') for x in ancestors) or any(x in ['A3.E3','A3.E4','A3.Ex8'] for x in ancestors): return 'NODE',['S:centered-A','S:marginal-PI','S:scalar-C4','S:macro-C4'],'C3 centeredness/actual marginal PI, C4 rearrangement and selfadjoint spectral norm interpretation; accepted scalar57 stationarity route is recorded separately.'
        return 'NODE',['S:sharp-C2'],'C1/C2 inherited score covariance, conditional curvature/PI, conditional CS, variance integral and density/closed gradient. Integration58 does not re-prove these or close full weighted weakH1.'
    if file.startswith('A4.SS1'):
        if any(x.startswith('A4.SS1.p3') for x in ancestors): return 'EXCLUDED',[], 'D5 density/chi-square evolution is a later dynamics/mixing consumer, outside58.'
        if any(x.startswith('A4.Thmtheorem2') for x in ancestors): return 'NODE',['S:centered-A','S:T-same'],'D4 stationary Markov L2 contraction/adjoint constants conventions; centeredness needs preserved mean, not constants alone.'
        if any(x=='A4.SS1.p2.2' for x in ancestors): return 'NODE',['BG:positive-root'],'D1 bounded Borel spectral calculus, unique nonnegative root convention; source text explicit but actual real-L2 root remains OPEN.'
        if any(x.startswith('A4.SS1.p2') for x in ancestors): return 'NODE',['S:U','S:blocks','BG:positive-root'],'Adjoint/selfadjoint/unitary/Loewner conventions. Source positivity is not a constructed Lean root.'
        return 'NODE',['S:real-L2','S:M','S:centered-onto'],'D1-D2 real AE quotient, norm/inner product, closed subspace and centered-space conventions.'
    if file.startswith('A2.E10'): return 'NODE',['BG:positive-root'],'B10 explicit positive root source definition; OPEN actual construction.'
    if file.startswith('A2.E11'): return 'NODE',['S:Gamma-norm'],'B11 later norm-root identification after actual root; OPEN.'
    if file.startswith('A2.E15'): return 'NODE',['S:Gamma-gap'],'B15 later positive-root gap;58 proves squared predecessor only.'
    if file.startswith('A2.E16'): return 'NODE',['S:inverse-polar'],'B16 inverse only centered macro; isometry into micro, no onto; OPEN.'
    raise ValueError(file)

source_seal=load(OUT/'source-first-seal.json'); graph=load(OUT/'source-proof-graph.json'); regions=[]; source_inputs=[]
for name in ['A2.SS1.raw.html','A3.SS1.raw.html','A4.SS1.raw.html','A2.E10.raw.html','A2.E11.raw.html','A2.E15.raw.html','A2.E16.raw.html']:
    source_inputs.append(snapshots(PRIMARY/name,name)); data=read(PRIMARY/name); text=data.decode(); parser=Spans(text); parser.feed(text)
    for number,r in enumerate(sorted(parser.regions,key=lambda x:(x['start'],x['end']))):
        status,ids,reason=assign(r,name); raw=text[r['start']:r['end']].encode()
        regions.append(dict(region_id=r['ident'] or name+':anonymous:'+str(number),source_file=name,source_span_byte_start=len(text[:r['start']].encode()),source_span_byte_end=len(text[:r['end']].encode()),source_span_raw_sha256=sha(raw),kind=r['types'],ancestors=r['ancestors'],formula=r['attrs'].get('alttext'),disposition=status,nodes=ids,reason=reason))
write('source-coverage.json',dict(schema_version=1,actor='/root/source_graph58',contract='Every p.ltx_p, ltx_equation including nested equation spans, theorem/proof,cite and math element in7 selected exact balanced source anchors has explicit disposition. Math formulas counted as spans, not independent theorem obligations.',regions=regions,counts=dict(total=len(regions),NODE=sum(x['disposition']=='NODE' for x in regions),EXCLUDED=sum(x['disposition']=='EXCLUDED' for x in regions)),creator_independent_review=False))

# Inherited606 is copied exactly as source inventory only. No prior theorem verdict or implementation determines58 graph topology.
old=ROOT/'pbps-marginal-poincare-sourcegraph57'
original=load(old/'source-only-freeze.json'); supplement=load(old/'coverage.citation-supplement.json')
write('inherited57.source-only-freeze.exactraw.snapshot.json',read(old/'source-only-freeze.json'))
write('inherited57.coverage.citation-supplement.exactraw.snapshot.json',read(old/'coverage.citation-supplement.json'))
write('inherited-source606-inventory.json',dict(source_freeze_pin=pin(old/'source-only-freeze.json',read(old/'source-only-freeze.json')),citation_supplement_pin=pin(old/'coverage.citation-supplement.json',read(old/'coverage.citation-supplement.json')),coverage=original['coverage'],citation_coverage=supplement['coverage'],semantic_scope='Inventory and source provenance only. Original exclusions and analytic gaps preserved exactly; not imported as58 compiled dependency/source-review authority.',consumer_scope='Inherited standalone marginal PI supplies source anchors2.13/D6/D10 and analytic predecessors of C3; actual57 closed-gradient PI and actual56 T/K graph alignment are independent interfaces.',candidate58_exposure=False))

interface_inputs=[]; interface_records=[]
for rel in ['AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean']:
    p=BASE/rel; data=read(p); cut=data.index(b':= by'); header=data[:cut]
    interface_records.append(dict(module=rel,whole_module_receipt_only=pin(p,data),header=write(p.stem+'.public-header.exactraw.snapshot.lean',header),header_lf=write(p.stem+'.public-header.crlf-to-lf.snapshot.lean',header.replace(b'\r\n',b'\n')),production_body_read=False))
test=BASE/'Tests/GaussianMarginalPoincare.lean'; interface_inputs.append(snapshots(test,'actual57-Test'))
inventory=load(ROOT/'phase-pbps-next-primary58/reuse.inventory.json')
write('public-interface-audit.json',dict(source_first_seal=pin(OUT/'source-first-seal.json',read(OUT/'source-first-seal.json')),interfaces=interface_records,actual57_test=pin(test,read(test)),actual57_test_body_read=True,production_bodies_read=False,candidate58_body_or_claim_read=False,actual57_centering_route='Test constructs actual reflected conditional joint Lambda=J.map(y,2x-y), Lambda.fst=Lambda.snd=nu; actual55 S disintegrates Lambda; AEmean/Tu integrability and pushforward integral derive mean preservation. This is a separately reviewed source-compatible stationarity route, not evidence that constants alone preserve centeredness.',same_operators='Actual55 T and actual56/57 T identified by identical literal AE conditional-mean action and actual same S; G same by exact smooth-compact graph iff. Equality is a derived edge, not a caller premise.',source_printed_route='C3 uses actual A selfadjoint plus A1=1, derivable from55 P/U/M. Keep this as OR route from actual-stationarity centering, not conjoin both. Source58 may expose selfadjoint T and T1 as conclusions.',reuse_inventory=inventory['inventory'],strict_mathlib_proof_body_blindness=False,incidental_mathlib_exposure='Header-targeted tool slices included existing FactorsThrough factorsThrough proof lines and final snippets of memLp/compMeasurePreserving definitions; explicitly disclosed, no58 implementation exists.'))

binders=[
dict(name='E;NormedAddCommGroup;InnerProductSpace REAL;FiniteDimensional;MeasurableSpace;BorelSpace',classification='TYPING/RULED',expansion='Finite real Hilbert and compatible Borel carrier generalizes printed R^d inclrank0; CompleteSpace E derived internally. L2(J) is complete potentially infinite real Hilbert; no finiteDimensional L2 or nontrivial centered subspace.'),
dict(name='V;alpha,beta:NNReal;eta:REAL',classification='SOURCE/TYPING',expansion='Real potential and numeric source parameters; alpha,beta nonnegative typing while0<alpha comes from explicit hAlpha.'),
dict(name='hAlpha;hAlphaBeta',classification='SOURCE',expansion='0<alpha and alpha<=beta, hence positive beta; all original bounds retained.'),
dict(name='hV',classification='SOURCE',expansion='ContDiff REAL2 V; no third/fourth derivative, analytic, Lipschitz-Hessian or added smoothness.'),
dict(name='hH.lower',classification='SOURCE',expansion='For all x,v: alpha||v||^2 <= HessV(x)[v,v]; global lower curvature, not an input posterior/marginal certificate.'),
dict(name='hH.upper',classification='SOURCE',expansion='For all x,v: HessV(x)[v,v] <= beta||v||^2; global upper curvature, no supplied conditional covariance.'),
dict(name='hEta;hBetaEta',classification='SOURCE',expansion='eta>0,beta eta<=1; derive0<alpha eta<=1 and denominator1+alpha eta>0 internally. Endpoint alpha eta=1 retained.'),
dict(name='mu;J;nu;Lambda;P;A;B',classification='DEFINED_ACTUAL_INPUTS',expansion='Literal same normalized tilted-volume target, independent Gaussian augmentation, snd marginal, actual reflection, real conditional projection comap snd and exact compressions. Probability/normalization/measurability/disintegration are conclusions from parents, never public law premises.'),
dict(name='M;T;isometry;intertwining;range;mean;centeredness',classification='DERIVED_OUTPUTS/PROOF_EDGES',expansion='One canonical uniform real snd pullback and bounded scalar reflected conditional mean before every u/f. Reverse macro range and centered onto/mean identities are outputs. No caller range/isometry/root/spectral/centering certificate.'),
dict(name='u:actualL2(nu);f:actualL2(J)',classification='CONCLUSION_DOMAIN',expansion='All rough scalar inputs or all true macrocentered f with Pf=f and meanJf=0. Macro operator bounded on entire centered closed subspace; no caller membership in gradient domain.'),
dict(name='Pf=f;meanJf=0',classification='CONCLUSION_RESTRICTION',expansion='Source H_P,0 membership for universal conclusion, equivalent actual closed centered macro subspace; not a theorem-level certificate of some chosen external operator.'),
]
write('binder-and-definition-audit.json',dict(status='SOURCE_BINDER_TEMPLATE_PENDING_EXACT58_SIGNATURE_INDEX',binders=binders,EXCESS=[],definition_audit=[dict(object='mu,J,nu,Lambda,F,P,A,B',kind='literal',requirement='Same actual inputs; source expressions/public55 literal definitions.'),dict(object='Lp classes/M',kind='quotient/representative',requirement='AEJ action and comap strongly-measurable representative; DoobDynkin factor and pushforward MemLp produce reverse range. Arbitrary representative equality every y is forbidden.'),dict(object='macroH_P and macroH_P0',kind='literal closed-subspace',requirement='ran actual P and intersection ker actual mean; closedness/onto produced.'),dict(object='T/M uniform choices',kind='characterized-after-existence',requirement='Existing actual55/56 producers provide existence; canonical AE action identifies choices, no fallback/default body or caller agreement.'),dict(object='Gamma',kind='unconstructed source-positive-root',requirement='Remain OPEN; cannot redefine as weighted Laplacian resolvent or generic scalar sqrt/certificate.')],proof_ingredients=[dict(node=n['id'],source_anchor=n['anchor'],input_policy='Dependency edge internally discharged; never added source-facing binder',status=n['status']) for n in graph['nodes'] if n['id'] not in ['S:model','S:real-L2']],quantifier_order='Original source assumptions -> one actual uniform M/T (and actual G/K from parents) -> all u/f; centered membership only restricts quantified conclusions.',source_hypothesis_equals_binder=True,proof_ingredient_equals_edge=True))

write('typed-missing-bridges.json',dict(bridges=[dict(id='reverse-range-adapter',classification='mathlib-available/local-integration',residual='Produce true lpMeas AE comap representative; real DoobDynkin factor; actual pushforward MemLp; identify same canonical M. Existing API availability is not a proof of integration.',public_premise_allowed=False),dict(id='same-T-and-G',classification='local-integration',residual='AE literalconditionalmean uniquely identifies55/56/57 T; exact graph iff identifies57/56 coreG before closure; uniform choices preserved.',public_premise_allowed=False),dict(id='actual-centered-macro-transport',classification='internal-paper-step',residual='Mean pullback plus reverse range => every macrocentered f has centered u; normisometry/intertwining consume same57C4.',public_premise_allowed=False),dict(id='positive-root-real-L2',classification='source-contract-gap/local-background',residual='Bounded unique positive Gamma on true real complete possibly infinite H_P; generic CFCsqrt requires unestablished class adapter. Source D1 supplies convention, not Lean construction.',public_premise_allowed=False),dict(id='full-weighted-weakH1',classification='source-contract-gap',residual='Accepted compact-gradient closure must still be identified with separately defined source weakH1;58 does not consume or close this equality.',public_premise_allowed=False)],retired_routes=['Inferring ranM=ranP solely from isometric embedding','Treating constant-preservation alone as mean-preservation','Replacing whole joint P-Afull² by I-Afull² off macro range','Caller supplied range/domain/centering/root certificate','Finite-dimensional L2 or excluding rank0/alphaeta1','Bundling unconstructed Gamma/root/inverse in squared-gap58'],failure_class='NONE',formal_obstruction=False,salvage='Source-only bounded reduction; no failed Lean theorem or rejected mathematics.'))

write('negative-path-observation.json',dict(kind='read-only-observability',attempts=['sourcegraph57/source-coverage.json','sourcegraph57/source-proof-graph.json','sourcegraph57/capsule.md','preproof57/topology-original.accepted-with-consumer-blockers.json'],result='Get-Content path-not-found; directory57 existed, requested file names/folder prefix were wrong. Correct existing inventory source-only-freeze.json/coverage.citation-supplement.json/graph.packet.json under pbps-marginal-poincare-sourcegraph57.',mathematical_effect='NONE',observed_tool_exit_codes=[1,1],no_source_mutation=True))

write('capsule.md','''Source-first58: exact actual macro range, centered transport and squared defect gap

The bounded DAG is B1/B2 actual conditional expectation and snd-pullback -> reverse macro-range factorization -> centered onto map -> same MT=AM + actual57 centered contraction -> C4 on every true macrocentered f -> B5 defect -> 4 alpha eta/(1+alpha eta)^2 squared gap. Printed C3 selfadjoint+A1 centering and actual57 stationary-disintegration centering are separate sufficient OR routes.

The source hypotheses are exactly C2 V, both global Hessian bounds, 0<alpha<=beta, eta>0,beta eta<=1 in the disclosed finite-real-Hilbert/Borel extension. Real L2 may be infinite; rank0/alphaeta1 remain allowed. Probability, actual laws, canonical M/T, Lp transfer, range, mean, domain and centeredness certificates must be produced as dependency edges. No additional smoothness or caller certificate is permitted.

Source B2 omits representative/factorization/Lp bookkeeping. Fixed Mathlib real-target DoobDynkin, lpMeas comap AE representative and memLp_map_measure_iff supply exact background contracts. They must still be integrated on actual laws; library-name existence does not discharge the edge. Existing actual55 public interface, actual56 G/T/K interface, actual57 closed-gradient PI header and accepted57 actualTest were read only after the source graph seal. Production proof bodies and candidate58 bodies were not read.

The squared gap is a strict predecessor of B15. Full weakH1 equality, actual positive Gamma root, positive-root norm/Loewner gap, centered inverse and polar isometry, C5-C7 lower bound, halfturn/dynamics/main/cost/composition remain OPEN. Gamma has no eta prefactor and cannot be a gradient/Laplacian resolvent. Creator cannot validate this source graph; independent topology review and later exact58signature binder index remain pending.

All7 selected balanced anchors receive explicit source dispositions. Inherited596+10 source606 spans are retained exactly as source inventory with original exclusions; they are not new proof edges or new source-review admission. Compiler NOT_STARTED_CLOSED. No production/shared files, Git, website, Goal or detached ASTIS were changed.
''')
write('input-manifest.json',dict(actual_source_inputs=source_inputs,actual_test=interface_inputs,prior_source_seal=source_seal,reads=reads,prior_source_first_pin_validation=pin(OUT/'pin-validation.json',read(OUT/'pin-validation.json')),historical_control_policy='Use immutable53strict source58 bindings and full-row original/current historical control maps; do not demand obsolete live control paths frozen. Original OPENlease remains snapshot, current closed lease not retroactively substituted.',snapshots_policy='Own raw/CRLF-to-LF snapshots for primary source and Test; exact prior own input receipts retained. Whole production module bytes are hash receipts only; exported/read text is PUBLIC header.'))
write('finish-io.json',dict(actor='/root/source_graph58',python_pid=os.getpid(),python_executable=sys.executable,foreground=True,elapsed_seconds=time.time()-started,reads=reads,writes=writes,compiler='NOT_STARTED_CLOSED',claim='Bookkeeping/source reconstruction only; no self-validation.'))
print(json.dumps(dict(status='SOURCE_PACKET_PREPARED',coverage=len(regions),own_nodes=len(graph['nodes']),own_edges=len(graph['edges']),inherited_coverage_type=type(original['coverage']).__name__,finish_io=str(OUT/'finish-io.json'))))
