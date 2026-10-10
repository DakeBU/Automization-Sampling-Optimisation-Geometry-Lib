from pathlib import Path
import json
import hashlib
import datetime

root=Path('E:/Samplinglib')
out=Path(__file__).resolve().parent
pre=out.parent
first=pre/'independent-source-first88'
header=pre/'header88.proposed.lean'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def pin(path):return dict(path=str(path.resolve()),raw_sha256=sha(path),bytes=path.stat().st_size)
def write(name,value):
 path=out/name;path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return path
assert sha(header)=='89890948b0716e9e8a0a4e4d5c634aa166361b7fb1575f57e751d49e024aeed3'
frozen={
 first/'source-first88.freeze.native.json':'9b3dc106bb0bd83bf846af82aef051c7af5c6c0e2142b33d6834bc89777011da',
 first/'source-proof-slice88.native.json':'7fe781cc3ab8092faf0c9970787c459f662a2e52585c4d637e57c0a328895726',
 first/'source-coverage88.native.json':'6e88954e891eac264d81416f5661e3726c6db3a39c4e38915c38d2f8617b2e92',
 first/'primary-source88.raw-manifest.native.json':'1c5977ef4f0a115811e10d53be294b37287e07d2c664f176e030c94483d49b37',
 first/'closed-raw-manifest.source-first88.native.json':'fedbc429c2e3cc01aa92a2b5dd94a0f5c4c431f005564bcb50631822681432f5'}
for path,value in frozen.items():assert sha(path)==value
old_manifest=json.loads((first/'closed-raw-manifest.source-first88.native.json').read_text(encoding='utf-8'))
for group in ['inputs','outputs']:
 for item in old_manifest[group]:
  path=Path(item['path']);assert sha(path)==item['raw_sha256'];assert path.stat().st_size==item['bytes']
pm=json.loads((first/'primary-source88.raw-manifest.native.json').read_text(encoding='utf-8'))
source=Path(pm['source']['path']);raw=source.read_bytes()
for span in pm['anchors']:assert hashlib.sha256(raw[span['byte_start_zero_based']:span['byte_end_exclusive']]).hexdigest()==span['raw_span_sha256']
snapshot=out/'header88.exactraw.snapshot.txt';snapshot.write_bytes(header.read_bytes())

definitions=[
 ('c','Literal source3.4 center y-eta*gradient(V,xRef).'),
 ('Phi','Literal harmonic position/momentum flow, including -sin(t)/sqrt(eta) coefficient for positive eta.'),
 ('S','Literal reflection. Total division gives zero correction at a zero gradient-difference normal, hence R0=I.'),
 ('rate','Literal sqrt(eta) times positive part of momentum/gradient-difference inner product.'),
 ('Lambda','Literal integrated rate along the actual deterministic flow, with finite nonnegative time argument.'),
 ('tau','Literal hittingAfter of Lambda-e into Ici0 after0; extended nonnegative time permits empty-set infinity. No strict-increase or finite-crossing requirement.'),
 ('next','The stopped tag is absorbing; infinite tau yields stopped. Finite extraction untopD0 occurs only after tau is checked non-top, followed by the actual flow and bounce.'),
 ('record','Actual finite recursive history initialized at live(0,z0), consuming threshold e_k at successor k.'),
 ('P','Original iid rate-one exponential raw input law realized as a countable real-coordinate product.'),
 ('epsilon','Declared ambient clipping Real.toNNReal. It changes only a null nonpositive raw-coordinate set under P; no negative-clock source dynamics are claimed.'),
 ('history','All records0..n, including stopped tags, indexed by Fin(n+1). Uses only raw coordinates below n.'),
 ('liveSurvival','For live(T,z), finite duration u is strictly smaller than the literal tau_z(toNNReal e). For an already stopped record it is False. This represents actual next waiting survival only on a live current record.'),
 ('survivalWeight','For live(T,z), ENNReal.ofReal(exp(-Lambda_z(u))); stopped gives0. This is the matching unnormalized live-guarded factor, not a survival law for an invented next state.')]
binder_audit=[
 dict(name='hAlpha',classification='STANDING',source_anchor='S1.p1/S1.E1',meaning='Positive lower Hessian constant.'),
 dict(name='hAlphaBeta',classification='STANDING',source_anchor='S1.p1/S1.E1',meaning='alpha<=beta with both nonnegative carriers.'),
 dict(name='hV',classification='STANDING',source_anchor='S1.p1',meaning='Global C2 potential.'),
 dict(name='hH',classification='STANDING',source_anchor='S1.E1',meaning='Both quadratic Hessian inequalities for every x and v; no omitted direction or additional estimate.'),
 dict(name='hEta',classification='STANDING',source_anchor='S2.SS2.p1',meaning='Positive eta.'),
 dict(name='hBetaEta',classification='STANDING',source_anchor='S2.SS2.p1',meaning='beta*eta<=1, equivalent to the printed scale bound under beta>=alpha>0.')]
test_class=dict(
 duration='d is an arbitrary deterministic function on the complete finite tagged-history Borel carrier with values in finite NNReal. Measurable d is explicitly a restriction to the admissible Borel test-function class. It is not a seventh analytic assumption on V/process/clock law, and not a measurability certificate for the actual history or random hazard.',
 duration_source_delta='The authors do not print this free d binder. It is an explicit source-implicit interface generalization justified by measurable-parameter exponential integration and needed for the random remaining-horizon consumer.',
 events='A ranges over every measurable history event, including null events. MeasurableSet A defines admissible event tests; no P(A)>0 restriction or conditional-probability division is added.',
 source_binder_discipline='Retain an explicit source-implicit/generalization ledger for these test-class quantifiers. Do not label Measurable d a printed paper-wide hypothesis or pure carrier-only typing, and do not hide it inside an unexplained provider bundle.',
 no_tail_inspection='d receives only a finite history argument. Since actual H_n is a consumed-prefix function, d(H_n) cannot inspect unused raw clocks. No additional causality assumption on d is needed.',
 required_consumer='For each fixed T>=0, define d_T(h) by matching the last record: live(t,z) maps to Real.toNNReal(T-t), stopped maps to0. This is Borel by finite evaluation, sum cases, time projection and continuous clipping. Universal d already includes it; no second fixed-u SAU is needed.')
pushforward=dict(
 notation='Let H=history(y,xRef,z0,n), mu=Measure.map H P, and W(h)=survivalWeight(y,xRef,h_n,d(h)).',
 header_RHS='Integral over h in A of W(h) against mu.',
 frozen_RHS='Integral over H^-1(A) intersect L_n of ENNReal.ofReal(exp(-Lambda_(Z_n)(d(H(w))))) against P.',
 equivalence_route=[
  'Derive actual H measurability from the unchanged accepted finite-history producer.',
  'The header itself requires W measurability as a conclusion, derived from literal hazard/record and Measurable d.',
  'For measurable A, nonnegative measurable pushforward integration gives integral_A W d(H_*P)=integral_(H^-1(A)) W(H(w)) dP.',
  'On a live last record W(H(w)) is the exponential hazard factor; on a stopped record it is0. Thus the integral equals the frozen live-restricted P-space formula exactly.',
  'The last record in H is definitionally record_n, so the two left survival events also agree exactly.'
 ],
 new_source_premise=False,normalization=False,regular_conditional_distribution_assumed=False,
 null_event='When mu(A)=P(H^-1(A))=0, the restricted lintegral and the live-guarded event probability both vanish.',
 probability_carriers='Header event measurability is on History_n times the entire unused raw-tail space. Its clock p.2(0) corresponds under the joint history/tail pushforward to raw w(n), source E_(n+1).')

slots={
 'objects':dict(original='Literal actual PBPS stopped recursion, complete finite history, next independent exponential clock, and tagged live survival weight.',candidate='The same first eleven literal definitions plus liveSurvival and survivalWeight; no arbitrary algorithm/kernel/provider is substituted.',relation='equivalent-after-expansion',evidence='Source A1.E1/E2 and the frozen actual-history/live-state formula; the candidate expands the private Prop explicitly.'),
 'domains':dict(original='Finite-dimensional real inner-product Borel space; original six analytic premises; finite tagged histories; nonnegative finite duration; real raw clock product with declared null-set input clipping.',candidate='Identical carriers and literal flow/hazard/recursion. The survival event uses a full unused raw-tail coordinate and the weight is ENNReal nonnegative.',relation='equivalent',evidence='Exact candidate let definitions and source-first88 fixed_inputs/objects/test_class. ENNReal is a nonnegative integral representation, not a changed probability model.'),
 'quantifiers':dict(original='For all fixed deterministic y/reference/z0/n, all measurable history-duration d and all measurable history events A.',candidate='Those universal quantifiers appear directly; event/weight measurability and pointwise weight<=1 hold for each admissible d and all histories.',relation='equivalent-with-derived-strengthening',evidence='No random depth/index is quantified. d has the complete finite history as its sole argument; A has no positivity condition.'),
 'assumptions':dict(original='Six source analytic binders; measurability of d and A restricts admissible tests. All actual process regularity and input independence must be derived internally.',candidate='Exactly six analytic binders plus explicit measurable-test quantifiers. No history/hazard/clock-law/independence/provider premise.',relation='equivalent',evidence='Literal hAlpha/hAlphaBeta/hV/hH/hEta/hBetaEta inspected and all private Prop binders expanded. The test-class generalization is explicitly recorded separately.'),
 'conclusion':dict(original='Unnormalized live-guarded P-space survival identity evaluated at a measurable random current state and duration.',candidate='The same event probability equals a history-law lintegral, plus derived joint-event measurability, weight measurability and weight<=1.',relation='equivalent-with-derived-strengthening',evidence='Pushforward proof above converts the history-law lintegral to the frozen P-space integral, with stopped weight0. Joint measurability and boundedness are required internally available source ingredients, not added assumptions.'),
 'scopes':dict(original='Deterministic finite event depth, live current record, all measurable duration/history tests including stopped/null/zero cases; I5 and full path assembly excluded.',candidate='Live record uses strict finite-duration survival, stopped record False; weight0 on stopped. Includes d_T remaining-horizon duration but does not assert its final-factor assembly, density iteration or random-time restart.',relation='equivalent',evidence='Current record live with tau=infinity is distinct from an already stopped record. The former survives every finite duration; the latter contributes zero. No physical-time clock-memorylessness statement appears.'),
 'constant_dependencies':dict(original='Unit exponential clock rate; fixed source alpha/beta/eta; no uniform bound on d, rate cap, horizon, failure budget or cost premise.',candidate='P uses expMeasure1; d is NNReal-valued but unbounded as a function; W<=1 is a conclusion from Lambda>=0.',relation='equivalent',evidence='Nonnegative rate makes each finite-duration hazard nonnegative, so exp(-Lambda)<=1 for every live history. No extra integrability/domination premise is present.')}

topology=dict(kind='Header-to-frozen-source-topology correspondence check',
 mapping=[
  dict(source_node='S87-I1/I2/I3',header_use='Actual deterministic finite history, original product P and raw next-coordinate relation; unchanged verified parents must supply the needed process measurability and independence.'),
  dict(source_node='S88-A1',header_use='Literal Lambda/tau and derived event/weight measurability plus weight bound; analytic regularity must be discharged internally.'),
  dict(source_node='S88-A2',header_use='liveSurvival uses exactly strict u<tau for the source >= crossing; no endpoint alteration or finite-wait premise.'),
  dict(source_node='S88-P1/P2',header_use='The joint history/raw-tail measurable event and unnormalized measure identity expose the independent exponential evaluation at d(H_n). No fixed-parameter substitution shortcut is part of the statement.'),
  dict(source_node='S87-I4',header_use='The prospective universal d-parametric live-guarded conditional-survival target.'),
  dict(source_node='S87-I5',header_use='No density/final-factor/iteration/whole-A7 assembly conclusion; remains excluded.')],
 frozen_graph_unchanged=True,coverage_unchanged=True,
 independent_header_source_review=True,
 separate_independent_approval_of_self_authored_graph=False,
 limitation='This reviewer authored the original source-only frozen graph. The present check independently compares a later formalizer header to that primary-derived graph, but must not be advertised as a distinct second-person approval of the reviewer own graph coverage. No new source-topology admission state is written.')

endpoints=dict(
 source_crossing='tau is first >=-hazard crossing, with empty crossing set infinity; liveSurvival is strict u<tau. Source continuity/monotonicity must prove equivalence to e>Lambda(u) internally.',
 zero_duration='At u=0 positive source clocks give survival1 on live records; zero raw clocks belong to the null ambient extension and have tau(0)=0.',
 zero_rate='An initially live zero-rate record has infinite next wait for positive clocks, hence survival1 for finite u. After a prior stopped tag no next wait is asserted and both event/weight contributions are0.',
 zero_normal='Total reflection formula remains R0=I; no nonzero-normal assumption.',
 infinite_wait='A live current record with next tau=infinity belongs to survival for every finite d. d itself is finite NNReal-valued, so the header does not assert an infinite-duration limit or an infinite-wait mass theorem.',
 unbounded_d='d can be unbounded across histories; every realized duration is finite, each deterministic arc hazard is finite, and the survival weight remains<=1.',
 final_horizon='d_T=(T-T_n)_+ is allowed, while the source final-factor consumer must still impose its correct live-before-T history event, endpoint convention and ordered-time integration in I5.')

deltas=[
 dict(id='H88-D1',slot='conclusion',classification='representation-elaboration',blocking=False,description='History-law nonnegative lintegral is exactly the frozen P-space live-guarded integral after measurable history pushforward; it adds no hypothesis.'),
 dict(id='H88-D2',slot='assumptions',classification='source-implicit-admissible-test-generalization',blocking=False,description='Measurable d and MeasurableSet A are explicit admissible-test restrictions, not new PBPS analytic assumptions or providers. The authors did not print a free duration-function binder.'),
 dict(id='H88-D3',slot='conclusion',classification='source-implicit-derived-strengthening',blocking=False,description='Joint history/raw-tail event measurability, weight measurability and pointwise weight<=1 are derived conclusions consistent with source hazard regularity and nonnegative intensity.'),
 dict(id='H88-D4',slot='scopes',classification='endpoint-and-tagged-representation-elaboration',blocking=False,description='False stopped survival and zero stopped weight match the live guard; live current records with infinite next waits are not discarded.'),
 dict(id='H88-D5',slot='scopes',classification='residual-boundary-retained',blocking=False,description='Only prospective S87-I4 is targeted; I5/fullA7/final-factor assembly/random-time restart/Markov/invariance/cost/main/Goal remain open.')]

run_record=write('header88.source-review.run.native.json',dict(schema=1,kind='assistant-authored-native-prospective-header-source-review',
 reviewer='/root/fresh_source87',formalizer='/root',stage='HEADER_ONLY_NO_BODY',input_header=pin(header),source_first_inputs=[pin(p) for p in frozen],
 semantic_comparison=slots,literal_definition_audit=[dict(name=n,kind='literal',evidence=e,accepted=True) for n,e in definitions],
 six_analytic_binder_audit=binder_audit,admissible_test_class_audit=test_class,pushforward_equivalence=pushforward,
 endpoints_and_tagged_branch_audit=endpoints,source_topology_correspondence=topology,
 outcome='Accept exact prospective header as an explicit ASTIS source-implicit measurable-duration survival target; no blocking delta or repair.',
 no_candidate_body_read=True,no_canonical_writes=True,no_verified_transition=True,
 recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
decision=write('header88.source-decision.native.json',dict(schema=1,kind='independent-exact-header-source-decision',
 reviewer='/root/fresh_source87',formalizer='/root',stage='PROSPECTIVE_HEADER_ONLY',
 verdict='ACCEPT_EXACT_HEADER_SOURCE_EQUIVALENT_AFTER_ELABORATION',semantic_slots=slots,deltas=deltas,blocking_deltas=[],repairs=[],
 header=pin(header),source_first_freeze=pin(first/'source-first88.freeze.native.json'),source_graph=pin(first/'source-proof-slice88.native.json'),source_coverage=pin(first/'source-coverage88.native.json'),
 review_run=pin(run_record),literal_definition_audit=[dict(name=n,kind='literal',evidence=e,accepted=True) for n,e in definitions],
 six_analytic_binder_audit=binder_audit,admissible_test_class_audit=test_class,pushforward_equivalence=pushforward,
 source_topology_correspondence=topology,endpoints_and_tagged_branch_audit=endpoints,
 prospective_truth_boundary='The target is S87-I4 only, a source-implicit random-state/measurable-history-duration survival completion. This statement-level decision supplies no proof or completed semantic BODY review.',
 open_consumers=['I5','conditional remainder of G86-11','conditional finite-event density','ordered-time/final-factor assembly','full A.7','physical-time residual memorylessness','random stopping/restart/Markovness','path reversal/invariance/all-L2','cost/main/composition/whole paper/Goal'],
 later_body_requirement='Fresh canonical anti-anchored BODY reviewer packet, independent blind reconstruction and exact module/prose review remain required after compilation. Do not replay this prospective header decision as BODY or VERIFIED acceptance.',
 canonical_writes=False,verified_transition=False,new_goal_credit=False))
chronology_path=out/'chronology.header-source88.native.jsonl'
events=[
 dict(sequence=1,event='Previously closed source-first88 freeze remained immutable before header exposure',freeze=pin(first/'source-first88.freeze.native.json')),
 dict(sequence=2,event='Root separately authorized exact prospective header comparison; no BODY exists'),
 dict(sequence=3,event='Read complete exact header and independently expanded literal definitions/binders/test domains',header=pin(header)),
 dict(sequence=4,event='Reverified unchanged source-first closed manifest and all exact primary spans; compared candidate to primary-derived frozen graph/coverage'),
 dict(sequence=5,event='Derived history pushforward equivalence and audited strict survival/tagged endpoints; no source repair required'),
 dict(sequence=6,event='Closed prospective header source decision and native run, without BODY/source-topology-admission/VERIFIED claims',decision=pin(decision),run=pin(run_record))]
chronology_path.write_text(''.join(json.dumps(dict(e,recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),ensure_ascii=False)+'\n' for e in events),encoding='utf-8')
inputs=[header,*frozen,source,first/'chronology.native.jsonl',first/'terminal-completion88.native.json',root/'lean-toolchain',root/'lake-manifest.json']
outputs=[p for p in sorted(out.iterdir()) if p.is_file() and p.name!='closed-raw-manifest.header-source88.native.json']
closed=write('closed-raw-manifest.header-source88.native.json',dict(schema=1,kind='closed-RAW-exact-prospective-header-source88-manifest',
 inputs=[pin(p) for p in inputs],outputs=[pin(p) for p in outputs],exact_primary_spans=pm['anchors'],
 inherited_source_first_closed_manifest=pin(first/'closed-raw-manifest.source-first88.native.json'),
 source_topology_scope='Header correspondence with unchanged primary-derived frozen graph only; no self-certified distinct second-person coverage approval.',
 body_read=False,body_source_acceptance=False,verified_transition=False))
for path in [decision,run_record,closed,chronology_path]:print(path.name,sha(path))
