from pathlib import Path
import json, hashlib, datetime
from source_parse78 import SRC,OUT,raw,p
expected='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert hashlib.sha256(raw).hexdigest()==expected
inventory={
 'schema':'independent-source-only-freeze-v1','reviewer_role':'anti-anchored independent SOURCE reviewer','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'independence':{'candidate_seen':False,'prior_verdict_seen':False,'prior_source_graph_seen':False,'only_primary_source_and_task_read':True},
 'source':{'arxiv':'2609.06905v1','title':'Accelerated High-Accuracy Sampling from a Warm Start via the Proximal Bouncy Particle Sampler','authors':['Fan Chen','Sinho Chewi','Jianfeng Lu','Matthew S. Zhang'],'path':str(SRC),'sha256':expected,'license':'arXiv.org perpetual non-exclusive license','parsing':'stdlib html.parser; mathematical alttext preferred; no bs4; only paraphrased scoped inventory and minimal identifying formulas emitted'},
 'scope':{'included':['standing analytic assumptions S1.p1/S1.E1','reflection S2.E4','fixed-reference center/residual S3.E4','Algorithm 1 alg1 lines 1-8 and S3.E8/S3.E9','explicit harmonic flow S4.E5, A1.Ex2','A1.SS1.p1.1-p3.7 through jump-time nonaccumulation only','A1.E1/A1.E2 stopped integrated-hazard recursion','A1.Ex4-A1.Ex9 energy, deterministic cap, waiting-time and partial-sum lower bounds'], 'excluded':['the remainder of A1.SS1.p3.7 claiming unique all-time process and time-homogeneous Markov property','global path construction and measurability','stationarity, detailed balance, kernels and semigroup properties','hypocoercivity','gradient-query costs','actual-input composition with other sampling results','any completion claim for Proposition 3.1 or Algorithm 1']},
 'binders':[
 {'id':'B01','content':'Finite dimension d, Euclidean position/momentum/reference points in R^d; arbitrary fixed y, xtilde, x0, p0. Fixed-reference result does not require that xtilde or p0 be sampled.','anchors':['A1.SS1.p1.1','A1.SS1.p2.1','S3.Thmtheorem1.p1.1']},
 {'id':'B02','content':'Paper-wide V is C^2(R^d), with 0<alpha<=beta and alpha I<=Hessian V<=beta I. Appendix nonaccumulation uses the consequent beta-Lipschitz gradient. Strong convexity is standing context, not an extra dynamical recursion premise. A more general Lipschitz-gradient helper must be identified as such.','anchors':['S1.p1','S1.E1','A1.SS1.p3.3']},
 {'id':'B03','content':'eta>0; fixed center c=y-eta grad V(xtilde), finite initial phase-space point; energy E=H(x0,p0) is finite and nonnegative.','anchors':['S2.Thmtheorem2.p1.1','S3.E4','A1.Ex4']},
 {'id':'B04','content':'On a probability space, clocks E_j for j>=1 are independent identically distributed Exp(rate 1). They are a.s. strictly positive and finite, have finite first moment and mean 1; SLLN supplies sum_{j=1}^n E_j / n -> 1 a.s. These properties are ingredients derived from this law, not freely added public source assumptions.','anchors':['A1.SS1.p2.1','A1.SS1.p3.7']},
 {'id':'B05','content':'Initialize T0=0 and zeta0=(x0,p0); the step out of state n uses clock E_(n+1). The minimum convention is infimum over u>=0 of integrated hazard >= E_(n+1), with explicit empty-set stop.','anchors':['A1.SS1.p2.1','A1.E1','A1.E2','A1.SS1.p2.2']}
 ],
 'definitions':[
 {'id':'D01','name':'reflection','formula':'R_h=I-2 hh^T/||h||^2 for h!=0; R_0=I','semantic_boundary':'orthogonal norm-preserving involution; no momentum update ambiguity at h=0; rate then zero','anchors':['S2.E4','A1.Ex3','A1.SS1.p1.3']},
 {'id':'D02','name':'residual-center','formula':'h_xtilde(x)=grad V(x)-grad V(xtilde); c=y-eta grad V(xtilde)','anchors':['S3.E4']},
 {'id':'D03','name':'harmonic-flow','formula':'Phi_t(x,p)=(c+(x-c)cos(t)+sqrt(eta)p sin(t), -(x-c)sin(t)/sqrt(eta)+p cos(t))','semantic_boundary':'fixed same center throughout recursion and arbitrary segment time; Algorithm1 terminal pi is not a restriction on this nonaccumulation leaf','anchors':['A1.Ex2','S4.E5','S3.E8']},
 {'id':'D04','name':'bounce-rate','formula':'lambda_xtilde(x,p)=sqrt(eta)*max(p dot h_xtilde(x),0)','semantic_boundary':'actual integrated rate; no external clipped/surrogate clock; nonnegative and continuous along each fixed-state harmonic segment','anchors':['A1.Ex1','S3.E9','alg1.l6']},
 {'id':'D05','name':'actual-stopped-recursion','formula':'S_(n+1)=inf{u>=0 : integral_0^u lambda(Phi_s(zeta_Tn)) ds >= E_(n+1)}; if finite, T_(n+1)=T_n+S_(n+1) and zeta_T(n+1)=S_bounce(Phi_S(n+1)(zeta_Tn)); if set empty, S_(n+1)=T_(n+1)=infinity and stop','semantic_boundary':'State after bounce is needed, not just a real time sequence satisfying an assumed increment inequality. Extended infinity may be represented by Option, but stopping must not be silently converted into an arbitrary finite continuation.','anchors':['A1.E1','A1.E2','A1.SS1.p2.2']},
 {'id':'D06','name':'shifted-energy-cap','formula':'H(x,p)=(||x-c||^2/eta+||p||^2)/2; C=sqrt(eta)*beta*sqrt(2E)*(sqrt(2eta E)+||c-xtilde||)','semantic_boundary':'one finite deterministic C fixed by initial state, y and xtilde; C>=0; not a per-step arbitrary cap; no cap positivity blanket assumption','anchors':['A1.Ex4','A1.Ex6']}
 ],
 'source_conclusions':[
 {'id':'C01','content':'Flow and bounce preserve H, hence all recursively reached states and their flow segments satisfy ||p||<=sqrt(2E) and ||x-c||<=sqrt(2eta E).','anchors':['A1.SS1.p3.2','A1.Ex5']},
 {'id':'C02','content':'Actual rate is bounded by C throughout each produced segment, therefore integrated hazard <=C*u for every u>=0.','anchors':['A1.SS1.p3.3','A1.Ex6','A1.Ex7']},
 {'id':'C03','content':'If C=0, actual rate vanishes and there are no jumps on the a.s. positive clock event.','anchors':['A1.SS1.p3.5']},
 {'id':'C04','content':'If C>0, every finite wait S_(n+1) is >= E_(n+1)/C. A rigorous infimum proof must justify passage from all threshold-reaching u to infimum, or threshold attainment using continuity; neither is an extra public source hypothesis.','anchors':['A1.E1','A1.SS1.p3.5','A1.Ex8']},
 {'id':'C05','content':'If recursion continues forever, T_n>=sum_{j=1}^n E_j/C and T_n->infinity almost surely by SLLN (mean 1). Together with stopping/no-jump branch, finite jump times cannot accumulate.','anchors':['A1.SS1.p3.6','A1.Ex9','A1.SS1.p3.7']}
 ],
 'review_traps':[
 'A theorem assuming finite recursion waits lower-bounded by clocks is only a scalar interface unless actual recursion constructs these bounds internally.',
 'Continuing-path divergence is not stop-aware nonaccumulation unless finite-stop and zero-cap alternatives are carried explicitly.',
 'Source clocks begin at E1. For zero-indexed Lean clocks, need expose a relabel Elean(n)=Esource(n+1), including initial T0 and exact partial-sum index.',
 'Source route directly uses Exp1 mean and SLLN. Infinite frequent large clocks, Bernoulli counting, Borel-Cantelli or another sufficient condition can be mathematically valid alternative but require their own proof/admission and explicit source-route difference.',
 'Probability product independence, measurable events, IID law, a.s. positivity/finiteness and convergence cannot be smuggled as assumed entire desired path property.',
 'Uniform cap must come from actual initial energy invariance and the fixed residual gradient, not be a free public premise.',
 'Ex8 holds only finite waits with positive cap. Division by zero is not legitimate; no total-real infinity replacement is source equivalent.',
 'The leaf supplies nonaccumulation only; proof does not automatically certify global process construction, Markov property, stationarity, output kernel, query cost or full paper theorem.'
 ]
}
# Every source item in this exact bounded paragraph range is classified individually.
coverage=[]
for n in p.nodes:
 id=n.attrs.get('id','')
 if id and ((n.tag=='p' and (id.startswith('A1.SS1.p1.') or id.startswith('A1.SS1.p2.') or id.startswith('A1.SS1.p3.'))) or id in ['A1.E1','A1.E2','A1.Ex1','A1.Ex2','A1.Ex3','A1.Ex4','A1.Ex5','A1.Ex6','A1.Ex7','A1.Ex8','A1.Ex9']):
  classification='included-with-sentence-boundary' if id=='A1.SS1.p3.7' else 'included'
  coverage.append({'anchor':id,'classification':classification,'boundary':'Include SLLN and cannot-accumulate clause; exclude unique-global-process and Markov clauses.' if id=='A1.SS1.p3.7' else 'Entire scoped mathematical source item.'})
inventory['exhaustive_scoped_coverage']=coverage
nodes=[
 ('G01','Source definitions: reflection, fixed center/residual, flow and rate',['S2.E4','S3.E4','S3.E8','S3.E9','A1.Ex1','A1.Ex2','A1.Ex3']),
 ('G02','Actual iid Exp1 stopped integrated-hazard recursion; T0 and E_(n+1)',['A1.SS1.p2.1','A1.E1','A1.E2','A1.SS1.p2.2']),
 ('G03','Flow and bounce preserve fixed shifted energy',['A1.Ex4','A1.SS1.p3.2']),
 ('G04','Recursive energy-sublevel bounds',['A1.Ex5']),
 ('G05','Lipschitz residual plus Cauchy-Schwarz and triangle inequality produce actual global cap',['A1.SS1.p3.3','A1.Ex6']),
 ('G06','Integrate cap to bound accumulated hazard',['A1.Ex7']),
 ('G07','Zero cap implies no jumps/empty threshold set for positive clock',['A1.SS1.p3.5']),
 ('G08','Positive cap gives finite waiting-time lower bound from infimum threshold',['A1.Ex8','A1.E1']),
 ('G09','Initialize T0 and telescope finite recursive increments',['A1.E2','A1.Ex9']),
 ('G10','Exp1 has mean1 and finite first moment; IID strong law gives divergence of partial sums a.s.',['A1.SS1.p2.1','A1.SS1.p3.7']),
 ('G11','Continuing branch jump times diverge; finite stopping/no jumps prevent finite accumulation',['A1.SS1.p2.2','A1.SS1.p3.5','A1.Ex9','A1.SS1.p3.7'])
]
edges=[('G01','G03'),('G02','G04'),('G03','G04'),('G04','G05'),('G01','G05'),('G05','G06'),('G06','G07'),('G02','G07'),('G06','G08'),('G02','G08'),('G08','G09'),('G02','G09'),('G02','G10'),('G09','G11'),('G10','G11'),('G07','G11'),('G02','G11')]
graph={'schema':'independent-source-proof-graph-v1','no_implementation_or_prior_graph_input':True,'nodes':[{'id':i,'statement':t,'anchors':a} for i,t,a in nodes], 'edges':[{'ingredient':a,'consumer':b,'kind':'source-proof-ingredient'} for a,b in edges], 'notes':['Cauchy-Schwarz, triangle inequality and continuity/infimum mechanics expand the source compressed steps, and must not become new source theorem binders.','G10 records the SOURCE route, independently of any later candidate route.','No all-time path, Markov, invariance, kernel, cost or composition node admitted.']}
for name,obj in [('source_inventory78.json',inventory),('source_proof_graph78.json',graph)]:
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'source_freeze78.md').write_text('''# Independent source-only freeze 78

Pinned primary source SHA256: `'''+expected+'''`.

This inventory and source Proof Graph were authored before any candidate Lean, candidate exposition, reviewer packet, previous review, lesson, or prior source graph was opened. Scope is actual iid Exp(1) stopped integrated-hazard recursion and energy/cap/SLLN nonaccumulation, with the specified standing context. The final global-path and Markov clauses and all later results are explicitly excluded.

The full source-only contract is in source_inventory78.json. It individually classifies every paragraph and displayed equation of the selected Appendix A.1 opening/nonaccumulation argument, and preserves the zero-cap/no-jump branch, empty-set stop, arbitrary fixed initial state, T0=0, source clock index E_(n+1), positive-cap finite-wait division, direct mean-one SLLN route, and the distinction between a helper interface and actual-input nonaccumulation.

source_proof_graph78.json independently records 11 nodes and their source proof ingredient edges. Mathematical derivations omitted by source compression must be proved internally, not introduced as new public assumptions.

Source license is the arXiv.org perpetual non-exclusive license. No full-source duplicate or long raw quotation is emitted. These are private run artifacts with a paraphrased inventory and minimal mathematical identifying formulas.

This freeze is immutable by protocol: later comparison belongs in distinct files and must reference the seal, never rewrite this source-only contract.
''',encoding='utf-8')
seal={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pinned_primary_sha256':expected,'frozen_before_candidate_access':True,'files':{name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in ['source_parse78.py','source_inventory78.json','source_proof_graph78.json','source_freeze78.md']}}
(OUT/'source_freeze78.seal.json').write_text(json.dumps(seal,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frozen':True,'coverage_items':len(coverage),'graph_nodes':len(nodes),'seal':str(OUT/'source_freeze78.seal.json'),'files':seal['files']},indent=2))
