from pathlib import Path
import json,hashlib,datetime
from primary_only80 import SRC,OUT,source,raw
sha=lambda b:hashlib.sha256(b).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
pinned='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert sha(raw)==pinned
scope={
 'primary_included':['Algorithm1 literal actual dynamics and initialization','AppendixA.1 opening actual flow/bounce/rate definitions','A.1/A.2 integrated-hazard finite postbounce recurrence and empty-set stopping','A1.SS1.p2.2 actual half-open between-jump phase formula','A1.SS1.p3.1-p3.7 nonaccumulation ingredient and source-compressed existence as a process','Standing C2/Hessian/eta source context','Only the Borel-bounce/affine-flow/finite-composition facts in later primary A1.SS1.SSS0.Px1.p4.4 as necessary background'],
 'bounded_target':'Measurable realization of the actual fixed-reference finite-physical-time phase from the actual iid clocks and stopped recursion, plus source initialization. A measurable interval selector and finite live elapsed duration are internal ingredients. The exact final signature is not known or read at this stage.',
 'source_explicit_vs_implicit':'Literal recurrence, half-open phase formula and initial phase are SOURCE_EXPLICIT. Borel stochastic realization and measurable countable interval selection are SOURCE_COMPRESSED_OBLIGATIONS, not explicit standalone source theorems. Joint measurability in time, sample and parameters is a useful possible ASTIS elaboration stronger than merely asserting each fixed-time coordinate is a random variable; any such claim must be labelled and proved at its exact domain.',
 'excluded':['Full Algorithm1 including random reference/momentum initialization and returned sample law','Path regularity/cadlag/global pathwise uniqueness beyond deterministic interval agreement','Strong/weak solution notions, filtration/adaptedness/stopping-time claims','Memoryless/time-homogeneous Markov/strong Markov','Stationarity/invariance/reversibility/kernel/semigroup/hypocoercivity','Numerical implementation errors or gradient/query/expected costs','Full PBPS theorem/PBPS-SPHMC composition/full Goal completion','Any implementation/source-review/VERIFIED/merge/purification credit from this preread']
}
roles={
 'A1.SS1.p1.1':'SOURCE_EXPLICIT fixed y,xtilde and actual rate identity.',
 'A1.Ex1':'SOURCE_EXPLICIT actual nonnegative rate, not a clipped surrogate.',
 'A1.SS1.p1.2':'SOURCE_EXPLICIT actual harmonic flow/bounce definitions.',
 'A1.Ex2':'SOURCE_EXPLICIT continuous harmonic flow including Phi0=id and finite real duration.',
 'A1.Ex3':'SOURCE_EXPLICIT phase bounce and R0=I.',
 'A1.SS1.p1.3':'SOURCE_EXPLICIT possible bounce discontinuity; only Borel measurability may be derived, not blanket continuity. Rate vanishes when residual0.',
 'A1.SS1.p2.1':'SOURCE_EXPLICIT iid Exp1 clocks, zeta0=z0,T0=0,index j>=1. Random variables entail measurable clocks; source E_(n+1) drives step n.',
 'A1.E1':'SOURCE_EXPLICIT integrated-hazard threshold infimum; parameter-measurability must be derived, not assumed.',
 'A1.E2':'SOURCE_EXPLICIT finite time increment and postbounce phase update. No update at infinity.',
 'A1.SS1.p2.2':'MIXED_EXPLICIT three source branches: finite-wait qualification; empty-hit-set infinity/stop; half-open arc formula 0<=u<S_(n+1), including final infinite-duration live arc.',
 'A1.SS1.p3.1':'SOURCE_PARENT energy argument introduced to ensure nonaccumulation; not new independent measurability theorem.',
 'A1.Ex4':'SOURCE_PARENT shifted energy literal formula.',
 'A1.SS1.p3.2':'SOURCE_PARENT flow/bounce invariance gives layer bounds.',
 'A1.Ex5':'SOURCE_PARENT finite layer norm bounds.',
 'A1.SS1.p3.3':'SOURCE_PARENT gradient Lipschitz gives deterministic layer cap.',
 'A1.Ex6':'SOURCE_PARENT exact finite deterministic cap; not a new source binder.',
 'A1.SS1.p3.4':'SOURCE_PARENT integral bound consequence.',
 'A1.Ex7':'SOURCE_PARENT accumulated hazard bounded by cap*time.',
 'A1.SS1.p3.5':'SOURCE_PARENT zero cap no jumps versus positive-cap finite wait lower bound.',
 'A1.Ex8':'SOURCE_PARENT finite waits >=clock/cap only positive-cap branch.',
 'A1.SS1.p3.6':'SOURCE_PARENT continuing recursion conditional branch.',
 'A1.Ex9':'SOURCE_PARENT event times lower-bound sums and diverge when recursion continues.',
 'A1.SS1.p3.7':'MIXED_SCOPE: source SLLN/nonaccumulation is parent; measurable process realization is a bounded SOURCE_COMPRESSED obligation inside the unique-process assertion; memoryless/Markov/Davis package is EXCLUDED.'
}
coverage=[]
for n in source.elements:
 ident=n.attrs.get('id','')
 if ident in roles and n.tag in ('p','table','tbody'):coverage.append({'anchor':ident,'classification':'NODE' if not roles[ident].startswith('MIXED') else 'NODE_AND_EXCLUDED_BY_CLAUSE','source_role':roles[ident]})
assert len(coverage)==23
coverage += [
 {'anchor':'license-tr','classification':'PROVENANCE','source_role':'arXiv.org perpetual non-exclusive license; no full rawsource reproduction in new artifacts.'},
 {'anchor':'S1.p1/S1.E1','classification':'NODE_STANDING','source_role':'C2 V; 0<alpha<=beta; source Hessian sandwich.'},
 {'anchor':'S2.SS2.p1.1','classification':'NODE_STANDING','source_role':'eta in (0,1/beta], equivalent to eta>0,beta*eta<=1 given beta>0.'},
 {'anchor':'S2.E4','classification':'NODE','source_role':'Literal reflection and R0=I; Borel piecewise expression without continuity at h0.'},
 {'anchor':'S3.E4','classification':'NODE','source_role':'Fixed center c and gradient residual h; continuous in source parameters under C2.'},
 {'anchor':'alg1.l1','classification':'NODE','source_role':'Actual deterministic input state.'},
 {'anchor':'alg1.l2','classification':'EXCLUDED','reason':'Random conditional-reference and Gaussian-momentum laws are outside fixed-reference/fixed-phase realization; iid event clocks remain included.'},
 {'anchor':'alg1.l3','classification':'EXCLUDED','reason':'Gradient caching/query action and costs are not this measurability edge.'},
 {'anchor':'alg1.l4','classification':'NODE','source_role':'Source position initialization x0=x; full initial phase is Appendix zeta0=(x0,p0).'},
 {'anchor':'alg1.l5/S3.E8','classification':'NODE','source_role':'Literal harmonic ODE and physical evolution; pi is an application horizon, not a restriction on finite-time construction.'},
 {'anchor':'alg1.l6/S3.E9','classification':'NODE','source_role':'Actual residual-gradient bounce rate.'},
 {'anchor':'alg1.l7','classification':'NODE','source_role':'Finite event endpoint owns the postbounce phase.'},
 {'anchor':'alg1.l8','classification':'EXCLUDED','reason':'A returned x_pi sample law/full algorithm contract is not yet admitted; coordinate evaluation could be a later explicitly proved consequence.'},
 {'anchor':'S3.Thmtheorem1.p1.1:defines-unique-process clause','classification':'NODE_PARTIAL_ONLY','source_role':'Measurable actual phase realization and initialization are necessary bounded pieces; do not close unique global Markov process assertion.'},
 {'anchor':'S3.Thmtheorem1.p1.1:Markov/stationary/returned-output clauses','classification':'EXCLUDED','reason':'Markov, invariant law and actual output-law claims need separate source/Lean evidence.'},
 {'anchor':'A1.SS1.SSS0.Px1.p4.4:Borel-composition clauses','classification':'NODE_NECESSARY_BACKGROUND_ONLY','source_role':'Source calls bounce a Borel involution and harmonic flows affine; finite prescribed compositions Borel. This supports Borel regularity only, not stationarity or random-time selector automatically.'},
 {'anchor':'A1.SS1.SSS0.Px1.p4.4:measure-preserving/inverse/time-reversal/Jacobian clauses','classification':'EXCLUDED','reason':'Measure preservation and path reversal are invariance proof ingredients, not required to establish mere phase measurability.'},
 {'anchor':'AppendixA.1 later invariance/operator/kernel proofs beyond the selected Borel clauses','classification':'EXCLUDED','reason':'Outside bounded phase measurability/initialization target.'}
]
inv={
 'schema':'independent-source-first-preread-v1','reviewer':'/root/fresh_source78 for successor80','created_utc':now,
 'independence':{'primary_read_first_this_phase':True,'fresh_stdlib_html_parser':True,'candidate80_header_seen':False,'candidate80_implementation_seen':False,'candidate80_statement_or_lesson_seen':False,'other80_preread_capsule_review_extractor_seen':False,'only_pinned_primary_and_task_scope_hint_read':True,'no_prior_result_or_source_graph_reused_as80_topology':True},
 'source':{'arxiv':'2609.06905v1','authors':['Fan Chen','Sinho Chewi','Jianfeng Lu','Matthew S. Zhang'],'pinned_local_raw_path':str(SRC),'raw_sha256':pinned,'license':'arXiv.org perpetual non-exclusive license','parsing':'Fresh stdlib html.parser, math alttext; no prior extractor imported','output_policy':'Private paraphrased source inventory/minimal identifying formulas only; no new full source duplicate.'},
 'scope':scope,
 'binder_inventory':[
 {'id':'B80-1','class':'STANDING','content':'Finite-dimensional Euclidean source space R^d with Borel structure; V in C2 and source Hessian sandwich 0<alpha<=beta. An intrinsic finite-dimensional real inner-product version can be explicit generalization; no new higher derivative assumption.'},
 {'id':'B80-2','class':'STANDING','content':'eta in (0,1/beta]; exact fixed center c=y-eta grad V(xtilde) and residual gradV(x)-gradV(xtilde).'},
 {'id':'B80-3','class':'SOURCE','content':'Arbitrary fixed y,xtilde,z0=(x0,p0). Source fixed-reference realization does not require random reference or Gaussian initial-momentum law.'},
 {'id':'B80-4','class':'SOURCE','content':'iid Exp(rate1) random clocks E_j,j>=1, with step n using E_(n+1). A canonical product R^N and NNReal clamps are possible ASTIS realizations; clamp/raw equality and all-coordinate positivity must be derived a.s.'},
 {'id':'B80-5','class':'TYPING','content':'Physical t and selected record stored time are finite nonnegative reals. Event/wait times may be infinity; no phase, flow or elapsed subtraction at infinity.'},
 {'id':'B80-6','class':'RULED','content':'Do not add supplied measurable-selector/global-phase/initialization/nonaccumulation/continuity-bounce certificates as source-facing public hypotheses. They are internal ingredient edges or remain named obligations.'}
 ],
 'definition_audit_before_candidate':[
 {'name':'actual recursion','source_formula':'T0=0,zeta0=z0; S_(n+1)=inf{u>=0:integral_0^u lambda(Phi_s(zeta_Tn))ds>=E_(n+1)}; finite next phase=S_bounce(Phi_S(n+1)(zeta_Tn)); empty hit set stops next event at infinity.','status':'SOURCE_LITERAL','failure_boundary':'A finite-wait record cannot be fabricated from a default extraction of infinity. Stopped records have no phase.'},
 {'name':'physical phase','source_formula':'zeta_(T_n+u)=Phi_u(zeta_Tn) for 0<=u<S_(n+1).','status':'SOURCE_LITERAL_ON_VALID_LIVE_ARCS','failure_boundary':'Any total extension on invalid/accumulating/zero-clock raw inputs is ASTIS semantics, not the source physical path. Must identify its domain and prove source agreement a.s.'},
 {'name':'interval selector','source_formula':'Select the unique n with T_n<=t<T_(n+1) on a valid nonaccumulating sample.','status':'SOURCE_COMPRESSED_ADAPTER_REQUIRED','failure_boundary':'Classical unique existence alone does not prove the selected index measurable. Countable interval events or an equivalent measurable search construction must be checked.'},
 {'name':'elapsed duration','source_formula':'u=t-T_n>=0, finite, with u<S_(n+1).','status':'SOURCE_LITERAL_DURATION','failure_boundary':'NNReal tsub agrees only after stored_time<=t; extended infinity subtraction is prohibited.'},
 {'name':'initialization','source_formula':'At physical t=0, zeta_0=z0; source positive first clock gives T1>0 or infinity so interval0 is selected and Phi0(z0)=z0.','status':'SOURCE_EXPLICIT_INITIAL_VALUE_WITH_COMPRESSED_SELECTOR_BRIDGE','failure_boundary':'record0 initialization alone is not the physical-time phase initialization theorem. If a total extension claims initialization for every raw sample, justify zero-clock/fallback branches separately.'}
 ],
 'required_mathematical_obligations_not_proofs':[
 {'id':'O80-clock-meas','content':'Establish measurability of source input coordinates and actual integrated-hazard waiting map, including empty-hit infinity. A proof may use nonnegative continuous hazard and the exact finite sublevel identity {tau<=t}={e<=Lambda(t)}; continuity/attainment must be internal, not new source premises.'},
 {'id':'O80-record-meas','content':'Derive each finite-step guarded active/stopped record and event time measurable; actual bounce need only be Borel, and the top/non-top branch plus finite extraction must be measurable.'},
 {'id':'O80-cover','content':'Use actual source nonaccumulation and initialized monotone clocks to establish the unique live half-open cover for every finite physical t on the source good-input event. Last live arc remains for infinite next wait.'},
 {'id':'O80-selector-meas','content':'Prove relevant joint or fixed-time selector measurable using countable index events T_n<=t<T_(n+1) or first crossing. State exact parameter/sample/time domain; no assumption that uncountable a.e. intersections are available.'},
 {'id':'O80-evaluate','content':'Compose selected actual live phase with actual flow at the finite nonnegative elapsed time; ensure countable selection remains Borel/measurable and source half-open arc agreement holds simultaneously for all finite t on the good event.'},
 {'id':'O80-init','content':'Join source a.s. all-coordinate positivity, actual positive-threshold first hit and Phi0=id to obtain physical-time initialization, not only finite-record0 initialization. Keep every-input totalization initialization distinct from source a.s. initialization.'},
 {'id':'O80-tail','content':'Infinite next wait permits all later finite elapsed durations from last live state. Never evaluate infinity or assign a phase to stopped next record.'},
 {'id':'O80-null-extension','content':'If the implementation defines an everywhere phase/selector, provide explicit measurable off-good behavior and prove that it alters no source-valid sample path. Alternative: work on an explicitly measurable full-measure valid domain. Defaults on unproved-good inputs cannot stand in for source process construction.'}
 ],
 'admissible_signature_distinctions':[
 'For every fixed y,xtilde,z0, each physical-time coordinate is measurable in the actual clock sample; this is a minimum stochastic-process realization piece.',
 'Joint measurability in finite physical time and sample, and possibly parameters, is a possible stronger ASTIS elaboration; review separately against actual theorem quantifiers/domains.',
 'Source agreement for all finite t on one a.s. event per fixed parameter triple differs from separately a.e. equality at each t.',
 'A global measurable map on all parameter triples can coexist with only pointwise-in-triple a.s. source agreement. Do not assert one shared full-measure event for every uncountable triple without proof.',
 'Conditional/Gaussian reference and initial-phase sampling, adaptedness, process law, transition kernel, Markov and invariance are not automatically certified by a measurable phase map.'
 ],
 'source_scope_coverage':coverage,
 'preread_status':'FROZEN_SOURCE_ONLY_NO_CANDIDATE_NO_LEAN_PROOF_NO_REVIEW_VERDICT'
}
nodes=[
 ('G80-01','Standing analytic/Borel context and literal center/gradient/rate/flow/bounce',['S1.p1/S1.E1','S2.SS2.p1.1','S2.E4','S3.E4','A1.Ex1-3']),
 ('G80-02','Actual measurable iid Exp1 clocks; common a.s. positive finite input event',['A1.SS1.p2.1']),
 ('G80-03','Actual integrated-hazard waiting map, empty-set infinity and parameter measurability',['A1.E1','A1.SS1.p2.2']),
 ('G80-04','Measurable literal finite guarded postbounce records/event times; no phase at infinity',['A1.E2','A1.SS1.p2.2','A1.SS1.SSS0.Px1.p4.4:Borel only']),
 ('G80-05','Initialized monotone actual event times and source finite-positive waits',['A1.SS1.p2.1','A1.E1','A1.E2']),
 ('G80-06','Actual source nonaccumulation covers all finite horizons or final stopped tail',['A1.Ex4-9','A1.SS1.p3.7:nonaccumulation']),
 ('G80-07','Unique half-open finite physical-time interval with actual live record and finite elapsed',['A1.E2','A1.SS1.p2.2']),
 ('G80-08','Countable Borel interval events and measurable index/live-record selection',['A1.SS1.p2.2','A1.SS1.p3.7:process construction compressed']),
 ('G80-09','Explicit measurable valid-domain restriction or off-good total extension',['A1.SS1.p3.7:a.s. qualifier','ASTIS necessary realization adapter, not direct source quotation']),
 ('G80-10','Measurable actual physical phase via selected finite elapsed flow; agrees with source arc formula',['A1.Ex2','A1.SS1.p2.2']),
 ('G80-11','Physical t0 initialization: first source wait positive, selected live record0 and Phi0=id',['A1.SS1.p2.1','A1.E1','A1.Ex2']),
 ('G80-12','Last live phase evaluated at every finite offset when next wait infinity',['A1.SS1.p2.2'])
]
edges=[(1,3),(2,3),(1,4),(3,4),(2,5),(3,5),(4,5),(1,6),(2,6),(4,6),(5,7),(6,7),(4,7),(4,8),(7,8),(2,9),(6,9),(7,9),(8,9),(1,10),(4,10),(7,10),(8,10),(9,10),(1,11),(2,11),(3,11),(5,11),(7,11),(10,11),(4,12),(7,12),(10,12)]
graph={'schema':'independent-source-proof-graph-preread-v1','created_utc':now,'candidate_seen':False,'source_raw_sha256':pinned,'truth_contract':'Source-driven planned mathematical obligations and dependencies; no claimed compiled Lean edge, no source review verdict, no completion credit.','nodes':[{'id':i,'obligation':t,'anchors':a,'status':'SOURCE_EXPLICIT_OR_COMPRESSED_OBLIGATION_NOT_YET_AUDITED_AGAINST_CANDIDATE'} for i,t,a in nodes],'edges':[{'ingredient':f'G80-{a:02d}','consumer':f'G80-{b:02d}','kind':'planned-source-proof-ingredient'} for a,b in edges],'source_compressed_measurability_nodes':['G80-03 parameter measurable hit map','G80-04 guarded record measurability','G80-08 countable selector measurability','G80-09 valid-domain/off-good representation','G80-10 physical phase measurable realization','G80-11 selector/flow initialization bridge'],'scope_exclusions':scope['excluded'],'nonaccumulation_route_note':'Source direct Exp first-moment/mean1 SLLN and any already accepted sufficient OR-route must remain distinct. This preread does not inspect or certify either implementation.','ordering_note':'Graph freezes source mathematics before candidate. It permits equivalent measurable countable-search/piecewise routes; it never permits assuming the desired physical phase or measurable selector as a new source binder.'}
for fn,obj in [('source_inventory80.json',inv),('source_proof_graph80.json',graph)]:
 (OUT/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'source_freeze80.md').write_text('''# Successor80 independent source-first freeze

Primary PBPS arXiv2609.06905v1 raw SHA256: `'''+pinned+'''`.

The pinned primary was read first in this phase with a fresh stdlib html.parser. No80 header, implementation, statement, lesson, preread, capsule, extractor or reviewer material was opened. The inventory and12-node,33-edge source Proof Graph were authored independently before any candidate access.

The source-explicit construction uses the actual integrated-hazard clocks, finite postbounce records, initialization, and left-inclusive/right-exclusive deterministic arcs. The measurable realization is compressed into the source process-construction sentence. Necessary measurable-clock/record/selector/evaluation and initialization bridges are kept as obligations, not as new public premises or completed results.

Finite stored time and elapsed, zero-residual Borel bounce, all-coordinate positive clocks, initialization at physical0, final infinite-wait live arc, simultaneous all-finite-time source agreement, and possible measurable null-input totalization are distinct contracts. A fixed-time measurable random phase is weaker than joint time/sample/parameter measurability; neither automatically proves Markov/invariance/cost/full-algorithm properties.

Only source inventory/graph planning is frozen here. No Lean declaration, proof, verification, candidate fidelity verdict or shared-state change is produced. Later review must use a fresh canonical packet and separate output files, preserving this source-first seal unchanged.
''',encoding='utf-8')
files=['primary_only80.py','freeze_source80.py','source_inventory80.json','source_proof_graph80.json','source_freeze80.md']
seal={'schema':'immutable-source-first-seal-v1','created_utc':now,'primary_raw_sha256':pinned,'candidate_access_before_freeze':False,'self_hash_not_included':True,'files':{n:sha((OUT/n).read_bytes()) for n in files}}
sealpath=OUT/'source_freeze80.seal.json';sealpath.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifestpath=OUT/'source_freeze80.raw-manifest.json'
manifest={'schema_version':1,'created_utc':now,'purpose':'Primary-only preread chronology and exact RAW evidence; no candidate review/Lean verification','source_first':True,'candidate_accessed':False,'raw_inputs':[{'path':str(SRC),'raw_sha256':pinned}],'raw_outputs':[{'path':str(OUT/n),'raw_sha256':sha((OUT/n).read_bytes())} for n in files+['source_freeze80.seal.json']],'self_output':{'path':str(manifestpath),'raw_sha256':'omitted-selfhash; reported externally'},'scope_item_count':len(coverage),'source_graph_node_count':len(nodes),'source_graph_edge_count':len(edges)}
manifestpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(sha((OUT/n).read_bytes())==h for n,h in seal['files'].items())
print(json.dumps({'ready':True,'inventory_items':len(coverage),'graph_nodes':len(nodes),'graph_edges':len(edges),'raw_inputs':manifest['raw_inputs'],'raw_outputs':manifest['raw_outputs']+[{'path':str(manifestpath),'raw_sha256':sha(manifestpath.read_bytes())}]},ensure_ascii=False,indent=2))
