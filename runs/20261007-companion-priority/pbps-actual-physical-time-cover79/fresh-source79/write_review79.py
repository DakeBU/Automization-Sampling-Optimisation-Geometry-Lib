from pathlib import Path
import json,hashlib,datetime,re
ROOT=Path(r'E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79/fresh-source79'
PACK=ROOT/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79/source-review79.packet.json'
SOURCE=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
packet=json.loads(PACK.read_text(encoding='utf-8-sig'));pcopy=dict(packet);pcopy.pop('packet_sha256')
assert sha(canonical(pcopy))==packet['packet_sha256']=='a04fb9a861cac2368722a69b9c899fd43f4884e1d075ffe5beae9c300fc10455'
context=packet['candidate_publication_context'];module=context['current_lean_module'];MODULE=ROOT/packet['lean']['file']
assert sha(MODULE.read_bytes())==sha(module.encode())==context['file']=='2f329dd32047f46adb81b65f51b9de56305021a944f7b8cdf62ae25665839c86'
assert sha((ROOT/'lean-toolchain').read_text(encoding='utf-8').encode())==context['toolchain']
assert sha((ROOT/'lake-manifest.json').read_text(encoding='utf-8').encode())==context['dependencies']
assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']
seal=json.loads((OUT/'source_freeze79.seal.json').read_text());assert all(sha((OUT/n).read_bytes())==h for n,h in seal['files'].items())
assert sha(SOURCE.read_bytes())==seal['primary_raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
inventory=json.loads((OUT/'source_inventory79.json').read_text());graph=json.loads((OUT/'source_proof_graph79.json').read_text())
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
slots={
 'objects':{
  'original':'The source fixes y, xtilde, z0 and uses its literal harmonic flow, residual-gradient reflection with R0=I, actual rate, integrated hazard and stopped actual postbounce recurrence. Between jumps the finite live phase at T_n supplies the arc with duration u in [0,S_(n+1)).',
  'reconstructed':'Same literal objects and actual recurrence, canonical Exp1 product coordinates clamped to NNReal, active finite (time,phase) records and absorbing no-phase stopped records. The selected interval yields this actual unique live record and finite elapsed t-s less than the next actual wait.',
  'relation':'explicit-elaboration',
  'evidence':'Frozen literal definitions and A1.Ex1-3/A1.E1-2/A1.SS1.p2.2 checked against entire private Prop/module. Body81-124 defines literal objects;168-210 links the selected finite clock to record_n=inl(a), not an external phase/certificate. Guarded untopD0 is used only when wait!=top. No physical-time phase function is defined by this theorem.'},
 'domains':{
  'original':'Source Euclidean R^d, finite physical t>=0 and finite live stored T_n; extended infinity for empty hazard hit set. Source scale eta in (0,1/beta].',
  'reconstructed':'Any finite-dimensional real inner-product Borel E, including dimension0; canonical sample carrier R^N; finite NNReal t, stored time and elapsed; WithTop NNReal event/wait times.',
  'relation':'explicit-elaboration',
  'evidence':'Intrinsic finite-dimensional formulation preserves all displayed norm/inner-product dynamics and specializes to R^d. Zero dimension/zero cap has no exclusion. NNReal subtraction is truncated generally, but part(ii) proves a.time<=t, making t-a.time genuine nonnegative elapsed time. Finite elapsed is never obtained by subtracting infinity.'},
 'quantifiers':{
  'original':'Arbitrary fixed y,xtilde,z0; almost surely the nonaccumulating source construction permits every finite physical time to lie on its appropriate between-jump arc. Source E_(n+1) drives the update out of state n; T0=0.',
  'reconstructed':'For every fixed triple, a.e. actual sample satisfies both conclusions simultaneously: every finite t has exactly one interval index; every t and every index satisfying the half-open inequalities has exactly one matching live finite record with elapsed below the next wait.',
  'relation':'explicit-elaboration',
  'evidence':'Public/private statement order is forall triple, a.e. sample, then conjunction with forall finite t and forall qualifying n. Body131-132 fixes the triple and lifts only actual nonaccumulation parent AE event. No uncountable common AE intersection over all triples and no random-initial-law theorem. Lean coordinate n matches source E_(n+1).'},
 'assumptions':{
  'original':'Standing C2 V, 0<alpha<=beta, Hessian sandwich (1.1), eta in (0,1/beta] (S2.SS2.p1.1), arbitrary finite fixed references/phase and independent Exp1 clocks. Initialization, actual recurrence, positivity, nonaccumulation and finite record existence are proof ingredients/definitions.',
  'reconstructed':'Six analytic binders hAlpha,hAlphaBeta,hV,hH,hEta,hBetaEta, finite-dimensional/Borel typing, literal product/threshold/flow/rate/hit/record definitions. No public interval selector, positivity, positive wait, recurrence, cap or nonaccumulation premise.',
  'relation':'explicit-elaboration',
  'evidence':'Source-first freeze included Section2.2 eta bound from the outset. Beta>0 follows from alpha>0/alpha<=beta, so eta range equals hEta and hBetaEta. Entire module private Prop/public signature checked. Parent76 derives monotonicity/guarded updates from actual recurrence; parent78 derives actual AE escape. Interval uniqueness uses monotonicity, not a new strict-wait assumption; zero-length intervals are empty.'},
 'conclusion':{
  'original':'Source between-jump formula applies on half-open arcs and, if the next hit set is empty, on the final live arc for all finite durations. Source nonaccumulation and initialization imply finite physical-time coverage; uniqueness of index/live record is a compressed necessary construction bridge.',
  'reconstructed':'Exactly one n with T_n<=t<T_(n+1), then exactly one genuine live finite record a with a.time<=t and finite NNReal t-a.time<tau(a.state,epsilon_n). Top stopped records cannot supply a phase; top next wait retains the last live record.',
  'relation':'explicit-elaboration',
  'evidence':'Body138-167 uses first-crossing predecessor rather than frozen possible greatest-sublevel route and proves interval disjointness.168-186 rejects stopped record and recovers actual stored time.187-207 proves elapsed inequality separately for infinite and finite waits.208-210 uses Sum.inl injectivity. This is the explicitly attributed ASTIS implicit adapter, not the entire source arc-assignment/global-process claim.'},
 'scopes':{
  'original':'The bounded source fragment is A.2 plus between-jump A1.SS1.p2.2 and the nonaccumulation ingredient. Full physical-time phase assignment and initial/interpolation identities, Markov/memoryless, measurable process, stationarity and costs are additional obligations.',
  'reconstructed':'Binding supports only actual-interval-cover. No global interpolated phase, measurable selector, path regularity/full process uniqueness, selected-index-at-t0 identity, Markov/invariance/kernel/hypocoercivity/cost/composition is asserted.',
  'relation':'explicit-elaboration',
  'evidence':'Checked all publication source/statement/obligations/assumption prose and nine formula steps. Source graph G79-11 is intentionally PARTIAL/OPEN: literal record0/T0 are retained, but physical-time initialization and phase interpolation identities are not proved here. Parent78 uses the declared bounded-indicator SLLN alternative; direct author Exp moment/mean1 expansion remains a separate open source route.'},
 'constant_dependencies':{
  'original':'No new constant is needed for interval selection. Source clocks/recursion depend on fixed eta,V,y,xtilde,z0; energy-based deterministic cap is upstream nonaccumulation evidence, not a free constant of the cover theorem.',
  'reconstructed':'No new cap, positive-wait lower bound, horizon cutoff constant or supplied witness. First crossing k and predecessor n may depend on fixed triple/sample/t. Finite stored time s and elapsed t-s are literal values from the record.',
  'relation':'same',
  'evidence':'Nat.find constructs k from actual AE escape for the current finite t; no uniform-in-t deterministic crossing index or sample-independent bound is claimed. Parent76/78 same six conditions and literal definitions checked directly. Eta/rate/flow normalizations match source; no constant or assumption is moved from a producer conclusion into a source-facing binder.'}
}
deltas=[
 {'id':'D79-intrinsic-space','slot':'domains','classification':'generalization','blocking':False,'description':'Source R^d is realized intrinsically in any finite-dimensional real inner-product Borel E, including dimension0; this specializes faithfully and imposes no source restriction.'},
 {'id':'D79-canonical-input','slot':'objects','classification':'explicit-elaboration','blocking':False,'description':'Actual product Exp1 coordinates and total NNReal clamp are a canonical source-input realization. Product parent proves the common a.s. positive/raw-clamp-equal event; transport to every arbitrary probability carrier is not a separately asserted theorem.'},
 {'id':'D79-halfopen-order-adapter','slot':'conclusion','classification':'source-implicit-adapter','blocking':False,'description':'Unique interval/live-record/elapsed is an ASTIS completion of the source compressed between-jump construction, not a direct quoted source theorem. Least first-crossing route is one of the independently frozen possible finite-order proofs; zero-length intervals remain empty.'},
 {'id':'D79-stopped-tail','slot':'objects','classification':'explicit-elaboration','blocking':False,'description':'Stopped next jump is encoded by top and no phase; it does not erase the prior finite live record. The infinite-wait branch bounds every finite elapsed offset. No phase or flow evaluation at infinity is introduced.'},
 {'id':'D79-elapsed-subtraction','slot':'domains','classification':'explicit-elaboration','blocking':False,'description':'NNReal tsub is total/truncated, but the conclusion proves stored time<=physical t before using it; hence it agrees with source finite nonnegative duration t-T_n.'},
 {'id':'D79-initial-interpolation-open','slot':'scopes','classification':'bounded-source-coverage','blocking':False,'description':'Frozen endpoint node G79-11 is only partially covered: actual record0=(0,z0) and finite postbounce next-record definitions are present, and half-open interval disjointness is proved. Explicit selected index(t0)=0, physical-time phase initial value and interpolation identities remain OPEN. Candidate source mapping explicitly excludes these, so no whole-source completion is accepted.'},
 {'id':'D79-parent-stochastic-or-route','slot':'scopes','classification':'alternative-sufficient-proof-in-parent','blocking':False,'description':'Actual nonaccumulation parent78 uses concrete bounded-indicator SLLN divergence. This cover does not newly prove the source direct exponential first-moment/mean1 SLLN route; that source route remains OPEN.'}
]
step_notes=[
 'Literal definitions and change target match the private Prop and source recurrence. Two conclusions refer to actual intervals/records; all finite values are NNReal and all possible infinities are WithTop.',
 'Parent76 supplies actual initialization/time monotonicity/guarded update; parent78 supplies AE finite-horizon escape. The three facts are internal results, not added public assumptions.',
 'Existence proof selects least k with t<T_k, proves k>0 using T0=0 and t>=0, sets n=k-1 and applies Nat.find minimality. This matches a frozen allowed route and correctly handles initialization predecessor.',
 'Symmetric monotonicity contradictions prove interval uniqueness with left<= and right<. No strict positive-wait assumption is needed, and equal adjacent times give empty intervals.',
 'Record_n=stopped would give T_n=top<=finite t, contradicted by finite<top. This links coverage to a genuine live record.',
 'The chosen record a is the actual inl branch; eventTime equals a.time and lower interval bound gives a.time<=t. No independently chosen state or time is substituted.',
 'Next wait top implies every finite t-a.time is below it. This preserves the last live arc and performs no phase/elapsed computation at infinity.',
 'For finite next wait q, guarded actual recurrence gives next time a.time+q and postbounce phase; t<that time and a.time<=t yield NNReal tsub<q. untopD0 is not used to create live updates from top.',
 'Uniqueness of the actual time/state pair follows from Sum.inl injectivity. This is uniqueness at a fixed record index, not a stochastic-process uniqueness theorem.'
]
lines=module.splitlines(keepends=True);covered=set();stepcov=[]
assert len(context['lesson']['steps'])==9
for i,s in enumerate(context['lesson']['steps']):
 rg=s['lean_source_region'];lo,hi=rg['start_line'],rg['end_line'];piece=''.join(lines[lo-1:hi]);assert piece==s['lean'];assert sha(piece.encode())==rg['exact_code_raw_sha256'];assert rg['source_raw_sha256']==context['file'];covered.update(range(lo,hi+1));stepcov.append({'step':i+1,'title':s['title'],'line_interval':[lo,hi],'exact_current_body_region_equal':True,'region_raw_sha256':rg['exact_code_raw_sha256'],'formula_checked':True,'prose_checked':True,'semantic_evidence':step_notes[i]})
assert covered==set(range(81,211))
node_status={
 'G79-1':('covered-literal-context','Whole private Prop/module retain literal center/residual/flow/bounce/rate and six source-standing conditions; no positive-dimension or higher-derivative premise.'),
 'G79-2':('covered-by-input-parent-not-extra-premise','UnitExponentialProduct full BODY realizes IID Exp1 and simultaneous positivity/raw-clamp equality. Cover does not use strict wait positivity directly; parent78 carries required AE escape.'),
 'G79-3':('covered-literal-and-parent','Record initialization is literal Nat.rec inl(0,z0); parent76 BODY hrec0 and htime gives T0=0. Current BODY133-142 uses T0 for first-crossing predecessor.'),
 'G79-4':('covered-literal-and-parent','Current literal hit clock/next record match A.1/A.2. Parent76 BODY proves guarded branch characterization; current finite-wait BODY190-207 invokes that exact actual update.'),
 'G79-5':('covered-literal-and-parent','Current stop branch is absorbing Sum.inr and eventTime=top with no phase. Parent76 hbranches/hstopped justify it. Current187-189 keeps the last live record elapsed below top.'),
 'G79-6':('covered-by-parent-relevant-subfacts-used','Parent76 BODY hmono/hstopped/hstrictevent and active eliminator supply monotonicity/absorption/strict finite transitions for positive clocks. Current BODY135-136 uses monotonicity,168-186 finite-time/live record; strict wait fact is available upstream but not a new binder/dependency needed for disjoint intervals.'),
 'G79-7':('covered-through-actual-nonaccumulation-parent','Parent78 entire BODY inspected: zero-cap first-stop/absorption and positive-cap clock-sum bound yield AE escape and finite bounded-horizon index sets. Current131-140 uses escape only. Original direct Exp moment route is OPEN; parent uses explicitly declared indicator-SLLN OR-route.'),
 'G79-8':('covered-equivalent-frozen-route','Current138-158 uses the independently frozen least-crossing alternative, not greatest-sublevel max: escape supplies crossing, T0 rules out k0, minimality bounds predecessor, and successor gives strict upper endpoint.'),
 'G79-9':('covered','Current159-167 proves unique half-open index by monotone disjointness;168-186 recovers actual live record with finite time;208-210 proves uniqueness of that record.'),
 'G79-10':('covered','Current187-207 separately treats infinite next wait and finite wait, verifies stored time<=physical t and NNReal elapsed<literal next wait. Source final live arc is preserved at every finite offset, without evaluating infinity.'),
 'G79-11':('partial-open-explicit-scope','Literal record0=(0,z0), T0=0 and finite next postbounce record are retained. Half-open conventions prevent overlap. This module does NOT compose a physical-time phase function, selected index(t0)=0, Phi0 physical initialization, or interpolation endpoint identities; these remaining source claims stay OPEN and are explicitly outside current binding.')
}
nodecov=[dict(n,status=node_status[n['id']][0],review_evidence=node_status[n['id']][1]) for n in graph['nodes']]
edgecov=[]
for e in graph['edges']:
 a,b=e['ingredient'],e['consumer'];status='partial-open-physical-initialization-interpolation' if b=='G79-11' else ('covered-through-parent-or-equivalent-route')
 edgecov.append(dict(e,status=status,review_evidence=node_status[b][1]))
# Each independent scoped item remains individually visible, including excluded
# and only-partly-admitted source clauses; no all-covered badge is synthesized.
itemcov=[]
for item in inventory['exhaustive_scoped_coverage']:
 anchor=item['anchor'];cls=item['classification']
 if cls.startswith('EXCLUDED'):
  status='excluded-scope-preserved';ev=item['reason']
 elif anchor=='A1.SS1.p2.2:between-jumps sentence':
  status='partial-interval-live-elapsed-only';ev='Current interval/live/elapsed conclusion supplies the source allowed domain; assignment zeta_(T_n+u)=Phi_u(zeta_Tn) as a global physical-time phase is not composed and stays OPEN.'
 elif anchor=='A1.SS1.p3.7:unique-process-for-all-times clause':
  status='partial-bounded-adapter-only';ev='Only unique interval/live record and elapsed bound admitted. Global stochastic process uniqueness/measurability remains OPEN.'
 elif anchor=='A1.SS1.p3.1-p3.6/A1.Ex4-Ex9':
  status='reused-parent-boundary-not-new-proof-credit';ev=node_status['G79-7'][1]
 elif anchor=='A1.SS1.p3.7:SLLN/nonaccumulation clauses':
  status='reused-nonaccumulation-with-original-stochastic-route-open';ev=node_status['G79-7'][1]
 elif anchor=='A1.SS1.p2.1':
  status='covered-initial-recursion-and-input-parent';ev='Literal record0/T0/source clock reindexing retained and product parent realizes inputs. Explicit selected physical index(t0)=0 is outside this module result.'
 elif anchor in ['A1.Ex2','alg1.l5/S3.E8']:
  status='covered-literal-flow-but-interpolation-open';ev='Literal harmonic flow/ODE source objects retained. No global interpolated physical-time phase is asserted by this adapter.'
 elif anchor in ['alg1.l7','A1.E2']:
  status='covered-actual-postbounce-recurrence-but-physical-endpoint-identity-open';ev='Exact finite postbounce next-record recurrence is retained and used. Physical-time phase assignment at the jump endpoint is a later composed claim.'
 else:
  status='covered-source-context-or-literal-parent';ev='Compared directly to frozen primary inventory, whole current private Prop/module and actual parent76/78 definitions/BODY; same source item, without replacing it by an external certificate.'
 itemcov.append(dict(item,review_status=status,review_evidence=ev))
assert len(itemcov)==28 and len(nodecov)==11 and len(edgecov)==20
inputs=[SOURCE,PACK,OUT/'fresh_primary79.py',OUT/'freeze_source79.py',OUT/'source_inventory79.json',OUT/'source_proof_graph79.json',OUT/'source_freeze79.md',OUT/'source_freeze79.seal.json',MODULE,ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean',ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
inputrows=[{'path':str(f),'raw_sha256':sha(f.read_bytes())} for f in inputs]
# Retain a byte-for-byte snapshot of the supplied reviewed module as private run evidence.
(OUT/'current-module.packet-snapshot79.lean').write_bytes(module.encode('utf-8'))
chronology={'source_first_freeze_created_utc':seal['created_utc'],'source_first_seal_raw_sha256':sha((OUT/'source_freeze79.seal.json').read_bytes()),'source_first_seal_original_unchanged':True,'primary_read_first_before_any79_candidate_header_implementation_or_review':True,'fresh_stdlib_parser_used_before_freeze':True,'candidate_packet_first_read_only_after_freeze':True,'packet_filesystem_mtime_utc':datetime.datetime.fromtimestamp(PACK.stat().st_mtime,datetime.timezone.utc).isoformat(),'final_review_created_utc':now,'primary_only_scope_phase':'Original inventory and source topology were independently authored/sealed before edge79 candidate existence/access; final phase compared all frozen items/edges without rewriting them.'}
runpath=OUT/'source-review.run-evidence79.json';manifestpath=OUT/'source-review.run-manifest79.json';resultpath=OUT/'source-review.result79.json'
run={'schema_version':1,'reviewer':'/root/fresh_source78','role':'independent anti-anchored source reviewer edge79','created_utc':now,'chronology':chronology,'raw_inputs':inputrows,'canonical_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'full_module_sha256':context['file'],'source_graph_raw_sha256':sha((OUT/'source_proof_graph79.json').read_bytes()),'scope_admission':'Only interval/live-record/elapsed adapter; source initialization/interpolation and full global-process obligations remain OPEN where not actually claimed/proved.','review_checks':['Seven semantic slots compared against fresh primary inventory and blind reconstruction','Entire private Prop/public theorem/imports/scoped context reviewed','Nine exact authored formula/BODY regions81-210 contiguous; actual parent76/78 entire BODY inspected','All28 independently frozen source items,11 nodes,20 ingredient edges individually classified','No prior verdict/header/extractor reviews or source-review78 consulted'],'hash_convention':'This immutable run-evidence file contains no hash of itself, result or final manifest. Final result review_run_sha256 is its exact RAW SHA256. Final manifest binds exact RAW hashes of all inputs and output files except manifest itself, so no circular/selfinclude hash exists.'}
runpath.write_text(json.dumps(run,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
result={
 'schema_version':1,'reviewer':'/root/fresh_source78','review_scope':'edge79 independent source review only','independent_from_formalizer':True,'independent_from_decoder':True,
 'reviewer_packet_sha256':packet['packet_sha256'],'reviewer_packet_raw_sha256':sha(PACK.read_bytes()),'publication_binding_sha256':packet['publication_binding_sha256'],'full_module_sha256':context['file'],'lean_statement_sha256':packet['lean']['statement_sha256'],
 'semantic_slots':slots,'deltas':deltas,'verdict':'equivalent-after-elaboration','repairs':[],'no_required_mathematical_repairs':True,
 'review_evidence':'Primary-first immutable source freeze preceded candidate existence/access. Independently compared all seven slots, all28 source inventory items, all11 source graph nodes/all20 edges, whole exact current module including private Prop/imports/scoped parameters, actual76/78 parent BODY and all9 authored formula/BODY regions. No blocking source/math delta for the explicitly bounded interval/live-record/elapsed adapter. Original direct exponential moment route and physical-time initialization/interpolation/global process claims remain OPEN rather than falsely marked source-complete. Separate Lean/fake-closure/aggregate/publication/source admission remains the coordinator/verifier obligation.',
 'independence':{'formalizer':'root-samplinglib-writer','blind_decoder':'/root/blind_decoder79','source_reviewer':'/root/fresh_source78','source_inventory_frozen_independently_before_candidate':True,'previous79_verdicts_seen':False,'candidate_header_or_prior_extractor_reviews_seen':False,'source_review78_consulted':False,'audit_cell_or_adoption_reports_consulted':False,'candidate_claims_treated_as_untrusted':True,'no_production_audit_ledger_cell_edits':True,'no_VERIFIED_transition':True,'chronology':chronology},
 'source_graph_coverage':{'frozen_source_inventory_raw_sha256':sha((OUT/'source_inventory79.json').read_bytes()),'frozen_source_graph_raw_sha256':sha((OUT/'source_proof_graph79.json').read_bytes()),'every_inventory_item_compared':True,'inventory_item_count':28,'inventory_items':itemcov,'every_node_compared':True,'nodes':nodecov,'every_ingredient_edge_compared':True,'edges':edgecov,'all_source_steps_claimed_complete':False,'bounded_admission':'Actual unique half-open interval/live finite record/nonnegative finite elapsed coverage only','open_source_nodes':['G79-11 physical-time initial index/phase and interpolation endpoint identities'],'original_source_route_open':'Direct exponential finite first-moment/mean1 SLLN route in upstream nonaccumulation; declared bounded-indicator sufficient alternative used instead.','missing_required_nodes_for_bounded_target':[]},
 'authored_step_coverage':{'entire_current_module_checked':True,'private_statement_is_meaningful_not_fake_closure':True,'private_statement_and_body_change_target_match':True,'step_count':9,'proof_body_line_interval':[81,210],'covered_line_count':130,'gaps':[],'exact_module_and_region_hashes_checked':True,'steps':stepcov},
 'truth_boundary':{'source_facts_retained':['Standing six analytic conditions including Section2.2 eta scale','Literal actual integrated-hazard stopped recurrence and source E_(n+1) index','T0=0/record0 initial live phase','Finite next record is literal flow then bounce; empty hit set stops next record','Source half-open arc convention and final infinite waiting-time live arc'], 'ASTIS_adapter_admitted':['Least first-crossing predecessor gives unique half-open interval for every finite t on actual AE nonaccumulation event','Finite lower endpoint identifies unique genuine live stored record with time<=t','NNReal elapsed equals ordinary finite nonnegative duration and is below actual next wait, including wait=infinity'], 'remains_open_or_excluded':['Explicit selected index(t=0)=0 and physical phase(t=0)=z0 identities','Composition of global physical-time phase/interpolation formula and endpoint phase identities','Measurable selector/jointly measurable process/path regularity/global process uniqueness','Source direct exponential first-moment/mean1 SLLN expansion','Arbitrary-probability-carrier transport theorem','Memoryless/time-homogeneous Markov/invariance/kernel/semigroup/hypocoercivity','PBPS main accuracy/implementation error/expected query costs or PBPS-SPHMC composition','Aggregate gates, VERIFIED, merged/stabilized/purified/live/full-paper/Goal completion'], 'no_required_mathematical_repairs':True},
 'compiler_boundary':{'packet_reports_compiled':packet['lean']['compiled'],'source_reviewer_reran_compiler':False,'pinned_toolchain':(ROOT/'lean-toolchain').read_text().strip(),'meaning':'Source fidelity and complete authored topology review only. Do not treat this as independent compiler/axiom/fake-closure or aggregate verification.'},
 'input_artifacts':inputrows,'review_run_sha256':sha(runpath.read_bytes()),'review_run_artifact':str(runpath),'run_manifest_path':str(manifestpath)
}
resultpath.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Exact RAW hashes for every emitted file, without a manifest/result circularity.
outputrows=[]
for f in sorted(OUT.rglob('*')):
 if f.is_file() and f!=manifestpath:outputrows.append({'path':str(f),'raw_sha256':sha(f.read_bytes())})
manifest={'schema_version':1,'created_utc':now,'reviewer':'/root/fresh_source78','hash_convention':'Every input/output file is bound by exact RAW SHA256. Only this manifest omits its own hash. The result review_run_sha256 binds standalone immutable run-evidence, which excludes itself/result/manifest. No normalized or canonical hash substitutes for raw input/output evidence. Canonical packet/publication hashes are separate metadata.','chronology':chronology,'raw_inputs':inputrows,'raw_outputs':outputrows,'self_output':{'path':str(manifestpath),'raw_sha256':'omitted-self-hash; return externally to coordinator'},'canonical_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'full_module_sha256':context['file']}
manifestpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(sha((OUT/n).read_bytes())==h for n,h in seal['files'].items())
assert all(sha(Path(x['path']).read_bytes())==x['raw_sha256'] for x in manifest['raw_inputs']+manifest['raw_outputs'])
assert json.loads(resultpath.read_text())['review_run_sha256']==sha(runpath.read_bytes())
print(json.dumps({'verdict':result['verdict'],'blocking_deltas':0,'no_required_mathematical_repairs':True,'result':str(resultpath),'result_raw_sha256':sha(resultpath.read_bytes()),'run_evidence_raw_sha256':sha(runpath.read_bytes()),'manifest_raw_sha256':sha(manifestpath.read_bytes()),'full_module_sha256':context['file'],'source_coverage':'28 items,11 nodes,20 edges; G79-11 physical initialization/interpolation residual OPEN','authored_coverage':'9 exact formula/BODY regions, lines81-210,130 lines,no gaps'},indent=2))
