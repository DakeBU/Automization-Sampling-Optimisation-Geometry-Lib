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
