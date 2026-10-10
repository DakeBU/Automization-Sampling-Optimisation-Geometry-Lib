from pathlib import Path
import json,hashlib,datetime
from fresh_primary79 import parsed,SRC,OUT,raw
sha=lambda b:hashlib.sha256(b).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sourcehash='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert sha(raw)==sourcehash
coverage=[
 {'anchor':'S1.p1/S1.E1','classification':'NODE','role':'C2 potential and 0<alpha<=beta Hessian sandwich standing context'},
 {'anchor':'S2.SS2.p1.1','classification':'NODE','role':'Standing eta in (0,1/beta]'},
 {'anchor':'S2.E4','classification':'NODE','role':'Specular reflection and R0=I'},
 {'anchor':'S3.E4','classification':'NODE','role':'Fixed center c and residual gradient'},
 {'anchor':'alg1.l1/alg1.l4','classification':'NODE','role':'Input and initial position'},
 {'anchor':'alg1.l2','classification':'EXCLUDED','reason':'Random reference/momentum law is not needed for arbitrary fixed-reference interval coverage; iid event clocks remain in scope.'},
 {'anchor':'alg1.l3','classification':'EXCLUDED','reason':'Gradient query execution/cost is not this theorem edge.'},
 {'anchor':'alg1.l5/S3.E8','classification':'NODE','role':'Literal harmonic deterministic arcs; terminal pi is an application, interval-cover quantifies any finite t.'},
 {'anchor':'alg1.l6/S3.E9','classification':'NODE','role':'Literal actual integrated rate'},
 {'anchor':'alg1.l7','classification':'NODE','role':'Postbounce phase belongs to next left endpoint'},
 {'anchor':'alg1.l8','classification':'EXCLUDED','reason':'Returning x_pi as a measurable random output/kernel is later process/output work.'},
 {'anchor':'A1.SS1.p1.1','classification':'NODE','role':'Arbitrary fixed y and xtilde plus rate identity'},
 {'anchor':'A1.Ex1','classification':'NODE','role':'Actual nonnegative residual bounce rate'},
 {'anchor':'A1.SS1.p1.2','classification':'NODE','role':'Explicit harmonic flow/bounce definitions'},
 {'anchor':'A1.Ex2','classification':'NODE','role':'Literal harmonic flow Phi, including Phi0=id'},
 {'anchor':'A1.Ex3','classification':'NODE','role':'Bounce S and zero-residual convention'},
 {'anchor':'A1.SS1.p1.3','classification':'NODE','role':'Involution/vanishing rate at zero residual remove bounce ambiguity; do not assume bounce continuity.'},
 {'anchor':'A1.SS1.p2.1','classification':'NODE','role':'iid Exp1 clocks; initial phase and T0=0; E_(n+1) indexing'},
 {'anchor':'A1.E1','classification':'NODE','role':'Actual integrated-hazard infimum waiting time'},
 {'anchor':'A1.E2','classification':'NODE','role':'Finite recurrence time addition and postbounce phase'},
 {'anchor':'A1.SS1.p2.2:first sentence','classification':'NODE','role':'Finite-wait qualifier; no phase update at infinity'},
 {'anchor':'A1.SS1.p2.2:empty-set sentence','classification':'NODE','role':'Stop recursion and assign next time/wait infinity'},
 {'anchor':'A1.SS1.p2.2:between-jumps sentence','classification':'NODE','role':'Half-open arc formula for 0<=duration<S_(n+1); includes full finite tail if S_(n+1)=infinity'},
 {'anchor':'A1.SS1.p3.1-p3.6/A1.Ex4-Ex9','classification':'NODE-AS-ESTABLISHED-PARENT-BOUNDARY','role':'Energy/cap/waiting lower bounds and stopping split produce finite-time nonaccumulation; not a new energy proof target in this edge.'},
 {'anchor':'A1.SS1.p3.7:SLLN/nonaccumulation clauses','classification':'NODE','role':'All finite horizons are eventually exceeded by times or a stopped infinity; reusable nonaccumulation parent, with original author direct SLLN distinct from any declared OR-route.'},
 {'anchor':'A1.SS1.p3.7:unique-process-for-all-times clause','classification':'NODE-PARTIAL-BRIDGE','role':'Unique half-open interval/live record is a necessary source-compressed coverage bridge; it is not the whole unique stochastic-process assertion.'},
 {'anchor':'A1.SS1.p3.7:memoryless/Markov/Davis citation clauses','classification':'EXCLUDED','reason':'Memoryless Markov/process construction package is outside finite physical-time interval selection.'},
 {'anchor':'A1.SS1.p4 onward','classification':'EXCLUDED','reason':'Stationarity, adjoints, kernels, path law, semigroup and later invariance analysis are outside the bounded edge.'}
]
inv={
 'schema':'independent-source-only-freeze-v1','reviewer':'/root/fresh_source78 acting on edge79','created_utc':now,
 'independence':{'primary_read_first_this_turn':True,'fresh_stdlib_parser_not_prior_extractor':True,'candidate_header_seen':False,'candidate_implementation_seen':False,'prior79_reviews_seen':False,'prior_graphs_audits_or_lessons_seen_this_turn':False,'scope_reconstructed_from_primary':True},
 'source':{'arxiv':'2609.06905v1','authors':['Fan Chen','Sinho Chewi','Jianfeng Lu','Matthew S. Zhang'],'path':str(SRC),'raw_sha256':sourcehash,'license':'arXiv.org perpetual non-exclusive license','dissemination':'Private scoped paraphrase and minimal formulas; no new full-source duplicate.'},
 'target_boundary':'For each fixed reference/initial phase, almost surely every finite physical time belongs to exactly one half-open interval [T_n,T_(n+1)) whose nth record is live with finite time and genuine postbounce phase, including the infinite-duration final live arc before absorbing stopped records. This is a source-compressed physical-time interval-cover leaf, not a measurable global process.',
 'binders':[
 {'id':'B79-analytic','classification':'STANDING','statement':'Finite-dimensional real Euclidean source space, V in C2, 0<alpha<=beta, alpha I<=Hessian V<=beta I, eta in (0,1/beta]; coordinate-free finite-dimensional formulation can be an explicit intrinsic elaboration; no higher derivative assumption.','anchors':['S1.p1','S1.E1','S2.SS2.p1.1']},
 {'id':'B79-fixed','classification':'SOURCE','statement':'Arbitrary fixed y,xtilde and initial phase z0=(x0,p0). No sampled-reference/momentum law needed to prove the fixed-reference coverage statement.','anchors':['A1.SS1.p1.1','A1.SS1.p2.1']},
 {'id':'B79-input','classification':'SOURCE','statement':'Independent Exp(rate1) clocks E_j for j>=1. Strict positivity/finiteness hold on a single countable full-measure event. A canonical product is a literal realization, not a supplied positivity/nonaccumulation certificate.','anchors':['A1.SS1.p2.1']},
 {'id':'B79-time','classification':'TYPING','statement':'Physical t is finite and nonnegative; event/waiting times may be infinity. The intended theorem quantifies all finite horizons on a common good-clock event after fixing y,xtilde,z0. It does not require an uncountable intersection over all reference triples.','anchors':['A1.SS1.p2.2','A1.SS1.p3.7']}
 ],
 'literal_definitions':[
 {'name':'center/residual','formula':'c=y-eta grad V(xtilde); h(x)=grad V(x)-grad V(xtilde)','anchors':['S3.E4']},
 {'name':'flow/bounce/rate','formula':'Phi_u(x,p)=(c+(x-c)cos u+sqrt(eta)p sin u,-(x-c)sin u/sqrt(eta)+p cos u); S(x,p)=(x,R_h(x)p); R0=I; lambda=sqrt(eta) max(0,p dot h(x))','anchors':['A1.Ex1','A1.Ex2','A1.Ex3','S2.E4']},
 {'name':'clock','formula':'S_(n+1)=inf{u>=0: integral_0^u lambda(Phi_s(zeta_Tn))ds >= E_(n+1)}; empty hit set gives infinity','anchors':['A1.E1','A1.SS1.p2.2']},
 {'name':'initial/live recurrence','formula':'T0=0; zeta0=z0; for finite S_(n+1), T_(n+1)=T_n+S_(n+1), zeta_T(n+1)=S(Phi_S(n+1)(zeta_Tn))','anchors':['A1.SS1.p2.1','A1.E2']},
 {'name':'stopped records','formula':'If hit set empty then next event time/wait are infinity and no phase at infinity is assigned. The last finite active phase continues along Phi_u for every finite u>=0. Absorbing no-phase record is an explicit total encoding.','anchors':['A1.SS1.p2.2']},
 {'name':'half-open physical arc','formula':'zeta_(T_n+u)=Phi_u(zeta_Tn), 0<=u<S_(n+1); equivalently T_n<=t<T_(n+1), u=t-T_n, for a live finite T_n','anchors':['A1.SS1.p2.2','A1.E2']}
 ],
 'required_source_compressed_bridges':[
 {'id':'BR79-positive-clock','statement':'Actual hazard begins at0 and is continuous; positive thresholds imply strictly positive waiting times (possibly infinity). Consequently every finite transition increases time. Derive it; do not add it as a new public source premise.','anchors':['A1.E1','A1.SS1.p2.1']},
 {'id':'BR79-order-stop','statement':'Event times are monotone from T0=0, stopped times are infinity and absorbing, and finite event time identifies an active/live record with its phase.','anchors':['A1.E2','A1.SS1.p2.2']},
 {'id':'BR79-exists-index','statement':'For each finite t, nonaccumulation gives finitely many indices with T_n<=t; T0=0 makes this set nonempty. Its greatest index n satisfies T_n<=t<T_(n+1). An equivalent least-crossing-index route must handle n0/successor carefully.','anchors':['A1.SS1.p3.7','A1.SS1.p2.1','A1.SS1.p2.2']},
 {'id':'BR79-unique-index','statement':'Two indices satisfying the half-open interval inequalities cannot differ: monotonicity would put the later left endpoint at or beyond the earlier right endpoint. Uniqueness is interval uniqueness, not uniqueness in law or strong-solution uniqueness.','anchors':['A1.E2','A1.SS1.p2.2','A1.SS1.p3.7']},
 {'id':'BR79-arc-duration','statement':'If nth record is (T_n,z), t in its interval implies u=t-T_n>=0 and finite. If next event is finite, u<S_(n+1) by A.2; if it stops, S_(n+1)=infinity and every finite u is allowed.','anchors':['A1.E2','A1.SS1.p2.2']},
 {'id':'BR79-endpoints','statement':'At t0 use initial live record0; Phi0(z0)=z0. At a finite jump t=T_(n+1), previous interval excludes that time and next interval includes the postbounce phase from A.2. No bounce/state is created at infinity.','anchors':['A1.Ex2','A1.E2','A1.SS1.p2.2']}
 ],
 'source_vs_implementation_graph_rule':'These bridges reconstruct the compressed source interval-coverage reasoning before candidate access. The eventual Lean graph may use existing compiled parents and a different finite-order selector proof, but each bridge and source branch must remain covered; a public hypothesis assuming the desired cover is not acceptable.',
 'critical_distinctions':[
 'Stopped recursion is not cessation of physical deterministic evolution: the final finite live arc has infinite waiting duration.',
 'The unique interval index and its live phase do not by themselves provide a measurable random index selector, jointly measurable physical-time path, or time-homogeneous Markov process.',
 'A theorem covering finite horizons with event times alone must still link the selected finite time to the actual live record/phase before it supports the between-jump arc formula.',
 'Half-open convention is left-inclusive/right-exclusive, including t=0 and assigning a finite jump endpoint to the postbounce next record.',
 'A source-positive Exp clock family excludes deterministic zero-threshold repeated-time artifacts only almost surely. A total zero-threshold extension must not be confused with the source input event.',
 'Nonaccumulation is an established ingredient edge, not a new public assumption or a new proof of all global properties.',
 'No source completion badge follows from an interval cover, a unique index, or a defined pointwise phase.'
 ],
 'excluded_claims':['measurable physical-time index selector','jointly measurable/global process construction and uniqueness','cadlag/right-continuous path theorem beyond endpoint convention','time-homogeneous Markov/memoryless theorem','stationarity/invariance/detailed balance/semigroup/kernel/hypocoercivity','return-law/gradient-query/expected cost/implementation error','full PBPS theorem or PBPS-SPHMC actual-input composition','independent Lean verification/PROVED_LOCAL/VERIFIED/merged/purified/Goal credit'],
 'exhaustive_scoped_coverage':coverage
}
nodes=[
 ('G79-1','Standing source context and literal flow/bounce/rate',['S1.E1','S2.SS2.p1.1','S2.E4','S3.E4','A1.Ex1-3']),
 ('G79-2','Actual iid Exp1 clocks and a.s. positive thresholds',['A1.SS1.p2.1']),
 ('G79-3','Initialize live record0 with finite T0=0',['A1.SS1.p2.1']),
 ('G79-4','Actual integrated-hazard wait and finite postbounce recurrence',['A1.E1','A1.E2']),
 ('G79-5','Empty hit set yields infinity/stop; no phase at infinity',['A1.SS1.p2.2']),
 ('G79-6','Monotone event times, strict finite transitions, absorbing stops and finite-time/live-record identification',['A1.E1','A1.E2','A1.SS1.p2.2']),
 ('G79-7','Nonaccumulation supplies finite bounded-horizon event-index sets',['A1.Ex9','A1.SS1.p3.7']),
 ('G79-8','Nonempty finite index set has greatest n; its right neighbor exceeds t',['A1.SS1.p2.1','A1.SS1.p3.7']),
 ('G79-9','Unique half-open interval and genuine nth live finite record',['A1.E2','A1.SS1.p2.2']),
 ('G79-10','Finite physical duration t-T_n lies in source allowed arc; stopped next record permits all finite durations',['A1.E2','A1.SS1.p2.2']),
 ('G79-11','Initial endpoint and finite-jump endpoint use Phi0 and postbounce next record',['A1.Ex2','A1.E2','A1.SS1.p2.2'])
]
edges=[(1,4),(2,6),(3,6),(4,6),(5,6),(2,7),(4,7),(5,7),(6,7),(3,8),(7,8),(6,9),(8,9),(4,10),(5,10),(9,10),(1,11),(3,11),(4,11),(9,11)]
graph={'schema':'independent-source-proof-graph-v1','created_before_candidate':True,'source_raw_sha256':sourcehash,'target':'Physical-time unique active half-open interval cover only','nodes':[{'id':a,'statement':b,'anchors':c} for a,b,c in nodes],'edges':[{'ingredient':f'G79-{a}','consumer':f'G79-{b}','kind':'source-proof-ingredient'} for a,b in edges],'compressed_source_expansion':'G79-8..11 expand the source between-jump/unique-for-all-t sentence as bounded interval and endpoint obligations. These are not quotations and do not certify the global stochastic-process claim.','not_lean_dependency_claim':True,'possible_routes':['greatest element of nonempty finite event-time sublevel indices','least crossing index with initialization predecessor case'], 'original_stochastic_route_boundary':'Source nonaccumulation uses direct Exp mean-one SLLN; an already compiled explicit sufficient alternative may supply the nonaccumulation parent without changing the source graph identity.'}
for filename,obj in [('source_inventory79.json',inv),('source_proof_graph79.json',graph)]:
 (OUT/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'source_freeze79.md').write_text('''# Edge79 independent source-first freeze

Pinned primary arXiv2609.06905v1 raw SHA256: `'''+sourcehash+'''`.

This turn inspected the pinned primary first and used a fresh stdlib html.parser. No edge79 prospective header, implementation, prior review, prior source extractor or prior source graph was opened. The independent source inventory and 11-node, 20-edge Proof Graph were frozen before candidate access.

The bounded obligation is unique coverage of every finite physical time by a genuine finite live record's half-open event interval. The last live arc remains defined for all finite durations when its next waiting time is infinity; stopped records carry no phase at infinity. T0, positive thresholds, source E_(n+1) indexing, left-inclusive/right-exclusive endpoint ownership, and postbounce phase are explicit.

A unique interval and live record are distinct from a measurable selector or global stochastic process. The source sentence asserting a unique process for all times is admitted only as the bounded interval-cover bridge, with Markov/invariance/semigroup/kernel/cost/composition and full-paper claims excluded. Direct source mean-one SLLN remains a distinct route within the reused nonaccumulation ingredient.

Do not rewrite this freeze after candidate access. Later review must use separate packet-bound files and reference this seal. No public source duplication, production/cell/ledger write, verification transition or completion credit is conferred.
''',encoding='utf-8')
files=['fresh_primary79.py','freeze_source79.py','source_inventory79.json','source_proof_graph79.json','source_freeze79.md']
seal={'schema':'immutable-source-first-seal-v1','created_utc':now,'primary_raw_sha256':sourcehash,'candidate_access_before_freeze':False,'self_hash_not_included':True,'files':{n:sha((OUT/n).read_bytes()) for n in files}}
(OUT/'source_freeze79.seal.json').write_text(json.dumps(seal,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'ready':True,'source_inventory_coverage_items':len(coverage),'source_graph_nodes':len(nodes),'source_graph_edges':len(edges),'seal':str(OUT/'source_freeze79.seal.json'),'seal_raw_sha256':sha((OUT/'source_freeze79.seal.json').read_bytes())},indent=2))
