"""Owned source-only inventory/API recommendation. No Lean candidate or claim writes."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, datetime, subprocess

ROOT=Path('E:/Samplinglib')
OUT=Path(__file__).resolve().parent
PRIMARY='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    q=ROOT/p; b=q.read_bytes()
    return {'path':str(p).replace('\\','/'),'raw_sha256':sha(b),'bytes':len(b)}
def put(name,value):
    p=OUT/name
    assert not p.exists(), ('immutable output already exists',name)
    p.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    return pin(p.relative_to(ROOT))
notes_path=OUT/'source-first-notes85.json'
notes=json.loads(notes_path.read_text(encoding='utf-8'))
assert sha(notes_path.read_bytes())=='9e9e3737db6cc73e351ffe7daa8ad7dbb124e546f1378a25372ae0dab36fa1c1'
assert pin(PRIMARY)['raw_sha256']==notes['primary_raw']['sha256']
class SourceHTML(HTMLParser):
    void={'br','hr','meta','link','img','input','source','wbr','area','base','col','embed','param','track'}
    def __init__(self): super().__init__(); self.stack=[]; self.text={}; self.math=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag not in self.void: self.stack.append((tag,a.get('id')))
        if tag=='math':
            self.math+=1
            if self.math==1:
                for _,i in self.stack:
                    if i: self.text.setdefault(i,[]).append(a.get('alttext',''))
    def handle_endtag(self,tag):
        if tag=='math': self.math-=1
        for k in range(len(self.stack)-1,-1,-1):
            if self.stack[k][0]==tag: self.stack=self.stack[:k]; break
    def handle_data(self,s):
        if not self.math:
            for _,i in self.stack:
                if i: self.text.setdefault(i,[]).append(s)
    def normalized(self,i): return ' '.join(' '.join(self.text[i]).split())
h=SourceHTML(); h.feed((ROOT/PRIMARY).read_text(encoding='utf-8'))
for a in notes['anchors']: assert sha(h.normalized(a['source_id']).encode())==a['normalized_anchor_sha256']
assert 'perpetual non-exclusive' in h.normalized('license-tr')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
pbps='AutoSamplingTheory/ExampleCases/ProximalBPS/'
apis=[pbps+p+'.lean' for p in ['ActualPhysicalTimeMeasurability','IdealHalfTurnKernel','ActualSmallTimeContinuity','ActualBoundedTestContinuity','ActualOuterBoundedL2Continuity']]
apis += ['AutoSamplingTheory/TechnicalLemmas/StochasticProcesses/MarkovSemigroup.lean','.lake/packages/mathlib/Mathlib/Probability/Kernel/Composition/MapComap.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean']
queries=[['rg','-l','ActualPhysicalTimeMeasurability|ActualBoundedTestContinuity|ActualOuterBoundedL2Continuity|IdealHalfTurnKernel','AutoSamplingTheory','-g','*.lean'],['rg','-n','Kernel.*E × E|Kernel.*ℝ≥0|actual.*transition.*kernel|physical.*kernel',pbps,'-g','*.lean'],['rg','-n','Kernel.*ℝ≥0|actual_.*transition.*kernel|physical_time.*kernel|actual.*phase.*kernel','AutoSamplingTheory','-g','*.lean']]
searches=[]
for args in queries:
    r=subprocess.run(args,cwd=ROOT,capture_output=True,encoding='utf-8')
    assert r.returncode in [0,1]
    searches.append({'argv':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
api={'schema':'astis.source-only-api-retrieval85.v1','created_utc':now,'chronology':'Primary-only notes85 were frozen before existing80/81/83/84 API retrieval. This retrieval does not use earlier reviewer verdicts or proposed85 mathematics.','source_first_notes':pin(notes_path.relative_to(ROOT)),'exact_inspected_inputs':[pin(p) for p in apis],'duplicate_searches':searches,'conclusions':[
 {'producer':'actual_physical_time_measurable_phase','scope':'Jointly measurable actual full phase Z, every live covering arc and uncovered initial-phase fallback; for each fixed tuple one P-AE event covers all finite times and initializes Z0=z. No exported Kernel.'},
 {'producer':'ideal_half_turn_returned_position_kernel','scope':'Ideal H mixes exact conditional-reference, independent standard momentum and clocks at time pi, then projects position. It is Kernel(E×E)E; its source is random reference/momentum, unlike deterministic-reference arbitrary-initial-phase K at all finite times.'},
 {'producer':'actual_bounded_test_expectation_continuity','scope':'Actual Z plus inner continuous bounded test expectations and zero-time convergence; no phase transition Kernel.'},
 {'producer':'actual_outer_bounded_l2_continuity','scope':'Same actual Z plus exact q/nu normalization, measurable state expectation and bounded squared outer convergence; internal conditional position kernel R only, no actual full-phase Kernel.'},
 {'producer':'MarkovSemigroup.TransitionKernelContract','scope':'Generic probability fibers, initial identity AND Chapman-Kolmogorov contract. The proposed actual-law interface can supply first two only. Existing generic semigroup leaves are not actual PBPS producers.'},
 {'producer':'Mathlib Kernel.map / IsMarkovKernel.map, existing81 id×const construction, MeasureTheory.integral_map','scope':'Reusable generic APIs; no need new generic pushforward wrapper. Source-specific integration must consume actual parent Z and actual iidExp1 P, derive K0 and actual test identity.'}],
 'bounded_negative_search':'No exported actual PBPS full-phase finite-time kernel found in direct producer declarations, their import/consumer search, or the recorded repository patterns. This is a bounded current-tree duplicate audit, not a universal theorem-name absence claim.'}
api_pin=put('api-retrieval85.json',api)

nodes=[]
def N(n,title,status,ids): nodes.append({'id':f'G85-{n:02d}','title':title,'status':status,'source_ids':ids})
N(1,'Original six analytic assumptions, finite Borel phase including rank0','SOURCE_ASSUMPTIONS',['S1.p1.1','S1.E1','S2.SS2.p1.1'])
N(2,'Actual literal flow/bounce/rate/stopped recursion and finite physical interpolation','SOURCE_AND_EXISTING_PARENT',['A1.Ex1','A1.Ex2','A1.Ex3','A1.E1','A1.E2','A1.SS1.p2.1','A1.SS1.p2.2'])
N(3,'Actual iid Exp1 product P is probability','SOURCE_AND_EXISTING_PARENT',['A1.SS1.p2.1'])
N(4,'Total actual joint phase Z with retained arc/fallback and fixed-parameter common AE semantics','EXISTING_ACTUAL80_83_84_INTERFACE_NOT_REVERIFIED',['A1.SS1.p3.7','A1.SS2.p3.1'])
N(5,'Joint map (parameter tuple, clock) to actual Z','ASTIS_ELABORATION_CANDIDATE',['A1.SS2.p3.1'])
N(6,'Parameter identity times constant actual-clock probability kernel','GENERIC_BACKGROUND_CANDIDATE',['A1.SS1.p2.1'])
N(7,'Actual full-phase pushforward kernel K with joint index y,r,z,t','ASTIS_ELABORATION_CANDIDATE',['A1.SS2.p3.1','A1.Thmtheorem1'])
N(8,'Exact fiber equality K(a)=map(Z(a))P and measurable-event identity','ACTUAL_INTEGRATION_CANDIDATE',['A1.SS1.p2.2','A1.SS2.p3.1'])
N(9,'Probability of every finite-time kernel fiber','ACTUAL_INTEGRATION_CANDIDATE',['A1.SS1.p2.1'])
N(10,'For each deterministic tuple, actual AE Z0=z','EXISTING_PARENT_INITIALIZATION',['A1.SS1.p2.1','A1.SS2.p3.1'])
N(11,'Zero-time phase law is Dirac z','ACTUAL_INTEGRATION_CANDIDATE',['A1.SS1.p2.1'])
N(12,'Bounded Borel real test, bound M>=0, actual joint composition','EXPLICIT_TEST_BINDERS',['A1.SS1.SSS0.Px1.p5.2'])
N(13,'Integrable kernel/clock tests and exact expectation transfer','ACTUAL_INTEGRATION_CANDIDATE',['A1.SS1.SSS0.Px1.p5.2','A1.SS1.SSS0.Px1.p6.1'])
N(14,'Exact normalized q_y times standard Gaussian candidate nu_y','EXISTING_ACTUAL84_INTERFACE_NOT_REVERIFIED',['S2.E8','S3.E1'])
N(15,'Actual n-jump path law, summability, reverse change of variables and survival/jump identity','FUTURE_OPEN',['A1.SS1.SSS0.Px1.p4.2','A1.SS1.SSS0.Px1.p4.3','A1.SS1.SSS0.Px1.p5.2'])
N(16,'Actual nu invariance from bounded reversal identity with F=1','FUTURE_OPEN',['A1.SS1.SSS0.Px1.p5.3'])
N(17,'AE-safe L2 operator and Jensen contraction','FUTURE_OPEN',['A1.SS1.SSS0.Px1.p6.1'])
N(18,'Independent compact-continuous density in L2(nu)','FUTURE_OPEN',['A1.SS1.SSS0.Px1.p6.2'])
N(19,'Actual bounded continuous outer convergence; source C_c subclass','EXISTING_ACTUAL84_INTERFACE_NOT_REVERIFIED',['A1.Ex22','A1.SS1.SSS0.Px1.p6.2'])
N(20,'Full all-L2 strong continuity','FUTURE_OPEN',['A1.SS1.SSS0.Px1.p6.2'])
N(21,'Process Markov/restart/Chapman-Kolmogorov, global invariance/cost/main claims','EXCLUDED_OPEN_BOUNDARY',['A1.SS1.p3.7','S3.Thmtheorem1','A1.Thmtheorem1'])
edges=[]
def E(a,b,kind='INGREDIENT',route='REQUIRED',dep=True,why=''):
    edges.append({'id':f'E85-{len(edges)+1:02d}','from':f'G85-{a:02d}','to':f'G85-{b:02d}','classification':kind,'route':route,'dependency_edge':dep,'reason':why})
for a,b in [(1,2),(2,4),(3,4),(4,5),(3,6),(5,7),(6,7),(7,8),(5,8),(7,9),(3,9),(4,10),(8,11),(10,11),(3,11),(8,13),(5,13),(12,13),(3,13)]: E(a,b)
E(1,14,'EXISTING_PARENT')
E(15,16,'FUTURE_OPEN');E(14,16,'FUTURE_OPEN')
E(16,17,'FUTURE_OPEN')
E(17,20,'FUTURE_OPEN');E(18,20,'FUTURE_OPEN');E(19,20,'FUTURE_OPEN')
E(8,16,'EXCLUDED_LAW_TARGET_ASSOCIATION','OPTIONAL_REPRESENTATION',False,'K gives a common typed target nu.bind K_t=nu. Kernel construction is not an invariance ingredient and is not logically required if the same proof uses direct pushforwards.')
E(13,17,'EXCLUDED_OPERATOR_INTERFACE_ASSOCIATION','OPTIONAL_REPRESENTATION',False,'Expectation transfer names the source pointwise operator; AE quotient well-definedness and L2 contraction still require true invariance.')
E(9,21,'EXCLUDED_BOUNDARY_ASSOCIATION','NO_IMPLICATION',False,'IsMarkovKernel means probability fibers only; it cannot establish process memorylessness/restart/Markov or Chapman-Kolmogorov.')
graph={'schema':'astis.source-proof-graph85.v1','status':'SOURCE_ONLY_PROSPECTIVE_NO_HEADER_OR_PROOF','source_first_notes':pin(notes_path.relative_to(ROOT)),'nodes':nodes,'edges':edges,'junctions':[
 {'target':'G85-07','kind':'AND','ingredients':['G85-05','G85-06']},
 {'target':'G85-11','kind':'AND','ingredients':['G85-08','G85-10','G85-03']},
 {'target':'G85-13','kind':'AND','ingredients':['G85-08','G85-05','G85-12','G85-03']},
 {'target':'G85-16','kind':'AND_FUTURE_OPEN','ingredients':['G85-15','G85-14']},
 {'target':'G85-20','kind':'AND_FUTURE_OPEN','ingredients':['G85-17','G85-18','G85-19']}],
 'route_boundary':'id×const/map and a direct parameter-integral construction are optional OR realizations of the same candidate kernel; not both required. Future invariance may use K or direct pushforwards as optional representations, not different mathematical invariance assumptions.',
 'coverage':'Every source inventory85 item has a mapping or explicit boundary below. Future nodes are neither candidate conclusions nor compiled claims.'}
graph_pin=put('source-proof-graph85.json',graph)
maps=[[1],[2,3,4,10],[4,10],[7,8],[5,6,7],[9,21],[10,11],[12,13],[14],[15,16],[17],[18,19,20],[7],[12,19],[15,16,17,18,20,21],[]]
inventory={'schema':'astis.source-inventory85.v1','status':'SOURCE_ONLY','primary_raw':pin(PRIMARY),'anchors':notes['anchors'],'additional_anchor_pins':[{'source_id':i,'normalized_anchor_sha256':sha(h.normalized(i).encode())} for i in ['A1.SS1.SSS0.Px1.p4.4','A1.SS1.SSS0.Px1.p1.1','A1.SS1.SSS0.Px1.p2.1']], 'license':'perpetual non-exclusive arXiv license; retain exact raw primary; this freeze reproduces only minimal formulas and paraphrases.','items':[dict(i,graph_nodes=[f'G85-{n:02d}' for n in m],coverage='API_DUPLICATE_AUDIT' if not m else 'MAPPED_OR_EXPLICIT_OPEN_BOUNDARY') for i,m in zip(notes['source_inventory'],maps)],'source_first_inventory_unchanged':pin(notes_path.relative_to(ROOT))}
inventory_pin=put('source-inventory85.json',inventory)
recommendation={'schema':'astis.source-only-recommendation85.v1','status':'PROSPECTIVE_ONLY_NO_SAU_HEADER_STATEMENTSEAL_OR_PROOF','recommendation':'Select one actual finite-physical-time full-phase law/kernel integration consumer, provided it includes zero-time law and exact bounded-Borel expectation transfer; retire a candidate containing only supplied measurable-map pushforward existence.','source_reason':'Appendix A.1 names actual transition operators, uses bounded measurable F,G in the path-reversal identity, derives invariance with F=1 and then Jensen contraction. Existing actual Z producers yield clock expectations but do not export the corresponding arbitrary-state finite-time phase law. This is a useful law interface, not a new proof of invariance and not a logically necessary representation of the pathwise proof.','duplicate_assessment':'No duplicate actual full-phase K found in recorded bounded current-tree/API audit. Existing81 H_y is ideal exact-reference random-initialization position law at pi; generic TransitionKernelContract requires unproved Chapman-Kolmogorov. Neither supplies this actual K.','bounded_candidate':{
 'parameters':'Same original six analytic binders; finite-dimensional real inner-product Borel E including rank0. Fixed dynamics V,alpha,beta,eta; jointly measurable index a=(y,r,z,t), y,r in E, z in E×E, t finite NNReal. No uniform constants or random parameter binder.',
 'producer':'Consume actual80/83/84 literal eleven definitions, actual P=infinite iid Exp1 product, and the SAME total joint Z satisfying every live arc/fallback, per-fixed-tuple common AE all finite times and Z0=z. Do not accept arbitrary Z or joint-measurability/probability premises.',
 'law':'K(a,A)=P{omega:Z(y,r,z,t,omega) in A}; equivalently K(a)=map(Z(y,r,z,t))P, for every finite t and measurable full-phase event A.',
 'outputs':['K is a jointly indexed probability kernel (parameter/time Borel measurability); probability of fibers is not process Markov.','K(y,r,z,0)=dirac z derived from retained actual AE initialization.','For every bounded Borel real g and M>=0 with |g|<=M, both kernel and clock tests are integrable and their integrals agree exactly; optionally state the immediate measurable pointwise operator as the same clock expectation.'],
 'nonchurn_consumer':'Exact expectation transfer turns source transition test identities into law/operator statements with literal actual clocks, zero-timeDirac, and measurable state/time dependence. A raw generic map-kernel existence wrapper alone is not sufficient advance.',
 'optional_not_required':'Transport actual84 continuous bounded outer convergence to the K-defined pointwise operator using the exact test identity; this is a derived compatibility result, not a second outer-continuity theorem. Can be omitted if no immediate consumer needs it.',
 'source_class':'Actual transition law and bounded-measurable transition tests are source-backed; all-finite jointly indexed kernel packaging is ASTIS measure-theoretic elaboration. Source Ex22 uses C_c; existing83/84 C_b extension remains explicitly attributed.',
 'exceptions':'Source E_(n+1) is ASTIS zeroindexed thresholds. Live T0=0 and R0=I retained; zero thresholds may give zero waits only on exceptional P-null inputs. Last live infinite wait is a genuine physical arc, no phase at infinity, stopped dummy is auxiliary only. Existing uncovered-z0 convention differs from source failed-limit0 but per-fixed-parameter AE laws coincide. No arbitrary correlated-clock substitution or uniform-parameter AE conclusion.'},
 'honest_readiness':'Dependency-ready at source/API level: actual parent provides joint Z/P/init; generic map/product APIs and integral_map already available and used by81. No proposed85 Lean/header/BODY was read or written; no compiler or proof credit.',
 'true_next_global_blocker':'Actual finite-jump path law expansion, absolute convergence on energy shells, reverse Borel change of variables and density/survival/jump-factor identity (A.1 p4.2-p5.3) are still needed for nu invariance. Kernel existence cannot discharge these. Restart/memorylessness/Chapman-Kolmogorov is a separate unproved source boundary.',
 'full_L2_boundary':'Bounded finite-probability outer DCT does not require invariance. Full L2(nu) requires actual invariance to make the pointwise operator AE-safe and Jensen-contractive, PLUS independent C_c density, then the bounded subclass limit. These are AND ingredients, not an optional density remark.',
 'excluded':['Actual process Markov/restart/time-homogeneity/semigroup or Chapman-Kolmogorov','True invariance/reversibility/path-space law/time-reversal proof','All-L2 contraction/density/strong continuity or generator-domain claims','Arbitrary correlated random initialization, uniform-parameter AE, adaptedness/strongMarkov','Ideal reference implemented sampler, mixing/hypocoercivity, cost, main theorem/composition/whole Goal completion'],
 'source_graph':graph_pin,'inventory':inventory_pin,'api_retrieval':api_pin,'independence':'Same independent source reader as84; primary-only85 notes fixed first. Prior proof/source verdicts, new85 candidate headers and implementation were not used. This is prospective extraction, not self-validation or independent review of a theorem.'}
rec_pin=put('candidate-recommendation85.json',recommendation)
seal=put('source-first-seal85.json',{'schema':'astis.source-only-freeze85.v1','closed_utc':now,'status':'CLOSED_SOURCE_ONLY_PROSPECTIVE','source_first_notes':pin(notes_path.relative_to(ROOT)),'original_source_first_created_utc':notes['created_utc'],'phase_order':['pinned primary/licensing read and independent source-first notes frozen','existing80/81/83/84 and generic APIs inspected plus bounded duplicate audit','separate prospective inventory/graph/recommendation frozen'],'inventory_items':len(inventory['items']),'nodes':len(nodes),'relations':len(edges),'dependency_edges':sum(e['dependency_edge'] for e in edges),'excluded_associations':sum(not e['dependency_edge'] for e in edges),'no_production_or_shared_writes':True,'no_statement_proof_or_verification_credit':True,'outputs':[api_pin,graph_pin,inventory_pin,rec_pin]})
outputs=[pin(p.relative_to(ROOT)) for p in sorted(OUT.iterdir()) if p.is_file()]
manifest={'schema':'astis.raw-manifest85.v1','status':'closed','raw_inputs':[pin(PRIMARY),*[pin(p) for p in apis]],'raw_outputs':outputs,'selfhash':'omitted to avoid circularity','boundary':'85 prospective source-only files only; no84 outputs, new Lean/header/proof, ledger/cell/production/site changes. Exact-byte hashes; JSON not canonicalized for these RAW pins.'}
mp=put('source-first-run-manifest85.json',manifest)
for p in manifest['raw_inputs']+manifest['raw_outputs']: assert pin(p['path'])==p
assert sha(notes_path.read_bytes())=='9e9e3737db6cc73e351ffe7daa8ad7dbb124e546f1378a25372ae0dab36fa1c1'
print(json.dumps({'status':'closed_source_only','inventory_items':len(inventory['items']),'nodes':len(nodes),'relations':len(edges),'recommendation':rec_pin,'seal':seal,'manifest':mp},ensure_ascii=False,indent=2))
