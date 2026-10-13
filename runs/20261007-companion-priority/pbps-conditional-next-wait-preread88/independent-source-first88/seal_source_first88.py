from pathlib import Path
import json
import hashlib
import datetime
import subprocess

root=Path('E:/Samplinglib')
out=Path(__file__).resolve().parent
source=root/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert b'arXiv:2609.06905v1 [math.ST] 07 Sep 2026' in raw
assert b'License: arXiv.org perpetual non-exclusive license' in raw
lines=raw.splitlines(keepends=True)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def pin(path):return dict(path=str(path.resolve()),raw_sha256=sha(path),bytes=path.stat().st_size)
def write(name,value):
 path=out/name;path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return path

source_spans=[]
for identity,start,end,scope in [
 ('license-tr',257,261,'Fixed version/date and local license'),
 ('S1.p1/S1.E1',349,361,'Original global smoothness/Hessian standing assumptions'),
 ('S2.SS2.p1',613,616,'Positive scale and beta*eta upper range'),
 ('S3.E4',1486,1492,'Source center and gradient difference'),
 ('A1.SS1.p1',2859,2887,'Literal fixed-reference flow, bounce and intensity'),
 ('A1.SS1.p2/A1.E1/A1.E2',2889,2911,'Independent clocks, integrated-hazard crossing, finite update and stopping convention'),
 ('A1.SS1.p3',2913,2973,'Energy/rate/non-explosion; separate memorylessness/Markov claim excluded'),
 ('A1.SS1.SSS0.Px1.p4/A1.E7',3147,3173,'Clock iteration and final trajectory survival consumer'),
 ('A1.SS2 joint Borel recursion paragraph',3325,3338,'Source explicit hazard/crossing/recursion measurability')]:
  startbyte=sum(map(len,lines[:start-1]));endbyte=sum(map(len,lines[:end]))
  source_spans.append(dict(id=identity,raw_line_start=start,raw_line_end=end,
   byte_start_zero_based=startbyte,byte_end_exclusive=endbyte,
   raw_span_sha256=hashlib.sha256(raw[startbyte:endbyte]).hexdigest(),scope=scope))
manifest=write('primary-source88.raw-manifest.native.json',dict(schema=1,kind='independent-primary-first88-RAW-source-manifest',
 source=dict(**pin(source),immutable_url='https://arxiv.org/html/2609.06905v1',version='arXiv:2609.06905v1',printed_date='07 Sep 2026',license='arXiv.org perpetual non-exclusive license'),
 anchors=source_spans,source_text_handling='Long source extract only in primary88.extracted.private.json, excluded from publication; public findings are attributed restatements and hash coordinates.'))

reuse_paths={
 root/'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/topology-repair-review86/source-proof-graph86.single-edge-proposed-successor.json':'c7ed4b13d3471c42d2e516edfef3009345ce156e961685a0ad6f11344aa0f7d8',
 root/'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/independent-source86/source-inventory86.exhaustive-successor.json':'cd5f487c3091946ab0699c4c50203a1703ff8b6e0f44a67cfa86920c9a26db3f',
 root/'runs/20261007-companion-priority/pbps-clock-tail-preread87/source-slice87.v2.json':'7c9873ef87bfb75c7a2ec86ecbb40b589384bc41bc197030acf7fa088fd611d9',
 root/'runs/20261007-companion-priority/pbps-clock-tail-preread87/independent-source-first87/source-first.freeze.native.json':'d8e37422b5597b0a5761282bcf88b94453a7b21a5176ef0cb71c2363f5ab87d7'}
for path,value in reuse_paths.items():assert sha(path)==value,(str(path),sha(path))
parent_commit=subprocess.check_output(['git','rev-parse','24210c17^{commit}'],cwd=root,text=True).strip()
parent_module=root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean'
assert sha(parent_module)=='01fcff944f1dbd42be2af30063b9baf4e191e2cde959e008724387cadb4fc899'
reuse=write('unchanged-source-evidence88.native.json',dict(schema=1,
 source_evidence=[dict(**pin(path),handling='RAW-only unchanged identity check; global proof topology not reconstructed from Lean') for path in reuse_paths],
 accepted_parent=dict(integration_commit=parent_commit,module=pin(parent_module),status='Prior independent BODY source review and root-reported verified integration reused; no new candidate88 read'),
 scope='Unchanged exhaustive global inventory/topology and validated local source slice retained. The new I4 refinement below was reconstructed directly from the primary, not inferred from candidate implementation.'))

nodes=[
 dict(id='S87-I1',kind='parent-source-implicit',status='unchanged-verified-parent-reused',claim='Actual finite stopped history is measurable in consumed clock prefix.',anchors=['A1.E1','A1.E2','A1.SS2 joint Borel recursion paragraph']),
 dict(id='S87-I2',kind='parent-source-implicit',status='unchanged-verified-parent-reused',claim='Mutual independent clocks give independent generated prefix/tail sigma algebras.',anchors=['A1.SS1.p2']),
 dict(id='S87-I3',kind='parent-source-implicit',status='unchanged-verified-parent-reused',claim='Generated fixed-depth history is independent of the unchanged complete unused raw-clock tail.',anchors=['A1.SS1.p2','A1.E7']),
 dict(id='S88-A1',kind='source-analytic-ingredient',status='required-reused-or-to-be-discharged-internally',claim='Along each deterministic flow arc, Lambda(z,u) is jointly Borel, finite/continuous/nondecreasing in finite nonnegative u, nonnegative and zero at u=0.',anchors=['A1.SS1.p1','A1.E1','A1.SS2 joint Borel recursion paragraph']),
 dict(id='S88-A2',kind='source-implicit-endpoint-bridge',status='required-reused-or-to-be-discharged-internally',claim='For finite u>=0 and nonnegative e, u<tau_z(e) iff Lambda_z(u)<e, with tau=inf crossing into >= and empty-set infinity.',anchors=['A1.E1','A1.SS1.p2.2']),
 dict(id='S88-P1',kind='source-implicit-probability-ingredient',status='required-internal-consumer-of-I3',claim='The next raw coordinate has Exp(1) law and is independent of H_n; any measurable d(H_n) and live current state remain past-measurable.',anchors=['A1.SS1.p2','A1.E7']),
 dict(id='S88-P2',kind='source-implicit-random-parameter-integration',status='next-new-probability-mechanism',claim='Integrate the independent exponential survival law against a measurable random state and history-duration threshold via the joint product law; do not substitute a random parameter into separate a.e.-for-fixed-parameter identities.',anchors=['A1.E1','A1.SS1.SSS0.Px1.p4/A1.E7']),
 dict(id='S87-I4',kind='live-source-implicit-target',status='OPEN_TARGET88',claim='At every deterministic event depth, derive unnormalized live-guarded next-wait survival for every measurable history event and every measurable nonnegative history-duration function.',anchors=['A1.E1','A1.E2','A1.SS1.SSS0.Px1.p4/A1.E7']),
 dict(id='S87-I5',kind='future-assembly-consumer',status='OPEN_EXCLUDED_FROM88',claim='Conditional finite-wait densities, final no-event factor integration, ordered-time iteration and full trajectory A.7 assembly.',anchors=['A1.E7'])]
edges=[
 ('S87-I1','S87-I3','Past-measurable actual history is required to descend coordinate-block independence.'),
 ('S87-I2','S87-I3','Independent input blocks give the unchanged independent unused tail.'),
 ('S87-I3','S88-P1','Project the unused raw tail to its first coordinate; keep law Exp(1).'),
 ('S88-A1','S88-A2','Continuity/nondecreasing hazard and closed target discharge first-crossing/survival endpoints.'),
 ('S87-I1','S88-P1','Last live record and d(H_n) are functions of the finite past.'),
 ('S88-A1','S88-P2','Joint Borel random hazard gives a measurable parameter-dependent clock event and survival weight.'),
 ('S88-P1','S88-P2','The product law allows integration of the random threshold against the unchanged exponential law.'),
 ('S88-A2','S87-I4','Convert threshold exceedance back to the literal next waiting-time event.'),
 ('S88-P2','S87-I4','Evaluate its probability for all history events without normalization.'),
 ('S87-I4','S87-I5','The d_T specialization supplies a final finite-horizon survival factor; density and iteration/trajectory assembly remain additional obligations.')]
graph=write('source-proof-slice88.native.json',dict(schema=1,kind='source-only local I4 refinement; not a Lean dependency certificate',nodes=nodes,
 edges=[dict(source=a,target=b,consumer_use_site='A1.E1 for next waiting time; A1.E7 clock iteration for the random-parameter factor',justification=j) for a,b,j in edges],
 route_semantics='One conjunctive sufficient route after all listed ingredients are actually discharged; individual directed edges are prerequisites, not standalone sufficient proofs. No alternative route is flattened into this route.',
 global_topology_handling='Unchanged existing global graph/inventory reused by exact RAW identity. This local graph neither supersedes them nor marks all G86-11 complete.',
 topology_provenance='Direct primary reread and source-only derivation before any candidate88/header/BODY exists.'))

coverage=write('source-coverage88.native.json',dict(schema=1,in_scope=[
 dict(anchor='A1.SS1.p1',disposition='NODE S88-A1',reason='The actual rate and flow determine hazard regularity; reflection discontinuity is not needed along a deterministic no-jump arc.'),
 dict(anchor='A1.SS1.p2',disposition='NODE S88-P1',reason='The next independent exponential clock is the probability input.'),
 dict(anchor='A1.E1',disposition='NODE S88-A1/S88-A2/S87-I4',reason='Literal integrated-hazard threshold crossing is converted to next-wait survival.'),
 dict(anchor='A1.E2/A1.SS1.p2.2',disposition='NODE S87-I1/S88-P1/S87-I4',reason='Live current state comes from finite recursion; infinite crossing stops recursion and must remain tagged.'),
 dict(anchor='A1.SS1.SSS0.Px1.p4 first iteration sentence/A1.E7 survival factor',disposition='NODE S88-P2/S87-I4; future consumer S87-I5',reason='Source omits random-parameter integration in the clock iteration; ASTIS makes that probability bridge explicit.'),
 dict(anchor='A1.SS2 joint Borel recursion paragraph',disposition='NODE S88-A1/S87-I1',reason='Explicit source Borel/continuous/nondecreasing-hazard/crossing/recursion reasoning supports measurability without a new public regularity premise.')],
 exclusions=[
 dict(anchor='A1.SS1.p3 energy/rate/SLLN',reason='Unchanged non-explosion route is a separate parent of global trajectory assembly, unnecessary for one deterministic finite-depth next-wait survival formula.'),
 dict(anchor='A1.SS1.p3 memorylessness/Markov assertion',reason='New-event survival uses a fresh independent exponential clock. Residual clocks at physical observation times and random-stopping Markovness are different obligations.'),
 dict(anchor='A1.E4-A1.E6/A1.E8',reason='Density reversal/change-of-variable/invariance mechanisms are outside the new conditional-survival edge.'),
 dict(anchor='A1.E7 full product/simplex/series and absolute-convergence paragraph',reason='Finite-event density, ordered-time iteration, final factor assembly and countable nonexplosive trajectory expansion remain S87-I5/global work.'),
 dict(anchor='Davis[12,Section2] cited at A1.SS1.p3',reason='Attribution retained, but no new external theorem is claimed or imported; the required local bridge is reconstructed from the pinned source construction and elementary iid integration.')],
 statement='Every substantive proof region in this bounded slice is assigned above. Existing global exhaustive coverage is reused, not newly certified by this local record.'))

freeze=write('source-first88.freeze.native.json',dict(schema=1,freeze_id='PBPS-S87-I4-HISTORY-DURATION-NEXT-WAIT-SOURCE-FIRST88',reviewer='/root/fresh_source87',
 source_manifest=pin(manifest),source_graph=pin(graph),source_coverage=pin(coverage),unchanged_evidence=pin(reuse),
 source_authored_vs_completion=dict(printed='The authors specify iid Exp(1) clocks, the integrated-hazard first crossing, finite flow/bounce updates, stopping at an empty crossing set, and attribute A.7 to clock iteration. The later A.2 paragraph explicitly discusses Borel hazards/crossings/recursion.',ASTIS_completion='The unnormalized survival identity at a random current state and a measurable history-duration parameter is an explicit ASTIS probability completion of that iteration. It is not a printed standalone theorem or a completed A.7 proof.'),
 recommended_single_bounded_target=dict(
  fixed_inputs='Retain original six analytic assumptions: alpha>0, alpha<=beta, V C2, both alpha/beta Hessian bounds for every x,v, eta>0 and beta*eta<=1. Fixed deterministic y/reference/z0 and deterministic finite event depth n. Use the actual literal stopped recursion and original iid input law.',
  objects='H_n is the complete finite tagged record history at depths0..n. L_n is the event that its final record is live(T_n,Z_n). Raw coordinate n is source E_(n+1), with NNReal clipping an explicitly declared ambient null-set extension only.',
  test_class='For every Borel history event A and every deterministic Borel measurable function d:History_n->[0,infinity), use duration d(H_n). No boundedness of d is required: every value is a finite nonnegative real and each finite-time hazard is finite.',
  unnormalized_formula='P(H_n in A AND L_n AND tau_(Z_n)(epsilon_n)>d(H_n)) = integral over (H_n^-1(A) intersect L_n) of exp(-Lambda_(Z_n)(d(H_n))) dP.',
  total_tagged_weight='Equivalently integrate over H_n^-1(A) the tagged weight W_d(history): live(T,z) maps to exp(-Lambda_z(d(history))), stopped maps to0. The event is explicitly live-guarded; no phase at infinity or next wait after stopping is assigned.',
  equivalent_conditioning_sense='For the indicator of the live-guarded survival event, conditional expectation given sigma(H_n) equals W_d(H_n) almost surely. The unnormalized event-integral identity suffices and avoids introducing a regular conditional distribution.',
  one_edge_reason='A universal measurable-duration interface contains the fixed-u case and supports the actual random remaining-horizon consumer. Do not introduce repeated wrapper lemmas for constant u versus d(H_n).'),
 duration_assumption_audit=dict(
  analytic_assumptions='The six actual PBPS analytic hypotheses remain unchanged; Measurable d is not a seventh assumption on V, the process, initial state or clock law.',
  function_domain='Measurable d restricts the admissible deterministic test-function class, like MeasurableSet A restricts test events. Relative to the printed paper it is an explicitly attributed source-implicit/generalized interface, not a claim that the authors wrote this free-function binder.',
  no_provider_premises='Actual history/last-live-state/hazard measurability, threshold-clock independence, product law, nonnegative hazard and threshold-crossing equivalence must be dependencies proved or consumed internally, never assumptions supplied by the caller.',
  forbidden_shortcut='A formal theorem for a separately assumed random state independent of a separately assumed clock is only generic infrastructure until actual generated history and next input clock discharge its conditions.',
  source_consumer_specialization='For fixed physical horizon T>=0, d_T(history)=max(T-last_live_time,0), with any declared stopped-branch value under the live guard, is Borel by finite projections/tagged cases/continuous clipping. Establish this specialization internally when consumed; a measurable d cannot inspect unused tail coordinates.'),
 independent_mathematical_derivation=[
  'The tagged last record and any measurable d(H_n) depend only on consumed clocks, using accepted I1-I3.',
  'The next raw input remains an independent Exp(1) coordinate; projecting the full unused tail preserves this law.',
  'For each live z and finite duration u, continuity and monotonicity of the integrated hazard give tau_z(e)>u iff e>Lambda_z(u), including flat/zero hazards and empty crossing sets.',
  'Joint measurability of the hazard and d makes the random-threshold event measurable. Use the joint product law and Tonelli/nonnegative parameter integration to evaluate the independent exponential tail at Lambda_z(d(h)).',
  'Retain the live guard and integrate this survival weight over arbitrary measurable history events. This yields an unnormalized formula even for null events; no point-history division is used.',
  'The bound 0<=exp(-Lambda)<=1 follows from nonnegative intensity, so no extra integrability or domination premise is needed. A nonnegative lintegral formulation can avoid analytic integration providers entirely.'],
 conditioning_and_stopping=dict(
  deterministic_depth='n is deterministic even though T_n and Z_n are random. This distinction permits iid input independence after a finite generated prefix.',
  duration_not_stopping_time='d(H_n) is a past-measurable duration for the next arc, not a random index or a future-informed physical stopping time.',
  random_parameter_warning='For each fixed u, a conditional identity may have a different null exceptional set. Substitution of random d(H_n) is not justified from those separate identities alone; derive the jointly measurable parameter identity directly.',
  stopped_history='Source recursion has no next phase state after stopping. Restrict to L_n, or declare a totalization and use matching stopped-branch weights. The recommended formula uses stopped weight0 and retains every stopped history without pretending its next event exists.',
  physical_time='N_T generally uses the current unused clock through observed survival. The original unused exponential is then truncated; conditional memorylessness of its residual is separate. No random-index restart or Markov theorem follows here.',
  null_events='If P(H_n in A)=0 both sides of the unnormalized formula vanish. Do not normalize and do not claim a conditional probability at each exact continuous history.'),
 endpoints_and_infinite_waits=dict(
  crossing='Source crossing uses >= at nonnegative times; survival uses strict tau>u and therefore strict E>Lambda(u). Continuity/closedness handles equality correctly, without requiring strictly increasing hazard.',
  duration_zero='At u=0, Lambda=0 and a positive exponential clock gives survival probability1 on every live history. Zero raw clocks occur only on a null ambient set; the deterministic crossing still has tau(0)=0.',
  zero_rate='A live zero-rate arc has Lambda identically0 and infinite next wait for positive clocks; survival through every finite duration is1. No positive-rate or finite-next-jump hypothesis is legal.',
  infinite_wait='The finite-duration formula includes tau=infinity automatically. It does not assert that the finite-wait law is proper.',
  limiting_mass='If L=lim_(u->infinity)Lambda_z(u), the infinite-wait mass is exp(-L), with exp(-infinity)=0, after a separate limit/measure-continuity argument. Exact equality at a finite total-hazard limit depends on whether the limit is attained, but the independent continuous clock makes that boundary conditionally null. Do not assert a pathwise > versus >= total-hazard criterion without this distinction.',
  finite_horizon='d_T=(T-T_n)_+ is a valid measurable duration. Actual n-event-before-T assembly also requires live T_n<T or the precise endpoint convention; that history event can be absorbed into A, but its ordered-time density integration remains I5.'),
 consumers_and_open_boundary=dict(
  immediate=['Conditional next-wait law at the actual random live state','Finite-horizon no-next-event factor with d_T=(T-T_n)_+'],
  still_open=['Derivative/finite-wait density and any density disintegration','Explicit infinite-wait atom if asserted as a separate theorem','Ordered jump-time integration/simplex bookkeeping','Products and iteration of all finite-event factors','Final survival factor assembly with live-before-horizon restrictions','Non-explosive countable trajectory decomposition','A.7 absolute convergence/full path-functional identity','Physical-time residual memorylessness and random stopping/restart/Markovness','Path reversal/invariance/L2/implementation error/cost/main/actual-input composition/whole paper/Goal'],
  global_node='This refines and targets S87-I4. I1-I3 are unchanged verified source/probability parents. I5 and the conditional assembly remainder of G86-11/G86-13/G86-14/G86-15 are not closed by the source freeze or by prospective survival-edge acceptance.'),
 candidate_acceptance_requirements=[
  'Retain the literal actual flow/rate/hazard/crossing/stopped history, with explicit source raw-to-NNReal clock indexing.',
  'Quantify deterministic n and measurable history-duration d; derive actual-history and random-hazard measurability and input independence internally.',
  'Prove live-guarded strict survival against the source >=-crossing, without positive-rate/finite-wait or normalized-history assumptions.',
  'Evaluate a jointly measurable random threshold directly; do not replace it with a fixed-state/fixed-duration wrapper or assume the desired factorization.',
  'Keep unrestricted measurable A including null events, stopped histories, zero duration/rate/normal, and infinite waiting possibilities.',
  'Attribute the new identity/argument to ASTIS as a source-implicit completion and keep I5/global conclusions open.'],
 independence_attestation=dict(candidate88_read=False,header88_read=False,body88_read=False,topology_inferred_from_Lean=False,prior_global_verdict_contents_read=False),
 lifecycle=dict(source_only=True,new_Lean_proof=False,new_verified_transition=False,new_goal_credit=False,canonical_writes=False),
 freeze_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))

with (out/'chronology.native.jsonl').open('a',encoding='utf-8') as chronology:
 for event in [dict(event='UNCHANGED_GLOBAL_SOURCE_REUSE_RAW_REVERIFIED',artifact=pin(reuse)),
  dict(event='INDEPENDENT_SOURCE88_DURATION_CONSUMER_ASSESSMENT',finding='One measurable-history-duration live-guarded survival interface is justified and needed to avoid invalid random-parameter substitution; no candidate88 read.'),
  dict(event='SOURCE_FIRST88_FREEZE_COMPLETED',freeze=pin(freeze),source_graph=pin(graph),source_coverage=pin(coverage))]:
  event.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate88_read=False);chronology.write(json.dumps(event,ensure_ascii=False)+'\n')
completion=write('terminal-completion88.native.json',dict(schema=1,status='SOURCE_FIRST_IMMUTABLE_FREEZE_CLOSED',
 reviewer='/root/fresh_source87',freeze=pin(freeze),graph=pin(graph),coverage=pin(coverage),candidate88_exposure=False,
 no_new_proof_or_VERIFIED_or_Goal_credit=True,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
inputs=[source,*reuse_paths,parent_module,root/'lean-toolchain',root/'lake-manifest.json',root/'.agents/skills/astis-substantive-advance/SKILL.md',root/'.agents/skills/astis-semantic-roundtrip/SKILL.md']
outputs=[p for p in sorted(out.iterdir()) if p.is_file() and p.name!='closed-raw-manifest.source-first88.native.json']
closed=write('closed-raw-manifest.source-first88.native.json',dict(schema=1,kind='closed-RAW-source-first88-evidence-manifest',
 inputs=[pin(p) for p in inputs],outputs=[pin(p) for p in outputs],exact_primary_spans=source_spans,
 freeze_raw_sha256=sha(freeze),global_source_evidence_reused_unchanged=True,
 excluded_from_publication=[str((out/'primary88.extracted.private.json').resolve())],new_candidate_exposure=False))
for path in [freeze,graph,coverage,manifest,reuse,closed,completion,out/'chronology.native.jsonl']:
 print(path.name,sha(path))
