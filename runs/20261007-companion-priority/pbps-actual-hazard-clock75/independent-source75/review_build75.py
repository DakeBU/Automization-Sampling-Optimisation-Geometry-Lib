import collections, copy, hashlib, json, os, re, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-actual-hazard-clock75/independent-source75'
RUN=ROOT/'runs/20261007-companion-priority/pbps-actual-hazard-clock75'
BASE=ROOT/'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75'
ACTOR='/root/independent_source75'
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean'
PUB=ROOT/'website/content/publications/pbps-actual-hazard-clock.json'
LESSON=ROOT/'website/content/declaration_lessons/pbps-actual-hazard-clock.json'
PACKET=RUN/'source-review.packet.json'
MAP=RUN/'implementation-source-map75.json'
FROZEN=RUN/'source-review.freeze75.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def rel(p):return p.relative_to(ROOT).as_posix()
def ref(p):
    b=p.read_bytes();return {'path':rel(p),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))}
def put(name,obj):
    p=OWN/name;p.write_bytes((json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8'));return ref(p)
def body(a,b,lines):
    data=b''.join(lines[a-1:b]);return {'path':rel(MODULE),'start_line':a,'end_line':b,'source_raw_sha256':sha(MODULE.read_bytes()),'exact_code_raw_sha256':sha(data)}

def main():
    assert not (OWN/'lease.final.json').exists()
    before=read(OWN/'source-only.freeze75.json')
    assert before['phase']=='SOURCE_ONLY_BEFORE_CURRENT_LEAN' and before['current_module_or_packet_read'] is False
    packet=read(PACKET);frozen=read(FROZEN);graph=read(BASE/'source-proof-graph75.json');inventory=read(BASE/'source-coverage-inventory75.json');formula=read(BASE/'exact-source-formulas75.json')
    module=MODULE.read_bytes();lines=module.splitlines(keepends=True);mtext=module.decode('utf-8')
    assert len(lines)==396 and len(module)==21771 and sha(module)=='fd93d01583eec206285573c1f1631b94739f95471c50e1ff940e66080238e23d'
    assert sha(canon({k:v for k,v in packet.items() if k!='packet_sha256'}))==packet['packet_sha256']
    assert packet['anti_anchoring']=={'prior_semantic_slots_included':False,'prior_deltas_included':False,'prior_verdict_included':False,'prior_repairs_included':False}
    assert packet['roles']['formalizer']!=ACTOR and packet['roles']['blind_decoder']!=ACTOR
    assert packet['blind_reconstruction']['source_text_visible'] is False
    assert sha(packet['source']['original_text'].encode())==packet['source']['text_sha256']
    assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']
    assert sha(packet['blind_reconstruction']['text'].encode())==packet['blind_reconstruction']['text_sha256']
    assert packet['candidate_publication_context']['current_lean_module']==mtext
    for p in (PACKET,MODULE,PUB,LESSON,MAP):
        expected=next(r for r in frozen['inputs'] if Path(r['path'])==p)
        assert ref(p)['RAW_sha256']==expected['RAW_sha256'] and ref(p)['RAW_bytes']==expected['RAW_bytes']
    pub=read(PUB)['items'][0];lesson=read(LESSON)['units'][0];impl=read(MAP)
    assert packet['candidate_publication_context']['lesson']=={k:lesson[k] for k in packet['candidate_publication_context']['lesson']}
    assert pub['statement']==lesson['statement']==packet['candidate_publication_context']['statement']
    assert len(lesson['steps'])==9
    for step in lesson['steps']:
        r=step['lean_source_region'];data=b''.join(lines[r['start_line']-1:r['end_line']])
        assert sha(data)==r['exact_code_raw_sha256'] and data.decode()==step['lean']
        assert r['source_raw_sha256']==sha(module)
    assert len(impl['nodes'])==32 and len(graph['nodes'])==32 and len(graph['edges'])==67
    for row,n in zip(impl['nodes'],graph['nodes']):
        assert row['source_node']==n['id'] and row['source_kind']==n['kind'] and row['meaning']==n['meaning']
        for region in row['BODY_regions']:
            assert sha(b''.join(lines[region['start_line']-1:region['end_line']]))==region['exact_code_raw_sha256']
    raw=PRIMARY.read_bytes()
    assert sha(raw)==before['source_primary']['RAW_sha256']
    for item in inventory['items']:
        a,b=item['RAW_range'];assert sha(raw[a:b])==item['RAW_sha256']
    manifest=read(ROOT/'lake-manifest.json')
    assert next(p for p in manifest['packages'] if p['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
    assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
    assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',mtext)

    inputs=[('primary-full',PRIMARY),('source-graph',BASE/'source-proof-graph75.json'),('source-inventory',BASE/'source-coverage-inventory75.json'),('baseline-stageA',BASE/'stageA.freeze75.json'),('exact-source-formulas',BASE/'exact-source-formulas75.json'),('official-anti-anchored-packet',PACKET),('current-module',MODULE),('publication',PUB),('declaration-lesson',LESSON),('implementation-source-map',MAP),('current-freeze',FROZEN),('actual-flow-parent',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'),('actual-rate-parent',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean'),('hittingAfter-API',ROOT/'.lake/packages/mathlib/Mathlib/Probability/Process/HittingTime.lean'),('Exp1-API',ROOT/'.lake/packages/mathlib/Mathlib/Probability/Distributions/Exponential.lean'),('primitive-API',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean'),('closed-inf-API',ROOT/'.lake/packages/mathlib/Mathlib/Topology/Order/Monotone.lean'),('joint-Borel-API',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Order.lean'),('toolchain',ROOT/'lean-toolchain'),('dependency-manifest',ROOT/'lake-manifest.json'),('semantic-schema',ROOT/'tools/astis_semantic_roundtrip_core.py'),('semantic-fragment-adapter',ROOT/'tools/astis_semantic_roundtrip.py')]
    (OWN/'inputs').mkdir(exist_ok=True)
    inputrows=[]
    for i,(name,path) in enumerate(inputs):
        rawpath=OWN/'inputs'/('{:02d}.{}.RAW'.format(i,name));lfpath=OWN/'inputs'/('{:02d}.{}.LF'.format(i,name))
        data=path.read_bytes();rawpath.write_bytes(data);lfpath.write_bytes(data.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))
        inputrows.append({'name':name,'origin':ref(path),'RAW_snapshot':ref(rawpath),'LF_snapshot':ref(lfpath)})
    inputref=put('source.0.input-manifest.json',{'schema':'pbps75-source-review-finite-input-manifest/v1','actor':ACTOR,'counts':{'finite_inputs':len(inputs)},'source_only_phase_precedes_current_candidate':before,'inputs':inputrows,'anti_anchoring_exception':{'exposed':True,'path':rel(PUB),'json_pointer':'/items/0/statement_seal/binder_audit','detail':'A terminal extraction of the required current publication metadata displayed historical header semantic slots, deltas and verdict after the independent source-only freeze and after the current module had already been assessed positively. No prior reviewer file, root.math75 adoption, mathematical-review verdict, or source-blind decoder verdict file was opened. Strict no-prior-header-exposure instruction was nonetheless violated. This is disclosed and not erased.'}})

    binder=[
      {'binder':'E and NormedAddCommGroup/InnerProductSpace/FiniteDimensional/MeasurableSpace/BorelSpace','classification':'TYPING','source':'S1.p1.1, S1.p1.m2; finite Euclidean phase space with Borel sets','audit':'Exactly five structure classes. Compatible norm/inner product and BorelSpace are carrier structure, not theorem-shaped providers. Dimension zero remains permitted.'},
      {'binder':'V:E→R; alpha,beta:NNReal; eta:R','classification':'TYPING','source':'S1.p1.1, S1.E1, S2.SS2.p1.1','audit':'Potential and scalar parameters. NNReal constants encode their source nonnegativity; alpha positivity is still explicit.'},
      {'binder':'hα:0<(α:R)','classification':'STANDING','source':'S1.p1.m4','audit':'Original strict positive strong-convexity parameter.'},
      {'binder':'hαβ:α≤β','classification':'STANDING','source':'S1.p1.m4','audit':'Original ordering, including equality.'},
      {'binder':'hV:ContDiff R 2 V','classification':'STANDING','source':'S1.p1.m3','audit':'Original C2 potential, no higher derivatives.'},
      {'binder':'hH:forall x v, alpha||v||²≤D²V(x)[v,v] and D²V(x)[v,v]≤beta||v||²','classification':'STANDING','source':'S1.E1.m1','audit':'Both bounds at every x,v, represented by twice Frechet derivative. No localization, Hessian variation bound, or gradient-Lipschitz provider.'},
      {'binder':'hη:0<η','classification':'STANDING','source':'S2.SS2.p1.m1','audit':'Exactly source positive step.'},
      {'binder':'hβη:(β:R)*η≤1','classification':'STANDING','source':'S2.SS2.p1.m1','audit':'Equivalent to eta≤1/beta under 0<alpha≤beta; equality allowed.'}
    ]
    definitions=[
      ('c',[25,25],'S3.E4.m1','y-eta gradV(xRef), actual center; scalar multiplication is the coordinate-free Euclidean product.'),
      ('Phi',[26,29],'A1.Ex2.m1/m2','Both position and momentum formulas agree for every real time. Negative sign and division by sqrt(eta) are unchanged; positive eta excludes singular source parameters.'),
      ('rate',[30,31],'A1.Ex1.m1; S3.E9.m1','sqrt(eta)*max(0,<p,gradV(x)-gradV(xRef)>), the literal positive part, with no refresh intensity or full-gradient substitute.'),
      ('H',[32,33],'A1.Ex4.m1','Weighted SUM ((eta^-1)||x-c||²+||p||²)/2, with exact half; not the product-space max norm.'),
      ('C',[34,36],'A1.Ex6.m1','Exact source cap at SAME H(z). All sqrt(eta), beta, sqrt(2H), sqrt(2etaH), norm(c-xRef) factors retained; C is independent of e,t.'),
      ('Lambda',[37,38],'A1.E1.m2; A1.Ex7.m1','Real Lebesgue interval integral of the actual orbit rate; endpoint NNReal means the orientation is nonnegative. Finite-interval integrability is proved internally.'),
      ('tau',[39,43],'A1.E1.m2; A1.SS1.p2.2','hittingAfter unfolds to the infimum of {u>=0:Lambda(u)>=e}, in WithTop NNReal; its no-hit branch is precisely source infinity. This is a literal infimum, not a choose-with-zero fallback or a discrete stopping theorem.'),
      ('W',[44,46],'A1.SS1.p2.1 and (A.1), one-marginal elaboration','Actual expMeasure(1) pushforward by e↦tau(toNNReal e). toNNReal is max(e,0) on R. Direct all-real preimage equality and exact CDF show this is the intended Exp1 threshold law. Map normalization/measurability are proved, not assumed.')
    ]
    definition_audit=[{'definition':n,'definition_kind':'literal','signature_lines':r,'source_anchor':a,'semantic_check':s,'result':'PASS','complete_body_in_module_snapshot':True} for n,r,a,s in definitions]

    slots={
      'objects':{'original':'Source (3.4), Ex1/2/4/6, (A.1) use the fixed actual center, gradient residual, harmonic orbit, bounce rate, weighted energy, energy cap and integrated first threshold crossing. E_(n+1) has Exp(1) marginal.','reconstructed':'The independent decoder reconstructs exactly eight lets c,Phi,rate,H,C,Lambda,tau,W and the same fixed rate-one real exponential pushforward.','relation':'explicit-elaboration','evidence':'Raw primary reread independently before candidate: S3.E4; A1.Ex1/2/4/6; A1.E1. Current lines25–46/202–223 agree term by term. hittingAfter definition at fixed Mathlib lines65–68 includes the source empty-set infinity branch. No arbitrary hazard/cap/law/provider appears.'},
      'domains':{'original':'Source state R^d, arbitrary fixed y,xRef and initial phase; flow in real time, waits on nonnegative continuous time with infinity; unit exponential threshold.','reconstructed':'Finite real inner-product Borel E (rank zero allowed), phase E×E, times and deterministic thresholds NNReal, waits WithTop NNReal; W is a measure on extended waiting time.','relation':'explicit-elaboration','evidence':'Finite real Hilbert representation is isometric Euclidean typing. NNReal is the complete nonnegative continuous order, not N; WithTop supplies the source no-hit infinity. Original raw source allows arbitrary fixed phase and does not impose positive energy/nonzero residual. e=0 is a harmless extension to the null Exp1 endpoint and is handled exactly.'},
      'quantifiers':{'original':'Standing assumptions precede all fixed y,xRef and initial phase. (A.1) depends on the current fixed phase and threshold; energy majorant is independent of time and threshold.','reconstructed':'Six outer analytic hypotheses; all y,xRef,z and finite nonnegative t/e universally quantified within ten conjunctions. Finite-tau/C>0/e>0 are local implications only.','relation':'equivalent','evidence':'Fully expanded private statement lines16–72 and public binders193–201 match packet and decoder. No regularity, integrability, probability, survival, nonexplosion, finite-wait or iid premise is an outer binder. C>0 only controls division in group10; finite-tau guard only controls untopA in group6.'},
      'assumptions':{'original':'C2 V, 0<alpha≤beta, global two-sided Hessian quadratic bounds, eta>0 and eta≤1/beta, on finite Euclidean/Borel state.','reconstructed':'hα,hαβ,hV,hH,hη,hβη with five ordinary typing classes; private helper repeats these exact same six.','relation':'equivalent','evidence':'S1.p1.1/S1.E1/S2.SS2.p1.1 reread from pinned primary. beta positivity follows from alpha>0 and alpha≤beta, so beta*eta≤1 is the source step bound. Rate/flow continuity and exact cap are internally obtained from actual73/74 lines136–147; actual74 derives Lipschitz gradient internally at r=0. EXCESS=0 and RULED=0.'},
      'conclusion':{'original':'One selected (A.1) first-clock definition, no-hit branch, exact actual integrated cap and finite waiting lower bound. Continuous-infimum, joint-Borel and probability details are omitted bridges to be supplied for this bounded edge.','reconstructed':'Ten groups: joint continuous/Borel Lambda; finite-interval integrability; zero/nonnegative/monotone; exact tau sublevels; infinity/finite equality/positive/e0; joint Borel tau; normalized actual W and strict survival; exact integrated C cap; extended wait bound and C0/e>0 infinity.','relation':'explicit-elaboration','evidence':'Thirteen internal bridge nodes remain source-only topology; the current body now discharges/internalizes them for the selected one-clock edge. Continuous closed-infimum proof269–287, IVT292–315, e0/positive316–326, joint Borel327–341, actual Exp1 law342–368, wait369–393 inspected. N21 uses direct preimage/CDF route, not a separate support lemma; N24 only legal specializations. No recursion/global process conclusion is inferred.'},
      'scopes':{'original':'(A.1) clock is an ingredient before (A.2); source later uses iid clocks/SLLN for nonaccumulation and memorylessness for Markov property. Reversal/invariance/costs are later claims.','reconstructed':'Only one fixed actual segment and its extended waiting-time law. Measure.real is the real-valued probability of strict Ioi(t), which includes infinity. untopA occurs only under a finite-hit guard.','relation':'explicit-elaboration','evidence':'Map measurability and probability normalization are separately proved. all-real event {t<tau(max(e,0))}={Lambda(t)<e} uses Lambda(t)>=0 and is valid even for negative e. Unit-CDF complement evaluates the exact event, with no loss of infinity mass. Nodes25–30 remain open/excluded. No joint clock continuity, finite-wait a.s., memorylessness, kernel, expected-query, composition, PURIFIED/live/Goal claim.'},
      'constant_dependencies':{'original':'Rate sqrt(eta); H=(eta^-1||x-c||²+||p||²)/2; C=sqrt(eta) beta sqrt(2H)(sqrt(2etaH)+||c-xRef||); Exp rate1; wait≥e/C for positive C.','reconstructed':'Same exact factors, initial H(z), unit rate, exp(-Lambda(t)), division under C>0; alpha appears only in hypotheses and C has no explicit dimension/time/threshold factor.','relation':'equivalent','evidence':'Raw Ex1/2/4/6/7/8 formula bytes checked; current lets25–46 agree. henergy lines143–147 supplies SAME starting energy to actual74 cap. Bound182–187 integrates that exact constant. WithTop handles infinite wait; toNNReal(e/C)=e/C because e≥0,C>0. No refresh or hidden multiplicative constant.'}
    }
    deltas=[
      {'id':'D75-domain','slot':'domains','severity':'informational','classification':'carrier-elaboration','blocking':False,'description':'Finite real Hilbert/Borel and NNReal/WithTop encode Euclidean nonnegative continuous time and infinity. e=0 is included although Exp1 has no endpoint mass.','evidence':'Raw source A1.E1 and no-hit paragraph; five typing classes and exact e0 conclusion.'},
      {'id':'D75-bridges','slot':'conclusion','severity':'informational','classification':'omitted-source-details-expanded','blocking':False,'description':'Ten groups explicitly supply the source omitted continuous-crossing, Borel and one-marginal law details; they are not numbered source theorems or full Proposition3.1.','evidence':'Frozen source graph N09–N24 and current BODY mappings.'},
      {'id':'D75-direct-law','slot':'scopes','severity':'informational','classification':'alternative-internal-route','blocking':False,'description':'N21 is discharged for this consumer by exact all-real survival preimage and nonnegative-endpoint CDF, rather than separately publishing support/zero-atom lemmas.','evidence':'Current lines353–368; mathematical equality holds for every real e. Standalone support and zero-atom declarations are not claimed.'},
      {'id':'D75-degenerate','slot':'conclusion','severity':'informational','classification':'legal-specialization-only','blocking':False,'description':'N24 rank0/H0 are legal specializations of exact formulas plus general C0/e0 branches, not additional separately published theorem claims.','evidence':'H=0 gives C=0 algebraically; rank0 gives H=0; lines323–326 and369–390 provide required general branches.'}
    ]
    node_reason={
      'N01':'All six original standing callers survive; ordinary five typing classes are not hidden providers.',
      'N02':'Actual center is a literal let and residual is inlined in rate, with no supplied reference law.',
      'N03':'Actual73 literal flow is reused through its theorem, not imported as an assumed arbitrary map.',
      'N04':'Actual74 rate continuity/nonnegativity used internally; no refresh term.',
      'N05':'Bounce identity is context only in this theorem; neither bounce continuity nor a path is claimed.',
      'N06':'Same actual weighted-sum energy is a literal expression in the theorem and C.',
      'N07':'Actual73 energy equality applies to each real-time harmonic orbit only.',
      'N08':'Actual74 same-energy-layer radii/cap applied to Phi_s(z) with actual energy equality.',
      'N09':'Joint orbit-rate continuity via composition of actual producers; nonnegativity from actual74.',
      'N10':'Local primitive theorem applies to real Lebesgue measure, internally continuous integrand; restriction to NNReal and finite interval integrability are correct.',
      'N11':'Empty integral, nonnegative integrand and nested-interval integral monotonicity are derived.',
      'N12':'Exact generic hittingAfter definition represents source infimum and empty-set top, with continuous index NNReal.',
      'N13':'Nonempty closed threshold set bounded below by0; IsClosed.csInf_mem, not WellFoundedLT, supplies attained infimum.',
      'N14':'Infimum and monotonicity give no-hit equivalence; IVT proves exact finite threshold. e0 and e>0 branches are explicit.',
      'N15':'Finite tau≤t iff e≤Lambda(t) follows from attained infimum and monotonicity; empty branch false both sides.',
      'N16':'All finite closed sublevels are Borel threshold inequalities; top sublevel univ, giving joint Borel without continuity claim.',
      'N17':'Same actual H at start is conserved by Phi, then actual74 cap is evaluated on Phi_s(z).',
      'N18':'Integrate derived C bound over every finite nonnegative interval, C nonnegative by exact displayed factors.',
      'N19':'Finite branch combines e=Lambda(tau)≤C tau and C>0; top branch automatic. C0 and positive e yield no hit.',
      'N20':'Actual expMeasure(1), not an input probability/survival provider; probability property from pinned API.',
      'N21':'Alternative route internalizes carrier transport at the exact consumer: all-real strict-preimage identity and CDF at Lambda≥0. Retired separate-support route gains no standalone declaration credit.',
      'N22':'Literal measurable pushforward on extended waiting time, probability normalization proved from actual Exp1.',
      'N23':'Strict Ioi(t) includes top; complement-CDF argument yields exact exp(-Lambda) and includes infinite-wait mass.',
      'N24':'Legal rank0/H0 specialization of exact C plus C0/e0 branches; no positive dimension/energy exclusion or separate theorem claim.',
      'N25':'OPEN: actual random postjump state substitution and production are not proved by universally quantified deterministic start.',
      'N26':'OPEN: equation(A.2), measurable recursive event/path construction and initial draws not produced.',
      'N27':'OPEN: stochastic path global energy propagation across arbitrarily many bounces not produced.',
      'N28':'OPEN: iid exponential sequence, moments/SLLN, nonaccumulation and unique full process not produced.',
      'N29':'OPEN: global Markov memorylessness and time-homogeneity not produced.',
      'N30':'EXCLUDED: reversal/invariance/semigroup/terminal/main/cost remain separate; Davis attribution is not an inspected theorem.',
      'N31':'Actual74 internally produces Lipschitz gradient from C2/Hessian at r=0, then rate continuity/cap. No gradient-Lipschitz caller.',
      'N32':'Algorithm initial Gaussian/reference draws are context, not ongoing refresh; literal hazard has none.'
    }
    nodes=[]
    for n,m in zip(graph['nodes'],impl['nodes']):
        status='OPEN_DOWNSTREAM' if n['id'] in ['N25','N26','N27','N28','N29'] else ('EXCLUDED_CONTEXT' if n['id']=='N30' else ('CONTEXT_ONLY' if n['id'] in ['N05','N32'] else 'SATISFIED_FOR_SELECTED_EDGE'))
        nodes.append({'source_node':copy.deepcopy(n),'implementation_mapping':copy.deepcopy(m),'review_status':status,'independent_reason':node_reason[n['id']],'source_topology_unchanged':True,'not_Lean_implication':True})
    items=[]
    for item in inventory['items']:
        items.append({'source_item':copy.deepcopy(item),'independent_disposition':item['classification'],'disposition_unchanged':True,'RAW_range_digest_rechecked':True,'independent_reason':('Excluded with the recorded explicit scope reason; no claim or Lean coverage is gained. '+item['reason']) if item['classification']=='EXCLUDED' else ('Source content retained within the bounded selection; mixed paragraphs preserve their future fragments as open. '+ ' '.join(node_reason[n] for n in item['nodes'])),'node_review_ids':item['nodes']})
    edges=[]
    for e in graph['edges']:
        edges.append({'source_edge':copy.deepcopy(e),'consumer_use_anchor_preserved':True,'producer_and_consumer_preserved':True,'review_status':'OPEN_SOURCE_TOPOLOGY' if int(e['consumer'][1:]) in range(25,31) else 'RETAINED_SOURCE_TOPOLOGY','not_Lean_implication':True,'reason':'This recorded prerequisite is source-topological only. Selected local consumer realization is reviewed in node mapping; open recursive/global consumers remain open.'})
    groups=[
      ('G01','Joint Lambda continuity',[151,161],'Actual q joint continuous; locally finite Lebesgue parametric primitive, then NNReal endpoint restriction.'),
      ('G02','Joint Lambda Borel',[188,189],'Continuous Lambda gives measurable on product Borel carriers.'),
      ('G03','Finite-interval integrability',[162,169],'Fixed-state actual orbit rate is continuous for all real s and interval integrable; no integrability premise.'),
      ('G04','Lambda zero/nonnegative/monotone',[170,181],'Nonnegative rate, t>=0 and nested interval monotonicity; equality at0.'),
      ('G05','Exact crossing sublevel',[269,287],'Closed nonempty set contains csInf, monotonicity; explicit no-hit branch.'),
      ('G06','Infinity/finite equality/positive/e0',[288,326],'No-hit iff all finite Lambda<e. IVT forbids overshoot. e>0 cannot hit0; e0 hits0.'),
      ('G07','Joint tau Borel',[327,341],'Closed finite sublevels from exact event equivalence, top sublevel univ.'),
      ('G08','Actual normalized W and strict survival',[342,368],'Measurable map of actual Exp1; exact all-real event equality; nonnegative endpoint CDF complement; top remains in Ioi.'),
      ('G09','Nonnegative original-energy C/integrated cap',[136,189],'Same H(z) from actual73 conserved orbit plus actual74 cap. C independent of t/e. Integrate bound.'),
      ('G10','Extended lower waiting bound and zero cap',[369,393],'C>0 local implication, finite/top split; C0 with e>0 has no hit. No finite-wait claim.')
    ]
    debt=[{'id':'META75-historical-comment','blocking':False,'location':'ActualHazardClock.lean:8–9','description':'Retained historical prospective statement-only comment no longer describes the implemented theorem body. It is cosmetic provenance debt, not a mathematical premise or semantic repair.'},{'id':'META75-prospective-coverage','blocking':False,'location':'publication source_proof_coverage and purification text','description':'Coverage still says13 internal bridges OPEN and implementation pending. The supplied current exhaustive source review and admission fields may replace that prospective coverage during serialized integration; full publication/PURIFIED remains open.'}]
    exposure={'classification':'PROCESS_ANTI_ANCHORING_EXPOSURE','blocking_for_strict_source_admission':True,'description':'Required publication snapshot contains historical header-review content inside statement_seal.binder_audit. A metadata extraction displayed those prior semantic slots/deltas/verdict after this reviewer completed source-first freeze and positively assessed the current proof. No claim of zero prior-header exposure can be made. A fresh source reviewer must satisfy the strict instruction before canonical acceptance.','not_a_mathematical_delta':True}
    review={
      'schema':'pbps75-exhaustive-independent-source-review/v1','reviewer':ACTOR,'parent_commit':'526a6af98cf0380032a3aed52da01c5304de3bb8','source_only_freeze':ref(OWN/'source-only.freeze75.json'),'input_manifest':inputref,'official_packet':{'RAW':ref(PACKET),'canonical_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256']},'source_graph':ref(BASE/'source-proof-graph75.json'),'source_inventory':ref(BASE/'source-coverage-inventory75.json'),'current_module':ref(MODULE),'current_publication':ref(PUB),'current_lesson':ref(LESSON),'current_implementation_source_map':ref(MAP),'counts':{'source_nodes':32,'source_edges':67,'source_items':137,'NODE':77,'EXCLUDED':60,'internal_bridges':13,'exact_source_formulas':23,'literal_definitions':8,'analytic_callers':6,'conclusion_groups':10,'formula_BODY_blocks':9,'semantic_slots':7,'mathematical_blocking_deltas':0,'repairs':0},'binder_audit':{'entries':binder,'EXCESS':0,'RULED':0,'six_analytic_callers_unchanged':True,'private_helper_requires_same_six_only':True,'expanded_public_statement':packet['lean']['statement']},'definition_audit':definition_audit,'semantic_slots':slots,'deltas':deltas,'mathematical_verdict':'equivalent-after-elaboration','repairs':[],'source_nodes':nodes,'source_edges':edges,'source_items':items,'conclusion_groups':[{'id':i,'name':n,'BODY_region':body(a,b,lines),'independent_reason':why,'result':'PASS'} for i,n,(a,b),why in groups],'formula_BODY_blocks':[{'index':i+1,'title':s['title'],'text':s['text'],'formula':s['formula'],'lean_source_region':s['lean_source_region'],'exact_contiguous_code_matches':True,'prose_and_formula_match_current_code':True} for i,s in enumerate(lesson['steps'])],'internal_route_notes':{'N21':'Direct all-real survival-preimage/CDF route replaces a separate support/zero-atom-provider route for this consumer. No separately published support or zero-atom theorem claimed.','N24':'Rank0/H0 are legal specializations only; general C0/e>0 and e0 laws are implemented. No new claim of a separately compiled specialization.'},'metadata_debt':debt,'anti_anchoring':{'official_packet_omits_prior_results':True,'source_first_freeze_completed_before_current_Lean':True,'independent_from_formalizer':True,'independent_from_decoder':True,'independent_from_mathematical_reviewer':True,'exposure':exposure},'source_admission_ready':False,'truth_boundary':before['expectations']['outside_scope'],'full_paper':False,'VERIFIED':False,'PURIFIED':False,'Goal_complete':False,'compiler_or_other_reviewer_verdict_used_for_source_acceptance':False}
    review['status']='SUPPLEMENTAL_SOURCE_REVIEW_NOT_ANTI_ANCHORED'
    review['fresh_anti_anchored_reviewer_required']=True
    reviewref=put('source.0.review.json',review)
    state={'actual_PID':os.getpid(),'actor':ACTOR,'official_packet_sha256':packet['packet_sha256'],'official_packet_RAW':ref(PACKET),'publication_binding_sha256':packet['publication_binding_sha256'],'source_text_sha256':packet['source']['text_sha256'],'statement_sha256':packet['lean']['statement_sha256'],'reconstruction_sha256':packet['blind_reconstruction']['text_sha256'],'input_manifest':inputref,'review':reviewref,'mathematical_verdict':'equivalent-after-elaboration','semantic_slots':slots,'deltas':deltas,'repairs':[],'metadata_debt':debt,'exposure':exposure,'counts':review['counts'],'truth_boundary':review['truth_boundary'],'declaration':packet['lean']['declaration'],'source_graph':ref(BASE/'source-proof-graph75.json'),'source_inventory':ref(BASE/'source-coverage-inventory75.json'),'module':ref(MODULE),'lesson':ref(LESSON),'publication':ref(PUB),'source_admission_ready':False,'successful_structural_checks':['primary RAW/source range checks','official canonical packet and RAW freeze checks','whole module and frozen lesson/source-map checks','nine exact contiguous formula BODY blocks','137 item/32 node/67 edge classification preservation','eight definitions/six callers/ten groups/seven slots','fixed toolchain/dependency pin','textual fake closure scan'],'process_failures':[{'type':'ENV_BLOCKED','scope':'source-first helper execution only','detail':'Python3.8 Path.write_text lacks newline keyword; switched to write_bytes. No mathematical consequence.'},{'type':'ENV_BLOCKED','scope':'source-first terminal rendering only','detail':'Default gbk stdout could not render NBSP; configured UTF8 and reran successfully. No mathematical consequence.'}]}
    put('build-state75.json',state)
    print(json.dumps({'status':'EXHAUSTIVE_REVIEW_WRITTEN_WITH_STRICT_ADMISSION_OBSTRUCTION','actual_PID':os.getpid(),'mathematical_verdict':state['mathematical_verdict'],'review':reviewref,'counts':state['counts'],'obstruction':exposure['classification']},ensure_ascii=False))

if __name__=='__main__':main()
