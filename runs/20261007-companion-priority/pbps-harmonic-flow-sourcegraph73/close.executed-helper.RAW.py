from pathlib import Path
import json,hashlib,os,sys,subprocess,datetime,importlib.util,re
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-sourcegraph73'
OLD=ROOT/'runs/20261007-companion-priority/pbps-half-turn-construction-preread73'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(j): return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def write(n,j):
    assert not (OWN/'lease.final.json').exists(),'CLOSED_LAST'
    (OWN/n).write_bytes(j if isinstance(j,bytes) else (json.dumps(j,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8'))
def read(p): return json.loads(p.read_text('utf-8'))
def pin(p):
    b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'lf_recipe':'CRLF byte pair -> LF only; preserve bare CR/every other byte'}
def compatible(row,now): return all(row[k]==now[k] for k in ['path','bytes','raw_sha256','lf_sha256'])
def parse():
    sp=importlib.util.spec_from_file_location('closed_source_parser73',OLD/'preread73.py'); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m.tree()
def text(n): return re.sub(r'\s+',' ',n.text()).strip()
def freeze():
    lease=read(OLD/'lease.final.json'); assert lease['state']=='CLOSED_LAST' and lease['owned_count_including_lease']==103
    for r in lease['all_files_except_self']: assert compatible(r,pin(ROOT/r['path'])),r['path']
    assert sha(canonical(lease['all_files_except_self']))==lease['closure_sha256']
    run=read(OLD/'run.json'); rh=run.pop('run_sha256'); assert sha(canonical(run))==rh
    assert compatible(run['complete_named_payload'],pin(ROOT/run['complete_named_payload']['path']))
    originals=read(OLD/'inputs.manifest.json')['inputs']; maps=[]
    for i,r in enumerate(originals):
        now=pin(ROOT/r['path']); assert compatible(r,now),r['path']
        maps.append({'index':i,'original_authority':pin(OLD/'inputs.manifest.json'),'original_input_reference':r,'current_input':now,'resolution':'EXACT_CURRENT_RAW_AND_CRLF_ONLY_LF_EQUALITY','historical_fallback':False})
    assert len(maps)==21
    names=['lease.final.json','run.json','complete-named-source-first-review.payload.json','inputs.manifest.json','selected-contract.json','source-expectations.json','source.regions.json','construction.formula-spans.json','api.regions.json','api.statement-regions.json','api.retrieval.json','preread73.py']
    inputs=[pin(OLD/n) for n in names]
    write('inputs.manifest.json',{'input_count':len(inputs),'inputs':inputs,'referenced_old_input_count':21,'old_input_version_map':'old21.version-map.json','no_recursive_package_or_source_snapshot_copy':True})
    write('old21.version-map.json',{'row_count':21,'rows':maps,'recipe':'finite exact current vs frozen RAW/LF check for EACH old input; no wildcard/exclusion or current-only fallback'})
    write('closed103.reference-validation.json',{'pid':os.getpid(),'source_scope':OLD.relative_to(ROOT).as_posix(),'state':'CLOSED_LAST','old_owned_count':103,'verified_native_nonself_rows':len(lease['all_files_except_self']),'closure_sha256':lease['closure_sha256'],'lease':pin(OLD/'lease.final.json'),'whole_logical_run_sha256':rh,'complete_named_payload':pin(OLD/'complete-named-source-first-review.payload.json'),'all_native_files_exact':True,'all21_old_inputs_exact_current':True,'old_native_byte_writes':0,'old_scope_has_complete_spg':False,'qualification':'CLOSED103 was planning only; this separate StageA completes the selected-edge source proof graph uncertainty.'})
    write('lease.open.json',{'state':'OPEN','actor':'/root/exact_science63','scope':OWN.relative_to(ROOT).as_posix(),'task':'independent source-first StageA73, selected actual_harmonic_flow_laws graph and binders only','owner_header_or_implementation_consumed':False,'proof_search':False,'compiler_run':False,'canonical_git_ledger_goal_writes':False})
    b,s,t=parse(); roots=read(OLD/'source.regions.json')['regions']; out=[]
    byid={n.a.get('id'):n for n in t.nodes if n.a.get('id')}
    def atoms(n):
        if n.tag=='math' or n.tag in ['p','table','figcaption','h6'] or 'ltx_listingline' in n.a.get('class',''): return [n]
        children=[c for c in n.children if not isinstance(c,str)]
        if not children: return [n] if text(n) else []
        return [v for c in children for v in atoms(c)]
    for region in roots:
        n=byid[region['source_id']]
        blocks=[]
        for k,a in enumerate(atoms(n)):
            if not text(a): continue
            lo=len(s[:a.start].encode('utf-8')); hi=len(s[:a.end].encode('utf-8')); q=b[lo:hi]
            blocks.append({'block_id':a.a.get('id') or region['source_id']+f'::block{k}','tag':a.tag,'raw_byte_start_inclusive':lo,'raw_byte_end_exclusive':hi,'literal_span_raw_sha256':sha(q),'bytes':len(q),'readview':text(a)})
        out.append({'source_id':region['source_id'],'whole_region_raw_sha256':region['literal_span_raw_sha256'],'raw_byte_start_inclusive':region['raw_byte_start_inclusive'],'raw_byte_end_exclusive':region['raw_byte_end_exclusive'],'blocks':blocks})
    write('source.blocks.json',{'source_primary':maps[0]['current_input'],'interval_recipe':'0-based RAW UTF8 bytes, inclusive start/exclusive end; block hashes are literal source bytes','region_count':len(out),'block_count':sum(len(x['blocks']) for x in out),'regions':out,'no_duplicate_source_snapshot_copy':'source bytes remain in fixed primary and CLOSED103 exact region snapshots; direct finite interval pins are sufficient'})
    for r in out:
        print('REGION',r['source_id'])
        for v in r['blocks']: print(v['block_id'],v['tag'],v['readview'])
    print(json.dumps({'pid':os.getpid(),'old_native_rows_verified':102,'old_inputs':21,'new_authority_inputs':len(inputs),'regions':len(out),'blocks':sum(len(x['blocks']) for x in out)}))

def graph():
    inventory=read(OWN/'source.blocks.json'); blocks={v['block_id']:v for r in inventory['regions'] for v in r['blocks']}
    nodes=[]
    def node(i,kind,claim,source,formula=None,scope='source printed'):
        row={'id':i,'kind':kind,'claim':claim,'source_block_ids':source,'source_provenance':scope,'compiled':False}
        if formula: row['formula']=formula
        nodes.append(row)
    node('STAND-C2','standing-source-assumption','V is C2 on the whole finite Euclidean carrier',['S1.p1.1'])
    node('STAND-MODULI','standing-source-assumption','0<α≤β; κ=β/α only contextual, not a new caller',['S1.p1.1','S1.E1'])
    node('STAND-HESSIAN','standing-source-assumption','αI≤D²V(x)≤βI for every x',['S1.E1'])
    node('STAND-STEP','standing-source-assumption','η∈(0,1/β], represented as η>0 and βη≤1 under β>0',['S2.SS2.p1.1'])
    node('PARAMETERS','source-quantifiers','Each y,xRef and initial x,p is arbitrary; fixed reference is kept constant on every deterministic arc',['alg1.l1','alg1.l3','alg1.l4','S3.Thmtheorem1.p1.1','A1.SS1.p1.1'])
    node('CENTER','literal-source-definition','Actual center uses the SAME queried gradient at xRef',['S3.E4.m1','alg1.l3'], 'c(y,xRef)=y−η•gradient V xRef')
    node('POSITION','reused-source-equation','The explicit position component is the source no-bounce harmonic trajectory',['S3.E6.m1'],'X_t=c+cos(t)•(x−c)+(sqrt(η)*sin(t))•p')
    node('PHASE-FLOW','literal-source-definition','Both components use the SAME center, η and initial phase point',['S4.E5.m1','A1.EGx1'],'Φ_t(x,p)=(c+cos(t)•(x−c)+(sqrt(η)*sin(t))•p, (−sin(t)/sqrt(η))•(x−c)+cos(t)•p)')
    node('ODE-X','source-equation','Position derivative has the exact source sqrtη coefficient',['alg1.l5'],'dX_t/dt=sqrt(η)•P_t')
    node('ODE-P','source-equation','Momentum derivative includes actual y and fixed queried reference gradient with the exact signs and reciprocal coefficient',['alg1.l5'],'dP_t/dt=−(sqrt(η))⁻¹•(X_t−y)−sqrt(η)•gradient V xRef')
    node('INIT','source-initial-condition','The actual arc starts from the given x,p; literal Φ0 must equal this same phase point',['alg1.l4','S4.E5.m1'],'Φ_0(x,p)=(x,p)','source initial condition; equality is an omitted formula check')
    node('GROUP','source-flow-interface','Restarting the same deterministic flow agrees with adding times; inverse is Φ_−t',['S4.E5.m1','A1.SS1.p1.2'],'Φ_(s+t) z=Φ_s(Φ_t z)','reconstructed explicit-flow consequence; all-real extension is not a quoted paper theorem')
    node('HALF-TURN','source-equation','At π the temporary momentum disappears from position and changes sign in momentum',['S3.E7.m1'],'Φ_π(x,p)=((2:ℝ)•c−x,−p)')
    node('ENERGY','literal-source-definition','Weighted sum of two squared E norms, not product max norm',['A1.SS1.p3.1','A1.Ex4'],'H(x,p)=(η⁻¹*‖x−c‖²+‖p‖²)/2')
    node('FLOW-ENERGY','source-proof-claim','The flow preserves this SAME shifted harmonic energy; this is only the flow half of the printed flow-and-bounce assertion',['A1.SS1.p3.2'],'H(Φ_t z)=H(z)')
    node('ENERGY-NONNEG','SOURCE_GAP','Nonnegative energy is required for its later square-root bounds; η>0 discharges the weights',['A1.Ex4','A1.Ex5'],'0≤H(z)','omitted background order check; future proof obligation, not a supplied binder')
    node('SCALE','SOURCE_GAP','Positive η permits reciprocal sqrtη and converts weighted position energy to normalized coordinate energy',['S4.E5.m1','A1.Ex4'],'r=sqrt(η)>0, r²=η; a=r⁻¹•(x−c); H=(‖a‖²+‖p‖²)/2','omitted scalar normalization bridge; future internal dependency')
    node('TRIG','SOURCE_GAP','Addition, zero/π evaluations and sin²+cos²=1 are background ingredients for the exact explicit-flow conclusions',['S3.E7.m1','S4.E5.m1','A1.SS1.p3.2'],'sin²t+cos²t=1; sinπ=0; cosπ=−1','Mathlib inspected APIs in CLOSED103; no new compile or theorem credit')
    node('NORM-CANCEL','SOURCE_GAP','The two squared E norm expansions cancel opposite mixed real inner terms',['A1.SS1.p3.2','A1.Ex4'],'‖cos(t)•a+sin(t)•p‖²+‖−sin(t)•a+cos(t)•p‖²=‖a‖²+‖p‖²','omitted Hilbert algebra bridge; future proof obligation, not a new public premise')
    node('DERIVATIVE','SOURCE_GAP','Differentiate the explicit two components and rewrite the fixed actual center to recover both Algorithm1 ODE coefficients',['alg1.l5','S4.E5.m1','A1.SS1.p1.2'],'c=y−η•gradient V xRef and η=(sqrtη)²','omitted derivative/center-conversion verification; no proof search or target proof here')
    node('GRAD-CONT','SOURCE_GAP','C2 implies continuity of the actual gradient; no gradient-continuity or Lipschitz caller is added',['S1.p1.1','S3.E4.m1'],'Continuous (gradient V)','omitted calculus bridge; future internal use, not formalized by this StageA')
    node('JOINT-CONT','SOURCE_GAP','For fixed η>0 the actual formula is jointly continuous in y,xRef,t,x,p, hence Borel',['S3.E4.m1','S4.E5.m1','A1.EGx1'],'Continuous ((y,xRef,t,x,p)↦Φ_t^(y,xRef)(x,p))','source-derived regularity strengthening for this interface; selected13 ranges do not print this full continuity theorem; follows by a future internal proof from C2/formula')
    node('SELECTED-ANCHOR','source-derived-target','One actual_harmonic_flow_laws interface, not whole Proposition3.1',['S3.E6.m1','S3.E7.m1','alg1.l5','S4.E5.m1','A1.Ex4','A1.SS1.p3.2'],'actual Φ, joint continuity, init/group/π, exact ODE, H nonnegative/invariant','selected source-derived bounded interface, unsealed/unproved; no 73 implementation/header inspected')
    N={n['id'] for n in nodes}; coverage=[]; excluded=[]
    def cover(block,claims):
        assert block in blocks,block
        dispositions=[]
        for j,(status,target,claim) in enumerate(claims):
            row={'semantic_subitem':j,'disposition':status,'claim':claim}
            if status=='NODE': assert target in N; row['node_id']=target
            else:
                assert status=='EXCLUDED'; xid=f'EX-{len(excluded):02d}'; row['excluded_id']=xid; row['reason']=target
                excluded.append({'id':xid,'source_block_id':block,'claim':claim,'reason':target,'future_math_credit':False})
            dispositions.append(row)
        coverage.append({'source_block_id':block,'literal_source_anchor':{k:blocks[block][k] for k in ['raw_byte_start_inclusive','raw_byte_end_exclusive','literal_span_raw_sha256','bytes']},'subitems':dispositions})
    C=lambda n,c:('NODE',n,c)
    X=lambda why,c:('EXCLUDED',why,c)
    cover('S1.p1.1',[C('PARAMETERS','finite Euclidean potential setting'),C('STAND-C2','V∈C2'),C('STAND-MODULI','0<α≤β'),X('Target measure normalization is already a separate library matter and not a selected deterministic-flow premise.','μ=Z⁻¹e⁻V dx probability sampling context')])
    cover('S1.E1',[C('STAND-HESSIAN','global lower/upper Hessians'),X('Condition number notation is contextual and not consumed by selected flow laws.','κ=β/α')])
    cover('S1.p1.2',[X('Navigation to whole-paper main result.','main-result introduction')])
    cover('S2.SS2.p1.1',[C('STAND-STEP','0<η≤1/β'),X('Historical proximal sampler citation [17] does not produce a dependency for explicit flow.','Lee/Shen/Tian augmentation attribution')])
    cover('S2.E6',[X('Actual augmentation is existing background, not new flow delta and not a supplied kernel/measure premise.','joint Gibbs law πη formula')])
    cover('S2.SS2.p1.2',[X('Gibbs transition construction excluded; existing conditional-law adapter is reused later.','original sampler Gibbs update context')])
    cover('S2.E7',[X('Gaussian augmentation law already exists, no new reference-law adapter or random initialization in selected deterministic leaf.','independent X,Z and Y=X+sqrtη Z')])
    cover('S2.SS2.p1.3',[X('Marginal laws and smoothed potential are not deterministic-flow dependencies.','X and Y marginals, Gaussian convolution, conditional notation')])
    cover('S2.E8',[X('Every-y posterior conditional kernel is existing library reuse; random sampling not selected.','Gaussian forward and quadratic-tilt backward conditional laws')])
    cover('S2.SS2.p1.4',[X('Iteration/query cost tradeoff, Gibbs updates and citations [6,9,15] remain outside bounded flow.','localization and sampler cost discussion')])
    cover('S2.E4.m1',[X('Future bounce uses exact R0=id and norm/involution; selected flow contains no reflection normal.','specular R_h and R0 convention')])
    cover('S3.E4.m1',[C('CENTER','actual c=y−η∇V(xRef)'),X('Residual h is future bounce/rate definition, not a flow hypothesis.','h(x)=∇V(x)−∇V(xRef)')])
    cover('S3.E6.m1',[C('POSITION','explicit no-bounce position formula')])
    cover('S3.E7.m1',[C('HALF-TURN','π endpoint (2c−x,−p)')])
    cover('alg1::block0',[X('Algorithm title is context; the whole algorithm is not being completed.','Algorithm1 title')])
    cover('alg1.l1',[C('PARAMETERS','arbitrary initial x,y')])
    cover('alg1.l2',[X('Reference sampling and independent Gaussian momentum are not needed to define/evaluate a deterministic phase arc; no process/clock law credit.','random xRef and p0 initialization')])
    cover('alg1.l3',[C('CENTER','same cached actual reference gradient'),X('One gradient query is operational context, not an expected-query-cost theorem.','query cost')])
    cover('alg1.l4',[C('INIT','set actual x0=x')])
    cover('alg1.l5',[C('ODE-X','exact dx coefficient'),C('ODE-P','exact dp signs and reference force'),C('HALF-TURN','fixed integration horizon π'),X('Jump-interrupted evolution is future process construction; selected arc law is deterministic only.','evolve while bounce process may occur')])
    cover('alg1.l6',[X('Actual residual event rate is future option2; not a supplied rate premise and not part of selected flow theorem.','λ=sqrtη[p·(∇Vx−∇VxRef)]positive')])
    cover('alg1.l7',[X('Future bounce update, no reflection or event-driven path completion here.','specular momentum update')])
    cover('alg1.l8',[X('Random terminal position requires actual path/nonexplosion/kernel construction; Φπ without bounces is not this return law.','return xπ')])
    cover('S3.Thmtheorem1::block0',[X('Whole Proposition3.1 is a consumer/remaining target, not the selected theorem.','well-posedness/stationarity title')])
    cover('S3.Thmtheorem1.p1.1',[C('PARAMETERS','for every fixed y,xRef and initial phase point'),X('Requires actual stochastic recursion and nonexplosion.','unique non-explosive time-homogeneous Markov process'),X('Requires separate path-reversal/invariance proof.','stationary νη,y'),X('Requires nonexplosion and actual terminal state, not deterministic endpoint alone.','xπ well-defined a.s.')])
    cover('S4.E5.m1',[C('PHASE-FLOW','both exact source flow components'),C('GROUP','restart at time t with increment u')])
    cover('A1.SS1.p1.1',[C('PARAMETERS','same fixed y,xRef'),X('Residual rate recall excluded from deterministic flow.','rate uses (3.4)/(3.9)')])
    cover('A1.Ex1',[X('Future actual rate construction, not an arbitrary new rate assumption.','λ formula recall')])
    cover('A1.SS1.p1.2',[C('PHASE-FLOW','deterministic harmonic flow'),C('DERIVATIVE','source calls (4.5) solution of (3.8); verification omitted'),X('Bounce map is a separate deterministic leaf.','bounce map introduction')])
    cover('A1.EGx1',[C('PHASE-FLOW','entire literal Φ formula'),X('Future bounce with zero-normal convention; no completion here.','S(x,p)=(x,R_h p), R0=id')])
    cover('A1.SS1.p1.3',[X('Future reflection geometry and Borel-at-zero analysis.','bounce involution'),X('Must preserve discontinuity caveat; cannot assume continuous bounce normal dependence.','possible discontinuity at h=0'),X('Future actual rate0 fact explains zero-normal convention, not selected flow proof.','rate vanishes at h=0, no ambiguity')])
    cover('A1.SS1.p2.1',[X('Canonical iid exponential clock law must be produced later, not a public deterministic-flow premise.','iid Exp1 clocks'),X('Event recursion initial state/time excluded; selected arc has its own initial value only.','ζ0 and T0 initialization')])
    cover('A1.EGx2',[X('Actual integrated hazards, thresholds and postjump recursion are future option3.','A.1 waiting time and A.2 jump time/postjump state')])
    cover('A1.SS1.p2.2',[X('Stopping at infinite waiting time and piecewise event recursion need separate construction.','finite/infinite waiting-time branches'),X('Selected Φ supplies the deterministic segment map, but existence of every random segment/state is not credited.','ζ_(Tn+t)=Φ_t(ζ_Tn) between jumps')])
    cover('A1.SS1.p3.1',[C('ENERGY','shifted harmonic energy introduced'),X('Nonexplosion is its later intended consumer, not the selected result.','nonexplosion purpose')])
    cover('A1.Ex4',[C('ENERGY','literal weighted sum energy')])
    cover('A1.SS1.p3.2',[C('FLOW-ENERGY','flow preserves energy'),X('Future bounce norm/isometry proof required.','each bounce preserves energy'),X('Requires construction/induction over all random jumps, not merely arc invariance.','initial energy E0 controls every recursion state')])
    cover('A1.Ex5',[X('These path-wide square-root norm bounds require bounce invariance and recursion as well as selected flow energy.','‖p‖≤sqrt2E0 and ‖x−c‖≤sqrt2ηE0')])
    cover('A1.SS1.p3.3',[X('β-Lipschitz gradient is an internally derived future dependency, not an added caller; rate envelope not selected.','gradient β-Lipschitz and whole-path λ bound')])
    cover('A1.Ex6',[X('Exact future energy-shell residual-rate cap; not selected and not an assumed global cap.','λbarE0=sqrtη β sqrt2E0 (sqrt2ηE0+‖c−xRef‖)')])
    cover('A1.SS1.p3.4',[X('Transition into the future hazard integral estimate.','hence')])
    cover('A1.Ex7',[X('Needs actual measurable/integrable hazard and prior pointwise rate envelope.','hazard integral≤λbarE0 u')])
    cover('A1.SS1.p3.5',[X('Future nonexplosion zero-envelope branch must remain explicit, not divide by0.','zero cap gives no jumps; positive cap case')])
    cover('A1.Ex8',[X('Future integrated-hazard hitting-time bound; clocks/rate constructor not available from selected flow alone.','finite waiting S≥Eclock/λbarE0')])
    cover('A1.SS1.p3.6',[X('Future infinite-recursion branch.','recursion does not terminate')])
    cover('A1.Ex9',[X('Future event-time lower bound and divergence, needing actual iid exponential law and SLLN.','Tn≥sum clocks/cap→∞')])
    cover('A1.SS1.p3.7',[X('SLLN must be applied with produced independence, identical law, integrability and positive mean.','a.s. SLLN'),X('Actual all-time path construction and uniqueness remain unproved.','no accumulation and unique all-time process'),X('Memoryless clocks must establish Markov property later.','time-homogeneous Markov property'),X('Davis [12] §2 is a cited construction, not an imported Lean certificate; external text not read in this task.','external Davis citation')])
    cover('A1.Thmtheorem2::block0',[X('A.2 is a future consumer, not selected complete result.','joint-measurability/operator title')])
    cover('A1.Thmtheorem2.p1.1',[X('Actual jointly Borel terminal kernel requires stochastic path and conditional integration, not just continuous Φ.','jointly Borel conditional half-turn kernel')])
    cover('A1.E9',[X('No terminal H_y kernel constructed; actual augmented half-turn operator remains future.','Hf conditional kernel integral')])
    cover('A1.Thmtheorem2.p1.2',[X('Invariance/reversibility and L2 contraction require actual process/kernel proofs.','self-adjoint Markov contraction on L2')])
    assert {r['source_block_id'] for r in coverage}==set(blocks); assert len(coverage)==len(blocks)==51
    gaps=[n['id'] for n in nodes if n['kind']=='SOURCE_GAP']
    edges=[]
    def edge(a,b,use,discharge):
        assert a in N and b in N
        edges.append({'producer':a,'consumer':b,'consumer_source_use_site':use,'use':discharge,'edge_layer':'source reconstructed obligation, not compiled Lean dependency'})
    for a,b,use,d in [
      ('STAND-STEP','SCALE','S4.E5.m1','η>0 internally gives sqrtη>0 and reciprocal identities; cap is retained standing condition but not needed for scale'),
      ('STAND-C2','GRAD-CONT','S3.E4.m1','derive actual gradient continuity internally from C2'),
      ('GRAD-CONT','JOINT-CONT','A1.EGx1','continuous actual center then scalar/vector flow formula'),
      ('CENTER','PHASE-FLOW','A1.EGx1','the SAME c in both position and momentum; no free center premise'),
      ('PHASE-FLOW','POSITION','S3.E6.m1','first component of literal phase formula'),
      ('PHASE-FLOW','DERIVATIVE','A1.SS1.p1.2','differentiate each actual component; source assertion of solution is not treated as a supplied certificate'),
      ('CENTER','DERIVATIVE','alg1.l5','rewrite c to actual y−η∇VxRef to match exact dp force'),
      ('SCALE','DERIVATIVE','alg1.l5','sqrt coefficients/inverses require η>0'),
      ('TRIG','DERIVATIVE','alg1.l5','actual sin/cos derivative APIs, future internal verification'),
      ('DERIVATIVE','ODE-X','alg1.l5','discharge dx equation internally'),
      ('DERIVATIVE','ODE-P','alg1.l5','discharge dp equation internally'),
      ('PHASE-FLOW','INIT','alg1.l4','literal formula evaluated at0'),
      ('TRIG','INIT','alg1.l4','sin0=0 cos0=1'),
      ('PHASE-FLOW','GROUP','S4.E5.m1','restart SAME center/η, expand both components'),
      ('TRIG','GROUP','S4.E5.m1','addition identities discharge time-composition equality; no supplied semigroup'),
      ('PHASE-FLOW','HALF-TURN','S3.E7.m1','evaluate SAME actual formula atπ'),
      ('TRIG','HALF-TURN','S3.E7.m1','sinπ=0 cosπ=−1 remove temporary p from position'),
      ('STAND-STEP','ENERGY-NONNEG','A1.Ex4','positive η gives nonnegative energy weight internally'),
      ('ENERGY','FLOW-ENERGY','A1.SS1.p3.2','preserve the exact shifted weighted sum'),
      ('PHASE-FLOW','NORM-CANCEL','A1.SS1.p3.2','normalized explicit rotation components'),
      ('SCALE','NORM-CANCEL','A1.Ex4','convert η⁻¹‖x−c‖² to normalized coordinate square'),
      ('TRIG','NORM-CANCEL','A1.SS1.p3.2','sin²+cos²=1, same cos/sin in both components'),
      ('NORM-CANCEL','FLOW-ENERGY','A1.SS1.p3.2','cancel opposite mixed real inner terms; no Prod max norm substitution'),
      ('PHASE-FLOW','JOINT-CONT','A1.EGx1','literal scalar/vector operations for all y,xRef,t,x,p at fixed positive η')
    ]: edge(a,b,use,d)
    for a in ['CENTER','PHASE-FLOW','JOINT-CONT','INIT','GROUP','HALF-TURN','ODE-X','ODE-P','ENERGY','ENERGY-NONNEG','FLOW-ENERGY']:
        edge(a,'SELECTED-ANCHOR','selected source-derived actual_harmonic_flow_laws contract','conjunct required in selected interface; not a public assumption')
    write('source-proof-graph.json',{'schema':'independent-source-first-stageA73-v1','target':'actual_harmonic_flow_laws (proposed source-derived anchor, not sealed/claimed/proved)','source_primary':inventory['source_primary'],'source_region_count':13,'source_block_count':51,'nodes':nodes,'node_count':len(nodes),'edges':edges,'edge_count':len(edges),'source_gap_node_ids':gaps,'source_gap_count':len(gaps),'excluded_items':excluded,'excluded_count':len(excluded),'coverage_inventory':'source.coverage.json','topology_source_only':True,'implementation_header_or_proof_used':False,'independent_topology_review_status':'PENDING_DISTINCT_REVIEWER','not_source_topology_reviewed':True,'scope':'Only selected deterministic flow. Future bounce/hazard/nonexplosion/invariance/kernel are excluded with precise consumer reasons.','alternatives':'One literal trig reconstruction route shown. No different ODE uniqueness route is silently ANDed into it.','proof_ingredient_equals_dependency_edge':True})
    node_items=sum(c['disposition']=='NODE' for r in coverage for c in r['subitems']); x_items=sum(c['disposition']=='EXCLUDED' for r in coverage for c in r['subitems'])
    write('source.coverage.json',{'region_count':13,'block_count':51,'semantic_item_count':node_items+x_items,'node_dispositions':node_items,'excluded_dispositions':x_items,'blocks':coverage,'mechanical_check':'exact set equality of all51 parsed substantive/formula/title DOM blocks in all13 fixed source regions; each has nonempty individually classified semantic subitems','qualification':'Semantic subitem exhaustiveness is an independent extractor claim for later distinct topology review; RAW markup coverage/lint is not that review. Overlapping parent anchors for split claims are explicitly block intervals, not invented substring hashes.','outside_selected13':'Whole-paper sources outside these exact selected13 ranges are out of scope; no whole-paper exhaustive claim.'})
    print(json.dumps({'pid':os.getpid(),'source_regions':13,'source_blocks':51,'semantic_items':node_items+x_items,'node_dispositions':node_items,'excluded_dispositions':x_items,'nodes':len(nodes),'source_gaps':len(gaps),'edges':len(edges),'topology_review':'PENDING_DISTINCT_REVIEWER'}))

def binders_and_reuse():
    source=read(OWN/'source.blocks.json'); blocks={v['block_id']:v for r in source['regions'] for v in r['blocks']}
    rows=[]
    def add(name,ty,category,why,anchors,fields=None):
        r={'name':name,'exact_prospective_surface':ty,'classification':category,'justification':why,'source_anchors':anchors,'is_73_declaration_binder_yet':False}
        if fields: r['recursively_expanded_fields']=fields
        rows.append(r)
    add('E','{E : Type*}','TYPING','finite Euclidean carrier represented abstractly; no positive-rank assumption',['S1.p1.1','S3.Thmtheorem1.p1.1'])
    add('normed_additive_carrier','[NormedAddCommGroup E]','TYPING','ambient vector/norm syntax implicit in ℝ^d',['S1.p1.1'])
    add('real_inner_product','[InnerProductSpace ℝ E]','TYPING','Euclidean inner product and induced norm, not a positivity/gap certificate',['S1.p1.1','A1.Ex4'])
    add('finite_dimensional','[FiniteDimensional ℝ E]','TYPING','source finite Euclidean space, finrank0 allowed; no Nontrivial',['S1.p1.1'])
    add('measurable_carrier','[MeasurableSpace E]','TYPING','sigma algebra carrier for Borel consequence, no measurability of flow assumed',['S1.p1.1'])
    add('borel_carrier','[BorelSpace E]','TYPING','standard Euclidean Borel convention; joint map measurability must be derived',['S1.p1.1','A1.Thmtheorem2.p1.1'])
    add('V','{V : E → ℝ}','TYPING','actual potential function carrier',['S1.p1.1'])
    add('αβ','{α β : ℝ≥0}','TYPING','NNReal is representation of source positive ordered moduli; nonnegativity already implied by standing0<α≤β',['S1.p1.1'])
    add('η','{η : ℝ}','TYPING','noise/flow scale carrier; positivity is separate standing field',['S2.SS2.p1.1'])
    add('hα','hα : 0 < (α : ℝ)','STANDING','source-wide positive lower-curvature modulus, not needed by isolated scalar rotation but retained unchanged',['S1.p1.1'])
    add('hαβ','hαβ : α ≤ β','STANDING','source-wide ordered curvature moduli; internally implies β>0 with hα',['S1.p1.1'])
    add('hV','hV : ContDiff ℝ 2 V','STANDING','source-wide C2; C1 and gradient continuity produced internally, never another public premise',['S1.p1.1'])
    add('hH','hH : ∀ x v : E, (α:ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧ (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β:ℝ)*‖v‖^2','STANDING','literal source global two Hessian bounds in real Frechet bilinear coordinates; no supplied Hessian operator',['S1.E1'],[
      {'field':'lower','classification':'STANDING','formula':'∀ x v, (α:ℝ)*‖v‖²≤D²V(x)[v,v]','anchor':'S1.E1'},
      {'field':'upper','classification':'STANDING','formula':'∀ x v, D²V(x)[v,v]≤(β:ℝ)*‖v‖²','anchor':'S1.E1'}])
    add('hη','hη : 0 < η','STANDING','source scale interval excludes0; sqrt inverse coefficients require this actual field',['S2.SS2.p1.1'])
    add('hβη','hβη : (β : ℝ)*η ≤ 1','STANDING','same original capped scale; equivalent to η≤1/β using internally derived β>0; not used to exclude αη=1',['S2.SS2.p1.1'])
    add('y','y : E','SOURCE','for every fixed y in Prop3.1; no distribution or mean premise',['S3.Thmtheorem1.p1.1','A1.SS1.p1.1'])
    add('xRef','xRef : E','SOURCE','for every fixed reference point; querying its same actual gradient determines c; no sampling premise in selected fixed-reference leaf',['S3.Thmtheorem1.p1.1','alg1.l3'])
    add('x','x : E','SOURCE','arbitrary initial position',['S3.Thmtheorem1.p1.1','alg1.l4'])
    add('p','p : E','SOURCE','arbitrary initial momentum, not constrained to a Gaussian realization in deterministic theorem',['S3.Thmtheorem1.p1.1'])
    add('s,t','s t : ℝ','TYPING','time carrier for explicit all-real formula/group extension; source physical simulation uses t∈[0,π], but no time-restriction premise is added','S4.E5.m1'.split())
    banned=[
      ('hGradContinuous : Continuous (gradient V)','C2→C1→existing local gradient-continuity theorem must discharge this internally.'),
      ('hGradLipschitz : LipschitzWith β (gradient V)','Future rate edge must derive this from original Hessians, not add it to flow callers.'),
      ('c : E or hc : c=y−η•gradient V xRef as an additional assumption','Actual c is a literal let/definition, not an arbitrary supplied center or assumption.'),
      ('Φ supplied with ODE/energy/group properties','Actual formula must be produced and its properties proved internally.'),
      ('energy or ODE identities supplied as public premises','These are conclusions/dependency edges.'),
      ('η≠0 or sqrtη≠0 convenience caller','Already derived from hη; retain six callers and no convenience premise.'),
      ('Nontrivial E or 0<finrank E','Would remove legal zero-dimensional case.'),
      ('αη<1 or βη<1','Would improperly remove allowed endpoint αη=1.'),
      ('h≠0 normal condition','Selected flow has no normal; future reflection must use R0=id.'),
      ('IsProbabilityMeasure μ or normalized reference law','Existing actual law normalization/disintegration is an internal earlier producer; deterministic flow requires none.'),
      ('PDMP exists/nonexplosion/stationarity/terminal H premise','These are the future targets, not assumptions closing selected edge.'),
      ('onto polar map, centered inverse/gap, higher derivative or finite moment premise','Unrelated/new assumptions forbidden by original source boundary.')
    ]
    counts={c:sum(r['classification']==c for r in rows) for c in ['SOURCE','STANDING','TYPING','RULED','EXCESS']}
    write('standing-assumptions.audit.json',{'audit_kind':'separate source-wide standing-field expansion within independent StageA, not a new theorem or accepted73 header','source_global_scope':['S1.p1.1 and (1.1)','S2.SS2.p1.1 scale interval'],'field_count':6,'expanded_hessian_field_count':2,'fields':[r for r in rows if r['classification']=='STANDING'],'only_positive_eta_and_C1_needed_for_selected_core':'C2 retained and supplies C1. Curvature/cap fields are original standing source compatibility, not new proof providers.','prior_literal_caller_reference':next(r['original_input_reference'] for r in read(OWN/'old21.version-map.json')['rows'] if r['original_input_reference']['path'].endswith('/ActualCorrectorChange.lean')),'independent_topology_review_status':'PENDING_DISTINCT_REVIEWER'})
    write('binder-audit.json',{'status':'PROSPECTIVE_EXACT_CLASSIFICATION_ONLY_BEFORE_73_HEADER','binder_item_count':len(rows),'classification_counts':counts,'items':rows,'standing_audit':'standing-assumptions.audit.json','source_rule':'SOURCE explicit statement premise/quantifier; STANDING separately expanded source-wide field; TYPING implicit carrier; RULED human correction; EXCESS unjustified convenience/proof premise','accepted_excess_count':0,'ruled_count':0,'rejected_candidate_excess':[{'surface':x,'classification':'EXCESS','reason':y,'accepted':False} for x,y in banned],'six_original_callers_preserved':True,'all_73_binders_actually_checked':False,'qualification':'No73 header or implementation exists in the input boundary; final writer must later match the sealed literal surface to this exact prospective inventory, without promoting dependency nodes into callers.'})
    definition={
      'status':'SOURCE_DEFINITION_SEMANTICS_ONLY','definitions':[
        {'name':'c','kind':'literal','source':'S3.E4.m1','formula':'c(y,xRef)=y−η•gradient V xRef','whole_carrier':'every y,xRef:E under same fixed V,η','must_match':'same xRef gradient used in both flow components and Algorithm1 ODE; no arbitrary center parameter in actual adapter'},
        {'name':'Φ','kind':'literal','source':['S4.E5.m1','A1.Ex2.m1','A1.Ex2.m2'],'formula':'(c+cos(t)•(x−c)+(sqrtη*sin(t))•p, (−sin(t)/sqrtη)•(x−c)+cos(t)•p)','whole_carrier':'all real t, all phase points; actual physical arcs nonnegative times','must_match':'same c,η and initial x,p; exact negative sign/reciprocal in momentum; no fallback path or characterized-but-unproved flow'},
        {'name':'H','kind':'literal','source':'A1.Ex4','formula':'(η⁻¹*‖x−c‖²+‖p‖²)/2','whole_carrier':'all x,p with same actual c','must_match':'weighted SUM of squared E norms; E×E is only coordinate/topology packaging, not max-norm energy; scalar H is distinct from future half-turn kernel/operator mathcalH/mathsfH'},
        {'name':'optional Flow ℝ (E×E)','kind':'characterized interface for literal Φ','source':['S4.E5.m1','A1.SS1.p1.2'],'must_match':'reuse Mathlib.Flow representation only after proving continuous/group/zero fields internally; object must be pointwise equal to source Φ, not an arbitrary assumed flow'}
      ],
      'boundary_cases':{
        'eta_positive':'r=sqrtη>0,r²=η,η⁻¹=r⁻² are future internally discharged coefficient identities. η=0 is outside source; no claim of continuous extension across0.',
        'fixed_eta_continuity':'Required joint continuity ranges over y,xRef,t,x,p at fixedη>0; no claim of continuity atη=0.',
        'rank0':'Finite-dimensional zero space allowed. Every vector/gradient/norm0; Φ=id,H=0 and π formula hold; no Nontrivial.',
        'alpha_eta_one':'Original α≤β and βη≤1 permit αη=1; selected formulas never divide by1−αη or require centered gap.',
        'zero_energy':'Initial (c,0) is fixed by selected flow; future cap0 branch remains separate; no division by energy.',
        'zero_normal':'Only a preserved future-boundary convention R0=id. Bounce is excluded; never infer normal-dependent reflection continuity or add h≠0.',
        'no_parent_operator_credit':'No ontoV, centered inverse, polar/68 energy/72 perturbation dependence is introduced. Deterministic finite-dimensional phase flow is different from the existing realL2 operator graph.'
      },
      'new_proof_or_definition_compiled':False}
    write('definition-semantics-and-boundary.json',definition)
    gps=[ROOT/'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean',ROOT/'AutoSamplingTheory/TechnicalLemmas/Analysis/GibbsGradientMean.lean',ROOT/'AutoSamplingTheory/TechnicalLemmas/Analysis/GibbsGradientMoment.lean']
    gp=gps[0].read_bytes(); a=gp.index(b'theorem continuous_gradient_of_contDiff_one'); z=gp.index(b':= by',a)
    write('gradient-continuity.statement.exactraw.txt',gp[a:z])
    callers=[]
    for p in gps[1:]:
        raw=p.read_bytes(); needle=b'Calculus.Gradient.continuous_gradient_of_contDiff_one'; start=raw.index(needle); end=raw.index(b'\n',start)+1
        callers.append({'path':p.relative_to(ROOT).as_posix(),'whole_file_raw_sha256':sha(raw),'raw_byte_start_inclusive':start,'raw_byte_end_exclusive':end,'literal_span_raw_sha256':sha(raw[start:end]),'exact_call_utf8':raw[start:end].decode('utf-8')})
    extra=[ROOT/'docs/proof-digestion-protocol.md',ROOT/'docs/evidence-routed-memory-protocol.md',*gps]
    write('supplemental.inputs.manifest.json',{'input_count':len(extra),'inputs':[pin(p) for p in extra],'finite_reason':'binder/SPG governance and exact newly located reusable gradient-continuity producer plus2 real existing consumers; no future73 or72 verdict'})
    write('reuse.gradient-continuity.json',{'node_id':'GRAD-CONT','omitted_source_bridge_resolution':'EXISTING_LOCAL_PRODUCER_FOUND; future73 must apply internally, no new regularity caller','declaration':'AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one','producer':pin(gps[0]),'raw_byte_start_inclusive':a,'raw_byte_end_exclusive':z,'literal_span_raw_sha256':sha(gp[a:z]),'signature_snapshot':'gradient-continuity.statement.exactraw.txt','required_input':'ContDiff ℝ 1 V; original hV:ContDiff ℝ 2 V implies this by lowering smoothness','complete_space':'derived from finite dimension; no extra public CompleteSpace/regularity certificate needed','actual_existing_consumers':callers,'new_compile_or73_proof_credit':False,'source_gap_status':'paper omits this calculus bridge; known canonical producer exists, actual73 application is still future','parent_pointer_not_topology_authority':True})
    write('stageA-decision.json',{'decision':'STAGE_A_SOURCE_FIRST_EXTRACTION_READY','scope':'independent selected deterministic flow source topology/binder/definition inventory only','source_proof_graph':pin(OWN/'source-proof-graph.json'),'coverage_inventory':pin(OWN/'source.coverage.json'),'binder_audit':pin(OWN/'binder-audit.json'),'definition_audit':pin(OWN/'definition-semantics-and-boundary.json'),'gradient_reuse':pin(OWN/'reuse.gradient-continuity.json'),'old103_planning_only_preserved':True,'all21_old_raw_lf_inputs_referenced':True,'no_new_header_or_implementation_consumed':True,'no_compiler_proof_sau_git_canonical_ledger_goal_writes':True,'topology_acceptance':'PENDING_DISTINCT_REVIEWER; extractor cannot approve own coverage per docs/proof-digestion-protocol.md §5','not_proved_or_verified':True,'future_bounce_hazard_nonexplosion_invariance_kernel_credit':False})
    print(json.dumps({'pid':os.getpid(),'binder_items':len(rows),'classification_counts':counts,'standing_fields':6,'rejected_extra_candidates':len(banned),'supplemental_input_count':len(extra),'gradient_producer':pin(gps[0]),'decision':'STAGE_A_SOURCE_FIRST_EXTRACTION_READY'}))

def input_union():
    core=read(OWN/'inputs.manifest.json')['inputs']; supplemental=read(OWN/'supplemental.inputs.manifest.json')['inputs']; old=[r['current_input'] for r in read(OWN/'old21.version-map.json')['rows']]
    rows=[]; seen=set()
    for category,group in [('CLOSED103_native_authority',core),('new_governance_and_exact_gradient_reuse',supplemental),('referenced_original21_current_exact',old)]:
        for r in group:
            assert compatible(r,pin(ROOT/r['path']))
            if r['path'] not in seen:
                rows.append({'category':category,**r}); seen.add(r['path'])
    write('inputs.complete-union.manifest.json',{'input_count':len(rows),'authority_input_count':len(core),'supplemental_input_count':len(supplemental),'referenced_old21_input_count':len(old),'inputs':rows,'every_version_resolution':'EXACT_RAW_AND_CRLF_ONLY_LF_EQUALITY; no historical drift/fallback needed','source_snapshots':'fixed primary and old CLOSED103 literal slices are reused by exact refs; no recursive historical payload copies'})
    write('header-existence.qualification.json',{'basis':'trusted parent message during StageA, not filesystem inspection','known_opaque_path':'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/header73.proposed.lean','parent_reports':'unsealed candidate signature created outside this StageA scope; no proof BODY and nonproduction','read_by_this_actor':False,'hash_read_or_recorded':False,'included_as_input':False,'historical_qualification':'CLOSED103 no-header-at-planning statements remain historical immutable. This StageA claims no73 header/implementation CONSUMED, not that no future candidate file currently exists.','source_topology_independence_unchanged':True})
    print(json.dumps({'pid':os.getpid(),'complete_input_union_count':len(rows),'new_authority_inputs':len(core),'supplemental':len(supplemental),'old_references':len(old),'header_consumed':False}))

def check_core():
    for fname in ['inputs.manifest.json','supplemental.inputs.manifest.json','inputs.complete-union.manifest.json']:
        j=read(OWN/fname); assert j['input_count']==len(j['inputs'])
        for r in j['inputs']: assert compatible(r,pin(ROOT/r['path'])),r['path']
    vm=read(OWN/'old21.version-map.json'); assert vm['row_count']==len(vm['rows'])==21
    for r in vm['rows']:
        assert compatible(r['original_input_reference'],r['current_input']); assert compatible(r['current_input'],pin(ROOT/r['current_input']['path']))
    inv=read(OWN/'source.blocks.json'); primary=(ROOT/inv['source_primary']['path']).read_bytes()
    assert sha(primary)==inv['source_primary']['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
    ids=set()
    for region in inv['regions']:
        q=primary[region['raw_byte_start_inclusive']:region['raw_byte_end_exclusive']]; assert sha(q)==region['whole_region_raw_sha256']
        for r in region['blocks']:
            assert r['block_id'] not in ids; ids.add(r['block_id'])
            q=primary[r['raw_byte_start_inclusive']:r['raw_byte_end_exclusive']]; assert sha(q)==r['literal_span_raw_sha256'] and len(q)==r['bytes']
    coverage=read(OWN/'source.coverage.json'); graph=read(OWN/'source-proof-graph.json'); nids={x['id'] for x in graph['nodes']}
    assert {x['source_block_id'] for x in coverage['blocks']}==ids
    assert len(coverage['blocks'])==len(ids)==51
    assert all(c['disposition'] in ['NODE','EXCLUDED'] for r in coverage['blocks'] for c in r['subitems'])
    assert all(r['subitems'] for r in coverage['blocks'])
    for r in coverage['blocks']:
        for c in r['subitems']:
            if c['disposition']=='NODE': assert c['node_id'] in nids
            else: assert c['reason'] and c['excluded_id']
    assert len(graph['nodes'])==graph['node_count']==23
    assert len(graph['edges'])==graph['edge_count']==35
    assert graph['independent_topology_review_status']=='PENDING_DISTINCT_REVIEWER'
    for e in graph['edges']: assert e['producer'] in nids and e['consumer'] in nids and e['consumer_source_use_site'] and e['use']
    # Source graph structural acyclicity; this does not replace independent topology review.
    pending=set(nids); done=set()
    while pending:
        ready={x for x in pending if all(e['producer'] in done for e in graph['edges'] if e['consumer']==x)}
        assert ready,'source obligation graph cycle'
        done|=ready; pending-=ready
    ba=read(OWN/'binder-audit.json'); assert ba['classification_counts']=={'SOURCE':4,'STANDING':6,'TYPING':10,'RULED':0,'EXCESS':0}
    assert ba['binder_item_count']==len(ba['items'])==20 and ba['accepted_excess_count']==0
    reuse=read(OWN/'reuse.gradient-continuity.json'); raw=(ROOT/reuse['producer']['path']).read_bytes(); span=raw[reuse['raw_byte_start_inclusive']:reuse['raw_byte_end_exclusive']]
    assert sha(span)==reuse['literal_span_raw_sha256']; assert span==(OWN/reuse['signature_snapshot']).read_bytes()
    return {'old21_exact_raw_lf':True,'core_authorities':12,'supplemental_inputs':5,'complete_input_union_count':read(OWN/'inputs.complete-union.manifest.json')['input_count'],'source_regions':13,'source_blocks':51,'semantic_items':coverage['semantic_item_count'],'node_dispositions':coverage['node_dispositions'],'excluded_dispositions':coverage['excluded_dispositions'],'source_graph_nodes':23,'source_graph_edges':35,'source_gap_nodes':7,'binder_items':20,'binder_classification_counts':ba['classification_counts'],'dag_structural_check':'PASS_ONLY','independent_topology_acceptance':'PENDING_DISTINCT_REVIEWER','header_or_implementation_consumed':False,'compiler_or_proof_search_run':False,'canonical_ledger_git_goal_writes':False}

def finalize():
    checked=check_core(); write('final-core-readback.json',{'pid':os.getpid(),'checks':checked})
    names=['stageA-decision.json','source-proof-graph.json','source.coverage.json','binder-audit.json','standing-assumptions.audit.json','definition-semantics-and-boundary.json','reuse.gradient-continuity.json','source.blocks.json','closed103.reference-validation.json','inputs.manifest.json','old21.version-map.json','supplemental.inputs.manifest.json','inputs.complete-union.manifest.json','header-existence.qualification.json','final-core-readback.json']
    payload={'schema':'complete-named-independent-stageA73-source-proof-graph','actor':'/root/exact_science63','decision':'STAGE_A_SOURCE_FIRST_EXTRACTION_READY','content':{n:read(OWN/n) for n in names},'exact_content_raw_pins':[pin(OWN/n) for n in names],'actual_native_terminals':{p.name:read(p) for p in sorted(OWN.glob('*.receipt.json'))},'no_theorem_proof_or_source_topology_self_approval':True}
    write('complete-named-stageA-source-review.payload.json',payload)
    files=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name not in ['outputs.manifest.json','run.json'] and not p.name.startswith('finalizer.')]
    write('outputs.manifest.json',{'output_count':len(files),'files':files,'deferred_self_layers':'run/this manifest and active finalizer/readback/close terminal layers all bound by final CLOSED_LAST lease; no final exclusion'})
    run={'schema':'native-independent-stageA73-sourcegraph','actor':'/root/exact_science63','decision':'STAGE_A_SOURCE_FIRST_EXTRACTION_READY','checked_primary_raw_sha256':checked and 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760','decision_file':pin(OWN/'stageA-decision.json'),'complete_named_payload':pin(OWN/'complete-named-stageA-source-review.payload.json'),'complete_input_manifest':pin(OWN/'inputs.complete-union.manifest.json'),'output_manifest':pin(OWN/'outputs.manifest.json'),'checks':checked,'logical_hash_recipe':'canonical UTF8 JSON sort_keys=true ensure_ascii=false separators comma/colon; delete ONLY top-level run_sha256'}
    run['run_sha256']=sha(canonical(run)); write('run.json',run)
    print(json.dumps({'pid':os.getpid(),'decision':run['decision'],'whole_logical_run_sha256':run['run_sha256'],'complete_named_payload':run['complete_named_payload'],'complete_input_manifest':run['complete_input_manifest'],'checks':checked,'baseline_output_count':len(files)}))

def verify_run():
    j=read(OWN/'run.json'); h=j.pop('run_sha256'); assert sha(canonical(j))==h
    for k in ['decision_file','complete_named_payload','complete_input_manifest','output_manifest']: assert compatible(j[k],pin(ROOT/j[k]['path']))
    for r in read(OWN/'outputs.manifest.json')['files']: assert compatible(r,pin(ROOT/r['path']))
    check_core(); return {'whole_logical_run_sha256':h,'complete_named_payload':j['complete_named_payload'],'complete_input_manifest':j['complete_input_manifest'],'checks':j['checks']}

def readback(): print(json.dumps({'pid':os.getpid(),'verdict':'PASS','read_only':True,**verify_run()}))

def close():
    assert not (OWN/'lease.final.json').exists()
    write('close.executed-helper.RAW.py',(OWN/'stageA73.py').read_bytes()); result=verify_run()
    cmd=[PY,'-B','-X','utf8',str(OWN/'stageA73.py'),'readback']; p=subprocess.Popen(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE); out,err=p.communicate(); assert p.returncode==0
    write('close.readonly-probe.receipt.json',{'pid':p.pid,'exit_code':p.returncode,'terminal_closed':True,'command':cmd,'stdout_raw_sha256':sha(out),'stdout_utf8':out.decode('utf-8'),'stderr_raw_sha256':sha(err),'stderr_utf8':err.decode('utf-8')})
    write('close.writer.receipt.json',{'pid':os.getpid(),'action':'all finite source/binder/input/native checks; await readonly probe; write CLOSED_LAST as last owned write; return normally','terminal_exit_expected':0,'probe_pid':p.pid,'probe_actual_exit_code':p.returncode,'no_owned_writes_after_lease':True})
    files=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file()]; ch=sha(canonical(files))
    lease={'state':'CLOSED_LAST','actor':'/root/exact_science63','scope':OWN.relative_to(ROOT).as_posix(),'owned_count_including_lease':len(files)+1,'all_files_except_self':files,'closure_sha256':ch,'whole_logical_run_sha256':result['whole_logical_run_sha256'],'complete_named_payload':result['complete_named_payload'],'close_writer_pid':os.getpid(),'read_only_probe_pid':p.pid,'read_only_probe_actual_exit_code':p.returncode,'finalizer_receipt':pin(OWN/'finalizer.receipt.json'),'readback_receipt':pin(OWN/'readback.receipt.json'),'last_owned_write':'lease.final.json','postclose':'external read-only checks only; zero owned writes'}
    write('lease.final.json',lease)
    print(json.dumps({'pid':os.getpid(),'state':'CLOSED_LAST','owned_count':len(files)+1,'closure_sha256':ch,'lease':pin(OWN/'lease.final.json'),'close_probe_pid':p.pid,'close_probe_actual_exit_code':p.returncode,**result}))

def postclose():
    lease=read(OWN/'lease.final.json'); assert lease['state']=='CLOSED_LAST'
    files=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name!='lease.final.json']; assert files==lease['all_files_except_self']; assert sha(canonical(files))==lease['closure_sha256']; assert len(files)+1==lease['owned_count_including_lease']
    for n in ['finalizer.receipt.json','readback.receipt.json','close.readonly-probe.receipt.json']:
        r=read(OWN/n); assert r['exit_code']==0 and r['terminal_closed']
    print(json.dumps({'pid':os.getpid(),'verdict':'PASS','read_only_postclose':True,'owned_writes':0,'owned_count':len(files)+1,'closure_sha256':lease['closure_sha256'],'lease':pin(OWN/'lease.final.json'),**verify_run()}))
def runner(label,mode):
    assert not (OWN/'lease.final.json').exists()
    write(label+'.executed-helper.RAW.py',(OWN/'stageA73.py').read_bytes())
    cmd=[PY,'-B','-X','utf8',str(OWN/'stageA73.py'),mode]; start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (OWN/(label+'.stdout.log')).open('wb') as out,(OWN/(label+'.stderr.log')).open('wb') as err:
        p=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err); print(json.dumps({'runner_pid':os.getpid(),'pid':p.pid,'command':cmd}),flush=True); ec=p.wait()
    receipt={'runner_pid':os.getpid(),'pid':p.pid,'exit_code':ec,'terminal_closed':True,'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'stdout':pin(OWN/(label+'.stdout.log')),'stderr':pin(OWN/(label+'.stderr.log'))}
    write(label+'.receipt.json',receipt); print(json.dumps(receipt),flush=True); sys.exit(ec)
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='run': runner(sys.argv[2],sys.argv[3])
    elif mode=='freeze': freeze()
    elif mode=='graph': graph()
    elif mode=='binders': binders_and_reuse()
    elif mode=='union': input_union()
    elif mode=='finalize': finalize()
    elif mode=='readback': readback()
    elif mode=='close': close()
    elif mode=='postclose': postclose()
